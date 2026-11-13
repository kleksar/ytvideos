"""Capture actual cold-session shell output without changing command semantics."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
import time

directory = Path(__file__).resolve().parent / "luna-provided"
command = sys.argv[1]
started = time.monotonic()
result = subprocess.run(command, cwd=directory, shell=True, executable="/bin/bash", text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
record = {"at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "command": command,
          "exit_code": result.returncode, "seconds": time.monotonic() - started,
          "stdout": result.stdout, "stderr": result.stderr}
with (directory.parent / "luna-provided-commands.jsonl").open("a") as output:
    output.write(json.dumps(record, ensure_ascii=False) + "\n")
print(result.stdout, end="")
print(result.stderr, end="", file=sys.stderr)
raise SystemExit(result.returncode)
