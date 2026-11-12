#!/usr/bin/env python3
"""Read-only comparison: python3 compare_candidate_to_export_20261031.py FILE.mp4.

Measures 10ms RMS-envelope lag and level differences; scores cannot replace
listening or prove that the two different stretch algorithms are identical.
"""
import json
import subprocess
import sys
from pathlib import Path
import numpy as np

RATE = 44100
BIN = 441
HERE = Path(__file__).resolve().parent
CANDIDATE = HERE / 'full_mix_candidate_20261031_pcm24.wav'
SFX_FRAMES = [88, 441, 1041, 1357, 2231, 2264]


def decode(path):
    cmd = ['ffmpeg', '-v', 'error', '-i', str(path), '-map', '0:a:0',
           '-ar', str(RATE), '-ac', '2', '-f', 'f32le', 'pipe:1']
    data = subprocess.run(cmd, stdout=subprocess.PIPE, check=True).stdout
    return np.frombuffer(data, dtype='<f4').reshape(-1, 2).astype(np.float64)


def rms(x):
    return float(np.sqrt(np.mean(x*x))) if x.size else 0.0


def envelope(x):
    x = x[:len(x)//BIN*BIN]
    return np.sqrt(np.mean(x.reshape(-1, BIN)**2, axis=1))


def correlation(x, y):
    if x.size < 2 or np.std(x) < 1e-12 or np.std(y) < 1e-12:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def measure(candidate, export, start, end):
    a = envelope((candidate[:, 0] + candidate[:, 1]) / 2)
    b = envelope((export[:, 0] + export[:, 1]) / 2)
    lo, hi = int(start*100), int(end*100)
    best = None
    for lag in range(-50, 51):
        i = max(lo, 0, -lag)
        j = min(hi, len(a), len(b)-lag)
        if j-i < 40:
            continue
        corr = correlation(a[i:j], b[i+lag:j+lag])
        if corr is not None and (best is None or corr > best[0]):
            best = (corr, lag)
    l, r = int(start*RATE), min(int(end*RATE), len(candidate), len(export))
    ca, ex = candidate[l:r], export[l:r]
    rc, re = rms(ca), rms(ex)
    sc, se = rms((ca[:, 0]-ca[:, 1])/2), rms((ex[:, 0]-ex[:, 1])/2)
    return {'seconds': [start, end],
            'envelope_correlation': round(best[0], 4) if best else None,
            'export_lag_ms': best[1]*10 if best else None,
            'rms_delta_export_minus_candidate_db': round(20*np.log10(re/rc), 3) if re and rc else None,
            'side_rms_delta_db': round(20*np.log10(se/sc), 3) if se and sc else None}


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    mp4 = Path(sys.argv[1]).resolve()
    if not mp4.is_file() or not CANDIDATE.is_file():
        raise SystemExit('Export or PCM candidate missing')
    candidate, export = decode(CANDIDATE), decode(mp4)
    common = min(len(candidate), len(export))/RATE
    if common < 75:
        raise SystemExit('Export shorter than expected; do not compare incomplete file')
    result = {'candidate': str(CANDIDATE), 'export': str(mp4),
              'candidate_seconds': len(candidate)/RATE, 'export_seconds': len(export)/RATE,
              'export_lag_sign': 'positive = export later than candidate',
              'windows': [measure(candidate, export, start, min(end, common)) for start, end in
                          [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30),
                           (30, 35), (35, 40), (40, 45), (45, 50), (50, 55), (55, 60),
                           (60, 65), (65, 70), (70, 75), (75, 76.5)]],
              'sfx_windows': [dict(frame=f, **measure(candidate, export,
                              max(0, f/30-0.4), min(common, f/30+1.2))) for f in SFX_FRAMES]}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
