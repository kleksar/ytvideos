import json, subprocess, sys, datetime
cmd = sys.argv[1:]
p = subprocess.run(cmd, capture_output=True, text=True)
entry = {"time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "argv": cmd, "exit_code": p.returncode, "stdout": p.stdout, "stderr": p.stderr}
with open('/workspace/scratch/10ddda0bd015/cold-eval/trace.jsonl','a',encoding='utf-8') as f:
    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
sys.stdout.write(p.stdout); sys.stderr.write(p.stderr)
sys.exit(p.returncode)
