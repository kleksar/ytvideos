#!/usr/bin/env python3
"""Prepare v22 IQ Gallery card stills, accepted cut-paper titles, and review sheets."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[5]
IMAGES = ROOT / "channels/paper_detour/videos/003_iq_gallery/Source/Images/iq_gallery_full_scene_v22"
LABELS = ROOT / "channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/prepared_labels_v13"
TITLE_MASTER = ROOT / "channels/paper_detour/videos/003_iq_gallery/Edit/typography_reset_v21_samples/iq_glyph_paper_v01.png"
TITLE_DIR = ROOT / "channels/paper_detour/videos/003_iq_gallery/Source/Images/iq_gallery_paper_titles_v22"
REVIEW = ROOT / "channels/paper_detour/videos/003_iq_gallery/Edit/iq_gallery_v22_review"
MANIFEST = ROOT / "channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/iq_gallery_v22_manifest.json"

CANVAS = (1080, 1920)
FPS = 30
ROW_CENTERS = (1304, 1426, 1560)
ROW_HEIGHTS = (96, 96, 108)
X_CENTER = 540
MAX_ROW_WIDTH = 820
IQ_INTERNAL_GAP = 10
IQ_GAP = 26
DIGIT_GAP = 10

CAST = [
    ("S01_JFK", "John F. Kennedy", 119, 120, "s01_jfk.png", "john_f_kennedy_name.png"),
    ("S02_KASPAROV", "Garry Kasparov", 123, 120, "s02_kasparov.png", "kasparov_name.png"),
    ("S03_FEYNMAN", "Richard Feynman", 125, 150, "s03_feynman.png", "feynman_name.png"),
    ("S04_KANYE", "Kanye West", 133, 120, "s04_kanye.png", "kanye_west_name.png"),
    ("S05_LOGAN", "Logan Paul", 139, 150, "s05_logan.png", "logan_paul_name.png"),
    ("S06_RM", "RM", 148, 120, "s06_rm.png", "rm_name.png"),
    ("S07_NOLAN", "Nolan Gould", 150, 150, "s07_nolan.png", "nolan_gould_name.png"),
    ("S08_LAMPARD", "Frank Lampard", 150, 120, "s08_lampard.png", "frank_lampard_name.png"),
    ("S09_KATE", "Kate Beckinsale", 152, 150, "s09_kate.png", "kate_beckinsale_name.png"),
    ("S10_SHARON", "Sharon Stone", 154, 120, "s10_sharon.png", "sharon_stone_name.png"),
    ("S11_LEE", "Lee Byung-hun", 155, 150, "s11_lee.png", "lee_byung_hun_name.png"),
    ("S12_TARANTINO", "Quentin Tarantino", 160, 150, "s12_tarantino.png", "tarantino_name.png"),
    ("S13_MARILYN", "Marilyn vos Savant", 228, 180, "s13_marilyn.png", "marilyn_name.png"),
]


def trim_alpha(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("Found an empty paper type asset")
    return image.crop(bbox)


def row_spans(alpha: Image.Image) -> list[tuple[int, int]]:
    active = [alpha.crop((0, y, alpha.width, y + 1)).getbbox() is not None for y in range(alpha.height)]
    spans: list[tuple[int, int]] = []
    start = None
    for y, is_active in enumerate(active + [False]):
        if is_active and start is None:
            start = y
        elif not is_active and start is not None:
            spans.append((start, y))
            start = None
    return spans


def crop_and_trim(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    return trim_alpha(image.crop(box))


def scale_height(image: Image.Image, height: int) -> Image.Image:
    width = max(1, round(image.width * height / image.height))
    return image.resize((width, height), Image.Resampling.LANCZOS)


def add_period(row: Image.Image) -> Image.Image:
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
    result.alpha_composite(row)
    result.alpha_composite(period, (row.width + 2, row.height - 22))
    return result


def split_iq_glyphs() -> list[Image.Image]:
    master = Image.open(TITLE_MASTER).convert("RGBA")
    hard_alpha = master.getchannel("A").point(lambda value: 255 if value > 240 else 0)
    active = [hard_alpha.crop((x, 0, x + 1, hard_alpha.height)).getbbox() is not None for x in range(hard_alpha.width)]
    spans: list[tuple[int, int]] = []
    start = None
    for x, on in enumerate(active + [False]):
        if on and start is None:
            start = x
        elif not on and start is not None:
            if x - start > 30:
                spans.append((start, x))
            start = None
    if len(spans) != 2:
        raise ValueError(f"Expected separate I and Q glyphs, found {spans}")
    return [crop_and_trim(master, (left, 0, right, master.height)) for left, right in spans]


def make_title(name_path: Path, score: int, iq_glyphs: list[Image.Image]) -> Image.Image:
    name = trim_alpha(Image.open(name_path))
    spans = row_spans(name.getchannel("A"))
    if len(spans) not in (1, 2):
        raise ValueError(f"Expected one or two name rows in {name_path.name}; found {spans}")
    centers = (1365,) if len(spans) == 1 else ROW_CENTERS[:2]
    title = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    for row_index, ((top, bottom), center_y) in enumerate(zip(spans, centers)):
        row = crop_and_trim(name, (0, top, name.width, bottom))
        row = scale_height(row, ROW_HEIGHTS[0])
        if name_path.name == "john_f_kennedy_name.png" and row_index == 0:
            row = add_period(row)
        if row.width > MAX_ROW_WIDTH:
            row = row.resize((MAX_ROW_WIDTH, row.height), Image.Resampling.LANCZOS)
        title.alpha_composite(row, (X_CENTER - row.width // 2, center_y - row.height // 2))

    iq = [scale_height(glyph, ROW_HEIGHTS[2]) for glyph in iq_glyphs]
    digits = [scale_height(trim_alpha(Image.open(LABELS / f"digit_{digit}.png")), ROW_HEIGHTS[2]) for digit in str(score)]
    width = sum(g.width for g in iq) + IQ_INTERNAL_GAP + IQ_GAP + sum(d.width for d in digits) + DIGIT_GAP * (len(digits) - 1)
    if width > MAX_ROW_WIDTH:
        factor = MAX_ROW_WIDTH / width
        iq = [g.resize((round(g.width * factor), ROW_HEIGHTS[2]), Image.Resampling.LANCZOS) for g in iq]
        digits = [g.resize((round(g.width * factor), ROW_HEIGHTS[2]), Image.Resampling.LANCZOS) for g in digits]
        internal_gap = round(IQ_INTERNAL_GAP * factor)
        iq_gap = round(IQ_GAP * factor)
        digit_gap = round(DIGIT_GAP * factor)
    else:
        internal_gap, iq_gap, digit_gap = IQ_INTERNAL_GAP, IQ_GAP, DIGIT_GAP
    row_width = sum(g.width for g in iq) + internal_gap + iq_gap + sum(d.width for d in digits) + digit_gap * (len(digits) - 1)
    x = X_CENTER - row_width // 2
    y = ROW_CENTERS[2] - ROW_HEIGHTS[2] // 2
    title.alpha_composite(iq[0], (x, y))
    x += iq[0].width + internal_gap
    title.alpha_composite(iq[1], (x, y))
    x += iq[1].width + iq_gap
    for index, digit in enumerate(digits):
        title.alpha_composite(digit, (x, y))
        x += digit.width + (digit_gap if index < len(digits) - 1 else 0)
    return title


def fit_scene(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if image.width / image.height < 0.55 or image.width / image.height > 0.57:
        raise ValueError(f"Scene must be portrait 9:16: {path} is {image.size}")
    return ImageOps.fit(image, CANVAS, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def save_contact(cards: list[tuple[str, Image.Image]], path: Path) -> None:
    tile = (360, 640)
    gutter = 24
    columns = 3
    rows = 3
    sheet = Image.new("RGB", (columns * tile[0] + (columns + 1) * gutter, rows * tile[1] + (rows + 1) * gutter), (238, 231, 215))
    draw = ImageDraw.Draw(sheet)
    for index, (label, card) in enumerate(cards):
        if index >= columns * rows:
            break
        x = gutter + (index % columns) * (tile[0] + gutter)
        y = gutter + (index // columns) * (tile[1] + gutter)
        sheet.paste(card.resize(tile, Image.Resampling.LANCZOS), (x, y))
        draw.rectangle((x, y, x + tile[0] - 1, y + tile[1] - 1), outline=(117, 95, 72), width=1)
    sheet.save(path, quality=95)


def main() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    TITLE_DIR.mkdir(parents=True, exist_ok=True)
    scene_dir = REVIEW / "scenes"
    preview_dir = REVIEW / "previews"
    scene_dir.mkdir(exist_ok=True)
    preview_dir.mkdir(exist_ok=True)
    iq_glyphs = split_iq_glyphs()
    records = []
    cards: list[tuple[str, Image.Image]] = []

    for index, (tag, name, score, frames, scene_file, name_file) in enumerate(CAST, start=1):
        scene = fit_scene(IMAGES / scene_file)
        scene_path = scene_dir / f"{tag.lower()}.png"
        scene.save(scene_path)
        title = make_title(LABELS / name_file, score, iq_glyphs)
        title_path = TITLE_DIR / f"{tag.lower()}_title.png"
        title.save(title_path)
        composite = Image.alpha_composite(scene.convert("RGBA"), title).convert("RGB")
        preview_path = preview_dir / f"{tag.lower()}_preview.jpg"
        composite.save(preview_path, quality=96)
        cards.append((name, composite))
        records.append({
            "id": tag,
            "name": name,
            "iq": score,
            "frames": frames,
            "scene": str(scene_path.relative_to(ROOT)),
            "title": str(title_path.relative_to(ROOT)),
            "preview": str(preview_path.relative_to(ROOT)),
        })

    if sum(row[3] for row in CAST) != 1800:
        raise ValueError("v22 scene durations must total exactly 1800 frames")
    save_contact(cards[:9], REVIEW / "contact_01-09.jpg")
    save_contact(cards[9:], REVIEW / "contact_10-13.jpg")
    manifest = {
        "schema_version": 1,
        "title": "Paper Detour IQ Gallery v22 — approved v21 paper-card style",
        "fps": FPS,
        "width": CANVAS[0],
        "height": CANVAS[1],
        "duration_frames": 1800,
        "duration_seconds": 60,
        "audio_source": "channels/paper_detour/videos/003_iq_gallery/Source/Audio/iq_gallery_music_mix_20261101.m4a",
        "grain_source": "channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Source/Graphics/director_trial_20261031/film_grain_vertical_8s_prores4444.mov",
        "source_export_audio_reference": "channels/paper_detour/legacy/025_iq_gallery/Deliverables/025_iq_gallery_paper_detour_60s_v19.mp4",
        "title_geometry": {"x_center": X_CENTER, "row_centers_y": list(ROW_CENTERS), "row_heights": list(ROW_HEIGHTS), "title_fade_in_frames": 9, "title_fade_out_frames": 12},
        "iq_caveat": "These are varied published estimates/results, not comparable scientific measurements or a verified ranking.",
        "scenes": records,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"manifest": str(MANIFEST), "contact_sheets": [str(REVIEW / "contact_01-09.jpg"), str(REVIEW / "contact_10-13.jpg")], "scenes": len(records), "frames": 1800}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
