from pathlib import Path
import subprocess, sys, json
import numpy as np
repo=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(repo/'automation'))
from music_beats import attacks, RATE, HOP
batch=repo/'Work/nuviko-four-shorts-20261110'
step=HOP/RATE

def analysis(path):
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-ac','1','-ar',str(RATE),'-f','f32le','-'])
    x=np.frombuffer(raw,'<f4')
    t,s,f=attacks(x)
    powers=np.abs(np.fft.rfft(np.lib.stride_tricks.sliding_window_view(np.pad(x,512),1024)[::HOP]*np.hanning(1024),axis=1))
    low=powers[:,2:7].sum(axis=1)
    low=np.log1p(low/max(0.001,np.percentile(low,85)*.06))
    low=np.maximum(0,low[6:]-low[:-6])
    low=np.interp(t,(np.arange(len(low))+3)*step,low)
    low/=max(1e-6,np.percentile(low,95))
    bands=np.vstack([low, *f])
    return t,bands

def peaks(t, s):
    chosen=[]
    for k in np.argsort(s)[::-1]:
        if not all(abs(t[k]-t[j])>0.11 for j in chosen): continue
        chosen.append(k)
        if len(chosen)==44: break
    return sorted(chosen)

