#!/usr/bin/env python3
"""Offline one-still-per-phrase conform from an exact retained PCM WAV and word map."""

import argparse
import hashlib
import json
import math
import re
import sys
import wave
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

_SHA = re.compile(r"[0-9a-f]{64}")
_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}")
_QUOTES = str.maketrans("", "", '"“”„‟«»')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def object_keys(value, required, optional=()):
    require(isinstance(value, dict) and set(required) <= value.keys()
            and value.keys() <= set(required) | set(optional),
            "invalid object fields; expected " + ", ".join(required))
    return value


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checked_file(path, sha, base, suffixes):
    require(isinstance(path, str) and bool(path), "input path is required")
    require(isinstance(sha, str) and _SHA.fullmatch(sha), "input SHA-256 is required")
    source = (base / path).resolve(strict=True)
    require(source.is_file() and source.suffix.lower() in suffixes, "unexpected input type")
    require(sha256(source) == sha, "input SHA-256 mismatch: " + source.name)
    return source


def pcm_duration(path):
    try:
        with wave.open(str(path), "rb") as wav:
            samples, rate = wav.getnframes(), wav.getframerate()
            stride = wav.getsampwidth() * wav.getnchannels()
            remaining = samples
            while remaining:
                size = min(remaining, 65536)
                require(len(wav.readframes(size)) == size * stride, "truncated PCM WAV")
                remaining -= size
    except (wave.Error, EOFError) as exc:
        raise ValueError("final voice must be a valid PCM WAV") from exc
    require(samples > 0 and rate > 0, "final voice cannot be empty")
    return Fraction(samples, rate)


def exact_number(value):
    require(type(value) in (int, str, Decimal), "expected a finite integer, decimal or ratio")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError("expected a finite integer, decimal or ratio") from exc


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"), parse_float=Decimal)


def round_frame(seconds, fps):
    return (seconds * fps + Fraction(1, 2)) // 1


def checked_id(ident, seen, kind):
    require(isinstance(ident, str) and _ID.fullmatch(ident) and ident not in seen,
            f"{kind} IDs must be safe and unique")
    seen.add(ident)
    return ident


def plan(request, base, *, timing_only=False):
    object_keys(request, ("schema", "fps", "origin_frame", "end_frame", "audio_start_frame",
                          "audio", "transcript_path", "alignment_path", "phrases"))
    require(type(request["schema"]) is int and request["schema"] == 1, "unsupported schema")
    fps = exact_number(request["fps"])
    require(fps > 1 and (fps.denominator == 1 or
            isinstance(request["fps"], str) and "/" in request["fps"]),
            "fps requires an integer or explicit ratio")
    origin, end, begin = (request[key] for key in ("origin_frame", "end_frame", "audio_start_frame"))
    require(all(type(x) is int for x in (origin, end, begin)) and 0 <= origin <= begin < end,
            "invalid absolute half-open record range")
    audio = object_keys(request["audio"], ("path", "sha256"))
    audio_path = checked_file(audio["path"], audio["sha256"], base, {".wav"})
    duration = pcm_duration(audio_path)
    require(begin + math.ceil(duration * fps) <= end, "final WAV exceeds timeline")
    transcript = (base / request["transcript_path"]).read_text(encoding="utf-8").strip()
    tokens = transcript.split()
    require(tokens, "exact transcript is empty")
    alignment_path = base / request["alignment_path"]
    alignment_bytes = alignment_path.read_bytes()
    alignment = json.loads(alignment_bytes.decode("utf-8"), parse_float=Decimal)
    transcript_sha = hashlib.sha256(transcript.encode("utf-8")).hexdigest()
    require(isinstance(alignment, dict) and alignment.get("status") == "REVIEW_REQUIRED"
            and alignment.get("audio_sha256") == audio["sha256"]
            and alignment.get("transcript_sha256") == transcript_sha,
            "need a review-required word map bound to this final WAV and exact transcript")
    aligned = alignment.get("words")
    require(isinstance(aligned, list) and len(aligned) == len(tokens), "word count mismatch")
    intervals, timing_flags, previous = [], [], Fraction(0)
    for index, (row, token) in enumerate(zip(aligned, tokens), 1):
        display = token.translate(_QUOTES)
        require(display and isinstance(row, dict) and row.get("text") == display,
                f"exact alignment token mismatch at word {index}")
        start, stop = (exact_number(row.get(key)) for key in ("start", "end"))
        require(previous <= start < stop <= duration, f"invalid source timing at word {index}")
        score = None if row.get("score") is None else exact_number(row["score"])
        require(score is None or 0 <= score <= 1, f"invalid confidence at word {index}")
        if score is None or score < Fraction(4, 5):
            reason = "missing confidence" if score is None else "confidence below 0.80"
            require(timing_only, f"{reason} at word {index}; review alignment")
            timing_flags.append(dict(word_index=index, reason=reason))
        intervals.append((start, stop))
        previous = stop
    rows = request["phrases"]
    require(isinstance(rows, list) and rows, "approved phrase list is empty")
    shots, titles, missing, ids, title_ids, cursor = [], [], [], set(), set(), 0
    for row in rows:
        object_keys(row, ("id", "text"), ("asset_path", "asset_sha256", "titles"))
        ident = checked_id(row["id"], ids, "phrase")
        phrase = row["text"]
        require(isinstance(phrase, str) and phrase.strip(), f"empty phrase {ident}")
        phrase = phrase.strip()
        part = phrase.split()
        next_cursor = cursor + len(part)
        require(part == tokens[cursor:next_cursor],
                f"phrase {ident} does not match the next exact transcript span")
        in_frame = begin + round_frame(intervals[cursor][0], fps)
        subcues = row.get("titles", [dict(id=ident, text=phrase)])
        require(isinstance(subcues, list) and subcues, f"no title groups for {ident}")
        at = cursor
        for cue in subcues:
            object_keys(cue, ("id", "text"))
            title_id = checked_id(cue["id"], title_ids, "title")
            display = cue["text"]
            require(isinstance(display, str) and display.strip(), f"empty title {title_id}")
            display = display.strip()
            through = at + len(display.split())
            require(through <= next_cursor and display.split() == tokens[at:through],
                    f"title {title_id} does not match the next exact phrase span")
            words = [dict(text=tokens[k], start=begin + round_frame(intervals[k][0], fps),
                          end=begin + round_frame(intervals[k][1], fps)) for k in range(at, through)]
            for source_index, word in enumerate(words, at + 1):
                if word["start"] == word["end"]:
                    reason = "word collapses at target frame rate"
                    require(timing_only, f"{reason} at word {source_index}; review alignment")
                    timing_flags.append(dict(word_index=source_index, reason=reason))
            a, b = words[0]["start"], words[-1]["end"]
            require(origin <= a < b <= end, f"title {title_id} collapsed or exceeded record")
            require(not titles or titles[-1]["end"] <= a, "quantized titles overlap")
            titles.append(dict(id=title_id, start=a, end=b, text=display, words=words))
            at = through
        require(at == next_cursor, f"titles omit words from phrase {ident}")
        shot = dict(id=ident, start=in_frame if shots else origin)
        has_path, has_hash = "asset_path" in row, "asset_sha256" in row
        require(has_path == has_hash, f"partial still identity for {ident}")
        if has_path:
            path = checked_file(row["asset_path"], row["asset_sha256"], base, {".jpg", ".jpeg", ".png"})
            shot.update(asset_path=str(path), asset_sha256=row["asset_sha256"])
        else:
            require(timing_only, f"approved still missing for {ident}")
            missing.append(ident)
        shots.append(shot)
        cursor = next_cursor
    require(cursor == len(tokens), "phrases omit trailing transcript words")
    for index, shot in enumerate(shots):
        shot["end"] = shots[index + 1]["start"] if index + 1 < len(shots) else end
        require(shot["start"] < shot["end"], "empty picture interval")
    return dict(schema=1, status="TIMING_ONLY" if timing_only else "OFFLINE_REVIEW_REQUIRED",
                fps=str(fps), origin_frame=origin, end_frame=end,
                audio=dict(path=str(audio_path), sha256=audio["sha256"], start=begin),
                transcript_sha256=transcript_sha, alignment_sha256=hashlib.sha256(alignment_bytes).hexdigest(),
                missing_art=missing, timing_flags=timing_flags, shots=shots, titles=titles,
                initial_picture_lead_frames=titles[0]["start"] - origin)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--timing-only", action="store_true")
    args = parser.parse_args(argv)
    try:
        require(not args.output.exists(), "choose a new output filename")
        result = plan(read_json(args.request), args.request.resolve().parent, timing_only=args.timing_only)
        with args.output.open("x", encoding="utf-8") as output:
            json.dump(result, output, ensure_ascii=False, indent=2)
            output.write("\n")
    except (OSError, ValueError, TypeError) as exc:
        print(f"Phrase conform refused: {exc}", file=sys.stderr)
        return 2
    print(result["status"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
