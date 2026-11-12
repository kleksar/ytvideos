#!/usr/bin/env python3
"""Build an original restrained synthetic score and mix it under the accepted VO."""
from __future__ import annotations

import hashlib
import json
import math
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
VOICE = ROOT / "Source/Voice/voice_en_speed110_v01.wav"
TIMINGS = ROOT / "Source/Voice/word_times_forced_v02.json"
OUT_DIR = ROOT / "Source/Audio"
RATE = 44_100
DURATION = 212.879660
N = round(RATE * DURATION)


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def phrase_time(words: list[dict], phrase: str, edge: str = "start") -> float:
    wanted = [w.strip(".,!?;:’'\"()[]").lower() for w in phrase.split()]
    actual = [str(w["text"]).strip(".,!?;:’'\"()[]").lower() for w in words]
    for i in range(len(actual) - len(wanted) + 1):
        if actual[i:i + len(wanted)] == wanted:
            return float(words[i]["start"] if edge == "start" else words[i + len(wanted) - 1]["end"])
    raise ValueError(f"Timing phrase not found: {phrase}")


def smooth_pulse(x: np.ndarray, hz: float, amount: float = 0.0, phase: float = 0.0) -> np.ndarray:
    return 1.0 + amount * np.sin(2 * np.pi * hz * x + phase)


def add_string_pad(dst_l: np.ndarray, dst_r: np.ndarray, start: float, end: float,
                   notes: list[float], gain: float, dissonance: float = 0.0) -> None:
    a = max(0, round(start * RATE)); b = min(N, round(end * RATE))
    if b <= a:
        return
    local = np.arange(b - a, dtype=np.float32) / RATE
    span = max(end - start, 0.01)
    fade = np.minimum(np.minimum(local / min(2.8, span / 3), (span - local) / min(3.6, span / 3)), 1.0)
    fade = np.clip(fade, 0, 1) ** 0.8
    vibrato = smooth_pulse(local, 4.2, 0.0016)
    for index, base in enumerate(notes):
        f_l = base * vibrato
        f_r = base * smooth_pulse(local, 4.05, 0.0013, 0.9)
        phase_l = 2 * np.pi * np.cumsum(f_l, dtype=np.float64) / RATE
        phase_r = 2 * np.pi * np.cumsum(f_r, dtype=np.float64) / RATE
        # A soft, slightly bowed additive tone. Keep upper partials subdued.
        tone_l = (np.sin(phase_l) + 0.20*np.sin(2*phase_l+0.2) + 0.055*np.sin(3*phase_l+0.6)
                  + 0.018*np.sin(4*phase_l+0.3))
        tone_r = (np.sin(phase_r+0.4) + 0.20*np.sin(2*phase_r+0.6) + 0.055*np.sin(3*phase_r+0.1)
                  + 0.018*np.sin(4*phase_r+0.5))
        part = gain / max(len(notes), 1)
        dst_l[a:b] += (tone_l * fade * part).astype(np.float32)
        dst_r[a:b] += (tone_r * fade * part).astype(np.float32)
    if dissonance:
        f = notes[0] * 2 ** (dissonance / 12)
        phase = 2 * np.pi * f * local
        sparse = np.sin(phase) * np.sin(np.pi * np.clip(local / span, 0, 1)) ** 1.2
        dst_l[a:b] += (sparse * gain * 0.035).astype(np.float32)
        dst_r[a:b] += (sparse * gain * 0.03).astype(np.float32)


def add_pluck(dst_l: np.ndarray, dst_r: np.ndarray, start: float, frequency: float, gain: float) -> None:
    a = max(0, round(start * RATE)); length = min(round(2.2 * RATE), N - a)
    if length <= 0:
        return
    t = np.arange(length, dtype=np.float32) / RATE
    env = np.exp(-t / 0.48) * (1 - np.exp(-t / 0.007))
    tone = np.sin(2*np.pi*frequency*t) + 0.34*np.sin(2*np.pi*frequency*2.01*t+0.15) + 0.11*np.sin(2*np.pi*frequency*3.97*t+0.6)
    dst_l[a:a+length] += (tone * env * gain * 0.34).astype(np.float32)
    dst_r[a:a+length] += (tone * env * gain * 0.27).astype(np.float32)


def read_pcm16(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as w:
        if w.getframerate() != RATE or w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise ValueError("Accepted narration must remain 44.1 kHz mono PCM16")
        frames = w.readframes(w.getnframes())
    return np.frombuffer(frames, dtype="<i2").astype(np.float32) / 32768.0


def write_wav(path: Path, audio: np.ndarray) -> None:
    pcm = np.round(np.clip(audio, -1.0, 1.0) * 32767.0).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(pcm.tobytes())


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    vo = read_pcm16(VOICE)
    if len(vo) != N:
        raise ValueError(f"Expected {N} samples, got {len(vo)}")
    alignment = json.loads(TIMINGS.read_text())
    words = alignment["words"]
    marks = {
        "opening": 0.0,
        "plot": phrase_time(words, "The group was led", "start"),
        "princess": phrase_time(words, "But the explosion was only", "start"),
        "letter": phrase_time(words, "Then a letter appeared", "start"),
        "search": phrase_time(words, "On the night before Parliament was due to open", "start"),
        "arrest": phrase_time(words, "and arrested him", "start"),
        "failed_rising": phrase_time(words, "While Fawkes was being questioned", "start"),
        "torture_order": phrase_time(words, "A royal order has survived", "start"),
        "executions": phrase_time(words, "In January 1606", "start"),
        "consequences": phrase_time(words, "The conspirators had wanted", "start"),
        "remembrance": phrase_time(words, "November 5 itself became", "start"),
        "effigy": phrase_time(words, "People began burning effigies", "start"),
        "final": phrase_time(words, "And so a man who had never led", "start"),
    }
    left = np.zeros(N, dtype=np.float32); right = np.zeros(N, dtype=np.float32)
    # The restrained harmonic palette evolves continuously. Section changes use
    # fades and sparse parts, not separate tracks or repeated per-cut accents.
    # Frequencies are pitch classes/voicings only, not claimed period instruments.
    sequence = [
        (0.0, marks["plot"], [98.0, 146.83, 196.0], 0.12, 0),
        (marks["plot"], marks["princess"], [98.0, 130.81, 155.56], 0.14, 0),
        (marks["princess"], marks["letter"], [103.83, 155.56, 196.0], 0.15, 1),
        (marks["letter"], marks["search"], [116.54, 146.83, 174.61], 0.10, 0),
        (marks["search"], marks["arrest"], [98.0, 123.47, 146.83, 155.56], 0.16, 1),
        (marks["arrest"]+0.55, marks["failed_rising"], [98.0, 130.81, 155.56], 0.075, 0),
        (marks["failed_rising"], marks["torture_order"], [87.31, 130.81, 174.61], 0.10, 1),
        (marks["torture_order"]+1.0, marks["executions"], [98.0, 146.83], 0.045, 0),
        (marks["executions"], marks["consequences"], [103.83, 138.59, 155.56], 0.085, 0),
        (marks["consequences"], marks["remembrance"], [103.83, 130.81, 155.56], 0.11, 0),
        (marks["remembrance"], marks["effigy"], [116.54, 146.83, 174.61], 0.12, 0),
        (marks["effigy"], DURATION, [103.83, 138.59, 155.56], 0.095, 0),
    ]
    for start, end, notes, gain, dissonance in sequence:
        add_string_pad(left, right, start, end, notes, gain, dissonance)
    # A quiet three-note motif: restrained at the opening, fuller at the plot,
    # then transformed and nearly gone beneath the final spoken line.
    motif = [196.0, 233.08, 293.66]
    for i, t in enumerate([4.0, 20.6, 25.4, 31.0, 38.5, 44.7, 50.0,
                           marks["remembrance"]+1.2, marks["remembrance"]+8.8,
                           marks["final"]+0.8, marks["final"]+6.2]):
        freq = motif[i % 3] * (0.89 if t >= marks["final"] else 1.0)
        add_pluck(left, right, t, freq, 0.025 if t < marks["final"] else 0.013)
    # Dampen score at the two dramatic moments named in the consultation.
    for center, halfspan, depth in [(marks["arrest"], 1.0, 0.08), (marks["torture_order"], 5.5, 0.01)]:
        a = max(0, round((center-halfspan) * RATE)); b = min(N, round((center+halfspan) * RATE))
        if b > a:
            phase = np.linspace(0, np.pi, b-a, dtype=np.float32)
            envelope = depth + (1-depth) * np.sin(phase) ** 2
            left[a:b] *= envelope; right[a:b] *= envelope
    # Calibrate score to voiced narration RMS, then lower it to the consultation
    # target and duck smoothly. Narration samples/gain are preserved unchanged.
    active = np.abs(vo) > 0.012
    speech_rms = float(np.sqrt(np.mean(vo[active] ** 2))) if np.any(active) else 0.08
    music_rms = float(np.sqrt(np.mean((left**2 + right**2) / 2)))
    target = speech_rms * (10 ** (-18 / 20))
    if music_rms > 1e-8:
        scale = target / music_rms
        left *= scale; right *= scale
    # Short-term speech detector, 80 ms RMS, 180 ms attack and 650 ms release.
    win = max(1, round(0.08 * RATE)); kernel = np.ones(win, dtype=np.float32) / win
    env = np.sqrt(np.convolve(vo**2, kernel, mode="same") + 1e-8)
    desired = np.clip(0.32 / (env + 0.06), 0.45, 1.0).astype(np.float32)
    smooth = np.empty_like(desired); smooth[0] = desired[0]
    attack = math.exp(-1/(0.16*RATE)); release = math.exp(-1/(0.65*RATE))
    for i in range(1, len(smooth)):
        coeff = attack if desired[i] < smooth[i-1] else release
        smooth[i] = coeff*smooth[i-1] + (1-coeff)*desired[i]
    left *= smooth; right *= smooth
    # Program bus: narration centered equally, original speech amplitude retained.
    mix = np.column_stack((vo + left, vo + right))
    if float(np.max(np.abs(mix))) >= 0.999:
        raise ValueError("Mix would clip; reduce music only and rebuild")
    bed_path = OUT_DIR / "music_bed_en_v01.wav"
    mix_path = OUT_DIR / "mix_en_v01.wav"
    write_wav(bed_path, np.column_stack((left, right)))
    write_wav(mix_path, mix)
    evidence = {
        "version": "v01",
        "status": "DRAFT_FOR_REVIEW",
        "duration_seconds": DURATION,
        "sample_rate_hz": RATE,
        "channels": 2,
        "voice_source": str(VOICE.relative_to(ROOT)),
        "voice_sha256": sha(VOICE),
        "voice_gain_change_db": 0,
        "alignment_source": str(TIMINGS.relative_to(ROOT)),
        "alignment_status": alignment["status"],
        "alignment_is_audibly_verified": False,
        "music_source": "Locally synthesized original layered pad and sparse plucks; no third-party samples.",
        "music_style_basis": "Source/Research/CONSULTATION_SOUND_v01.md",
        "music_rms_target_below_active_voice_db": -18,
        "music_ducking": {"window_seconds": 0.08, "attack_seconds": 0.16, "release_seconds": 0.65, "gain_range": [0.45, 1.0]},
        "story_landmarks_seconds_from_forced_alignment": marks,
        "no_sfx_added": "No licensed/acquired scene effects were available; sparse effects were left out rather than fabricated.",
        "music_bed_sha256": sha(bed_path),
        "mix_sha256": sha(mix_path),
        "music_bed_path": str(bed_path.relative_to(ROOT)),
        "mix_path": str(mix_path.relative_to(ROOT)),
        "mix_review": "No listening was available; mix remains draft pending the authorized final playback/QA stage.",
    }
    (OUT_DIR / "mix_en_v01.evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps({"mix": str(mix_path), "mix_sha256": evidence["mix_sha256"], "landmarks": marks}, indent=2))


if __name__ == "__main__":
    main()
