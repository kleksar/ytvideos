"""Validate chapter syntax and intervals; never certify media review."""
import argparse
import json
import math
import re
import subprocess
from pathlib import Path


def validate(text, duration):
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Duration must be finite and positive')
    chapters = []
    for line in text.splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r'(\d{2,}):(\d{2})(?::(\d{2}))?\s+(.+)', line.strip())
        if not match:
            raise ValueError('Invalid chapter line: ' + line)
        first, second, third, title = match.groups()
        if int(second) >= 60 or (third is not None and int(third) >= 60):
            raise ValueError('Invalid clock components: ' + line)
        seconds = (int(first)*3600 + int(second)*60 + int(third)
                   if third is not None else int(first)*60 + int(second))
        chapters.append({'timestamp': line.strip().split()[0],
                         'seconds': seconds, 'title': title.strip()})
    if len(chapters) < 3 or chapters[0]['seconds'] != 0:
        raise ValueError('Need at least three chapters starting at 00:00')
    for i, chapter in enumerate(chapters):
        end = chapters[i+1]['seconds'] if i+1 < len(chapters) else duration
        if chapter['seconds'] >= duration or end - chapter['seconds'] < 10:
            raise ValueError('Chapter outside media or shorter than 10 seconds: ' + chapter['timestamp'])
        chapter['duration_seconds'] = end - chapter['seconds']
    return {'formal_validation': 'passed', 'media_review': 'not_assessed',
            'duration_seconds': duration, 'chapters': chapters}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('chapters', type=Path)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--media', type=Path)
    source.add_argument('--duration', type=float)
    args = parser.parse_args()
    duration = args.duration
    if args.media:
        duration = float(subprocess.check_output(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(args.media)], text=True).strip())
    try:
        result = validate(args.chapters.read_text(encoding='utf-8'), duration)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
