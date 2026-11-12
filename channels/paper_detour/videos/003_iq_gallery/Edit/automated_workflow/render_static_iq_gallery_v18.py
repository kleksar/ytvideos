#!/usr/bin/env python3
"""Build one-minute Paper Detour IQ Gallery v18 from complete stills."""
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
from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[5]
FPS = 30
WIDTH = 1080
HEIGHT = 1920


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


def title_bands(source: Image.Image) -> list[Image.Image]:
    rgba = source.convert("RGBA")
    alpha = np.asarray(rgba.getchannel("A"))
    active = (alpha > 16).sum(axis=1) > max(1, int(rgba.width * 0.01))
    runs: list[tuple[int, int]] = []
    start: int | None = None
    for y, value in enumerate(active.tolist()):
        if value and start is None:
            start = y
        elif not value and start is not None:
            runs.append((start, y))
            start = None
    if start is not None:
        runs.append((start, len(active)))
    if len(runs) not in (2, 3):
        fail(f"title source has {len(runs)} visible rows, expected name row(s) and IQ row")

    rows: list[Image.Image] = []
    for top, bottom in runs:
        row = rgba.crop((0, top, rgba.width, bottom))
        bbox = row.getchannel("A").getbbox()
        if not bbox:
            fail("empty row in title source")
        rows.append(row.crop(bbox))
    return rows


def build_title(rows: list[Image.Image], scale: float, gap: int) -> Image.Image:
    width = max(row.width for row in rows)
    height = sum(row.height for row in rows) + gap * (len(rows) - 1)
    group = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    y = 0
    for row in rows:
        group.alpha_composite(row, ((width - row.width) // 2, y))
        y += row.height + gap
    if scale != 1:
        group = group.resize(
            (round(group.width * scale), round(group.height * scale)), Image.Resampling.LANCZOS
        )
    return group


def alpha_overlays_and_cards(manifest: dict[str, Any], temp: Path) -> tuple[list[Path], list[tuple[Path, int, int]], list[dict[str, Any]]]:
    sequence_root = temp / "title_sequences"
    background_dir = temp / "normalized_backgrounds"
    sequence_root.mkdir()
    background_dir.mkdir()
    card_dir = resolve("channels/paper_detour/videos/003_iq_gallery/Source/Images/iq_gallery_person_centric_v18_cards")
    card_dir.mkdir(parents=True, exist_ok=True)
    title_layout = manifest["title_layout"]
    scale = float(title_layout["scale"])
    gap = int(title_layout["line_gap_px"])
    bottom = round(float(title_layout["group_bottom_ratio"]) * HEIGHT)
    fade_in_frames = int(manifest["title_motion"]["fade_in_frames"])
    fade_out_frames = int(manifest["title_motion"]["fade_out_frames"])
    backgrounds: list[Path] = []
    title_sequences: list[tuple[Path, int, int]] = []
    records: list[dict[str, Any]] = []

    for index, scene in enumerate(manifest["scenes"], 1):
        image_path = resolve(scene["image"])
        title_path = resolve(scene["title_source"])
        if not image_path.is_file() or not title_path.is_file():
            fail(f"{scene['id']}: missing scene image or approved paper title asset")
        background = Image.open(image_path).convert("RGB")
        background = ImageOps.fit(background, (WIDTH, HEIGHT), Image.Resampling.LANCZOS, centering=(0.5, 0.5))
        bg_path = background_dir / f"s{index:02d}_background.png"
        background.save(bg_path, format="PNG", optimize=True)

        rows = title_bands(Image.open(title_path))
        title = build_title(rows, scale=scale, gap=gap)
        left = (WIDTH - title.width) // 2
        top = bottom - title.height
        if left < 0 or top < HEIGHT * 0.65 or bottom > HEIGHT:
            fail(f"{scene['id']}: title group does not fit in the lower reserved zone")
        card = background.convert("RGBA")
        card.alpha_composite(title, (left, top))
        card_path = card_dir / f"s{index:02d}_{scene['id'].lower()}_card.png"
        card.convert("RGB").save(card_path, format="PNG", optimize=True)

        frames = int(scene["frames"])
        sequence_dir = sequence_root / f"s{index:02d}"
        sequence_dir.mkdir()
        title_alpha = title.getchannel("A")
        fade_out_start = frames - fade_out_frames
        for frame_no in range(frames):
            if frame_no < fade_in_frames:
                x = frame_no / max(1, fade_in_frames - 1)
                opacity = x * x * (3 - 2 * x)
            elif frame_no >= fade_out_start:
                x = (frame_no - fade_out_start) / max(1, fade_out_frames - 1)
                opacity = 1.0 - x * x * (3 - 2 * x)
            else:
                opacity = 1.0
            title_frame = title.copy()
            title_frame.putalpha(title_alpha.point(lambda value, o=opacity: round(value * o)))
            title_frame.save(sequence_dir / f"frame_{frame_no:03d}.png", format="PNG", optimize=True)
        backgrounds.append(bg_path)
        title_sequences.append((sequence_dir / "frame_%03d.png", left, top))
        records.append({
            "id": scene["id"], "name": scene["name"], "iq": scene["iq"],
            "frames": scene["frames"], "image": str(image_path),
            "title_source": str(title_path), "complete_card": str(card_path),
            "normalized_size": [WIDTH, HEIGHT], "title_box": [left, top, title.width, title.height],
            "image_sha256": sha256(image_path), "card_sha256": sha256(card_path),
        })
    return backgrounds, title_sequences, records


def make_contact_sheet(manifest: dict[str, Any]) -> None:
    card_dir = resolve("channels/paper_detour/videos/003_iq_gallery/Source/Images/iq_gallery_person_centric_v18_cards")
    output = resolve(manifest["contact_sheet"])
    tile_w, tile_h = 270, 480
    label_h = 28
    cols = 3
    rows = math.ceil(len(manifest["scenes"]) / cols)
    sheet = Image.new("RGB", (cols * tile_w, rows * (tile_h + label_h)), (14, 19, 30))
    draw = ImageDraw.Draw(sheet)
    for i, scene in enumerate(manifest["scenes"]):
        card = card_dir / f"s{i+1:02d}_{scene['id'].lower()}_card.png"
        im = Image.open(card).convert("RGB")
        im = ImageOps.fit(im, (tile_w, tile_h), Image.Resampling.LANCZOS)
        x = (i % cols) * tile_w
        y = (i // cols) * (tile_h + label_h)
        sheet.paste(im, (x, y))
        draw.rectangle((x, y + tile_h, x + tile_w, y + tile_h + label_h), fill=(14, 19, 30))
        draw.text((x + 8, y + tile_h + 7), f"{i+1:02d}  {scene['name']}  |  IQ {scene['iq']}", fill=(245, 234, 211))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, format="JPEG", quality=92, optimize=True)


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
    grain_seconds = 8.0
    grain_period = grain_seconds - 0.2
    duration = int(manifest["duration_frames"]) / FPS
    grain_repeats = math.ceil((duration - grain_seconds) / grain_period) + 1
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
        "grain_repeat_count": grain_repeats, "grain_period_frames": 234,
        "grain_alpha": 0.24, "frame_decode": "full decode via ffmpeg -xerror succeeded",
    }
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--probe", action="store_true", help="validate sources and print the render plan")
    args = parser.parse_args()
    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            fail(f"missing required tool: {binary}")
    manifest_path = args.manifest.expanduser().resolve()
    manifest = json.loads(manifest_path.read_text())
    scenes = manifest.get("scenes")
    if not isinstance(scenes, list) or len(scenes) != 13:
        fail("v18 requires exactly 13 complete scenes")
    if manifest.get("fps") != FPS or manifest.get("width") != WIDTH or manifest.get("height") != HEIGHT:
        fail("v18 must be 1080x1920 at 30 fps")
    if sum(int(scene["frames"]) for scene in scenes) != manifest.get("duration_frames"):
        fail("scene durations do not sum to the declared frame count")
    if manifest["duration_frames"] != 1800:
        fail("v18 duration must be exactly 1800 frames / 60 seconds")
    if len({scene["name"] for scene in scenes}) != 13:
        fail("scene names must be unique")
    for scene in scenes:
        if scene["iq"] <= 0 or scene["frames"] not in (120, 150, 180):
            fail(f"invalid IQ or duration in {scene['id']}")
    if args.probe:
        print(json.dumps({
            "scenes": [{k: s[k] for k in ("id", "name", "iq", "frames", "image")} for s in scenes],
            "duration_frames": manifest["duration_frames"], "fps": FPS,
            "duration_seconds": manifest["duration_frames"] / FPS,
            "output": str(resolve(manifest["output"])),
            "audio": str(resolve(manifest["audio"])), "grain": str(resolve(manifest["grain"])),
        }, indent=2, ensure_ascii=False))
        return

    with tempfile.TemporaryDirectory(prefix="iq_gallery_v18_") as temp_name:
        backgrounds, title_sequences, card_records = alpha_overlays_and_cards(manifest, Path(temp_name))
        make_contact_sheet(manifest)
        report = render(manifest, backgrounds, title_sequences)
    report["scenes"] = card_records
    Path(str(resolve(manifest["output"])) + ".report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    )
    print(json.dumps({"output": report["output"], "sha256": report["sha256"], "frames": 1800}, indent=2))


if __name__ == "__main__":
    main()
