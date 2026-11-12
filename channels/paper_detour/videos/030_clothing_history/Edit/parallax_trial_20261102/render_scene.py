import json
import sys
import time
from math import cos, pi
from pathlib import Path

from depthflow.scene import DepthScene

ROOT = Path(__file__).resolve().parent
SHOTLIST = ROOT.parent.parent / "Storyboard" / "SHOTLIST_v06.json"
ZOOM = float(sys.argv[2]) if len(sys.argv) > 2 else 0.90


class StrongParallax(DepthScene):
    def update(self):
        ease = (1 - cos(pi * self.tau)) / 2
        self.state.height = 0.26
        self.state.steady = 0.0
        self.state.sticky = True
        self.state.zoom = ZOOM
        self.state.offset = (-0.22 + 0.44 * ease, 0.0)


def main():
    index = int(sys.argv[1])
    entry = json.loads(SHOTLIST.read_text())[index - 1]
    frames = entry["endFrame"] - entry["startFrame"]
    source = Path(entry["framed_path"])
    if not source.is_file() or frames <= 0:
        raise ValueError(f"Invalid source or duration: {source}, {frames}")
    output = ROOT / (f"wide_{index:02d}.mp4" if len(sys.argv) > 2 else f"scene_{index:02d}.mp4")
    start = time.monotonic()
    scene = StrongParallax(backend="headless")
    scene.input(image=str(source))
    scene.main(output=str(output), fps=30, time=frames / 30,
               width=1920, height=1080, quality=80, ssaa=1, turbo=False)
    print(json.dumps({"scene": index, "frames": frames, "output": str(output),
                      "wall_seconds": round(time.monotonic() - start, 2)}), flush=True)


if __name__ == "__main__":
    main()
