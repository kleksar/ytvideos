#!/usr/bin/env python3
"""Create an original, quiet synthetic score and mix it under the accepted VO."""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import wave
from pathlib import Path

import numpy as np

EP = Path(__file__).resolve().parents[2]
ROOT = EP.parents[3]
VOICE_MP3 = EP / "Source/Voice/v02/voice_en.mp3"
ALIGNMENT = EP / "Source/Voice/v02/voice_en.alignment.json"
REQUEST = EP / "Source/Voice/v02/voice_en.request.json"
OUT = EP / "Source/Audio"
RATE = 44_100
DURATION = 612.320
N = round(RATE * DURATION)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_voice(path: Path) -> np.ndarray:
    raw = subprocess.check_output([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(path),
        "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", str(RATE), "-"
    ])
    voice = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if len(voice) != N:
        raise ValueError(f"Voice sample count {len(voice)} differs from expected {N}")
    return voice


def write_stereo(path: Path, left: np.ndarray, right: np.ndarray) -> None:
    interleaved = np.empty((N, 2), dtype="<i2")
    interleaved[:, 0] = np.round(np.clip(left, -1.0, 1.0) * 32767).astype("<i2")
    interleaved[:, 1] = np.round(np.clip(right, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as stream:
        stream.setnchannels(2)
        stream.setsampwidth(2)
        stream.setframerate(RATE)
        stream.writeframes(interleaved.tobytes())


def add_pad(left: np.ndarray, right: np.ndarray, start: float, end: float,
            notes: list[float], gain: float, *, low_drone: bool = False) -> None:
    a = max(0, round(start * RATE))
    b = min(N, round(end * RATE))
    if b <= a:
        return
    local = np.arange(b - a, dtype=np.float64) / RATE
    span = max(end - start, 0.01)
    fade_in = min(4.0, span / 3)
    fade_out = min(5.0, span / 3)
    env = np.minimum(np.minimum(local / fade_in, (span - local) / fade_out), 1.0)
    env = np.clip(env, 0.0, 1.0) ** 0.9
    vibrato_l = 1.0 + 0.0010 * np.sin(2 * np.pi * 4.1 * local)
    vibrato_r = 1.0 + 0.0008 * np.sin(2 * np.pi * 4.0 * local + 0.8)
    for i, hz in enumerate(notes):
        phase_l = 2 * np.pi * np.cumsum(hz * vibrato_l, dtype=np.float64) / RATE
        phase_r = 2 * np.pi * np.cumsum(hz * vibrato_r, dtype=np.float64) / RATE + 0.31
        if low_drone:
            l = np.sin(phase_l) + 0.11 * np.sin(2 * phase_l + 0.16)
            r = np.sin(phase_r) + 0.11 * np.sin(2 * phase_r + 0.2)
        else:
            # A soft synthetic string color. It does not imitate a period instrument.
            l = np.sin(phase_l) + 0.16 * np.sin(2 * phase_l + 0.2) + 0.025 * np.sin(3 * phase_l + 0.4)
            r = np.sin(phase_r) + 0.16 * np.sin(2 * phase_r + 0.25) + 0.025 * np.sin(3 * phase_r + 0.3)
        scale = gain / max(1, len(notes))
        left[a:b] += (l * env * scale).astype(np.float32)
        right[a:b] += (r * env * scale).astype(np.float32)


def apply_soft_window(env: np.ndarray, start: float, end: float, depth: float, ramp: float = 0.9) -> None:
    a = max(0, round(start * RATE)); b = min(N, round(end * RATE))
    if b > a:
        env[a:b] *= depth
    la = max(0, round((start - ramp) * RATE)); lb = min(N, round(start * RATE))
    if lb > la:
        u = np.arange(lb - la, dtype=np.float32) / max(1, lb - la)
        env[la:lb] *= 1 - (1 - depth) * (0.5 - 0.5 * np.cos(np.pi * u))
    ra = max(0, round(end * RATE)); rb = min(N, round((end + ramp) * RATE))
    if rb > ra:
        u = np.arange(rb - ra, dtype=np.float32) / max(1, rb - ra)
        env[ra:rb] *= depth + (1 - depth) * (0.5 - 0.5 * np.cos(np.pi * u))


def make_word_map(text: str, alignment_data: dict, audio_hash: str, transcript_hash: str) -> dict:
    source = alignment_data["alignment"]
    chars = "".join(source["characters"])
    if chars != text:
        raise ValueError("Character alignment differs from accepted transcript")
    starts = source["character_start_times_seconds"]
    ends = source["character_end_times_seconds"]
    words = []
    cursor = 0
    for token in text.split():
        pos = text.find(token, cursor)
        if pos < 0:
            raise ValueError(f"Cannot locate transcript token {token!r}")
        last = pos + len(token) - 1
        start = float(starts[pos])
        end = min(DURATION, float(ends[last]))
        if start >= DURATION or end <= start:
            raise ValueError(f"Invalid aligned word interval for {token!r}: {start}, {end}")
        words.append({"text": token, "start": round(start, 6), "end": round(end, 6)})
        cursor = last + 1
    return {"status": "REVIEW_REQUIRED", "audio_sha256": audio_hash,
            "transcript_sha256": transcript_hash, "words": words,
            "source": "ElevenLabs character alignment, clamped at measured MP3 duration 612.320 s",
            "audible_sync_verified": False}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    voice = read_voice(VOICE_MP3)
    voice_hash = sha(VOICE_MP3)
    request = json.loads(REQUEST.read_text(encoding="utf-8"))
    if request.get("status") != "success" or request.get("audio_sha256") != voice_hash or request.get("speed") != 1.1:
        raise ValueError("Voice receipt does not bind this 1.10x source MP3")
    narration = (EP / "Source/Script/narration_en_v01.md").read_text(encoding="utf-8").strip()
    alignment = json.loads(ALIGNMENT.read_text(encoding="utf-8"))
    transcript_hash = hashlib.sha256(narration.encode("utf-8")).hexdigest()
    words = make_word_map(narration, alignment, voice_hash, transcript_hash)
    (OUT / "transcript_en_v01.txt").write_text(narration + "\n", encoding="utf-8")
    (OUT / "word_map_voice_v02.json").write_text(json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    left = np.zeros(N, dtype=np.float32)
    right = np.zeros(N, dtype=np.float32)
    # Eight restrained phases follow the accepted shot-map's scene boundaries.
    phases = [
        (0.000, 54.320, [73.42, 110.00, 146.83], 0.050, True),
        (54.320, 202.640, [65.41, 98.00, 130.81, 164.81], 0.075, False),
        (202.640, 282.853, [73.42, 110.00, 146.83], 0.038, False),
        (282.853, 364.400, [65.41, 98.00, 123.47], 0.055, True),
        (364.400, 461.040, [73.42, 110.00], 0.030, True),
        (461.040, 520.560, [73.42, 110.00, 146.83], 0.045, True),
        (520.560, 555.280, [65.41, 98.00], 0.027, True),
        (555.280, 612.320, [73.42, 110.00], 0.018, True),
    ]
    for start, end, notes, gain, low in phases:
        add_pad(left, right, start, end, notes, gain, low_drone=low)

    # Quietly let the upper layer breathe under narration; leave emphasized
    # chronology, statistics and final quotation almost completely bare.
    masks = [
        (25.387, 36.720, 0.12),  # Schlieper quotation
        (227.000, 282.853, 0.18),  # thirst, wounded people and the memorial
        (328.600, 364.400, 0.20),  # collapse of the Citadel positions
        (374.000, 390.400, 0.24),  # end-of-June / July distinction
        (416.000, 442.520, 0.18),  # July 23 and the capture account
        (502.280, 520.560, 0.16),  # 453 / 668 and their scope
        (584.000, 603.920, 0.10),  # unknown author and limits
        (603.920, 612.320, 0.0),  # final repeated quotation in silence
    ]
    envelope = np.ones(N, dtype=np.float32)
    for start, end, depth in masks:
        apply_soft_window(envelope, start, end, depth)
    left *= envelope
    right *= envelope

    active = np.abs(voice) > 0.012
    voice_rms = float(np.sqrt(np.mean(voice[active] ** 2))) if np.any(active) else 0.08
    music_rms = float(np.sqrt(np.mean((left ** 2 + right ** 2) / 2)))
    target_rms = voice_rms * 10 ** (-24 / 20)
    if music_rms > 1e-9:
        left *= target_rms / music_rms
        right *= target_rms / music_rms

    # Gentle voice detector: music can fall by at most another 7 dB; VO is unchanged.
    block = round(0.08 * RATE)
    padded = np.pad(voice, (0, (-len(voice)) % block))
    rms = np.sqrt(np.mean(padded.reshape(-1, block) ** 2, axis=1) + 1e-8)
    wanted = np.clip(0.32 / (rms + 0.06), 0.45, 1.0).astype(np.float32)
    block_rate = RATE / block
    duck_blocks = np.empty_like(wanted)
    duck_blocks[0] = wanted[0]
    attack = math.exp(-1 / (0.16 * block_rate))
    release = math.exp(-1 / (0.65 * block_rate))
    for i in range(1, len(duck_blocks)):
        coeff = attack if wanted[i] < duck_blocks[i - 1] else release
        duck_blocks[i] = coeff * duck_blocks[i - 1] + (1 - coeff) * wanted[i]
    duck = np.interp(np.arange(N, dtype=np.float32),
                     (np.arange(len(duck_blocks), dtype=np.float32) * block).clip(max=N - 1),
                     duck_blocks).astype(np.float32)
    left *= duck
    right *= duck

    mix_l = voice + left
    mix_r = voice + right
    peak = float(max(np.max(np.abs(mix_l)), np.max(np.abs(mix_r))))
    if peak >= 0.999:
        raise ValueError(f"Mix peak {peak:.6f} would clip")
    bed_path = OUT / "music_bed_en_v01.wav"
    mix_path = OUT / "mix_en_v01.wav"
    write_stereo(bed_path, left, right)
    write_stereo(mix_path, mix_l, mix_r)
    evidence = {
        "version": "v01", "status": "DRAFT_FOR_USER_REVIEW",
        "duration_seconds": DURATION, "sample_rate_hz": RATE, "channels": 2,
        "voice_source": str(VOICE_MP3.relative_to(EP)), "voice_sha256": voice_hash,
        "voice_source_speed": 1.10, "speed_applied_again": False,
        "voice_gain_change_db": 0,
        "alignment_source": str(ALIGNMENT.relative_to(EP)),
        "alignment_is_audibly_verified": False,
        "music_source": "Locally synthesized original low drone and soft string-like additive tones; no third-party samples.",
        "music_score": "Research/CONSULTATION_SOUND_v01.md",
        "music_rms_target_below_active_voice_db": -24,
        "ducking": {"window_seconds": 0.08, "attack_seconds": 0.16, "release_seconds": 0.65, "gain_range": [0.45, 1.0]},
        "phase_boundaries_seconds": [p[0] for p in phases] + [DURATION],
        "emphasis_reduction_windows": masks,
        "sfx": "None; no event-specific sound effects were created.",
        "music_bed_sha256": sha(bed_path), "mix_sha256": sha(mix_path),
        "music_bed_path": str(bed_path.relative_to(EP)), "mix_path": str(mix_path.relative_to(EP)),
        "peak_linear": peak,
        "listening_review": "Not performed in this build step; human playback remains unverified.",
    }
    (OUT / "mix_en_v01.evidence.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"mix": str(mix_path), "sha256": evidence["mix_sha256"], "peak": peak,
                      "voice_rms": voice_rms, "music_rms_after_masks_before_duck": music_rms,
                      "words": len(words["words"])}, indent=2))


if __name__ == "__main__":
    main()
