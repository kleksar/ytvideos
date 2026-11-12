#!/usr/bin/env python3
"""Read-only diagnostic of Russian pauses and English speech on a Palmier timeline.

Silence detection is acoustic, not semantic; output is evidence for review, never
an instruction to move/cut clips. Requires ffmpeg, ffprobe and the local Palmier
MCP bridge. It does not edit the project or change the active timeline.
"""
import argparse
import csv
import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'automation/palmier'))
from inspect_connection import PalmierConnection

PROJECT = '/Users/diplomat/Documents/Palmier Pro/Borisenko English Pilot 001.palmier'
VIDEO = ROOT / 'projects/borisenko/pilot_001/Source/К чему эти разговоры если гибнyт русские люди.mp4'
ENGLISH = ROOT / 'projects/borisenko/pilot_001/Source/Maxim_Orlov_english_speed_095.wav'
EDIT = ROOT / 'projects/borisenko/pilot_001/Edit'


def read_tool(conn, name, arguments):
    r = conn.request('tools/call', {'name': name, 'arguments': arguments})
    if r.get('isError'):
        raise RuntimeError(f'{name}: {r.get("content")}')
    return json.loads(next(item['text'] for item in r['content'] if item.get('type') == 'text'))


def duration(path):
    proc = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                           '-of', 'default=noprint_wrappers=1:nokey=1', str(path)],
                          capture_output=True, text=True, check=True)
    return float(proc.stdout.strip())


def silence(path, noise, minimum, total):
    """Return source seconds as [start,end] half-open intervals detected by FFmpeg."""
    proc = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', str(path),
                           '-vn', '-af', f'silencedetect=n={noise}dB:d={minimum}',
                           '-f', 'null', '-'], capture_output=True, text=True, check=True)
    starts = []
    spans = []
    for line in proc.stderr.splitlines():
        start = re.search(r'silence_start:\s*([\d.]+)', line)
        end = re.search(r'silence_end:\s*([\d.]+)', line)
        if start:
            starts.append(float(start.group(1)))
        if end and starts:
            spans.append((starts.pop(0), min(float(end.group(1)), total)))
    if starts:
        spans.append((starts[0], total))
    return spans


def complement(spans, total):
    p = 0.0
    out = []
    for a, b in spans:
        if a > p:
            out.append((p, a))
        p = max(p, b)
    if p < total:
        out.append((p, total))
    return out


def intersect(a, b):
    start, end = max(a[0], b[0]), min(a[1], b[1])
    return (start, end) if end > start else None


def contexts(segments, start, end):
    return [{'start': round(s['start'], 3), 'end': round(s['end'], 3),
             'text': s['text'].strip()}
            for s in segments if s['end'] >= start and s['start'] <= end]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--project', default=PROJECT, help='Expected active and visible .palmier project path')
    parser.add_argument('--timeline-id', default='B791704C', help='Required exact active timeline ID')
    parser.add_argument('--video', type=Path, default=VIDEO, help='Russian source video (the original imported file)')
    parser.add_argument('--english', type=Path, default=ENGLISH, help='English source audio (already slowed to 0.95)')
    parser.add_argument('--video-ref', default='404792DB', help='Expected Palmier Russian video mediaRef')
    parser.add_argument('--english-ref', default='6BA86F3F', help='Expected Palmier English audio mediaRef')
    parser.add_argument('--track', default='English095', help='Exact English track name')
    parser.add_argument('--start', type=float, default=0, help='Timeline window start in seconds (inclusive)')
    parser.add_argument('--end', type=float, help='Timeline window end in seconds (exclusive; default timeline duration)')
    parser.add_argument('--ru-noise', type=float, default=-35, help='Russian silence threshold dBFS (default -35)')
    parser.add_argument('--ru-min', type=float, default=0.3, help='Minimum Russian silence in seconds (default 0.3)')
    parser.add_argument('--en-noise', type=float, default=-45, help='English silence threshold dBFS (default -45)')
    parser.add_argument('--en-min', type=float, default=0.18, help='Minimum English silence in seconds (default 0.18)')
    parser.add_argument('--json', type=Path, required=True, help='New JSON report path (never overwritten)')
    parser.add_argument('--csv', type=Path, required=True, help='New CSV report path (never overwritten)')
    args = parser.parse_args()
    if args.json.exists() or args.csv.exists():
        parser.error('Output exists; choose new --json and --csv paths.')
    if args.json.resolve() == args.csv.resolve():
        parser.error('--json and --csv must be different files.')
    for path in (args.video, args.english):
        if not path.is_file():
            parser.error(f'Media not found: {path}')
    if args.start < 0 or (args.end is not None and args.end <= args.start):
        parser.error('Invalid time window.')
    conn = PalmierConnection()
    conn.connect()
    projects = read_tool(conn, 'manage_project', {'action': 'list'})
    wanted = Path(args.project).resolve()
    for state in ('active', 'visible'):
        if not projects.get(state) or Path(projects[state]['path']).resolve() != wanted:
            raise RuntimeError(f'Wrong {state} project; refusing analysis')
    t = read_tool(conn, 'get_timeline', {})
    if t['id'] != args.timeline_id:
        raise RuntimeError(f'Wrong timeline: {t["id"]}; expected {args.timeline_id}')
    fps = float(t['fps'])
    if fps <= 0:
        raise RuntimeError('Invalid timeline FPS')
    tracks = t['tracks']
    vids = [c for tr in tracks for c in tr.get('clips', []) if c.get('mediaRef') == args.video_ref]
    if len(vids) != 1:
        raise RuntimeError('Expected exactly one Russian source video clip')
    video = vids[0]
    if video.get('speed', 1) != 1 or video.get('speedCurve'):
        raise RuntimeError('Unsupported video speed/curve: use a speed-aware mapping')
    if not video.get('audio'):
        raise RuntimeError('Russian video has no linked audio')
    linked = video['audio']
    if linked.get('trimStartFrame') is not None or linked.get('trimEndFrame') is not None:
        raise RuntimeError('Russian linked audio has separate trims; inspect before mapping')
    track = next((tr for tr in tracks if tr.get('name') == args.track), None)
    if not track or track.get('muted'):
        raise RuntimeError('English track is missing or muted')
    clips = track.get('clips', [])
    if not clips or any(c.get('mediaRef') != args.english_ref or c.get('speed', 1) != 1 or c.get('speedCurve') for c in clips):
        raise RuntimeError('English clips must all use expected mediaRef at 1x')
    assets = read_tool(conn, 'get_media', {'ids': [args.video_ref, args.english_ref]}).get('assets', [])
    by_ref = {a['id']: a for a in assets}
    ru_duration, en_duration = duration(args.video), duration(args.english)
    for ref, path, actual in ((args.video_ref, args.video, ru_duration), (args.english_ref, args.english, en_duration)):
        asset = by_ref.get(ref)
        if not asset or asset.get('name') != path.stem or abs(float(asset['durationSeconds']) - actual) > 0.2:
            raise RuntimeError(f'Asset name/duration mismatch: {ref} vs {path}')
    end = min(args.end if args.end is not None else t['durationSeconds'], t['durationSeconds'])
    if end <= args.start:
        raise RuntimeError('Window outside timeline')
    ru_silence = silence(args.video, args.ru_noise, args.ru_min, ru_duration)
    en_silence = silence(args.english, args.en_noise, args.en_min, en_duration)
    en_active = complement(en_silence, en_duration)
    ru_trans = json.loads((EDIT / 'transcript_ru.json').read_text())['segments'] if (EDIT / 'transcript_ru.json').exists() else []
    en_trans = json.loads((EDIT / 'transcript_en_095_whisper.json').read_text())['segments'] if (EDIT / 'transcript_en_095_whisper.json').exists() else []
    clip_map = []
    for c in clips:
        start, finish = c['frames'][0] / fps, c['frames'][1] / fps
        src = c.get('trimStartFrame', 0) / fps
        clip_map.append({'clipId': c['id'], 'timeline': (start, finish), 'source': (src, src + finish - start)})
    video_start = video['frames'][0] / fps
    video_end = video['frames'][1] / fps
    ru_source_start = video.get('trimStartFrame', 0) / fps
    rows = []
    for ra, rb in ru_silence:
        original_start = video_start + ra - ru_source_start
        original_end = video_start + rb - ru_source_start
        span = intersect((original_start, original_end), (max(args.start, video_start), min(end, video_end)))
        if not span:
            continue
        hits = []
        candidates = []
        for clip in clip_map:
            if not intersect(clip['timeline'], span):
                continue
            offset = clip['timeline'][0] - clip['source'][0]
            for v in en_active:
                source_overlap = intersect(v, clip['source'])
                if not source_overlap:
                    continue
                hit = intersect((source_overlap[0] + offset, source_overlap[1] + offset), span)
                if hit:
                    hits.append({'clipId': clip['clipId'], 'timelineStart': round(hit[0], 3),
                                 'timelineEnd': round(hit[1], 3),
                                 'sourceStart': round(hit[0] - offset, 3),
                                 'sourceEnd': round(hit[1] - offset, 3),
                                 'englishContext': contexts(en_trans, hit[0] - offset, hit[1] - offset)})
            # A frame-aligned point at least 75ms inside an acoustically quiet span.
            # This is only a candidate; a quiet consonant or a poor semantic break
            # still requires human inspection and listening.
            for a, b in en_silence:
                a, b = max(a, clip['source'][0]), min(b, clip['source'][1])
                if b - a < 0.15:
                    continue
                sf = round(((a + b) / 2) * fps)
                s = sf / fps
                if s-a < 0.075 or b-s < 0.075:
                    continue
                timeline_s = s + offset
                if span[0]-5 <= timeline_s <= span[1]+5:
                    candidates.append({'clipId': clip['clipId'], 'sourceFrame': sf,
                        'sourceSeconds': round(s, 3), 'timelineFrame': round(timeline_s * fps),
                        'silence': [round(a, 3), round(b, 3)],
                        'warning': 'Acoustic candidate only; verify words and meaning before cutting'})
        rows.append({'russianPauseTimeline': [round(span[0], 3), round(span[1], 3)],
                     'russianPauseSource': [round(ra, 3), round(rb, 3)],
                     'englishSoundOverlapSeconds': round(sum(h['timelineEnd']-h['timelineStart'] for h in hits), 3),
                     'englishSoundHits': hits,
                     'russianContext': contexts(ru_trans, ra-1.5, rb+1.5),
                     'englishSafeCutCandidates': candidates})
    # Analysis is a snapshot, not a lock: refuse stale results if the user changed
    # the project or either track while the FFmpeg scans were running.
    projects_after = read_tool(conn, 'manage_project', {'action': 'list'})
    t_after = read_tool(conn, 'get_timeline', {})
    if (t_after.get('id') != t['id'] or t_after.get('fps') != t['fps']
            or t_after.get('tracks') != t['tracks']
            or any(not projects_after.get(state) or
                   Path(projects_after[state]['path']).resolve() != wanted
                   for state in ('active', 'visible'))):
        raise RuntimeError('Timeline or project changed during analysis; rerun')
    report = {'timeline': {'id': t['id'], 'name': t['name'], 'fps': fps,
                 'videoTrimStartFrames': video.get('trimStartFrame', 0),
                 'russianVideoRef': args.video_ref, 'englishAudioRef': args.english_ref},
              'settings': {'window': [args.start, end], 'russianThresholdDb': args.ru_noise,
                           'russianMinimumSeconds': args.ru_min, 'englishThresholdDb': args.en_noise,
                           'englishMinimumSeconds': args.en_min},
              'media': {'video': str(args.video.resolve()), 'english': str(args.english.resolve()),
                        'videoSeconds': ru_duration, 'englishSeconds': en_duration},
              'warning': 'Acoustic silence and automatic transcripts are imperfect. Sound overlap is not proof of semantic misalignment; verify source identity, words, and audio by listening. No timeline modifications were made.',
              'russianPauses': rows}
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.json.open('x', encoding='utf8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    with args.csv.open('x', encoding='utf8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['ru_pause_start_s', 'ru_pause_end_s', 'english_sound_overlap_s',
                    'clip_ids', 'russian_context', 'english_context', 'safe_cut_candidates_s'])
        for row in rows:
            w.writerow([*row['russianPauseTimeline'], row['englishSoundOverlapSeconds'],
                        '; '.join(sorted({h['clipId'] for h in row['englishSoundHits']})),
                        ' '.join(s['text'] for s in row['russianContext']),
                        ' '.join(s['text'] for h in row['englishSoundHits'] for s in h['englishContext']),
                        '; '.join(str(c['sourceSeconds']) for c in row['englishSafeCutCandidates'])])
    print(f'{len(rows)} Russian pauses; {sum(bool(r["englishSoundHits"]) for r in rows)} with English sound overlap.')
    print(f'JSON: {args.json}\nCSV: {args.csv}')


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError, KeyError, ValueError) as exc:
        print(f'Error: {exc}', file=sys.stderr)
        sys.exit(1)
