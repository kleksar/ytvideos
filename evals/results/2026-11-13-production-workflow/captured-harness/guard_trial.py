"""Exercise the real hook process with explicitly simulated host events."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys

base = Path(__file__).resolve().parent
name, kind = sys.argv[1:3]
root = base / name
host = json.loads((base / (name + '-host.json')).read_text())
history_path = base / (name + '-host-events.jsonl')
history = [json.loads(line) for line in history_path.read_text().splitlines()] if history_path.exists() else []
prior_blocks = [item['output'] for item in history if item.get('output', {}).get('decision') == 'block']
event = {'hook_event_name': kind, 'session_id': host['session_id'], 'cwd': str(root),
         'model': 'gpt-6-luna', 'turn_id': host['turn_id']}
if kind == 'UserPromptSubmit':
    event['prompt'] = prior_blocks[-1]['reason'] if prior_blocks else (base / (name + '-prompt.txt')).read_text()
elif kind == 'Stop':
    event['stop_hook_active'] = bool(prior_blocks)
    answer = base / (name + '-output.txt')
    event['last_assistant_message'] = answer.read_text() if answer.exists() else ''
else:
    raise SystemExit('Use UserPromptSubmit or Stop for this explicit simulation')
process = subprocess.run(['uv', 'run', '--offline', '--no-sync', '--project', str(root),
                          'python', str(root / '.codex/hooks/entrypoint.py')],
                         cwd=root, input=json.dumps(event), text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, timeout=20,
                         env={**os.environ, 'CODEX_THREAD_ID': host['session_id'],
                              'YTV_DATABASE_URL': str(root / '.ytvideos/state.sqlite3'),
                              'YTV_WORKSPACE': str(root / '.ytvideos')})
record = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'host_mode': 'simulated_stop_lifecycle_not_live_hook_activation',
          'input': event, 'stdout': process.stdout, 'stderr': process.stderr, 'exit_code': process.returncode}
if process.returncode == 0:
    record['output'] = json.loads(process.stdout)
with history_path.open('a') as stream:
    stream.write(json.dumps(record, ensure_ascii=False) + '\n')
print(json.dumps(record, ensure_ascii=False, indent=2))
raise SystemExit(process.returncode)
