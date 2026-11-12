#!/usr/bin/env python3
"""Flatten the approved JFK paper title over the Berlin motorcade scene."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "Source/Images/iq_gallery_type_fade_20261101"
SCENE = ASSETS / "JFK_WestBerlin_motorcade_scene_raw_v01.png"
TITLE_SOURCE = ASSETS / "JFK_IQ119_type_overlay_v01.png"
TITLE = ASSETS / "JFK_IQ119_type_overlay_v02.png"
BACKGROUND = ASSETS / "JFK_WestBerlin_motorcade_background_v01.png"
STILL = ASSETS / "JFK_IQ119_Berlin_motorcade_card_v02.png"
VIDEO = ASSETS / "JFK_IQ119_Berlin_motorcade_fade_preview_v02.mp4"
SIZE = (1080, 1920)
TITLE_SHIFT_Y = 80


def main() -> None:
    scene = Image.open(SCENE).convert("RGB")
    source_ratio = scene.width / scene.height
    target_ratio = SIZE[0] / SIZE[1]
    if abs(source_ratio - target_ratio) > 0.002:
        raise ValueError(f"Scene aspect ratio {source_ratio:.5f} does not match 9:16")
    background = scene.resize(SIZE, Image.Resampling.LANCZOS)
    background.save(BACKGROUND)

    overlay_source = Image.open(TITLE_SOURCE).convert("RGBA")
    if overlay_source.size != SIZE:
        raise ValueError(f"Title overlay must be {SIZE}, got {overlay_source.size}")
    overlay = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    overlay.alpha_composite(overlay_source.crop((0, 0, SIZE[0], SIZE[1] - TITLE_SHIFT_Y)), (0, TITLE_SHIFT_Y))
    overlay.save(TITLE)
    still_rgba = background.convert("RGBA")
    still_rgba.alpha_composite(overlay)
    still_rgba.convert("RGB").save(STILL, quality=95)

    original_alpha = overlay.getchannel("A")
    with tempfile.TemporaryDirectory(prefix="jfk_berlin_fade_") as tmp:
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
            frame.putalpha(original_alpha.point(lambda value, o=opacity: round(value * o)))
            frame.save(str(sequence) % frame_no)

        command = [
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-framerate", "30", "-i", str(BACKGROUND),
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
