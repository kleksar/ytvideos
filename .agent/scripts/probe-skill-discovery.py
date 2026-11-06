#!/usr/bin/env python3.11
"""Probe native Codex discovery only: no thread/start, turn/start or model calls."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import select
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cwd', action='append', help='Project-relative entry point; default: all registered directories')
parser.add_argument('--output', required=True, help='Project-relative JSON evidence file')
args = parser.parse_args()
expected = {p.parent.name for p in (ROOT / '.agents/skills').glob('*/SKILL.md')}
if args.cwd:
    cwds = [str(ROOT / p) for p in args.cwd]
else:
    registry = json.loads((ROOT / '.agent/episode-registry.json').read_text())
    entries = registry.get('episodes', registry.get('entries'))
    inventory = json.loads((ROOT / '.agent/entrypoints.json').read_text())
    cwds = [str(ROOT / p) for p in inventory['managed_entrypoints']]
cwds = list(dict.fromkeys(cwds))
for cwd in cwds:
    assert Path(cwd).is_dir() and Path(cwd).is_relative_to(ROOT), cwd
output = ROOT / args.output
assert output.is_relative_to(ROOT / '.agent'), 'Evidence must remain in .agent'
version = subprocess.check_output(['codex', '--version'], text=True).strip()
process = subprocess.Popen(['codex', 'app-server', '--stdio'], stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)


def send(data):
    process.stdin.write(json.dumps(data) + '\n')
    process.stdin.flush()


def response(identifier):
    deadline = time.monotonic() + 45
    while time.monotonic() < deadline:
        if not select.select([process.stdout], [], [], max(0, deadline - time.monotonic()))[0]:
            break
        line = process.stdout.readline()
        if not line:
            raise RuntimeError('Native app-server closed before response')
        message = json.loads(line)
        if message.get('id') == identifier:
            if 'error' in message:
                raise RuntimeError(message['error'])
            return message['result']
    raise TimeoutError('Native app-server response')


try:
    send({'id': 1, 'method': 'initialize', 'params': {'clientInfo': {
        'name': 'ytvideos_skill_audit', 'title': 'Read-only local skill audit', 'version': '1.0'}}})
    response(1)
    send({'method': 'initialized', 'params': {}})
    send({'id': 2, 'method': 'skills/list', 'params': {'cwds': cwds, 'forceReload': True}})
    data = response(2)
    rows = []
    for item in data['data']:
        skills = []
        for skill in item['skills']:
            if not skill.get('name', '').startswith('ytv-'):
                continue
            filtered = {k: skill.get(k) for k in ('name', 'path', 'scope', 'enabled', 'policy')}
            actual = Path(skill['path']).resolve()
            target = ROOT / '.agents/skills' / skill['name'] / 'SKILL.md'
            filtered['resolved_path'] = str(actual)
            filtered['canonical_match'] = actual == target.resolve()
            skills.append(filtered)
        enabled = {s['name'] for s in skills if s['enabled']}
        duplicates = sorted(n for n, count in Counter(s['name'] for s in skills).items() if count > 1)
        row = {'cwd': item['cwd'], 'skills': skills, 'missing': sorted(expected - enabled),
               'duplicates': duplicates, 'errors': item.get('errors', [])}
        row['pass'] = not (row['missing'] or duplicates or row['errors']) and all(s['canonical_match'] for s in skills)
        rows.append(row)
    result = {'runtime': version, 'method': 'skills/list', 'forceReload': True,
              'no_thread_or_turn_started': True, 'implicit_model_selection_tested': False,
              'skill_file_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                    for p in sorted((ROOT / '.agents/skills').glob('*/SKILL.md'))},
              'pass': len(rows) == len(cwds) and all(row['pass'] for row in rows), 'cwds': rows}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    for row in rows:
        print(Path(row['cwd']).relative_to(ROOT), 'PASS' if row['pass'] else 'FAIL',
              f"skills={len(row['skills'])} missing={len(row['missing'])} duplicates={len(row['duplicates'])} errors={len(row['errors'])}")
finally:
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
raise SystemExit(0 if result['pass'] else 1)
