#!/usr/bin/env python3
"""Isolated draft grain test; does not change Palmier or channel defaults.

Run with automation/image_motion/.venv/bin/python render_grain.py preset.json.
Requires FFmpeg, numpy and scipy. Streams frames; no long overlay master.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter


def read_exact(stream, size):
    parts = bytearray()
    while len(parts) < size:
        data = stream.read(size - len(parts))
        if not data:
            raise RuntimeError(f"Incomplete source frame: {len(parts)}/{size}")
        parts.extend(data)
    return parts


def render(preset_path):
    p = json.loads(preset_path.read_text())
    root = preset_path.parent
    source = (root / p['source']).resolve()
    output = root / p['output']
    if output.exists():
        raise FileExistsError(f"Refusing to replace {output}")
    w, h, fps, count = (p[k] for k in ('width', 'height', 'fps', 'frames'))
    assert w % 2 == h % 2 == 0 and count > 0
    start = p['start_frame'] / fps
    duration = count / fps
    temporary = root / 'video_only.partial.mp4'
    dec_cmd = ['ffmpeg','-v','error','-ss',str(start),'-i',str(source),
               '-map','0:v:0','-frames:v',str(count),'-vf',
               f'scale={w}:{h}:flags=lanczos:in_range=tv:out_range=tv,setsar=1',
               '-pix_fmt','yuv420p','-f','rawvideo','pipe:1']
    enc_cmd = ['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','yuv420p',
               '-video_size',f'{w}x{h}','-framerate',str(fps),'-i','pipe:0',
               '-an','-c:v','libx264','-preset','fast','-tune','grain','-threads','8',
               '-profile:v','high','-b:v',p['video_bitrate'],'-maxrate','60M',
               '-bufsize','90M','-g','15','-bf','2','-x264-params','open-gop=0',
               '-color_range','tv','-colorspace','bt709','-color_trc','bt709',
               '-color_primaries','bt709','-movflags','+faststart',str(temporary)]
    rng = np.random.default_rng(p['seed'])
    knots = np.asarray(p['mask_knots_limited_range'])
    mask_lut = np.interp(np.arange(256),knots[:,0],knots[:,1]).astype(np.float32)
    rho = p['temporal_rho']
    assert 0 <= rho < 1
    innovation_weight = math.sqrt(1-rho*rho)
    state = None
    y_size = w*h
    frame_bytes = y_size*3//2
    stats = []
    samples = {0, 80, 164, 243, 322, 400, 449}
    dec_log = (root/'decode.log').open('w')
    enc_log = (root/'encode.log').open('w')
    dec = subprocess.Popen(dec_cmd,stdout=subprocess.PIPE,stderr=dec_log)
    enc = subprocess.Popen(enc_cmd,stdin=subprocess.PIPE,stderr=enc_log)
    try:
        for i in range(count):
            frame = read_exact(dec.stdout,frame_bytes)
            y = np.frombuffer(frame,dtype=np.uint8,count=y_size).reshape(h,w).copy()
            innovation = rng.standard_normal((h,w),dtype=np.float32)
            gaussian_filter(innovation,p['gaussian_sigma_px'],output=innovation,mode='reflect')
            innovation -= innovation.mean()
            innovation /= innovation.std()
            if state is None:
                state = innovation
            else:
                state *= rho
                state += innovation_weight*innovation
            noise = state*p['luma_rms_codes']*mask_lut[y]
            out_y = np.clip(np.rint(y.astype(np.float32)+noise),16,235).astype(np.uint8)
            frame[:y_size] = out_y.tobytes()
            enc.stdin.write(frame)
            if i in samples:
                d = out_y.astype(np.float32)-y
                stats.append({'frame':i,'applied_rms_codes':float(np.sqrt(np.mean(d*d))),
                              'unmasked_state_std':float(state.std()),
                              'chroma_input_untouched':True})
                if i in (80,243,400):
                    # Raw originals and modified pairs allow exact pre-encode QA.
                    (root/f'sample_{i:03}_clean.yuv').write_bytes(y.tobytes()+frame[y_size:])
                    (root/f'sample_{i:03}_grain.yuv').write_bytes(frame)
            if i % 30 == 0:
                print(f'{i}/{count}',flush=True)
        enc.stdin.close()
        if dec.wait() or enc.wait():
            raise RuntimeError('FFmpeg failed; inspect decode.log/encode.log')
    except BaseException:
        dec.kill(); enc.kill()
        raise
    finally:
        dec_log.close(); enc_log.close()
    # Reuse accepted existing audio packets. No new sound or mix is synthesized.
    mux_cmd = ['ffmpeg','-v','error','-i',str(temporary),'-ss',str(start),'-i',str(source),
               '-map','0:v:0','-map','1:a:0?','-c','copy','-t',str(duration),
               '-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0',
               '-color_range','tv','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709',
               '-movflags','+faststart',str(output)]
    subprocess.run(mux_cmd,check=True)
    report = {'preset':p,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
              'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
              'output_bytes':output.stat().st_size,'samples':stats,
              'decode_command':dec_cmd,'encode_command':enc_cmd,'mux_command':mux_cmd,
              'audio':'existing accepted source AAC stream copied; not remixed',
              'limitations':['Post-composite test: existing paper text is also grained.',
                             '1080p source upscaled; this does not create new scene detail.',
                             'Local grain settings do not guarantee YouTube preservation.']}
    (root/'render_receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    temporary.unlink()
    print(output,flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('preset',type=Path)
    render(parser.parse_args().preset.resolve())
