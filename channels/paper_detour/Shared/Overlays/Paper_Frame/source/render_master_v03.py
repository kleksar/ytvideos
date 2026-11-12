from pathlib import Path
import argparse, subprocess, time
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates
p=argparse.ArgumentParser();p.add_argument('--width',type=int,default=2560);p.add_argument('--height',type=int,default=1440);p.add_argument('--output',required=True);p.add_argument('--duration',type=float,default=16);p.add_argument('--frame',action='store_true');p.add_argument('--at-time',type=float,default=0);a=p.parse_args()
W,H=a.width,a.height
gen=Path(__file__).resolve().parent/'assets'
def read(prefix): return Image.open(gen/({'ef6a0d90':'layer1.png','2a48f76a':'layer2.png','9c45f38a':'layer3.png'}[prefix])).convert('RGBA')
yy,xx=np.mgrid[:H,:W].astype(np.float32)
layers=[]
for pre,factor in [('ef6a0d90',1),('2a48f76a',1.5),('9c45f38a',2.6)]:
 source=read(pre)
 if W/H<1: source=source.transpose(Image.Transpose.ROTATE_90)
 im=np.asarray(source.resize((W,H),Image.Resampling.LANCZOS))
 factor /= (0.67 * 0.67)  # Approved preview: 44.89% of the original thickness.
 if factor!=1:
  # Thin across each edge, never along it. A smooth corner blend preserves
  # organic texture instead of stretching the midpoint column/row into a line.
  dx=np.minimum(xx,W-1-xx);dy=np.minimum(yy,H-1-yy)
  wt=dx**4/(dx**4+dy**4+1e-6)
  fx=1+(factor-1)*(1-wt);fy=1+(factor-1)*wt
  mx=np.where(xx<W/2,np.minimum(xx*fx,W/2),np.maximum(W-1-(W-1-xx)*fx,W/2))
  my=np.where(yy<H/2,np.minimum(yy*fy,H/2),np.maximum(H-1-(H-1-yy)*fy,H/2))
  im=np.stack([map_coordinates(im[:,:,c],[my,mx],order=1,mode='nearest',prefilter=False) for c in range(4)],axis=-1)
 # Calculate only edge region; full-frame nonzero alpha checked below.
 margin=int(min(W,H)*.16)
 mask=(xx<margin)|(xx>=W-margin)|(yy<margin)|(yy>=H-margin)
 assert not np.any(im[:,:,3][~mask]>2), 'Unexpected interior alpha outside edge region'
 layers.append(im)
idx=np.where(mask);x=xx[idx];y=yy[idx]
wx=np.minimum(x,W-1-x)/W;wy=np.minimum(y,H-1-y)/H;weight=wx/(wx+wy+0.0001)
# Approved displacement is 12 px horizontal and 7 px vertical at 640x360.
ax=12*W/640;ay=7*H/360
fps=30;n=1 if a.frame else round(a.duration*fps)
if not a.frame:
 proc=subprocess.Popen(['ffmpeg','-n','-v','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{W}x{H}','-r',str(fps),'-i','-','-an','-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le','-alpha_bits','16','-threads','2',a.output],stdin=subprocess.PIPE)
t0=time.time()
for k in range(n):
 t=(a.at_time if a.frame else k/fps);edge=np.zeros((len(x),3),np.float32);coverage=np.zeros((len(x),1),np.float32)
 for j,im in enumerate(layers):
  period=(16.0,8.0,16.0/3.0)[j]
  phase=j*1.2
  mx=np.clip(x+ax*weight*np.sin(2*np.pi*(x/W-t/period)+phase),0,W-1)
  my=np.clip(y+ay*(1-weight)*np.sin(2*np.pi*(y/H-t/period)+phase),0,H-1)
  rgba=np.stack([map_coordinates(im[:,:,c],[my,mx],order=1,mode='nearest',prefilter=False) for c in range(4)],axis=-1).astype(np.float32)
  alpha=rgba[:,3:4]/255
  edge=rgba[:,:3]*alpha+edge*(1-alpha)
  coverage=alpha+coverage*(1-alpha)
 straight=np.divide(edge,coverage,out=np.zeros_like(edge),where=coverage>0)
 frame=np.zeros((H,W,4),np.uint8)
 frame[idx]=np.clip(np.rint(np.concatenate([straight,coverage*255],axis=1)),0,255).astype(np.uint8)
 if a.frame: Image.fromarray(frame).save(a.output)
 else: proc.stdin.write(frame.tobytes())
 if k%30==0: print(f'{k}/{n} frames {time.time()-t0:.1f}s',flush=True)
if not a.frame:
 proc.stdin.close(); assert proc.wait()==0
print('DONE',a.output,flush=True)
