#!/usr/bin/env python3
"""Index a local film's source-time dialogue and editorial search windows."""

import argparse
from dataclasses import dataclass
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


TEXT_CODECS = {
    "ass", "eia_608", "jacosub", "microdvd", "mpl2", "mov_text", "pjs",
    "realtext", "sami", "srt", "ssa", "stl", "subrip", "subviewer",
    "subviewer1", "text", "vplayer", "webvtt",
}
LANGUAGE_GROUPS = (
    "ar ara", "bg bul", "cs ces cze", "da dan", "de deu ger", "el ell gre",
    "en eng", "es spa", "fa fas per", "fi fin", "fr fra fre", "he heb",
    "hi hin", "hr hrv", "hu hun", "id ind", "it ita", "ja jpn", "ko kor",
    "nl nld dut", "no nor", "pl pol", "pt por", "ro ron rum", "ru rus",
    "sk slk slo", "sr srp scc", "sv swe", "th tha", "tr tur", "uk ukr",
    "vi vie", "zh zho chi",
)
LANGUAGE_ALIASES = {
    alias: group.split()[0] for group in LANGUAGE_GROUPS for alias in group.split()
}
SRT_TIME = r"(\d{2,}):(\d{2}):(\d{2})[,.](\d{3})"
SRT_RANGE = re.compile(rf"^{SRT_TIME}\s*-->\s*{SRT_TIME}(?:\s.*)?$")
FORCED_TITLE = re.compile(r"\bforced\b|форсирован", re.IGNORECASE)
WINDOW_MS = 45_000
STEP_MS = 30_000


@dataclass(frozen=True)
class Cue:
    start: int
    end: int
    text: str


def run(*command):
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"{command[0]} exited {result.returncode}")
    return result.stdout


def normalize_language(value):
    code = value.strip().lower().replace("_", "-").partition("-")[0]
    if code in {"", "und", "mul", "zxx", "auto"}:
        return None
    return LANGUAGE_ALIASES.get(code, code)


def stream_language(stream):
    return normalize_language(stream.get("tags", {}).get("language", ""))


def disposition(stream, flag):
    return bool(stream.get("disposition", {}).get(flag, 0))


def positive_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) and number > 0 else 0.0


def cue_ms(groups):
    hours, minutes, seconds, millis = map(int, groups)
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def timecode(ms):
    seconds, millis = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"


def parse_srt(path):
    if not path.is_file():
        return []
    cues = []
    for block in re.split(r"\n[ \t]*\n", path.read_text(encoding="utf-8-sig")):
        lines = block.strip().splitlines()
        time_line = int(bool(lines and lines[0].isdigit()))
        if len(lines) <= time_line:
            continue
        match = SRT_RANGE.fullmatch(lines[time_line].strip())
        if match is None:
            continue
        start, end = cue_ms(match.groups()[:4]), cue_ms(match.groups()[4:])
        dialogue = " ".join(lines[time_line + 1:])
        dialogue = html.unescape(re.sub(r"<[^>]+>|\{\\[^}]+\}", "", dialogue))
        dialogue = " ".join(dialogue.split())
        if start < end and dialogue:
            cues.append(Cue(start, end, dialogue))
    return sorted(cues, key=lambda cue: (cue.start, cue.end))


def extract_text_tracks(source, streams, language, duration, stage):
    tracks = []
    candidates = []
    for stream in streams:
        index = stream["index"]
        title = stream.get("tags", {}).get("title", "")
        track = {
            "stream": index, "codec": stream.get("codec_name"),
            "language": stream_language(stream), "title": title,
            "default": disposition(stream, "default"),
            "hearing_impaired": disposition(stream, "hearing_impaired"),
        }
        tracks.append(track)
        if disposition(stream, "forced") or FORCED_TITLE.search(title):
            track["status"] = "skipped_forced"
            continue
        if track["codec"] not in TEXT_CODECS:
            track["status"] = "skipped_non_text"
            continue
        target = stage / f"subtitle-{index}.srt"
        try:
            run("ffmpeg", "-v", "error", "-nostdin", "-copyts", "-start_at_zero",
                "-i", str(source), "-map", f"0:{index}", "-c:s", "srt", str(target))
        except RuntimeError as exc:
            track.update(status="extract_error", error=str(exc))
            continue
        cues = parse_srt(target)
        track["cue_count"] = len(cues)
        if not cues:
            track["status"] = "empty"
            continue
        first = cues[0].start / 1000
        last = max(cue.end for cue in cues) / 1000
        track.update(first_cue=first, last_cue=last)
        # Screen out sparse signs-only or partial tracks lacking forced metadata.
        if duration >= 300 and (len(cues) < duration / 180 or last - first < duration / 2):
            track["status"] = "sparse_or_partial"
            continue
        track["status"] = "usable"
        rank = (bool(language and track["language"] == language),
                (last - first) / duration, len(cues),
                not track["hearing_impaired"], track["default"], -index)
        candidates.append((rank, track, target, cues))
    if not candidates:
        return tracks, None
    _, selected, target, cues = max(candidates, key=lambda item: item[0])
    selected["status"] = "selected"
    return tracks, (selected, target, cues)


def local_whisper(source, audio_index, language, model, stage):
    whisper = shutil.which("whisper")
    if whisper is None:
        raise RuntimeError("No usable text subtitles. Install local OpenAI Whisper on PATH.")
    if model is None:
        cache = Path(os.environ.get("XDG_CACHE_HOME") or Path.home() / ".cache") / "whisper"
        local_cache = Path.home() / "Library" / "Caches" / "whisper"
        preferred = ("small.pt", "base.pt", "tiny.pt", "large-v3-turbo.pt", "medium.pt")
        model = next((folder / name for name in preferred for folder in (cache, local_cache)
                      if (folder / name).is_file()), None)
    if model is None or not model.is_file():
        raise RuntimeError("No usable text subtitles. Pass --whisper-model with a local .pt file.")

    audio = stage / "selected-audio.wav"
    run("ffmpeg", "-v", "error", "-nostdin", "-copyts", "-start_at_zero", "-i", str(source),
        "-map", f"0:{audio_index}", "-af", "aresample=async=1:first_pts=0",
        "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(audio))
    command = [whisper, str(audio), "--model", str(model.resolve()), "--device", "cpu",
               "--task", "transcribe", "--fp16", "False", "--verbose", "False",
               "--threads", str(min(4, os.cpu_count() or 1)),
               "--output_dir", str(stage), "--output_format", "srt"]
    if language:
        command.extend(("--language", language))
    run(*command)
    target = audio.with_suffix(".srt")
    if not target.is_file():
        raise RuntimeError("Local Whisper returned without an SRT file.")
    return target, parse_srt(target), model.name


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def index_windows(cues, duration_ms):
    rows = []
    for start in range(0, duration_ms, STEP_MS):
        end = min(start + WINDOW_MS, duration_ms)
        hits = [(index, cue) for index, cue in enumerate(cues, 1)
                if cue.start < end and cue.end > start]
        cursor = start
        longest_gap = 0
        for _, cue in hits:
            longest_gap = max(longest_gap, cue.start - cursor)
            cursor = max(cursor, cue.end)
        samples = []
        if hits:
            sample_positions = sorted({0, len(hits) // 2, len(hits) - 1})
            samples = [hits[position][1].text for position in sample_positions]
        rows.append({
            "id": f"window-{len(rows) + 1:03}", "start": start / 1000, "end": end / 1000,
            "cue_count": len(hits), "first_cue_id": hits[0][0] if hits else None,
            "last_cue_id": hits[-1][0] if hits else None,
            "question_cues": sum("?" in cue.text for _, cue in hits),
            "exclamation_cues": sum("!" in cue.text for _, cue in hits),
            "longest_gap_in_text": max(longest_gap, end - cursor) / 1000,
            "samples": samples,
        })
        if end == duration_ms:
            break
    return rows


def write_indexes(stage, cues, duration, subtitle_method):
    with (stage / "transcript.txt").open("w", encoding="utf-8") as transcript:
        transcript.write(f"Source-time search transcript ({subtitle_method}). "
                         "Verify dialogue and timing against the selected audio before captioning.\n\n")
        for index, cue in enumerate(cues, 1):
            transcript.write(f"{index:04} {timecode(cue.start)} – {timecode(cue.end)}  {cue.text}\n")

    windows = index_windows(cues, round(duration * 1000))
    write_json(stage / "candidates.json", windows)
    with (stage / "candidates.md").open("w", encoding="utf-8") as index:
        index.write("# Film scene search index\n\n"
                    "Chronological windows cover the source, including windows without subtitles. "
                    "Gaps measure absence of text cues. Use the footage and audio to choose scenes.\n\n"
                    "| Window | Source time | Cues | ? | ! | Longest text gap | Samples |\n"
                    "| --- | --- | ---: | ---: | ---: | ---: | --- |\n")
        for row in windows:
            span = f"{timecode(round(row['start'] * 1000))}–{timecode(round(row['end'] * 1000))}"
            samples = " · ".join(row["samples"]).replace("|", r"\|")
            index.write(f"| {row['id']} | {span} | {row['cue_count']} | {row['question_cues']} | "
                        f"{row['exclamation_cues']} | {row['longest_gap_in_text']:.1f}s | {samples} |\n")
    return len(windows)


def discover(source, output, audio_index, requested_language, model):
    identity = source.stat()
    probe = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format",
                           "-of", "json", str(source)))
    streams = probe.get("streams", [])
    duration = positive_number(probe.get("format", {}).get("duration")) or max(
        (positive_number(stream.get("duration")) for stream in streams), default=0,
    )
    if not duration:
        raise RuntimeError("The source has no measurable duration.")

    video = next((stream for stream in streams if stream["codec_type"] == "video"
                  and not disposition(stream, "attached_pic")), None)
    if video is None:
        raise RuntimeError("The source has no video stream.")
    audio_tracks = [stream for stream in streams if stream["codec_type"] == "audio"]
    if audio_index is not None:
        audio_tracks = [stream for stream in audio_tracks if stream["index"] == audio_index]
    if not audio_tracks:
        raise RuntimeError(f"Stream {audio_index} is not audio." if audio_index is not None
                           else "The source has no audio stream.")
    audio = max(audio_tracks, key=lambda stream: (
        bool(requested_language and stream_language(stream) == requested_language),
        not disposition(stream, "visual_impaired"), not disposition(stream, "comment"),
        disposition(stream, "default"), -stream["index"],
    ))
    language = stream_language(audio) or requested_language
    subtitles = [stream for stream in streams if stream["codec_type"] == "subtitle"]
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".discover-", dir=output) as temporary:
        stage = Path(temporary)
        tracks, embedded = extract_text_tracks(source, subtitles, language, duration, stage)
        if embedded:
            selected, subtitle_file, cues = embedded
            subtitle_info = {"method": "embedded_text", "stream": selected["stream"],
                             "language": selected["language"], "title": selected["title"],
                             "matches_dub": "unverified"}
        else:
            subtitle_file, cues, model_name = local_whisper(source, audio["index"], language, model, stage)
            subtitle_info = {"method": "local_whisper", "stream": None, "language": language,
                             "model": model_name, "audio_stream": audio["index"],
                             "matches_dub": "machine_draft"}

        source_srt = stage / "source.srt"
        subtitle_file.replace(source_srt)
        subtitle_info.update(
            srt="source.srt", transcript="transcript.txt", cue_count=len(cues),
            cues_ending_after_source=sum(cue.end > round(duration * 1000) for cue in cues),
            srt_sha256=hashlib.sha256(source_srt.read_bytes()).hexdigest(),
        )
        window_count = write_indexes(stage, cues, duration, subtitle_info["method"])
        current = source.stat()
        if (identity.st_dev, identity.st_ino, identity.st_size, identity.st_mtime_ns) != (
            current.st_dev, current.st_ino, current.st_size, current.st_mtime_ns,
        ):
            raise RuntimeError("The source changed during discovery. Run discovery again.")
        write_json(stage / "discovery.json", {
            "schema_version": 1, "source": str(source), "duration": duration,
            "source_size_bytes": identity.st_size, "source_mtime_ns": identity.st_mtime_ns,
            "video_stream": video["index"], "width": video.get("width"), "height": video.get("height"),
            "audio_stream": audio["index"], "audio_language": stream_language(audio),
            "audio_title": audio.get("tags", {}).get("title"),
            "subtitles": subtitle_info, "subtitle_tracks": tracks,
            "candidates": "candidates.json", "candidate_index": "candidates.md", "window_count": window_count,
        })
        for filename in ("source.srt", "transcript.txt", "candidates.json", "candidates.md", "discovery.json"):
            (stage / filename).replace(output / filename)
    return output / "discovery.json"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Local movie file")
    parser.add_argument("output_dir", type=Path, help="Dedicated working directory for this source")
    parser.add_argument("--audio-stream", type=int, help="Absolute ffprobe stream index")
    parser.add_argument("--language", default="ru", help="Preferred audio language (default ru, or auto)")
    parser.add_argument("--whisper-model", type=Path, help="Local Whisper .pt checkpoint for ASR fallback")
    args = parser.parse_args()
    try:
        source = args.source.expanduser().resolve(strict=True)
        if not source.is_file():
            raise RuntimeError("SOURCE must be a local movie file.")
        result = discover(source, args.output_dir.expanduser().resolve(), args.audio_stream,
                          normalize_language(args.language),
                          args.whisper_model.expanduser() if args.whisper_model else None)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"discovery: {exc}\n")
    print(result)


if __name__ == "__main__":
    main()
