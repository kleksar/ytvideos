#!/usr/bin/env python3
"""Rebuild only the delivered soundtrack from approved sources; never edits Palmier."""
import argparse
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
INTRO = PROJECT / 'Source/Voice/002_en_intro_voice_original.mp3'
MAIN = PROJECT / 'Source/Voice/ElevenLabs_At_first,_lightweight_white_stones_began_.mp3'

# Palmier 002_en_long (7D4B5711), 30 fps, 44.1 kHz mono.
# Clip windows: [0,789), [789,1024), [1024,26914); each plays at 1.05x.
# Intro source trim: clip 1 ends ~27.615 s; clip 2 begins at 841/30 s.
FILTER = (
    '[1:a]atrim=start_sample=0:end_sample=1217822,asetpts=PTS-STARTPTS,'
    'atempo=1.05,apad,atrim=end_sample=1159830,asetpts=PTS-STARTPTS[a0];'
    '[1:a]atrim=start_sample=1236270,asetpts=PTS-STARTPTS,'
    'atempo=1.05,apad,atrim=end_sample=345450,asetpts=PTS-STARTPTS[a1];'
    '[2:a]atempo=1.05,apad,atrim=end_sample=38058300,'
    'asetpts=PTS-STARTPTS[a2];'
    '[a0][a1][a2]concat=n=3:v=0:a=1[aout]'
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--video-input', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    video = args.video_input.resolve()
    output = args.output.resolve()
    for item in (video, INTRO, MAIN):
        if not item.is_file():
            parser.error(f'missing input: {item}')
    if output.exists():
        parser.error(f'output already exists: {output}')
    cmd = [
        'ffmpeg', '-hide_banner', '-v', 'error', '-xerror', '-n',
        '-i', str(video), '-i', str(INTRO), '-i', str(MAIN),
        '-filter_complex', FILTER,
        '-map', '0:v:0', '-map', '[aout]',
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
        '-ar', '44100', '-ac', '1', '-movflags', '+faststart',
        str(output),
    ]
    subprocess.run(cmd, check=True)
    print(output)


if __name__ == '__main__':
    main()
