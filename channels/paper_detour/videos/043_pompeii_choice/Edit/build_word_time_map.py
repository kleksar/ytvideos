#!/usr/bin/env python3
"""Adapt the retained narration alignment to the montage renderer schema."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT = ROOT / "Source/Script/narration_en_v05_tts.txt"
MAP = ROOT / "Source/Voice/en_v05_lawrence/word_timings_v01.json"
OUT = Path(__file__).resolve().parent / "word_times_v04.json"

text = TEXT.read_text(encoding="utf-8")
source = json.loads(MAP.read_text(encoding="utf-8"))
matches = list(re.finditer(r"[\w]+(?:['’][\w]+)*", text, flags=re.UNICODE))
timings = source["words"]
if len(matches) != len(timings):
    raise SystemExit(f"spoken token count {len(matches)} != alignment count {len(timings)}")

words = []
for index, (match, timing) in enumerate(zip(matches, timings)):
    token = match.group(0)
    if re.sub(r"\W", "", token).casefold() != re.sub(r"\W", "", timing["text"]).casefold():
        raise SystemExit(f"token mismatch at {index + 1}: {token!r} / {timing['text']!r}")
    next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
    gap = text[match.end():next_start]
    punctuation = next((ch for ch in gap if ch in ".,?!:;"), "")
    if not punctuation and "—" in gap:
        punctuation = ","
    words.append({"text": token + punctuation, "start": timing["start_seconds"], "end": timing["end_seconds"]})

OUT.write_text(json.dumps({
    "version": 1,
    "source_tts_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    "source_alignment": "../Source/Voice/en_v05_lawrence/word_timings_v01.json",
    "alignment_field": source.get("alignment_field"),
    "review_required": "Timing is an automatic draft; auditory sync has not been verified.",
    "words": words,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"WROTE {OUT} ({len(words)} spoken tokens)")
