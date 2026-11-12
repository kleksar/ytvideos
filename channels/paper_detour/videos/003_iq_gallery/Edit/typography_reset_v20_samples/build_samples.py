#!/usr/bin/env python3
"""Build four review samples with independent Paper Detour image and title PNGs."""

from pathlib import Path
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
LABELS = ROOT / "channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/prepared_labels_v13"
SOURCES = OUT / "source_images"
CANVAS = (1080, 1920)
ROW_CENTERS = (1304, 1426, 1560)
ROW_HEIGHTS = (96, 96, 108)
X_CENTER = 540

ITEMS = [
    (
        "01_jfk",
        "John F. Kennedy — IQ 119",
        SOURCES / "01_jfk.png",
        "john_f_kennedy_text_group.png",
    ),
    (
        "02_kasparov",
        "Garry Kasparov — IQ 123",
        SOURCES / "02_kasparov.png",
        "kasparov_text_group.png",
    ),
    (
        "03_kanye",
        "Kanye West — IQ 133",
        SOURCES / "03_kanye.png",
        "kanye_west_text_group.png",
    ),
    (
        "04_marilyn",
        "Marilyn vos Savant — IQ 228",
        SOURCES / "04_marilyn.png",
        "marilyn_text_group.png",
    ),
]


def row_spans(alpha: Image.Image):
    active = []
    for y in range(alpha.height):
        active.append(alpha.crop((0, y, alpha.width, y + 1)).getbbox() is not None)
    spans = []
    start = None
    for y, is_active in enumerate(active + [False]):
        if is_active and start is None:
            start = y
        elif not is_active and start is not None:
            spans.append((start, y))
            start = None
    return spans


def prepare_scene(source: Path, output: Path):
    image = Image.open(source).convert("RGB")
    image = ImageOps.fit(image, CANVAS, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    image.save(output)
    return image.convert("RGBA")


def prepare_title(source: Path, output: Path):
    group = Image.open(source).convert("RGBA")
    spans = row_spans(group.getchannel("A"))
    if len(spans) != 3:
        raise ValueError(f"Expected three title rows in {source.name}, found {spans}")

    title = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    for (start, end), height, center_y in zip(spans, ROW_HEIGHTS, ROW_CENTERS):
        row = group.crop((0, start, group.width, end))
        bbox = row.getchannel("A").getbbox()
        if bbox is None:
            continue
        row = row.crop(bbox)
        width = max(1, round(row.width * height / row.height))
        row = row.resize((width, height), Image.Resampling.LANCZOS)
        x = X_CENTER - width // 2
        y = center_y - height // 2
        title.alpha_composite(row, (x, y))

    title.save(output)
    return title


def main():
    previews = []
    for stem, label, scene_source, title_filename in ITEMS:
        scene_path = OUT / f"{stem}_scene.png"
        title_path = OUT / f"{stem}_title.png"
        preview_path = OUT / f"{stem}_preview.png"
        scene = prepare_scene(scene_source, scene_path)
        title = prepare_title(LABELS / title_filename, title_path)
        composite = Image.alpha_composite(scene, title).convert("RGB")
        composite.save(preview_path, quality=96)
        previews.append((label, composite))

    tile = (486, 864)
    gutter = 24
    contact = Image.new("RGB", (tile[0] * 2 + gutter * 3, tile[1] * 2 + gutter * 3), (238, 231, 215))
    for i, (_label, image) in enumerate(previews):
        x = gutter + (i % 2) * (tile[0] + gutter)
        y = gutter + (i // 2) * (tile[1] + gutter)
        contact.paste(image.resize(tile, Image.Resampling.LANCZOS), (x, y))
    contact.save(OUT / "contact_4_pairs.jpg", quality=94)


if __name__ == "__main__":
    main()
