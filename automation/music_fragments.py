#!/usr/bin/env python3
"""Record video and audio source intervals from versioned, checked Short exports."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def read(path):
    return json.loads(Path(path).read_text())


def source_identity(path, page):
    reference = page or ''
    match = re.search(r'pexels\.com/video/(?:[^/]*-)?(\d+)(?:/|$)', reference)
    if match:
        return f'pexels:{match[1]}'
    match = re.fullmatch(r'pexels-(\d+)', Path(path).stem)
    return f'pexels:{match[1]}' if match else None


def audio_packet_hash(path):
    result = subprocess.check_output([
        'ffmpeg', '-nostdin', '-v', 'error', '-i', str(path), '-map', '0:a:0',
        '-c', 'copy', '-f', 'hash', '-hash', 'sha256', '-',
    ], text=True).strip()
    return result.split('=', 1)[1]


def collect(index_path):
    exports = []
    for row in read(index_path):
        video = Path(row['file'])
        sha = hashlib.sha256(video.read_bytes()).hexdigest()
        qa_path = Path(row['qa'])
        qa = read(qa_path)
        if sha != row['sha256'] or sha != qa['sha256'] or qa['full_decode'] != 'PASS':
            raise ValueError(f'Export and QA identity disagree for {video}')
        contract_path = qa_path.with_name(qa_path.name.replace('-qa.json', '-contract.json'))
        edit = read(contract_path)
        fps = edit['fps']
        frames = edit['frames']
        cuts = [0, *edit['transition_centres'], frames]
        if len(edit['motion']) != len(edit['clips']) or len(cuts) != len(edit['clips']) + 1:
            raise ValueError(f'Invalid shot map in {contract_path}')
        visual = []
        for slot, (clip, motion) in enumerate(zip(edit['clips'], edit['motion'])):
            start = clip['source_in']
            page = clip.get('source_page')
            visual.append({
                'slot': slot + 1, 'subject': clip.get('subject'), 'scale': clip.get('scale'),
                'source_file': clip['path'], 'source_page': page,
                'source_id': source_identity(clip['path'], page), 'source_sha256': clip['sha256'],
                'source_in_seconds': start, 'source_out_exclusive_seconds': round(start + motion['frames']/fps, 6),
                'visible_timeline_frames': [motion['first_frame'], motion['first_frame'] + motion['frames']],
                'hold_frames': [cuts[slot], cuts[slot+1]],
            })
        start = edit['offset']
        exports.append({
            'file': str(video), 'sha256': sha, 'edit_contract': str(contract_path),
            'fps': fps, 'frames': frames, 'transition_centres': cuts[1:-1],
            'audio': {'source_file': edit['source'], 'source_sha256': edit['source_sha256'],
                      'source_in_seconds': start, 'source_out_exclusive_seconds': round(start + frames/fps, 6),
                      'timeline_frames': [0, frames], 'embedded_packets_sha256': audio_packet_hash(video)},
            'video': visual,
        })
    return exports


def repeated_sources(current, previous):
    seen = {}
    for export in previous:
        for clip in export['video']:
            for key in {clip['source_sha256'], clip.get('source_id')} - {None}:
                seen.setdefault(key, (export['file'], clip['slot']))
    repeated = []
    for export in current:
        for clip in export['video']:
            keys = {clip['source_sha256'], clip.get('source_id')} - {None}
            previous_uses = {seen[key] for key in keys if key in seen}
            for earlier_file, earlier_slot in sorted(previous_uses):
                repeated.append({'file': export['file'], 'slot': clip['slot'],
                                 'earlier_file': earlier_file, 'earlier_slot': earlier_slot})
            for key in keys:
                seen.setdefault(key, (export['file'], clip['slot']))
    return repeated


def repeated_audio(current, previous):
    seen = list(previous)
    result = []
    for export in current:
        audio = export['audio']
        for earlier in seen:
            other = earlier['audio']
            same = audio['source_sha256'] == other['source_sha256']
            start = max(audio['source_in_seconds'], other['source_in_seconds'])
            end = min(audio['source_out_exclusive_seconds'], other['source_out_exclusive_seconds'])
            if same and start < end:
                result.append({'file': export['file'], 'earlier_file': earlier['file'],
                               'overlap_seconds': [start, end]})
        seen.append(export)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--index', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--compare', type=Path, action='append', default=[],
                        help='Previous fragment journal for other active or published edits')
    args = parser.parse_args()
    current = collect(args.index)
    previous = [row for path in args.compare for row in read(path)['exports']]
    video_repeats = repeated_sources(current, previous)
    audio_repeats = repeated_audio(current, previous)
    with args.output.open('x') as file:
        json.dump({'exports': current, 'comparison_journals': [str(p) for p in args.compare],
                   'repeated_video_sources': video_repeats, 'overlapping_audio': audio_repeats},
                  file, ensure_ascii=False, indent=2)
        file.write('\n')
    if video_repeats or audio_repeats:
        print(f'{len(video_repeats)} repeated video sources, {len(audio_repeats)} overlapping audio uses.', file=sys.stderr)
        return 2
    print(f'{len(current)} exports, {sum(len(row["video"]) for row in current)} distinct video source uses.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
