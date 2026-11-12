"""Render the 2026 pilot with sample-aligned J-cuts and two title turns."""
import json
import math
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from PIL import Image, ImageChops, ImageFilter

from render_meme_2026_v11 import BG, EFFECT, FFMPEG, FPS, SAMPLE_RATE, SAMPLES_PER_FRAME, overlay_image
from render_ranked_v06 import EDIT, EPISODE, HEIGHT, WIDTH, digest
from render_ranked_v09 import CENTER, OVERSAMPLE, START_SCALE, TITLE_HEIGHT, TITLE_TOP, title_layer, write_json
from render_ranked_v10 import START_BLUR

OUTPUT = EPISODE / "Deliverables" / "meme-time-machine-2026_pilot-v12.mp4"
OVERLAP_SAMPLES = SAMPLE_RATE // 10
HOLD_FRAMES = FPS // 4
FADE_FRAMES = 6
TURN_DEGREES = 720


def effect_length():
    pcm = subprocess.check_output([*FFMPEG, "-i", str(EFFECT), "-ar", str(SAMPLE_RATE),
                                   "-ac", "2", "-f", "f32le", "-"])
    return len(pcm) // 8


def title_frames(name, slate, folder, frame_count):
    base = Image.open(slate).convert("RGBA")
    layer, (source_x, source_y) = title_layer(name)
    center_x, center_y = CENTER[0], CENTER[1] - TITLE_TOP
    landing = frame_count - HOLD_FRAMES - FADE_FRAMES
    fade_start = landing + HOLD_FRAMES
    mask = Image.new("L", (1, TITLE_HEIGHT))
    mask.putdata([round(255 * min(y / 40, (TITLE_HEIGHT - 1 - y) / 40, 1))
                  for y in range(TITLE_HEIGHT)])
    mask = mask.resize((WIDTH, TITLE_HEIGHT))
    sharp = None
    for frame in range(frame_count):
        target = folder / f"{frame:02d}.png"
        if landing < frame < fade_start:
            os.link(folder / f"{landing:02d}.png", target)
            continue
        if frame <= landing:
            # A short acceleration lets the lettering move on the first frame.
            progress = frame / landing
            remaining = (1 + math.cos(math.pi * progress)) / 2
            angle = math.radians(-TURN_DEGREES * remaining)
            scale = 1 + (START_SCALE - 1) * remaining ** 2
            blur = START_BLUR * remaining ** 1.5
            cosine = math.cos(angle) * OVERSAMPLE / scale
            sine = math.sin(angle) * OVERSAMPLE / scale
            inverse = (
                cosine, sine, source_x - cosine * center_x - sine * center_y,
                -sine, cosine, source_y + sine * center_x - cosine * center_y,
            )
            lettering = layer.transform((WIDTH, TITLE_HEIGHT), Image.Transform.AFFINE, inverse,
                                        resample=Image.Resampling.BICUBIC)
            if blur > 0.05:
                lettering = lettering.convert("RGBa").filter(ImageFilter.GaussianBlur(blur)).convert("RGBA")
            lettering.putalpha(ImageChops.multiply(lettering.getchannel("A"), mask))
            if frame == landing:
                sharp = lettering
        else:
            opacity = (frame_count - 1 - frame) / FADE_FRAMES
            lettering = sharp.copy()
            lettering.putalpha(lettering.getchannel("A").point(lambda alpha: round(alpha * opacity)))
        picture = base.copy()
        picture.alpha_composite(lettering, (0, TITLE_TOP))
        picture.convert("RGB").save(target, compress_level=1)
    return landing


def render(directory):
    if OUTPUT.exists():
        raise FileExistsError(OUTPUT)
    clips = json.loads((EDIT / "selection-2026-v11.json").read_text())["clips"]
    assert sorted(clip["rank"] for clip in clips) == [1, 2, 3, 4, 5]
    fx_samples = effect_length()
    args = [*FFMPEG, "-filter_complex_threads", "3", "-i", str(EFFECT)]
    effect_taps = "".join(f"[fx{i}]" for i in range(len(clips)))
    graph = [f"[0:a]aresample={SAMPLE_RATE},aformat=channel_layouts=stereo,"
             f"asetpts=PTS-STARTPTS,asplit={len(clips)}{effect_taps}"]
    video_parts, audio_parts, records, extracts = [], [], [], []
    revealed = {}
    frame = 0
    old_overlay = directory / "rank-before.png"
    overlay_image(old_overlay, revealed, None)
    for i, clip in enumerate(clips):
        source = EPISODE / clip["source"]
        clip_frames = clip["frames"]
        source_in = 1 + 3 * i
        crop = f"crop={clip['crop']}," if clip.get("crop") else ""
        pre_roll = OVERLAP_SAMPLES if i else 0
        card_frames = round((fx_samples - pre_roll - OVERLAP_SAMPLES) / SAMPLES_PER_FRAME)
        effect_start = frame * SAMPLES_PER_FRAME - pre_roll
        effect_end = effect_start + fx_samples
        audio_start = effect_end - OVERLAP_SAMPLES
        clip_end = frame + card_frames + clip_frames
        audio_samples = clip_end * SAMPLES_PER_FRAME - audio_start

        slate = directory / f"slate-{i}.png"
        extract = [*FFMPEG, "-ss", str(clip["start"]), "-i", str(source), "-i", str(old_overlay),
                   "-filter_complex", f"[0:v]{crop}{BG},eq=brightness=-0.12[bg];[bg][1:v]overlay",
                   "-frames:v", "1", "-update", "1", str(slate)]
        extracts.append(extract)
        subprocess.run(extract, check=True)
        sequence = directory / f"title-{i}"
        sequence.mkdir()
        landing = title_frames(clip["name"], slate, sequence, card_frames)
        revealed[clip["rank"]] = clip["name"]
        current_overlay = directory / f"rank-{i}.png"
        overlay_image(current_overlay, revealed, clip["rank"])
        old_overlay = current_overlay

        args += ["-ss", str(clip["start"]), "-t", f"{clip_frames / FPS + 0.10:.6f}", "-i", str(source),
                 "-framerate", str(FPS), "-start_number", "0", "-i", str(sequence / "%02d.png"),
                 "-i", str(current_overlay)]
        graph += [
            f"[{source_in}:v]{crop}fps={FPS},tpad=stop_mode=clone:stop=3,trim=end_frame={clip_frames},"
            f"settb=1/{FPS},setpts=N,split=2[copy{i}][front{i}]",
            f"[copy{i}]{BG}[bg{i}]",
            f"[front{i}]scale=1080:1000:force_original_aspect_ratio=decrease:force_divisible_by=2:"
            f"flags=lanczos,setsar=1[fg{i}]",
            f"[bg{i}][fg{i}]overlay=(W-w)/2:865-h/2:shortest=1[main{i}]",
            f"[main{i}][{source_in + 2}:v]overlay=eof_action=repeat:format=yuv420[clipv{i}]",
            f"[{source_in + 1}:v]scale=out_color_matrix=bt709:out_range=tv,"
            f"format=yuv420p,setsar=1,settb=1/{FPS},setpts=N[title{i}]",
            f"[fx{i}]adelay={effect_start}S:all=1[jet{i}]",
            f"[{source_in}:a]aresample={SAMPLE_RATE},aformat=channel_layouts=stereo,"
            f"apad=whole_len={audio_samples},atrim=end_sample={audio_samples},asetpts=PTS-STARTPTS,"
            f"volume={clip['gain_db']}dB,afade=t=in:ss=0:ns=192,"
            f"afade=t=out:ss={audio_samples - 1680}:ns=1680,"
            f"alimiter=limit=0.84:level=false:latency=true,adelay={audio_start}S:all=1[clipa{i}]",
        ]
        video_parts.append(f"[title{i}][clipv{i}]")
        audio_parts.append(f"[jet{i}][clipa{i}]")
        records.append({**clip, "sha256": digest(source), "title_in_frame": frame,
                        "title_hold_start_frame": frame + landing,
                        "title_dissolve_start_frame": frame + landing + HOLD_FRAMES,
                        "clip_in_frame": frame + card_frames, "clip_out_frame_exclusive": clip_end,
                        "effect_start_sample": effect_start, "effect_end_sample_exclusive": effect_end,
                        "clip_audio_start_sample": audio_start,
                        "clip_audio_end_sample_exclusive": clip_end * SAMPLES_PER_FRAME})
        frame = clip_end

    graph += [
        f'{"".join(video_parts)}concat=n={len(video_parts) * 2}:v=1:a=0,settb=1/{FPS},setpts=N[outv]',
        f'{"".join(audio_parts)}amix=inputs={len(audio_parts) * 2}:normalize=0:duration=longest,'
        f'atrim=end_sample={frame * SAMPLES_PER_FRAME}[outa]',
    ]
    args += [
        "-filter_complex", ";".join(graph), "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-profile:v", "high",
        "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_trc", "bt709",
        "-color_primaries", "bt709", "-color_range", "tv",
        "-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
        "-c:a", "aac", "-b:a", "256k", "-ar", str(SAMPLE_RATE), "-ac", "2",
        "-movflags", "+faststart", str(OUTPUT),
    ]
    write_json(EDIT / "export-contract-v12.json", {
        "revision": "v12", "purpose": "local pilot", "trend_year": 2026,
        "width": WIDTH, "height": HEIGHT, "fps": FPS, "frames": frame, "duration": frame / FPS,
        "output": str(OUTPUT), "clips": records,
        "animation": {"clockwise_turns": 2, "hold_frames": HOLD_FRAMES, "dissolve_frames": FADE_FRAMES,
                      "start_scale": START_SCALE, "gaussian_radius_from_px": START_BLUR,
                      "gaussian_radius_to_px": 0},
        "audio": {"codec": "AAC-LC", "sample_rate": SAMPLE_RATE, "channels": 2,
                  "effect": str(EFFECT.relative_to(EPISODE)), "effect_sha256": digest(EFFECT),
                  "effect_samples": fx_samples, "overlap_samples": OVERLAP_SAMPLES,
                  "effect_processing": "original decoded extent and speed, sample rate conversion only",
                  "first_card_effect_starts_at_zero": True},
        "loop": {"spoken": False, "reason": "The last animal moment completes the ranking."},
    })
    write_json(EDIT / "render-command-v12.json", {"extract_slates": extracts, "render": args})
    subprocess.run(args, check=True)


if __name__ == "__main__":
    with TemporaryDirectory(prefix="scenes-2026-v12-render-") as scratch:
        render(Path(scratch))
