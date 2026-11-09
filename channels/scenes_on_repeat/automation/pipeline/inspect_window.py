#!/usr/bin/env python3
"""Index the source cuts in a candidate scene and show each shot at three points."""

import argparse
import io
import json
import math
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


def seconds(value):
    fields = value.split(":")
    if len(fields) > 3:
        raise argparse.ArgumentTypeError("Use seconds or HH:MM:SS.sss")
    try:
        result = sum(float(field) * 60 ** i for i, field in enumerate(reversed(fields)))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use seconds or HH:MM:SS.sss") from exc
    if not math.isfinite(result) or result < 0:
        raise argparse.ArgumentTypeError("Time must be finite and nonnegative")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("start", type=seconds)
    parser.add_argument("end", type=seconds)
    parser.add_argument("output", type=Path, help="Output filename stem")
    parser.add_argument("--threshold", type=float, default=10)
    args = parser.parse_args()
    if args.end <= args.start or not 0 < args.threshold <= 100:
        parser.error("Need end > start and a threshold above 0 and at most 100")
    report = subprocess.run(
        ["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-ss", str(args.start),
         "-i", str(args.source), "-t", str(args.end - args.start), "-map", "0:v:0",
         "-an", "-vf", f"scale=480:-2,scdet=threshold={args.threshold},showinfo", "-f", "null", "-"],
        capture_output=True, check=True, text=True,
    )
    frames = [float(t) for t in re.findall(r"\bn:\s*\d+\s+pts:\s*-?\d+\s+pts_time:([\d.e+-]+)", report.stderr)]
    frames = [t for t in frames if t >= 0 and round(args.start + t, 6) < round(args.end, 6)]
    cuts = {round(float(t), 6) for t in re.findall(r"lavfi.scd.time: ([\d.e+-]+)", report.stderr)}
    if not frames:
        raise SystemExit("No decoded frames in the source range")
    bounds = [0, *(i for i, t in enumerate(frames) if i and round(t, 6) in cuts), len(frames)]
    shots = []
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for group in range(0, len(bounds) - 1, 8):
        rows = list(zip(bounds[group:group + 8], bounds[group + 1:group + 9]))
        sheet = Image.new("RGB", (960, len(rows) * 165), "#151515")
        draw = ImageDraw.Draw(sheet)
        for offset, (start, end) in enumerate(rows):
            sample_indices = (start, (start + end - 1) // 2, end - 1)
            times = [round(args.start + frames[f], 6) for f in sample_indices]
            y = 165 * offset
            for column, stamp in enumerate(times):
                data = subprocess.check_output(
                    ["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{max(0, stamp - 0.0005):.6f}",
                     "-i", str(args.source), "-map", "0:v:0", "-frames:v", "1",
                     "-vf", "scale=320:138:force_original_aspect_ratio=decrease,setsar=1",
                     "-c:v", "mjpeg", "-threads", "1", "-f", "image2pipe", "-"],
                )
                if not data:
                    raise SystemExit(f"No source image at {stamp:.3f} s")
                with Image.open(io.BytesIO(data)) as frame:
                    sheet.paste(frame, (320 * column + (320 - frame.width) // 2, y))
                draw.text((320 * column + 6, y + 142), f"{group + offset + 1:02d} / {stamp:.3f}s",
                          fill="#ffffff")
            shot_out = round(args.start + frames[end], 6) if end < len(frames) else args.end
            shots.append({"in": times[0], "out": shot_out, "samples": times})
        sheet.save(args.output.with_name(f"{args.output.name}-{group // 8 + 1:02}.jpg"), quality=85)
    args.output.with_suffix(".json").write_text(json.dumps(shots, indent=2) + "\n")


if __name__ == "__main__":
    main()
