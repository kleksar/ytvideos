#!/usr/bin/env python3
"""Create a restrained original synth bed and additive provisional mix."""
from __future__ import annotations

import hashlib
import json
import math
import wave
from pathlib import Path

import numpy as np

EPISODE = Path(__file__).resolve().parents[2]
VOICE = EPISODE / "Source/Voice/voice_en_mix_v02.wav"
VOICE_WORDS = EPISODE / "Source/Voice/voice_en.words.json"
TRANSCRIPT = EPISODE / "Source/Voice/voice_en_text_v01.txt"
OUT = EPISODE / "Source/Audio"
RATE = 44_100
DURATION = 725.76
TOTAL = round(RATE * DURATION)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def wav_mono(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as f:
        assert f.getframerate() == RATE and f.getnchannels() == 1 and f.getsampwidth() == 2
        data = np.frombuffer(f.readframes(f.getnframes()), dtype="<i2").astype(np.float32) / 32768.0
    if len(data) != TOTAL:
        raise ValueError(f"Voice duration mismatch: {len(data) / RATE:.6f} sec")
    return data


def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def additive_tone(freq: float, t: np.ndarray, phase: float, *, triangle: bool = False) -> np.ndarray:
    p = 2.0 * np.pi * freq * t + phase
    if triangle:
        # Odd harmonics with a steep decay create a soft, non-period-instrument color.
        out = np.zeros_like(t, dtype=np.float64)
        for k in (1, 3, 5):
            out += ((-1.0) ** ((k - 1) // 2)) * np.sin(k * p) / (k * k)
        return out
    return np.sin(p) + 0.12 * np.sin(2 * p + 0.23) + 0.025 * np.sin(3 * p + 0.41)


def section_layer(start: float, end: float, components: list[tuple[float, float, bool]],
                  gain: float, pan: float = 0.0, fade: float = 12.0) -> tuple[np.ndarray, np.ndarray]:
    a = max(0, round(start * RATE))
    b = min(TOTAL, round(end * RATE))
    left = np.zeros(TOTAL, dtype=np.float32)
    right = np.zeros(TOTAL, dtype=np.float32)
    if b <= a:
        return left, right
    t = np.arange(b - a, dtype=np.float64) / RATE
    span = end - start
    fi = min(fade, span / 2)
    fo = min(fade, span / 2)
    env = smoothstep(t / max(fi, 0.01)) * smoothstep((span - t) / max(fo, 0.01))
    # Very slow, non-cyclic-in-attention movement; modulation is below 0.2 dB.
    drift = 1.0 + 0.012 * np.sin(2 * np.pi * t / 37.0 + 0.3)
    raw = np.zeros_like(t)
    for i, (hz, weight, tri) in enumerate(components):
        raw += weight * additive_tone(hz, t * drift, i * 0.31, triangle=tri)
    raw *= env * gain
    l_gain = math.sqrt((1.0 - pan) / 2.0)
    r_gain = math.sqrt((1.0 + pan) / 2.0)
    left[a:b] = (raw * l_gain).astype(np.float32)
    right[a:b] = (raw * r_gain).astype(np.float32)
    return left, right


def write_stereo(path: Path, left: np.ndarray, right: np.ndarray) -> None:
    interleaved = np.empty((TOTAL, 2), dtype="<i2")
    interleaved[:, 0] = np.round(np.clip(left, -1, 1) * 32767).astype("<i2")
    interleaved[:, 1] = np.round(np.clip(right, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(RATE)
        f.writeframes(interleaved.tobytes())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    voice = wav_mono(VOICE)
    voice_hash = sha(VOICE)
    transcript = TRANSCRIPT.read_text(encoding="utf-8").strip()
    transcript_hash = hashlib.sha256(transcript.encode("utf-8")).hexdigest()
    source_words = json.loads(VOICE_WORDS.read_text(encoding="utf-8"))["words"]
    tokens = transcript.split()
    normalized = lambda s: "".join(ch for ch in s.casefold() if ch.isalnum() or ch in "'’-")
    lexical_words = []
    token_cursor = 0
    for mapped in source_words:
        while token_cursor < len(tokens) and not any(ch.isalnum() for ch in tokens[token_cursor]):
            token_cursor += 1  # The provider map omits punctuation-only separators such as an em dash.
        if token_cursor >= len(tokens) or normalized(tokens[token_cursor]) != normalized(mapped["text"]):
            raise ValueError(f"Transcript/alignment mismatch at word {len(aligned_words)}")
        lexical_words.append({**mapped, "text": tokens[token_cursor], "token_index": token_cursor})
        token_cursor += 1
    if any(any(ch.isalnum() for ch in token) for token in tokens[token_cursor:]):
        raise ValueError("Unaligned spoken tokens remain after the provider word map")
    # Preserve the exact standalone em dash in the transcript. It occupies the
    # actual 1.04-second pause between “Tu-160” and “the” in the voice map.
    source_words = []
    lexical_by_index = {w["token_index"]: w for w in lexical_words}
    for token_index, token in enumerate(tokens):
        if token_index in lexical_by_index:
            item = lexical_by_index[token_index]
            source_words.append({k: item[k] for k in ("text", "start_seconds", "end_seconds")})
        else:
            if any(ch.isalnum() for ch in token):
                raise ValueError(f"Unaligned lexical token: {token!r}")
            previous = next((w for w in reversed(source_words) if any(ch.isalnum() for ch in w["text"])), None)
            following = next((lexical_by_index[j] for j in range(token_index + 1, len(tokens)) if j in lexical_by_index), None)
            if previous is None or following is None or float(following["start_seconds"]) <= float(previous["end_seconds"]):
                raise ValueError(f"No positive pause available for transcript punctuation token {token!r}")
            source_words.append({"text": token, "start_seconds": previous["end_seconds"],
                                 "end_seconds": following["start_seconds"]})

    # Phase boundaries use the actual narration paragraphs and the consultation's
    # seven-part arc; this preserves semantic order instead of forcing percentages.
    para_count = 86
    words_per_para = [len(p.split()) for p in transcript.split("\n\n") if p.strip()]
    if len(words_per_para) != para_count or sum(words_per_para) != len(source_words):
        raise ValueError("Unexpected narration paragraph structure")
    paragraph_starts: dict[int, float] = {}
    cursor = 0
    for pnum, count in enumerate(words_per_para, 1):
        paragraph_starts[pnum] = float(source_words[cursor]["start_seconds"])
        cursor += count
    phases = [
        (1, 19, "Cold War and strategic need", [(110.00, .34, False), (146.83, .28, False)], 0.30, -0.04),
        (19, 23, "Speed/range problem and new design", [(110.00, .24, False), (164.81, .20, True)], 0.23, 0.00),
        (23, 38, "Variable-sweep wing and mass", [(146.83, .28, False), (220.00, .18, True)], 0.24, 0.02),
        (38, 49, "NK-32, range, refuelling and altitude", [(130.81, .24, False), (164.81, .20, True), (196.00, .08, True)], 0.24, 0.04),
        (49, 65, "Cruise missiles and nuclear triad", [(98.00, .32, False), (146.83, .18, False)], 0.20, -0.03),
        (65, 79, "Vulnerability, tests and service", [(146.83, .23, False), (220.00, .10, True)], 0.18, 0.00),
        (79, para_count + 1, "Soviet collapse and aircraft fates", [(110.00, .22, False), (146.83, .11, False)], 0.15, 0.00),
    ]
    boundaries = [0.0] + [paragraph_starts[p0] for p0, _, _, _, _, _ in phases[1:]] + [DURATION]
    if any(a >= b for a, b in zip(boundaries, boundaries[1:])):
        raise ValueError(f"Non-increasing phase boundaries: {boundaries}")

    # Coherent phase beds overlap briefly at each narration-based boundary.
    l = np.zeros(TOTAL, dtype=np.float32)
    r = np.zeros(TOTAL, dtype=np.float32)
    records = []
    for i, (pstart, pend, label, comps, gain, pan) in enumerate(phases):
        start = boundaries[i]
        end = boundaries[i + 1]
        sl, sr = section_layer(start, end, comps, gain=gain, pan=pan, fade=12.0)
        l += sl
        r += sr
        records.append({"label": label, "start_seconds": round(start, 6), "end_seconds": round(end, 6),
                        "first_paragraph": pstart, "last_paragraph_exclusive": pend,
                        "components_hz_weight_triangle": comps, "synthesis_gain": gain, "pan": pan,
                        "crossfade_seconds": min(12.0, (end - start) / 2)})

    active = np.abs(voice) > 0.012
    voice_rms = float(np.sqrt(np.mean(voice[active] ** 2))) if np.any(active) else float(np.sqrt(np.mean(voice ** 2)))
    bed_rms = float(np.sqrt(np.mean((l * l + r * r) / 2.0)))
    target_rms = voice_rms * 10 ** (-24.0 / 20.0)
    if bed_rms > 0:
        l *= target_rms / bed_rms
        r *= target_rms / bed_rms

    # Tiny smooth attenuation during voice keeps the source untouched and avoids pumping.
    frame = round(0.08 * RATE)
    padded = np.pad(voice, (0, (-len(voice)) % frame))
    env_rms = np.sqrt(np.mean(padded.reshape(-1, frame) ** 2, axis=1) + 1e-9)
    wanted = np.where(env_rms > 0.012, 0.92, 1.0).astype(np.float32)
    smooth = np.empty_like(wanted)
    smooth[0] = wanted[0]
    rate_blocks = RATE / frame
    attack = math.exp(-1.0 / (0.50 * rate_blocks))
    release = math.exp(-1.0 / (1.20 * rate_blocks))
    for i in range(1, len(wanted)):
        coeff = attack if wanted[i] < smooth[i - 1] else release
        smooth[i] = coeff * smooth[i - 1] + (1 - coeff) * wanted[i]
    duck = np.interp(np.arange(TOTAL, dtype=np.float32), np.arange(len(smooth), dtype=np.float32) * frame, smooth).astype(np.float32)
    l *= duck
    r *= duck

    peak = float(max(np.max(np.abs(voice + l)), np.max(np.abs(voice + r))))
    if peak >= 0.999:
        # Preserve the accepted VO level; only reduce the new music layer if headroom is needed.
        scale = max(0.0, min(1.0, (0.998 - float(np.max(np.abs(voice)))) / max(float(np.max(np.abs(l))), float(np.max(np.abs(r))), 1e-9)))
        l *= scale
        r *= scale
        peak = float(max(np.max(np.abs(voice + l)), np.max(np.abs(voice + r))))
    if peak >= 0.999:
        raise ValueError("Voice source itself leaves insufficient unaltered headroom")

    bed_path = OUT / "music_bed_en_v01.wav"
    mix_path = OUT / "mix_en_v01.wav"
    write_stereo(bed_path, l, r)
    write_stereo(mix_path, voice + l, voice + r)
    mix_hash = sha(mix_path)
    words = [{"text": w["text"], "start": round(float(w["start_seconds"]), 6), "end": round(float(w["end_seconds"]), 6)} for w in source_words]
    word_map = {
        "status": "REVIEW_REQUIRED", "audio_sha256": mix_hash, "transcript_sha256": transcript_hash,
        "words": words,
        "source": {"voice_path": str(VOICE), "voice_sha256": voice_hash, "speed_applied_once": 1.10,
                   "alignment_path": str(EPISODE / "Source/Voice/voice_en.alignment.json"),
                   "word_timing_source": str(VOICE_WORDS), "offset_seconds": 0.0,
                   "mix_method": "additive music under unchanged centered mono VO; no VO trim, speed change, offset, or gain change",
                   "audible_sync_verified": False}
    }
    word_path = OUT / "word_map_mix_v01.json"
    word_path.write_text(json.dumps(word_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    evidence = {
        "version": "v01", "status": "DRAFT_FOR_REVIEW", "duration_seconds": DURATION,
        "sample_rate_hz": RATE, "channels": 2, "voice_source": str(VOICE), "voice_sha256": voice_hash,
        "voice_source_speed": 1.10, "speed_applied_again": False, "voice_gain_change_db": 0.0,
        "music_source": "Locally synthesized sine/triangle and additive harmonics; no third-party samples or SFX.",
        "music_score": str(EPISODE / "Research/CONSULTATION_SOUND_v01.md"),
        "music_rms_target_below_active_voice_db": -24.0, "ducking": {"maximum_reduction_db": -0.72, "attack_seconds": 0.50, "release_seconds": 1.20, "voice_unchanged": True},
        "phases": records, "sfx": "None.", "music_bed_path": str(bed_path), "music_bed_sha256": sha(bed_path),
        "mix_path": str(mix_path), "mix_sha256": mix_hash,
        "word_map_path": str(word_path), "word_map_sha256": sha(word_path),
        "transcript_path": str(TRANSCRIPT), "transcript_sha256": transcript_hash,
        "peak_linear": peak, "voice_active_rms": voice_rms,
        "audition": "UNVERIFIED; local playback unavailable in this session.",
        "pronunciation": "UNVERIFIED; no voice replacement or text change was made.",
        "audible_sync": "UNVERIFIED; word times are inherited from provider character alignment and bound to the additive mix identity."
    }
    evidence_path = OUT / "mix_en_v01.evidence.json"
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"mix": str(mix_path), "sha256": mix_hash, "music": str(bed_path), "peak": peak,
                      "voice_rms": voice_rms, "music_rms": bed_rms, "words": len(words),
                      "phase_boundaries": boundaries}, indent=2))


if __name__ == "__main__":
    main()
