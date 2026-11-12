#!/usr/bin/env python3
"""Render one Pompeii still as 16:9 letterboxed clean parallax + opposed camera.

G08 is intentionally applied by automation/image_motion/apply_g08_layered.py
after this clean render. Source still and the original Palmier framing remain
available as dependencies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
import time

import numpy as np
from PIL import Image

W, H, FPS = 1920, 1080, 30
REFERENCE_WIDTH = 1672
FG_TRAVEL_REFERENCE_PX = 12.0
CAMERA_SCALE = 1.10
CAMERA_TRAVEL_FRACTION = 0.045


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fit_layers(foreground: Path, background: Path):
    fg = Image.open(foreground).convert("RGBA")
    bg = Image.open(background).convert("RGB")
    if fg.size != bg.size:
        raise ValueError(f"Layer dimensions differ: {fg.size} vs {bg.size}")
    src_w, src_h = fg.size
    fit_scale = min(W / src_w, H / src_h)
    dst_w = max(1, round(src_w * fit_scale))
    dst_h = max(1, round(src_h * fit_scale))
    x = (W - dst_w) // 2
    y = (H - dst_h) // 2

    bg_fit = bg.resize((dst_w, dst_h), Image.Resampling.LANCZOS)
    bg_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    bg_canvas.paste(bg_fit.convert("RGBA"), (x, y))

    fg_fit = fg.resize((dst_w, dst_h), Image.Resampling.LANCZOS)
    fg_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fg_canvas.alpha_composite(fg_fit, (x, y))
    return fg_canvas, bg_canvas, fit_scale, (src_w, src_h), (dst_w, dst_h), (x, y)


def choose_direction(mask: Path, scene: int) -> tuple[str, float]:
    alpha = np.asarray(Image.open(mask).convert("L")) > 127
    ys, xs = np.nonzero(alpha)
    if len(xs) == 0:
        raise ValueError(f"K{scene:03d}: empty segmentation mask")
    centroid = float(xs.mean() / alpha.shape[1])
    # Let the foreground travel toward the visual center; centered compositions
    # alternate to keep consecutive cuts from feeling mechanically identical.
    if centroid < 0.46:
        direction = "parallax-left-camera-right"
    elif centroid > 0.54:
        direction = "parallax-right-camera-left"
    else:
        direction = "parallax-left-camera-right" if scene % 2 == 0 else "parallax-right-camera-left"
    return direction, centroid


def render(foreground: Path, background: Path, mask: Path, output: Path,
           scene: int, frames: int) -> dict:
    start = time.monotonic()
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite {output}")
    fg, bg, fit_scale, src_size, fit_size, fit_xy = fit_layers(foreground, background)
    direction, centroid_x = choose_direction(mask, scene)
    # The image's accepted 12px foreground motion is scaled through contain fit.
    travel = FG_TRAVEL_REFERENCE_PX * fit_scale
    if frames < 2:
        raise ValueError("At least two frames required")
    left = direction == "parallax-left-camera-right"
    sign = 1 if left else -1
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="pompeii-clean-motion-") as tmp:
        raw = Path(tmp) / "parallax.mp4"
        set_bt709 = (
            "setparams=range=limited:color_primaries=bt709:"
            "color_trc=bt709:colorspace=bt709"
        )
        command = [
            "ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-vf",
            f"setsar=1,{set_bt709}", "-c:v", "libx264", "-crf", "16", "-preset", "fast",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709", "-color_range", "tv", "-an", str(raw),
        ]
        enc = subprocess.Popen(command, stdin=subprocess.PIPE)
        try:
            for frame in range(frames):
                dx = sign * travel * frame / (frames - 1)
                moved = fg.transform(
                    (W, H), Image.Transform.AFFINE, (1, 0, dx, 0, 1, 0),
                    resample=Image.Resampling.BICUBIC,
                )
                enc.stdin.write(Image.alpha_composite(bg, moved).tobytes())
            enc.stdin.close()
            if enc.wait() != 0:
                raise RuntimeError("Clean parallax encode failed")

            camera_sign = -1 if left else 1
            travel_px = W * CAMERA_TRAVEL_FRACTION
            expression = f"{camera_sign}*(-{travel_px / 2}+{travel_px}*on/{frames - 1})"
            camera_w, camera_h = round(W * CAMERA_SCALE), round(H * CAMERA_SCALE)
            crop_x = (camera_w - W) // 2
            crop_y = (camera_h - H) // 2
            vf = (
                f"scale={camera_w}:{camera_h}:flags=lanczos,"
                f"perspective=x0='{expression}':y0=0:x1='W+({expression})':y1=0:"
                f"x2='{expression}':y2=H:x3='W+({expression})':y3=H:"
                f"interpolation=cubic:eval=frame,crop={W}:{H}:{crop_x}:{crop_y},"
                f"setsar=1,{set_bt709}"
            )
            subprocess.run([
                "ffmpeg", "-v", "error", "-n", "-i", str(raw), "-vf", vf,
                "-frames:v", str(frames), "-c:v", "libx264", "-crf", "16", "-preset", "fast",
                "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-colorspace", "bt709", "-color_range", "tv", "-an", str(output),
            ], check=True)
        except BaseException:
            if enc.poll() is None:
                enc.kill()
            enc.wait()
            output.unlink(missing_ok=True)
            raise

    return {
        "scene": scene,
        "frames": frames,
        "fps": FPS,
        "output_size": [W, H],
        "source_size": list(src_size),
        "fit_size": list(fit_size),
        "fit_offset": list(fit_xy),
        "fit_scale": fit_scale,
        "foreground_travel_px": travel,
        "direction": direction,
        "mask_centroid_x": round(centroid_x, 5),
        "camera_scale": CAMERA_SCALE,
        "camera_travel_fraction": CAMERA_TRAVEL_FRACTION,
        "grain": "none in this stage; G08 is applied after camera",
        "foreground": str(foreground),
        "background": str(background),
        "mask": str(mask),
        "output": str(output),
        "source_hashes": {
            "foreground": sha256(foreground),
            "background": sha256(background),
            "mask": sha256(mask),
        },
        "elapsed_seconds": round(time.monotonic() - start, 3),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--foreground", type=Path, required=True)
    p.add_argument("--background", type=Path, required=True)
    p.add_argument("--mask", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--scene", type=int, required=True)
    p.add_argument("--frames", type=int, required=True)
    args = p.parse_args()
    print(json.dumps(render(args.foreground, args.background, args.mask, args.output,
                            args.scene, args.frames)))


if __name__ == "__main__":
    main()
