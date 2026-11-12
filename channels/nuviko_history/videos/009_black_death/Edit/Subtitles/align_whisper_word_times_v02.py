#!/usr/bin/env python3
"""Align the accepted narration text to local Whisper word timestamps.

This reads the original audio-derived Whisper JSON and the existing subtitle
cue map, then writes a new word-aligned map, continuous SRT, and a screen-space
ASS track with per-word highlight overlays. It does not modify audio or Palmier.
"""
from __future__ import annotations

import difflib
import hashlib
import html
import json
import re
from pathlib import Path

EPISODE = Path(__file__).resolve().parents[2]
SUBS = EPISODE / "Edit/Subtitles"
SOURCE = EPISODE / "Source/Recovered"
INPUT_MAP = SUBS / "karaoke_v01/cue_map_candidate_v01.json"
WHISPER = EPISODE / "Work/audio_alignment_whisper_large_v3_turbo/black_death_original_audio.json"
OUTPUT = SUBS / "karaoke_v02"
OUTPUT.mkdir(parents=True, exist_ok=True)
AUDIO = SOURCE / "black_death_original_audio.m4a"
DURATION = 707.465578
FPS = 30


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(text: str) -> str:
    text = text.casefold().replace("’", "'").replace("–", "-").replace("—", "-")
    text = re.sub(r"[^\w']", "", text, flags=re.UNICODE)
    aliases = {
        "neighbour": "neighbor", "neighbours": "neighbors", "neighbouring": "neighboring",
        "recognise": "recognize", "recognised": "recognized", "travell(ed|ing)": "travel",
        "labour": "labor", "chuy": "chüy",
    }
    for pattern, value in aliases.items():
        if re.fullmatch(pattern, text):
            return value
    if text in {"travelled", "traveling", "travelling"}:
        return "travel"
    return text


def ms_time(seconds: float) -> str:
    ms = max(0, min(round(seconds * 1000), round(DURATION * 1000)))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, milli = divmod(rem, 1000)
    return f"{h:02}:{m:02}:{s:02},{milli:03}"


def ass_time(seconds: float) -> str:
    cs = max(0, min(round(seconds * 100), round(DURATION * 100)))
    h, rem = divmod(cs, 360_000)
    m, rem = divmod(rem, 6_000)
    s, centi = divmod(rem, 100)
    return f"{h}:{m:02}:{s:02}.{centi:02}"


def split_weights(words: list[str]) -> list[float]:
    # Character length is a stable low-risk proxy where Whisper grouped spoken
    # number words into one token; those spans remain explicitly marked.
    return [float(max(1, len(re.sub(r"[^A-Za-z0-9]", "", w)))) for w in words]


cue_map = json.loads(INPUT_MAP.read_text(encoding="utf-8"))
manual_words = [w["text"] for cue in cue_map["cues"] for w in cue["words"]]
whisper_data = json.loads(WHISPER.read_text(encoding="utf-8"))
whisper_words = [word for seg in whisper_data["segments"] for word in seg.get("words", [])]
# The local recognizer can hallucinate a short tail after the actual file ends.
whisper_words = [w for w in whisper_words if float(w["start"]) < DURATION]

manual_norm = [norm(w) for w in manual_words]
whisper_norm = [norm(w["word"]) for w in whisper_words]
matcher = difflib.SequenceMatcher(a=manual_norm, b=whisper_norm, autojunk=False)
aligned: list[dict | None] = [None] * len(manual_words)
reconciliations = []
unmatched = []

for tag, i1, i2, j1, j2 in matcher.get_opcodes():
    if tag == "equal":
        for mi, wi in zip(range(i1, i2), range(j1, j2)):
            aligned[mi] = {
                "text": manual_words[mi], "start": float(whisper_words[wi]["start"]),
                "end": float(whisper_words[wi]["end"]), "source_word": whisper_words[wi]["word"],
                "timing_source": "local_whisper_large_v3_turbo_word_timestamp",
                "mapping": "normalized_exact_token",
            }
        continue
    if tag == "delete":
        unmatched.append({"kind": "manual_missing_in_whisper", "manual": manual_words[i1:i2]})
        continue
    if tag == "insert":
        # Extra Whisper words after the last source-caption word are ignored;
        # any insertion inside the narration is reported for review.
        if i1 < len(manual_words):
            unmatched.append({"kind": "whisper_extra_inside_narration", "manual_index": i1,
                              "whisper": [w["word"] for w in whisper_words[j1:j2]]})
        continue
    if tag == "replace":
        mwords = manual_words[i1:i2]
        wwords = whisper_words[j1:j2]
        if not mwords or not wwords:
            unmatched.append({"kind": "unmapped_replace", "manual": mwords,
                              "whisper": [w["word"] for w in wwords]})
            continue
        start = min(float(w["start"]) for w in wwords)
        end = max(float(w["end"]) for w in wwords)
        weights = split_weights(mwords)
        total = sum(weights)
        cursor = start
        for k, (mi, word, weight) in enumerate(zip(range(i1, i2), mwords, weights)):
            next_cursor = end if k == len(mwords) - 1 else cursor + (end - start) * weight / total
            aligned[mi] = {
                "text": word, "start": cursor, "end": next_cursor,
                "source_word": " ".join(w["word"].strip() for w in wwords),
                "timing_source": "local_whisper_large_v3_turbo_word_timestamp",
                "mapping": "reconciled_span_weighted_by_written_length",
            }
            cursor = next_cursor
        reconciliations.append({"manual_range": [i1, i2], "whisper_range": [j1, j2],
                                "manual": mwords, "whisper": [w["word"] for w in wwords],
                                "mapping": "proportional_span_reconciliation"})

if unmatched or any(w is None for w in aligned):
    raise SystemExit(json.dumps({"unmatched": unmatched,
                                 "unmapped_indices": [i for i, w in enumerate(aligned) if w is None]},
                                ensure_ascii=False, indent=2))

# Keep timestamps monotone and inside the original unchanged audio duration.
for i, word in enumerate(aligned):
    assert word is not None
    word["start"] = max(0.0, min(float(word["start"]), DURATION))
    word["end"] = max(word["start"] + 0.015, min(float(word["end"]), DURATION))
    if i and word["start"] < aligned[i - 1]["start"]:
        raise SystemExit(f"non-monotone word timing at index {i}: {word}")

new_cues = []
word_i = 0
for i, old in enumerate(cue_map["cues"]):
    words = aligned[word_i:word_i + len(old["words"])]
    if len(words) != len(old["words"]):
        raise SystemExit(f"cue word count mismatch at {old['cue_id']}")
    start = words[0]["start"]
    spoken_end = words[-1]["end"]
    display_end = aligned[word_i + len(words)]["start"] if word_i + len(words) < len(aligned) else DURATION
    if display_end <= start:
        raise SystemExit(f"non-positive cue span {old['cue_id']}")
    new_cues.append({**old, "start": start, "spoken_end": spoken_end,
                     "display_start": start, "display_end": display_end, "words": words,
                     "text": " ".join(w["text"] for w in words)})
    word_i += len(words)

ass_escape = lambda s: s.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")
header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Georgia,62,&H00272D30,&H002C8AC2,&H00272D30,&H00F3E9D5,1,0,0,0,100,100,0,0,3,16,0,5,120,120,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
events = []
for cue in new_cues:
    phrase = [w["text"] for w in cue["words"]]
    full = ass_escape(" ".join(phrase))
    base_line = r"{\an5\pos(960,990)}" + full
    events.append(f"Dialogue: 0,{ass_time(cue['display_start'])},{ass_time(cue['display_end'])},Default,,0,0,0,,{base_line}")
    for wi, word in enumerate(cue["words"]):
        start, end = word["start"], word["end"]
        if end - start < 0.02:
            continue
        pieces = []
        for j, token in enumerate(phrase):
            color = r"\1c&H002C8AC2&" if j == wi else r"\1c&H00272D30&"
            pieces.append("{" + color + "}" + ass_escape(token))
        line = r"{\an5\pos(960,990)}" + " ".join(pieces)
        events.append(f"Dialogue: 1,{ass_time(start)},{ass_time(end)},Default,,0,0,0,,{line}")

ass_text = header + "\n".join(events) + "\n"
ass_path = OUTPUT / "black_death_en_word_highlight_v02.ass"
ass_path.write_text(ass_text, encoding="utf-8")

srt_rows = []
for i, cue in enumerate(new_cues, 1):
    srt_rows.append(f"{i}\n{ms_time(cue['display_start'])} --> {ms_time(cue['display_end'])}\n{cue['text']}\n")
srt_path = OUTPUT / "black_death_en_continuous_v02.srt"
srt_path.write_text("\n".join(srt_rows), encoding="utf-8")

result = {
    "version": "nuviko-black-death-s01-karaoke-v02",
    "status": "WHISPER_WORD_TIMING_RECONCILED_REQUIRES_COMPOSITE_REVIEW",
    "language": "en", "source_audio": str(AUDIO.relative_to(EPISODE)),
    "source_audio_sha256": sha(AUDIO), "audio_duration_seconds": DURATION,
    "timing_model": str(WHISPER.relative_to(EPISODE)), "timing_model_sha256": sha(WHISPER),
    "text_source": cue_map["source_transcript"], "text_sha256": cue_map["transcript_sha256"],
    "canvas": [1920, 1080], "fps": FPS,
    "style": {"reference": cue_map["style"]["reference"], "font": "Georgia Bold",
              "font_size_px": 62, "center_x": 960, "center_y": 990,
              "panel_fill": "#F3E9D5", "neutral_text": "#302D27",
              "active_text": "#C28A2C", "active_word_only": True},
    "continuity": "Base subtitle phrases stay continuously visible through the next phrase start; word highlights overlay only during spoken word timing.",
    "word_count": len(aligned), "cue_count": len(new_cues),
    "reconciliations": reconciliations,
    "limitations": [
        "Whisper supplies local word timestamps; spelling and phrase text remain from the recovered creator caption track.",
        "Words grouped into one Whisper token (notably spoken number phrases) are split proportionally by written length and are approximate.",
        "Subtitle line wrapping has not yet been checked on the rendered composite.",
    ],
    "outputs": {"srt": srt_path.name, "ass": ass_path.name},
    "cues": new_cues,
}
map_path = OUTPUT / "cue_map_candidate_v02.json"
map_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
summary = {"status": result["status"], "manual_words": len(manual_words),
           "whisper_words_used": len(whisper_words), "cues": len(new_cues),
           "reconciliations": reconciliations, "unmatched": unmatched,
           "duration": DURATION, "srt_sha256": sha(srt_path), "ass_sha256": sha(ass_path)}
(OUTPUT / "alignment_report_v02.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: summary[k] for k in ("status", "manual_words", "whisper_words_used", "cues", "reconciliations", "unmatched", "duration")}, ensure_ascii=False, indent=2))
