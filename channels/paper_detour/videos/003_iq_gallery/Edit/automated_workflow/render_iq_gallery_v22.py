#!/usr/bin/env python3
"""Render a full-card IQ Gallery manifest with separate paper title overlays."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[5]
MANIFEST = ROOT / "channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/iq_gallery_v22_manifest.json"
OUTPUT = ROOT / "channels/paper_detour/legacy/025_iq_gallery/Deliverables/025_iq_gallery_paper_detour_60s_v22.mp4"
REPORT = ROOT / "channels/paper_detour/videos/003_iq_gallery/Edit/automated_workflow/QA_V22_RENDER_REPORT.json"
EXPECTED_FRAMES = 1800
FPS = 30
WIDTH = 1080
HEIGHT = 1920
TITLE_FADE_IN_FRAMES = 9
TITLE_FADE_OUT_FRAMES = 12
GRAIN_ALPHA = 0.4


def cmd(args: list[str]) -> None:
    subprocess.run(args, check=True)


def probe(path: pathlib.Path) -> dict[str, Any]:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def audio_packets(path: pathlib.Path) -> list[dict[str, Any]]:
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a:0", "-show_packets",
            "-show_entries", "packet=data_hash", "-show_data_hash", "sha256", "-of", "json", str(path)
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)["packets"]


def require_file(path: pathlib.Path, label: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"missing {label}: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a full-card IQ Gallery manifest.")
    parser.add_argument("--manifest", type=pathlib.Path, default=MANIFEST)
    parser.add_argument("--output", type=pathlib.Path, default=OUTPUT)
    parser.add_argument("--report", type=pathlib.Path, default=REPORT)
    options = parser.parse_args()
    manifest_path = options.manifest.resolve()
    output_path = options.output.resolve()
    report_path = options.report.resolve()

    require_file(manifest_path, "manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    scenes = manifest["scenes"]
    title_y_offset = int(manifest.get("title_y_offset", 0))
    if title_y_offset < 0:
        raise ValueError("title_y_offset must be zero or greater")
    total = sum(item["frames"] for item in scenes)
    if total != EXPECTED_FRAMES or manifest.get("duration_frames") != EXPECTED_FRAMES:
        raise ValueError(f"scene frames must total {EXPECTED_FRAMES}, got {total}")
    if manifest.get("fps") != FPS or (manifest.get("width"), manifest.get("height")) != (WIDTH, HEIGHT):
        raise ValueError("manifest output dimensions or frame rate differ from the vertical-card contract")

    audio = ROOT / manifest["audio_source"]
    grain = ROOT / manifest["grain_source"]
    require_file(audio, "existing music mix")
    require_file(grain, "existing grain loop")
    audio_meta = probe(audio)
    audio_stream = next(stream for stream in audio_meta["streams"] if stream.get("codec_type") == "audio")
    if audio_stream.get("codec_name") != "aac":
        raise ValueError("the reused music mix must be AAC so it can be copied without re-encoding")
    if float(audio_stream.get("duration", 0)) < EXPECTED_FRAMES / FPS - 0.025:
        raise ValueError("the existing music mix is shorter than the video")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {output_path}")
    if report_path.exists():
        raise FileExistsError(f"refusing to overwrite existing report: {report_path}")

    with tempfile.TemporaryDirectory(prefix=".iq_gallery_", dir=output_path.parent) as temp_dir:
        temp = pathlib.Path(temp_dir)
        inputs: list[pathlib.Path] = []
        args = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-filter_complex_threads", "1"]
        fade_in = TITLE_FADE_IN_FRAMES / FPS
        fade_out = TITLE_FADE_OUT_FRAMES / FPS
        graph: list[str] = []
        segment_labels: list[str] = []

        for index, scene in enumerate(scenes):
            scene_path = ROOT / scene["scene"]
            title_path = ROOT / scene["title"]
            require_file(scene_path, f"scene {scene['id']}")
            require_file(title_path, f"title {scene['id']}")
            inputs.extend((scene_path, title_path))
            args += ["-loop", "1", "-framerate", str(FPS), "-i", str(scene_path)]
            args += ["-loop", "1", "-framerate", str(FPS), "-i", str(title_path)]
            frames = scene["frames"]
            duration = frames / FPS
            bg_index = index * 2
            title_index = bg_index + 1
            bg = f"bg{index}"
            title = f"title{index}"
            composite = f"card{index}"
            end_fade = max(0.0, duration - fade_out)
            graph.append(
                f"[{bg_index}:v]scale={WIDTH}:{HEIGHT}:flags=lanczos,setsar=1,fps={FPS},"
                f"trim=end_frame={frames},setpts=PTS-STARTPTS,format=rgba[{bg}]"
            )
            graph.append(
                f"[{title_index}:v]format=rgba,fade=t=in:st=0:d={fade_in:.9f}:alpha=1,"
                f"fade=t=out:st={end_fade:.9f}:d={fade_out:.9f}:alpha=1,"
                f"trim=end_frame={frames},setpts=PTS-STARTPTS[{title}]"
            )
            graph.append(
                f"[{bg}][{title}]overlay=0:{title_y_offset}:shortest=1:format=auto,format=yuv420p,"
                f"settb=AVTB,setpts=PTS-STARTPTS[{composite}]"
            )
            segment_labels.append(f"[{composite}]")

        concat_label = "cards"
        graph.append(f"{''.join(segment_labels)}concat=n={len(scenes)}:v=1:a=0[{concat_label}]")

        grain_index = len(inputs)
        args += ["-stream_loop", "-1", "-i", str(grain)]
        audio_index = grain_index + 1
        args += ["-i", str(audio)]
        graph.append(
            f"[{grain_index}:v]scale={WIDTH}:{HEIGHT}:flags=lanczos,fps={FPS},format=rgba,"
            f"colorchannelmixer=aa={GRAIN_ALPHA:.3f}[grain]"
        )
        graph.append(
            f"[{concat_label}][grain]overlay=0:0:shortest=1:format=auto,"
            f"trim=end_frame={EXPECTED_FRAMES},settb=AVTB,setpts=PTS-STARTPTS,"
            f"format=yuv420p,setsar=1[outv]"
        )

        temp_mp4 = temp / "verified.mp4"
        args += [
            "-filter_complex", ";".join(graph),
            "-map", "[outv]", "-map", f"{audio_index}:a:0",
            "-frames:v", str(EXPECTED_FRAMES), "-t", str(EXPECTED_FRAMES / FPS),
            "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", "-n", str(temp_mp4),
        ]
        print("Rendering 13 full-frame cards with title fades, direct cuts, continuous grain, and copied music.", file=sys.stderr, flush=True)
        cmd(args)
        cmd(["ffmpeg", "-v", "error", "-xerror", "-i", str(temp_mp4), "-f", "null", "-"])

        actual = probe(temp_mp4)
        video_stream = next(stream for stream in actual["streams"] if stream.get("codec_type") == "video")
        output_audio = next(stream for stream in actual["streams"] if stream.get("codec_type") == "audio")
        if (int(video_stream["width"]), int(video_stream["height"])) != (WIDTH, HEIGHT):
            raise ValueError("rendered video dimensions do not match the output contract")
        if video_stream.get("codec_name") != "h264" or output_audio.get("codec_name") != "aac":
            raise ValueError("rendered output codecs do not match H.264/AAC")
        if int(video_stream.get("nb_frames", -1)) != EXPECTED_FRAMES:
            raise ValueError(f"expected {EXPECTED_FRAMES} video frames; got {video_stream.get('nb_frames')}")
        if abs(float(video_stream.get("duration", 0)) - EXPECTED_FRAMES / FPS) > 0.02:
            raise ValueError("rendered video duration is not 60 seconds")
        if int(output_audio.get("sample_rate", 0)) != 44100 or int(output_audio.get("channels", 0)) != 2:
            raise ValueError("reused music mix channel layout or sample rate changed")

        source_packets = audio_packets(audio)
        output_packets = audio_packets(temp_mp4)
        if not output_packets or source_packets[: len(output_packets)] != output_packets:
            raise ValueError("output audio packets differ from the existing source mix")
        validation = {
            "full_decode": "passed with ffmpeg -xerror",
            "video": {
                "codec": video_stream["codec_name"],
                "dimensions": f"{WIDTH}x{HEIGHT}",
                "fps": FPS,
                "frames": EXPECTED_FRAMES,
                "duration_seconds": float(video_stream["duration"]),
            },
            "audio": {
                "codec": output_audio["codec_name"],
                "sample_rate": int(output_audio["sample_rate"]),
                "channels": int(output_audio["channels"]),
                "duration_seconds": float(output_audio.get("duration", 0)),
                "packets": len(output_packets),
                "source_packet_hashes_match": True,
                "source": str(audio),
            },
            "picture_review": "not assessed by the renderer; see the dedicated QA report for the actual review",
            "playback": "continuous 1x video viewing and subjective listening not performed",
            "editing": f"one complete static scene image per card; direct cuts; separate title PNG fades in/out; title_y_offset={title_y_offset}px; no parallax",
            "sound_generation": "none; existing AAC music mix copied without re-encoding",
        }
        validation["title_y_offset_px"] = title_y_offset
        report_data = {"manifest": str(manifest_path), "output": str(output_path), "validation": validation}
        temp_report = temp / "report.json"
        temp_report.write_text(json.dumps(report_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.link(temp_mp4, output_path)
        try:
            os.link(temp_report, report_path)
        except FileExistsError:
            raise FileExistsError(f"video saved but report path already exists: {report_path}")
        print(json.dumps({"output": str(output_path), "report": str(report_path), "validation": validation}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, FileNotFoundError, FileExistsError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
