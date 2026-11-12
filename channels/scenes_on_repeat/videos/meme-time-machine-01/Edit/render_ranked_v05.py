"""Render the revised Meme Time Machine layout and visual transitions."""
import hashlib
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw, ImageFont

EPISODE = Path(__file__).resolve().parents[1]
EDIT = EPISODE / "Edit"
MIX = EDIT / "mix-v03.m4a"
OUTPUT = EPISODE / "Deliverables" / "meme-time-machine-01_draft-v05.mp4"
FONT = "/System/Library/Fonts/Avenir Next.ttc"
WIDTH, HEIGHT, FPS = 1080, 1920, 24
CREAM, GOLD, SHADOW = "#F9EED6", "#FFD07D", "#211C20"
TITLES = {1: "Corn Kid", 2: "Bottle Flip", 3: "Baby Yoda", 4: "Gru’s Plan", 5: "Dramatic Chipmunk"}
ROW_TOP, ROW_STEP = 1380, 65
CAPTION_TOP = 1284
BLUR_SIGMA = 17  # At the working scale of 270 × 480.
TRANSITION_FRAMES = 6


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def font(size, index=0):
    return ImageFont.truetype(FONT, size, index=index)


def rank_graphic(path, rank, revealed):
    image = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    title_font = font(92)
    while draw.textlength(TITLES[rank], font=title_font) > 925:
        title_font = font(title_font.size - 2)
    draw.text((540, 455), TITLES[rank], anchor="mm", font=title_font, fill=CREAM,
              stroke_width=2, stroke_fill=SHADOW)

    for place, title in TITLES.items():
        y = ROW_TOP + (place - 1) * ROW_STEP
        active = place == rank
        visible = place in revealed
        color = GOLD if active else CREAM
        draw.text((107, y), str(place), anchor="mm", font=font(49), fill=color,
                  stroke_width=1, stroke_fill=SHADOW)
        if visible:
            draw.text((149, y), title, anchor="lm", font=font(50, 2),
                      fill=color, stroke_width=1, stroke_fill=SHADOW)
    image.save(path)


def caption_graphic(path, line, last):
    image = Image.new("RGBA", (960, 76))
    draw = ImageDraw.Draw(image)
    draw.text((480, 37), line, anchor="mm", font=font(54 if last else 49),
              fill=GOLD if last else CREAM, stroke_width=2, stroke_fill=SHADOW)
    image.save(path)


def run():
    previous = json.loads((EDIT / "export-contract-v03.json").read_text())
    segments = previous["segments"]
    order = list(dict.fromkeys(segment["rank"] for segment in segments))
    assert order == [2, 4, 3, 5, 1] and previous["fps"] == FPS

    with TemporaryDirectory(prefix="scenes-meme-v05-") as temp_name:
        temp = Path(temp_name)
        args = ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-n",
                "-filter_complex_threads", "2"]
        graph = []
        position = 0
        reveals = []
        for index, segment in enumerate(segments):
            source = EPISODE / segment["source"]
            assert digest(source) == segment["sha256"], source
            assert segment["frame_in"] == position
            position = segment["frame_out_exclusive"]
            frames = position - segment["frame_in"]
            args += ["-ss", str(segment["source_in_seconds"]), "-t", f"{frames / FPS + 0.1:.6f}",
                     "-i", str(source)]

            if not reveals or reveals[-1]["rank"] != segment["rank"]:
                reveals.append({"rank": segment["rank"], "frame_in": segment["frame_in"],
                                "title": TITLES[segment["rank"]]})
            reveals[-1]["frame_out_exclusive"] = position

            crop = f'crop={segment["source_crop"]},' if segment["source_crop"] else ""
            graph += [
                f"[{index}:v]{crop}fps={FPS},tpad=stop_mode=clone:stop_duration=0.09,"
                f"trim=end_frame={frames},setpts=N/({FPS}*TB),format=yuv420p,"
                f"split=2[clean{index}][duplicate{index}]",
                f"[clean{index}]scale={WIDTH}:640:force_original_aspect_ratio=decrease:"
                f"force_divisible_by=2:flags=lanczos,setsar=1[foreground{index}]",
                f"[duplicate{index}]scale=270:480:flags=bilinear,setsar=1,"
                f"gblur=sigma={BLUR_SIGMA}:steps=3,eq=contrast=0.91:brightness=-0.14:saturation=0.90,"
                f"scale={WIDTH}:{HEIGHT}:flags=bilinear[background{index}]",
                f"[background{index}][foreground{index}]overlay=(W-w)/2:(H-h)/2:shortest=1[v{index}]",
            ]

        assert position == previous["frames"]
        # Keep the intra-meme cut in Corn Kid. Only a new rank starts a slide.
        rank_clips = []
        transitions = []
        for index, reveal in enumerate(reveals):
            rank = reveal["rank"]
            indices = [i for i, segment in enumerate(segments) if segment["rank"] == rank]
            input_video = f"v{indices[0]}"
            if len(indices) > 1:
                inputs = "".join(f"[v{i}]" for i in indices)
                input_video = f"joined{rank}"
                graph.append(f"{inputs}concat=n={len(indices)}:v=1:a=0[{input_video}]")
            # One cloned incoming frame lets the slide begin immediately before the cut.
            # The live first frame of the incoming clip still lands on its audio cue.
            start_pad = 1 if index else 0
            end_pad = TRANSITION_FRAMES - 1 if index < len(reveals) - 1 else 0
            label = f"ready{rank}"
            graph.append(f"[{input_video}]format=yuv444p,"
                         f"tpad=start={start_pad}:stop={end_pad}:start_mode=clone:stop_mode=clone,"
                         f"settb=expr=1/{FPS},setpts=N[{label}]")
            rank_clips.append(label)

        previous_video = rank_clips[0]
        for index, reveal in enumerate(reveals[1:], start=1):
            start = reveal["frame_in"] - 1
            label = f"slide{index}"
            graph.append(f"[{previous_video}][{rank_clips[index]}]xfade=transition=slideleft:"
                         f"duration={TRANSITION_FRAMES / FPS:.6f}:offset={start / FPS:.6f}[{label}]")
            previous_video = label
            transitions.append({"kind": "slideleft", "frame_in": start,
                                "frame_out_exclusive": start + TRANSITION_FRAMES,
                                "rank_switch_frame": reveal["frame_in"]})
        graph.append(f"[{previous_video}]trim=end_frame={position},format=yuv420p[cutv]")
        previous_video = "cutv"
        image_index = len(segments)
        revealed = set()
        for reveal in reveals:
            rank = reveal["rank"]
            revealed.add(rank)
            reveal["revealed"] = {str(place): TITLES[place] for place in sorted(revealed)}
            path = temp / f"rank-{rank}.png"
            rank_graphic(path, rank, revealed)
            args += ["-framerate", str(FPS), "-i", str(path)]
            label = f"ranked{rank}"
            start, end = reveal["frame_in"], reveal["frame_out_exclusive"]
            graph.append(f"[{previous_video}][{image_index}:v]overlay=eof_action=repeat:"
                         f"enable='gte(n,{start})*lt(n,{end})'[{label}]")
            previous_video = label
            image_index += 1

        for index, cue in enumerate(previous["caption_cues"]):
            path = temp / f"caption-{index}.png"
            caption_graphic(path, cue["text"], index == len(previous["caption_cues"]) - 1)
            args += ["-framerate", str(FPS), "-i", str(path)]
            label = f"captioned{index}"
            graph.append(f"[{previous_video}][{image_index}:v]overlay=60:{CAPTION_TOP}:eof_action=repeat:"
                         f"enable='gte(t,{cue['start']})*lt(t,{cue['end']})'[{label}]")
            previous_video = label
            image_index += 1

        graph.append(f"[{previous_video}]format=yuv420p[outv]")
        args += ["-i", str(MIX), "-filter_complex", ";".join(graph), "-map", "[outv]",
                 "-map", f"{image_index}:a:0", "-c:v", "libx264", "-crf", "18", "-preset", "fast",
                 "-profile:v", "high", "-r", str(FPS), "-pix_fmt", "yuv420p", "-colorspace", "bt709",
                 "-color_trc", "bt709", "-color_primaries", "bt709", "-color_range", "tv",
                 "-c:a", "copy", "-movflags", "+faststart", str(OUTPUT)]

        contract = {
            **previous, "revision": "v05", "layout": "Meme Time Machine",
            "output": str(OUTPUT), "rank_reveals": reveals, "transitions": transitions,
            "composition": {
                "foreground_window": [WIDTH, 640], "foreground_fit": "preserve aspect, centered",
                "background": "synchronized duplicate of the same crop, stretched on both axes",
                "background_blur": {"filter": "gblur", "sigma": BLUR_SIGMA, "steps": 3,
                                    "working_dimensions": [270, 480]},
                "title_y": 455, "rank_row_centers": [ROW_TOP + (place - 1) * ROW_STEP for place in TITLES],
                "caption_top": CAPTION_TOP, "active_row_highlight": "text color only",
            },
            "audio": {**previous["audio"], "source": str(MIX.relative_to(EPISODE)),
                      "source_sha256": digest(MIX), "mode": "AAC stream copy",
                      "stream_sha256": "603ee3dbee12d0f1c033068956600f38aa39bd1a4d966d3913093e551a44d80e"},
        }
        (EDIT / "export-contract-v05.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n")
        (EDIT / "render-command-v05.json").write_text(json.dumps(args, indent=2) + "\n")
        subprocess.run(args, check=True)


if __name__ == "__main__":
    run()
