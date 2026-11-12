#!/usr/bin/env python3
"""Build a flat JFK IQ card and a silent title-fade preview."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "Source/Images/iq_gallery_type_fade_20261101"
ORIGINAL = ROOT / "Source/Images/iq_gallery_flat_card_redesign_20261101/JFK_IQ119_pilot_v02.png"
CLEAN_BG = IMAGE_DIR / "JFK_IQ119_textless_bg_v01.png"
TYPE_ASSET = IMAGE_DIR / "JFK_cutpaper_type_block_v01.png"
REPAIRED_BG = IMAGE_DIR / "JFK_IQ119_repaired_bg_v01.png"
OVERLAY = IMAGE_DIR / "JFK_IQ119_type_overlay_v01.png"
STILL = IMAGE_DIR / "JFK_IQ119_papercut_type_v01.png"
VIDEO = IMAGE_DIR / "JFK_IQ119_type_fade_preview_v01.mp4"

# Crops are ordered as JOHN F., KENNEDY, IQ 119 within the generated alpha PNG.
ROW_BOUNDS = ((108, 397), (399, 674), (677, 972))
ROW_HEIGHTS = (82, 82, 92)
ROW_TOPS = (1202, 1288, 1378)
CANVAS = (1080, 1920)


def repair_title_area() -> Image.Image:
    original = Image.open(ORIGINAL).convert("RGBA")
    cleaned = Image.open(CLEAN_BG).convert("RGBA")
    a = np.asarray(original.convert("RGB"), dtype=np.int16)
    b = np.asarray(cleaned.convert("RGB"), dtype=np.int16)
    diff = np.max(np.abs(a - b), axis=2)
    mask = Image.fromarray(np.where(diff > 28, 255, 0).astype("uint8"))
    mask = mask.filter(ImageFilter.MaxFilter(31)).filter(ImageFilter.GaussianBlur(5))

    # The original title ends above this boundary. Keeping the repair inside it
    # preserves untouched ribbon texture and avoids artifacts in the clean-up pass.
    clip_arr = np.zeros((CANVAS[1], CANVAS[0]), dtype="uint8")
    clip_arr[1188:1484, :] = 255
    for y in range(1484, 1501):
        clip_arr[y, :] = round(255 * (1500 - y) / 16)
    mask = Image.fromarray(np.minimum(np.asarray(mask), clip_arr).astype("uint8"))
    repaired = Image.composite(cleaned, original, mask)
    repaired.save(REPAIRED_BG)
    return repaired


def make_overlay() -> Image.Image:
    source = Image.open(TYPE_ASSET).convert("RGBA")
    overlay = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    for (y0, y1), target_h, top in zip(ROW_BOUNDS, ROW_HEIGHTS, ROW_TOPS):
        row = source.crop((0, y0, source.width, y1))
        alpha = np.asarray(row.getchannel("A"))
        ys, xs = np.where(alpha > 8)
        if len(xs) == 0:
            raise RuntimeError(f"No visible pixels in title row {y0}:{y1}")
        pad = 8
        row = row.crop(
            (
                max(0, int(xs.min()) - pad),
                max(0, int(ys.min()) - pad),
                min(row.width, int(xs.max()) + pad + 1),
                min(row.height, int(ys.max()) + pad + 1),
            )
        )
        width = round(row.width * target_h / row.height)
        row = row.convert("RGBa").resize((width, target_h), Image.Resampling.LANCZOS).convert("RGBA")
        x = round(CANVAS[0] / 2 - width / 2)
        overlay.alpha_composite(row, (x, top))
    overlay.save(OVERLAY)
    return overlay


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    background = repair_title_area()
    overlay = make_overlay()
    composed = background.copy()
    composed.alpha_composite(overlay)
    composed.convert("RGB").save(STILL, quality=95)

    alpha = overlay.getchannel("A")
    with tempfile.TemporaryDirectory(prefix="iq_gallery_fade_") as tmp:
        sequence = Path(tmp) / "title_%03d.png"
        for frame_no in range(150):
            if frame_no <= 8:
                x = frame_no / 8
                opacity = x * x * (3 - 2 * x)
            elif frame_no <= 137:
                opacity = 1.0
            else:
                x = (frame_no - 138) / 11
                opacity = 1.0 - x * x * (3 - 2 * x)
            frame = overlay.copy()
            frame.putalpha(alpha.point(lambda value, o=opacity: round(value * o)))
            frame.save(str(sequence) % frame_no)

        command = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-framerate", "30", "-i", str(REPAIRED_BG),
            "-framerate", "30", "-start_number", "0", "-i", str(sequence),
            "-filter_complex", "[0:v][1:v]overlay=shortest=1:format=auto,format=yuv420p[v]",
            "-map", "[v]", "-t", "5.00", "-an", "-c:v", "libx264",
            "-preset", "medium", "-crf", "17", "-movflags", "+faststart", str(VIDEO),
        ]
        subprocess.run(command, check=True)
    print(f"still: {STILL}")
    print(f"preview: {VIDEO}")


if __name__ == "__main__":
    main()
