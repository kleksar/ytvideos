#!/usr/bin/env python3
"""Hold a per-machine advisory lock while editing a shared ChatGPT composer."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


def save_state(path, state):
    fd, name = tempfile.mkstemp(prefix='.composer-state-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as out:
            json.dump(state, out, separators=(',', ':'))
            out.flush()
            os.fsync(out.fileno())
        os.replace(name, path)
        directory_fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def controlled(lock_path, task_id):
    """Cooperative protocol: browser observations are provided by the caller."""
    state_path = Path(str(lock_path) + '.state.json')
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            print('NEEDS_INSPECTION unreadable state', flush=True)
            return 4
        if not isinstance(state, dict):
            print('NEEDS_INSPECTION invalid state', flush=True)
            return 4
        if state.get('partial_holds'):
            print('NEEDS_INSPECTION use composer_recovery.py for partial holds', flush=True)
            return 4
        if state.get('version') == 2 and state.get('status') not in ('verified', 'inspected', 'resolved'):
            print('NEEDS_INSPECTION use composer_recovery.py', flush=True)
            return 4
        if state.get('status') not in ('verified', 'inspected', 'resolved'):
            print('NEEDS_INSPECTION ' + json.dumps(state, separators=(',', ':')), flush=True)
            if sys.stdin.readline().strip() != 'INSPECTED':
                return 4
            # Caller must first inspect both the original conversation and composer.
            save_state(state_path, {'status': 'inspected', 'task_id': task_id,
                                    'prior_task_id': state.get('task_id'),
                                    'prompt_sha256': state.get('prompt_sha256')})
            print('INSPECTION_RECORDED', flush=True)
    print('READY', flush=True)
    pending = False
    for line in sys.stdin:
        parts = line.strip().split()
        if len(parts) == 2 and parts[0] == 'PENDING' and re.fullmatch(r'[0-9a-f]{64}', parts[1]) and not pending:
            save_state(state_path, {'status': 'pending', 'task_id': task_id, 'prompt_sha256': parts[1]})
            pending = True
            print('PENDING_RECORDED', flush=True)
        elif parts == ['VERIFIED'] and pending:
            save_state(state_path, {'status': 'verified', 'task_id': task_id})
            print('LOCK_RELEASED verified', flush=True)
            return 0
        elif parts == ['UNCERTAIN'] and pending:
            print('LOCK_RELEASED needs inspection', flush=True)
            return 4
        else:
            print('INVALID_COMMAND', flush=True)
    # EOF, interruption, or crash never erases an unresolved pending state.
    return 4 if pending else 0


def default_lock_path() -> Path:
    override = os.environ.get("YTVIDEOS_CHATGPT_SESSION_LOCK")
    if override:
        return Path(override)
    return Path(tempfile.gettempdir()) / "ytvideos-chatgpt-composer.lock"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True, help="Short task identifier; do not include prompt text")
    parser.add_argument('--controlled', action='store_true', help='Use stdin PENDING/VERIFIED protocol')
    args = parser.parse_args(argv)
    task_id = args.task_id.strip()
    if not task_id or any(ch in task_id for ch in "\r\n\0"):
        parser.error("--task-id must be a non-empty single-line identifier")

    path = default_lock_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, "r+", encoding="utf-8") as lock_file:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            lock_file.seek(0)
            previous = lock_file.read().strip()
            print(f"LOCK_BUSY {previous or '{}'}", file=sys.stderr, flush=True)
            return 3

        metadata = {
            "task_id": task_id,
            "pid": os.getpid(),
            "acquired_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        lock_file.seek(0)
        lock_file.truncate()
        json.dump(metadata, lock_file, separators=(",", ":"))
        lock_file.flush()
        os.fsync(lock_file.fileno())
        if not args.controlled:
            # Legacy callers must not see LOCK_ACQUIRED before state validation.
            state_path = Path(str(path) + '.state.json')
            if state_path.exists():
                try:
                    state = json.loads(state_path.read_text(encoding='utf-8'))
                    if not isinstance(state, dict) or state.get('partial_holds') or state.get('status') not in ('verified', 'inspected', 'resolved'):
                        raise ValueError('unresolved state')
                except (OSError, ValueError):
                    print('NEEDS_INSPECTION use --controlled', flush=True)
                    return 4
        print(f"LOCK_ACQUIRED {json.dumps(metadata, separators=(',', ':'))}", flush=True)
        try:
            if args.controlled:
                return controlled(path, task_id)
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            print("LOCK_RELEASED", flush=True)
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
