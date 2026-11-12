"""Insert fading title cards before the approved Meme Time Machine excerpts."""
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from render_ranked_v06 import (
    BLUR_SIGMA, CAPTION_TOP, CREAM, EDIT, EPISODE, FPS, GOLD, HEIGHT, MIX,
    ROW_STEP, ROW_TOP, SHADOW, TITLES, WIDTH, caption_graphic, digest, font,
)

OUTPUT = EPISODE / "Deliverables" / "meme-time-machine-01_draft-v07.mp4"
CARD_FRAMES = 20
FADE_FRAMES = 7
SAMPLE_RATE = 48000
SAMPLES_PER_FRAME = SAMPLE_RATE // FPS


def title_image(path, title):
    image = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    face = font(100)
    while draw.textlength(title, font=face) > 940:
        face = font(face.size - 2)
    draw.text((WIDTH // 2, HEIGHT // 2), title, anchor="mm", font=face,
              fill=CREAM, stroke_width=2, stroke_fill=SHADOW)
    image.save(path)


def list_image(path, active_rank, revealed):
    image = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    for place, title in TITLES.items():
        y = ROW_TOP + (place - 1) * ROW_STEP
        color = GOLD if place == active_rank else CREAM
        draw.text((107, y), str(place), anchor="mm", font=font(49),
                  fill=color, stroke_width=1, stroke_fill=SHADOW)
        if str(place) in revealed:
            draw.text((149, y), title, anchor="lm", font=font(50),
                      fill=color, stroke_width=1, stroke_fill=SHADOW)
    image.save(path)


def run(temp):
    previous = json.loads((EDIT / "export-contract-v06.json").read_text())
    source_reveals = previous["rank_reveals"]
    assert digest(MIX) == previous["audio"]["source_sha256"]
    titles = []
    for index, reveal in enumerate(source_reveals):
        card_start = reveal["frame_in"] + index * CARD_FRAMES
        titles.append({"rank": reveal["rank"], "text": reveal["title"], "frame_in": card_start,
                       "frame_out_exclusive": card_start + CARD_FRAMES,
                       "fade_in_frames": FADE_FRAMES})
    total_frames = previous["frames"] + len(titles) * CARD_FRAMES
    title_by_rank = {title["rank"]: title for title in titles}
    args = ["ffmpeg", "-hide_banner", "-nostdin", "-loglevel", "error", "-n",
            "-filter_complex_threads", "2"]
    graph = []
    segments = []

    for index, original in enumerate(previous["segments"]):
        rank = original["rank"]
        source = EPISODE / original["source"]
        assert digest(source) == original["sha256"], source
        source_start, source_end = original["frame_in"], original["frame_out_exclusive"]
        frames = source_end - source_start
        shift = title_by_rank[rank]["frame_out_exclusive"] - next(
            reveal["frame_in"] for reveal in source_reveals if reveal["rank"] == rank)
        segments.append({**original, "frame_in": source_start + shift,
                         "frame_out_exclusive": source_end + shift})
        args += ["-ss", str(original["source_in_seconds"]), "-t", f"{frames / FPS + 0.1:.6f}",
                 "-i", str(source)]
        crop = f'crop={original["source_crop"]},' if original["source_crop"] else ""
        first_of_rank = index == 0 or previous["segments"][index - 1]["rank"] != rank
        background_outputs = (f",split=2[background{index}][still{rank}]" if first_of_rank
                              else f"[background{index}]")
        graph += [
            f"[{index}:v]{crop}fps={FPS},tpad=stop_mode=clone:stop_duration=0.09,"
            f"trim=end_frame={frames},setpts=N/({FPS}*TB),format=yuv420p,split=2[clean{index}][duplicate{index}]",
            f"[clean{index}]scale={WIDTH}:640:force_original_aspect_ratio=decrease:"
            f"force_divisible_by=2:flags=lanczos,setsar=1[foreground{index}]",
            f"[duplicate{index}]scale=270:480:flags=bilinear,setsar=1,"
            f"gblur=sigma={BLUR_SIGMA}:steps=3,eq=contrast=0.91:brightness=-0.14:saturation=0.90,"
            f"scale={WIDTH}:{HEIGHT}:flags=bilinear{background_outputs}",
            f"[background{index}][foreground{index}]overlay=(W-w)/2:(H-h)/2:shortest=1[v{index}]",
        ]

    image_index = len(segments)
    for title in titles:
        rank = title["rank"]
        path = temp / f"title-{rank}.png"
        title_image(path, title["text"])
        args += ["-framerate", str(FPS), "-i", str(path)]
        graph += [
            f"[still{rank}]trim=end_frame=1,tpad=stop={CARD_FRAMES - 1}:stop_mode=clone,"
            f"settb=1/{FPS},setpts=N,eq=brightness=-0.12[slate{rank}]",
            f"[{image_index}:v]format=rgba,tpad=stop={CARD_FRAMES - 1}:stop_mode=clone,"
            f"fade=t=in:s=0:n={FADE_FRAMES}:alpha=1[lettering{rank}]",
            f"[slate{rank}][lettering{rank}]overlay=shortest=1[card{rank}]",
        ]
        image_index += 1

    parts = []
    for index, segment in enumerate(segments):
        if index == 0 or segments[index - 1]["rank"] != segment["rank"]:
            parts.append(f'[card{segment["rank"]}]')
        parts.append(f"[v{index}]")
    graph.append(f'{"".join(parts)}concat=n={len(parts)}:v=1:a=0,settb=1/{FPS},setpts=N[cutv]')

    track = "cutv"
    reveals = []
    for index, title in enumerate(titles):
        original = source_reveals[index]
        reveals.append({**original, "frame_in": title["frame_out_exclusive"],
                        "frame_out_exclusive": original["frame_out_exclusive"] + (index + 1) * CARD_FRAMES})
    list_states = [(None, {}, 0, CARD_FRAMES)]
    for index, reveal in enumerate(reveals):
        end = reveals[index + 1]["frame_in"] if index + 1 < len(reveals) else total_frames
        list_states.append((reveal["rank"], reveal["revealed"], reveal["frame_in"], end))
    for rank, revealed, start, end in list_states:
        path = temp / f"list-{rank}.png"
        list_image(path, rank, revealed)
        args += ["-framerate", str(FPS), "-i", str(path)]
        label = f"ranked{rank}"
        graph.append(f"[{track}][{image_index}:v]overlay=eof_action=repeat:"
                     f"enable='gte(n,{start})*lt(n,{end})'[{label}]")
        track = label
        image_index += 1

    cues = []
    for index, cue in enumerate(previous["caption_cues"]):
        rank_index = next(i for i, reveal in enumerate(source_reveals)
                          if reveal["frame_in"] / FPS <= cue["start"] < reveal["frame_out_exclusive"] / FPS)
        shift = (rank_index + 1) * CARD_FRAMES / FPS
        start, end = cue["start"] + shift, cue["end"] + shift
        cues.append({**cue, "start": round(start, 6), "end": round(end, 6)})
        path = temp / f"caption-{index}.png"
        caption_graphic(path, cue["text"])
        args += ["-framerate", str(FPS), "-i", str(path)]
        label = f"captioned{index}"
        graph.append(f"[{track}][{image_index}:v]overlay=60:{CAPTION_TOP}:eof_action=repeat:"
                     f"enable='gte(t,{start:.6f})*lt(t,{end:.6f})'[{label}]")
        track = label
        image_index += 1
    graph.append(f"[{track}]format=yuv420p[outv]")

    args += ["-i", str(MIX)]
    taps = "".join(f"[audio{i}]" for i in range(len(titles)))
    graph.append(f"[{image_index}:a:0]asplit={len(titles)}{taps}")
    audio_parts = []
    for index, reveal in enumerate(source_reveals):
        start = reveal["frame_in"] * SAMPLES_PER_FRAME
        end = reveal["frame_out_exclusive"] * SAMPLES_PER_FRAME
        graph += [
            f"anullsrc=r={SAMPLE_RATE}:cl=stereo,atrim=end_sample={CARD_FRAMES * SAMPLES_PER_FRAME}[gap{index}]",
            f"[audio{index}]atrim=start_sample={start}:end_sample={end},asetpts=PTS-STARTPTS[clipa{index}]",
        ]
        audio_parts.append(f"[gap{index}][clipa{index}]")
    graph.append(f'{"".join(audio_parts)}concat=n={len(titles) * 2}:v=0:a=1[outa]')
    args += ["-filter_complex", ";".join(graph), "-map", "[outv]", "-map", "[outa]",
             "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-profile:v", "high",
             "-r", str(FPS), "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_trc", "bt709",
             "-color_primaries", "bt709", "-color_range", "tv", "-c:a", "aac", "-b:a", "256k",
             "-ar", str(SAMPLE_RATE), "-ac", "2", "-movflags", "+faststart", str(OUTPUT)]
    composition = {**previous["composition"], "title_y": HEIGHT // 2, "title_visibility": "title cards only"}
    audio = {**previous["audio"], "mode": "insert silent cards and encode AAC"}
    audio.pop("stream_sha256", None)
    contract = {**previous, "revision": "v07", "output": str(OUTPUT), "segments": segments,
                "frames": total_frames, "duration": total_frames / FPS, "rank_reveals": reveals,
                "transitions": titles, "caption_cues": cues, "composition": composition, "audio": audio}
    (EDIT / "export-contract-v07.json").write_text(json.dumps(contract, indent=2, ensure_ascii=False) + "\n")
    (EDIT / "render-command-v07.json").write_text(json.dumps(args, indent=2) + "\n")
    subprocess.run(args, check=True)


if __name__ == "__main__":
    with TemporaryDirectory(prefix="scenes-meme-v07-") as scratch:
        run(Path(scratch))
