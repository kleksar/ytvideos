from pathlib import Path
import json,importlib.util
from PIL import Image,ImageDraw
ROOT=Path('/Users/diplomat/ytvideos'); EP=ROOT/'channels/paper_detour/videos/032_galveston_1900'; W=EP/'Edit/Motion_v01'
spec=importlib.util.spec_from_file_location('motion',ROOT/'automation/image_motion/run.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
b=json.loads((W/'baseline_live.json').read_text()); manifest=json.loads((EP/'Edit/Review_v01/static_review_manifest_v01.json').read_text())
for cue in manifest['cues']:
 if cue['id'] in ['C14','C15']:
  cue['transform']['centerX']-=.28
  cue['placement_source']='Motion v02 alternate visible anchor X=.22 Y=.20; protect church roof/crosses'
(W/'cue_motion_manifest_v02.json').write_text(json.dumps(manifest['cues'],indent=2)+'\n')
# Explicit scene decisions; direction refers to visible image motion.
modes='''push-in pan-down pan-left pull-out push-in pan-up pan-right pan-left pan-right pull-out push-in pull-out pan-right pan-left push-in pull-out pan-left push-in pan-right pull-out pan-left push-in pan-left pan-down push-in pan-right push-in push-in pan-left pan-up pull-out push-in pan-left pan-right pull-out pan-left push-in push-in pan-down push-in pull-out pull-out pan-left pan-down pan-right push-in pull-out push-in push-in pull-out pull-out pan-left pan-down pan-right push-in push-in pull-out push-in pull-out push-in pan-left push-in pan-down pull-out pan-up pan-right push-in pull-out pull-out push-in pan-up pan-left push-in pan-right pan-down pan-left pan-right pan-down pan-left pull-out pan-right push-in pull-out push-in pan-up pan-down pan-right pan-up push-in pull-out pan-left pan-right push-in pan-left pan-right push-in push-in pan-left pull-out pull-out pan-right pan-down push-in push-in pan-down pull-out pull-out pan-down push-in pan-right pan-left pan-up pan-right pan-left pull-out pan-right pull-out pan-left push-in pull-out pan-left pan-right pull-out pan-left push-in pan-right pull-out pull-out'''.split()
rows=json.loads((EP/'Edit/ImageMotion/sources.json').read_text());assert len(rows)==len(modes)==128
for row,mode in zip(rows,modes):row['camera']=mode
(EP/'Edit/ImageMotion/sources.json').write_text(json.dumps(rows,indent=2)+'\n')
clips=next(t for t in b['tracks'] if t['name']=='Main')['clips'];out=W/'Preflight_2D';out.mkdir(exist_ok=True)
def scene_frame(clip,image,mode,frac):
 keys,_=m.camera_keys(clip,.75,mode,0)
 pp=keys['position'];ss=keys['scale'];x=pp[0][1]*(1-frac)+pp[1][1]*frac;y=pp[0][2]*(1-frac)+pp[1][2]*frac;sw=ss[0][1]*(1-frac)+ss[1][1]*frac;sh=ss[0][2]*(1-frac)+ss[1][2]*frac
 src=Image.open(image).convert('RGB');return src.transform((960,540),Image.Transform.AFFINE,(src.width/(sw*960),0,-x*src.width/sw,0,src.height/(sh*540),-y*src.height/sh),resample=Image.Resampling.BICUBIC)
for page in range(8):
 sheet=Image.new('RGB',(1920,4*294),'#202020');d=ImageDraw.Draw(sheet)
 for k in range(16):
  i=page*16+k;c=clips[i];r=rows[i];im=scene_frame(c,r['image'],r['camera'],1).resize((480,270))
  x=(k%4)*480;y=(k//4)*294;sheet.paste(im,(x,y+24));d.text((x+6,y+5),f"{r['scene_id']} {r['camera']} final crop (2D only)",fill='white')
 sheet.save(out/f'scenes_{page+1:02}.jpg',quality=90)
# Entry/hold/exit corridor extremes: full-opacity samples deliberately expose collisions.
for page in range(4):
 sheet=Image.new('RGB',(1920,4*384),'#202020');d=ImageDraw.Draw(sheet)
 for k in range(4):
  i=page*4+k
  if i>=len(manifest['cues']):break
  cue=manifest['cues'][i];si=int(cue['scene_id'][1:])-1;c=clips[si];r=rows[si];tr=cue['transform'];png=Image.open(cue['image']).convert('RGBA');png=png.resize((round(tr['width']*640),round(tr['height']*360)),Image.Resampling.LANCZOS)
  for j,dy in enumerate([.02,0,-.02]):
   f=cue['start_frame'] if j==0 else (cue['end_frame_exclusive']-1 if j==2 else (cue['start_frame']+cue['end_frame_exclusive'])//2)
   frac=(f-c['frames'][0])/(c['frames'][1]-c['frames'][0]-1);im=scene_frame(c,r['image'],r['camera'],frac).resize((640,360)).convert('RGBA');im.alpha_composite(png,(round((tr['centerX']-tr['width']/2)*640),round((tr['centerY']-tr['height']/2+dy)*360)))
   x=j*640;y=k*384;sheet.paste(im.convert('RGB'),(x,y+24));d.text((x+5,y+5),f"{cue['id']} {cue['scene_id']} {['entry','hold','exit'][j]} {r['camera']}",fill='white')
 sheet.save(out/f'cues_{page+1:02}.jpg',quality=93)
from collections import Counter
print(Counter(modes))
