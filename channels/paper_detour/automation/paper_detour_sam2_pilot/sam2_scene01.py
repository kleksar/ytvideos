#!/usr/bin/env python3
"""Local SAM 2.1 point/box -> pixel-registered binary masks and RGBA groups.

Does not inpaint. Does not resize or redraw the approved master.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

CFG = "configs/sam2.1/sam2.1_hiera_t.yaml"


def mask_image(m: np.ndarray) -> Image.Image:
    return Image.fromarray((m.astype(np.uint8) * 255))


def coordinate_grid(master: Image.Image, step: int = 100) -> Image.Image:
    img = master.convert("RGB").copy()
    pen = ImageDraw.Draw(img)
    w, h = img.size
    for x in range(0, w, step):
        pen.line([(x, 0), (x, h)], fill=(255, 170, 40), width=1)
        pen.text((x + 3, 2), f"x{x}", fill=(255, 210, 100))
    for y in range(0, h, step):
        pen.line([(0, y), (w, y)], fill=(255, 170, 40), width=1)
        pen.text((3, y + 3), f"y{y}", fill=(255, 210, 100))
    return img


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--prompts", type=Path)
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--device", choices=["mps", "cpu"], default="mps")
    parser.add_argument("--grid-only", action="store_true")
    args = parser.parse_args()

    original = Image.open(args.image).convert("RGBA")
    w, h = original.size
    args.out.mkdir(parents=True, exist_ok=True)
    coordinate_grid(original).save(args.out / "coordinate_grid.png")
    print(f"Master size: {w}x{h}; coordinate_grid.png saved")
    if args.grid_only:
        return

    if not args.prompts or not args.checkpoint:
        parser.error("--prompts and --checkpoint are required except for --grid-only")

    import torch
    from sam2.build_sam import build_sam2
    from sam2.sam2_image_predictor import SAM2ImagePredictor

    if args.device == "mps" and not torch.backends.mps.is_available():
        raise RuntimeError("PyTorch MPS unavailable; run --device cpu or check arm64 torch")

    spec = json.loads(args.prompts.read_text(encoding="utf-8"))
    if not spec.get("objects"):
        raise ValueError("prompts JSON must contain a nonempty objects list")

    model = build_sam2(CFG, str(args.checkpoint), device=args.device,
                       apply_postprocessing=False)
    predictor = SAM2ImagePredictor(model)
    # Compute features once, then issue multiple prompts against the same image.
    union = {"MG": np.zeros((h, w), dtype=bool),
             "FG": np.zeros((h, w), dtype=bool)}
    with torch.inference_mode():
        predictor.set_image(np.asarray(original.convert("RGB")))
        for obj in spec["objects"]:
            name, layer = obj["name"], obj["layer"]
            if layer not in union:
                raise ValueError(f"Invalid layer for {name}: {layer}")
            prompts = obj.get("points", [])  # [x, y, label], label=1 positive, 0 negative
            points = np.asarray([p[:2] for p in prompts], dtype=np.float32).reshape(-1, 2)
            labels = np.asarray([p[2] for p in prompts], dtype=np.int32)
            box = obj.get("box")  # [x1, y1, x2, y2] in original image pixels
            if points.size == 0 and box is None:
                raise ValueError(f"{name}: specify positive/negative points or box")
            if box is not None and len(box) != 4:
                raise ValueError(f"{name}: box must have four coordinates")
            masks, scores, _ = predictor.predict(
                point_coords=points if len(points) else None,
                point_labels=labels if len(points) else None,
                box=np.asarray(box, dtype=np.float32) if box is not None else None,
                multimask_output=(len(points) <= 1 and box is None),
            )
            index = int(np.argmax(scores))
            mask = np.asarray(masks[index], dtype=bool)
            if mask.shape != (h, w):
                raise RuntimeError(f"{name}: mask is {mask.shape}, expected {(h,w)}")
            mask_image(mask).save(args.out / f"mask_{name}.png")
            union[layer] |= mask
            print(f"{name} -> {layer}: {(100 * mask.mean()):.2f}% pixels; score={float(scores[index]):.3f}")

    # Foreground occludes the middle ground in their intersections.
    fg = union["FG"]
    mg = union["MG"] & ~fg
    for layer, mask in (("MG", mg), ("FG", fg)):
        alpha = mask_image(mask)
        alpha.save(args.out / f"mask_{layer}.png")
        rgba = original.copy()
        rgba.putalpha(alpha)
        rgba.save(args.out / f"{layer}.png")
        print(f"Saved {layer}.png, {rgba.size}, alpha=0/255")

    holes = fg | mg
    mask_image(holes).save(args.out / "holes_exact.png")
    mask_image(holes).filter(ImageFilter.MaxFilter(9)).save(args.out / "holes_inpaint_dilated.png")

    preview = original.convert("RGB")
    for mask, color in ((mg, (230, 50, 60)), (fg, (40, 190, 210))):
        flat = Image.new("RGB", (w, h), color)
        mixed = Image.blend(preview, flat, 0.35)
        preview.paste(mixed, (0, 0), mask_image(mask))
    preview.save(args.out / "preview_masks.png")
    print("Saved preview_masks.png; no background inpainting performed")


if __name__ == "__main__":
    main()
