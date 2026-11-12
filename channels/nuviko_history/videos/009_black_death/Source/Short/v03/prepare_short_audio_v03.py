#!/usr/bin/env python3
"""Create the authorized Short audio derivative with one 1.10x pass."""
import hashlib, json, subprocess
from pathlib import Path
ROOT = Path("/Users/diplomat/ytvideos/channels/nuviko_history/videos/009_black_death")
SOURCE_MAP = ROOT / "Source/Short/v01/word_times_v01.json"
SOURCE_AUDIO = ROOT / "Source/Short/v01/black_death_short_mix_v01.wav"
OUTPUT_DIR = ROOT / "Source/Short/v03"
OUTPUT_AUDIO = OUTPUT_DIR / "black_death_short_mix_v03.wav"
OUTPUT_MAP = OUTPUT_DIR / "word_times_v03.json"
OUTPUT_TEXT = OUTPUT_DIR / "SHORT_TEXT_EN_v03.txt"
SPEED = 1.10
for path in (OUTPUT_AUDIO, OUTPUT_MAP, OUTPUT_TEXT):
    if path.exists():
        raise SystemExit(f"refusing overwrite: {path}")
source_map = json.loads(SOURCE_MAP.read_text())
if source_map["status"] != "PROVISIONAL_REQUIRES_AUDIBLE_ALIGNMENT_REVIEW":
    raise SystemExit("unexpected word-map review state")
cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-n", "-i", str(SOURCE_AUDIO),
       "-af", "atempo=1.10", "-ar", "44100", "-ac", "2", "-c:a", "pcm_s24le", str(OUTPUT_AUDIO)]
subprocess.run(cmd, check=True)
words=[]
for word in source_map["words"]:
    row=dict(word)
    row["start"] = round(word["start"] / SPEED, 6)
    row["end"] = round(word["end"] / SPEED, 6)
    row["timing_source"] = "youtube_auto_caption_word_marker; edit_time_divided_by_1.10_once"
    words.append(row)
segments=[]
for seg in source_map["segments"]:
    item=dict(seg)
    item["output_in"] = round(seg["output_in"] / SPEED, 6)
    item["duration"] = round(seg["duration"] / SPEED, 6)
    segments.append(item)
payload = {
  "status": "PROVISIONAL_REQUIRES_AUDIBLE_ALIGNMENT_REVIEW",
  "source_audio": str(SOURCE_AUDIO),
  "source_audio_sha256": hashlib.sha256(SOURCE_AUDIO.read_bytes()).hexdigest(),
  "source_alignment": source_map["source_alignment"],
  "source_alignment_status": source_map["source_alignment_status"],
  "source_vtt_sha256": source_map["source_vtt_sha256"],
  "edit_audio": str(OUTPUT_AUDIO),
  "source_word_map": str(SOURCE_MAP),
  "source_word_map_sha256": hashlib.sha256(SOURCE_MAP.read_bytes()).hexdigest(),
  "applied_speed": SPEED,
  "speed_application_count": 1,
  "timing_conform": "divide source edit word times by 1.10 exactly once",
  "segments": segments,
  "expected_duration_seconds": round(source_map["expected_duration_seconds"] / SPEED, 6),
  "words": words,
  "alignment_review": "Automatic caption word markers; audible synchronization not verified."
}
OUTPUT_MAP.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n")
text=" ".join(w["text"] for w in source_map["words"])
OUTPUT_TEXT.write_text(text+"\n")
print(json.dumps({"audio":str(OUTPUT_AUDIO),"expected_duration":payload["expected_duration_seconds"],"words":len(words),"speed":SPEED,"applications":1},indent=2))
