#!/usr/bin/env python3
"""Reconstruct Shorts 01 mix from saved Palmier timeline, retaining all tracks.

The smooth fade curve below is an approximation. The 576-sample MP3 voice
offset and unity mono-to-stereo gain were measured against the raw export.
"""
import json
import subprocess
from pathlib import Path

import numpy as np

root = Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game')
short = root / 'Shorts/01_radio_signal'
edit = short / 'Edit/pacing_20261031'
deliver = short / 'Deliverables'
timeline = json.loads((edit / 'timeline_final.json').read_text())
assert timeline['id'] == '7178D5B6' and timeline['fps'] == 30 and timeline['totalFrames'] == 885
files = {
    'A613549D': short / 'Source/Voice/strategy_v1/generated/voice_en.mp3',
    'B125E330': short / 'Source/Audio/strategy_v1/music_bed_56s_synth_stereo.wav',
    '7A83EDA7': short / 'Source/Audio/strategy_v1/sfx_radio_search_synth_1_8s.wav',
    '9019AE92': short / 'Source/Audio/strategy_v1/book-page-02.wav',
    '298075B6': root / 'Source/Audio/paper_motion_cc0_20261030/book-page-01.wav',
}
for file in files.values():
    assert file.is_file(), file
rate, per_frame = 44100, 1470
decoded = {}
for ref, file in files.items():
    channels = 1 if ref == 'A613549D' else 2
    cmd = ['ffmpeg', '-v', 'error', '-i', str(file), '-map', '0:a:0', '-ac', str(channels), '-ar', str(rate), '-f', 'f32le', 'pipe:1']
    samples = np.frombuffer(subprocess.run(cmd, check=True, stdout=subprocess.PIPE).stdout, dtype='<f4').copy().reshape(-1, channels)
    if channels == 1:
        samples = np.repeat(samples, 2, axis=1)
    decoded[ref] = samples

mix = np.zeros((timeline['totalFrames'] * per_frame, 2), dtype=np.float64)
clips = [c for t in timeline['tracks'] if t.get('type') == 'audio' for c in t['clips']]
assert len(clips) == 14 and {c['mediaRef'] for c in clips} == set(files)
for clip in clips:
    start, end = clip['frames']
    count = (end - start) * per_frame
    trim = clip.get('trimStartFrame', 0) * per_frame
    src = decoded[clip['mediaRef']][trim:trim + count]
    samples = np.zeros((count, 2), dtype=np.float64)
    shift = 576 if clip['mediaRef'] == 'A613549D' else 0
    available = min(len(src), count - shift)
    samples[shift:shift + available] = src[:available]
    samples *= 10 ** (clip.get('volumeDb', 0) / 20)
    for fade in ('fadeIn', 'fadeOut'):
        n = clip.get(fade + 'Frames', 0) * per_frame
        if not n:
            continue
        envelope = np.arange(n, dtype=np.float64) / n
        if clip.get(fade + 'Interpolation') == 'smooth':
            envelope = envelope * envelope * (3 - 2 * envelope)
        if fade == 'fadeIn':
            samples[:n] *= envelope[:, None]
        else:
            samples[-n:] *= envelope[::-1, None]
    mix[start * per_frame:end * per_frame] += samples
    print(clip['id'], clip['mediaRef'], start, end, flush=True)

wav = edit / 'full_mix_candidate_pcm24_20261031.wav'
raw = deliver / '001_short_01_pacing_era_palmier_raw_20261031.mp4'
output = deliver / '001_short_01_pacing_era_audio320_20261031.mp4'
assert raw.is_file() and not wav.exists() and not output.exists()
assert np.max(np.abs(mix)) < 1, f"unclipped sample peak exceeds 0 dBFS: {np.max(np.abs(mix))}"
cmd = ['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(rate), '-ac', '2', '-i', 'pipe:0', '-c:a', 'pcm_s24le', str(wav)]
subprocess.run(cmd, input=mix.astype('<f4').tobytes(), check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-i', str(raw), '-i', str(wav), '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-ar', str(rate), '-movflags', '+faststart', str(output)], check=True)
print('sample_peak', float(np.max(np.abs(mix))), 'samples', len(mix), 'output', output)
