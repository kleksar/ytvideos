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
EPISODE = ROOT.parents[2]
ASSETS = EPISODE / "Assets/Generated/Pompeii_Remake_v01"
VISION = json.loads((ASSETS / "vision_masks/vision_receipt.json").read_text())
MANIFEST = json.loads((ROOT / "vision_manifest_v01.json").read_text())
IMAGE_BY_SCENE = {int(row["scene"]): Path(row["image"]) for row in MANIFEST}
OUT = ASSETS / "layered_v01"
OUT.mkdir(parents=True, exist_ok=True)
RECEIPT_PATH = ROOT / "layer_prep_receipt_v01.json"

os.environ["LAMA_MODEL"] = str(
    Path(__file__).resolve().parents[5]
    / "Shared/Image_Motion/Tools/sam2-local/cache/torch/hub/checkpoints/big-lama.pt"
)
if not Path(os.environ["LAMA_MODEL"]).exists():
    os.environ["LAMA_MODEL"] = "/Users/diplomat/ytvideos/Shared/Image_Motion/Tools/sam2-local/cache/torch/hub/checkpoints/big-lama.pt"
lama = SimpleLama(device=torch.device("mps"))


def fill_holes(mask: np.ndarray) -> np.ndarray:
    padded = cv2.copyMakeBorder(mask, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
    flood = padded.copy()
    h, w = flood.shape
    cv2.floodFill(flood, np.zeros((h + 2, w + 2), np.uint8), (0, 0), 255)
    holes = cv2.bitwise_not(flood)[1:-1, 1:-1]
    return cv2.bitwise_or(mask, holes)


vision_by_scene = {int(row["scene"]): row for row in VISION}
receipt = json.loads(RECEIPT_PATH.read_text()) if RECEIPT_PATH.exists() else []
done = {int(row["scene"]) for row in receipt}

for scene in range(1, 180):
    vision = vision_by_scene[scene]
    if vision.get("status") != "MASK_READY" or scene in done:
        continue
    source_path = IMAGE_BY_SCENE[scene]
    image = Image.open(source_path).convert("RGB")
    width, height = image.size
    mask_path = Path(vision["mask"])
    raw = Image.open(mask_path).convert("L").resize((width, height), Image.Resampling.NEAREST)
    mask = (np.asarray(raw) > 127).astype(np.uint8) * 255
    mask = fill_holes(mask)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    mask = fill_holes(mask)
    mask_area = float((mask > 0).mean())
    if not 0.002 <= mask_area <= 0.90:
        raise RuntimeError(f"K{scene:03d}: unusable mask area {mask_area:.4f}")

    rgb = np.asarray(image)
    alpha = cv2.GaussianBlur(mask, (0, 0), 0.55)
    foreground = np.dstack([rgb, alpha])
    expanded = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
    expanded_img = Image.fromarray(expanded)
    restored = lama(image, expanded_img)
    restored_rgb = np.asarray(restored.convert("RGB"))[:height, :width]
    background = rgb.copy()
    background[expanded > 0] = restored_rgb[expanded > 0]

    folder = OUT / f"K{scene:03d}"
    folder.mkdir(exist_ok=True)
    Image.fromarray(foreground, "RGBA").save(folder / "foreground.png")
    Image.fromarray(background, "RGB").save(folder / "background.png")
    Image.fromarray(mask).save(folder / "mask.png")
    Image.fromarray(expanded).save(folder / "inpaint_mask.png")
    row = {
        "scene": scene,
        "source": str(source_path),
        "source_size": [width, height],
        "vision_mask": str(mask_path),
        "mask_area_percent": round(mask_area * 100, 4),
        "inpaint_area_percent": round(float((expanded > 0).mean()) * 100, 4),
        "foreground": str(folder / "foreground.png"),
        "background": str(folder / "background.png"),
        "mask": str(folder / "mask.png"),
        "inpaint_mask": str(folder / "inpaint_mask.png"),
        "method": "Apple Vision instance mask + LaMa MPS, 12px inpaint dilation",
    }
    receipt.append(row)
    RECEIPT_PATH.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(row), flush=True)

