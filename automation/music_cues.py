#!/usr/bin/env python3
"""Index candidate music cues in a hash-verified library. Requires FFmpeg and NumPy."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np


RATE = 22050
FRAME = 2048
HOP = 512
BINS_PER_SECOND = 4


def relative(values):
    low, high = np.percentile(values, [10, 90])
    return np.clip((values - low) / max(high - low, 1e-6), 0, 1)


def measure(path):
    pcm = subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-xerror', '-i', str(path),
        '-map', '0:a:0', '-ac', '1', '-ar', str(RATE), '-f', 'f32le', '-',
    ])
    samples = np.frombuffer(pcm, dtype='<f4')
    frames = np.lib.stride_tricks.sliding_window_view(samples, FRAME)[::HOP]
    times = (np.arange(len(frames)) * HOP + FRAME / 2) / RATE
    power = np.abs(np.fft.rfft(frames * np.hanning(FRAME))) ** 2
    frequencies = np.fft.rfftfreq(FRAME, 1 / RATE)
    bands = []
    for lower, upper in [(40, 180), (180, 2500)]:
        band = power[:, (frequencies >= lower) & (frequencies < upper)]
        bands.append(band.sum(axis=1))
    loudness = 10 * np.log10(np.mean(frames**2, axis=1) + 1e-12)
    floor = max(loudness.max() - 27, -65)
    # Positive spectral change over about 70 ms, with a floor tied to the track.
    compressed = np.log1p(power / max(np.percentile(power.max(axis=1), 90) * 0.001, 1e-12))
    flux = np.pad(np.maximum(compressed[3:] - compressed[:-3], 0).mean(axis=1), (3, 0))
    flux[loudness < floor] = 0
    attacks = np.maximum(np.r_[0, np.diff(bands[0])], 0)
    attacks[loudness < floor] = 0
    edges = np.searchsorted(times, np.arange(int(times[-1] * BINS_PER_SECOND) + 1) / BINS_PER_SECOND)
    bins = [slice(a, b) for a, b in zip(edges, edges[1:])]
    level = np.array([np.median(loudness[chunk]) for chunk in bins])
    bass = np.array([np.median(bands[0][chunk]) for chunk in bins])
    mid = np.array([np.median(bands[1][chunk]) for chunk in bins])
    novelty = np.array([flux[chunk].max() for chunk in bins])
    pulse = np.array([attacks[chunk].max() for chunk in bins])
    activity = 0.45 * relative(level) + 0.30 * relative(novelty) + 0.25 * relative(bass)
    attack_times = [times[chunk.start + int(np.argmax(flux[chunk]))] for chunk in bins]
    return level, floor, activity, relative(mid), relative(pulse), relative(novelty), attack_times


def choose(candidates, count=3):
    selected = []
    for score, cue in sorted(candidates, key=lambda item: item[0], reverse=True):
        if all(abs(cue['anchor_s'] - other['anchor_s']) >= 12
               and (cue['end_s'] <= other['start_s'] or other['end_s'] <= cue['start_s'])
               for other in selected):
            selected.append(cue)
            if len(selected) == count:
                break
    return selected


def find_cues(level, floor, activity, mid, pulse, novelty, attack_times):
    rate = BINS_PER_SECOND
    results = {name: [] for name in ('bed', 'build', 'impact', 'release')}
    def mean(values, start, end):
        return float(values[start:end].mean())

    def add(role, start, anchor, end, score, evidence):
        results[role].append((score, {
            'start_s': start / rate,
            'anchor_s': round(float(anchor), 2),
            'end_s': end / rate,
            'evidence': evidence,
        }))

    for index in range(3 * rate, len(level) - 4 * rate):
        after = slice(index, index + 4 * rate)
        if np.count_nonzero(level[after] >= floor) < 3 * rate:
            continue
        before = slice(index - 3 * rate, index)
        previous = float(np.median(level[before]))
        following = float(np.median(level[index:index + 2 * rate]))
        change = following - previous
        lift = mean(activity, index, index + 2 * rate) - mean(activity, index - 3 * rate, index)
        context_audible = np.count_nonzero(level[before] >= floor) >= 2 * rate
        attack = max(pulse[index], novelty[index])
        local_lift = mean(activity, index, index + 2) - mean(activity, index - 2, index)
        if context_audible and attack >= 0.65 and local_lift >= 0.08 and (change >= 2 or lift >= 0.16):
            score = min(max(0, change), 9) / 9 + lift + 0.55 * attack + 0.5 * local_lift
            add('impact', max(0, index - 5 * rate), attack_times[index], index + 4 * rate, score,
                {'level_change_db': round(change, 1), 'activity_change': round(lift, 2)})
        tail_change = float(np.median(level[index + 2 * rate:index + 4 * rate])) - previous
        if context_audible and (change <= -2.5 or lift <= -0.16) and tail_change <= -1:
            score = max(0, -change) / 9 - lift
            add('release', index - 3 * rate, index / rate, index + 4 * rate, score,
                {'level_change_db': round(change, 1), 'activity_change': round(lift, 2)})

        if index >= 8 * rate:
            start = index - 8 * rate
            early = mean(activity, start, start + 2 * rate)
            middle = mean(activity, index - 5 * rate, index - 3 * rate)
            late = mean(activity, index - 2 * rate, index)
            rise = late - early
            if rise >= 0.16 and early - 0.03 <= middle <= late + 0.03 and level[start] >= floor:
                add('build', start, index / rate, index + 2 * rate, rise + 0.2 * late,
                    {'activity_change': round(rise, 2)})

        end = index + 16 * rate
        if index % rate or end > len(level) or np.percentile(level[index:end], 10) < floor:
            continue
        segment = activity[index:end]
        mid_load = mean(mid, index, end)
        score = 1 - float(segment.mean()) - 0.6 * float(segment.std()) - 0.35 * mid_load
        add('bed', index, index / rate, end, score,
            {'median_level_dbfs': round(float(np.median(level[index:end])), 1),
             'relative_mid_load': round(mid_load, 2)})

    return {role: choose(candidates) for role, candidates in results.items()}


def timecode(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f'{int(minutes):02}:{seconds:05.2f}'


def markdown(tracks):
    lines = [
        '# Таймкоды музыкальных акцентов', '',
        'Таймкоды отсчитаны от начала MP3. Это кандидаты по звуковому сигналу. Слуховая и монтажная проверка ещё впереди.',
        'В таблице показан первый кандидат каждой роли. В JSON есть до трёх разнесённых по времени вариантов.', '',
        '| Трек | Ровная подложка | Нарастание | Акцент | Спад |',
        '|---|---|---|---|---|',
    ]
    for track in tracks:
        cells = [track['title']]
        for role in ('bed', 'build', 'impact', 'release'):
            cues = track['cues'][role]
            if cues:
                cue = cues[0]
                interval = f"{timecode(cue['start_s'])}–{timecode(cue['end_s'])}"
                if role in ('impact', 'release'):
                    interval += f" · **{timecode(cue['anchor_s'])}**"
                cells.append(interval)
            else:
                cells.append('—')
        lines.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    library = args.manifest.parent
    manifest = json.loads(args.manifest.read_text())
    tracks = []
    for entry in manifest['tracks']:
        path = library / entry['file']
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry['sha256']:
            raise ValueError(f'Source hash differs from manifest: {path}')
        track = {key: entry[key] for key in ('title', 'file', 'sha256', 'duration_seconds')}
        track['cues'] = find_cues(*measure(path))
        tracks.append(track)
        print(track['title'], flush=True)
    index = {'version': 1, 'status': 'signal_candidates', 'tracks': tracks}
    (library / 'CUES.json').write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n')
    (library / 'CUES.md').write_text(markdown(tracks))


if __name__ == '__main__':
    main()
