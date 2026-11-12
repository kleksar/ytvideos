#!/usr/bin/env python3
"""Render one silent controlled grain comparison, streaming into one encoder."""
import hashlib
import json
import math
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
W, H, FPS, HOLD, SLATE, BAR = 2560, 1440, 30, 120, 8, 1248
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_layer(shape, text, xy, size, bold=False):
    im = Image.new('L', shape, 0)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(BOLD if bold else FONT, size)
    box = draw.textbbox(xy, text, font=font)
    assert 0 <= box[0] and box[2] < shape[0] and box[3] < shape[1], box
    draw.text(xy, text, fill=255, font=font)
    return np.asarray(im, dtype=np.float32) / 255


def label(base, p, slate=False):
    y = np.full((H, W), 25, np.float32) if slate else base.astype(np.float32).copy()
    if not slate:
        y[BAR:] = 16 + (y[BAR:] - 16) * .17
    title = f"{p['id']:02d}  {p['name']}"
    settings = f"RMS {p['rms']:.1f} / 255    |    Size sigma {p['sigma']:.2f} px    |    {p['hz']} Hz    |    rho {p['rho']:.2f}"
    layers = [(title, (84, 485), 124, True), (settings, (84, 680), 52, False)] if slate else [
        (title, (72, BAR + 22), 64, True), (settings, (72, BAR + 108), 43, False)]
    for s, xy, size, bold in layers:
        a = text_layer((W, H), s, xy, size, bold)
        y = y*(1-a) + 226*a
    return np.rint(y).astype(np.uint8), settings


def main():
    config = json.loads((HERE/'presets.json').read_text())
    run = ROOT/'Work/matrix10-v01'
    output = run/'previews/PAPER_DETOUR_GRAIN_10_PRESETS_1440P_v01.mp4'
    assert not output.exists(), output
    assert len(config['presets']) == 10
    source = run/'scratch/base_1440.yuv'
    raw = source.read_bytes()
    n = W*H
    assert len(raw) == n*3//2
    base = np.frombuffer(raw, np.uint8, count=n).reshape(H,W).copy()
    uv = np.frombuffer(raw, np.uint8, offset=n).copy().reshape(2,H//2,W//2)
    uv[:, BAR//2:] = np.rint(128+(uv[:, BAR//2:].astype(np.float32)-128)*.17).astype(np.uint8)
    picture_uv = uv.tobytes()
    slate_uv = bytes([128])*(n//2)
    mask = np.interp(base, [0,20,64,208,235,255], [0,0,1,1,0,0]).astype(np.float32)
    mask[BAR:] = 0
    cmd = ['ffmpeg','-hide_banner','-v','error','-n','-f','rawvideo','-pixel_format','yuv420p',
           '-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-an',
           '-vf','setsar=1','-c:v','libx264','-preset','fast','-tune','grain','-crf','16','-threads','8',
           '-profile:v','high','-g','15','-bf','2','-x264-params','open-gop=0',
           '-color_range','tv','-colorspace','bt709','-color_trc','bt709','-color_primaries','bt709',
           '-bsf:v','h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0',
           '-use_editlist','0','-movflags','+faststart+negative_cts_offsets',str(output)]
    started = time.monotonic()
    receipts = []
    with (HERE/'encode.log').open('w') as log:
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=log)
        try:
            for p in config['presets']:
                assert p['hz'] in (10,15,30) and 0 <= p['rho'] < 1
                frame_y, settings = label(base,p)
                card_y, _ = label(base,p,True)
                card = card_y.tobytes()+slate_uv
                for _ in range(SLATE): enc.stdin.write(card)
                rng = np.random.default_rng(config['seed'])
                state = None
                step = FPS//p['hz']
                metrics = []
                for i in range(HOLD):
                    if i % step == 0:
                        innovation = rng.standard_normal((BAR,W), dtype=np.float32)
                        gaussian_filter(innovation, p['sigma'], output=innovation, mode='reflect')
                        innovation -= innovation.mean()
                        innovation /= innovation.std()
                        if state is None: state = innovation
                        else:
                            state *= p['rho']
                            state += math.sqrt(1-p['rho']**2)*innovation
                        noise = state*p['rms']*mask[:BAR]
                        out = frame_y.copy()
                        out[:BAR] = np.clip(np.rint(base[:BAR].astype(np.float32)+noise),16,235).astype(np.uint8)
                        payload = out.tobytes()+picture_uv
                    enc.stdin.write(payload)
                    if i in (0,1,2,59,60,119):
                        d = out[:BAR].astype(np.float32)-base[:BAR]
                        metrics.append({'frame':i,'applied_rms':float(np.sqrt(np.mean(d*d))),
                                        'unmasked_state_std':float(state.std()),
                                        'y_sha256':hashlib.sha256(out.tobytes()).hexdigest(),
                                        'chroma_unchanged_above_label':True})
                    if i == 60:
                        (run/f'scratch/expected_{p["id"]:02d}.yuv').write_bytes(payload)
                receipts.append({'preset':p,'slate_start':(p['id']-1)*(HOLD+SLATE),
                                 'image_start':(p['id']-1)*(HOLD+SLATE)+SLATE,
                                 'image_frames':HOLD,'slate_frames':SLATE,'settings_label':settings,'metrics':metrics})
                print(f"Preset {p['id']:02d}/10 complete; {time.monotonic()-started:.0f}s elapsed",flush=True)
            enc.stdin.close()
            assert enc.wait() == 0, 'See encode.log'
        except BaseException:
            enc.kill(); enc.wait()
            raise
    receipt = {'file':str(output),'sha256':sha(output),'bytes':output.stat().st_size,
               'source_yuv_sha256':sha(source),'command':cmd,'frames':10*(HOLD+SLATE),
               'duration':10*(HOLD+SLATE)/FPS,'segments':receipts,'elapsed_seconds':time.monotonic()-started,
               'source_image_sha256':sha(ROOT/'Source/watchmaker_user.png'),
               'colour':'sRGB source converted to BT709 limited before grain; tags and SPS set',
               'audio':'N_A; silent visual experiment, no audio created',
               'labels':'Static neutral labels after grain; lower panel excluded from grain',
               'production_defaults_changed':False}
    (HERE/'render_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(output,flush=True)


if __name__ == '__main__':
    main()
