import subprocess, json
from pathlib import Path
import numpy as np
from scipy.signal import fftconvolve
from PIL import Image
R=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history/Edit/parallax_inverse_20261102')
for n in range(1,16):
 p=R/f'inverse_{n:02}.mp4'; N=int(json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',str(p)]))['streams'][0]['nb_frames'])-2
 def frame(i):
  d=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf',f'select=eq(n\\,{i}),scale=768:432,format=gray','-vsync','0','-frames:v','1','-f','rawvideo','-'])
  return np.frombuffer(d,np.uint8).reshape(432,768).astype(float)
 a,b=frame(5),frame(N-6); shifts=[]
 for y in (60,140,220,300):
  for x in (80,200,320,440,560,640):
   A=a[y:y+72,x:x+72]; B=b[y-35:y+107,x-35:x+107]; A=A-A.mean()
   numerator=fftconvolve(B,A[::-1,::-1],mode='valid'); ones=np.ones(A.shape); sums=fftconvolve(B,ones,mode='valid'); sq=fftconvolve(B*B,ones,mode='valid'); denom=np.sqrt(np.maximum(sq-sums*sums/A.size,1)*np.sum(A*A)); z=numerator/denom; iy,ix=np.unravel_index(z.argmax(),z.shape)
   shifts.append((int(ix-35),int(iy-35),round(float(z[iy,ix]),2)))
 print(n,shifts,flush=True)
