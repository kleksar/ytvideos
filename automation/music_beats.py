#!/usr/bin/env python3
"""Find frame-aligned cut candidates from percussion attacks in a local audio mix."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np


RATE = 22050
WINDOW = 1024
HOP = 55
DIFFERENCE = 4
BANDS = ((35, 180), (180, 2500), (2500, 8500))
WEIGHTS = np.array([0.45, 0.28, 0.27])


def attacks(samples):
    padded = np.pad(samples, (WINDOW // 2, WINDOW // 2))
    windows = np.lib.stride_tricks.sliding_window_view(padded, WINDOW)[::HOP]
    spectrum = np.abs(np.fft.rfft(windows * np.hanning(WINDOW), axis=1))
    floor = max(np.percentile(spectrum.max(axis=1), 90) * 0.012, 1e-6)
    compressed = np.log1p(spectrum / floor)
    change = np.maximum(compressed[DIFFERENCE:] - compressed[:-DIFFERENCE], 0)
    frequencies = np.fft.rfftfreq(WINDOW, 1 / RATE)
    flux = np.stack([
        change[:, (frequencies >= low) & (frequencies < high)].mean(axis=1)
        for low, high in BANDS
    ])
    flux /= np.maximum(np.percentile(flux, 95, axis=1)[:, None], 1e-7)
    strength = WEIGHTS @ np.minimum(flux, 4)
    # Refer the rising difference to the midpoint of its two analysis windows.
    time = (np.arange(len(strength)) + DIFFERENCE / 2) * HOP / RATE
    return time, strength, flux


def periodic_pulse(time, strength):
    step = HOP / RATE
    centered = strength - strength.mean()
    fft_size = 1 << (2 * len(centered) - 1).bit_length()
    autocorrelation = np.fft.irfft(abs(np.fft.rfft(centered, n=fft_size)) ** 2)
    if autocorrelation[0] < 1e-10:
        return None
    lags = np.arange(round(60 / 175 / step), round(60 / 75 / step) + 1)
    index = int(np.argmax(autocorrelation[lags] + 0.35 * autocorrelation[2 * lags]))
    period = lags[index] * step
    confidence = float(autocorrelation[lags[index]] / autocorrelation[0])
    if confidence < 0.14:
        return None
    phases = np.arange(0, period, step)
    ticks = phases[:, None] + period * np.arange(int(time[-1] / period) + 1)
    average = np.interp(ticks, time, strength, left=0, right=0).sum(axis=1)
    return period, float(phases[int(np.argmax(average))]), confidence


def cut_candidates(samples, fps):
    time, strength, flux = attacks(samples)
    grid = periodic_pulse(time, strength)
    if grid is None:
        return {'pulse': None, 'candidates': []}
    period, phase, confidence = grid
    marks = []
    for center in np.arange(phase, time[-1], period):
        start, stop = np.searchsorted(time, [center - 0.038, center + 0.038])
        if stop == start:
            continue
        peak = start + int(np.argmax(strength[start:stop]))
        if strength[peak] < 0.60:
            continue
        seconds = float(time[peak])
        frame = math.floor(seconds * fps + 0.5)
        bands = [round(float(level), 3) for level in flux[:, peak]]
        marks.append({'seconds': round(seconds, 6), 'frame': frame,
                      'frame_offset_ms': round((frame / fps - seconds) * 1000, 2),
                      'strength': round(float(strength[peak]), 3), 'band_flux': bands})
    return {
        'pulse': {'bpm': round(60 / period, 2), 'period_seconds': round(period, 6),
                  'phase_seconds': round(phase, 6), 'periodicity': round(confidence, 3)},
        'candidates': marks,
    }


def audit_cuts(candidates, cuts, fps):
    tolerance = max(1, round(0.05 * fps))
    matched, unmatched = [], []
    for mark in candidates:
        nearest = min(cuts, key=lambda cut: abs(cut - mark['frame']))
        distance = abs(nearest - mark['frame'])
        row = {**mark, 'nearest_cut_frame': nearest, 'distance_frames': distance}
        (matched if distance <= tolerance else unmatched).append(row)
    strengths = [mark['strength'] for mark in matched or candidates]
    threshold = float(np.median(strengths)) * 0.82 if strengths else None
    return {
        'tolerance_frames': tolerance,
        'strength_threshold': round(threshold, 3) if threshold is not None else None,
        'matched': matched,
        'strong_uncovered': [mark for mark in unmatched if mark['strength'] >= threshold],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mix', type=Path, help='Exact edited audio, or a preview plus --start and --duration')
    parser.add_argument('--start', type=float, default=0)
    parser.add_argument('--duration', type=float)
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--cut-map', type=Path, help='Optional JSON with fps and cut_frames to flag strong uncovered attacks')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.fps <= 0 or not math.isfinite(args.start) or args.start < 0:
        parser.error('fps must be positive and start must be nonnegative')
    if args.duration is not None and (not math.isfinite(args.duration) or args.duration < 3):
        parser.error('duration must be at least 3 seconds')
    cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(args.mix), '-ss', str(args.start)]
    if args.duration is not None:
        cmd += ['-t', str(args.duration)]
    cmd += ['-map', '0:a:0', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-']
    samples = np.frombuffer(subprocess.check_output(cmd), dtype='<f4')
    if len(samples) < 3 * RATE:
        parser.error('the decoded excerpt must be at least 3 seconds')
    with args.mix.open('rb') as source:
        digest = hashlib.sha256()
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    result = {'source': str(args.mix.resolve()), 'sha256': digest.hexdigest(), 'fps': args.fps,
              'source_start_seconds': args.start, 'duration_seconds': len(samples) / RATE,
              'frames': round(len(samples) * args.fps / RATE),
              'status': 'signal_candidates', **cut_candidates(samples, args.fps)}
    result['candidates'] = [candidate for candidate in result['candidates'] if 0 <= candidate['frame'] < result['frames']]
    if args.cut_map:
        cut_map = json.loads(args.cut_map.read_text(encoding='utf-8'))
        cuts = cut_map.get('cut_frames')
        if (cut_map.get('fps') != args.fps or not isinstance(cuts, list) or not cuts
                or any(type(cut) is not int or not 0 < cut < len(samples) * args.fps / RATE for cut in cuts)
                or cuts != sorted(set(cuts))):
            parser.error('cut map needs matching fps and unique, increasing interior cut_frames')
        result['cut_audit'] = audit_cuts(result['candidates'], cuts, args.fps)
    with args.output.open('x', encoding='utf-8') as out:
        json.dump(result, out, indent=2)
        out.write('\n')


if __name__ == '__main__':
    main()
