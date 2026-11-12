"""Read-only normalized patch matching on actual rendered frames; not a renderer."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.signal import fftconvolve
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
raw={r['scene']:r for r in json.loads((ROOT/'Edit/v13/QA/depth_sample_map.json').read_text())}
report=json.loads((HERE/'QA/technical/report.json').read_text())
frames={r['index']:HERE/'QA/technical'/r['path'] for r in report['frame_map']}
plan=json.loads((HERE/'qa-plan-v14.json').read_text())
parameters=json.loads((ROOT/'Edit/ComplianceAudit_20261102/MOTION_PARAMETER_AUDIT.json').read_text())
def gray(p):
 with Image.open(p) as im:return np.asarray(im.convert('L').resize((960,540)),dtype=float)
def flow(pa,pb):
 a,b=gray(pa),gray(pb);matches=[];half=36;search=28;ones=np.ones((72,72))
 for y in [180,280,380,460]:
  for x in [140,280,420,560,700,840]:
   patch=a[y-half:y+half,x-half:x+half]; patch=patch-patch.mean()
   if patch.std()<7:continue
   area=b[y-half-search:y+half+search,x-half-search:x+half+search]
   cross=fftconvolve(area,patch[::-1,::-1],mode='valid')
   sm=fftconvolve(area,ones,mode='valid');ss=fftconvolve(area*area,ones,mode='valid')
   score=cross/np.sqrt(np.maximum(ss-sm*sm/patch.size,1e-8)*np.sum(patch*patch))
   py,px=np.unravel_index(score.argmax(),score.shape);best=float(score[py,px]);rest=score.copy();rest[max(0,py-2):py+3,max(0,px-2):px+3]=-1
   if best<.80 or best-float(rest.max())<.003 or px in [0,56] or py in [0,56]:continue
   matches.append({'x':x,'y':y,'dx_960':int(px-search),'dy_540':int(py-search),'correlation':round(best,4)})
 lower=[m for m in matches if m['y']>=280]
 chosen=lower if len(lower)>=4 else matches
 dx=float(np.median([m['dx_960'] for m in chosen])) if chosen else None
 return {'matches':matches,'strong_count':len(matches),'lower_count':len(lower),'median_dx_960':dx,'visible_direction':'right' if dx is not None and dx>=1 else 'left' if dx is not None and dx<=-1 else 'UNVERIFIED_negligible_or_weak'}
rows=[]
for s,p in zip(plan['scenes'],parameters):
 d=flow(raw[s['id']]['files'][0],raw[s['id']]['files'][2]);f=flow(frames[s['start']],frames[s['end']-1]);horizontal=abs(p['dx'])>.0025
 direction='right' if p['dx']>0 else 'left'
 agreement='PASS' if horizontal and d['visible_direction']==direction else 'UNVERIFIED' if horizontal else 'N_A_zoom_or_vertical'
 mode=('push-in' if p['scale_delta']>0 else 'pull-out') if abs(p['scale_delta'])>.001 else ('pan-right' if p['dx']>0 else 'pan-left') if horizontal else ('pan-down' if p['dy']>0 else 'pan-up')
 rows.append({**p,'mode':mode,'camera_direction':direction if horizontal else 'zoom_or_vertical','depth_features':d,'final_features':f,'horizontal_alignment':agreement})
(HERE/'MOTION_FEATURE_AUDIT.json').write_text(json.dumps({'method':'Normalized FFT template matching on72pxpatches,960x540;minimumcorrelation.80;medianofstronglower-framefeatures. Weak/negligible matches never prove direction. Camera centre from actual API position+scale/2.','rows':rows},indent=2)+'\n')
print(json.dumps({'horizontal':sum(abs(r['dx'])>.0025 for r in rows),'direction_pass':sum(r['horizontal_alignment']=='PASS' for r in rows),'unverified':[{'scene':r['scene'],'camera':r['camera_direction'],'depth':r['depth_features']['visible_direction'],'dx':r['depth_features']['median_dx_960']} for r in rows if r['horizontal_alignment']=='UNVERIFIED']},indent=2))
