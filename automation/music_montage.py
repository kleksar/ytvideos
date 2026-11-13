#!/usr/bin/env python3
"""Plan accent-aligned shot changes and varied shot sequences for music edits."""
import argparse
import json
from pathlib import Path
import subprocess

import numpy as np

from music_beats import HOP, RATE, WINDOW, attacks


def accent_signal(media):
    """Use attack flux plus rising bass energy from the exact edited audio."""
    raw = subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-i', str(media), '-map', '0:a:0',
        '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-',
    ])
    samples = np.frombuffer(raw, '<f4')
    times, _, flux = attacks(samples)
    windows = np.lib.stride_tricks.sliding_window_view(np.pad(samples, WINDOW // 2), WINDOW)[::HOP]
    fft = np.abs(np.fft.rfft(windows * np.hanning(WINDOW), axis=1))
    bass = fft[:, 2:7].sum(axis=1)
    bass = np.log1p(bass / max(0.001, np.percentile(bass, 85) * 0.06))
    rising = np.maximum(0, bass[6:] - bass[:-6])
    rising = np.interp(times, (np.arange(len(rising)) + 3) * HOP / RATE, rising)
    rising /= max(1e-6, np.percentile(rising, 95))
    strength = .55 * rising + .28 * flux[0] + .10 * flux[1] + .07 * flux[2]
    return times, strength


def candidate_accents(times, strength, fps, pulse=None):
    """Find a distinct onset on each eligible beat or phrase attack."""
    if pulse:
        period, phase = pulse
        nominal = np.arange(phase % period, times[-1], period)
        radius = min(.075, .18 * period)
    else:
        strongest = np.argsort(strength)[::-1]
        retained = []
        for index in strongest:
            if strength[index] < .85 or len(retained) == 85:
                break
            if all(abs(times[index] - previous) >= .14 for previous in retained):
                retained.append(times[index])
        nominal, radius = sorted(retained), .012

    accents = {}
    for tick in nominal:
        indices = np.flatnonzero(abs(times - tick) <= radius)
        if not len(indices):
            continue
        peak = indices[np.argmax(strength[indices])]
        time, value = float(times[peak]), float(strength[peak])
        if value >= .45:
            frame = round(time * fps)
            accents[frame] = {'frame': frame, 'attack_seconds': round(time, 6),
                              'strength': round(value, 4)}
    return accents


def select_rhythm(accents, total_frames, fps, profile):
    """Find the best feasible route through musical attacks for a cadence profile."""
    # Keep the first reveal quick and alternate the requested short and long holds.
    pattern = [round(seconds * fps) for seconds in profile['holds']]
    lower = round(profile['min'] * fps)
    upper = round(profile['max'] * fps)
    opening_limit = round(profile['opening_max'] * fps)
    required = set(profile.get('required', []))
    accents = {frame: accent for frame, accent in accents.items() if 0 < frame < total_frames}
    missing = required - set(accents)
    if missing:
        raise ValueError(f'Required frames are missing from accent map: {sorted(missing)}')
    frames = [0, *sorted(accents), total_frames]
    costs = {0: {0: (0.0, [])}}
    for right_index, right in enumerate(frames[1:], 1):
        paths = {}
        for left in reversed(frames[:right_index]):
            gap = right - left
            if gap > upper:
                break
            if gap < lower or (left == 0 and gap > opening_limit) or any(left < f < right for f in required):
                continue
            for step, (cost, chain) in costs.get(left, {}).items():
                desired = pattern[step % len(pattern)]
                timing_cost = 2.7 * ((gap - desired) / desired) ** 2 + .28
                reward = .20 * min(3, accents.get(right, {}).get('strength', 0.0))
                candidate = (cost + timing_cost - reward, chain + [right])
                slot = (step + 1) % len(pattern)
                if slot not in paths or candidate[0] < paths[slot][0]:
                    paths[slot] = candidate
        costs[right] = paths
    if not costs[total_frames]:
        raise ValueError('No sequence satisfies the cadence and available accents')
    _, chain = min(costs[total_frames].values())
    return [accents[frame] for frame in chain[:-1]]


def select_shots(shots, lengths, first, last, motif=None):
    """Favor visible changes in framing, subject and motion while avoiding repeats."""
    ending_path = next(shot['path'] for shot in shots if shot['id'] == last)
    beam = [(0.0, ())]
    for i, seconds in enumerate(lengths):
        candidates = []
        for score, chosen in beam:
            motif_due = motif and i + 1 in motif['positions']
            for j, shot in enumerate(shots):
                if (i == 0 and shot['id'] != first) or ((i == len(lengths) - 1) != (shot['id'] == last)):
                    continue
                if motif_due and shot['subject'] not in motif['subjects']:
                    continue
                if seconds > shot['max_seconds']:
                    continue
                path = shot['path']
                if i == len(lengths) - 2 and path == ending_path:
                    continue
                recent = [shots[k] for k in chosen[-3:]]
                if recent and path == recent[-1]['path']:
                    continue
                if any(path == item['path'] and abs(shot['source_in'] - item['source_in']) < 3.5 for item in recent):
                    continue
                # One excerpt is used once; a separate excerpt from the same file may appear later.
                if j in chosen:
                    continue
                previous = recent[-1] if recent else shot
                change = (1.0 * (previous['scale'] != shot['scale'])
                          + .7 * (previous['subject'] != shot['subject'])
                          + .5 * (previous['motion'] != shot['motion']))
                preferred = .7 if (seconds <= 1.0) == (shot['motion'] == 'active') else 0.0
                reuse = .8 * sum(shots[k]['path'] == path for k in chosen)
                candidates.append((score + shot['priority'] + change + preferred - reuse,
                                   chosen + (j,)))
        if not candidates:
            raise ValueError(f'No fitting reviewed shot for position {i+1}')
        beam = sorted(candidates, reverse=True)[:140]
    return [shots[j] for j in beam[0][1]]


def plan_timeline(plan):
    """Use the same planner from the CLI and the bound music compositor."""
    fps = plan['fps']
    times, strength = accent_signal(plan['media'])
    accents = candidate_accents(times, strength, fps, plan.get('pulse'))
    accents.update({row['frame']: row for row in plan.get('approved_accents', [])})
    selected = select_rhythm(accents, plan['frames'], fps, plan['profile'])
    boundaries = [0, *(row['frame'] for row in selected), plan['frames']]
    lengths = [(right - left + (1 if i else 0) + (2 if right < plan['frames'] else 0)) / fps
               for i, (left, right) in enumerate(zip(boundaries, boundaries[1:]))]
    clips = select_shots(plan['shots'], lengths, plan['first'], plan['last'], plan.get('motif'))
    return {'accents': selected, 'clips': clips, 'holds_seconds': [
        round((right-left)/fps, 4) for left, right in zip(boundaries, boundaries[1:])
    ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path, help='JSON with media, fps, frames, profile, pulse, shots, first and last')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = plan_timeline(json.loads(args.plan.read_text()))
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')


if __name__ == '__main__':
    main()
