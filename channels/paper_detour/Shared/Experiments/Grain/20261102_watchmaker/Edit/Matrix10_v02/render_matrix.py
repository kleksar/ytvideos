"""Same120-frame camera/depth sequence for ten grain settings;30-frame cards."""
import hashlib
import importlib.util
import json
import math
import subprocess
import time
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('grain_v01',ROOT/'Edit/Matrix10_v01/render_matrix.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
W,H,FPS,HOLD,SLATE,BAR=2560,1440,30,120,30,1248
N=W*H;FB=N*3//2


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    config=json.loads((HERE/'presets.json').read_text())
    contract=json.loads((HERE/'EXPORT_CONTRACT_v02.json').read_text());assert contract['status']=='READY_TO_RENDER'
    output=Path(contract['output']);assert not output.exists()
    run=ROOT/'Work/matrix10-v02-motion'
    # Decode/scale/colour-convert once;120frames stay in RAM, not a raw disk master.
    dec=json.loads((HERE/'common_motion_decode.json').read_text())['command']
    raw=subprocess.check_output(dec);assert len(raw)==HOLD*FB
    common=np.frombuffer(raw,np.uint8).reshape(HOLD,FB)
    common_hash=hashlib.sha256(raw).hexdigest()
    middle=common[60].tobytes();(run/'scratch/clean_middle.yuv').write_bytes(middle)
    first=common[0,:N].reshape(H,W)
    mask_lut=np.interp(np.arange(256),[0,20,64,208,235,255],[0,0,1,1,0,0]).astype(np.float32)
    old=json.loads((ROOT/'Edit/Matrix10_v01/render_receipt.json').read_text())['command']
    cmd=old[:-1]
    at=cmd.index('-an')+1;cmd[at:at]=['-vf','setsar=1']
    cmd[cmd.index('-movflags')+1]='+faststart+negative_cts_offsets'
    cmd.append(str(output))
    begun=time.monotonic();segments=[]
    with (HERE/'encode.log').open('w') as log:
        enc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        try:
            for p in config['presets']:
                card,settings=g.label(first,p,True)
                cardbytes=card.tobytes()+bytes([128])*(N//2)
                for _ in range(SLATE): enc.stdin.write(cardbytes)
                title=f"{p['id']:02d}  {p['name']}"
                a1=g.text_layer((W,H-BAR),title,(72,22),64,True)
                a2=g.text_layer((W,H-BAR),settings,(72,108),43,False)
                alpha=np.maximum(a1,a2)
                rng=np.random.default_rng(config['seed']);state=None;step=FPS//p['hz'];samples=[];updates=0
                for i in range(HOLD):
                    clean=common[i,:N].reshape(H,W)
                    if i%step==0:
                        innovation=rng.standard_normal((BAR,W),dtype=np.float32)
                        gaussian_filter(innovation,p['sigma'],output=innovation,mode='reflect')
                        innovation-=innovation.mean();innovation/=innovation.std()
                        if state is None: state=innovation
                        else:
                            state*=p['rho'];state+=math.sqrt(1-p['rho']**2)*innovation
                        updates+=1
                    # Hold only the NOISE field at15/10Hz; underlying video remains30Hz.
                    noise=state*p['rms']*mask_lut[clean[:BAR]]
                    y=clean.copy();y[:BAR]=np.clip(np.rint(clean[:BAR].astype(np.float32)+noise),16,235).astype(np.uint8)
                    panel=16+(clean[BAR:].astype(np.float32)-16)*.17
                    y[BAR:]=np.rint(panel*(1-alpha)+226*alpha).astype(np.uint8)
                    uv=common[i,N:].copy().reshape(2,H//2,W//2)
                    uv[:,BAR//2:]=np.rint(128+(uv[:,BAR//2:].astype(np.float32)-128)*.17).astype(np.uint8)
                    payload=y.tobytes()+uv.tobytes();enc.stdin.write(payload)
                    if i in (0,1,2,30,60,90,119):
                        d=y[:BAR].astype(np.float32)-clean[:BAR]
                        samples.append({'frame':i,'applied_rms':float(np.sqrt(np.mean(d*d))),
                                        'noise_field_sha256':hashlib.sha256(state.tobytes()).hexdigest(),
                                        'clean_frame_sha256':hashlib.sha256(common[i].tobytes()).hexdigest()})
                    if i==60: (run/f'scratch/expected_{p["id"]:02d}.yuv').write_bytes(payload)
                segments.append({'preset':p,'slate_start':(p['id']-1)*150,'slate_frames':30,
                                 'image_start':(p['id']-1)*150+30,'image_frames':120,
                                 'noise_field_updates':updates,'settings_label':settings,'metrics':samples,
                                 'common_sequence_sha256':common_hash})
                print(f"Preset{p['id']:02d}/10 complete;{time.monotonic()-begun:.0f}s",flush=True)
            enc.stdin.close();assert enc.wait()==0,'Inspect encode.log'
        except BaseException:
            enc.kill();enc.wait();raise
    receipt={'file':str(output),'sha256':sha(output),'bytes':output.stat().st_size,'frames':1500,'duration':50,
             'segments':segments,'command':cmd,'common_motion_decode_command':dec,'common_sequence_sha256':common_hash,
             'common_sequence_frames':120,'source_image_sha256':sha(ROOT/'Source/watchmaker_user.png'),
             'contract_sha256':sha(HERE/'EXPORT_CONTRACT_v02.json'),'elapsed_seconds':time.monotonic()-begun,
             'notes':['Exactly same30fps motion sequence in all10variants, including15/10Hzgrain','No audio created','Screen-coordinate grain added after camera/depth;labels not grained','Old static comparison retained;no universal preset adopted']}
    (HERE/'render_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(output,flush=True)


if __name__=='__main__': main()
