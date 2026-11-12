#!/usr/bin/env python3
"""Build the 007 v04 stereo narration + one paper gesture mix from source audio."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

EPISODE = Path(__file__).resolve().parents[2]
SOUND = EPISODE / "Edit" / "Sound"
VOICE = EPISODE / "Source" / "Voice" / "lawrence_v3" / "voice_en.mp3"
FOLEY = EPISODE / "Source" / "Audio" / "book-page-02.wav"
OUTPUT = SOUND / "007_joshua_jessica_stereo_mix_v04.wav"
RECEIPT = SOUND / "007_joshua_jessica_stereo_mix_v04_receipt.json"

FILTER = (
    "[0:a]aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[voice];"
    "[1:a]atrim=0:0.7,asetpts=PTS-STARTPTS,"
    "volume='if(lt(t,0.566666667),0.0630957344,"
    "if(lt(t,0.666666667),0.0630957344*pow(10,-18*(t-0.566666667)),0.001))':eval=frame,"
    "adelay=34267|34267[page];"
    "[voice][page]amix=inputs=2:duration=first:normalize=0:dropout_transition=0,"
    "loudnorm=I=-22:TP=-2:LRA=3:print_format=json[mix]"
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    if not VOICE.is_file() or not FOLEY.is_file():
        raise RuntimeError("Required original voice or CC0 page sound is missing")
    if OUTPUT.exists() or RECEIPT.exists():
        raise RuntimeError("v04 mix output/receipt already exists; inspect before retrying")

    args = [
        "ffmpeg", "-hide_banner", "-nostdin", "-n", "-i", str(VOICE), "-i", str(FOLEY),
        "-filter_complex", FILTER, "-map", "[mix]", "-ar", "44100", "-ac", "2",
        "-c:a", "pcm_s24le", str(OUTPUT),
    ]
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f"ffmpeg mix failed: {proc.stderr[-4000:]}")

    probe = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_name,codec_type,sample_rate,channels,channel_layout,duration,bit_rate",
        "-show_entries", "format=duration,size", "-of", "json", str(OUTPUT),
    ], check=True, capture_output=True, text=True)
    receipt = {
        "version": 1,
        "status": "built_pending_measurement_and_remux",
        "voice": str(VOICE),
        "foley": str(FOLEY),
        "output": str(OUTPUT),
        "output_sha256": sha256(OUTPUT),
        "ffmpeg_args": args,
        "loudnorm_measurements": proc.stderr[-2000:],
        "ffprobe": json.loads(probe.stdout),
        "placement": {"sfx_start_frame": 1028, "sfx_start_seconds": 1028 / 30,
                      "sfx_timeline_frames": [1028, 1049], "sfx_trim_seconds": 0.7,
                      "gain": "-24 dB through frame 17, logarithmic dB keyframe fade to -60 dB at frame 20",
                      "voice_preserved_at_original_timing": True},
        "target_loudness_lufs": -22,
        "true_peak_limit_dbtp": -2,
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("status", "output", "output_sha256", "ffprobe", "loudnorm_measurements")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
