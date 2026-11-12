#!/usr/bin/env python3
"""Create an FFmpeg highlight pulse stage from music_beats.py candidates."""
import argparse
import json
from pathlib import Path


def build_stage(data, fps, strength=0.8, radius_frames=5.0):
    if data.get('fps') != fps:
        raise ValueError('Beat map FPS does not match the edit')
    frames = sorted({int(event['frame']) for event in data.get('candidates', [])})
    if not frames:
        raise ValueError('No detected beat candidates; inspect the audio before rendering')
    if not 0 < strength <= 1 or not 0 < radius_frames <= fps / 4:
        raise ValueError('Invalid pulse strength or duration')
    envelope = '+'.join(
        f'(1+cos(PI*min(abs(T*{fps}-{frame})/{radius_frames},1)))/2' for frame in frames
    )
    stage = (
        '[pre_pulse]split[pulse_base][pulse_high];\n'
        "[pulse_high]lutyuv=y='max(val,min(235,90+1.35*(val-90)))':u=val:v=val[pulse_boost];\n"
        f"[pulse_base][pulse_boost]blend=c0_expr='A+(B-A)*min(1,{strength}*({envelope}))':"
        "c1_expr='A':c2_expr='A'[vbase];\n"
    )
    return stage, frames


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('beats', type=Path)
    parser.add_argument('--fps', type=int, required=True)
    parser.add_argument('--strength', type=float, default=0.8)
    parser.add_argument('--radius-frames', type=float, default=5.0)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    stage, frames = build_stage(json.loads(args.beats.read_text()), args.fps, args.strength, args.radius_frames)
    args.output.write_text(stage)
    print(f'{len(frames)} beat pulses; frames: {frames}')


if __name__ == '__main__':
    main()
