from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
BASE = Path("/Users/diplomat/ytvideos")
LAYERED = BASE / "automation/image_motion/layered_render.py"
G08 = BASE / "automation/image_motion/apply_g08_layered.py"
PROCESSING_PYTHON = BASE / "Shared/Image_Motion/Tools/sam2-local/.venv/bin/python"
MANIFEST = json.loads((ROOT / "vision_manifest.json").read_text())
PRE = ROOT / "motion_pre_g08"
FINAL = ROOT / "motion_g08"
PRE.mkdir(exist_ok=True)
FINAL.mkdir(exist_ok=True)
# Exact 179-frame exceptions read from Palmier's original still-image track;
# all remaining scene clips are 180 frames.
SHORT = {1, 8, 15, 23, 30, 37, 45, 52, 60, 67, 74, 82, 89, 96, 104, 111}
items = []
for rec in MANIFEST:
    scene = int(rec["scene"])
    image_path = Path(rec["image"])
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    fg_path = ROOT / "layers" / f"S{scene:03d}" / "foreground.png"
    bg_path = ROOT / "layers" / f"S{scene:03d}" / "background.png"
    alpha = np.asarray(Image.open(fg_path).getchannel("A"), dtype=np.float64) / 255
    yy, xx = np.mgrid[0:height, 0:width]
    total = max(float(alpha.sum()), 1.0)
    cx = float((xx * alpha).sum() / total) / max(width - 1, 1)
    cy = float((yy * alpha).sum() / total) / max(height - 1, 1)
    if cx > 0.55:
        direction = "parallax-left-camera-right"
    elif cx < 0.45:
        direction = "parallax-right-camera-left"
    else:
        direction = "parallax-left-camera-right" if scene % 2 else "parallax-right-camera-left"
    # The approved crop-safe 1.045 camera leaves 54 vertical pixels to place
    # the subject's visual center without clipping the head or feet.
    camera_height = round(1080 * 1.045)
    max_crop_y = camera_height - 1080
    crop_y = int(round(max(0.0, min(float(max_crop_y), cy * camera_height - 540))))
    items.append({
        "scene": scene, "image": str(image_path),
        "image_sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
        "frames": 179 if scene in SHORT else 180, "fps": 30,
        "foreground": str(fg_path), "background": str(bg_path),
        "mask_centroid_normalized": [round(cx, 5), round(cy, 5)],
        "direction": direction, "camera_scale": 1.045,
        "camera_travel_width_fraction": 0.045, "camera_crop_y": crop_y,
        "pre_g08": str(PRE / f"S{scene:03d}_pre_g08.mp4"),
        "output": str(FINAL / f"S{scene:03d}.mp4"),
    })
plan = {"project": "Nuviko 009 Black Death", "fps": 30, "resolution": [1920, 1080],
        "motion_order": ["layered parallax", "opposed whole-image camera", "G08"],
        "items": items}
plan_path = ROOT / "render_manifest.json"
plan_path.write_text(json.dumps(plan, indent=2) + "\n")
receipt_path = ROOT / "render_receipt.json"
receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else []
done = {int(r["scene"]) for r in receipt}
lock = Lock()

def video_has_frames(path, frames):
    if not path.exists():
        return False
    probe = subprocess.run([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=nb_frames,r_frame_rate,width,height,pix_fmt", "-of", "json", str(path)
    ], capture_output=True, text=True)
    if probe.returncode:
        return False
    try:
        stream = json.loads(probe.stdout)["streams"][0]
        return (int(stream.get("nb_frames", 0)) == frames and stream.get("r_frame_rate") == "30/1"
                and stream.get("pix_fmt") == "yuv420p" and int(stream["width"]) == 1920
                and int(stream["height"]) == 1080)
    except (KeyError, ValueError, IndexError):
        return False

def render_item(item):
    scene = item["scene"]
    pre, output = Path(item["pre_g08"]), Path(item["output"])
    g08_receipt = Path(item["output"] + ".g08.json")
    if (scene in done and video_has_frames(output, item["frames"]) and g08_receipt.exists()):
        return None
    if pre.exists() and not video_has_frames(pre, item["frames"]):
        pre.unlink()
    if output.exists() and not video_has_frames(output, item["frames"]):
        output.unlink()
        g08_receipt.unlink(missing_ok=True)
    if not pre.exists():
        subprocess.run([
            sys.executable, str(LAYERED),
            "--foreground", item["foreground"], "--background", item["background"],
            "--output", str(pre), "--direction", item["direction"],
            "--frames", str(item["frames"]), "--camera-scale", str(item["camera_scale"]),
            "--camera-travel-width-fraction", str(item["camera_travel_width_fraction"]),
            "--camera-crop-y", str(item["camera_crop_y"]),
        ], check=True)
    if not video_has_frames(output, item["frames"]) or not g08_receipt.exists():
        if output.exists():
            output.unlink()
        subprocess.run([
            str(PROCESSING_PYTHON), str(G08), "--input", str(pre), "--output", str(output),
            "--image-sha256", item["image_sha256"], "--frames", str(item["frames"]),
        ], check=True)
    entry = {k: item[k] for k in ("scene", "image", "frames", "fps", "direction",
                                  "camera_scale", "camera_travel_width_fraction",
                                  "camera_crop_y", "pre_g08", "output")}
    entry["g08_receipt"] = str(output) + ".g08.json"
    print(json.dumps(entry), flush=True)
    return entry

with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(render_item, item) for item in items]
    for future in as_completed(futures):
        entry = future.result()
        if entry:
            with lock:
                receipt[:] = [r for r in receipt if int(r["scene"]) != int(entry["scene"])]
                receipt.append(entry)
                receipt.sort(key=lambda r: int(r["scene"]))
                receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
