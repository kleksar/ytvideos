"""Compare offline instruction bundles from two checkouts, without creating runs."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys


MEASURE = r'''
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
from ytvideos.context import instruction_packet
from ytvideos.entry import reading_packet

rows = []
for channel in ("paper_detour", "nuviko_history", "scenes_on_repeat"):
    for stage in ("research", "scene_image", "render"):
        packet = instruction_packet(Path.cwd(), channel=channel, stage=stage, format="short")
        packet.update(run_id="offline-measurement", task_id=stage, input_hash="offline-measurement",
                      task_guide={"goal": "Offline measurement only"})
        with tempfile.TemporaryDirectory() as temporary:
            result = reading_packet(SimpleNamespace(workspace=Path(temporary)), packet)
            task_file = Path(result["task_file"])
            payload = json.loads(task_file.read_text())
            rows.append({"channel": channel, "stage": stage,
                         "bundle_utf8_bytes": sum(p.stat().st_size for p in task_file.parent.rglob("*")
                                                  if p.is_file()),
                         "task_json_bytes": task_file.stat().st_size,
                         "duplicated_skill_text": "text" in payload["skill"]})
print(json.dumps(rows))
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    results = {}
    for label, root in (("baseline", args.baseline), ("candidate", args.candidate)):
        root = root.resolve()
        environment = {**os.environ, "PYTHONPATH": str(root / "src")}
        result = subprocess.run([sys.executable, "-c", MEASURE], cwd=root, env=environment,
                                capture_output=True, text=True, check=True)
        results[label] = json.loads(result.stdout)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
