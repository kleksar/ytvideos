#!/usr/bin/env python3
"""Explicit, immutable rule publications; no process control or instruction delivery."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
import time
import uuid


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        raise ValueError(f'Cannot read valid JSON {path}: {e}') from e


def safe_id(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', value):
        raise ValueError(f'Invalid identifier: {value!r}')
    return value


def atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.tmp-')
    try:
        with os.fdopen(fd, 'wb') as out:
            out.write(data); out.flush(); os.fsync(out.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()


def validate_change(c):
    required = {'id', 'summary', 'channels', 'formats', 'stages', 'impact', 'files'}
    if not isinstance(c, dict) or set(c) != required: raise ValueError('Invalid change fields')
    safe_id(c['id'])
    if not isinstance(c['summary'], str) or not c['summary'].strip(): raise ValueError('Empty summary')
    if c['impact'] not in ('future', 'review', 'hold', 'unclassified'): raise ValueError('Invalid impact')
    for key in ('channels', 'formats', 'stages'):
        if not isinstance(c[key], list) or not c[key] or any(not isinstance(x, str) or not x.strip() for x in c[key]): raise ValueError(f'Invalid {key}')
    if not isinstance(c['files'], list) or not c['files']: raise ValueError('No rule files')
    for name in c['files']:
        if not isinstance(name, str): raise ValueError('Invalid path')
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or str(p) != name: raise ValueError(f'Unsafe path: {name}')


def snapshot(store):
    pointer = read_json(store / 'current.json')
    if set(pointer) != {'generation', 'sha256'}: raise ValueError('Invalid current pointer')
    gen = safe_id(pointer['generation'])
    root = store / 'generations' / gen
    data = (root / 'manifest.json').read_bytes()
    if digest(data) != pointer['sha256']: raise ValueError('Manifest hash mismatch')
    m = json.loads(data)
    if set(m) != {'schema', 'generation', 'changes'} or m['schema'] != 1 or m['generation'] != gen or not isinstance(m['changes'], list): raise ValueError('Invalid manifest')
    ids = set()
    for entry in m['changes']:
        c = entry['change']; validate_change(c)
        if c['id'] in ids: raise ValueError('Duplicate change ID')
        ids.add(c['id'])
        if set(entry) != {'change', 'files'} or set(entry['files']) != set(c['files']): raise ValueError('Invalid file map')
        for name, sha in entry['files'].items():
            if not isinstance(sha, str) or not re.fullmatch(r'[0-9a-f]{64}', sha): raise ValueError('Invalid file hash')
            data = (root / 'files' / sha).read_bytes()
            if digest(data) != sha: raise ValueError(f'Corrupt snapshot: {name}')
    return m, pointer['sha256']


def publish(a):
    source = Path(a.source).resolve(strict=True); store = Path(a.store).resolve()
    proposed = read_json(Path(a.changes))
    if not isinstance(proposed, list) or not proposed: raise ValueError('Changes must be nonempty list')
    store.mkdir(parents=True, exist_ok=True)
    with (store / '.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        old = snapshot(store)[0]['changes'] if (store / 'current.json').exists() else []
        ids = {e['change']['id'] for e in old}; new = []; blobs = {}
        for c in proposed:
            validate_change(c)
            if c['id'] in ids: raise ValueError(f'Change ID already published: {c["id"]}')
            ids.add(c['id']); filemap = {}
            for name in c['files']:
                path = (source / name).resolve(strict=True)
                if not path.is_relative_to(source) or not path.is_file(): raise ValueError(f'Unsafe file: {name}')
                data = path.read_bytes(); sha = digest(data); filemap[name] = sha; blobs[sha] = data
            new.append({'change': c, 'files': filemap})
        # Detect edits during capture, including unsaved Git work; no commit is required.
        for entry in new:
            for name, sha in entry['files'].items():
                if digest((source / name).resolve(strict=True).read_bytes()) != sha: raise ValueError(f'File changed during capture: {name}')
        generation = f'{time.time_ns()}-{uuid.uuid4().hex[:8]}'
        root = store / 'generations' / generation
        root.mkdir(parents=True)
        for entry in old:
            for sha in entry['files'].values():
                blobs[sha] = (store / 'generations' / read_json(store / 'current.json')['generation'] / 'files' / sha).read_bytes()
        for sha, data in blobs.items(): atomic(root / 'files' / sha, data)
        manifest = encoded({'schema': 1, 'generation': generation, 'changes': old + new})
        atomic(root / 'manifest.json', manifest)
        atomic(store / 'current.json', encoded({'generation': generation, 'sha256': digest(manifest)}))
        print(f'Published {generation}, {len(new)} changes; source files were not modified.')


def matches(c, a):
    return c['impact'] == 'unclassified' or all('*' in c[k] or getattr(a, k[:-1]) in c[k] for k in ('channels', 'formats', 'stages'))


def ack_path(store, session):
    return store / 'ack' / (safe_id(session) + '.json')


def load_ack(path):
    if not path.exists(): return {}
    v = read_json(path)
    if not isinstance(v, dict) or any(not isinstance(k, str) or not isinstance(val, str) for k, val in v.items()): raise ValueError('Invalid acknowledgement')
    return v


def check(a):
    store = Path(a.store); m, mh = snapshot(store); ack = load_ack(ack_path(store, a.session)); pending = []
    for entry in m['changes']:
        c = entry['change']; fingerprint = digest(encoded(entry))
        if matches(c, a) and ack.get(c['id']) != fingerprint:
            pending.append({'id': c['id'], 'summary': c['summary'], 'impact': c['impact'], 'files': [{'source_path': name, 'snapshot_path': str((store / 'generations' / m['generation'] / 'files' / sha).resolve()), 'sha256': sha} for name, sha in entry['files'].items()]})
    print(json.dumps({'generation': m['generation'], 'manifest_sha256': mh, 'pending': pending}, ensure_ascii=False, indent=2))
    return 2 if pending else 0


def acknowledge(a):
    store = Path(a.store); path = ack_path(store, a.session)
    with (store / '.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        m, mh = snapshot(store)
        if mh != a.manifest_sha256: raise ValueError('Publication changed; check and read again')
        entries = {e['change']['id']: e for e in m['changes']}
        if not a.read_and_assessed: raise ValueError('Explicit --read-and-assessed required')
        if any(x not in entries for x in a.ids): raise ValueError('Unknown change ID')
        state = load_ack(path)
        for x in a.ids: state[x] = digest(encoded(entries[x]))
        atomic(path, encoded(state))
        print('Recorded explicit reading and assessment; no episode or approval was changed.')


def main():
    p = argparse.ArgumentParser(); subs = p.add_subparsers(dest='command', required=True)
    s = subs.add_parser('publish'); s.add_argument('--store', required=True); s.add_argument('--source', required=True); s.add_argument('--changes', required=True)
    s = subs.add_parser('check'); s.add_argument('--store', required=True); s.add_argument('--session', required=True); s.add_argument('--channel', required=True); s.add_argument('--format', required=True); s.add_argument('--stage', required=True)
    s = subs.add_parser('ack'); s.add_argument('--store', required=True); s.add_argument('--session', required=True); s.add_argument('--manifest-sha256', required=True); s.add_argument('--read-and-assessed', action='store_true'); s.add_argument('ids', nargs='+')
    a = p.parse_args()
    try:
        return {'publish': publish, 'check': check, 'ack': acknowledge}[a.command](a) or 0
    except (ValueError, OSError, KeyError, TypeError) as e:
        print(f'RULES CHECK ERROR: {e}', file=__import__('sys').stderr); return 1

if __name__ == '__main__': raise SystemExit(main())
