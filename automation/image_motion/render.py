"""One DepthScene per process; run.py owns caching and final frame validation."""
import json
import math
import sys
from pathlib import Path
from importlib.metadata import version

import numpy as np
from PIL import Image
from depthflow.estimators.anything import DepthAnythingV2

if version("depthflow") != "1.0.1":
    raise RuntimeError("This renderer requires depthflow==1.0.1")


def depth(image, output):
    values = DepthAnythingV2(model="small").estimate(np.array(Image.open(image).convert("RGB")))
    temporary = output.with_suffix(".tmp.npy")
    np.save(temporary, values)
    temporary.replace(output)


def render(job):
    from depthflow.scene import DepthScene

    class Parallax(DepthScene):
        def update(self):
            self.state.height = job["preset"]["height"]
            self.state.steady = job["preset"]["steady"]
            self.state.sticky = job["preset"]["sticky"]
            self.state.zoom = job["depth_zoom"]
            # Positive sign means visible foreground travels LEFT (verified in030).
            self.state.offset = (-job["sign"] * job["preset"]["offset"] *
                                 math.cos(math.pi * self.tau), 0.0)

    values = np.load(job["depth"], allow_pickle=False)
    if values.ndim != 2 or not np.isfinite(values).all() or values.max() <= values.min():
        raise ValueError("Depth must be a finite, nonconstant 2D float .npy map")
    image_size = Image.open(job["image"]).size
    if abs(image_size[0]/image_size[1] - job["width"]/job["height"]) > .015:
        raise ValueError("Prepare an approved image with the timeline aspect ratio before rendering")
    scene = Parallax(backend="headless")
    scene.input(image=job["image"], depth=values)
    scene.main(output=job["raw"], fps=job["fps"], time=job["frames"] / job["fps"],
               width=job["width"], height=job["height"], quality=80, ssaa=1, turbo=False)


if __name__ == "__main__":
    if sys.argv[1] == "depth":
        depth(Path(sys.argv[2]), Path(sys.argv[3]))
    elif sys.argv[1] == "render":
        render(json.loads(Path(sys.argv[2]).read_text()))
    else:
        raise SystemExit("Expected depth or render")
