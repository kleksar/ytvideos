#!/usr/bin/env python3
"""Render and collect exact-file QA evidence for one film-short edit plan."""
import argparse
import hashlib
import io
import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 24
HOOK_SECONDS = 5
END_CARD_SECONDS = 5
WIDTH = 1080
HEIGHT = 1920
PANEL_HEIGHT = HEIGHT // 3
CAPTION_TOP = 2 * PANEL_HEIGHT - 40
AUDIO_RATE = 48000
FADE_MS = 75
FADE_SAMPLES = AUDIO_RATE * FADE_MS // 1000
SAMPLES_PER_FRAME = AUDIO_RATE // FPS
CONTIGUOUS_EPSILON = 0.00001
CHANNEL = Path(__file__).resolve().parents[2]
ROOT = CHANNEL.parents[1]
POSTER_TOOL = CHANNEL / "automation/add_film_poster.py"
SRT_TOOL = ROOT / ".agents/skills/ytv-srt/scripts/srt_tool.py"
DEFAULT_CTA = CHANNEL / "brand/shorts-cta.png"
CTA_BOX = (190, 1398, 830, 1530)
CTA_PERIOD_SECONDS = 6
CTA_TILT_DEGREES = 1.5
CTA_SCALE_SWING = 0.035
TIMER_HEIGHT = 52
TIMER_Y = HEIGHT - TIMER_HEIGHT - 2
TIMER_MARGIN = 48
BRAND_ACCENT = "#F8B242"
BRAND_TEXT = "#F9EED6"
BRAND_FONT = Path("/System/Library/Fonts/Avenir Next.ttc")
BRAND_WEIGHTS = {"bold": 0, "demi": 2, "medium": 5}
FONT_PATHS = (
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
)
FFMPEG = ["ffmpeg", "-nostdin", "-hide_banner", "-v", "error", "-xerror"]


def run(args, **kwargs):
    return subprocess.run([str(arg) for arg in args], check=True, **kwargs)


def probe(path):
    result = run(["ffprobe", "-v", "error", "-show_streams", "-show_format",
                  "-of", "json", path], capture_output=True)
    return json.loads(result.stdout)


def seconds(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


def even(value):
    return round(value / 2) * 2


def make_edit(plan, video, duration):
    coded_width = int(video["width"])
    coded_height = int(video["height"])
    active_crop = plan.get("active_crop", [0, 0, coded_width, coded_height])
    if (not isinstance(active_crop, list) or len(active_crop) != 4
            or any(type(value) is not int or value % 2 for value in active_crop)):
        raise ValueError("active_crop must be four even integers: x, y, width, height")
    x, y, source_width, source_height = active_crop
    if (min(x, y) < 0 or min(source_width, source_height) < 2
            or x + source_width > coded_width or y + source_height > coded_height):
        raise ValueError("active_crop must be within the coded frame")
    if video.get("sample_aspect_ratio") not in {None, "1:1", "0:1", "N/A"}:
        numerator, denominator = map(int, video["sample_aspect_ratio"].split(":"))
        source_width = even(source_width * numerator / denominator)
    if source_height % 2 or source_width % 2:
        raise ValueError("the square-pixel source dimensions must be even")

    scale = max(WIDTH / source_width, PANEL_HEIGHT / source_height)
    picture_width = even(source_width * scale)
    picture_height = even(source_height * scale)
    if min(picture_width, picture_height) < 2:
        raise ValueError("source aspect ratio cannot fit the middle panel")
    crop_y = even((picture_height - PANEL_HEIGHT) / 2)

    shots, runs = [], []
    cursor = 0
    for number, entry in enumerate(plan["shots"], 1):
        start = seconds(entry["in"], f"shot {number} in")
        end = seconds(entry["out"], f"shot {number} out")
        if end <= start or end > duration + CONTIGUOUS_EPSILON:
            raise ValueError(f"shot {number} source range is outside the movie or empty")
        if not runs or abs(start - runs[-1]["out"]) > CONTIGUOUS_EPSILON:
            runs.append({"in": start, "out": end, "start_frame": cursor})
        audio_run = runs[-1]
        end_frame = audio_run["start_frame"] + round((end - audio_run["in"]) * FPS)
        if end_frame <= cursor:
            raise ValueError(f"shot {number} must retain at least one frame")
        audio_run.update(out=end, end_frame=end_frame)
        focus = entry.get("focus_x", 0.5)
        if isinstance(focus, list):
            if len(focus) != 3 or any(seconds(point, "focus_x") > 1 for point in focus):
                raise ValueError("focus_x samples must be three positions from 0 to 1")
            focus = focus[1]
        if seconds(focus, "focus_x") > 1:
            raise ValueError("focus_x must be from 0 to 1")
        crop_x = even(max(0, min(picture_width - WIDTH, focus * picture_width - WIDTH / 2)))
        shots.append({
            "number": number, "in": start, "out": end, "start_frame": cursor, "end_frame": end_frame,
            "crop_x": crop_x, "crop_y": crop_y,
            "picture_width": picture_width, "picture_height": picture_height,
        })
        cursor = end_frame
    if cursor < END_CARD_SECONDS * FPS:
        raise ValueError(f"the Short must be at least {END_CARD_SECONDS} seconds to fit the film card")

    for audio_run in runs:
        length = audio_run["end_frame"] - audio_run["start_frame"]
        if length * SAMPLES_PER_FRAME < 2 * FADE_SAMPLES:
            raise ValueError("a retained audio range is too short for both 75 ms fades")
    return shots, runs, (source_width, source_height, active_crop)


def conform_cues(entries, runs):
    cues = []
    for entry in entries:
        start = seconds(entry["start"], "cue start")
        end = seconds(entry["end"], "cue end")
        text = entry["text"].strip()
        if end <= start or not text:
            raise ValueError("a subtitle has an empty interval or empty text")
        for audio_run in runs:
            if end <= audio_run["in"] or start >= audio_run["out"]:
                continue
            fade = FADE_MS / 1000
            if (start < audio_run["in"] + fade - CONTIGUOUS_EPSILON
                    or end > audio_run["out"] - fade + CONTIGUOUS_EPSILON):
                raise ValueError(
                    f"speech at {start:.3f}–{end:.3f} enters a cut or its 75 ms fade "
                    f"({audio_run['in']:.3f}–{audio_run['out']:.3f}): {text}"
                )
            offset = audio_run["start_frame"]
            start_frame = offset + round((start - audio_run["in"]) * FPS)
            end_frame = offset + round((end - audio_run["in"]) * FPS)
            if end_frame <= start_frame:
                raise ValueError(f"subtitle at {start:.3f} is shorter than one frame")
            cues.append({"start_frame": start_frame, "end_frame": end_frame, "text": text,
                         "source_start": start, "source_end": end})

    cues.sort(key=lambda cue: cue["start_frame"])
    for first, second in zip(cues, cues[1:]):
        if first["end_frame"] > second["start_frame"]:
            raise ValueError(f"subtitle timings overlap at output frame {second['start_frame']}")
    return cues


def get_font(size, weight="demi"):
    if BRAND_FONT.is_file():
        return ImageFont.truetype(str(BRAND_FONT), size, index=BRAND_WEIGHTS[weight])
    for path in FONT_PATHS:
        if path.is_file():
            return ImageFont.truetype(str(path), size)
    raise ValueError("Arial Bold or DejaVu Sans Bold is required for Cyrillic overlays")


def make_overlay(path, text, hook=False):
    canvas = Image.new("RGBA", (WIDTH, PANEL_HEIGHT if hook else 222))
    draw = ImageDraw.Draw(canvas)
    max_width = 920 if hook else 790
    center_x = WIDTH // 2 if hook else 510
    max_lines = 3 if hook else 1
    for size in (range(86, 39, -2) if hook else (66,)):
        font = get_font(size, "bold")
        lines = []
        for paragraph in text.splitlines():
            line = ""
            for word in paragraph.split():
                candidate = f"{line} {word}" if line else word
                if line and draw.textlength(candidate, font=font) > max_width:
                    lines.append(line)
                    line = word
                else:
                    line = candidate
            if line:
                lines.append(line)
        if lines and len(lines) <= max_lines and all(
            draw.textlength(line, font=font) <= max_width for line in lines
        ):
            break
    else:
        raise ValueError(f"text does not fit its overlay: {text}")
    line_height = size + 12
    top = (canvas.height - (len(lines) - 1) * line_height) // 2
    for index, line in enumerate(lines):
        accent = hook and index == len(lines) - 1 and len(lines) > 1
        draw.text((center_x, top + index * line_height), line, font=font, anchor="mm",
                  fill=BRAND_ACCENT if accent else BRAND_TEXT, stroke_width=4 if hook else 3,
                  stroke_fill="#11151b")
    canvas.save(path)


def prepare_cta(source, output):
    data = source.read_bytes()
    with Image.open(io.BytesIO(data)) as image:
        if image.format != "PNG":
            raise ValueError(f"CTA artwork must be a transparent PNG: {source}")
        image_size = image.size
        rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    bounds = alpha.point(lambda value: 255 if value > 12 else 0).getbbox()
    if not bounds or alpha.getextrema()[0] == 255:
        raise ValueError(f"CTA artwork must contain visible pixels and transparency: {source}")

    x1, y1, x2, y2 = bounds
    crop = (max(0, x1 - 6), max(0, y1 - 6),
            min(rgba.width, x2 + 6), min(rgba.height, y2 + 6))
    left, top, right, bottom = CTA_BOX
    art = rgba.crop(crop)
    scale = min((right - left) / art.width, (bottom - top) / art.height)
    width, height = max(2, even(art.width * scale)), max(2, even(art.height * scale))
    if source.name == DEFAULT_CTA.name:
        # Reposition the two generated text lines as one block, inside the ticket border.
        art.resize((464, 96), Image.Resampling.LANCZOS).save(output)
        positioned = output.with_name("cta-positioned.png")
        run([*FFMPEG, "-n", "-i", output, "-filter_complex",
             "[0:v]format=rgba,split[base][panel];[panel]crop=308:64:104:14[text];"
             "[base][text]overlay=104:18:format=rgb", "-frames:v", "1", "-pix_fmt", "rgba", positioned])
        with Image.open(positioned) as corrected:
            art = corrected.copy()
        positioned.unlink()
    art.resize((width, height), Image.Resampling.LANCZOS).save(output)
    x, y = even((left + right - width) / 2), even((top + bottom - height) / 2)
    return {
        "path": str(source), "sha256": hashlib.sha256(data).hexdigest(),
        "source_size": image_size, "source_crop_bbox": crop,
        "delivery_bbox": [x, y, x + width, y + height],
    }


def prepare_cta_motion(source, work):
    """Make one seamless alpha cycle around the ticket's raised center."""
    still = work / "cta.png"
    record = prepare_cta(source, still)
    with Image.open(still) as image:
        art = image.convert("RGBA")
    width, height = art.width + 60, art.height + 52
    left, top, _, _ = record["delivery_bbox"]
    position = [left - 30, top - 26]
    period_frames = CTA_PERIOD_SECONDS * FPS
    animation = work / "cta-motion.mov"
    args = [*FFMPEG, "-n", "-f", "rawvideo", "-pix_fmt", "rgba", "-video_size",
            f"{width}x{height}", "-framerate", str(FPS), "-i", "pipe:0", "-an",
            "-c:v", "qtrle", "-pix_fmt", "argb", str(animation)]
    with subprocess.Popen(args, stdin=subprocess.PIPE) as encoder:
        for frame in range(period_frames):
            phase = math.tau * frame / period_frames
            scale = 1 + CTA_SCALE_SWING * math.sin(phase + math.pi / 2)
            angle = math.radians(CTA_TILT_DEGREES * math.sin(phase))
            a, b = math.cos(angle) / scale, math.sin(angle) / scale
            cx, cy = width / 2, height / 2
            # Transform at double resolution to keep the border and type stable.
            transform = (a / 2, b / 2, art.width / 2 - a * cx - b * cy,
                         -b / 2, a / 2, art.height / 2 + b * cx - a * cy)
            image = art.transform((2 * width, 2 * height), Image.Transform.AFFINE,
                                  transform, Image.Resampling.BICUBIC)
            image = image.resize((width, height), Image.Resampling.LANCZOS)
            encoder.stdin.write(image.tobytes())
        encoder.stdin.close()
        if encoder.wait() != 0:
            raise subprocess.CalledProcessError(encoder.returncode, args)
    record.update(overlay_position=position, period_frames=period_frames,
                  tilt_degrees=CTA_TILT_DEGREES, scale_swing=CTA_SCALE_SWING)
    return animation, record


def hook_end_frame(frames):
    return min(HOOK_SECONDS * FPS, frames - END_CARD_SECONDS * FPS)


def prepare_hook_animation(text, work, end_frame):
    still = work / "hook.png"
    animation = work / "hook-animation.mov"
    make_overlay(still, text, hook=True)
    fade_frames = FPS // 2
    fade_out = end_frame - fade_frames - 1
    run([*FFMPEG, "-n", "-loop", "1", "-framerate", str(FPS), "-i", still,
         "-vf", f"format=rgba,fade=t=in:s=0:n={fade_frames}:alpha=1,"
                f"fade=t=out:s={fade_out}:n={fade_frames}:alpha=1",
         "-frames:v", str(end_frame), "-c:v", "qtrle", animation])
    return animation


def hook_overlay_y(time, end_frame):
    fade_out = (end_frame - FPS // 2 - 1) / FPS
    entrance = f"max(0\\,min(1\\,1-{time}/0.5))"
    exit = f"max(0\\,min(1\\,({time}-{fade_out:.9f})/0.5))"
    return f"40*pow({entrance}\\,3)-40*pow({exit}\\,3)"


def live_picture_layers(picture):
    return [
        f"[{picture}]split=2[foreground][background]",
        "[background]scale=144:256:force_original_aspect_ratio=increase:force_divisible_by=2,"
        "crop=144:256:(iw-ow)/2:(ih-oh)/2,setsar=1,gblur=sigma=18,"
        "eq=brightness=-0.18:saturation=0.76,scale=1080:1920,setsar=1[matte]",
        f"[matte][foreground]overlay=0:{PANEL_HEIGHT}[picture]",
    ]


def render_shot(source, stream, dimensions, shot, overlays, work):
    start_frame, end_frame = shot["start_frame"], shot["end_frame"]
    frames = end_frame - start_frame
    source_width, source_height, (crop_left, crop_top, crop_width, crop_height) = dimensions
    seek = max(0, shot["in"] - 0.08)
    trim_in = max(0, shot["in"] - seek - 0.0005)
    trim_out = shot["out"] - seek - 0.0005
    args = [*FFMPEG, "-n", "-threads", "2", "-ss", f"{seek:.9f}", "-i", source]
    graph = [
        f"[0:{stream}]trim=start={trim_in:.9f}:end={trim_out:.9f},"
        f"crop={crop_width}:{crop_height}:{crop_left}:{crop_top},"
        f"scale={source_width}:{source_height},setsar=1,"
        f"setpts=PTS-STARTPTS,fps={FPS},tpad=stop=2:stop_mode=clone,"
        f"scale={shot['picture_width']}:{shot['picture_height']},setsar=1,"
        f"crop={WIDTH}:{PANEL_HEIGHT}:{shot['crop_x']}:{shot['crop_y']}[pic]",
        *live_picture_layers("pic"),
    ]
    last_label = "picture"
    input_index = 1
    for first, last, x, y, path in overlays:
        local_first = max(0, first - start_frame)
        local_last = min(frames, last - start_frame)
        if local_first >= local_last:
            continue
        is_hook = path.name == "hook-animation.mov"
        if is_hook:
            args.extend(["-ss", f"{start_frame / FPS:.9f}"])
        args.extend(["-i", path])
        label = f"layer{input_index}"
        position = str(x).format(start_frame=start_frame)
        y_position = str(y)
        global_time = f"(t+{start_frame / FPS:.9f})"
        if is_hook:
            y_position = hook_overlay_y(global_time, last)
        enable = ("" if local_first == 0 and local_last == frames
                  else f":enable='between(n,{local_first},{local_last - 1})'")
        graph.append(f"[{last_label}][{input_index}:v]overlay=x='{position}':y='{y_position}'"
                     f"{enable}[{label}]")
        last_label = label
        input_index += 1
    graph.append(f"[{last_label}]format=yuv420p[v]")
    output = work / f"shot-{shot['number']:03d}.mp4"
    run([*args, "-filter_complex_threads", "2", "-filter_complex", ";".join(graph),
         "-map", "[v]", "-an", "-frames:v", frames, "-fps_mode", "passthrough",
         "-c:v", "libx264", "-preset", "ultrafast", "-crf", "13", "-threads", "2",
         "-video_track_timescale", "24000", output])
    actual = int(probe(output)["streams"][0]["nb_frames"])
    if actual != frames:
        raise ValueError(f"shot {shot['number']} returned {actual} frames, expected {frames}")
    return output


def read_pcm(source, stream, start=None, length=None):
    args = [*FFMPEG]
    if start is not None:
        args.extend(["-ss", f"{start:.9f}"])
    args.extend(["-i", source, "-map", f"0:{stream}", "-vn", "-ac", "2", "-ar", AUDIO_RATE])
    if length is not None:
        args.extend(["-t", f"{length:.9f}"])
    args.extend(["-f", "f32le", "pipe:1"])
    return np.frombuffer(run(args, capture_output=True).stdout, dtype="<f4").reshape(-1, 2)


def prepare_audio(source, stream, runs, work):
    before_fades = []
    fade_in = np.linspace(0, 1, FADE_SAMPLES, dtype=np.float32)[:, None]
    destination = work / "audio.f32le"
    with destination.open("wb") as handle:
        for audio_run in runs:
            n = (audio_run["end_frame"] - audio_run["start_frame"]) * SAMPLES_PER_FRAME
            raw = read_pcm(source, stream, audio_run["in"], audio_run["out"] - audio_run["in"])
            if len(raw) < n - SAMPLES_PER_FRAME:
                raise ValueError(f"source audio is shorter than the edit near {audio_run['out']:.3f}")
            exact = np.zeros((n, 2), dtype="<f4")
            exact[:min(n, len(raw))] = raw[:n]
            before_fades.append(exact.copy())
            exact[:FADE_SAMPLES] *= fade_in
            exact[-FADE_SAMPLES:] *= fade_in[::-1]
            handle.write(exact.tobytes())
    return destination, np.concatenate(before_fades)


def make_film_details(path, details):
    canvas = Image.new("RGBA", (WIDTH, PANEL_HEIGHT))
    draw = ImageDraw.Draw(canvas)
    left, text_width = 480, 560
    title = details["title"]
    for size in range(76, 43, -2):
        font = get_font(size, "bold")
        lines = []
        for word in title.split():
            candidate = f"{lines[-1]} {word}" if lines else word
            if lines and draw.textlength(candidate, font=font) <= text_width:
                lines[-1] = candidate
            else:
                lines.append(word)
        if 1 <= len(lines) <= 3 and all(draw.textlength(line, font=font) <= text_width for line in lines):
            break
    else:
        raise ValueError("film title does not fit the end card")

    metadata = "  ·  ".join(details[key] for key in ("year", "genre", "runtime") if details.get(key))
    cast = details.get("cast", "")
    y = (PANEL_HEIGHT - (len(lines) * (size + 3) + 120)) // 2
    for line in lines:
        draw.text((left, y), line, font=font, anchor="lt", fill=BRAND_TEXT,
                  stroke_width=3, stroke_fill="#11151b")
        y += size + 3
    draw.rectangle((left, y + 3, left + 64, y + 8), fill=BRAND_ACCENT)
    for row, color, offset in ((metadata, BRAND_ACCENT, 30), (cast, BRAND_TEXT, 78)):
        for row_size in range(34, 21, -2):
            row_font = get_font(row_size, "demi" if row == metadata else "medium")
            if draw.textlength(row, font=row_font) <= text_width:
                break
        else:
            raise ValueError("film details do not fit the end card")
        draw.text((left, y + offset), row, font=row_font, anchor="lt", fill=color,
                  stroke_width=2, stroke_fill="#11151b")
    canvas.save(path)


def countdown_overlays(frames, work):
    font = get_font(36, "demi")
    seconds_left = (frames + FPS - 1) // FPS
    width = even(math.ceil(font.getlength(f"{'8' * len(str(seconds_left // 60))}:88")) + 28)
    height = TIMER_HEIGHT
    travel = WIDTH - 2 * TIMER_MARGIN - width
    x = f"{TIMER_MARGIN}+{travel}*(n+{{start_frame}})/{frames - 1}"
    zero_start = frames - FPS // 4
    overlays = []
    for seconds_value in range(seconds_left, -1, -1):
        first = max(0, frames - seconds_value * FPS) if seconds_value else zero_start
        last = min(zero_start, frames - (seconds_value - 1) * FPS) if seconds_value else frames
        minutes, seconds_part = divmod(seconds_value, 60)
        canvas = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle((0, 0, width - 1, height - 1), radius=13, fill=(10, 13, 22, 221))
        draw.text((width // 2, height // 2), f"{minutes}:{seconds_part:02d}", font=font,
                  anchor="mm", fill=BRAND_TEXT)
        path = work / f"countdown-{seconds_value}.png"
        canvas.save(path)
        overlays.append((first, last, x, TIMER_Y, path))
    return overlays


def render(source, plan, shots, runs, cues, stream, dimensions, poster, destination, work):
    frames = shots[-1]["end_frame"]
    cta_path, cta = prepare_cta_motion(DEFAULT_CTA, work)
    x, y = cta["overlay_position"]
    overlays = []
    for index, cue in enumerate(cues):
        path = work / f"cue-{index:03d}.png"
        make_overlay(path, cue["text"])
        overlays.append((cue["start_frame"], cue["end_frame"], 0, CAPTION_TOP, path))

    paths = [render_shot(source, stream, dimensions, shot, overlays, work) for shot in shots]
    concat = work / "shots.ffconcat"
    concat.write_text("ffconcat version 1.0\n" + "".join(
        f"file '{path.name}'\nduration {(shot['end_frame'] - shot['start_frame']) / FPS:.9f}\n"
        for path, shot in zip(paths, shots)
    ), encoding="utf-8")
    audio, before_fades = prepare_audio(source, plan["audio_stream"], runs, work)
    base = work / "base.mp4"
    run([*FFMPEG, "-n", "-f", "concat", "-i", concat, "-f", "f32le",
         "-ar", AUDIO_RATE, "-ac", "2", "-i", audio, "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-metadata:s:a:0",
         f"language={'eng' if plan['language'] == 'en' else 'rus'}",
         "-video_track_timescale", "24000", base])

    details = plan.get("film_details")
    args = [sys.executable, POSTER_TOOL, base, destination, poster,
            "--picture-top", f"{frames - END_CARD_SECONDS * FPS}:{PANEL_HEIGHT}",
            "--subscribe-overlay", cta_path, x, y]
    if details:
        overlay = work / "film-details.png"
        make_film_details(overlay, details)
        args.extend(["--details-overlay", overlay])
    result = run(args, capture_output=True)
    poster_record = json.loads(result.stdout)
    poster_record["subscribe_ticket"] = cta
    if details:
        poster_record["film_details"] = details
    return poster_record, before_fades


def write_srt(path, cues, frames):
    timing = path.parent / "srt-cues.json"
    transcript = path.parent / "srt-transcript.txt"
    timing.write_text(json.dumps({"cues": [
        {"start_seconds": cue["start_frame"] / FPS, "end_seconds": cue["end_frame"] / FPS,
         "text": cue["text"]}
        for cue in cues
    ]}, ensure_ascii=False), encoding="utf-8")
    transcript.write_text("\n".join(cue["text"] for cue in cues), encoding="utf-8")
    result = run([sys.executable, SRT_TOOL, "build", "--cues", timing, "--text", transcript,
                  "--duration", frames / FPS, "--timebase", "final", "--output", path],
                 capture_output=True)
    report = json.loads(result.stdout)
    return {key: report[key] for key in ("structure", "text_coverage", "result")}


def review_frames(video, output_prefix, shots, poster, cta_samples=None):
    width, height = 240, 426
    triplets = []
    for shot in shots:
        start, last = shot["start_frame"], shot["end_frame"] - 1
        triplets.append((f"План {shot['number']}  |  {shot['in']:.3f}–{shot['out']:.3f} исходника",
                         (start, (start + last) // 2, last)))
    start = poster["first_poster_frame"]
    triplets.append(("Постер  |  до входа / вход / последний кадр",
                     (max(0, start - 1), start, poster["frames"] - 1)))
    if cta_samples is not None:
        triplets.append(("CTA  |  первый / средний / последний кадр", cta_samples))
    frame_numbers = sorted({frame for _, group in triplets for frame in group})
    selection = "+".join(f"eq(n,{frame})" for frame in frame_numbers)
    result = run([*FFMPEG, "-threads", "2", "-i", video, "-map", "0:v:0", "-an",
                  "-vf", f"select='{selection}',scale={width}:{height}", "-fps_mode", "passthrough",
                  "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"], capture_output=True)
    image_size = width * height * 3
    if len(result.stdout) != len(frame_numbers) * image_size:
        raise ValueError("could not extract every requested review frame")
    images = {
        frame: Image.frombytes("RGB", (width, height),
                               result.stdout[index * image_size:(index + 1) * image_size])
        for index, frame in enumerate(frame_numbers)
    }

    sheets = []
    per_sheet = 4
    for index in range(0, len(triplets), per_sheet):
        groups = triplets[index:index + per_sheet]
        row_height = height + 62
        sheet = Image.new("RGB", (3 * width + 32, len(groups) * row_height), "#171920")
        draw = ImageDraw.Draw(sheet)
        font = get_font(16)
        for row, (label, frames) in enumerate(groups):
            y = row * row_height
            draw.text((8, y + 6), label, font=font, fill="#f7f2e9")
            for col, frame in enumerate(frames):
                x = 8 + col * (width + 8)
                draw.text((x, y + 28), f"#{frame}   {frame / FPS:.3f} с", font=font, fill="#f7f2e9")
                sheet.paste(images[frame], (x, y + 50))
        path = output_prefix.with_suffix(f".shots-{len(sheets) + 1:02d}.jpg")
        sheet.save(path, quality=90)
        sheets.append(path)
    return sheets, triplets


def dbfs(data):
    if not data.size:
        return None
    peak = float(np.abs(data).max())
    rms = float(np.sqrt(np.mean(np.square(data))))
    return {"peak_dbfs": round(20 * math.log10(max(peak, 1e-6)), 1),
            "rms_dbfs": round(20 * math.log10(max(rms, 1e-6)), 1)}


def waveform_review(before, final, runs, output):
    seams = [(0, "Начало")]
    seams.extend((r["start_frame"] * SAMPLES_PER_FRAME, "Скачок в исходнике") for r in runs[1:])
    seams.append((len(before), "Конец"))
    width, row_height, left = 840, 128, 16
    sheet = Image.new("RGB", (width, row_height * len(seams)), "#171920")
    draw = ImageDraw.Draw(sheet)
    font = get_font(16)
    window = int(AUDIO_RATE * 0.22)
    plot_width = width - 2 * left
    review = []
    for index, (at, label) in enumerate(seams):
        offset = index * row_height
        begin, end = max(0, at - window), min(len(before), at + window)
        draw.text((left, offset + 5), f"{label}  |  {at / AUDIO_RATE:.3f} с  |  "
                  "серый — до фейда, голубой — точный MP4", font=font, fill="#f7f2e9")
        center = offset + 70
        draw.line((left, center, width - left, center), fill="#3a3d4a")
        draw.line((width // 2, center - 42, width // 2, center + 42), fill="#f4b860")
        for audio, color in ((before, "#666e81"), (final, "#7bdff2")):
            for x in range(plot_width):
                a = at - window + (x * 2 * window) // plot_width
                b = at - window + ((x + 1) * 2 * window) // plot_width
                if a >= end or b <= begin:
                    continue
                segment = audio[max(begin, a):min(end, b)]
                low, high = segment.min(), segment.max()
                draw.line((left + x, center - int(np.clip(high, -1, 1) * 38),
                           left + x, center - int(np.clip(low, -1, 1) * 38)), fill=color)
        review.append({
            "kind": "start" if at == 0 else "end" if at == len(before) else "source_jump",
            "time": round(at / AUDIO_RATE, 6),
            "before_fade_left": dbfs(before[max(0, at - FADE_SAMPLES):at]),
            "before_fade_right": dbfs(before[at:at + FADE_SAMPLES]),
            "final_left": dbfs(final[max(0, at - FADE_SAMPLES):at]),
            "final_right": dbfs(final[at:at + FADE_SAMPLES]),
        })
    sheet.save(output, quality=90)
    return review


def main(source, plan_path, output):
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    name = plan["id"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", name):
        raise ValueError("id may contain only letters, digits, dashes and underscores")
    if plan["language"] not in {"ru", "en"}:
        raise ValueError("language must be ru or en")
    if not isinstance(plan["title"], str) or not plan["title"].strip():
        raise ValueError("title must be a non-empty string")
    if not isinstance(plan["hook"], str):
        raise ValueError("hook must be a string")
    if isinstance(plan["audio_stream"], bool) or not isinstance(plan["audio_stream"], int):
        raise ValueError("audio_stream must be the absolute integer ffprobe index")
    poster = Path(plan["poster"])
    if not poster.is_absolute() or not poster.is_file():
        raise ValueError("poster must be an absolute path to an existing poster file")

    source_info = probe(source)
    videos = [s for s in source_info["streams"] if s["codec_type"] == "video"
              and not s["disposition"]["attached_pic"]]
    audio = next((s for s in source_info["streams"] if s["codec_type"] == "audio"
                  and s["index"] == plan["audio_stream"]), None)
    if not videos or audio is None:
        raise ValueError("source has no main picture or the specified audio index is not audio")
    video = videos[0]
    shots, audio_runs, dimensions = make_edit(
        plan, video, float(source_info["format"]["duration"])
    )
    cues = conform_cues(plan.get("cues", []), audio_runs)
    output.mkdir(parents=True, exist_ok=True)
    if any(path.is_file() for path in output.glob(f"{name}.*")):
        raise FileExistsError(f"outputs for {name} already exist in {output}; choose a new ID or directory")

    with tempfile.TemporaryDirectory(prefix=f".{name}-", dir=output) as staging:
        work = Path(staging)
        prefix = work / name
        destination = prefix.with_suffix(".mp4")
        srt = prefix.with_suffix(f".{plan['language']}.srt") if cues else None
        srt_review = write_srt(srt, cues, shots[-1]["end_frame"]) if srt else None
        poster_result, before_fades = render(
            source, plan, shots, audio_runs, cues, video["index"], dimensions,
            poster, destination, work
        )
        report = probe(destination)
        result_video = next(stream for stream in report["streams"] if stream["codec_type"] == "video")
        result_audio = next(stream for stream in report["streams"] if stream["codec_type"] == "audio")
        frames = shots[-1]["end_frame"]
        actual_video = (result_video["width"], result_video["height"], result_video["codec_name"],
                        result_video["pix_fmt"], result_video["r_frame_rate"],
                        result_video["avg_frame_rate"], int(result_video["nb_frames"]))
        if actual_video != (WIDTH, HEIGHT, "h264", "yuv420p", "24/1", "24/1", frames):
            raise ValueError(f"final video does not match the delivery spec: {actual_video}")
        if (result_audio["codec_name"], int(result_audio["sample_rate"]), result_audio["channels"]) != (
                "aac", AUDIO_RATE, 2):
            raise ValueError("final audio does not match AAC stereo 48 kHz")
        if abs(float(result_audio["duration"]) - frames / FPS) > 0.002:
            raise ValueError("final audio and picture durations disagree")

        run([*FFMPEG, "-threads", "2", "-i", destination, "-map", "0:v:0", "-map", "0:a:0",
             "-f", "null", "-"])
        final_audio = read_pcm(destination, result_audio["index"])
        if len(final_audio) < len(before_fades) or len(final_audio) - len(before_fades) > 1024:
            raise ValueError("decoded AAC length diverges from the edit beyond codec padding")
        waveform_path = prefix.with_suffix(".audio.jpg")
        audio_review = waveform_review(before_fades, final_audio[:len(before_fades)], audio_runs,
                                       waveform_path)
        sheets, review_samples = review_frames(destination, prefix, shots, poster_result,
                                               (0, frames // 2, frames - 1))
        files = [destination, waveform_path, *sheets]
        if srt:
            files.append(srt)

        qa = prefix.with_suffix(".qa.json")
        digest = hashlib.sha256()
        with destination.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        record = {
            "id": name, "title": plan["title"], "source": str(source), "plan": str(plan_path),
            "mp4": destination.name, "sha256": digest.hexdigest(), "full_decode": "pass",
            "fps": FPS, "frames": frames, "duration": frames / FPS,
            "video": result_video, "audio": result_audio, "source_audio_stream": audio,
            "picture_shots": shots, "active_crop": dimensions[2],
            "audio_runs": audio_runs, "audio_fade_ms": FADE_MS,
            "audio_policy": "Linear fades at clip ends and source discontinuities; "
                            "contiguous picture cuts retain source audio.",
            "audio_waveform": waveform_path.name, "audio_seams": audio_review,
            "screen_overlays": ["subscribe_ticket", "film_card"] + (["speech_captions"] if cues else []),
            "poster": poster_result, "poster_path": str(poster), "cues": cues,
            "srt_review": srt_review, "typography": {"font": get_font(16).getname()[0],
                                                      "accent": BRAND_ACCENT, "text": BRAND_TEXT},
            "shot_sheets": [path.name for path in sheets], "sampled_frames": review_samples,
            "editorial_review": "pending visual inspection and speech verification against dub",
        }
        qa.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        files.append(qa)
        for path in files:
            path.rename(output / path.name)
    print(output / destination.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("plan", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    try:
        main(args.source.resolve(), args.plan.resolve(), args.output_dir.resolve())
    except (KeyError, TypeError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        if isinstance(exc, subprocess.CalledProcessError) and exc.stderr:
            print(exc.stderr.decode(errors="replace"), file=sys.stderr, end="")
        parser.exit(1, f"{parser.prog}: {exc}\n")
