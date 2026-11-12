import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
shots = json.loads((ROOT.parent.parent / "Storyboard/SHOTLIST_v06.json").read_text())
start = time.monotonic()
for n, shot in enumerate(shots, 1):
    output = ROOT / f"scene_{n:02}.mp4"
    if n != 1:
        with (ROOT / f"scene_{n:02}.log").open("w") as log:
            subprocess.run([sys.executable, str(ROOT / "render_scene.py"), str(n)],
                           stdout=log, stderr=subprocess.STDOUT, check=True)
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                            "-show_entries", "stream=width,height,r_frame_rate,nb_frames",
                            "-of", "json", str(output)], capture_output=True, text=True, check=True)
    data = json.loads(probe.stdout)["streams"][0]
    expected = shot["endFrame"] - shot["startFrame"]
    if (int(data["nb_frames"]) != expected or data["r_frame_rate"] != "30/1"
            or (data["width"], data["height"]) != (1920, 1080)):
        raise ValueError(f"Invalid video for scene {n}: {data}, expected {expected}")
    print(json.dumps({"completed": n, "frames": expected,
                      "elapsed": round(time.monotonic() - start, 1)}), flush=True)
