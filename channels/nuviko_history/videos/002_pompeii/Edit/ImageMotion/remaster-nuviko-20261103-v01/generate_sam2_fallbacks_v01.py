from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")
import torch
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

ROOT = Path(__file__).resolve().parent
EPISODE = ROOT.parents[2]
ASSETS = EPISODE / "Assets/Generated/Pompeii_Remake_v01"
OUT = ASSETS / "sam2_masks_v01"
OUT.mkdir(parents=True, exist_ok=True)
PROMPTS = json.loads((ROOT / "sam2_fallback_prompts_v01.json").read_text())
MANIFEST = json.loads((ROOT / "vision_manifest_v01.json").read_text())
IMAGE_BY_SCENE = {int(row["scene"]): Path(row["image"]) for row in MANIFEST}
CHECKPOINT = Path(__file__).resolve().parents[5] / "Shared/Image_Motion/Tools/sam2-local/models/sam2.1_hiera_tiny.pt"
if not CHECKPOINT.exists():
    CHECKPOINT = Path("/Users/diplomat/ytvideos/Shared/Image_Motion/Tools/sam2-local/models/sam2.1_hiera_tiny.pt")
model = build_sam2("configs/sam2.1/sam2.1_hiera_t.yaml", str(CHECKPOINT), device="mps", apply_postprocessing=False)
predictor = SAM2ImagePredictor(model)
receipt_path = ROOT / "sam2_fallback_receipt_v01.json"
receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else []
done = {int(row["scene"]) for row in receipt}

with torch.inference_mode():
    for spec in PROMPTS:
        scene = int(spec["scene"])
        if scene in done:
            continue
        image_path = IMAGE_BY_SCENE[scene]
        image = Image.open(image_path).convert("RGB")
        width, height = image.size
        sx, sy = width / 1672.0, height / 941.0
        predictor.set_image(np.asarray(image).copy())
        points = np.asarray([[point[0] * sx, point[1] * sy] for point in spec["points"]], dtype=np.float32)
        labels = np.asarray([point[2] for point in spec["points"]], dtype=np.int32)
        box = np.asarray([spec["box"][0] * sx, spec["box"][1] * sy,
                          spec["box"][2] * sx, spec["box"][3] * sy], dtype=np.float32)
        masks, scores, _ = predictor.predict(
            point_coords=points,
            point_labels=labels,
            box=box,
            multimask_output=False,
        )
        mask = np.asarray(masks[0], dtype=np.uint8)
        mask_path = OUT / f"K{scene:03d}_sam2_v01.png"
        Image.fromarray(mask * 255, mode="L").save(mask_path)
        row = {
            "scene": scene,
            "image": str(image_path),
            "mask": str(mask_path),
            "box": spec["box"],
            "points": spec["points"],
            "scaled_box": box.tolist(),
            "score": float(scores[0]),
            "mask_area_percent": round(float(mask.mean() * 100), 4),
            "source_size": list(image.size),
            "method": "SAM2.1 Hiera Tiny MPS, per-scene point+box prompt",
        }
        receipt.append(row)
        receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
        print(json.dumps(row), flush=True)
