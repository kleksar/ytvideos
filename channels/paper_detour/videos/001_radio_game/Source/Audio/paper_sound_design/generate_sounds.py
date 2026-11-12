#!/usr/bin/env python3
"""Original sample-free synthetic sketches for the Rarovista edit.

No outside recordings, loops or melody are used.  These sounds are working
materials and must be auditioned and mixed before treating them as final.
"""
import math
from pathlib import Path
import wave

import numpy as np

HERE = Path(__file__).resolve().parent
RATE = 44100
RNG = np.random.default_rng(42001)


def save(name, stereo):
    stereo = np.clip(stereo, -0.99, 0.99)
    pcm = np.asarray(stereo * 32767, dtype='<i2').tobytes()
    with wave.open(str(HERE / name), 'wb') as out:
        out.setnchannels(2)
        out.setsampwidth(2)
        out.setframerate(RATE)
        out.writeframes(pcm)


def fade(t, duration, attack, release):
    return np.minimum(np.minimum(t / attack, (duration - t) / release), 1).clip(0, 1)


def lowpass(samples, width):
    # Running average via cumulative sum; efficient even for long clips.
    padded = np.pad(samples, (width, 0))
    sums = np.cumsum(padded, dtype=np.float64)
    return (sums[width:] - sums[:-width]) / width


def music_bed():
    duration = 56.0
    t = np.arange(round(RATE * duration)) / RATE
    left = np.zeros_like(t)
    right = np.zeros_like(t)
    # Different softly blended voicings of C minor, Ab major, Eb major, Bb major.
    chords = [[130.81, 155.56, 196.00], [103.83, 155.56, 207.65],
              [116.54, 155.56, 196.00], [116.54, 146.83, 174.61]]
    for i, chord in enumerate(chords * 2):
        start = 7.0 * i
        local = t - start
        env = (np.sin(np.pi * np.clip(local / 7, 0, 1)) ** 0.7)
        env *= (local >= 0) & (local < 7)
        for j, fundamental in enumerate(chord):
            phase = 0.45 * (i + j)
            for dest, detune in [(left, -0.001), (right, 0.001)]:
                f = fundamental * (1 + detune)
                signal = (np.sin(2 * np.pi * f * t + phase)
                          + 0.16 * np.sin(2 * np.pi * (2*f) * t + phase)
                          + 0.05 * np.sin(2 * np.pi * (3*f) * t + phase))
                dest += 0.014 * env * signal
    # Sparse glock-like notes; all locally synthesized, never copied from audio.
    melody = [261.63, 311.13, 392.0, 311.13, 207.65, 261.63, 311.13, 392.0]
    for i in range(32):
        start = 0.8 + i * 1.68
        local = t - start
        env = np.exp(-np.maximum(local, 0) / 0.72) * (local >= 0) * (local < 4)
        env *= np.minimum(np.maximum(local, 0) / .045, 1)
        freq = melody[(i * 3 + i // 8) % len(melody)]
        note = env * (np.sin(2*np.pi*freq*local) + 0.23*np.sin(2*np.pi*freq*2.01*local))
        left += note * (0.010 if i % 2 else 0.007)
        right += note * (0.007 if i % 2 else 0.010)
    envelope = fade(t, duration, 1.2, 2.0)
    save('music_bed_56s_synth_stereo.wav', np.column_stack((left*envelope, right*envelope)))


def record_button():
    duration = .56
    t = np.arange(round(RATE * duration)) / RATE
    noise = RNG.standard_normal(t.size)
    click = noise * np.exp(-t*75) * 0.08
    mech = (np.sin(2*np.pi*680*t) + .4*np.sin(2*np.pi*1160*t)) * np.exp(-t*32) * .045
    clunk = np.sin(2*np.pi*(165*t - 90*t*t)) * np.exp(-t*16) * .12
    stereo = np.column_stack((click + mech + clunk, click + mech*.85 + clunk))
    save('sfx_button_click_synth.wav', stereo * fade(t, duration, .002, .1)[:, None])


def cassette_motor():
    duration = 5.0
    t = np.arange(round(RATE * duration)) / RATE
    low_noise = lowpass(RNG.standard_normal(t.size), 140)
    rumble = .055 * np.sin(2*np.pi*64*t + .12*np.sin(2*np.pi*2.1*t))
    motor = .035 * np.sin(2*np.pi*128*t) + rumble + low_noise * .22
    flutter = 1 + .10*np.sin(2*np.pi*1.7*t)
    env = fade(t, duration, .25, .45)
    save('sfx_tape_motor_synth_5s.wav', np.column_stack((motor, motor*.94)) * (flutter*env)[:, None])


def signal_tone():
    duration = 1.8
    t = np.arange(round(RATE * duration)) / RATE
    f = 530 + 620 * t/duration + 45*np.sin(2*np.pi*4*t)
    phase = 2*np.pi*np.cumsum(f)/RATE
    hiss = lowpass(RNG.standard_normal(t.size), 8)*.025
    tone = .055*np.sin(phase) + hiss
    env = fade(t, duration, .1, .2)
    save('sfx_radio_search_synth_1_8s.wav', np.column_stack((tone, tone*.90)) * env[:, None])


if __name__ == '__main__':
    music_bed()
    record_button()
    cassette_motor()
    signal_tone()
