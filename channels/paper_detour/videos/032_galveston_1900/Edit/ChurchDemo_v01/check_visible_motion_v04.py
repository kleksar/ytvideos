"""Matched visible patches in final decoded frames; no source-coordinate inference."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from scipy.signal import fftconvolve
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Edit/QA/full-v04'
R=json.loads((D/'report.json').read_text());F={x['index']:(D/x['path']).resolve() for x in R['frame_map']}
S=json.loads((E/'Storyboard/storyboard_v02.json').read_text())['scenes'];M=json.loads((E/'Edit/ChurchDemo_v01/motion_plan_coverage_v02.json').read_text())['records']
out=[]
for s,m in zip(S,M):
 a,b=s['in_frame'],s['out_frame_exclusive']-1
 im=[np.asarray(Image.open(F[f]).convert('L').resize((640,360),Image.Resampling.LANCZOS),dtype=float) for f in (a,b)]
 matches=[];rad=16;search=75
 for y in [110,180,250]:
  for x in [160,267,373,480]:
   t=im[0][y-rad:y+rad,x-rad:x+rad];t=t-t.mean();tn=np.sqrt((t*t).sum())
   if t.std()<10:continue
   x0=max(0,x-rad-search);y0=max(0,y-rad-search);x1=min(640,x+rad+search);y1=min(360,y+rad+search)
   w=im[1][y0:y1,x0:x1];ones=np.ones(t.shape);n=t.size
   sums=fftconvolve(w,ones[::-1,::-1],mode='valid');sq=fftconvolve(w*w,ones,mode='valid');den=np.sqrt(np.maximum(sq-sums*sums/n,1))*tn
   corr=fftconvolve(w,t[::-1,::-1],mode='valid')/den;iy,ix=np.unravel_index(np.argmax(corr),corr.shape);score=float(corr[iy,ix]);qx=int(x0+ix+rad);qy=int(y0+iy+rad)
   if score>=.72:matches.append({'p':[x,y],'q':[qx,qy],'score':score})
 if len(matches)>=3:
  # Similarity fit separates translation of the picture centre from radial scale.
  A=[];z=[]
  for k in matches:
   x,y=k['p'];qx,qy=k['q'];A.extend([[x-320,-(y-180),1,0],[y-180,x-320,0,1]]);z.extend([qx-320,qy-180])
  v=np.linalg.lstsq(np.asarray(A),np.asarray(z),rcond=None)[0];scale,rotation,dx,dy=map(float,v);pred=np.asarray(A)@v;res=float(np.median(np.abs(pred-z)))
  mode=m['mode'];ok={'pan-right':dx>2,'pan-left':dx< -2,'pan-down':dy>2,'pan-up':dy< -2,'push-in':scale>1.008,'pull-out':scale<.992}[mode]
  result={'scale':scale,'rotation_component':rotation,'centre_dx_640px':dx,'centre_dy_360px':dy,'median_fit_residual_px':res,'direction_agrees':bool(ok),'confidence':'STRONG' if ok and res<6 else 'REVIEW'}
 else:result={'confidence':'REVIEW','reason':'Fewer than3 strong textured patch matches'}
 out.append({'scene_id':s['scene_id'],'frames':[a,b],'requested_mode':m['mode'],'matches':matches,'result':result})
result={'file':R['file'] if 'file' in R else None,'media_sha256':R['sha256'],'method':'Final decoded start/last frames resized640x360;12 textured32x32 patches, local normalized FFT correlation ±75px; retain score≥.72; similarity fit separates radial scale/centre translation. Values are evidence, not a universal framing threshold.','records':out,'needs_review':[x['scene_id'] for x in out if x['result']['confidence']!='STRONG']}
(D/'visible_motion_matches_v02.json').write_text(json.dumps(result,indent=2));print('Scenes',len(out),'strong',len(out)-len(result['needs_review']),'needs review',result['needs_review'])
