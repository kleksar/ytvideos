from __future__ import annotations

import csv
import json
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps


EPISODE = Path(__file__).resolve().parents[1]
SCENES = EPISODE / "Source" / "Images"
CUE_DIR = SCENES / "Text_Cues_EN_v01"
PREFLIGHT_DIR = EPISODE / "Storyboard" / "Text_Cue_Preflight_EN_v01"
REFERENCE = (
    EPISODE.parents[2]
    / "new_channel"
    / "videos"
    / "001_radio_game"
    / "Source"
    / "Images"
    / "accent_typography_v2"
    / "MATCH.png"
)
FONT_PATH = Path("/System/Library/Fonts/SFNSRounded.ttf")
FONT_VARIATION = "Black"

CANVAS = (941, 1672)
SUPERSAMPLE = 4
BASE_FONT_PX = 100
PRIMARY_CENTER = (0.50, 0.13)
ALT_S11_CENTER = (0.35, 0.17)
PRIMARY_SAFE_WIDTH_PX = round(CANVAS[0] * 0.90)
ALT_S11_SAFE_WIDTH_PX = round(CANVAS[0] * 0.70)
CREAM = (238, 200, 155)
ORANGE = (234, 79, 22)
EXTRUSION = (145, 45, 22)
SHADOW = (36, 17, 13)

CUES = [
    {
        "id": "S01",
        "scene": "S01_Ahmad_Answer_v01.png",
        "filename": "CUE_S01_Answer_EN_v01.png",
        "text": "Of course. I'm good at it.",
        "lines": ["Of course.", "I'm good at it."],
        "zone": "primary",
        "center": PRIMARY_CENTER,
        "cue_role": "Ahmad's answer; loops from S11's question.",
    },
    {
        "id": "S02",
        "scene": "S02_King_Order_v01.png",
        "filename": "CUE_S02_Answer_Price_EN_v01.png",
        "text": "The Price of One Answer",
        "lines": ["The Price of", "One Answer"],
        "zone": "primary",
        "center": PRIMARY_CENTER,
        "cue_role": "Frames the cost of Ahmad's answer.",
    },
    {
        "id": "S04",
        "scene": "S04_Ahmad_Model_Detail_v01.png",
        "filename": "CUE_S04_Years_Of_Precision_EN_v01.png",
        "text": "22 Years of Precision",
        "lines": ["22 Years of Precision"],
        "zone": "primary",
        "center": PRIMARY_CENTER,
        "cue_role": "Compresses the painstaking construction span.",
    },
    {
        "id": "S06",
        "scene": "S06_King_No_Repetition_v01.png",
        "filename": "CUE_S06_No_Repetition_EN_v01.png",
        "text": "No One Else Could Replicate It",
        "lines": ["No One Else", "Could Replicate It"],
        "zone": "primary",
        "center": PRIMARY_CENTER,
        "cue_role": "States the king's motive for the order.",
    },
    {
        "id": "S08",
        "scene": "S08_Work_Out_Of_Reach_v01.png",
        "filename": "CUE_S08_Work_Out_Of_Reach_EN_v01.png",
        "text": "A Craft Beyond His Reach",
        "lines": ["A Craft Beyond", "His Reach"],
        "zone": "primary",
        "center": PRIMARY_CENTER,
        "cue_role": "Contrasts the master craftsman's skill with his loss of ability.",
    },
    {
        "id": "S10",
        "scene": "S10_Ahmad_Behind_Masterpiece_v01.png",
        "filename": "CUE_S10_Person_Behind_Masterpiece_EN_v01.png",
        "text": "Behind the Masterpiece: A Man",
        "lines": ["Behind the", "Masterpiece: A Man"],
        "zone": "primary",
        "center": PRIMARY_CENTER,
        "cue_role": "Turns the Taj Mahal back into a human story.",
    },
    {
        "id": "S11",
        "scene": "S11_King_Question_v03.png",
        "filename": "CUE_S11_King_Question_EN_v01.png",
        "text": "Will You Keep Working as an Architect?",
        "lines": ["Will You Keep", "Working as an", "Architect?"],
        "zone": "alternate_left",
        "center": ALT_S11_CENTER,
        "cue_role": "The king's question that loops into Ahmad's opening answer.",
    },
]


def shifted(mask: Image.Image, dx: int, dy: int) -> Image.Image:
    out = Image.new("L", mask.size, 0)
    out.paste(mask, (dx, dy))
    return out


def mask_bbox(mask: Image.Image, threshold: int = 30):
    return mask.point(lambda a: 255 if a > threshold else 0).getbbox()


def is_face_pixel(r: int, g: int, b: int, a: int) -> bool:
    return (
        a > 30
        and r > 160
        and g > 110
        and b > 70
        and g > 0.58 * r
        and b > 0.50 * g
    )


def load_font(font_px: int):
    font = ImageFont.truetype(str(FONT_PATH), font_px)
    font.set_variation_by_name(FONT_VARIATION.encode())
    return font


def face_bbox(image: Image.Image):
    arr = np.asarray(image.convert("RGBA"))
    r, g, b, a = (arr[:, :, i] for i in range(4))
    mask = (
        (a > 30)
        & (r > 160)
        & (g > 110)
        & (b > 70)
        & (g > 0.58 * r)
        & (b > 0.50 * g)
    )
    ys, xs = np.where(mask)
    if len(xs) == 0:
        raise ValueError("No cream-face pixels found in rendered cue.")
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def face_cap_height(image: Image.Image) -> int:
    arr = np.asarray(image.convert("RGBA"))
    r, g, b, a = (arr[:, :, i] for i in range(4))
    mask = (
        (a > 30)
        & (r > 160)
        & (g > 110)
        & (b > 70)
        & (g > 0.58 * r)
        & (b > 0.50 * g)
    )
    rows = np.where(mask.any(axis=1))[0]
    if len(rows) == 0:
        raise ValueError("No cream-face pixels found in rendered cue.")
    breaks = np.where(np.diff(rows) > 1)[0]
    starts = np.r_[rows[0], rows[breaks + 1]]
    ends = np.r_[rows[breaks], rows[-1]]
    return int(np.max(ends - starts + 1))


def get_reference_face_patch(seed: int) -> Image.Image:
    ref = Image.open(REFERENCE).convert("RGBA")
    arr = np.asarray(ref)
    r, g, b, a = (arr[:, :, i] for i in range(4))
    mask = (
        (a > 30)
        & (r > 160)
        & (g > 110)
        & (b > 70)
        & (g > 0.58 * r)
        & (b > 0.50 * g)
    )
    rng = np.random.default_rng(seed)
    patch = 112
    for _ in range(2500):
        x = int(rng.integers(0, ref.width - patch))
        y = int(rng.integers(0, ref.height - patch))
        if mask[y : y + patch, x : x + patch].mean() > 0.995:
            tile = ref.crop((x, y, x + patch, y + patch)).convert("RGB")
            if rng.integers(0, 2):
                tile = ImageOps.mirror(tile)
            if rng.integers(0, 2):
                tile = ImageOps.flip(tile)
            return tile
    raise ValueError("Could not find a clean paper-face texture patch in MATCH.png")


def tiled_texture(size, seed: int, base_color):
    width, height = size
    rng = random.Random(seed)
    tile = get_reference_face_patch(seed)
    texture = Image.new("RGB", (width, height), base_color)
    tile_w = tile.width
    tile_h = tile.height
    start_x = -rng.randrange(tile_w)
    start_y = -rng.randrange(tile_h)
    y = start_y
    row = 0
    while y < height:
        x = start_x - (tile_w // 2 if row % 2 else 0)
        while x < width:
            variant = tile
            if (row + x) % 2:
                variant = ImageOps.mirror(variant)
            texture.paste(variant, (x, y))
            x += tile_w
        y += tile_h
        row += 1

    # Keep the channel-reference paper grain while softening obvious tile seams.
    texture = texture.filter(ImageFilter.GaussianBlur(radius=0.4))
    arr = np.asarray(texture).astype(np.int16)
    noise = np.random.default_rng(seed + 123).normal(0, 1.6, (height, width, 1))
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def render_text_mask(lines, seed: int, font_px: int):
    scale = SUPERSAMPLE
    font = load_font(font_px * scale)
    line_metrics = []
    max_width = 0
    for line in lines:
        bbox = font.getbbox(line)
        width = int(round(font.getlength(line)))
        height = bbox[3] - bbox[1]
        line_metrics.append((bbox, width, height))
        max_width = max(max_width, width)

    line_gap = 8 * scale
    pad = 30 * scale
    total_height = sum(item[2] for item in line_metrics) + line_gap * (len(lines) - 1)
    canvas = Image.new(
        "L",
        (max_width + pad * 2, total_height + pad * 2),
        0,
    )
    draw = ImageDraw.Draw(canvas)
    current_y = pad
    for line, (bbox, width, height) in zip(lines, line_metrics):
        left = pad + (max_width - width) // 2
        draw.text((left - bbox[0], current_y - bbox[1]), line, fill=255, font=font)
        current_y += height + line_gap

    # Create paper-like depth: soft contact shadow, warm card extrusion, orange cut edge.
    shadow = shifted(canvas, 3 * scale, 5 * scale).filter(
        ImageFilter.GaussianBlur(radius=2 * scale)
    )
    extrusion = Image.new("L", canvas.size, 0)
    for dx, dy in ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)):
        extrusion = ImageChops.lighter(extrusion, shifted(canvas, dx * scale, dy * scale))
    outline = canvas.filter(ImageFilter.MaxFilter(2 * (3 * scale) + 1))

    out = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_rgba = Image.new("RGBA", canvas.size, SHADOW + (0,))
    shadow_rgba.putalpha(shadow.point(lambda a: int(a * 0.62)))
    out = Image.alpha_composite(out, shadow_rgba)

    extrusion_rgba = Image.new("RGBA", canvas.size, EXTRUSION + (0,))
    extrusion_rgba.putalpha(extrusion)
    out = Image.alpha_composite(out, extrusion_rgba)

    orange_rgba = Image.new("RGBA", canvas.size, ORANGE + (0,))
    orange_rgba.putalpha(outline)
    out = Image.alpha_composite(out, orange_rgba)

    face_texture = tiled_texture(canvas.size, seed, CREAM).convert("RGBA")
    face_texture.putalpha(canvas)
    out = Image.alpha_composite(out, face_texture)

    # Downsample only after bevel, texture, and shadow have been assembled.
    out = out.resize(
        (int(round(out.width / scale)), int(round(out.height / scale))),
        Image.Resampling.LANCZOS,
    )
    alpha = out.getchannel("A")
    bbox = mask_bbox(alpha)
    if bbox is None:
        raise ValueError("Rendered cue has no visible pixels")
    crop_pad = 4
    left = max(0, bbox[0] - crop_pad)
    top = max(0, bbox[1] - crop_pad)
    right = min(out.width, bbox[2] + crop_pad)
    bottom = min(out.height, bbox[3] + crop_pad)
    return out.crop((left, top, right, bottom))


def cue_metrics(image: Image.Image):
    alpha = image.getchannel("A")
    alpha_box = mask_bbox(alpha)
    face_box = face_bbox(image)
    if alpha_box is None:
        raise ValueError("No alpha bounds in cue")
    return {
        "width": image.width,
        "height": image.height,
        "alpha_bbox": alpha_box,
        "alpha_width": alpha_box[2] - alpha_box[0],
        "face_bbox": face_box,
        "face_bbox_height": face_box[3] - face_box[1],
        "face_cap_height": face_cap_height(image),
        "face_width": face_box[2] - face_box[0],
    }


def normalize_face_height(image: Image.Image, target_height: int) -> Image.Image:
    out = image
    for _ in range(4):
        actual = cue_metrics(out)["face_cap_height"]
        if actual == target_height:
            return out
        factor = target_height / actual
        size = (
            max(1, int(round(out.width * factor))),
            max(1, int(round(out.height * factor))),
        )
        out = out.resize(size, Image.Resampling.LANCZOS)
    return out


def composite_at_anchor(scene: Image.Image, cue: Image.Image, center, face_box):
    image = scene.convert("RGBA").copy()
    center_x = round(center[0] * image.width)
    center_y = round(center[1] * image.height)
    face_center_x = (face_box[0] + face_box[2]) / 2
    face_center_y = (face_box[1] + face_box[3]) / 2
    left = round(center_x - face_center_x)
    top = round(center_y - face_center_y)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    layer.alpha_composite(cue, (left, top))
    return Image.alpha_composite(image, layer), (left, top)


def main():
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"Mockup typeface not found: {FONT_PATH}")
    if not REFERENCE.exists():
        raise FileNotFoundError(f"Paper typography reference not found: {REFERENCE}")
    if CUE_DIR.exists() or PREFLIGHT_DIR.exists():
        raise FileExistsError("Versioned output already exists; create the next version.")

    base_cues = []
    safe_widths = []
    cap_candidates = []
    for index, cue_spec in enumerate(CUES, start=1):
        scene_path = SCENES / cue_spec["scene"]
        if not scene_path.exists():
            raise FileNotFoundError(scene_path)
        with Image.open(scene_path) as scene:
            if scene.size != CANVAS:
                raise ValueError(
                    f"Unexpected scene dimensions for {scene_path.name}: {scene.size}"
                )

        base_cue = render_text_mask(
            cue_spec["lines"], seed=20261101 + index, font_px=BASE_FONT_PX
        )
        metrics = cue_metrics(base_cue)
        safe_width = (
            ALT_S11_SAFE_WIDTH_PX
            if cue_spec["zone"] == "alternate_left"
            else PRIMARY_SAFE_WIDTH_PX
        )
        cap_candidates.append(
            safe_width * metrics["face_cap_height"] / metrics["alpha_width"]
        )
        safe_widths.append(safe_width)
        base_cues.append(base_cue)

    # Pick one shared visible face height from the tightest safe-width constraint.
    target_face_height = int(min(cap_candidates) // 10 * 10)
    if target_face_height < 30:
        raise ValueError(f"Derived cap height is too small: {target_face_height}px")

    final_cues = []
    while target_face_height >= 30:
        final_cues = [
            normalize_face_height(cue, target_face_height) for cue in base_cues
        ]
        final_metrics = [cue_metrics(cue) for cue in final_cues]
        if all(
            metric["alpha_width"] <= safe_width
            for metric, safe_width in zip(final_metrics, safe_widths)
        ):
            break
        target_face_height -= 10
    else:
        raise ValueError("Could not fit all cue layers inside the safe-width limits.")

    CUE_DIR.mkdir(parents=True)
    PREFLIGHT_DIR.mkdir(parents=True)
    rows = []
    previews = []

    for cue_spec, cue, safe_width in zip(CUES, final_cues, safe_widths):
        scene_path = SCENES / cue_spec["scene"]
        scene = Image.open(scene_path).convert("RGBA")
        metrics = cue_metrics(cue)
        if metrics["alpha_width"] > safe_width:
            raise ValueError(
                f"{cue_spec['id']} alpha width {metrics['alpha_width']} exceeds "
                f"the {cue_spec['zone']} safe width {safe_width}px"
            )

        cue_path = CUE_DIR / cue_spec["filename"]
        cue.save(cue_path)
        preview, position = composite_at_anchor(scene, cue, cue_spec["center"], metrics["face_bbox"])
        preview_path = PREFLIGHT_DIR / f"{cue_spec['id']}_preview_EN_v01.png"
        preview.save(preview_path)

        row = {
            **cue_spec,
            "lines": cue_spec["lines"],
            "center_x": cue_spec["center"][0],
            "center_y": cue_spec["center"][1],
            "safe_width_px": safe_width,
            "font_file": FONT_PATH.name,
            "font_variation": FONT_VARIATION,
            "font_size_source_px": BASE_FONT_PX,
            "target_face_height_px": target_face_height,
            "measured": metrics,
            "layer_top_left_px": position,
            "cue_path": str(cue_path),
            "preview_path": str(preview_path),
            "timing_status": "PENDING — no accepted English narration/recording/alignment",
            "asset_status": "STATIC VISUAL MOCKUP — not imported",
        }
        rows.append(row)
        previews.append((cue_spec["id"], preview))

    (PREFLIGHT_DIR / "manifest.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (PREFLIGHT_DIR / "manifest.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "ID",
                "exact_text",
                "line_breaks",
                "zone",
                "center_x",
                "center_y",
                "safe_width_px",
                "alpha_width_px",
                "face_cap_height_px",
                "face_bbox_height_px",
                "line_count",
                "cue_png",
                "preview_png",
                "timing_status",
            ]
        )
        for row in rows:
            m = row["measured"]
            writer.writerow(
                [
                    row["id"],
                    row["text"],
                    " / ".join(row["lines"]),
                    row["zone"],
                    row["center_x"],
                    row["center_y"],
                    row["safe_width_px"],
                    m["alpha_width"],
                    m["face_cap_height"],
                    m["face_bbox_height"],
                    len(row["lines"]),
                    row["cue_path"],
                    row["preview_path"],
                    row["timing_status"],
                ]
            )

    # Overview only: every full-size preview is also saved and must be reviewed individually.
    thumb_w = 270
    thumb_h = round(thumb_w * CANVAS[1] / CANVAS[0])
    label_h = 34
    cols = 3
    rows_n = (len(previews) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows_n * (thumb_h + label_h)), (20, 30, 45))
    label_font = load_font(18)
    draw = ImageDraw.Draw(sheet)
    for i, (scene_id, preview) in enumerate(previews):
        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + label_h)
        thumb = preview.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.text((x + 8, y + thumb_h + 7), scene_id, font=label_font, fill=(242, 226, 202))
    sheet.save(PREFLIGHT_DIR / "CONTACT_SHEET_preview_EN_v01.jpg", quality=92)

    phone_w = 360
    phone_h = round(phone_w * CANVAS[1] / CANVAS[0])
    phone_label_h = 40
    phone_cols = 2
    phone_rows = (len(previews) + phone_cols - 1) // phone_cols
    phone_sheet = Image.new(
        "RGB",
        (phone_cols * phone_w, phone_rows * (phone_h + phone_label_h)),
        (20, 30, 45),
    )
    phone_font = load_font(22)
    phone_draw = ImageDraw.Draw(phone_sheet)
    for i, (scene_id, preview) in enumerate(previews):
        x = (i % phone_cols) * phone_w
        y = (i // phone_cols) * (phone_h + phone_label_h)
        thumb = preview.convert("RGB").resize((phone_w, phone_h), Image.Resampling.LANCZOS)
        phone_sheet.paste(thumb, (x, y))
        phone_draw.text(
            (x + 12, y + phone_h + 8), scene_id, font=phone_font, fill=(242, 226, 202)
        )
    phone_sheet.save(PREFLIGHT_DIR / "PHONE_CONTACT_SHEET_preview_EN_v01.jpg", quality=94)

    print(f"Wrote {len(rows)} transparent cue mockups to {CUE_DIR}")
    print(f"Wrote {len(rows)} full-size composites to {PREFLIGHT_DIR}")
    print(f"Shared target cap height: {target_face_height}px")
    for row in rows:
        m = row["measured"]
        print(
            f"{row['id']}: alpha={m['alpha_width']}x{m['height']} "
            f"cap_h={m['face_cap_height']} group_h={m['face_bbox_height']} "
            f"center=({row['center_x']:.2f},{row['center_y']:.2f}) "
            f"zone={row['zone']}"
        )


if __name__ == "__main__":
    main()
