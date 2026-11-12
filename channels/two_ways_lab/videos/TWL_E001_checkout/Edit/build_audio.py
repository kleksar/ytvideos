"""Synthesize the retained English script locally; preserve word/sample placement."""

import hashlib
import json
import math
import os
import wave
from pathlib import Path

import numpy as np
import torch
from kokoro import KPipeline

EP = Path(__file__).resolve().parents[1]
RATE = 24_000
SPEED = 0.91
VOICE = "af_heart"


def hash_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, payload):
    path.write_text(json.dumps(payload, indent=2) + "\n")


def wav(path, samples, rate):
    with wave.open(str(path), "wb") as file:
        file.setparams((1 if samples.ndim == 1 else samples.shape[1], 2, rate, 0, "NONE", ""))
        file.writeframes(np.rint(np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes())


def tokens_for(result):
    groups, group = [], []
    for token in result.tokens:
        group.append(token)
        if token.whitespace:
            groups.append(group)
            group = []
    if group:
        groups.append(group)
    words = []
    for group in groups:
        timed = [token for token in group if token.start_ts is not None and token.end_ts is not None]
        if not timed:
            raise ValueError(f"untimed word in {result.graphemes!r}")
        words.append(("".join(token.text for token in group), timed[0].start_ts, timed[-1].end_ts))
    return words


def chime(track, time, note, duration, level, pan=0.0):
    first = round(time * RATE)
    n = min(round(duration * RATE), len(track) - first)
    t = np.arange(n) / RATE
    hz = 440 * 2 ** ((note - 69) / 12)
    a = 2 * np.pi * hz * t
    shape = np.minimum(t / .012, 1) * np.exp(-t * 5.5) * np.minimum((duration - t) / .045, 1)
    pluck = level * shape * (np.sin(a) + .23 * np.sin(a * 2.002) + .11 * np.sin(a * 3.006))
    track[first:first+n] += pluck[:, None] * np.array([1 - pan, 1 + pan])


def main():
    # Configuration and weights must already be present; the render is offline.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"
    torch.set_num_threads(3)
    pipe = KPipeline("a", repo_id="hexgrad/Kokoro-82M", device="cpu")
    script = (EP / "EPISODE.md").read_text().split("<!-- narration:en:start -->", 1)[1].split(
        "<!-- narration:en:end -->", 1)[0].strip()
    lines = script.splitlines()
    out = EP / "Source/Audio/v01"
    out.mkdir(parents=True)

    def render(text):
        result, = pipe(text, voice=VOICE, speed=SPEED, split_pattern=None)
        return result.audio.detach().cpu().numpy().copy(), tokens_for(result)

    def fade(samples, n=80):
        samples[:n] *= np.linspace(0, 1, n, endpoint=False)
        samples[-n:] *= np.linspace(1, 0, n)
        return samples

    # Synthesize the wrap as one phrase; rotate it at the onset of "two".
    seam, words = render(lines[-1] + " " + lines[0][0].lower() + lines[0][1:])
    split_index = len(lines[-1].split())
    # Cut on the estimated sample onset; the timeline is frame-aligned below.
    split = round(words[split_index][1] * RATE)
    chunks = [(seam[split:].copy(), words[split_index:], split/RATE)]
    for line in lines[1:-1]:
        signal, local = render(line)
        # Keep sentence tails, shorten leading synthesized blank consistently.
        first = max(0, round((local[0][1] - .065) * RATE))
        chunks.append((fade(signal[first:].copy()), local, first/RATE))
    # Keep the two sides of the seam un-faded, so the wave matches on replay.
    chunks.append((seam[:split].copy(), words[:split_index], 0.0))
    speech = []
    aligned = []
    line_times = []
    cursor = 0
    gaps = [.21, .22, .34, .58, .25, .48, .30, 0]
    for (samples, local, offset), line, gap in zip(chunks, lines, gaps, strict=True):
        exact = line.split()
        if [w[0].casefold() for w in local] != [w.casefold() for w in exact]:
            raise ValueError(f"Kokoro tokenization differs from transcript: {local!r}")
        start = cursor / RATE
        for ((_, a, b), label) in zip(local, exact, strict=True):
            aligned.append({
                "text": label, "start": round(start + max(0, a - offset), 6),
                "end": round(start + min(len(samples)/RATE, b - offset), 6),
            })
        line_times.append({"word_index": len(aligned)-len(exact), "start": aligned[-len(exact)]["start"]})
        speech.append(samples)
        if gap:
            speech.append(np.zeros(round(RATE * gap)))
        cursor += len(samples) + round(RATE * gap)

    # Extend the final frame by less than a frame, without inserting a beat pause.
    frames = math.ceil(cursor / (RATE/30))
    speech = np.pad(np.concatenate(speech), (0, round(frames*RATE/30)-cursor))
    speech *= .72 / np.max(np.abs(speech))
    music = np.zeros((len(speech), 2))
    sfx = np.zeros_like(music)
    # Original four-bar arpeggio, a full number of cycles within the exact loop.
    cycle_count = max(1, round(len(speech) / RATE / 8.5))
    beat = len(speech) / RATE / (cycle_count * 16)
    chords = [(48, 55, 62, 64), (45, 52, 59, 60), (41, 53, 57, 64), (43, 55, 62, 65)]
    for i in range(cycle_count*16):
        root, fifth, top, color = chords[(i//4)%4]
        chime(music, i*beat, [root, fifth, top, color][i%4], .47, .037 if i%4==0 else .026, -.21)
        chime(music, (i+.54)*beat, [top, color, fifth, top][i%4]+12, .26, .014, .31)
    # Original, synthesized checkout and result accents on the measured speech beats.
    for i in (2, 4):
        at = line_times[i]["start"]+.08
        chime(sfx, at, 91, .115, .049, -.2)
        chime(sfx, at+.12, 95, .14, .039, .2)
    for i in (3, 5):
        at = max(0, line_times[i]["start"]-.12)
        for j, note in enumerate((72, 76, 81)):
            chime(sfx, at+j*.077, note, .32, .060-j*.012, .16*(-1)**j)
    wav(out / "voice.wav", speech, RATE)
    wav(out / "music.wav", music, RATE)
    wav(out / "sfx.wav", sfx, RATE)
    mix = speech[:, None] + music + sfx
    wav(out / "mix.wav", mix, RATE)
    (out / "narration.txt").write_text(script + "\n")
    dump(out / "word_times.json", {
        "status": "MODEL_TIMING_REVIEW_REQUIRED",
        "method": "Kokoro predicted durations + exact sample placement; not human-verified alignment",
        "transcript_sha256": hashlib.sha256(script.encode()).hexdigest(),
        "audio_sha256": hash_file(out / "mix.wav"), "words": aligned,
    })
    dump(out / "timing.json", {"frames": frames, "lines": line_times, "tts_speed": SPEED})
    (out / "mix-evidence.md").write_text(
        "# TWL_E001 · local audio v01\n\n"
        "Kokoro 0.9.4, preset af_heart, English US, CPU. Upstream model snapshot "
        "f3ff3571791e39611d31c381e3a41a3af07b4987. [Model card and Apache 2.0 weights](https://huggingface.co/hexgrad/Kokoro-82M); "
        "[voice list](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md). "
        "No recording of a named person was used. This voice is a pilot choice.\n\n"
        f"Synthesis speed {SPEED}x; no time stretch or resampling in the edit (mix playback 1.0x). "
        "Narration is derived from the exact EN block in EPISODE. The start and end of the spoken loop come from one "
        "synthesized phrase split at the estimated onset of the hook. Word timings come from model duration estimates "
        "on the exact audio; the retained cue QA records independent timing limits.\n\n"
        "Music and effects are original sine partials and musical sequences generated by build_audio.py for this project. "
        "No third-party recording, sample or composition.\n\n"
        f"- Voice WAV: `{hash_file(out / 'voice.wav')}`\n"
        f"- Music WAV: `{hash_file(out / 'music.wav')}`\n"
        f"- SFX WAV: `{hash_file(out / 'sfx.wav')}`\n"
        f"- Mix PCM WAV (24 kHz stereo): `{hash_file(out / 'mix.wav')}`\n"
    )
    print(f"{frames} frames / {frames/30:.2f} seconds; mix peak {np.max(np.abs(mix)):.3f}")


if __name__ == "__main__":
    main()
