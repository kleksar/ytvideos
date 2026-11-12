#!/usr/bin/env python3
"""Build a reproducible IQ Gallery manifest from an explicit cast JSON.

Only derived title PNGs and the manifest are written. Source artworks are read-only.
Requires Pillow for alpha-trimming the generated paper-title images.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import tempfile

try:
    from PIL import Image, ImageChops, ImageDraw
except ImportError as exc:  # pragma: no cover - environment diagnostic
    raise SystemExit("Pillow is required to trim transparent paper title assets") from exc


HERE = pathlib.Path(__file__).resolve().parent
CAST_FILE = HERE / "cast_v3.json"
DEFAULT_MANIFEST = HERE / "iq_gallery_v3_manifest.json"


def require_file(path: pathlib.Path, label: str) -> pathlib.Path:
    if not path.is_file():
        raise SystemExit(f"{label}: missing file: {path}")
    return path.resolve()


def absolute_from_workflow(value: str, label: str) -> pathlib.Path:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{label}: path is required")
    return require_file((HERE / value).expanduser().resolve(), label)


def absolute_dir_from_workflow(value: str, label: str) -> pathlib.Path:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{label}: directory is required")
    path = (HERE / value).expanduser().resolve()
    if not path.is_dir():
        raise SystemExit(f"{label}: missing directory: {path}")
    return path


def trim_png(source: pathlib.Path, destination: pathlib.Path) -> tuple[int, int]:
    """Trim transparent padding without changing visible pixels or source art."""
    try:
        with Image.open(source) as im:
            im.load()
            rgba = im.convert("RGBA")
    except Exception as exc:
        raise SystemExit(f"cannot decode PNG {source}: {exc}") from exc
    alpha = rgba.getchannel("A")
    visible = alpha.point(lambda value: 255 if value > 8 else 0)
    bbox = visible.getbbox()
    if not bbox:
        raise SystemExit(f"no visible alpha pixels in {source}")
    cropped = rgba.crop(bbox)
    destination.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(destination, format="PNG", optimize=True)
    return cropped.size


def add_letter_tracking(word_image: Image.Image, char_count: int, spacing_px: int,
                       display_name: str, word: str) -> Image.Image:
    """Separate touching paper glyphs along dark seams, preserving each source pixel."""
    if char_count <= 1 or spacing_px <= 0:
        return word_image
    width, height = word_image.size
    if len(word) != char_count:
        raise SystemExit(f"{display_name}: character count mismatch while tracking {word}")

    # Character width priors center the seam search near likely letter boundaries.
    # They guide the search only; the final cut follows the darkest continuous path.
    weights = {"I": 0.38, "J": 0.78, "L": 0.68, "F": 0.74, "T": 0.74,
               "M": 1.18, "W": 1.25, "-": 0.45, "'": 0.35, "’": 0.35}
    char_weights = [weights.get(character, 1.0) for character in word]
    weight_total = sum(char_weights)
    targets = []
    cumulative = 0.0
    for value in char_weights[:-1]:
        cumulative += value
        targets.append(round(width * cumulative / weight_total))

    # Alpha-weighted luminance prefers transparent or dark outline/shadow pixels.
    pixels = word_image.load()
    costs = []
    for y in range(height):
        row = []
        for x in range(width):
            red, green, blue, alpha = pixels[x, y]
            opacity = alpha / 255.0
            luminance = (0.2126 * red + 0.7152 * green + 0.0722 * blue) / 255.0
            row.append(opacity * (0.15 + 0.85 * luminance))
        costs.append(row)

    seams = []
    average_width = width / char_count
    for target in targets:
        radius = max(6, round(average_width * 0.30))
        left = max(1, target - radius)
        right = min(width - 1, target + radius + 1)
        band_width = right - left
        if band_width < 3:
            raise SystemExit(f"{display_name}: no safe tracking band at {word}")

        center_penalty = 0.0008
        step_penalty = 0.006
        previous = [
            costs[0][left + x] + center_penalty * abs(left + x - target)
            for x in range(band_width)
        ]
        predecessors = []
        for y in range(1, height):
            current = [0.0] * band_width
            back = [0] * band_width
            for x in range(band_width):
                begin = max(0, x - 2)
                end = min(band_width, x + 3)
                best_index = min(
                    range(begin, end),
                    key=lambda prior: previous[prior] + step_penalty * abs(prior - x),
                )
                absolute_x = left + x
                current[x] = (
                    costs[y][absolute_x]
                    + center_penalty * abs(absolute_x - target)
                    + previous[best_index]
                    + step_penalty * abs(best_index - x)
                )
                back[x] = best_index
            previous = current
            predecessors.append(back)

        band_x = min(range(band_width), key=previous.__getitem__)
        path = [left + band_x]
        for row_index in range(height - 2, -1, -1):
            band_x = predecessors[row_index][band_x]
            path.append(left + band_x)
        path.reverse()
        seam_cost = sum(costs[y][x] for y, x in enumerate(path)) / height
        if seam_cost > 0.38:
            raise SystemExit(
                f"{display_name}: cannot find a clean letter seam in {word} "
                f"(average seam cost {seam_cost:.3f})"
            )
        seams.append(path)

    for y in range(height):
        if any(right[y] - left[y] < 2 for left, right in zip(seams, seams[1:])):
            raise SystemExit(f"{display_name}: letter seams cross in {word}")

    transparent = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    output = Image.new("RGBA", (width + spacing_px * (char_count - 1), height), (0, 0, 0, 0))
    for index in range(char_count):
        mask = Image.new("L", (width, height), 0)
        draw = ImageDraw.Draw(mask)
        for y in range(height):
            x0 = 0 if index == 0 else seams[index - 1][y] + 1
            x1 = width if index == char_count - 1 else seams[index][y] + 1
            if x1 > x0:
                draw.line((x0, y, x1 - 1, y), fill=255)
        piece = Image.composite(word_image, transparent, mask)
        bbox = piece.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
        if not bbox:
            raise SystemExit(f"{display_name}: empty letter segment in {word}")
        piece = piece.crop(bbox)
        output.alpha_composite(piece, (bbox[0] + index * spacing_px, bbox[1]))
    return output


def stack_name_png(
    source: pathlib.Path,
    destination: pathlib.Path,
    display_name: str,
    line_texts: list[str],
    max_width: int,
    max_line_height: int,
    line_gap: int,
    letter_spacing_em: float = 0.0,
) -> tuple[int, int]:
    """Wrap existing tracked title art at word spaces; do not redraw its letters."""
    if not line_texts or any(not isinstance(line, str) or not line.strip() for line in line_texts):
        raise SystemExit(f"{display_name}: name_lines must be nonempty strings")
    source_words = display_name.split()
    requested_words = [word for line in line_texts for word in line.split()]
    if requested_words != source_words:
        raise SystemExit(f"{display_name}: name_lines must preserve the exact word order and spelling")
    try:
        with Image.open(source) as im:
            im.load()
            rgba = im.convert("RGBA")
    except Exception as exc:
        raise SystemExit(f"cannot decode title PNG {source}: {exc}") from exc

    alpha = rgba.getchannel("A")
    visible = alpha.point(lambda value: 255 if value > 8 else 0)
    bbox = visible.getbbox()
    if not bbox:
        raise SystemExit(f"no visible title pixels in {source}")
    rgba = rgba.crop(bbox)
    visible = visible.crop(bbox)
    width, height = rgba.size
    expected_spaces = len(source_words) - 1

    # A source title is one line. Long fully transparent column runs mark word spaces;
    # short intra-letter gaps are left intact so the generated paper lettering survives.
    projection = visible.resize((width, 1), Image.Resampling.BOX)
    active = [projection.getpixel((x, 0)) > 0 for x in range(width)]
    min_word_gap = max(12, round(width * 0.01))
    gaps = []
    x = 0
    while x < width:
        if active[x]:
            x += 1
            continue
        end = x
        while end < width and not active[end]:
            end += 1
        if end - x >= min_word_gap:
            gaps.append((x, end))
        x = end
    if expected_spaces == 0:
        gaps = []
    if len(gaps) != expected_spaces:
        raise SystemExit(
            f"{display_name}: expected {expected_spaces} visible word gaps, found {len(gaps)} in {source}"
        )

    word_boxes = []
    begin = 0
    for gap_start, gap_end in gaps:
        word_boxes.append((begin, gap_start))
        begin = gap_end
    word_boxes.append((begin, width))

    if not isinstance(letter_spacing_em, (int, float)) or not 0 <= letter_spacing_em <= 0.08:
        raise SystemExit(f"{display_name}: name_letter_spacing_em must be 0..0.08")
    tracking_px = round(height * letter_spacing_em)
    line_images = []
    word_index = 0
    for line in line_texts:
        line_words = line.split()
        line_parts = []
        for line_word_index, word in enumerate(line_words):
            left, right = word_boxes[word_index]
            part = rgba.crop((left, 0, right, height))
            part = add_letter_tracking(part, len(word), tracking_px, display_name, word)
            line_parts.append(part)
            if line_word_index < len(line_words) - 1:
                gap_width = gaps[word_index][1] - gaps[word_index][0]
                line_parts.append(Image.new("RGBA", (gap_width, height), (0, 0, 0, 0)))
            word_index += 1
        line_width = sum(part.width for part in line_parts)
        part = Image.new("RGBA", (line_width, height), (0, 0, 0, 0))
        cursor_x = 0
        for line_part in line_parts:
            part.alpha_composite(line_part, (cursor_x, 0))
            cursor_x += line_part.width
        part_alpha = part.getchannel("A").point(lambda value: 255 if value > 8 else 0)
        part_bbox = part_alpha.getbbox()
        if not part_bbox:
            raise SystemExit(f"{display_name}: empty wrapped word group: {line}")
        part = part.crop(part_bbox)
        aspect = part.width / part.height
        target_width = min(max_width, max_line_height * aspect)
        target_height = target_width / aspect
        new_size = (max(1, round(target_width)), max(1, round(target_height)))
        part = part.resize(new_size, Image.Resampling.LANCZOS)
        line_images.append(part)

    canvas_width = max(part.width for part in line_images)
    canvas_height = sum(part.height for part in line_images) + line_gap * (len(line_images) - 1)
    canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
    cursor_y = 0
    for part in line_images:
        cursor_x = (canvas_width - part.width) // 2
        canvas.alpha_composite(part, (cursor_x, cursor_y))
        cursor_y += part.height + line_gap
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, format="PNG", optimize=True)
    return canvas.size


def image_aspect(path: pathlib.Path) -> float:
    with Image.open(path) as im:
        im.load()
        if im.mode != "RGBA" and "A" not in im.getbands():
            raise SystemExit(f"alpha channel required: {path}")
        width, height = im.size
    if width <= 0 or height <= 0:
        raise SystemExit(f"invalid image size: {path}")
    return width / height


def fit_box(path: pathlib.Path, max_width: float, max_height: float) -> tuple[float, float]:
    aspect = image_aspect(path)
    width = min(max_width, max_height * aspect)
    height = width / aspect
    return round(width, 2), round(height, 2)


def compose_text_group_png(
    glyphs: list[dict], destination: pathlib.Path, group_label: str, padding: int = 18
) -> dict:
    """Composite the name and IQ score into one movable transparent title group."""
    canvas = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    for glyph in glyphs:
        try:
            with Image.open(glyph["file"]) as im:
                im.load()
                layer = im.convert("RGBA")
        except Exception as exc:
            raise SystemExit(f"cannot decode title group input {glyph['file']}: {exc}") from exc
        target_size = (max(1, round(glyph["w"])), max(1, round(glyph["h"])))
        if layer.size != target_size:
            layer = layer.resize(target_size, Image.Resampling.LANCZOS)
        x, y = round(glyph["x"]), round(glyph["y"])
        if x < 0 or y < 0 or x + layer.width > canvas.width or y + layer.height > canvas.height:
            raise SystemExit(f"title group element exceeds the frame: {glyph['char']}")
        canvas.alpha_composite(layer, (x, y))

    alpha = canvas.getchannel("A").point(lambda value: 255 if value > 8 else 0)
    bbox = alpha.getbbox()
    if not bbox:
        raise SystemExit("cannot compose an empty title group")
    left = max(0, bbox[0] - padding)
    top = max(0, bbox[1] - padding)
    right = min(canvas.width, bbox[2] + padding)
    bottom = min(canvas.height, bbox[3] + padding)
    group = canvas.crop((left, top, right, bottom))
    destination.parent.mkdir(parents=True, exist_ok=True)
    group.save(destination, format="PNG", optimize=True)
    return {
        "kind": "group",
        "char": group_label,
        "file": str(destination.resolve()),
        "x": left,
        "y": top,
        "w": group.width,
        "h": group.height,
    }


def make_polygon_overlay(
    source: pathlib.Path,
    destination: pathlib.Path,
    polygon_px: list[list[int]],
    label: str,
) -> tuple[int, int]:
    """Copy an existing layer region into a transparent overlay without redrawing pixels."""
    try:
        with Image.open(source) as im:
            im.load()
            rgba = im.convert("RGBA")
    except Exception as exc:
        raise SystemExit(f"cannot decode occlusion overlay source {source}: {exc}") from exc

    if not isinstance(polygon_px, list) or len(polygon_px) < 3:
        raise SystemExit(f"{label}: polygon_px must contain at least three points")
    width, height = rgba.size
    points: list[tuple[int, int]] = []
    for point in polygon_px:
        if (
            not isinstance(point, list)
            or len(point) != 2
            or type(point[0]) is not int
            or type(point[1]) is not int
        ):
            raise SystemExit(f"{label}: polygon_px points must be integer [x, y] pairs")
        x, y = point
        if not 0 <= x < width or not 0 <= y < height:
            raise SystemExit(f"{label}: polygon point {(x, y)} exceeds source canvas {width}x{height}")
        points.append((x, y))

    # Supersampling softens only the polygon boundary; source RGB and source alpha remain intact.
    supersample = 4
    mask_hi = Image.new("L", (width * supersample, height * supersample), 0)
    ImageDraw.Draw(mask_hi).polygon(
        [(x * supersample, y * supersample) for x, y in points], fill=255
    )
    mask = mask_hi.resize((width, height), Image.Resampling.LANCZOS)
    rgba.putalpha(ImageChops.multiply(rgba.getchannel("A"), mask))
    if not rgba.getchannel("A").getbbox():
        raise SystemExit(f"{label}: polygon contains no visible source pixels")

    destination.parent.mkdir(parents=True, exist_ok=True)
    rgba.save(destination, format="PNG", optimize=True)
    return rgba.size


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cast", type=pathlib.Path, default=CAST_FILE)
    parser.add_argument("--output", type=pathlib.Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--prepared-dir", type=pathlib.Path, default=pathlib.Path("prepared_labels"),
                        help="version-specific output folder for trimmed label PNGs")
    parser.add_argument("--force", action="store_true", help="replace only the generated manifest")
    args = parser.parse_args()

    cast_file = args.cast.expanduser().resolve()
    try:
        cast = json.loads(cast_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read cast JSON {cast_file}: {exc}") from exc
    if cast.get("schema_version") != 1:
        raise SystemExit("unsupported cast schema_version")
    scenes = cast.get("scenes")
    if not isinstance(scenes, list) or len(scenes) < 2:
        raise SystemExit("cast file must contain at least two scenes")
    duration_frames = cast.get("duration_frames", 1800)
    if type(duration_frames) is not int or duration_frames <= 0:
        raise SystemExit("duration_frames must be a positive integer")
    transition_frames = cast.get("transition_frames", 15)
    if type(transition_frames) is not int or not 1 <= transition_frames <= 30:
        raise SystemExit("transition_frames must be an integer from 1 to 30")
    base_frames, extra_frames = divmod(duration_frames, len(scenes))
    if base_frames <= transition_frames + 30:
        raise SystemExit("duration_frames gives each scene too little time")

    output = args.output.expanduser().resolve()
    if output.exists() and not args.force:
        raise SystemExit(f"refusing to overwrite {output}; pass --force to rebuild it")

    # Project-specific locations are resolved relative to this workflow folder.
    title_dir = absolute_dir_from_workflow(cast["title_assets"], "title_assets")
    digit_dir = absolute_dir_from_workflow(cast["digit_assets"], "digit_assets")
    iq_source = absolute_from_workflow(cast["iq_asset"], "iq_asset")
    audio = absolute_from_workflow(cast["audio"], "audio")
    grain = absolute_from_workflow(cast["grain"], "grain")
    out_value = cast.get("output")
    if not isinstance(out_value, str) or not out_value:
        raise SystemExit("output path is required in cast JSON")
    render_output = (HERE / out_value).resolve()
    if render_output.suffix.lower() != ".mp4":
        raise SystemExit("render output must end with .mp4")
    if not render_output.parent.is_dir():
        raise SystemExit(f"render output folder does not exist: {render_output.parent}")

    layout = cast.get("layout", {})
    prepared_value = args.prepared_dir.expanduser()
    prepared = (HERE / prepared_value).resolve() if not prepared_value.is_absolute() else prepared_value.resolve()
    iq_png = prepared / "iq.png"
    iq_size = trim_png(iq_source, iq_png)
    iq_aspect = iq_size[0] / iq_size[1]
    iq_h = float(layout.get("iq_max_height", 108))
    iq_w = min(float(layout.get("iq_max_width", 172)), iq_h * iq_aspect)
    digit_h = float(layout.get("iq_digit_height", 110))
    digit_gap = float(layout.get("digit_gap", 22))
    iq_gap = float(layout.get("iq_gap", 24))
    iq_x = float(layout.get("iq_x", 42))
    iq_y = float(layout.get("iq_y", 1142))
    iq_box_y = iq_y + (max(iq_h, digit_h) - iq_h) / 2

    manifest_scenes = []
    seen_slugs = set()
    for idx, scene in enumerate(scenes):
        slug = scene.get("slug")
        name = scene.get("display_name")
        score = scene.get("iq")
        if not isinstance(slug, str) or slug in seen_slugs:
            raise SystemExit(f"scenes[{idx}]: missing or duplicate slug")
        seen_slugs.add(slug)
        if not isinstance(name, str) or not name or name != name.upper():
            raise SystemExit(f"scenes[{idx}]: display_name must be exact uppercase text")
        if type(score) is not int or not 0 <= score <= 999:
            raise SystemExit(f"scenes[{idx}]: iq must be an integer")

        label_source = require_file(title_dir / scene["name_asset"], f"{slug} title")
        label_png = prepared / f"{slug}_name.png"
        label_size = stack_name_png(
            label_source,
            label_png,
            name,
            scene.get("name_lines", [name]),
            int(scene.get("name_max_width", layout.get("name_max_width", 480))),
            int(layout.get("name_line_max_height", 128)),
            int(layout.get("name_line_gap", 22)),
            float(scene.get("name_letter_spacing_em", layout.get("name_letter_spacing_em", 0.0))),
        )
        name_w, name_h = fit_box(
            label_png,
            float(scene.get("name_max_width", layout.get("name_max_width", 500))),
            float(scene.get("name_max_height", layout.get("name_max_height", 999))),
        )
        name_x = float(layout.get("name_x", 42))
        name_y = float(layout.get("name_y", 930))

        glyphs = [
            {
                "kind": "name",
                "char": name,
                "file": str(label_png.resolve()),
                "x": name_x,
                "y": name_y,
                "w": name_w,
                "h": name_h,
            },
            {
                "kind": "iq",
                "char": "IQ",
                "file": str(iq_png.resolve()),
                "x": iq_x,
                "y": round(iq_box_y, 2),
                "w": round(iq_w, 2),
                "h": round(iq_h, 2),
            },
        ]

        x = iq_x + iq_w + iq_gap
        for character in str(score):
            suffix = "reference" if character in "01" else "generated"
            digit_source = require_file(
                digit_dir / f"digit_{character}_{suffix}.png",
                f"digit {character}",
            )
            digit_png = prepared / f"digit_{character}.png"
            trim_png(digit_source, digit_png)
            aspect = image_aspect(digit_png)
            digit_w = digit_h * aspect
            digit_y = iq_y + (max(iq_h, digit_h) - digit_h) / 2
            glyphs.append(
                {
                    "kind": "digit",
                    "char": character,
                    "file": str(digit_png.resolve()),
                    "x": round(x, 2),
                    "y": round(digit_y, 2),
                    "w": round(digit_w, 2),
                    "h": digit_h,
                }
            )
            x += digit_w + digit_gap

        text_group = compose_text_group_png(
            glyphs, prepared / f"{slug}_text_group.png", f"{name} IQ {score}"
        )

        for field in ("background", "midground", "foreground"):
            scene[field] = str(absolute_from_workflow(scene[field], f"{slug}.{field}"))
        overlay_specs = scene.get("occlusion_overlays", [])
        if not isinstance(overlay_specs, list):
            raise SystemExit(f"{slug}.occlusion_overlays must be a list")
        occlusion_overlays = []
        seen_overlay_names = set()
        for overlay_index, overlay in enumerate(overlay_specs):
            overlay_label = f"{slug}.occlusion_overlays[{overlay_index}]"
            if not isinstance(overlay, dict):
                raise SystemExit(f"{overlay_label} must be an object")
            overlay_name = overlay.get("name")
            if (
                not isinstance(overlay_name, str)
                or not overlay_name
                or any(not (character.isalnum() or character in "_-") for character in overlay_name)
            ):
                raise SystemExit(f"{overlay_label}.name must contain only letters, digits, '_' or '-'")
            if overlay_name in seen_overlay_names:
                raise SystemExit(f"{slug}: duplicate occlusion overlay name {overlay_name}")
            seen_overlay_names.add(overlay_name)
            transform_layer = overlay.get("transform_layer", "midground")
            if transform_layer not in ("midground", "foreground"):
                raise SystemExit(f"{overlay_label}.transform_layer must be midground or foreground")
            source = pathlib.Path(scene[transform_layer])
            overlay_path = prepared / f"{slug}_occlusion_{overlay_name}.png"
            dimensions = make_polygon_overlay(
                source,
                overlay_path,
                overlay.get("polygon_px"),
                overlay_label,
            )
            occlusion_overlays.append({
                "name": overlay_name,
                "file": str(overlay_path.resolve()),
                "transform_layer": transform_layer,
                "source_dimensions": list(dimensions),
            })
        manifest_scenes.append(
            {
                "frames": base_frames + (1 if idx < extra_frames else 0),
                "background": scene["background"],
                "midground": scene["midground"],
                "foreground": scene["foreground"],
                "overscan_x": int(layout.get("overscan_x", 40)),
                "overscan_y": int(layout.get("overscan_y", 36)),
                "velocity_x": scene.get("velocity_x", layout.get("velocity_x", {"background": 6, "midground": -7, "foreground": 10})),
                "layer_scale": {
                    "midground": float(scene.get("midground_scale", layout.get("midground_scale", 0.74))),
                    "foreground": float(scene["foreground_scale"]),
                },
                "layer_anchor": {
                    "midground": scene.get("midground_anchor", layout.get("midground_anchor", "right_bottom")),
                    "foreground": scene["foreground_anchor"],
                },
                "layer_offset": {
                    "midground": scene.get("midground_offset", layout.get("midground_offset", {})),
                    "foreground": scene.get("foreground_offset", layout.get("foreground_offset", {})),
                },
                "entry": layout.get("entry", {"start": 0.45, "duration": 0.8, "rise": 650}),
                "foreground_anchor_side": scene.get("foreground_anchor_side"),
                "motion_direction": scene.get("motion_direction"),
                "direction_exception_reason": scene.get("direction_exception_reason"),
                "display_name": name,
                "iq_value": score,
                "name_letter_spacing_em": float(scene.get(
                    "name_letter_spacing_em", layout.get("name_letter_spacing_em", 0.0)
                )),
                "glyphs": glyphs,
                "text_group": text_group,
                "occlusion_overlays": occlusion_overlays,
            }
        )

    title_motion = cast.get("title_motion", {})
    if not isinstance(title_motion, dict):
        raise SystemExit("title_motion must be an object")
    manifest = {
        "output": str(render_output),
        "audio": str(audio),
        "grain": str(grain),
        "title_motion": title_motion,
        "direction_rules_version": cast.get("direction_rules_version"),
        "expected_frames": duration_frames,
        "transition_frames": transition_frames,
        "scenes": manifest_scenes,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=output.parent, prefix=f".{output.name}.", delete=False
    ) as tmp:
        temp_path = pathlib.Path(tmp.name)
        json.dump(manifest, tmp, ensure_ascii=False, indent=2)
        tmp.write("\n")
        tmp.flush()
        os.fsync(tmp.fileno())
    try:
        if output.exists() and not args.force:
            raise SystemExit(f"manifest appeared while building; refusing to replace {output}")
        os.replace(temp_path, output)
    finally:
        temp_path.unlink(missing_ok=True)

    print(
        json.dumps(
            {
                "manifest": str(output),
                "scenes": len(manifest_scenes),
                "frames": sum(scene["frames"] for scene in manifest_scenes),
                "seconds": sum(scene["frames"] for scene in manifest_scenes) / 30,
                "trimmed_labels": str(prepared.resolve()),
                "name_source_dimensions": label_size,
                "iq_source_dimensions": iq_size,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
