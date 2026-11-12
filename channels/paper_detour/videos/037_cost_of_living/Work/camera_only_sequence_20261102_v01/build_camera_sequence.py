#!/usr/bin/env python3
"""Render the accepted Paper still map as camera-only H.264 scenes."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


EPISODE = Path(__file__).resolve().parents[2]
RUN = Path(__file__).resolve().parent
SCRATCH = RUN / "scratch"
SEGMENTS = SCRATCH / "segments"
TIMING = EPISODE / "Edit/Timeline/timing_map_v01.json"
OUTPUT = RUN / "previews/037_v01_camera_only_video.mp4"
FPS = 30
WIDTH = 2560
HEIGHT = 1440


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def motion_filter(move: str, frames: int) -> str:
    n = max(1, frames - 1)
    smooth = f"(on/{n})*(on/{n})*(3-2*on/{n})"
    if move == "push-in":
        zoom = f"1+0.035*{smooth}"
        x = "(iw-iw/zoom)/2"
        y = "(ih-ih/zoom)/2"
    elif move == "pull-out":
        zoom = f"1.035-0.035*{smooth}"
        x = "(iw-iw/zoom)/2"
        y = "(ih-ih/zoom)/2"
    elif move == "pan-right":
        zoom = "1.04"
        x = f"(iw-iw/zoom)*{smooth}"
        y = "(ih-ih/zoom)/2"
    elif move == "pan-left":
        zoom = "1.04"
        x = f"(iw-iw/zoom)*(1-{smooth})"
        y = "(ih-ih/zoom)/2"
    else:
        raise ValueError(f"Unsupported accepted motion: {move}")
    return (
        f"scale={WIDTH}:{HEIGHT},"
        f"zoompan=z='{zoom}':x='{x}':y='{y}':d={frames}:"
        f"s={WIDTH}x{HEIGHT}:fps={FPS},setsar=1"
    )


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    data = json.loads(TIMING.read_text())
    scenes = data["scenes"]
    if len(scenes) != 73 or data["parallax"] != "disabled":
        raise RuntimeError("Unexpected scene count or parallax state")
    SEGMENTS.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    entries = []
    input_log = []
    expected_frame = 0
    for index, scene in enumerate(scenes):
        if scene["start_frame"] != expected_frame:
            raise RuntimeError(f"Frame gap/overlap before {scene['scene']}")
        frames = scene["end_frame"] - scene["start_frame"]
        if not 120 <= frames <= 180:
            raise RuntimeError(f"Duration outside 4-6 s: {scene['scene']} = {frames} frames")
        source = EPISODE / "Source/Images/paper_v01" / scene["filename"]
        if not source.is_file():
            raise FileNotFoundError(source)
        segment = SEGMENTS / f"{index + 1:02d}_{scene['scene']}.mp4"
        cmd = [
            "ffmpeg", "-hide_banner", "-y", "-i", str(source),
            "-filter_complex", f"[0:v]{motion_filter(scene['motion'], frames)}[v]",
            "-map", "[v]", "-frames:v", str(frames), "-an",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-pix_fmt", "yuv420p", "-color_primaries", "bt709",
            "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
            "-movflags", "+faststart", str(segment),
        ]
        run(cmd)
        entries.append(segment)
        input_log.append({
            "scene": scene["scene"], "source": str(source),
            "source_sha256": sha256(source), "segment": str(segment),
            "frames": frames, "motion": scene["motion"],
        })
        expected_frame = scene["end_frame"]
        print(f"Rendered {scene['scene']} ({frames} frames)", flush=True)
    if expected_frame != data["total_frames"]:
        raise RuntimeError("Final frame count does not match timing map")
    concat_file = SCRATCH / "segments.ffconcat"
    concat_file.write_text("ffconcat version 1.0\n" + "".join(f"file '{p.as_posix()}'\n" for p in entries))
    run([
        "ffmpeg", "-hide_banner", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file), "-c", "copy", "-movflags", "+faststart", str(OUTPUT),
    ])
    receipt = {
        "status": "RENDERED_VIDEO_ONLY",
        "output": str(OUTPUT), "output_sha256": sha256(OUTPUT),
        "timing_map": str(TIMING), "fps": FPS, "width": WIDTH,
        "height": HEIGHT, "frames": data["total_frames"],
        "duration_s": data["duration_s"], "codec": "H.264",
        "audio": "none", "depth_parallax": "disabled",
        "motion": "whole-image 2D push/pull and horizontal pan only",
        "encoder": "FFmpeg libx264 medium CRF 19; Rec.709; yuv420p",
        "segments": input_log,
    }
    (RUN / "render_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({k: receipt[k] for k in (
        "status", "output", "output_sha256", "frames", "duration_s", "width", "height"
    )}, indent=2))


if __name__ == "__main__":
    main()
