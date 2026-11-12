#!/usr/bin/env python3
"""Render a Paper Detour gallery from complete still scenes, shared moving titles and existing audio."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

from PIL import Image


ROOT = pathlib.Path(__file__).resolve().parents[5]
WIDTH = 1080
HEIGHT = 1920
FPS = 30


def fail(message: str) -> None:
    raise SystemExit(f"error: {message}")


def resolve_path(value: str, base: pathlib.Path = ROOT) -> pathlib.Path:
    path = pathlib.Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def run(args: list[str]) -> str:
    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        if exc.stderr:
            sys.stderr.write(exc.stderr)
        fail(f"command failed ({exc.returncode}): {' '.join(args[:5])} …")
    return result.stdout


def probe(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(
        run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_streams",
                "-show_format",
                "-of",
                "json",
                str(path),
            ]
        )
    )


def name_bands(path: pathlib.Path, name_rows_end_ratio: float) -> list[Image.Image]:
    with Image.open(path) as source:
        source.load()
        image = source.convert("RGBA")
    name_rows_end = round(image.height * name_rows_end_ratio)
    if not 0 < name_rows_end < image.height:
        fail(f"invalid name-row crop for title PNG: {path}")

    # Only scan the name area. Some approved title groups place the surname
    # almost against their baked-in IQ row, so extracting score text from the
    # group can merge two distinct lines and shrink both during layout.
    name_image = image.crop((0, 0, image.width, name_rows_end))
    alpha = name_image.getchannel("A")
    active_rows = [alpha.crop((0, y, image.width, y + 1)).point(lambda value: 255 if value > 8 else 0).getbbox() is not None for y in range(name_image.height)]
    ranges: list[tuple[int, int]] = []
    start: int | None = None
    for y, active in enumerate(active_rows + [False]):
        if active and start is None:
            start = y
        elif not active and start is not None:
            ranges.append((start, y))
            start = None
    merged: list[tuple[int, int]] = []
    for top, bottom in ranges:
        if merged and top - merged[-1][1] <= 6:
            merged[-1] = (merged[-1][0], bottom)
        else:
            merged.append((top, bottom))
    bands: list[Image.Image] = []
    for top, bottom in merged:
        row_crop = name_image.crop((0, top, image.width, bottom))
        bbox = row_crop.getchannel("A").point(lambda x: 255 if x > 8 else 0).getbbox()
        if bbox:
            bands.append(row_crop.crop(bbox))
    if len(bands) < 1 or len(bands) > 2:
        fail(f"expected one or two name rows, found {len(bands)} in {path}")
    return bands


def fit_line(image: Image.Image, target_height: int, max_width: int) -> Image.Image:
    scale = min(target_height / image.height, max_width / image.width)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, Image.Resampling.LANCZOS)


def build_iq_line(
    score: int,
    assets_dir: pathlib.Path,
    target_height: int,
    max_width: int,
    digit_gap: int,
    label_gap: int,
) -> Image.Image:
    names = ["iq.png", *(f"digit_{digit}.png" for digit in str(score))]
    pieces: list[Image.Image] = []
    for name in names:
        source = assets_dir / name
        if not source.is_file():
            fail(f"missing approved IQ paper asset: {source}")
        with Image.open(source) as im:
            im.load()
            part = im.convert("RGBA")
        bbox = part.getchannel("A").point(lambda value: 255 if value > 8 else 0).getbbox()
        if not bbox:
            fail(f"empty approved IQ paper asset: {source}")
        pieces.append(fit_line(part.crop(bbox), target_height, max_width))

    gaps = [label_gap, *([digit_gap] * (len(pieces) - 2))]
    total_width = sum(piece.width for piece in pieces) + sum(gaps)
    if total_width > max_width:
        scale = max_width / total_width
        pieces = [
            piece.resize(
                (max(1, round(piece.width * scale)), max(1, round(piece.height * scale))),
                Image.Resampling.LANCZOS,
            )
            for piece in pieces
        ]
        gaps = [max(1, round(gap * scale)) for gap in gaps]
        total_width = sum(piece.width for piece in pieces) + sum(gaps)

    line_height = max(piece.height for piece in pieces)
    line = Image.new("RGBA", (total_width, line_height), (0, 0, 0, 0))
    x = 0
    for index, piece in enumerate(pieces):
        line.alpha_composite(piece, (x, (line_height - piece.height) // 2))
        x += piece.width
        if index < len(gaps):
            x += gaps[index]
    return line


def prepare_title(
    source: pathlib.Path,
    destination: pathlib.Path,
    name_center_y: float,
    iq_center_y: float,
    center_x: float,
    score: int,
    iq_assets_dir: pathlib.Path,
    name_rows_end_ratio: float,
    name_line_height: int,
    iq_line_height: int,
    max_line_width: int,
    digit_gap: int,
    label_gap: int,
) -> dict[str, Any]:
    name_lines = [fit_line(line, name_line_height, max_line_width) for line in name_bands(source, name_rows_end_ratio)]
    iq_line = build_iq_line(score, iq_assets_dir, iq_line_height, max_line_width, digit_gap, label_gap)
    line_gap = 8
    name_height = sum(line.height for line in name_lines) + line_gap * (len(name_lines) - 1)
    name_top = round(name_center_y * HEIGHT - name_height / 2)
    iq_top = round(iq_center_y * HEIGHT - iq_line.height / 2)
    min_y = min(name_top, iq_top)
    max_y = max(name_top + name_height, iq_top + iq_line.height)
    canvas_width = max(line.width for line in name_lines + [iq_line])
    canvas = Image.new("RGBA", (canvas_width, max_y - min_y), (0, 0, 0, 0))
    y = name_top - min_y
    for line in name_lines:
        canvas.alpha_composite(line, ((canvas_width - line.width) // 2, y))
        y += line.height + line_gap
    canvas.alpha_composite(iq_line, ((canvas_width - iq_line.width) // 2, iq_top - min_y))
    bbox = canvas.getchannel("A").point(lambda x: 255 if x > 8 else 0).getbbox()
    if not bbox:
        fail(f"empty prepared title: {source}")
    canvas = canvas.crop(bbox)
    destination.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(destination, format="PNG", optimize=True)
    return {
        "file": str(destination),
        "size": list(canvas.size),
        "center_x": center_x,
        "name_center_y": name_center_y,
        "iq_center_y": iq_center_y,
        "iq_row_center_in_group_px": round(iq_top - min_y + iq_line.height / 2 - bbox[1], 2),
    }


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def camera_progress_expression(move_duration: float, ease_duration: float) -> str:
    if move_duration <= 2 * ease_duration:
        fail("camera move must be longer than its two easing ramps")
    r = f"{ease_duration:.6f}"
    d = f"{move_duration:.6f}"
    middle = f"(t-0.5*{r})/({d}-{r})"
    ramp_in = f"t*t/(2*{r}*({d}-{r}))"
    ramp_out = f"(1-({d}-t)*({d}-t)/(2*{r}*({d}-{r})))"
    moving = f"if(lt(t,{r}),{ramp_in},if(lt(t,{d}-{r}),{middle},{ramp_out}))"
    return f"if(lt(t,{d}),{moving},1)"


def validate_camera(scene: dict[str, Any], image: pathlib.Path, scene_index: int) -> dict[str, Any]:
    camera = scene.get("camera")
    required = (
        "x_start_px",
        "x_end_px",
        "y_start_px",
        "y_end_px",
        "scale_start_percent",
        "scale_end_percent",
        "ease_frames",
    )
    if not isinstance(camera, dict) or any(key not in camera for key in required):
        fail(f"scene {scene_index + 1}: camera motion fields are required")
    values = {key: float(camera[key]) for key in required}
    frames = int(scene["frames"])
    move_frames = int(camera.get("move_frames", frames))
    if move_frames > frames or move_frames <= 0:
        fail(f"scene {scene_index + 1}: camera move_frames must be within the scene")
    if values["scale_start_percent"] < 100 or values["scale_end_percent"] < 100:
        fail(f"scene {scene_index + 1}: camera scale must keep full-frame coverage")
    if values["scale_start_percent"] > 112 or values["scale_end_percent"] > 112:
        fail(f"scene {scene_index + 1}: camera scale exceeds this profile's 112% safety cap")
    if values["ease_frames"] <= 0:
        fail(f"scene {scene_index + 1}: ease_frames must be positive")
    with Image.open(image) as im:
        source_width, source_height = im.size
    minimum_scale = min(values["scale_start_percent"], values["scale_end_percent"]) / 100
    scaled_width = HEIGHT * minimum_scale * source_width / source_height
    scaled_height = HEIGHT * minimum_scale
    margin_x = (scaled_width - WIDTH) / 2
    margin_y = (scaled_height - HEIGHT) / 2
    max_x = max(abs(values["x_start_px"]), abs(values["x_end_px"]))
    max_y = max(abs(values["y_start_px"]), abs(values["y_end_px"]))
    if margin_x + 1 < max_x or margin_y + 1 < max_y:
        fail(
            f"scene {scene_index + 1}: requested pan exceeds overscan at minimum scale "
            f"({margin_x:.1f}px x / {margin_y:.1f}px y available)"
        )
    return {
        **camera,
        "move_frames": move_frames,
        "move_duration_seconds": move_frames / FPS,
        "source_dimensions": [source_width, source_height],
        "minimum_overscan_px": [round(margin_x, 2), round(margin_y, 2)],
    }


def audio_packet_hashes(path: pathlib.Path) -> list[str]:
    raw = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_packets",
            "-show_data_hash",
            "sha256",
            "-of",
            "json",
            str(path),
        ]
    )
    return [packet["data_hash"] for packet in json.loads(raw).get("packets", [])]


def encode_scene(
    image: pathlib.Path,
    title: pathlib.Path,
    output: pathlib.Path,
    frames: int,
    title_meta: dict[str, Any],
    scene_index: int,
    camera: dict[str, Any],
) -> None:
    title_w, title_h = title_meta["size"]
    max_w = math.ceil((title_w * 1.055 + 12) / 2) * 2
    max_h = math.ceil((title_h * 1.055 + 12) / 2) * 2
    rotated = int(math.ceil(math.sqrt(max_w * max_w + max_h * max_h) + 8))
    rotated += rotated % 2
    duration = frames / FPS
    move_duration = int(camera["move_frames"]) / FPS
    ease_duration = int(camera["ease_frames"]) / FPS
    progress = camera_progress_expression(move_duration, ease_duration)
    x_start = float(camera["x_start_px"])
    x_delta = float(camera["x_end_px"]) - x_start
    y_start = float(camera["y_start_px"])
    y_delta = float(camera["y_end_px"]) - y_start
    scale_start = float(camera["scale_start_percent"])
    scale_delta = float(camera["scale_end_percent"]) - scale_start
    scale_expr = f"({scale_start:.6f}+({scale_delta:.6f})*{progress})"
    x_expr = f"({x_start:.6f}+({x_delta:.6f})*{progress})"
    y_expr = f"({y_start:.6f}+({y_delta:.6f})*{progress})"
    scaled_width = f"trunc({HEIGHT}*({scale_expr})/100*iw/ih/2)*2"
    scaled_height = f"trunc({HEIGHT}*({scale_expr})/100/2)*2"
    crop_x = f"((iw-{WIDTH})/2-({x_expr}))"
    crop_y = f"((ih-{HEIGHT})/2-({y_expr}))"
    center_x = round(title_meta["center_x"] * WIDTH)
    title_center_y = round((title_meta["name_center_y"] + title_meta["iq_center_y"]) * HEIGHT / 2)
    angle = math.radians(1.2)
    cycle = 3.6
    entry_duration = 0.5
    u = f"clip(t/{entry_duration:.6f},0,1)"
    smooth = f"({u}*{u}*{u}*({u}*({u}*6-15)+10))"
    envelope = f"clip((t-{entry_duration:.3f})/0.30,0,1)*clip(({duration:.6f}-t)/0.30,0,1)"
    pulse = f"sin(2*PI*t/{cycle:.3f})*({envelope})"
    scale_expr = f"(0.94+0.06*{smooth}+0.04*{pulse})"
    rotation_expr = f"({angle:.10f}*sin(2*PI*t/{cycle:.3f}+0.72)*({envelope}))"
    title_x = center_x - rotated / 2
    title_y = title_center_y - rotated / 2
    filters = (
        f"[0:v]scale=w='{scaled_width}':h='{scaled_height}':eval=frame,setsar=1,"
        f"crop={WIDTH}:{HEIGHT}:x='{crop_x}':y='{crop_y}',setsar=1[base];"
        f"[1:v]scale=w='trunc(iw*{scale_expr}/2)*2':h='trunc(ih*{scale_expr}/2)*2':eval=frame,"
        f"format=rgba,pad={max_w}:{max_h}:(ow-iw)/2:(oh-ih)/2:color=0x00000000:eval=frame,"
        f"rotate=a='{rotation_expr}':ow={rotated}:oh={rotated}:c=none,"
        f"fade=t=in:st=0:d={entry_duration:.6f}:alpha=1[title];"
        f"[base][title]overlay=x={title_x}:y={title_y}:format=auto,format=yuv420p,setsar=1[v]"
    )
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-filter_complex_threads",
            "1",
            "-loop",
            "1",
            "-framerate",
            str(FPS),
            "-i",
            str(image),
            "-loop",
            "1",
            "-framerate",
            str(FPS),
            "-i",
            str(title),
            "-filter_complex",
            filters,
            "-map",
            "[v]",
            "-an",
            "-frames:v",
            str(frames),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "15",
            "-pix_fmt",
            "yuv420p",
            "-n",
            str(output),
        ]
    )
    print(
        f"Rendered scene {scene_index + 1}: {frames / FPS:.2f}s; "
        f"camera X {x_start:g}→{x_start + x_delta:g}px, "
        f"scale {scale_start:g}→{scale_start + scale_delta:g}%",
        file=sys.stderr,
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="JSON manifest path; relative paths resolve from the repository root")
    parser.add_argument("--probe", action="store_true", help="validate inputs and prepare title overlays without rendering")
    parser.add_argument("--force-titles", action="store_true", help="replace only generated prepared-title PNGs")
    args = parser.parse_args()
    manifest_path = resolve_path(args.manifest)
    if not manifest_path.is_file():
        fail(f"manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("schema_version") != 1:
        fail("schema_version must be 1")
    width = int(manifest.get("width", WIDTH))
    height = int(manifest.get("height", HEIGHT))
    fps = int(manifest.get("fps", FPS))
    if (width, height, fps) != (WIDTH, HEIGHT, FPS):
        fail(f"this profile requires {WIDTH}x{HEIGHT} at {FPS} fps")
    scenes = manifest.get("scenes")
    if not isinstance(scenes, list) or len(scenes) != 13:
        fail("exactly 13 complete-scene records are required")
    total_frames = sum(int(scene["frames"]) for scene in scenes)
    expected_frames = int(manifest.get("duration_frames", -1))
    if total_frames != expected_frames or total_frames != 60 * FPS:
        fail(f"scene frames total {total_frames}; expected exactly {60 * FPS}")
    title_layout = manifest.get("title_layout", {})
    name_rows_end_ratio = float(title_layout.get("name_rows_end_ratio", 347 / 474))
    name_line_height = int(title_layout.get("name_line_height_px", 76))
    iq_line_height = int(title_layout.get("iq_line_height_px", 72))
    max_line_width = int(title_layout.get("max_line_width_px", 500))
    digit_gap = int(title_layout.get("digit_gap_px", 10))
    label_gap = int(title_layout.get("label_gap_px", 18))
    if not 0.65 < name_rows_end_ratio < 0.85 or min(name_line_height, iq_line_height, max_line_width) <= 0 or min(digit_gap, label_gap) < 0:
        fail("title_layout values are outside the supported range")
    iq_assets_dir = resolve_path(manifest["iq_assets_dir"])
    previous_direction = 0
    for index, scene in enumerate(scenes):
        camera = scene.get("camera", {})
        delta_x = float(camera.get("x_end_px", 0)) - float(camera.get("x_start_px", 0))
        direction = 1 if delta_x > 0 else -1 if delta_x < 0 else 0
        if direction and previous_direction and direction == previous_direction:
            fail(f"scene {index + 1}: horizontal camera direction repeats the previous scene")
        if direction:
            previous_direction = direction
    audio = resolve_path(manifest["audio"])
    grain = resolve_path(manifest["grain"])
    output = resolve_path(manifest["output"])
    report = resolve_path(manifest.get("report", str(output) + ".report.json"))
    title_dir = resolve_path(manifest["prepared_titles_dir"])
    if not audio.is_file() or not grain.is_file():
        fail(f"missing existing music or grain source: {audio if not audio.is_file() else grain}")
    if output.exists() or report.exists():
        fail("output or report already exists; choose a new versioned path")
    if title_dir.exists() and any(title_dir.iterdir()) and not args.force_titles:
        fail(f"prepared title directory is nonempty; pass --force-titles only to rebuild these derived PNGs: {title_dir}")
    audio_probe = probe(audio)
    audio_streams = [stream for stream in audio_probe.get("streams", []) if stream.get("codec_type") == "audio"]
    if not audio_streams:
        fail(f"no audio stream found: {audio}")
    audio_stream = audio_streams[0]
    if audio_stream.get("codec_name") != "aac":
        fail("existing music must already be AAC so it can be stream-copied")
    if float(audio_stream.get("duration", audio_probe.get("format", {}).get("duration", 0))) < total_frames / FPS - 0.05:
        fail("existing music is shorter than the 60-second sequence")

    prepared_scenes: list[dict[str, Any]] = []
    for index, scene in enumerate(scenes):
        image = resolve_path(scene["image"])
        source_title = resolve_path(scene["title_source"])
        if not image.is_file() or not source_title.is_file():
            fail(f"scene {index + 1}: missing complete-scene image or approved title source")
        with Image.open(image) as im:
            im.load()
            if im.width < 900 or im.height < 1600 or im.width / im.height < 0.55 or im.width / im.height > 0.575:
                fail(f"scene {index + 1}: expected a high-resolution vertical 9:16 image, found {im.size}")
        camera = validate_camera(scene, image, index)
        dest = title_dir / f"s{index + 1:02d}_title.png"
        title_meta = prepare_title(
            source_title,
            dest,
            float(scene["name_center_y"]),
            float(scene["iq_center_y"]),
            float(scene["center_x"]),
            int(scene["iq"]),
            iq_assets_dir,
            name_rows_end_ratio,
            name_line_height,
            iq_line_height,
            max_line_width,
            digit_gap,
            label_gap,
        )
        prepared_scenes.append(
            {
                **scene,
                "image_path": str(image),
                "source_title_path": str(source_title),
                "camera": camera,
                "prepared_title": title_meta,
            }
        )
    if args.probe:
        print(
            json.dumps(
                {
                    "manifest": str(manifest_path),
                    "canvas": f"{WIDTH}x{HEIGHT} {FPS} fps",
                    "frames": total_frames,
                    "audio": str(audio),
                    "audio_codec": audio_stream.get("codec_name"),
                    "grain": str(grain),
                    "output": str(output),
                    "scenes": prepared_scenes,
                    "title_motion": {
                        "common_group": True,
                        "entry_scale": "0.94 to 1.00 over 0.5 seconds, eased",
                        "breathing_scale": "4% sinusoidal amplitude",
                        "rotation": "1.2 degrees sinusoidal amplitude",
                        "scene_transition": "direct cut",
                    },
                    "camera_motion": {
                        "source": "Transform of each complete still only",
                        "interpolation": "12-frame ease-in and ease-out with continuous middle travel; no bounce or overshoot",
                        "title_group": "screen-space; independent of background camera",
                        "scene_movements": [
                            {
                                "id": scene["id"],
                                "x_start_px": scene["camera"]["x_start_px"],
                                "x_end_px": scene["camera"]["x_end_px"],
                                "y_start_px": scene["camera"]["y_start_px"],
                                "y_end_px": scene["camera"]["y_end_px"],
                                "scale_start_percent": scene["camera"]["scale_start_percent"],
                                "scale_end_percent": scene["camera"]["scale_end_percent"],
                                "move_frames": scene["camera"]["move_frames"],
                                "minimum_overscan_px": scene["camera"]["minimum_overscan_px"],
                            }
                            for scene in prepared_scenes
                        ],
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".full_scene_iq_", dir=output.parent) as temp_name:
        temp = pathlib.Path(temp_name)
        clips: list[pathlib.Path] = []
        for index, scene in enumerate(prepared_scenes):
            clip = temp / f"scene_{index + 1:02d}.mp4"
            encode_scene(
                pathlib.Path(scene["image_path"]),
                pathlib.Path(scene["prepared_title"]["file"]),
                clip,
                int(scene["frames"]),
                scene["prepared_title"],
                index,
                scene["camera"],
            )
            clips.append(clip)
        concat_list = temp / "concat.txt"
        concat_list.write_text("".join(f"file '{clip.as_posix()}'\n" for clip in clips))
        silent = temp / "silent_concat.mp4"
        run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_list),
                "-c",
                "copy",
                "-an",
                "-n",
                str(silent),
            ]
        )
        temporary_output = temp / "verified.mp4"
        grain_streams = [stream for stream in probe(grain).get("streams", []) if stream.get("codec_type") == "video"]
        if not grain_streams:
            fail(f"grain source has no video stream: {grain}")
        grain_stream = grain_streams[0]
        grain_duration = float(grain_stream.get("duration", 0))
        grain_frames = int(grain_stream.get("nb_frames", 0))
        grain_fps = grain_stream.get("avg_frame_rate", "0/1")
        if (abs(grain_duration - 8.0) > 0.01 or grain_frames != 240 or grain_fps != "30/1"):
            fail(
                "this loop profile expects the existing 8-second, 240-frame, 30 fps grain source; "
                f"found {grain_duration:g}s / {grain_frames} frames / {grain_fps}"
            )
        grain_overlap = 0.2
        grain_period = grain_duration - grain_overlap
        grain_repeats = math.ceil((total_frames / FPS - grain_duration) / grain_period) + 1
        grain_filters: list[str] = []
        for repeat in range(grain_repeats):
            input_index = repeat + 1
            grain_filters.append(
                f"[{input_index}:v]fps={FPS},scale={WIDTH}:{HEIGHT},format=rgba,"
                f"settb=AVTB,setpts=PTS-STARTPTS[g{repeat}]"
            )
        grain_label = "[g0]"
        for repeat in range(1, grain_repeats):
            next_label = f"[gx{repeat}]"
            offset = repeat * grain_period
            grain_filters.append(
                f"{grain_label}[g{repeat}]xfade=transition=fade:duration={grain_overlap:.6f}:"
                f"offset={offset:.6f}{next_label}"
            )
            grain_label = next_label
        grain_filters.append(
            f"{grain_label}trim=start=0:duration={total_frames / FPS:.6f},"
            f"setpts=PTS-STARTPTS,colorchannelmixer=aa=0.24[g]"
        )
        grain_filters.append("[0:v][g]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v]")
        final_filter = ";".join(grain_filters)
        final_args = [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-filter_complex_threads",
            "1",
            "-i",
            str(silent),
        ]
        for _ in range(grain_repeats):
            final_args.extend(["-i", str(grain)])
        final_args.extend(["-i", str(audio), "-filter_complex", final_filter, "-map", "[v]"])
        audio_input_index = grain_repeats + 1
        final_args.extend(
            [
                "-map",
                f"{audio_input_index}:a:0",
                "-t",
                str(total_frames / FPS),
                "-frames:v",
                str(total_frames),
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "18",
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "copy",
                "-movflags",
                "+faststart",
                "-n",
                str(temporary_output),
            ]
        )
        run(final_args)
        run(["ffmpeg", "-v", "error", "-xerror", "-i", str(temporary_output), "-f", "null", "-"])
        actual = probe(temporary_output)
        video_streams = [stream for stream in actual.get("streams", []) if stream.get("codec_type") == "video"]
        output_audio = [stream for stream in actual.get("streams", []) if stream.get("codec_type") == "audio"]
        if not video_streams or not output_audio:
            fail("rendered file must contain both video and existing music")
        video = video_streams[0]
        actual_frames = int(video.get("nb_frames", 0))
        if (video.get("width"), video.get("height"), actual_frames) != (WIDTH, HEIGHT, total_frames):
            fail(f"unexpected video output: {video.get('width')}x{video.get('height')} / {actual_frames} frames")
        if output_audio[0].get("codec_name") != "aac":
            fail("output music is not AAC")
        source_packets = audio_packet_hashes(audio)
        output_packets = audio_packet_hashes(temporary_output)
        if not source_packets or source_packets[: len(output_packets)] != output_packets:
            fail("output music packets do not match the source prefix")
        os.link(temporary_output, output)
    report_data = {
        "manifest": str(manifest_path),
        "output": str(output),
        "output_sha256": sha256(output),
        "actual": probe(output),
        "validation": {
            "complete_decode": True,
            "frames": total_frames,
            "direct_scene_cuts": True,
            "audio": "existing AAC packet hashes match the output prefix; stream copy; no new audio generated",
            "visual_review": "manual full-length review remains external to renderer",
            "title_animation": "shared compact name + IQ group; 0.94 to 1.00 eased entry, 4% scale breathing, 1.2 degree rotation",
            "camera_motion": "whole-frame X/Scale transform; positions reverse direction at every cut; titles remain screen-space",
            "grain_loop": "existing 8-second source crossfaded over 6 frames every 7.8 seconds; constant 0.24 nominal alpha with no opening or ending fade",
        },
        "scenes": prepared_scenes,
    }
    report.parent.mkdir(parents=True, exist_ok=True)
    try:
        report.write_text(json.dumps(report_data, ensure_ascii=False, indent=2) + "\n")
    except FileExistsError:
        fail(f"video saved but report already exists: {report}")
    print(json.dumps({"output": str(output), "report": str(report), "frames": total_frames}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, FileNotFoundError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        fail(str(exc))
