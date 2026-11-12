from pathlib import Path
from PIL import Image
import numpy as np,json
ep=Path(__file__).resolve().parents[2]
qa=ep/'Edit/QA'
run=qa/'brocklesby-en-v01'
r=json.loads((run/'report.json').read_text())
mp={x['index']:run/x['path'] for x in r['frame_map']}
m=json.loads((ep/'Edit/montage-v01.json').read_text())
measurements=[]
def gray(k):
 with Image.open(mp[k]) as im:
  return np.asarray(im.convert('L').resize((360,640),Image.Resampling.LANCZOS),dtype=np.float32)
for i,s in enumerate(m['scenes'],1):
 a,b=s['camera']['start'],s['camera']['end']
 k0,k1=s['start_frame'],s['end_frame']-1
 v0,v1=gray(k0),gray(k1)
 pts=[]
 for y in (120,200,280,360,420):
  for x in (78,130,180,230,282):
   src=v0[y-8:y+9,x-8:x+9]
   src=src-src.mean()
   if src.std()<12: continue
   tx=(x-180)/a['scale']+360*a['center'][0]
   ty=(y-320)/a['scale']+640*a['center'][1]
   ex=(tx-360*b['center'][0])*b['scale']+180
   ey=(ty-640*b['center'][1])*b['scale']+320
   xx,yy=round(ex),round(ey)
   arr=v1[yy-14:yy+15,xx-14:xx+15]
   win=np.lib.stride_tricks.sliding_window_view(arr,(17,17)).copy()
   win-=win.mean(axis=(-1,-2),keepdims=True)
   scores=(win*src).mean(axis=(-1,-2))/np.maximum(win.std(axis=(-1,-2))*src.std(),1e-5)
   iy,ix=np.unravel_index(scores.argmax(),scores.shape)
   if scores[iy,ix]>.90: pts.append((x,y,xx+ix-6,yy+iy-6,ex,ey,float(scores[iy,ix])))
 err=np.array([[p[2]-p[4],p[3]-p[5]] for p in pts])
 assert len(pts)>=5 and float(np.median(np.linalg.norm(err,axis=1)))<1.2
 fit=np.linalg.lstsq([[x-180,1] for x,y,xp,yp,ex,ey,c in pts],[xp-x for x,y,xp,yp,ex,ey,c in pts],rcond=None)[0]
 measurements.append(dict(scene=f'S{i:03d}',sample_frames=[k0,k1],matches=len(pts),median_endpoint_error_px=float(np.median(np.linalg.norm(err,axis=1))),visible_midline_translation_x_px=float(fit[1]),visible_scale_ratio=float(fit[0]+1),requested_direction=s['direction'],requested_zoom=s['zoom']))
(qa/'motion-v01.json').write_text(json.dumps(dict(phone_width_px=360,method='Decoded first/last grayscale texture patch matching; source affine endpoint predictions. Interior features only; no overlay or captions.',scenes=measurements),indent=2)+'\n')
print(measurements)
