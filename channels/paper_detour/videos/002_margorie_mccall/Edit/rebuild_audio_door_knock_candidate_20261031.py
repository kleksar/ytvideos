#!/usr/bin/env python3
"""Rebuild a provisional PCM mix for the saved 002 timeline; does not touch MP4.

Time stretch, fade curves and mono panning are approximations until compared
against the actual Palmier export. Refuses changed receipt or source bytes.
"""
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np

BASE = Path('/Users/diplomat/ytvideos/channels/paper_detour/videos')
EPISODE = BASE / '002_margorie_mccall'
RECEIPT = EPISODE / 'Edit/palmier_door_knock_receipt.json'
OUT = EPISODE / 'Edit/full_mix_door_knock_candidate_20261031_pcm24.wav'
EXPECTED_RECEIPT = 'db7bba0249f39936469806d2dff244cb452b43a5e38773009b3871ec96069730'
SOURCES = {
    '299695C7': (EPISODE / 'Source/Voice/voice_en_lawrence_1x.wav', '2bd8fe081358a8db4e4bec01c6d674ec064cc022d5893e641d066adce9cbd2ff', 1),
    '58DBC196': (BASE / '001_radio_game/Source/Audio/paper_sound_design/music_bed_continuous_260s.wav', '969f439f7b890113191416fc2213289b576a88ef1864bfa119aff2f0605bf9c5', 2),
    'EF90746D': (BASE / '001_radio_game/Source/Audio/paper_motion_cc0_20261030/book-page-02.wav', 'b14e15141984eb84bcbe8841139d3f1d4715eac4e64cf52091acffd8fe440331', 2),
    '56897AF5': (EPISODE / 'Source/Audio/door_knock_cc0_351144/triple_knock_preview_hq.mp3', '1e75295fadb9ab35e9019bae13df7e89c6e334758902cffda4a284637756e219', 2),
}
RATE = 44100
FPS = 30
SAMPLES_PER_FRAME = RATE // FPS
FRAMES = 2296


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def decode(path, channels, speed=1.0):
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0']
    if speed != 1.0:
        cmd += ['-af', f'atempo={speed}']
    cmd += ['-ar', str(RATE), '-ac', str(channels), '-f', 'f32le', 'pipe:1']
    data = subprocess.run(cmd, check=True, stdout=subprocess.PIPE).stdout
    samples = np.frombuffer(data, dtype='<f4').reshape(-1, channels)
    return np.repeat(samples, 2, axis=1) if channels == 1 else samples


def main():
    if OUT.exists():
        raise SystemExit(f'Refusing to overwrite {OUT}')
    if sha256(RECEIPT) != EXPECTED_RECEIPT:
        raise SystemExit('Receipt changed: inspect final timeline before rebuilding')
    timeline = json.loads(RECEIPT.read_text())['timeline']
    if (timeline['id'], timeline['fps'], timeline['totalFrames']) != ('7AD04C1F', FPS, FRAMES):
        raise SystemExit('Unexpected timeline identity, frame rate, or duration')
    tracks = [t for t in timeline['tracks'] if t.get('type') == 'audio']
    clips = [c for track in tracks for c in track['clips']]
    expected = {'4605B1B1', 'EFAF8B7D', '59CFE337', 'B521480E',
                '7E6A09B4', '39CFB5A4', 'ABF126B1', 'D403B832'}
    if len(clips) != 8 or {c['id'] for c in clips} != expected or {c['mediaRef'] for c in clips} != set(SOURCES):
        raise SystemExit('Audio clip inventory changed or is incomplete')
    for ref, (path, checksum, _) in SOURCES.items():
        if sha256(path) != checksum:
            raise SystemExit(f'Source changed: {ref} {path}')

    cache = {}
    mix = np.zeros((FRAMES * SAMPLES_PER_FRAME, 2), dtype=np.float64)
    for clip in clips:
        ref, speed = clip['mediaRef'], clip.get('speed', 1.0)
        if speed != 1.0 and clip.get('trimStartFrame', 0):
            raise SystemExit('Speed with trim requires separately verified semantics')
        if speed not in (1.0, 1.1):
            raise SystemExit('Unsupported speed')
        key = (ref, speed)
        if key not in cache:
            path, _, channels = SOURCES[ref]
            cache[key] = decode(path, channels, speed)
        start, end = clip['frames']
        if not (0 <= start < end <= FRAMES):
            raise SystemExit(f'Invalid interval: {clip}')
        n = (end - start) * SAMPLES_PER_FRAME
        source_start = clip.get('trimStartFrame', 0) * SAMPLES_PER_FRAME
        source = cache[key][source_start:source_start+n]
        missing = n - len(source)
        # MP3 decodes shorter than its 43-frame container clip; silence-pad only this
        # verified effect, and report the amount so its tail can be compared.
        limit = 3 * SAMPLES_PER_FRAME if ref == '56897AF5' else SAMPLES_PER_FRAME
        if missing > limit:
            raise SystemExit(f'Source too short by {missing} samples for {clip["id"]}')
        samples = np.zeros((n, 2), dtype=np.float64)
        samples[:len(source)] = source
        samples *= 10 ** (clip.get('volumeDb', 0) / 20)
        for kind in ('fadeIn', 'fadeOut'):
            count = clip.get(kind + 'Frames', 0) * SAMPLES_PER_FRAME
            if not count:
                continue
            if count > n:
                raise SystemExit(f'Invalid fade for {clip["id"]}')
            mode = clip.get(kind + 'Interpolation', 'linear')
            if mode not in ('linear', 'smooth'):
                raise SystemExit(f'Unsupported fade: {mode}')
            curve = np.arange(count, dtype=np.float64) / count
            if mode == 'smooth':
                curve = curve * curve * (3.0 - 2.0 * curve)
            if kind == 'fadeIn':
                samples[:count] *= curve[:, None]
            else:
                samples[-count:] *= curve[::-1, None]
        mix[start*SAMPLES_PER_FRAME:end*SAMPLES_PER_FRAME] += samples
        print(f'{clip["id"]} {ref} [{start},{end}) speed={speed} pad_samples={missing}')

    peak = float(np.max(np.abs(mix)))
    if not np.isfinite(peak) or peak >= 1:
        raise SystemExit(f'Invalid or clipping sample peak: {peak}')
    cmd = ['ffmpeg', '-v', 'error', '-n', '-f', 'f32le', '-ar', str(RATE), '-ac', '2',
           '-i', 'pipe:0', '-c:a', 'pcm_s24le', str(OUT)]
    subprocess.run(cmd, input=mix.astype('<f4').tobytes(), check=True)
    print(f'candidate={OUT}\nsample_peak={peak:.8f}\nsha256={sha256(OUT)}')


if __name__ == '__main__':
    main()
