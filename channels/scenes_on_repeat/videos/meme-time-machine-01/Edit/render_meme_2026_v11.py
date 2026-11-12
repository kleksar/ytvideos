"""Build the 2026-only review cut from the selected clips and animated titles."""
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw

from render_ranked_v06 import CREAM, EDIT, EPISODE, GOLD, HEIGHT, ROW_STEP, ROW_TOP, SHADOW, WIDTH, digest, font
from render_ranked_v10 import FPS, LANDING_FRAME, START_BLUR, START_SCALE, title_frames, write_json

FFMPEG = ["ffmpeg", "-nostdin", "-hide_banner", "-v", "error", "-n"]
OUTPUT = EPISODE / "Deliverables" / "meme-time-machine-2026_pilot-v11.mp4"
CARD_FRAMES = LANDING_FRAME + 1
SAMPLE_RATE = 48000
SAMPLES_PER_FRAME = SAMPLE_RATE // FPS
EFFECT = EPISODE / "Source" / "jet-set-radio-spray-fully.mp3"
EFFECT_FILTER = (
    f"aresample={SAMPLE_RATE},atrim=start_sample=3360:end_sample=54240,asetpts=PTS-STARTPTS,"
    "atempo=1.8,apad=whole_len=29000,atrim=end_sample=29000,"
    "afade=t=in:ss=0:ns=192,afade=t=out:ss=27080:ns=1920,volume=-2dB"
)
BG = (
    "scale=270:480:flags=bilinear,setsar=1,gblur=sigma=17:steps=3,"
    "eq=contrast=0.91:brightness=-0.14:saturation=0.90,scale=1080:1920:flags=bilinear"
)


def overlay_image(path, revealed, active):
    image = Image.new("RGBA", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.text((540, 170), "2026 MEMES", anchor="mm", font=font(48), fill=CREAM,
              stroke_width=2, stroke_fill=SHADOW)
    for rank in range(1, 6):
        y = ROW_TOP + (rank - 1) * ROW_STEP
        ink = GOLD if rank == active else CREAM
        draw.text((107, y), str(rank), anchor="mm", font=font(49), fill=ink,
                  stroke_width=1, stroke_fill=SHADOW)
        if rank in revealed:
            draw.text((149, y), revealed[rank], anchor="lm", font=font(50), fill=ink,
                      stroke_width=1, stroke_fill=SHADOW)
    image.save(path)


def make_card(clip, index, source, prior_overlay, directory):
    still = directory / f"slate-{index}.png"
    crop = f"crop={clip['crop']}," if clip.get("crop") else ""
    extract = [*FFMPEG, "-ss", str(clip["start"]), "-i", str(source), "-i", str(prior_overlay),
               "-filter_complex", f"[0:v]{crop}{BG},eq=brightness=-0.12[bg];[bg][1:v]overlay",
               "-frames:v", "1", "-update", "1", str(still)]
    subprocess.run(extract, check=True)
    sequence = directory / f"title-{index}"
    sequence.mkdir()
    # The shared animator lands at frame 28. The trim below includes that frame and cuts next.
    title_frames({"text": clip["name"], "frame_in": 0, "frame_out_exclusive": 15}, still, sequence)
    return sequence / "%02d.png", extract


def render(directory):
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    plan = json.loads((EDIT / "selection-2026-v11.json").read_text())
    clips = plan["clips"]
    assert sorted(clip["rank"] for clip in clips) == [1, 2, 3, 4, 5]
    assert CARD_FRAMES * SAMPLES_PER_FRAME == 29000

    args = [*FFMPEG, "-filter_complex_threads", "3", "-i", str(EFFECT)]
    title_audio = "".join(f"[jet{i}]" for i in range(len(clips)))
    graph = [f"[0:a]{EFFECT_FILTER},asplit={len(clips)}{title_audio}"]
    parts, records, extracts = [], [], []
    revealed = {}
    frame = 0
    old_overlay = directory / "rank-before.png"
    overlay_image(old_overlay, revealed, None)
    for i, clip in enumerate(clips):
        source = EPISODE / clip["source"]
        clip_frames = clip["frames"]
        samples = clip_frames * SAMPLES_PER_FRAME
        source_in = 1 + 3 * i
        duration = clip_frames / FPS
        revealed[clip["rank"]] = clip["name"]
        current_overlay = directory / f"rank-{i}.png"
        overlay_image(current_overlay, revealed, clip["rank"])
        title, extract = make_card(clip, i, source, old_overlay, directory)
        extracts.append(extract)
        old_overlay = current_overlay

        args += ["-ss", str(clip["start"]), "-t", f"{duration + 0.10:.6f}", "-i", str(source),
                 "-framerate", str(FPS), "-start_number", "0", "-i", str(title),
                 "-i", str(current_overlay)]
        crop = f"crop={clip['crop']}," if clip.get("crop") else ""
        graph += [
            f"[{source_in}:v]{crop}fps={FPS},tpad=stop_mode=clone:stop=3,trim=end_frame={clip_frames},"
            f"settb=1/{FPS},setpts=N,split=2[copy{i}][front{i}]",
            f"[copy{i}]{BG}[bg{i}]",
            f"[front{i}]scale=1080:1000:force_original_aspect_ratio=decrease:force_divisible_by=2:"
            f"flags=lanczos,setsar=1[fg{i}]",
            f"[bg{i}][fg{i}]overlay=(W-w)/2:865-h/2:shortest=1[main{i}]",
            f"[main{i}][{source_in + 2}:v]overlay=eof_action=repeat:format=yuv420[clipv{i}]",
            f"[{source_in + 1}:v]trim=end_frame={CARD_FRAMES},scale=out_color_matrix=bt709:out_range=tv,"
            f"format=yuv420p,setsar=1,settb=1/{FPS},setpts=N[title{i}]",
            f"[{source_in}:a]aresample={SAMPLE_RATE},aformat=channel_layouts=stereo,"
            f"apad=whole_len={samples},atrim=end_sample={samples},asetpts=PTS-STARTPTS,"
            f"volume={clip['gain_db']}dB,afade=t=in:ss=0:ns=192,"
            f"afade=t=out:ss={samples - 1680}:ns=1680,"
            f"alimiter=limit=0.84:level=false:latency=true[clipa{i}]",
        ]
        parts.append(f"[title{i}][jet{i}][clipv{i}][clipa{i}]")
        records.append({**clip, "sha256": digest(source), "title_in_frame": frame,
                        "clip_in_frame": frame + CARD_FRAMES,
                        "clip_out_frame_exclusive": frame + CARD_FRAMES + clip_frames})
        frame += CARD_FRAMES + clip_frames

    graph.append(f'{"".join(parts)}concat=n={len(parts) * 2}:v=1:a=1[catv][outa]')
    graph.append(f"[catv]settb=1/{FPS},setpts=N[outv]")
    args += [
        "-filter_complex", ";".join(graph), "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-profile:v", "high",
        "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_trc", "bt709",
        "-color_primaries", "bt709", "-color_range", "tv",
        "-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
        "-c:a", "aac", "-b:a", "256k", "-ar", str(SAMPLE_RATE), "-ac", "2",
        "-movflags", "+faststart", str(OUTPUT),
    ]
    write_json(EDIT / "export-contract-v11.json", {
        "revision": "v11", "purpose": "local pilot", "trend_year": 2026,
        "width": WIDTH, "height": HEIGHT, "fps": FPS, "frames": frame, "duration": frame / FPS,
        "output": str(OUTPUT), "clips": records,
        "animation": {"start_frame": 0, "landing_frame": LANDING_FRAME, "frames": CARD_FRAMES,
                      "clockwise_turns": 1, "start_scale": START_SCALE,
                      "gaussian_radius_from_px": START_BLUR, "gaussian_radius_to_px": 0,
                      "timing": "animated from entry, cut on next frame after settling"},
        "audio": {"codec": "AAC-LC", "sample_rate": SAMPLE_RATE, "channels": 2,
                  "effect": str(EFFECT.relative_to(EPISODE)), "effect_sha256": digest(EFFECT),
                  "effect_filters": EFFECT_FILTER},
        "loop": {"spoken": False, "reason": "The final animal moment completes the ranking; the next sweep restarts it."},
    })
    write_json(EDIT / "render-command-v11.json", {"extract_slates": extracts, "render": args})
    subprocess.run(args, check=True)


if __name__ == "__main__":
    with TemporaryDirectory(prefix="scenes-2026-render-") as scratch:
        render(Path(scratch))
