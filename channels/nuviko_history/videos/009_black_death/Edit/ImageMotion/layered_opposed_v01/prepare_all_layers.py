from __future__ import annotations

import json
import os
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from simple_lama_inpainting import SimpleLama

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "layers"
OUT.mkdir(exist_ok=True)
VISION = json.loads((ROOT / "vision_masks" / "vision_receipt.json").read_text())
FALLBACK = json.loads((ROOT / "sam_fallback_receipt_v02.json").read_text())
MANIFEST = json.loads((ROOT / "vision_manifest.json").read_text())
vision_by_scene = {int(r["scene"]): r for r in VISION}
fallback_by_scene = {int(r["scene"]): r for r in FALLBACK}
image_by_scene = {int(r["scene"]): Path(r["image"]) for r in MANIFEST}

os.environ["LAMA_MODEL"] = "/Users/diplomat/ytvideos/Shared/Image_Motion/Tools/sam2-local/cache/torch/hub/checkpoints/big-lama.pt"
lama = SimpleLama(device=torch.device("mps"))

def fill_holes(mask: np.ndarray) -> np.ndarray:
    # A foreground mask may touch the original top-left pixel. Pad with a
    # guaranteed background border so flood fill never mistakes foreground
    # for the outside region.
    padded = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    flood = padded.copy()
    h, w = flood.shape
    cv2.floodFill(flood, np.zeros((h + 2, w + 2), np.uint8), (0, 0), 255)
    holes = cv2.bitwise_not(flood)[1:-1, 1:-1]
    return cv2.bitwise_or(mask, holes)

receipt_path = ROOT / "layer_prep_receipt.json"
receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else []
done = {int(r["scene"]) for r in receipt}
for scene in range(1, 119):
    if scene in done:
        continue
    image_path = image_by_scene[scene]
    image = Image.open(image_path).convert("RGB")
    w, h = image.size
    rec = vision_by_scene[scene]
    if rec.get("status") == "MASK_READY":
        mask_path = Path(rec["mask"])
        source = "vision"
    else:
        fallback = fallback_by_scene.get(scene)
        if not fallback:
            raise RuntimeError(f"No segmentation mask for S{scene:03d}")
        mask_path = Path(fallback["mask"])
        source = "sam2-fallback"
    raw = Image.open(mask_path).convert("L").resize((w, h), Image.Resampling.NEAREST)
    mask = (np.asarray(raw) > 127).astype(np.uint8) * 255
    mask = fill_holes(mask)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    mask = fill_holes(mask)
    area = float((mask > 0).mean())
    if area < 0.002 or area > 0.90:
        raise RuntimeError(f"S{scene:03d}: unusable subject mask area {area:.4f}")
    alpha = cv2.GaussianBlur(mask, (0, 0), 0.55)
    rgb = np.asarray(image)
    fg = np.dstack([rgb, alpha])
    folder = OUT / f"S{scene:03d}"
    folder.mkdir(exist_ok=True)
    Image.fromarray(fg, "RGBA").save(folder / "foreground.png")
    expanded = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (37, 37)))
    mask_img = Image.fromarray(expanded)
    mask_img.save(folder / "inpaint_mask_18px.png")
    restored = lama(image, mask_img)
    restored_arr = np.asarray(restored)[:h, :w]
    base = rgb.copy()
    base[expanded > 0] = restored_arr[expanded > 0]
    Image.fromarray(base).save(folder / "background.png")
    entry = {
        "scene": scene, "image": str(image_path), "size": [w, h],
        "mask": str(mask_path), "mask_source": source,
        "mask_area_percent": round(area * 100, 4),
        "inpaint_area_percent": round(float((expanded > 0).mean()) * 100, 4),
        "foreground": str(folder / "foreground.png"),
        "background": str(folder / "background.png"),
    }
    receipt.append(entry)
    print(json.dumps(entry), flush=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
