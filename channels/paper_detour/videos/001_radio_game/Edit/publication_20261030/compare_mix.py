#!/usr/bin/env python3
"""Read-only comparison of candidate and Palmier export. Not a substitute for listening."""
import sys,subprocess,numpy as np
def correlate(x,y,mode): return np.correlate(x,y,mode)
def correlation_lags(n,m): return np.arange(-m+1,n)
if len(sys.argv)!=3: raise SystemExit('Usage: compare_mix.py CANDIDATE.wav PALMIER.mp4')
rate=22050

def block(path,start,duration):
 p=subprocess.run(['ffmpeg','-v','error','-ss',str(start),'-i',path,'-t',str(duration),'-vn','-ac','1','-ar',str(rate),'-f','f32le','pipe:1'],check=True,stdout=subprocess.PIPE)
 return np.frombuffer(p.stdout,np.float32).copy()

def envelope(a,step=441):
 n=len(a)//step
 a=a[:n*step].reshape(n,step)
 return np.sqrt(np.mean(a*a,axis=1))

# All five voice clips covered at multiple positions; each SFX sampled in 2 s window.
marks=[2,12,25,32,36,40,45,65,95,100.6,104,125,155,166,170,174,180,196,203,219,226,230,248,257]
marks+=sorted(set(round(x/30,3) for x in [108,156,1323,1414,2772,2794,3021,3032,3116,4492,4770,5276,5829,6896,7617]))
for start in marks:
 a=envelope(block(sys.argv[1],start,2));b=envelope(block(sys.argv[2],start,2)); n=min(len(a),len(b));a=a[:n];b=b[:n]
 if n<20: print(f'{start:.3f} insufficient');continue
 x=a-a.mean();y=b-b.mean(); cc=correlate(x,y,'full');lags=correlation_lags(n,n);sel=np.abs(lags)<=15;i=np.argmax(cc[sel]);lag=lags[sel][i];corr=cc[sel][i]/(np.linalg.norm(x)*np.linalg.norm(y)+1e-15)
 ar=float(np.sqrt(np.mean(a*a)));br=float(np.sqrt(np.mean(b*b)))
 print(f'{start:8.3f}s rms_candidate={ar:.6f} rms_export={br:.6f} lag20ms={lag:+d} envelope_corr={corr:.3f}')
