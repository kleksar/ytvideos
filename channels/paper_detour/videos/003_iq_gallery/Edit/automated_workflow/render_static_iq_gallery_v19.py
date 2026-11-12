#!/usr/bin/env python3
"""Build the unified one-minute Paper Detour IQ Gallery v19 from full-frame scenes."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[5]
FPS = 30
WIDTH = 1080
HEIGHT = 1920
SUPERSAMPLE = 3


def fail(message: str) -> None:
    raise SystemExit(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def resolve(value: str) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def run(command: list[str]) -> None:
    print("$", " ".join(command), flush=True)
    subprocess.run(command, check=True)


def probe(path: Path) -> dict[str, Any]:
    raw = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        text=True,
    )
    return json.loads(raw)


def normalize_scene(image_path: Path, face: dict[str, float], layout: dict[str, Any]) -> Image.Image:
    """Fit the detected face and estimated eye line to one shared portrait geometry."""
    source = ImageOps.fit(
        Image.open(image_path).convert("RGB"), (WIDTH, HEIGHT), Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    target_face_h = float(layout["face_height_ratio"])
    scale = max(target_face_h / float(face["height"]), 1.0)
    scaled_w, scaled_h = round(WIDTH * scale), round(HEIGHT * scale)
    scaled = source.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)

    eye_source_y = float(face["eye_y"]) * HEIGHT
    target_x = float(layout["face_center_x_ratio"]) * WIDTH
    target_y = float(layout["eye_y_ratio"]) * HEIGHT
    dx = round(target_x - float(face["center_x"]) * WIDTH * scale)
    dy = round(target_y - eye_source_y * scale)

    pixels = np.asarray(scaled)
    left = max(dx, 0)
    top = max(dy, 0)
    right = max(WIDTH - (dx + scaled_w), 0)
    bottom = max(HEIGHT - (dy + scaled_h), 0)
    if left or top or right or bottom:
        pixels = np.pad(pixels, ((top, bottom), (left, right), (0, 0)), mode="edge")
    crop_x = left - dx
    crop_y = top - dy
    crop = pixels[crop_y:crop_y + HEIGHT, crop_x:crop_x + WIDTH]
    return Image.fromarray(np.ascontiguousarray(crop))


def paper_wall_texture(reference_path: Path) -> Image.Image:
    """Reuse the clean indigo handmade-paper wall from the accepted Paper 004 frame."""
    reference = Image.open(reference_path).convert("RGB")
    # This region is the unoccupied indigo wall above the set dressing in the reference.
    patch = reference.crop((80, 0, min(440, reference.width), min(280, reference.height)))
    return ImageOps.fit(patch, (WIDTH, HEIGHT - 1080), Image.Resampling.LANCZOS)


def apply_shared_lower_field(image: Image.Image, wall: Image.Image, layout: dict[str, Any]) -> Image.Image:
    start = int(layout["lower_field_fade_start_y"])
    end = int(layout["lower_field_fade_end_y"])
    base = np.asarray(image).astype(np.float32)
    field = np.asarray(wall).astype(np.float32)
    result = base.copy()
    y = np.arange(start, HEIGHT, dtype=np.float32)
    x = np.clip((y - start) / max(1, end - start), 0.0, 1.0)
    alpha = x * x * (3.0 - 2.0 * x)
    mask = alpha[:, None, None]
    field_start = field[:HEIGHT - start]
    result[start:] = base[start:] * (1.0 - mask) + field_start * mask
    return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))


def tracked_width(text: str, font: ImageFont.FreeTypeFont, tracking: float) -> float:
    visible = [char for char in text]
    return sum(font.getlength(char) for char in visible) + max(0, len(visible) - 1) * tracking


def draw_tracked_line(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    center_x: float,
    center_y: float,
    tracking: float,
    fill: int,
    stroke_width: int = 0,
) -> None:
    text_width = tracked_width(text, font, tracking)
    x = center_x - text_width / 2
    visible_boxes = [font.getbbox(char) for char in text if not char.isspace()]
    top = min(box[1] for box in visible_boxes)
    bottom = max(box[3] for box in visible_boxes)
    y = center_y - (top + bottom) / 2
    for char in text:
        draw.text(
            (round(x), round(y)), char, font=font, fill=fill,
            stroke_width=stroke_width, stroke_fill=fill,
        )
        x += font.getlength(char) + tracking


def draw_text_mask(lines: list[tuple[str, int, int]], font_path: Path, layout: dict[str, Any], stroke_px: int = 0) -> Image.Image:
    canvas = Image.new("L", (WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE), 0)
    draw = ImageDraw.Draw(canvas)
    tracking = float(layout["letter_spacing_px"]) * SUPERSAMPLE
    for text, font_px, cx, cy in lines:
        font = ImageFont.truetype(str(font_path), int(font_px) * SUPERSAMPLE)
        draw_tracked_line(
            draw, text, font, float(cx) * SUPERSAMPLE, float(cy) * SUPERSAMPLE,
            tracking, 255, stroke_width=stroke_px * SUPERSAMPLE,
        )
    width_scale = float(layout.get("text_width_scale", 1.0))
    if not 0.5 <= width_scale <= 1.0:
        fail("text_width_scale must be between 0.5 and 1.0")
    if width_scale != 1.0:
        center = float(layout["title_center_x"]) * SUPERSAMPLE
        canvas = canvas.transform(
            canvas.size, Image.Transform.AFFINE,
            (1.0 / width_scale, 0.0, center * (1.0 - 1.0 / width_scale), 0.0, 1.0, 0.0),
            resample=Image.Resampling.BICUBIC,
        )
    return canvas


def sample_paper_colour(reference_path: Path) -> np.ndarray:
    source = np.asarray(Image.open(reference_path).convert("RGBA"))
    r, g, b, a = [source[:, :, i] for i in range(4)]
    paper = (a > 220) & (r > 210) & (g > 150) & (g < 225) & (b > 110) & (b < 200) & ((r.astype(np.int16) - g.astype(np.int16)) < 90)
    if not np.any(paper):
        fail("could not sample cream paper from approved typography reference")
    return np.median(source[:, :, :3][paper], axis=0).astype(np.float32)


def textured_paper(reference_path: Path) -> Image.Image:
    """Create a restrained, non-repeating paper surface from the approved letter stock colour."""
    rng = np.random.default_rng(2519)
    base = sample_paper_colour(reference_path)
    coarse = rng.normal(0, 1.5, size=(120, 68)).astype(np.float32)
    coarse_img = Image.fromarray(np.uint8(np.clip(128 + coarse * 18, 0, 255)))
    coarse_img = coarse_img.resize((WIDTH * SUPERSAMPLE, HEIGHT * SUPERSAMPLE), Image.Resampling.BICUBIC)
    coarse_arr = (np.asarray(coarse_img).astype(np.float32) - 128.0) / 18.0
    fine = rng.normal(0, 2.2, size=(HEIGHT * SUPERSAMPLE, WIDTH * SUPERSAMPLE)).astype(np.float32)
    texture = np.empty((HEIGHT * SUPERSAMPLE, WIDTH * SUPERSAMPLE, 3), dtype=np.uint8)
    variance = coarse_arr * 1.8 + fine
    channel_scale = np.array([1.0, 0.9, 0.75], dtype=np.float32)
    for channel in range(3):
        texture[:, :, channel] = np.clip(base[channel] + variance * channel_scale[channel], 0, 255).astype(np.uint8)
    return Image.fromarray(texture)


def build_title(scene: dict[str, Any], layout: dict[str, Any], font_path: Path, paper: Image.Image) -> tuple[Image.Image, tuple[int, int]]:
    center_x = int(layout["title_center_x"])
    name_size = int(layout["name_font_px"])
    iq_size = int(layout["iq_font_px"])
    name_lines = list(scene["lines"])
    if len(name_lines) == 1:
        line_specs = [(name_lines[0], name_size, center_x, int(layout["single_name_center_y"]))]
    elif len(name_lines) == 2:
        line_specs = [
            (name_lines[0], name_size, center_x, int(layout["name_line_centers_y"][0])),
            (name_lines[1], name_size, center_x, int(layout["name_line_centers_y"][1])),
        ]
    else:
        fail(f"{scene['id']}: names must use one or two fixed rows")
    line_specs.append((f"IQ {scene['iq']}", iq_size, center_x, int(layout["iq_center_y"])))
    width_scale = float(layout.get("text_width_scale", 1.0))
    for text, font_px, _, _ in line_specs:
        font = ImageFont.truetype(str(font_path), font_px)
        line_width = tracked_width(text, font, float(layout["letter_spacing_px"])) * width_scale
        if line_width > 820:
            fail(f"{scene['id']}: {text!r} exceeds the shared 820 px title width")
    fill_mask = draw_text_mask(line_specs, font_path, layout)
    outline_mask = draw_text_mask(line_specs, font_path, layout, int(layout["title_stroke_px"]))

    # The cast-shadow silhouette and short warm extrusion give the same cut-paper depth on every card.
    shadow = Image.new("L", outline_mask.size, 0)
    shadow.paste(outline_mask, (0, int(layout["title_shadow_y_px"]) * SUPERSAMPLE))
    shadow = shadow.filter(ImageFilter.GaussianBlur(int(layout["title_shadow_blur_px"]) * SUPERSAMPLE))
    shadow = shadow.point(lambda value: round(value * 0.68))
    shadow_layer = Image.new("RGBA", outline_mask.size, (6, 13, 25, 170))
    shadow_layer.putalpha(shadow)

    extrusion = Image.new("L", outline_mask.size, 0)
    extrusion.paste(outline_mask, (0, int(layout["title_extrusion_y_px"]) * SUPERSAMPLE))
    extrusion_layer = Image.new("RGBA", outline_mask.size, (140, 55, 24, 255))
    extrusion_layer.putalpha(extrusion)
    edge_layer = Image.new("RGBA", outline_mask.size, (218, 91, 35, 255))
    edge_layer.putalpha(outline_mask)
    paper_layer = paper.convert("RGBA")
    paper_layer.putalpha(fill_mask)

    title = Image.new("RGBA", outline_mask.size, (0, 0, 0, 0))
    title.alpha_composite(shadow_layer)
    title.alpha_composite(extrusion_layer)
    title.alpha_composite(edge_layer)
    title.alpha_composite(paper_layer)
    title = title.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    bbox = title.getchannel("A").getbbox()
    if not bbox:
        fail(f"{scene['id']}: rendered title is empty")
    left, top, right, bottom = bbox
    pad = 3
    bounds = (max(0, left - pad), max(0, top - pad), min(WIDTH, right + pad), min(HEIGHT, bottom + pad))
    return title.crop(bounds), (bounds[0], bounds[1])


def alpha_overlays_and_cards(
    manifest: dict[str, Any], temp: Path, prepare_sequences: bool = True
) -> tuple[list[Path], list[tuple[Path, int, int]], list[dict[str, Any]]]:
    sequence_root = temp / "title_sequences"
    sequence_root.mkdir()
    normalized_dir = resolve(manifest["normalized_dir"])
    title_dir = resolve(manifest["title_dir"])
    card_dir = resolve(manifest["card_dir"])
    for directory in (normalized_dir, title_dir, card_dir):
        directory.mkdir(parents=True, exist_ok=True)

    layout = manifest["layout"]
    font_path = resolve(manifest["font"])
    wall = paper_wall_texture(resolve(manifest["style_reference"]))
    paper = textured_paper(resolve(manifest["title_texture_reference"]))
    fade_in = int(layout["title_fade_in_frames"])
    fade_out = int(layout["title_fade_out_frames"])
    backgrounds: list[Path] = []
    title_sequences: list[tuple[Path, int, int]] = []
    records: list[dict[str, Any]] = []

    for index, scene in enumerate(manifest["scenes"], 1):
        image_path = resolve(scene["image"])
        if not image_path.is_file():
            fail(f"{scene['id']}: missing source scene {image_path}")
        background = normalize_scene(image_path, scene["face"], layout)
        background = apply_shared_lower_field(background, wall, layout)
        bg_path = normalized_dir / f"s{index:02d}_{scene['id'].lower()}_background.png"
        background.save(bg_path, format="PNG", optimize=True)

        title, title_position = build_title(scene, layout, font_path, paper)
        title_path = title_dir / f"s{index:02d}_{scene['id'].lower()}_title.png"
        title.save(title_path, format="PNG", optimize=True)

        card = background.convert("RGBA")
        card.alpha_composite(title, title_position)
        card_path = card_dir / f"s{index:02d}_{scene['id'].lower()}_card.png"
        card.convert("RGB").save(card_path, format="PNG", optimize=True)

        frames = int(scene["frames"])
        sequence = None
        if prepare_sequences:
            sequence_dir = sequence_root / f"s{index:02d}"
            sequence_dir.mkdir()
            title_alpha = title.getchannel("A")
            fade_out_start = frames - fade_out
            for frame_no in range(frames):
                if frame_no < fade_in:
                    x = frame_no / max(1, fade_in - 1)
                    opacity = x * x * (3 - 2 * x)
                elif frame_no >= fade_out_start:
                    x = (frame_no - fade_out_start) / max(1, fade_out - 1)
                    opacity = 1.0 - x * x * (3 - 2 * x)
                else:
                    opacity = 1.0
                title_frame = title.copy()
                title_frame.putalpha(title_alpha.point(lambda value, o=opacity: round(value * o)))
                title_frame.save(sequence_dir / f"frame_{frame_no:03d}.png", format="PNG")
            sequence = (sequence_dir / "frame_%03d.png", 0, 0)
        backgrounds.append(bg_path)
        if sequence is not None:
            title_sequences.append((sequence[0], title_position[0], title_position[1]))
        records.append({
            "id": scene["id"], "name": scene["name"], "iq": scene["iq"], "lines": scene["lines"],
            "frames": frames, "source_image": str(image_path), "normalized_background": str(bg_path),
            "title_png": str(title_path), "complete_card": str(card_path),
            "title_box": [title_position[0], title_position[1], title.width, title.height],
            "face_anchor": scene["face"], "normalized_face_height_ratio": layout["face_height_ratio"],
            "normalized_eye_y_ratio": layout["eye_y_ratio"], "normalized_face_center_x_ratio": layout["face_center_x_ratio"],
            "image_sha256": sha256(image_path), "card_sha256": sha256(card_path),
        })
    return backgrounds, title_sequences, records


def make_contact_sheet(manifest: dict[str, Any]) -> None:
    card_dir = resolve(manifest["card_dir"])
    output = resolve(manifest["contact_sheet"])
    tile_w, tile_h = 270, 480
    label_h = 28
    cols = 3
    rows = math.ceil(len(manifest["scenes"]) / cols)
    sheet = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), (14, 19, 30))
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
    for i, scene in enumerate(manifest["scenes"]):
        card_path = card_dir / f"s{i+1:02d}_{scene['id'].lower()}_card.png"
        im = Image.open(card_path).convert("RGB")
        im = ImageOps.fit(im, (tile_w, tile_h), Image.Resampling.LANCZOS)
        x = (i % cols) * tile_w
        y = (i // cols) * (tile_h + label_h)
        sheet.paste(im, (x, y))
        draw.rectangle((x, y + tile_h, x + tile_w, y + tile_h + label_h), fill=(14, 19, 30))
        draw.text((x + 7, y + tile_h + 6), f"{i+1:02d}  {scene['name']}  |  IQ {scene['iq']}", fill=(245, 234, 211), font=label_font)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="JPEG", quality=93, optimize=True)


def make_filter(manifest: dict[str, Any], grain_repeats: int, title_boxes: list[tuple[int, int]]) -> tuple[str, int]:
    filters: list[str] = []
    scene_labels: list[str] = []
    scene_count = len(manifest["scenes"])
    for i, scene in enumerate(manifest["scenes"]):
        frames = int(scene["frames"])
        bg_index, title_index = i, scene_count + i
        left, top = title_boxes[i]
        filters.append(
            f"[{bg_index}:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase:flags=lanczos,"
            f"crop={WIDTH}:{HEIGHT},setsar=1,format=rgba,trim=end_frame={frames},"
            f"settb=AVTB,setpts=PTS-STARTPTS[bg{i}]"
        )
        filters.append(
            f"[{title_index}:v]format=rgba,trim=end_frame={frames},settb=AVTB,setpts=PTS-STARTPTS[title{i}]"
        )
        label = f"[scene{i}]"
        filters.append(
            f"[bg{i}][title{i}]overlay=x={left}:y={top}:format=auto:shortest=1,format=rgba,"
            f"settb=AVTB,setpts=PTS-STARTPTS{label}"
        )
        scene_labels.append(label)
    filters.append("".join(scene_labels) + f"concat=n={len(scene_labels)}:v=1:a=0[base]")

    grain_start = scene_count * 2
    for i in range(grain_repeats):
        filters.append(
            f"[{grain_start+i}:v]fps={FPS},scale={WIDTH}:{HEIGHT},format=rgba,"
            f"settb=AVTB,setpts=PTS-STARTPTS[g{i}]"
        )
    period = 7.8
    label = "[g0]"
    for i in range(1, grain_repeats):
        next_label = f"[gx{i}]"
        filters.append(
            f"{label}[g{i}]xfade=transition=fade:duration=0.200000:offset={i*period:.6f}{next_label}"
        )
        label = next_label
    filters.append(
        f"{label}trim=start=0:duration={manifest['duration_frames']/FPS:.6f},"
        "setpts=PTS-STARTPTS,colorchannelmixer=aa=0.24[grain]"
    )
    filters.append(
        "[base][grain]overlay=0:0:format=auto:eof_action=pass,format=yuv420p,setsar=1,"
        f"fps={FPS},trim=end_frame={manifest['duration_frames']},settb=AVTB,setpts=PTS-STARTPTS[v]"
    )
    return ";".join(filters), grain_start + grain_repeats


def render(manifest: dict[str, Any], backgrounds: list[Path], title_sequences: list[tuple[Path, int, int]]) -> dict[str, Any]:
    audio = resolve(manifest["audio"])
    grain = resolve(manifest["grain"])
    output = resolve(manifest["output"])
    report_path = Path(str(output) + ".report.json")
    if not audio.is_file() or not grain.is_file():
        fail("required existing music or grain source is missing")
    if output.exists() or report_path.exists():
        fail(f"refusing to overwrite {output} or its report")
    output.parent.mkdir(parents=True, exist_ok=True)

    audio_info = probe(audio)
    audio_stream = next((s for s in audio_info["streams"] if s.get("codec_type") == "audio"), None)
    if not audio_stream or audio_stream.get("codec_name") != "aac":
        fail("music source must contain AAC for stream-copy")
    grain_info = probe(grain)
    grain_stream = next((s for s in grain_info["streams"] if s.get("codec_type") == "video"), None)
    if not grain_stream or int(grain_stream.get("nb_frames", 0)) != 240 or grain_stream.get("avg_frame_rate") != "30/1":
        fail("grain source must match the accepted 240-frame, 30 fps loop")
    duration = int(manifest["duration_frames"]) / FPS
    grain_repeats = math.ceil((duration - 8.0) / 7.8) + 1
    title_boxes = [(left, top) for _, left, top in title_sequences]
    filter_graph, audio_index = make_filter(manifest, grain_repeats, title_boxes)

    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-filter_complex_threads", "1"]
    for background in backgrounds:
        command.extend(["-loop", "1", "-framerate", str(FPS), "-i", str(background)])
    for sequence, _, _ in title_sequences:
        command.extend(["-framerate", str(FPS), "-start_number", "0", "-i", str(sequence)])
    for _ in range(grain_repeats):
        command.extend(["-i", str(grain)])
    command.extend(["-i", str(audio), "-filter_complex", filter_graph, "-map", "[v]", "-map", f"{audio_index}:a:0"])
    command.extend([
        "-frames:v", str(manifest["duration_frames"]), "-t", f"{duration:.6f}", "-fps_mode", "cfr",
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-g", "30", "-keyint_min", "30", "-sc_threshold", "0", "-c:a", "copy",
        "-movflags", "+faststart", "-video_track_timescale", "90000", str(output),
    ])
    run(command)

    result = probe(output)
    video = next((s for s in result["streams"] if s.get("codec_type") == "video"), None)
    out_audio = next((s for s in result["streams"] if s.get("codec_type") == "audio"), None)
    if not video or video.get("codec_name") != "h264" or (video.get("width"), video.get("height")) != (WIDTH, HEIGHT):
        fail("rendered video does not match 1080x1920 H.264")
    if video.get("avg_frame_rate") != "30/1" or int(video.get("nb_frames", 0)) != manifest["duration_frames"]:
        fail("rendered video does not contain exactly 1800 frames at 30 fps")
    if not out_audio or out_audio.get("codec_name") != "aac":
        fail("rendered file is missing the existing AAC music stream")
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-xerror", "-i", str(output), "-f", "null", "-"], check=True)

    report = {
        "output": str(output), "sha256": sha256(output), "probe": result,
        "audio_source": str(audio), "audio_source_sha256": sha256(audio),
        "audio_codec_copied": out_audio.get("codec_name"), "grain_source": str(grain),
        "grain_repeat_count": grain_repeats, "grain_period_frames": 234, "grain_alpha": 0.24,
        "face_geometry": {k: manifest["layout"][k] for k in ("face_height_ratio", "eye_y_ratio", "face_center_x_ratio")},
        "title_geometry": {k: manifest["layout"][k] for k in ("name_font_px", "iq_font_px", "name_line_centers_y", "single_name_center_y", "iq_center_y")},
        "frame_decode": "full decode via ffmpeg -xerror succeeded",
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--probe", action="store_true", help="validate and print the render plan")
    parser.add_argument("--assets-only", action="store_true", help="prepare normalized scenes and cards without rendering MP4")
    args = parser.parse_args()
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            fail(f"missing required tool: {binary}")
    manifest_path = args.manifest.expanduser().resolve()
    manifest = json.loads(manifest_path.read_text())
    scenes = manifest.get("scenes")
    if not isinstance(scenes, list) or len(scenes) != 13:
        fail("v19 requires exactly 13 complete scenes")
    if manifest.get("fps") != FPS or manifest.get("width") != WIDTH or manifest.get("height") != HEIGHT:
        fail("v19 must be 1080x1920 at 30 fps")
    if sum(int(scene["frames"]) for scene in scenes) != manifest.get("duration_frames"):
        fail("scene durations do not sum to the declared frame count")
    if manifest["duration_frames"] != 1800:
        fail("v19 duration must be exactly 1800 frames / 60 seconds")
    if len({scene["name"] for scene in scenes}) != 13:
        fail("scene names must be unique")
    for scene in scenes:
        if scene["iq"] <= 0 or scene["frames"] not in (120, 150, 180):
            fail(f"invalid IQ or duration in {scene['id']}")
        if not 0.08 <= scene["face"]["height"] <= 0.20 or not 0.10 <= scene["face"]["eye_y"] <= 0.30:
            fail(f"face geometry out of expected range in {scene['id']}")
    paths = [resolve(manifest[k]) for k in ("font", "audio", "grain", "style_reference", "title_texture_reference")]
    paths += [resolve(s["image"]) for s in scenes]
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        fail("missing required source(s):\n" + "\n".join(missing))
    if args.probe:
        print(json.dumps({
            "scenes": [{k: s[k] for k in ("id", "name", "iq", "lines", "frames", "image", "face")} for s in scenes],
            "duration_frames": manifest["duration_frames"], "fps": FPS,
            "duration_seconds": manifest["duration_frames"] / FPS,
            "output": str(resolve(manifest["output"])), "audio": str(resolve(manifest["audio"])),
            "grain": str(resolve(manifest["grain"])), "font": str(resolve(manifest["font"])),
        }, indent=2, ensure_ascii=False))
        return

    with tempfile.TemporaryDirectory(prefix="iq_gallery_v19_") as temp_name:
        backgrounds, title_sequences, card_records = alpha_overlays_and_cards(
            manifest, Path(temp_name), prepare_sequences=not args.assets_only
        )
        make_contact_sheet(manifest)
        if args.assets_only:
            print(json.dumps({"prepared_scenes": len(card_records), "contact_sheet": str(resolve(manifest["contact_sheet"]))}, indent=2))
            return
        report = render(manifest, backgrounds, title_sequences)
    report["scenes"] = card_records
    Path(str(resolve(manifest["output"])) + ".report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps({"output": report["output"], "sha256": report["sha256"], "frames": manifest["duration_frames"]}, indent=2))


if __name__ == "__main__":
    main()
