"""Observed media checks at the completion boundary; no network or creative verdicts."""
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path
import subprocess

from .errors import WorkflowError
from .util import canonical, file_digest


def _run(argv, *, timeout):
    try:
        result = subprocess.run(argv, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                check=False, shell=False, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise WorkflowError(f"media validation could not finish: {type(exc).__name__}") from exc
    if result.returncode:
        raise WorkflowError(f"media validation failed: {result.stderr[-1500:].strip()}")
    return result.stdout


def _positive(value, name):
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise WorkflowError(f"media has no valid {name}") from None
    if not math.isfinite(result) or result <= 0:
        raise WorkflowError(f"media has no positive finite {name}")
    return result


def probe_media(path):
    """Return a stable summary obtained from ffprobe, not from caller JSON."""
    path = Path(path).resolve()
    raw = _run(["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe",
                "-format_whitelist", "mov,mp3,wav,flac,ogg,matroska,webm,aac,avi,mpegts",
                "-show_format", "-show_streams", "-of", "json", str(path)], timeout=30)
    try:
        data = json.loads(raw)
        streams, container = data["streams"], data["format"]
    except (ValueError, KeyError, TypeError):
        raise WorkflowError("ffprobe did not return media streams and format") from None
    durations = [container.get("duration")] + [stream.get("duration") for stream in streams]
    duration = next((value for value in durations if value not in (None, "N/A")), None)
    video, audio = [], []
    for stream in streams:
        if stream.get("codec_type") not in {"video", "audio"}:
            continue
        codec = stream.get("codec_name")
        if not codec or codec == "unknown":
            raise WorkflowError("media contains an unknown codec")
        if stream.get("codec_type") == "video" and not stream.get("disposition", {}).get("attached_pic"):
            width, height = stream.get("width"), stream.get("height")
            if type(width) is not int or type(height) is not int or min(width, height) < 1:
                raise WorkflowError("video has invalid dimensions")
            video.append({"codec": codec, "tag": stream.get("codec_tag_string"), "width": width, "height": height,
                          **{key: stream.get(key) for key in (
                              "pix_fmt", "sample_aspect_ratio", "avg_frame_rate", "r_frame_rate", "nb_frames",
                              "duration", "color_primaries", "color_transfer", "color_space", "color_range")}})
        elif stream.get("codec_type") == "audio":
            channels = stream.get("channels")
            if type(channels) is not int or channels < 1:
                raise WorkflowError("audio has invalid channels")
            audio.append({"codec": codec, "sample_rate": int(_positive(stream.get("sample_rate"), "sample rate")),
                          "channels": channels, "duration": stream.get("duration"), "start_time": stream.get("start_time")})
    return {"duration_seconds": round(_positive(duration, "duration"), 6),
            "format_name": container.get("format_name"), "major_brand": container.get("tags", {}).get("major_brand"),
            "video": video, "audio": audio}


def _decode(path, *, timeout=300):
    _run(["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-err_detect", "explode", "-threads", "2",
          "-protocol_whitelist", "file,pipe", "-format_whitelist", "mov,mp3,wav,flac,ogg,matroska,webm,aac,avi,mpegts",
          "-i", str(Path(path).resolve()), "-map", "0:v?", "-map", "0:a?", "-f", "null", "-"], timeout=timeout)


def validate_video(path, *, require_audio=True, mp4=True):
    before = file_digest(path)
    summary = probe_media(path)
    if not summary["video"] or (require_audio and not summary["audio"]):
        raise WorkflowError("video needs a video stream and the expected audio stream")
    if mp4:
        brand = summary["major_brand"] or ""
        if "mp4" not in (summary["format_name"] or "").split(",") or not (
                brand.startswith("iso") or brand in {"mp41", "mp42", "avc1", "M4V ", "MSNV", "dash", "cmfc", "cmfs"}):
            raise WorkflowError("render must be an actual MP4 container")
        tags = {"h264": {"avc1", "avc3"}, "hevc": {"hvc1", "hev1"}, "av1": {"av01"},
                "vp9": {"vp09"}, "mpeg4": {"mp4v"}}
        if any(stream["tag"] not in tags.get(stream["codec"], set()) for stream in summary["video"]):
            raise WorkflowError("render has an unsupported MP4 video codec/tag")
    _decode(path)
    if file_digest(path) != before:
        raise WorkflowError("video changed during validation")
    return summary


def validate_audio(path):
    before = file_digest(path)
    summary = probe_media(path)
    if not summary["audio"] or summary["video"]:
        raise WorkflowError("audio output must contain an audio stream without video")
    _decode(path)
    if file_digest(path) != before:
        raise WorkflowError("audio changed during validation")
    return summary


def validate_image(path):
    try:
        from PIL import Image
    except ImportError as exc:
        raise WorkflowError("image validation requires the media dependency extra") from exc
    before = file_digest(path)
    try:
        with Image.open(path) as picture:
            width, height = picture.size
            if picture.format not in {"PNG", "JPEG", "WEBP"} or min(width, height) < 1 or width * height > 64_000_000:
                raise WorkflowError("image must be a supported raster with bounded positive dimensions")
            if getattr(picture, "n_frames", 1) != 1:
                raise WorkflowError("scene image must be a single frame")
            result = {"width": width, "height": height, "format": picture.format, "mime": Image.MIME[picture.format]}
            picture.verify()
        with Image.open(path) as picture:
            picture.load()
    except (OSError, SyntaxError, ValueError, Image.DecompressionBombError) as exc:
        raise WorkflowError("image bytes cannot be fully decoded") from exc
    if file_digest(path) != before:
        raise WorkflowError("image changed during validation")
    return result


def validate_font_face(path, index, expected):
    """Read the selected face; a renamed file or different TTC index is not the brand font."""
    try:
        from PIL import ImageFont
        if type(index) is not int or index < 0:
            raise ValueError("invalid font index")
        family, style = ImageFont.truetype(str(path), 16, index=index).getname()
    except (ImportError, OSError, ValueError) as exc:
        raise WorkflowError("the required caption font face cannot be inspected") from exc
    if {"family": family, "style": style} != expected:
        raise WorkflowError("caption font family/style differs from the pinned brand face")
    return {"family": family, "style": style, "index": index, "sha256": file_digest(path)}


def source_frame_anchors(path, start, end):
    """Read first/middle/last real PTS in one used source interval, including VFR."""
    path = str(Path(path).resolve())
    options = ["ffprobe", "-v", "error", "-protocol_whitelist", "file,pipe", "-select_streams", "v:0"]
    metadata = json.loads(_run([*options, "-show_entries",
        "stream=time_base,start_time,duration,avg_frame_rate,has_b_frames:format=start_time,duration",
        "-of", "json", path], timeout=30))
    try:
        origin = Fraction(str(metadata.get("format", {}).get("start_time", "0")))
        stream = metadata["streams"][0]
        time_base = Fraction(stream["time_base"])
        video_end = (Fraction(str(stream.get("start_time", origin))) + Fraction(str(stream["duration"])) - origin
                     if stream.get("duration") not in (None, "N/A") else None)
        container_end = (Fraction(str(metadata["format"]["duration"]))
                         if metadata.get("format", {}).get("duration") not in (None, "N/A") else None)
        first, stop = Fraction(str(start)), Fraction(str(end))
        if first < 0 or stop <= first or time_base <= 0:
            raise ValueError
    except (KeyError, IndexError, TypeError, ValueError, ZeroDivisionError) as exc:
        raise WorkflowError("source frame timestamps need an exact video time base and interval") from exc
    # Seek can land on an earlier keyframe. Reordering spans frames, not a
    # fixed second: at 1-2 fps even an ordinary
    # B-frame queue can exceed one second. Use the observed rate and decoder
    # delay for bounded lookahead, retaining the actual-PTS witness below.
    lookahead = Fraction(1)
    try:
        rate = Fraction(stream.get("avg_frame_rate", "0/1"))
        delay = int(stream.get("has_b_frames", 0))
        if rate > 0 and delay >= 0:
            lookahead = max(lookahead, Fraction(delay + 2) / rate)
    except (TypeError, ValueError, ZeroDivisionError):
        pass
    read_stop = stop + lookahead
    frames = json.loads(_run([*options, "-read_intervals", f"{float(origin + first):.9f}%{float(origin + read_stop):.9f}",
        "-show_frames", "-show_entries", "frame=best_effort_timestamp,duration,pkt_duration", "-of", "json", path], timeout=30))
    try:
        times = sorted({Fraction(frame["best_effort_timestamp"]) * time_base - origin for frame in frames["frames"]})
        extents = [(Fraction(frame["best_effort_timestamp"])
                    + Fraction(frame.get("duration") or frame.get("pkt_duration") or 0)) * time_base - origin
                   for frame in frames["frames"]]
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        raise WorkflowError("source frames do not provide inspectable actual timestamps") from exc
    tolerance = Fraction(1, 1_000_000)  # ffprobe's format.start_time is rounded to microseconds.
    if video_end is not None and stop > video_end + tolerance:
        raise WorkflowError("used source interval exceeds the actual video stream")
    known_end = video_end if video_end is not None else container_end
    reached_end = known_end is not None and read_stop >= known_end
    if reached_end and video_end is None:
        # A longer audio stream can define container EOF. Only decoded video
        # frame extents can establish video coverage when stream.duration is absent.
        if not extents or max(extents) < stop - tolerance:
            raise WorkflowError("used source interval exceeds the actual video stream")
    if not (any(extent >= stop - tolerance for extent in extents) or reached_end):
        raise WorkflowError("bounded source probe could not confirm the final used frame; inspect the source timestamps")
    times = [time for time in times if first - tolerance <= time < stop - tolerance]
    if not times:
        raise WorkflowError("used source interval contains no observed video frames")
    midpoint = min(times, key=lambda time: (abs(time - (first + stop) / 2), time))
    return [round(float(time), 6) for time in (times[0], midpoint, times[-1])]


def validate_srt(path, *, duration, project_root):
    parser_path = Path(project_root) / "automation/helpers/srt/scripts/srt_tool.py"
    specification = importlib.util.spec_from_file_location("ytvideos_canonical_srt", parser_path)
    parser = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(parser)
    try:
        cues = parser.parse_srt(Path(path).read_text(encoding="utf-8"))
        previous_end = 0.0
        for cue in cues:
            start, end = float(cue["start_seconds"]), float(cue["end_seconds"])
            if (not math.isfinite(start) or not math.isfinite(end) or start < previous_end or end <= start
                    or end > _positive(duration, "subtitle media duration") + 0.001
                    or not cue["text"].strip() or "\x00" in cue["text"]):
                raise WorkflowError("SRT has invalid, overlapping or out-of-media cue bounds")
            previous_end = end
    except (ValueError, UnicodeError) as exc:
        raise WorkflowError("SRT structure is invalid") from exc
    return {"cues": len(cues), "last_end_seconds": previous_end, "media_duration_seconds": duration}


def validate_review(path, *, render_path, render_sha256, require_audio=True):
    try:
        review = json.loads(Path(path).read_text())
    except (ValueError, UnicodeError) as exc:
        raise WorkflowError("review must be a QA JSON document") from exc
    actual = probe_media(render_path)
    if (type(review) is not dict or review.get("reviewed_sha256") != render_sha256
            or file_digest(render_path) != render_sha256 or canonical(review.get("probe")) != canonical(actual)):
        raise WorkflowError("review must bind the exact rendered MP4 and its actual ffprobe summary")
    if not actual["video"] or (require_audio and not actual["audio"]):
        raise WorkflowError("reviewed media is missing required streams")
    return actual
