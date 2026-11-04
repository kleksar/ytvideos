#!/usr/bin/env python3
"""Render accepted opposed-v06 motion from a prepared RGBA foreground and restored background.

The mask and background must be separately prepared and visually checked; this
renderer does not perform automatic segmentation, inpainting, or Palmier edits.
"""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import time

from PIL import Image

HERE = Path(__file__).resolve().parent
PRESET = json.loads((HERE / 'layered_presets.json').read_text())['opposed-v06']


def render(foreground, background, output, direction, frames,
           camera_scale=None, camera_travel_fraction=None, camera_crop_y=None,
           output_width=1920, output_height=1080):
    start = time.monotonic()
    fg = Image.open(foreground).convert('RGBA')
    bg = Image.open(background).convert('RGBA')
    if fg.size != bg.size:
        raise ValueError('Foreground and background must have the same dimensions')
    if frames < 2:
        raise ValueError('At least two frames required')
    if (output_width % 2 or output_height % 2 or min(output_width, output_height) < 16
            or abs((output_width / output_height) - (fg.width / fg.height)) > 0.002):
        raise ValueError('Output must have even dimensions and preserve the source aspect ratio')
    width, height = fg.size
    travel = PRESET['foreground_travel_px'] * width / PRESET['reference_width']
    # Pillow inverse transform: positive coefficient translates the picture left.
    left = direction == 'parallax-left-camera-right'
    sign = 1 if left else -1
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite {output}')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='layered-motion-') as tmp:
        raw = Path(tmp) / 'parallax.mp4'
        output_size = f'{output_width}x{output_height}'
        set_bt709 = ('setparams=range=limited:color_primaries=bt709:'
                     'color_trc=bt709:colorspace=bt709')
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s',
               f'{width}x{height}', '-r', str(PRESET['fps']), '-i', 'pipe:0', '-vf',
               f'scale={output_size}:flags=lanczos,setsar=1,{set_bt709}', '-c:v', 'libx264', '-crf', '16',
               '-preset', 'fast', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
               '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv', '-an', str(raw)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        try:
            for i in range(frames):
                dx = sign * travel * i / (frames - 1)
                moved = fg.transform((width, height), Image.Transform.AFFINE, (1, 0, dx, 0, 1, 0),
                                     resample=Image.Resampling.BICUBIC)
                proc.stdin.write(Image.alpha_composite(bg, moved).tobytes())
            proc.stdin.close()
            if proc.wait() != 0:
                raise RuntimeError('Parallax encoder failed')
        except BaseException:
            proc.kill()
            proc.wait()
            raise
        mid = time.monotonic()
        # Positive x translates the full image right; directions are opposed.
        # perspective's default source-coordinate mapping has the inverse visual sign.
        camera_sign = -1 if left else 1
        scale = PRESET['camera_scale'] if camera_scale is None else camera_scale
        travel_fraction = (PRESET['camera_travel_width_fraction'] if camera_travel_fraction is None
                           else camera_travel_fraction)
        if scale < 1.0 or scale > 1.2 or travel_fraction < 0 or travel_fraction > 0.1:
            raise ValueError('Camera scale must be 1.0–1.2 and travel fraction 0–0.1')
        travel_px = output_width * travel_fraction
        expression = f'{camera_sign}*(-{travel_px / 2}+{travel_px}*on/{frames-1})'
        camera_width = round(output_width * scale)
        camera_height = round(output_height * scale)
        crop_x = (camera_width - output_width) // 2
        centered_y = (camera_height - output_height) // 2
        crop_y = centered_y if camera_crop_y is None else camera_crop_y
        if not 0 <= crop_y <= camera_height - output_height:
            raise ValueError(f'Camera crop y {crop_y} outside 0–{camera_height - output_height}')
        vf = (f"scale={camera_width}:{camera_height}:flags=lanczos,perspective=x0='{expression}':y0=0:"
              f"x1='W+({expression})':y1=0:x2='{expression}':y2=H:"
              f"x3='W+({expression})':y3=H:interpolation=cubic:eval=frame,"
              f'crop={output_width}:{output_height}:{crop_x}:{crop_y},setsar=1,{set_bt709}')
        try:
            subprocess.run(['ffmpeg', '-v', 'error', '-n', '-i', str(raw), '-vf', vf,
                            '-frames:v', str(frames), '-c:v', 'libx264', '-crf', '16',
                            '-preset', 'fast', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
                            '-color_trc', 'bt709', '-colorspace', 'bt709', '-color_range', 'tv',
                            '-an', str(output)], check=True)
        except BaseException:
            output.unlink(missing_ok=True)
            raise
    print(json.dumps({'output': str(output), 'direction': direction, 'frames': frames,
                      'width': output_width, 'height': output_height,
                      'camera_scale': scale, 'camera_travel_width_fraction': travel_fraction,
                      'camera_crop_y': crop_y,
                      'parallax_seconds': round(mid-start, 2),
                      'camera_seconds': round(time.monotonic()-mid, 2),
                      'total_seconds': round(time.monotonic()-start, 2)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--foreground', type=Path, required=True)
    parser.add_argument('--background', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--direction', choices=PRESET['directions'], required=True)
    parser.add_argument('--frames', type=int, default=180)
    parser.add_argument('--camera-scale', type=float)
    parser.add_argument('--camera-travel-width-fraction', type=float)
    parser.add_argument('--camera-crop-y', type=int,
                        help='Vertical crop origin in the scaled output canvas; defaults to center')
    parser.add_argument('--output-width', type=int, default=1920,
                        help='Even output width (default 1920, the accepted sample canvas)')
    parser.add_argument('--output-height', type=int, default=1080,
                        help='Even output height (default 1080, the accepted sample canvas)')
    args = parser.parse_args()
    render(args.foreground, args.background, args.output, args.direction, args.frames,
           args.camera_scale, args.camera_travel_width_fraction, args.camera_crop_y,
           args.output_width, args.output_height)


if __name__ == '__main__':
    main()
