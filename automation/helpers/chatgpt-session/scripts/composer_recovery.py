#!/usr/bin/env python3
"""Cooperative, fail-closed journal for a shared browser composer.

Browser observations and UI actions remain the caller's responsibility.
Protocol is JSON lines over stdin after lock acquisition. Never manages the UI.
"""
import argparse
import fcntl
import hashlib
import json
import os
import select
from pathlib import Path
import sys
import tempfile
import time
import uuid


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def save(path, data):
    fd, name = tempfile.mkstemp(prefix='.composer-journal-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
        d = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(d)
        finally:
            os.close(d)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def emit(event, **kwargs):
    print(json.dumps({'event': event, **kwargs}, ensure_ascii=False), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--wait-seconds', type=float, default=0, help='Wait up to 60 seconds for a cooperating lock')
    parser.add_argument('--wait', action='store_true', help='Wait until available; cancel by closing stdin')
    parser.add_argument('--activation-seconds', type=float, default=60, help='Unused grant deadline, at most 60 seconds')
    a = parser.parse_args()
    if not 0 <= a.wait_seconds <= 60:
        parser.error('--wait-seconds must be between 0 and 60')
    if a.wait and a.wait_seconds:
        parser.error('--wait and --wait-seconds cannot be combined')
    if not 0 < a.activation_seconds <= 60:
        parser.error('--activation-seconds must be greater than zero and at most 60')
    if not a.task_id.strip() or any(c in a.task_id for c in '\r\n\0'):
        parser.error('invalid task ID')
    lock = Path(os.environ.get('YTVIDEOS_CHATGPT_SESSION_LOCK', str(Path(tempfile.gettempdir()) / 'ytvideos-chatgpt-composer.lock')))
    state = Path(str(lock) + '.state.json')
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, 'r+', encoding='utf-8') as f:
        deadline = time.monotonic() + a.wait_seconds
        waiting_announced = False
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if a.wait:
                    if not waiting_announced:
                        emit('WAITING'); waiting_announced = True
                    readable, _, _ = select.select([sys.stdin], [], [], 0.1)
                    if readable:
                        data = os.read(sys.stdin.fileno(), 4096)
                        emit('CANCELLED' if not data else 'EARLY_INPUT')
                        return 0 if not data else 4
                else:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        f.seek(0)
                        emit('LOCK_BUSY', owner=f.read())
                        return 3
                    time.sleep(min(0.1, remaining))
        if a.wait:
            # No UI work is permitted until a live controller activates the grant.
            emit('GRANTED', activation_seconds=a.activation_seconds)
            activation_deadline = time.monotonic() + a.activation_seconds
            data = b''
            while b'\n' not in data:
                remaining = activation_deadline - time.monotonic()
                if remaining <= 0:
                    emit('ACTIVATION_TIMEOUT'); return 4
                readable, _, _ = select.select([sys.stdin], [], [], remaining)
                if not readable:
                    emit('ACTIVATION_TIMEOUT'); return 4
                chunk = os.read(sys.stdin.fileno(), 4096)
                if not chunk:
                    emit('CANCELLED'); return 0
                data += chunk
                if len(data) > 4096:
                    emit('INVALID_ACTIVATION'); return 4
            try:
                line, extra = data.split(b'\n', 1)
                if extra or json.loads(line) != {'op': 'activate'}:
                    raise ValueError('invalid activation')
            except (ValueError, UnicodeError):
                emit('INVALID_ACTIVATION'); return 4
        f.seek(0); f.truncate(); json.dump({'task_id': a.task_id, 'pid': os.getpid()}, f); f.flush(); os.fsync(f.fileno())
        try:
            current = json.loads(state.read_text(encoding='utf-8')) if state.exists() else None
        except (OSError, ValueError):
            emit('NEEDS_INSPECTION', reason='unreadable state'); return 4
        if current is not None and not isinstance(current, dict):
            emit('NEEDS_INSPECTION', reason='invalid state'); return 4
        holds = current.get('partial_holds', {}) if current else {}
        if not isinstance(holds, dict) or any(not isinstance(k, str) or not isinstance(v, dict) or not isinstance(v.get('operation_id'), str) for k, v in holds.items()):
            emit('NEEDS_INSPECTION', reason='invalid partial holds'); return 4
        # Upgrade the last legacy resolved recovery, without resurrecting an explicitly released hold.
        if current and current.get('version') == 2 and current.get('status') == 'resolved' and current.get('history') in ('partial', 'full') and not current.get('submission_hold_migrated'):
            key, op_id = current.get('prompt_sha256'), current.get('operation_id')
            audit = current.get('partial_hold_audit', [])
            if not isinstance(key, str) or len(key) != 64 or not isinstance(op_id, str) or not isinstance(audit, list):
                emit('NEEDS_INSPECTION', reason='invalid recovered submission state'); return 4
            if key not in holds and not any(isinstance(e, dict) and e.get('operation_id') == op_id and e.get('prompt_sha256') == key for e in audit):
                holds[key] = {'operation_id': op_id, 'chat': current.get('chat'), 'task_id': current.get('task_id'), 'history': current['history']}
            current['partial_holds'] = holds
            current['submission_hold_migrated'] = True
            save(state, current)
        active = current and current.get('status') not in ('verified', 'inspected', 'resolved')
        visible = {k: v for k, v in current.items() if k != 'prompt'} if active else None
        emit('NEEDS_INSPECTION' if active else 'READY', state=visible)
        for line in sys.stdin:
            try:
                cmd = json.loads(line)
                if not isinstance(cmd, dict): raise ValueError('object required')
                op = cmd.get('op')
                if op == 'prepare':
                    if active: raise ValueError('unresolved prior operation')
                    if cmd.get('initial_empty') is not True: raise ValueError('composer must have been observed empty')
                    chat, anchor, source = (cmd.get(k) for k in ('chat', 'history_anchor', 'prompt_file'))
                    if not all(isinstance(x, str) and x.strip() for x in (chat, anchor, source)):
                        raise ValueError('chat, history_anchor and prompt_file required')
                    raw = Path(source).read_bytes()
                    prompt = raw.decode('utf-8')
                    if not prompt: raise ValueError('empty prompt')
                    if digest(prompt) in holds:
                        emit('SUBMISSION_HOLD', prompt_sha256=digest(prompt), operation_id=holds[digest(prompt)]['operation_id'], history=holds[digest(prompt)].get('history', 'partial')); continue
                    current = {'version': 2, 'status': 'armed', 'operation_id': str(uuid.uuid4()),
                               'task_id': a.task_id, 'chat': chat, 'history_anchor': anchor,
                               'prompt': prompt, 'prompt_sha256': digest(prompt), 'initial_empty': True, 'partial_holds': holds, 'partial_hold_audit': (current or {}).get('partial_hold_audit', [])}
                    save(state, current); active = True
                    emit('PREPARED', operation_id=current['operation_id'], prompt_sha256=current['prompt_sha256'])
                elif op == 'inserted':
                    if not active or current.get('version') != 2 or current.get('status') != 'armed' or current.get('task_id') != a.task_id:
                        raise ValueError('not owner of armed operation')
                    if cmd.get('observed_text') != current['prompt'] or cmd.get('chat') != current['chat']:
                        raise ValueError('text or chat differs')
                    current['status'] = 'inserted'; save(state, current); emit('INSERTED')
                elif op == 'send_attempt':
                    if not active or current.get('status') != 'inserted' or current.get('task_id') != a.task_id:
                        raise ValueError('not owner of inserted operation')
                    if cmd.get('observed_text') != current['prompt'] or cmd.get('chat') != current['chat'] or cmd.get('history') != 'none':
                        raise ValueError('composer, chat or history not verified')
                    current['status'] = 'send_attempted'; save(state, current); emit('SEND_ATTEMPT_RECORDED')
                elif op == 'confirmed':
                    if not active or current.get('status') != 'send_attempted' or current.get('task_id') != a.task_id:
                        raise ValueError('not owner of attempted send')
                    if cmd.get('posted_text') != current['prompt'] or cmd.get('chat') != current['chat'] or cmd.get('composer_empty') is not True:
                        raise ValueError('posted text, chat or empty composer not verified')
                    current['status'] = 'verified'; current.pop('prompt', None); save(state, current)
                    emit('LOCK_RELEASED', result='verified'); return 0
                elif op == 'reconcile':
                    if not active or current.get('version') != 2: raise ValueError('no v2 operation to recover')
                    if cmd.get('chat') != current['chat'] or cmd.get('history') not in ('none', 'full', 'partial', 'unknown'):
                        raise ValueError('original chat and history assessment required')
                    # Exact full prompt only, after independently verified insertion; do not infer ownership of fragments.
                    known = (current.get('status') in ('inserted', 'send_attempted', 'clearing') and
                             cmd.get('observed_text') == current['prompt'] and
                             cmd.get('no_intervening_edit') is True)
                    if cmd['history'] in ('partial', 'full'):
                        holds[current['prompt_sha256']] = {'operation_id': current['operation_id'], 'chat': current['chat'], 'task_id': current['task_id'], 'history': cmd['history']}
                        current['partial_holds'] = holds
                    current['history'] = cmd['history']
                    current['recovery_task_id'] = a.task_id
                    if cmd['history'] == 'unknown':
                        save(state, current); emit('STOP', reason='unknown send status')
                    elif known:
                        current['status'] = 'clearing'; save(state, current)
                        emit('EXACT_AGENT_DRAFT', operation_id=current['operation_id'], history=cmd['history'],
                             instruction='Recheck exact text and ownership immediately before clearing; then verify empty.')
                    elif cmd.get('observed_text') == '' and cmd.get('composer_empty') is True:
                        current['status'] = 'resolved'; current.pop('prompt', None); save(state, current)
                        emit('RESOLVED', history=cmd['history'], instruction='Do not retry a partial or full submission.'); return 0
                    else:
                        save(state, current); emit('STOP', reason='draft not proven to be the exact recorded agent insertion')
                elif op == 'cleared':
                    if not active or current.get('status') != 'clearing' or current.get('recovery_task_id') != a.task_id:
                        raise ValueError('no authorized clear observation')
                    if cmd.get('composer_empty') is not True or cmd.get('chat') != current['chat']:
                        raise ValueError('empty composer and chat must be confirmed')
                    current['status'] = 'resolved'; current.pop('prompt', None); save(state, current)
                    emit('RESOLVED', history=current.get('history'), instruction='Do not retry a partial or full submission.'); return 0
                elif op == 'release_submission_hold':
                    if active: raise ValueError('resolve current operation first')
                    key, op_id, chat, reason = (cmd.get(k) for k in ('prompt_sha256', 'operation_id', 'chat', 'reason'))
                    if not isinstance(key, str) or key not in holds or holds[key].get('operation_id') != op_id or holds[key].get('chat') != chat:
                        raise ValueError('hold identity mismatch')
                    if cmd.get('history_rechecked') is not True or not isinstance(reason, str) or not reason.strip():
                        raise ValueError('rechecked history and specific decision required')
                    # Retain an audit trail in the same atomic state document.
                    current = dict(current or {})
                    audit = current.get('partial_hold_audit', [])
                    if not isinstance(audit, list): raise ValueError('invalid audit')
                    audit.append({'prompt_sha256': key, 'operation_id': op_id, 'chat': chat, 'task_id': a.task_id, 'reason': reason})
                    del holds[key]
                    current.update(status='resolved', partial_holds=holds, partial_hold_audit=audit)
                    save(state, current)
                    emit('SUBMISSION_HOLD_RELEASED', prompt_sha256=key)
                else:
                    raise ValueError('unknown operation')
            except (ValueError, KeyError, OSError, UnicodeError, json.JSONDecodeError) as exc:
                emit('ERROR', reason=str(exc))
        return 4 if active else 0

if __name__ == '__main__':
    sys.exit(main())
