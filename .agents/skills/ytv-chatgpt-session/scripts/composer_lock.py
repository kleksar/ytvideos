#!/usr/bin/env python3
"""Hold a per-machine advisory lock while editing a shared ChatGPT composer."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


def default_lock_path() -> Path:
    override = os.environ.get("YTVIDEOS_CHATGPT_SESSION_LOCK")
    if override:
        return Path(override)
    return Path(tempfile.gettempdir()) / "ytvideos-chatgpt-composer.lock"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task-id", required=True, help="Short task identifier; do not include prompt text")
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
        print(f"LOCK_ACQUIRED {json.dumps(metadata, separators=(',', ':'))}", flush=True)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            print("LOCK_RELEASED", flush=True)
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
