"""Record a cold evaluator's actual shell command, output and exit status."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

base = Path(__file__).resolve().parent
name, command = sys.argv[1:3]
directory = base / name
if directory.parent != base or not directory.is_dir():
    raise SystemExit('Unknown isolated trial')
started = time.monotonic()
trial_env = {**os.environ, 'YTV_DATABASE_URL': str(directory / '.ytvideos/state.sqlite3'),
             'YTV_WORKSPACE': str(directory / '.ytvideos')}
result = subprocess.run(command, cwd=directory, shell=True, executable='/bin/bash', text=True, env=trial_env,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
record = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'command': command,
          'exit_code': result.returncode, 'seconds': time.monotonic() - started,
          'stdout': result.stdout, 'stderr': result.stderr}
with (base / (name + '-commands.jsonl')).open('a') as output:
    output.write(json.dumps(record, ensure_ascii=False) + '\n')
print(result.stdout, end='')
print(result.stderr, end='', file=sys.stderr)
raise SystemExit(result.returncode)
