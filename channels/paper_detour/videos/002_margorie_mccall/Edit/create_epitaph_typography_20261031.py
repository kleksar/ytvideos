#!/usr/bin/env python3
"""Create two new transparent, uniformly sized epitaph layers from system Baskerville."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT = "/System/Library/Fonts/Supplemental/Baskerville.ttc"
OUT = Path(__file__).resolve().parent.parent / "Source/Graphics/epitaph_20261031"
SCALE = 2
WIDTH, HEIGHT = 1120, 220
SIZE, TRACKING = 124, 2
LINES = (("LIVED ONCE", "epitaph_lived_once_baskerville.png"),
         ("BURIED TWICE", "epitaph_buried_twice_baskerville.png"))

font = ImageFont.truetype(FONT, SIZE * SCALE, index=1)  # Baskerville Bold
OUT.mkdir(parents=True, exist_ok=True)
for value, filename in LINES:
    path = OUT / filename
    if path.exists():
        raise FileExistsError(f"Refusing to overwrite {path}")
    layer = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    advances = [draw.textlength(character, font=font) for character in value]
    full_width = sum(advances) + TRACKING * SCALE * (len(value) - 1)
    start = (WIDTH * SCALE - full_width) / 2
    baseline = 156 * SCALE
    for offset, fill in (((2 * SCALE, 2 * SCALE), (49, 37, 31, 220)),
                         ((0, 0), (220, 211, 192, 244))):
        cursor = start
        for character, advance in zip(value, advances):
            draw.text((round(cursor + offset[0]), baseline + offset[1]), character,
                      font=font, fill=fill, anchor="ls")
            cursor += advance + TRACKING * SCALE
    layer = layer.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    layer.save(path)
    print(f"{value}: {path} {layer.size}, alpha_bbox={layer.getchannel('A').getbbox()}")
