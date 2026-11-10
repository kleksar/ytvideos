#!/usr/bin/env python3
"""Wait for an exact unresolved journal operation without holding its lock.

A RETRY signal only means the caller should reacquire the normal lock and
recheck all state. It does not authorize a browser action or a resend.
"""
import argparse
import json
import os
from pathlib import Path
import select
import sys
import tempfile


def emit(event, **values):
    print(json.dumps({'event': event, **values}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--operation-id', required=True)
    parser.add_argument('--interval-seconds', type=float, default=1.0)
    args = parser.parse_args()
    if not args.operation_id.strip() or any(c in args.operation_id for c in '\r\n\0'):
        parser.error('invalid operation ID')
    if not 0.05 <= args.interval_seconds <= 60:
        parser.error('interval must be between 0.05 and 60 seconds')
    lock = Path(os.environ.get('YTVIDEOS_CHATGPT_SESSION_LOCK', str(Path(tempfile.gettempdir()) / 'ytvideos-chatgpt-composer.lock')))
    state = Path(str(lock) + '.state.json')
    emit('WAITING_FOR_RESOLUTION', operation_id=args.operation_id)
    while True:
        try:
            record = json.loads(state.read_text(encoding='utf-8'))
        except (OSError, ValueError):
            record = None
        if isinstance(record, dict):
            seen = record.get('operation_id')
            if isinstance(seen, str) and seen != args.operation_id:
                emit('STATE_CHANGED', instruction='Reacquire the normal lock and inspect; do not infer send outcome.')
                return 4
            if seen == args.operation_id and record.get('status') in ('verified', 'resolved'):
                emit('RETRY', instruction='Reacquire the normal lock and recheck state and browser; do not resend an uncertain request.')
                return 0
        try:
            readable, _, _ = select.select([sys.stdin], [], [], args.interval_seconds)
            if readable:
                data = os.read(sys.stdin.fileno(), 4096)
                emit('CANCELLED' if not data else 'EARLY_INPUT')
                return 0 if not data else 4
        except OSError:
            return 0

if __name__ == '__main__':
    sys.exit(main())
