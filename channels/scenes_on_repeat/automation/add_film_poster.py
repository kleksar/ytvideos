#!/usr/bin/env python3
"""Add the official film poster to the last five seconds of a 1080x1920 CFR short."""
import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path

from PIL import Image

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("source", type=Path)
parser.add_argument("output", type=Path)
parser.add_argument("poster", type=Path)
parser.add_argument("--picture-top", action="append", required=True, metavar="FRAME:Y",
                    help="First frame and upper edge of the picture for each ending shot")
parser.add_argument("--details-overlay", type=Path,
                    help="Transparent upper-panel artwork with film details to the right of the poster")
parser.add_argument("--subscribe-overlay", nargs=3, metavar=("FILE", "X", "Y"),
                    help="Looping alpha video for the lower subscribe ticket")
args = parser.parse_args()

probe = subprocess.check_output([
    "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
    "-show_entries", "stream=width,height,avg_frame_rate,r_frame_rate,nb_read_frames",
    "-of", "json", str(args.source),
])
video, = json.loads(probe)["streams"]
fps = Fraction(video["avg_frame_rate"])
if (video["width"], video["height"]) != (1080, 1920) or fps != Fraction(video["r_frame_rate"]):
    parser.error("input must be a 1080x1920 CFR short")
frames = int(video["nb_read_frames"])
start_frame = max(0, frames - round(5 * fps))

# Keep the artwork above the picture even when the picture's upper edge changes.
try:
    boundaries = [(int(frame), int(y)) for frame, y in
                  (item.split(":") for item in args.picture_top)]
except ValueError:
    parser.error("--picture-top must use FRAME:Y")
if (boundaries[0][0] != start_frame or
    any(not start_frame <= frame < frames or not 160 <= y <= 1920 for frame, y in boundaries) or
    any(a >= b for (a, _), (b, _) in zip(boundaries, boundaries[1:]))):
    parser.error("picture-top entries must start at the poster and increase within the ending")
upper_block = video["height"] // 3
panel_height = min(upper_block, min(y for _, y in boundaries)) // 2 * 2
max_width, max_height = 960, min(510, panel_height - 50)
if args.details_overlay:
    if panel_height != upper_block:
        parser.error("film details require the full upper panel")
    max_width, max_height = 344, panel_height - 88
with Image.open(args.poster) as poster:
    source_width, source_height = poster.size
    if poster.getexif().get(274) in (5, 6, 7, 8):
        source_width, source_height = source_height, source_width
fit = min(max_width / source_width, max_height / source_height)
poster_width = max(2, round(source_width * fit / 2) * 2)
poster_height = max(2, round(source_height * fit / 2) * 2)
art_y = (panel_height - poster_height) // 4 * 2
art_center_x = 232 if args.details_overlay else video["width"] // 2
art_x = (art_center_x - poster_width // 2) // 2 * 2
graph = [
    f"[1:v]scale={poster_width}:{poster_height},setsar=1,format=rgba,"
    f"fade=t=in:st={start_frame / float(fps):.6f}:d=0.6:alpha=1[art]",
]
progress = f"max(0\\,min(1\\,1-(n-{start_frame})/({float(fps)}*0.6)))"
graph.append(f"[0:v][art]overlay=x='{art_x}-120*pow({progress}\\,3)':y={art_y}:"
             f"enable='gte(n,{start_frame})'[withposter]")
base = "withposter"
details_input = []
if args.details_overlay:
    details_input = ["-loop", "1", "-framerate", str(fps), "-i", str(args.details_overlay)]
    graph.append(f"[2:v]format=rgba,fade=t=in:st={start_frame / float(fps):.6f}:"
                 "d=0.6:alpha=1[details]")
    graph.append(f"[{base}][details]overlay=x='120*pow({progress}\\,3)':y=0:"
                 f"enable='gte(n,{start_frame})'[withdetails]")
    base = "withdetails"
subscribe_input = []
if args.subscribe_overlay:
    ticket, x, y = args.subscribe_overlay
    try:
        x, y = int(x), int(y)
    except ValueError:
        parser.error("--subscribe-overlay coordinates must be integers")
    index = 3 if args.details_overlay else 2
    subscribe_input = ["-stream_loop", "-1", "-i", ticket]
    graph.append(f"[{base}][{index}:v]overlay=x={x}:y={y}:shortest=1[withticket]")
    base = "withticket"
graph.append(f"[{base}]trim=end_frame={frames}[v]")

subprocess.run([
    "ffmpeg", "-nostdin", "-v", "error", "-n", "-filter_complex_threads", "2",
    "-i", str(args.source), "-loop", "1", "-framerate", str(fps), "-i", str(args.poster),
    *details_input, *subscribe_input,
    "-filter_complex", ";".join(graph),
    "-map", "[v]", "-map", "0:a:0", "-map_chapters", "-1", "-fps_mode", "passthrough",
    "-frames:v", str(frames),
    "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-threads", "6",
    "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
    "-c:a", "copy", "-movflags", "+faststart+write_colr", str(args.output),
], check=True)
print(json.dumps({
    "first_poster_frame": start_frame, "frames": frames, "fps": str(fps),
    "poster_x": art_x, "poster_y": art_y, "poster_width": poster_width,
    "poster_height": poster_height, "poster_source_size": [source_width, source_height],
    "panel_height": panel_height,
}))
