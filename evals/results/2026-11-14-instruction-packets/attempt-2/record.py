import json, subprocess, sys, time

cmd = sys.argv[1:]
p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
row = {"command": cmd, "stdout": p.stdout, "stderr": p.stderr, "exit_code": p.returncode, "ts": time.time()}
with open('/workspace/scratch/10ddda0bd015/cold-eval-final/trace.jsonl', 'a', encoding='utf-8') as f:
    f.write(json.dumps(row, ensure_ascii=False) + '\n')
sys.stdout.write(p.stdout)
sys.stderr.write(p.stderr)
sys.exit(p.returncode)
