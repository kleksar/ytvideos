#!/usr/bin/env python3
"""Create frame-accurate film cut candidates from attacks in the actual edited mix.

Requires ffmpeg and numpy. Detected attacks are candidates; musical meaning and
perceptual synchronization must be checked on the delivered file.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from music_beats import RATE, cut_candidates


def make_plan(samples, fps, excerpt_start, first_after, stride, count):
    analysis = cut_candidates(samples, fps)
    if not analysis['pulse']:
        raise ValueError('No reliable pulse detected; use another excerpt or review manually')
    detected = []
    for candidate in analysis['candidates']:
        timestamp = excerpt_start + candidate['seconds']
        frame = math.floor(timestamp * fps + 0.5)
        detected.append({'time_seconds': round(timestamp, 6), 'frame': frame,
                         'frame_seconds': round(frame / fps, 6),
                         'frame_offset_ms': round((frame / fps - timestamp) * 1000, 2),
                         'strength': candidate['strength'], 'band_flux': candidate['band_flux']})
    eligible = [row for row in detected if row['time_seconds'] >= first_after]
    selected = eligible[::stride][:count]
    if len(selected) != count:
        raise ValueError(f'Only {len(selected)} cuts available; requested {count}')
    if len({row['frame'] for row in selected}) != len(selected):
        raise ValueError('Multiple detections map to one frame')
    return {'pulse': analysis['pulse'], 'detected_attacks': detected, 'selected_transitions': selected}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('media', type=Path)
    p.add_argument('--start', type=float, required=True, help='Analysis start in media timeline, seconds')
    p.add_argument('--duration', type=float, required=True)
    p.add_argument('--first-after', type=float, required=True, help='Earliest eligible transition in media timeline')
    p.add_argument('--fps', type=int, default=24)
    p.add_argument('--stride', type=int, default=1, help='Select every Nth detected attack (default: every detected attack)')
    p.add_argument('--count', type=int, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    if not all(math.isfinite(n) for n in (a.start, a.duration, a.first_after)) or a.start < 0 or a.duration < 3 or a.first_after < a.start or a.fps < 1 or a.stride < 1 or a.count < 1:
        p.error('Invalid timeline, duration, fps, stride or count')
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(a.media), '-ss', str(a.start), '-t', str(a.duration), '-map', '0:a:0', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-']
    try:
        data = subprocess.check_output(cmd)
        samples = np.frombuffer(data, dtype='<f4')
        if len(samples) < 3 * RATE:
            raise ValueError('Decoded audio is shorter than 3 seconds')
        plan = make_plan(samples, a.fps, a.start, a.first_after, a.stride, a.count)
    except (ValueError, subprocess.CalledProcessError) as exc:
        p.error(str(exc))
    sha = hashlib.sha256()
    with a.media.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            sha.update(chunk)
    result = {'status': 'signal_candidates_not_listening_verified', 'media': str(a.media.resolve()),
              'media_sha256': sha.hexdigest(), 'fps': a.fps, 'analysis_start_seconds': a.start,
              'analysis_duration_seconds': len(samples) / RATE, 'first_after_seconds': a.first_after,
              'stride': a.stride, **plan}
    with a.output.open('x', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write('\n')

if __name__ == '__main__':
    main()
