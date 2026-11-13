"""Freeze only source inputs for an isolated cold-session workflow evaluation."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

base = Path(__file__).resolve().parent
project = base.parent / 'ytvideos'
name = sys.argv[1]
destination = base / name
destination.mkdir()
paths = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=project).decode().split('\0')
manifest = {}
for relative in sorted(set(paths)):
    path = project / relative
    if not relative or not path.is_file() or relative.startswith(('tests/', 'evals/', 'output/', 'Work/')):
        continue
    if path.suffix not in {'.py', '.md', '.json', '.toml', '.lock', '.txt', '.yml', '.yaml'} and path.name != '.gitignore':
        continue
    target = destination / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(path, target)
    manifest[relative] = hashlib.sha256(target.read_bytes()).hexdigest()
record = {'case': name, 'source_files': manifest, 'code_sha256': hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()}
(base / (name + '-source.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
subprocess.run(['git', 'init', '-q', str(destination)], check=True)
subprocess.run(['git', 'add', '.'], cwd=destination, check=True)
subprocess.run(['git', '-c', 'user.name=Workflow Eval', '-c', 'user.email=workflow-eval@example.invalid', 'commit', '-qm', 'Isolated evaluated source'], cwd=destination, check=True)
print(json.dumps({'directory': str(destination), 'files': len(manifest), 'source_manifest_sha256': record['code_sha256']}))
