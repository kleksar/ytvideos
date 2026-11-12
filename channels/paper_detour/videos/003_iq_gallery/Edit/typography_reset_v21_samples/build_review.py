#!/usr/bin/env python3
"""Build the v21 scene/title review pairs from approved Paper Detour assets."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
SOURCE = ROOT / "channels/paper_detour/videos/003_iq_gallery/Source/Images/iq_gallery_subject_relevance_v21"
LABELS = ROOT / "channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/prepared_labels_v13"

CANVAS = (1080, 1920)
ROW_CENTERS = (1304, 1426, 1560)
ROW_HEIGHTS = (96, 96, 108)
X_CENTER = 540

ITEMS = [
    ("01_jfk", "John F. Kennedy — IQ 119", "01_jfk.png", "john_f_kennedy_name.png", "119"),
    ("02_kasparov", "Garry Kasparov — IQ 123", "02_kasparov.png", "kasparov_name.png", "123"),
    ("03_kanye", "Kanye West — IQ 133", "03_kanye.png", "kanye_west_name.png", "133"),
    ("04_marilyn", "Marilyn vos Savant — IQ 228", "04_marilyn.png", "marilyn_name.png", "228"),
]

MAX_ROW_WIDTH = 820
DIGIT_GAP = 10
IQ_GAP = 26


def row_spans(alpha: Image.Image):
    active = [alpha.crop((0, y, alpha.width, y + 1)).getbbox() is not None for y in range(alpha.height)]
    spans = []
    start = None
    for y, is_active in enumerate(active + [False]):
        if is_active and start is None:
            start = y
        elif not is_active and start is not None:
            spans.append((start, y))
            start = None
    return spans


def prepare_scene(source: Path) -> Image.Image:
    image = Image.open(source).convert("RGB")
    return ImageOps.fit(image, CANVAS, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def trim_asset(path: Path) -> Image.Image:
    asset = Image.open(path).convert("RGBA")
    bbox = asset.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"Empty paper type asset: {path}")
    return asset.crop(bbox)


def scale_height(asset: Image.Image, height: int) -> Image.Image:
    width = max(1, round(asset.width * height / asset.height))
    return asset.resize((width, height), Image.Resampling.LANCZOS)


def add_paper_period(row: Image.Image) -> Image.Image:
    """Add a small dimensional cream-paper full stop after JOHN F."""
    period = Image.new("RGBA", (22, 22), (0, 0, 0, 0))
    mask = Image.new("L", period.size, 0)
    ImageDraw.Draw(mask).ellipse((3, 3, 14, 14), fill=255)

    shadow_mask = Image.new("L", period.size, 0)
    shadow_mask.paste(mask, (4, 5))
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(3))
    shadow = Image.new("RGBA", period.size, (10, 21, 37, 0))
    shadow.putalpha(shadow_mask.point(lambda value: round(value * 0.48)))
    period.alpha_composite(shadow)

    edge_mask = Image.new("L", period.size, 0)
    edge_mask.paste(mask, (3, 3))
    edge = Image.new("RGBA", period.size, (196, 111, 67, 0))
    edge.putalpha(edge_mask)
    period.alpha_composite(edge)

    face = Image.new("RGBA", period.size, (241, 227, 201, 0))
    face.putalpha(mask)
    period.alpha_composite(face)

    result = Image.new("RGBA", (row.width + 24, row.height), (0, 0, 0, 0))
    result.alpha_composite(row, (0, 0))
    result.alpha_composite(period, (row.width + 2, row.height - 22))
    return result


def make_title(name_source: Path, score: str) -> Image.Image:
    """Use the approved cut-paper name, IQ, and individual numeral assets."""
    name = trim_asset(name_source)
    spans = row_spans(name.getchannel("A"))
    if len(spans) != 2:
        raise ValueError(f"Expected two name rows in {name_source.name}; found {spans}")

    title = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    for row_index, ((top, bottom), center_y) in enumerate(zip(spans, ROW_CENTERS[:2])):
        row = trim_asset_from_crop(name, (0, top, name.width, bottom))
        row = scale_height(row, ROW_HEIGHTS[0])
        if name_source.name == "john_f_kennedy_name.png" and row_index == 0:
            row = add_paper_period(row)
        if row.width > MAX_ROW_WIDTH:
            row = row.resize((MAX_ROW_WIDTH, row.height), Image.Resampling.LANCZOS)
        title.alpha_composite(row, (X_CENTER - row.width // 2, center_y - row.height // 2))

    iq_master = Image.open(OUT / "iq_glyph_paper_v01.png").convert("RGBA")
    hard_alpha = iq_master.getchannel("A").point(lambda value: 255 if value > 240 else 0)
    active_columns = [hard_alpha.crop((x, 0, x + 1, hard_alpha.height)).getbbox() is not None for x in range(hard_alpha.width)]
    glyph_spans = []
    start = None
    for x, active in enumerate(active_columns + [False]):
        if active and start is None:
            start = x
        elif not active and start is not None:
            if x - start > 30:
                glyph_spans.append((start, x))
            start = None
    if len(glyph_spans) != 2:
        raise ValueError(f"Expected separate I and Q glyphs in the IQ master; found {glyph_spans}")
    iq_glyphs = [
        scale_height(trim_asset_from_crop(iq_master, (left, 0, right, iq_master.height)), ROW_HEIGHTS[2])
        for left, right in glyph_spans
    ]
    iq_internal_gap = 10
    iq_gap = IQ_GAP
    digit_gap = DIGIT_GAP
    iq_width = sum(glyph.width for glyph in iq_glyphs) + iq_internal_gap
    digits = [scale_height(trim_asset(LABELS / f"digit_{digit}.png"), ROW_HEIGHTS[2]) for digit in score]
    score_width = iq_width + iq_gap + sum(digit.width for digit in digits) + digit_gap * (len(digits) - 1)
    if score_width > MAX_ROW_WIDTH:
        factor = MAX_ROW_WIDTH / score_width
        iq_glyphs = [glyph.resize((round(glyph.width * factor), ROW_HEIGHTS[2]), Image.Resampling.LANCZOS) for glyph in iq_glyphs]
        iq_internal_gap = round(iq_internal_gap * factor)
        iq_gap = round(iq_gap * factor)
        digit_gap = round(digit_gap * factor)
        iq_width = sum(glyph.width for glyph in iq_glyphs) + iq_internal_gap
        digits = [digit.resize((round(digit.width * factor), ROW_HEIGHTS[2]), Image.Resampling.LANCZOS) for digit in digits]
        score_width = iq_width + iq_gap + sum(digit.width for digit in digits) + digit_gap * (len(digits) - 1)

    x = X_CENTER - score_width // 2
    y = ROW_CENTERS[2] - ROW_HEIGHTS[2] // 2
    title.alpha_composite(iq_glyphs[0], (x, y))
    x += iq_glyphs[0].width + iq_internal_gap
    title.alpha_composite(iq_glyphs[1], (x, y))
    x += iq_glyphs[1].width + iq_gap
    for index, digit in enumerate(digits):
        title.alpha_composite(digit, (x, y))
        x += digit.width + (digit_gap if index < len(digits) - 1 else 0)
    return title


def trim_asset_from_crop(asset: Image.Image, crop) -> Image.Image:
    row = asset.crop(crop)
    bbox = row.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Found an empty name row")
    return row.crop(bbox)


def main():
    previews = []
    for stem, label, scene_name, name_asset, score in ITEMS:
        scene = prepare_scene(SOURCE / scene_name)
        scene.save(OUT / f"{stem}_scene.png")

        title = make_title(LABELS / name_asset, score)
        title_path = OUT / f"{stem}_title.png"
        preview_path = OUT / f"{stem}_preview.png"
        title.save(title_path)

        composite = Image.alpha_composite(scene.convert("RGBA"), title).convert("RGB")
        composite.save(preview_path, quality=96)
        previews.append((label, composite))

    tile = (486, 864)
    gutter = 24
    contact = Image.new("RGB", (tile[0] * 2 + gutter * 3, tile[1] * 2 + gutter * 3), (238, 231, 215))
    for index, (_label, image) in enumerate(previews):
        x = gutter + (index % 2) * (tile[0] + gutter)
        y = gutter + (index // 2) * (tile[1] + gutter)
        contact.paste(image.resize(tile, Image.Resampling.LANCZOS), (x, y))
    contact.save(OUT / "contact_4_pairs.jpg", quality=94)


if __name__ == "__main__":
    main()
