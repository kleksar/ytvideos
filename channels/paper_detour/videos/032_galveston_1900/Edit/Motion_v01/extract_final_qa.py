"""Extract inspectable evidence from the exact exported MP4, without a player."""
from pathlib import Path
import json,subprocess,argparse,math
from PIL import Image,ImageDraw
EP=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');W=EP/'Edit/Motion_v01';p=argparse.ArgumentParser();p.add_argument('video');args=p.parse_args();video=Path(args.video).resolve();q=W/'Final_QA';q.mkdir(exist_ok=True);fdir=q/'Frames';fdir.mkdir(exist_ok=True)
b=json.loads((EP/'Edit/Review_v01/static_review_manifest_v01.json').read_text());cues=json.loads((W/'cue_motion_applied_v02.json').read_text());frames={0,b['total_frames']-1};scene_frames=[];cue_frames=[]
for scene in b['scenes']:
 a,z=scene['start_frame'],scene['end_frame_exclusive'];ns=[round(a+(z-a-1)*f) for f in [0,.25,.5,.75,1]];frames.update(ns);scene_frames.append({'id':scene['id'],'frames':ns})
for cue in cues:
 a,z=cue['start_frame'],cue['end_frame_exclusive'];N=z-a;ns=sorted(set([a-1,a,a+2,a+4,a+N//4,a+N//2,a+3*N//4,z-5,z-3,z-1,z]));frames.update(ns);cue_frames.append({'id':cue['id'],'scene_id':cue['scene_id'],'frames':ns})
frames=sorted(n for n in frames if 0<=n<b['total_frames']);mapping={n:fdir/f'frame_{n:05}.jpg' for n in frames};missing=[n for n in frames if not mapping[n].exists()]
if missing:
 expr='+'.join(f'eq(n\\,{n})' for n in missing)
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(video),'-vf',f'select={expr}','-vsync','0','-q:v','2',str(fdir/'sequence_%05d.jpg')],check=True)
 generated=sorted(fdir.glob('sequence_*.jpg'));assert len(generated)==len(missing),(len(generated),len(missing))
 for old,n in zip(generated,missing):old.rename(mapping[n])
for page in range(math.ceil(len(scene_frames)/4)):
 sheet=Image.new('RGB',(2400,4*294),'#202020');d=ImageDraw.Draw(sheet)
 for row,scene in enumerate(scene_frames[page*4:page*4+4]):
  for col,n in enumerate(scene['frames']):
   im=Image.open(mapping[n]).resize((480,270));x=col*480;y=row*294;sheet.paste(im,(x,y+24));d.text((x+4,y+5),f'{scene["id"]} FINAL MP4 n={n}',fill='white')
 sheet.save(q/f'scenes_{page+1:02}.jpg',quality=95)
for cue in cue_frames:
 sheet=Image.new('RGB',(1920,math.ceil(len(cue['frames'])/3)*384),'#202020');d=ImageDraw.Draw(sheet)
 for j,n in enumerate(cue['frames']):
  im=Image.open(mapping[n]).resize((640,360));x=(j%3)*640;y=(j//3)*384;sheet.paste(im,(x,y+24));d.text((x+4,y+5),f'{cue["id"]} {cue["scene_id"]} FINAL MP4 n={n}',fill='white')
 sheet.save(q/f'{cue["id"]}_path.jpg',quality=96)
# Phone-size comparison, all held cues.
phone=Image.new('RGB',(4*384,math.ceil(len(cues)/4)*240),'#202020');d=ImageDraw.Draw(phone)
for j,cue in enumerate(cues):
 n=(cue['start_frame']+cue['end_frame_exclusive'])//2;nearest=min(frames,key=lambda x:abs(x-n));im=Image.open(mapping[nearest]).resize((384,216));x=(j%4)*384;y=(j//4)*240;phone.paste(im,(x,y+24));d.text((x+4,y+5),f'{cue["id"]} n={nearest}',fill='white')
phone.save(q/'phone_cues.jpg',quality=96)
(q/'frame_manifest.json').write_text(json.dumps({'video':str(video),'frames':frames,'count':len(frames),'scenes':scene_frames,'cues':cue_frames,'coverage':'5 points per scene, every direct cut, cue entry/hold/exit and adjacent frames; sampled visual QA, not continuous playback'},indent=2)+'\n')
print(json.dumps({'frames':len(frames),'scenes':len(scene_frames),'cues':len(cue_frames)}))
