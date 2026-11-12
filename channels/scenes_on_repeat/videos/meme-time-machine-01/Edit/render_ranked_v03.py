"""Render the local review cut from the five selected YouTube files."""
import hashlib
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw, ImageFont

EPISODE = Path(__file__).resolve().parents[1]
EDIT = EPISODE / "Edit"
SOURCE = EPISODE / "Source" / "YouTube"
OUTPUT = EPISODE / "Deliverables" / "meme-time-machine-01_draft-v03.mp4"
FONT = "/System/Library/Fonts/Avenir Next.ttc"
W, H, FPS = 1080, 1920, 24
RATE = 48000
SAMPLES_PER_FRAME = RATE // FPS

# (rank, filename, source in, output frames, source crop, audio gain in dB)
CUTS = [
    (2, "GdUVtEeg9I4.mkv", 14.958333, 58, "836:496:222:52", -3.0),
    (4, "yXcWolrJZ08.mkv", 3.333333, 198, "608:360:16:0", 10.0),
    (3, "R9SC0Up0TDE.mkv", 9.416667, 51, "392:232:436:258", 12.0),
    (5, "y8Kyi0WNg40.mkv", 0.250000, 61, "320:190:0:24", -5.0),
    (1, "1VbZE6YhjKk.mp4", 0.000000, 62, None, 0.5),
    (1, "1VbZE6YhjKk.mp4", 40.290000, 28, None, 0.5),
]

LABELS = {
    2: ("Bottle Flip", "REAL LIFE", "2016"),
    4: ("Gru’s Plan", "MOVIE", "2018"),
    3: ("Baby Yoda", "TV SERIES", "2019"),
    5: ("Dramatic Chipmunk", "VIRAL VIDEO", "2007"),
    1: ("Corn Kid", "REAL LIFE", "2022"),
}
ORDER = [2, 4, 3, 5, 1]
INK = "#121218"
CREAM = "#F9EED6"
GOLD = "#F8B242"


def typeface(size, index=0):
    return ImageFont.truetype(FONT, size, index=index)


def slate(rank, path):
    title, category, year = LABELS[rank]
    im = Image.new("RGBA", (W, H), INK)
    draw = ImageDraw.Draw(im)
    draw.text((72, 272), "SCENES ON REPEAT", font=typeface(31, 2), fill="#AAA5A1")
    draw.text((72, 320), "MEME TIME MACHINE", font=typeface(46), fill=CREAM)
    draw.line((72, 401, 950, 401), fill="#4B4140", width=2)

    badge_color = GOLD if rank == 1 else "#2B2628"
    badge_text = INK if rank == 1 else GOLD
    draw.rounded_rectangle((72, 455, 266, 583), radius=28, fill=badge_color)
    draw.text((169, 521), f"#{rank}", font=typeface(88, 8), anchor="mm", fill=badge_text)
    draw.text((296, 454), f"{category}  /  {year}", font=typeface(30), fill=GOLD)
    size = 72
    while draw.textlength(title, font=typeface(size)) > 670:
        size -= 1
    draw.text((296, 500), title, font=typeface(size), fill=CREAM)
    draw.rectangle((0, 640, W - 1, 1279), fill=(0, 0, 0, 0))
    draw.rectangle((0, 637, W - 1, 639), fill=GOLD)
    draw.rectangle((0, 1280, W - 1, 1282), fill="#4B4140")

    active = ORDER.index(rank)
    for index in range(len(ORDER)):
        left = 72 + 59 * index
        color = GOLD if index == active else "#5B5050"
        draw.rounded_rectangle((left, 1584, left + 46, 1592), radius=4, fill=color)
    im.save(path)


def captions():
    # Gru timing is based on the actual source file's local word map.
    gru_offset = CUTS[0][3] / FPS - CUTS[1][2]
    cues = [
        (3.59, 4.82, "I fly to the moon."),
        (5.61, 6.57, "I shrink the moon."),
        (7.37, 8.35, "I grab the moon."),
        (9.30, 10.70, "I sit on the toilet..."),
        (10.88, 11.39, "What?"),
    ]
    for start, end, line in cues:
        yield start + gru_offset, end + gru_offset, line, CREAM, 62
    # Corn's opening is already captioned in the source.
    corn_start = sum(cut[3] for cut in CUTS[:-1]) / FPS
    yield corn_start + 0.11, corn_start + 1.14, "It’s corn!", GOLD, 72


def caption_image(path, line, color, size):
    im = Image.new("RGBA", (900, 106))
    draw = ImageDraw.Draw(im)
    draw.text((450, 53), line, font=typeface(size), anchor="mm", fill=color, stroke_width=2,
              stroke_fill=INK)
    im.save(path)


def main():
    with TemporaryDirectory(prefix="scenes-meme-v03-") as temp_name:
        temp = Path(temp_name)
        args = ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-n", "-filter_complex_threads", "2"]
        manifest = []
        position = 0
        for rank, filename, start, frames, crop, gain in CUTS:
            source = SOURCE / filename
            duration = frames / FPS
            args += ["-ss", f"{start:.6f}", "-t", f"{duration + 0.1:.6f}", "-i", str(source)]
            manifest.append({
                "rank": rank, "source": str(source.relative_to(EPISODE)),
                "youtube_id": source.stem, "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "source_in_seconds": start, "source_out_seconds": round(start + duration, 6),
                "frame_in": position, "frame_out_exclusive": position + frames,
                "source_crop": crop, "audio_gain_db": gain,
            })
            position += frames

        for rank in ORDER:
            art = temp / f"rank-{rank}.png"
            slate(rank, art)
            args += ["-framerate", str(FPS), "-i", str(art)]

        graph = []
        for index, (rank, _file, _start, frames, crop, gain) in enumerate(CUTS):
            duration = frames / FPS
            cropped = f"crop={crop}," if crop else ""
            graph.append(
                f"[{index}:v]{cropped}fps={FPS},"
                "scale=1080:640:force_original_aspect_ratio=decrease:force_divisible_by=2:flags=lanczos,"
                "pad=1080:640:(ow-iw)/2:(oh-ih)/2:color=0x121218,"
                "setsar=1,tpad=stop_mode=clone:stop_duration=0.09,"
                f"trim=end_frame={frames},setpts=N/({FPS}*TB),format=yuv420p,"
                f"pad=1080:1920:0:640:color=0x121218[footage{index}]"
            )
            overlay_input = len(CUTS) + ORDER.index(rank)
            overlay_label = f"card{index}"
            graph.append(f"[{overlay_input}:v]format=rgba[{overlay_label}]")
            graph.append(f"[footage{index}][{overlay_label}]overlay=eof_action=repeat[v{index}]")

            # The opening of Corn Kid starts mid-breath, so it gets a shorter fade-in.
            fade_in = 0.015 if index == 4 else 0.075
            graph.append(
                f"[{index}:a]aresample={RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,"
                f"apad=whole_len={frames * SAMPLES_PER_FRAME},atrim=end_sample={frames * SAMPLES_PER_FRAME},"
                f"asetpts=N/SR/TB,volume={gain}dB,afade=t=in:d={fade_in},"
                f"afade=t=out:st={duration - 0.075:.6f}:d=0.075[a{index}]"
            )

        # The same single-frame rank card is referenced twice for the two Corn Kid edits.
        corn_input = len(CUTS) + ORDER.index(1)
        graph = [line for line in graph if not line.startswith(f"[{corn_input}:v]")]
        graph.insert(0, f"[{corn_input}:v]format=rgba,split=2[card4][card5]")
        streams = "".join(f"[v{i}][a{i}]" for i in range(len(CUTS)))
        graph.append(f"{streams}concat=n={len(CUTS)}:v=1:a=1[cutv][cuta]")
        preceding = "cutv"
        cue_manifest = []
        for index, (start, end, line, color, size) in enumerate(captions()):
            card = temp / f"caption-{index}.png"
            caption_image(card, line, color, size)
            args += ["-framerate", str(FPS), "-i", str(card)]
            input_index = len(CUTS) + len(ORDER) + index
            output_label = f"captioned{index}"
            graph.append(
                f"[{preceding}][{input_index}:v]overlay=90:1320:eof_action=repeat:"
                f"enable='gte(t,{start:.6f})*lt(t,{end:.6f})'[{output_label}]"
            )
            preceding = output_label
            cue_manifest.append({"start": round(start, 6), "end": round(end, 6), "text": line})
        graph.append(f"[{preceding}]format=yuv420p[v]")
        graph.append("[cuta]alimiter=limit=0.84:attack=5:release=60:level=0:latency=1[a]")
        args += [
            "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-profile:v", "high",
            "-r", str(FPS), "-pix_fmt", "yuv420p", "-colorspace", "bt709",
            "-color_trc", "bt709", "-color_primaries", "bt709", "-color_range", "tv",
            "-c:a", "aac", "-b:a", "256k", "-ar", str(RATE), "-ac", "2",
            "-movflags", "+faststart", str(OUTPUT),
        ]

        contract = {
            "revision": "v03", "purpose": "local review only", "output": str(OUTPUT),
            "width": W, "height": H, "fps": FPS, "frames": position,
            "duration": position / FPS, "visible_rank_order": ORDER, "segments": manifest, "caption_cues": cue_manifest,
            "video": {"codec": "H.264 High", "crf": 18, "pixel_format": "yuv420p", "color": "BT.709"},
            "audio": {"codec": "AAC-LC", "channels": 2, "sample_rate": RATE,
                      "bitrate_target": 256000, "sources": "the original five YouTube audio tracks",
                      "fade_seconds": 0.075, "corn_opening_fade_seconds": 0.015,
                      "limiter_linear_ceiling": 0.84, "speed": 1.0},
        }
        (EDIT / "export-contract-v03.json").write_text(json.dumps(contract, indent=2) + "\n")
        (EDIT / "render-command-v03.json").write_text(json.dumps(args, indent=2) + "\n")
        subprocess.run(args, check=True)


if __name__ == "__main__":
    main()
