"""Offline visual evidence for existing canonical renders; never changes source assets."""
from pathlib import Path
import json,subprocess,io,math
from PIL import Image,ImageDraw
EP=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900'); W=EP/'Edit/Motion_v01'; R=EP/'Edit/ImageMotion/3cd1ad0ab0dcb2e88e3d'
scenes=json.loads((R/'rendered_preflight.json').read_text());cues=json.loads((W/'cue_motion_applied_v02.json').read_text());out=W/'Depth_Preflight';out.mkdir(exist_ok=True)
reverse=R/'rendered_reverse.json'
if reverse.exists():
 for i,s in enumerate(json.loads(reverse.read_text())):
  if s.get('video') and Path(s['video']).exists():scenes[i]['video']=s['video']
correction=W/'s041_camera_correction.json'
if correction.exists():scenes[40]['keyframes']=json.loads(correction.read_text())['expected_gentle_keys']
correction=W/'s110_camera_correction.json'
if correction.exists():scenes[109]['keyframes']=json.loads(correction.read_text())['expected_gentle_keys']
def image_at(s,n):
 key=f"S{s['source']['frames'][0]:05}_{n:04}";file=out/(key+'.jpg')
 if file.exists():return Image.open(file).convert('RGBA')
 v=subprocess.run(['ffmpeg','-v','error','-i',s['video'],'-vf',f'select=eq(n\\,{n})','-frames:v','1','-f','image2pipe','-vcodec','png','-'],capture_output=True,check=True);src=Image.open(io.BytesIO(v.stdout));f=n/(s['frames']-1);p=s['keyframes']['position'];z=s['keyframes']['scale'];x=p[0][1]*(1-f)+p[1][1]*f;y=p[0][2]*(1-f)+p[1][2]*f;sw=z[0][1]*(1-f)+z[1][1]*f;sh=z[0][2]*(1-f)+z[1][2]*f
 im=src.transform((960,540),Image.Transform.AFFINE,(src.width/(sw*960),0,-x*src.width/sw,0,src.height/(sh*540),-y*src.height/sh),resample=Image.Resampling.BICUBIC).convert('RGBA');im.convert('RGB').save(file,quality=96);return im
def interp(keys,t):
 for a,b in zip(keys,keys[1:]):
  if a[0]<=t<=b[0]:
   v=(t-a[0])/(b[0]-a[0]);typ=a[-1] if isinstance(a[-1],str) else 'smooth'
   if typ=='hold':v=0
   elif typ=='smooth':v=v*v*(3-2*v)
   return [a[j]*(1-v)+b[j]*v for j in range(1,len(a)-(1 if isinstance(a[-1],str) else 0))]
 return [x for x in keys[-1][1:] if isinstance(x,(int,float))]
ready=[(i,s) for i,s in enumerate(scenes) if s.get('video') and Path(s['video']).exists()]
def prime_scene(i,s):
 times={round((s['frames']-1)*f) for f in [0,.25,.5,.75,1]}
 for cue in cues:
  if int(cue['scene_id'][1:])-1!=i:continue
  N=cue['end_frame_exclusive']-cue['start_frame'];a=cue['start_frame']-s['source']['frames'][0]
  times.update(a+t for t in [0,2,4,N//4,N//2,3*N//4,N-5,N-3,N-1])
 times=sorted(n for n in times if not (out/f"S{s['source']['frames'][0]:05}_{n:04}.jpg").exists())
 if not times:return
 expr='+'.join(f'eq(n\\,{n})' for n in times)
 result=subprocess.run(['ffmpeg','-v','error','-i',s['video'],'-vf',f'select={expr},scale=960:540','-vsync','0','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True,check=True)
 size=960*540*3;assert len(result.stdout)==size*len(times)
 for k,n in enumerate(times):
  src=Image.frombytes('RGB',(960,540),result.stdout[k*size:(k+1)*size]);f=n/(s['frames']-1);p=s['keyframes']['position'];z=s['keyframes']['scale'];x=p[0][1]*(1-f)+p[1][1]*f;y=p[0][2]*(1-f)+p[1][2]*f;sw=z[0][1]*(1-f)+z[1][1]*f;sh=z[0][2]*(1-f)+z[1][2]*f
  im=src.transform((960,540),Image.Transform.AFFINE,(1/sw,0,-x*960/sw,0,1/sh,-y*540/sh),resample=Image.Resampling.BICUBIC);im.save(out/f"S{s['source']['frames'][0]:05}_{n:04}.jpg",quality=96)
for i,s in ready:prime_scene(i,s)
# Canonical renderer cosine pass and linear camera have no interior scalar extrema;
# quarter points sample depth-warp geometry in addition to endpoint framing.
for page in range(math.ceil(len(scenes)/4)):
 group=[(i,s) for i,s in ready if page*4<=i<page*4+4]
 if len(group)<min(4,len(scenes)-page*4):continue
 file=out/f'scenes_{page+1:02}.jpg'
 if file.exists():continue
 sheet=Image.new('RGB',(2400,4*294),'#202020');d=ImageDraw.Draw(sheet)
 for row,(i,s) in enumerate(group):
  for col,f in enumerate([0,.25,.5,.75,1]):
   n=round((s['frames']-1)*f);im=image_at(s,n).resize((480,270));x=col*480;y=row*294;sheet.paste(im.convert('RGB'),(x,y+24));d.text((x+4,y+5),f'S{i+1:03} depth+camera {n}/{s["frames"]-1}',fill='white')
 sheet.save(file,quality=94)
for cue in cues:
 i=int(cue['scene_id'][1:])-1;s=scenes[i]
 if not s.get('video'):continue
 file=out/f"{cue['id']}_path_v02.jpg"
 if file.exists():continue
 a,b=cue['start_frame'],cue['end_frame_exclusive'];N=b-a;times=sorted(set([0,2,4,N//4,N//2,3*N//4,N-5,N-3,N-1]));sheet=Image.new('RGB',(1920,math.ceil(len(times)/3)*384),'#202020');d=ImageDraw.Draw(sheet);png0=Image.open(cue['image']).convert('RGBA');tr=cue['transform'];png0=png0.resize((round(tr['width']*960),round(tr['height']*540)),Image.Resampling.LANCZOS)
 for j,t in enumerate(times):
  im=image_at(s,a+t-s['source']['frames'][0]);pos=interp(cue['keyframes']['position'],t);alpha=interp(cue['keyframes']['opacity'],t)[0];png=png0.copy();png.putalpha(png.getchannel('A').point(lambda v:round(v*alpha)));im.alpha_composite(png,(round(pos[0]*960),round(pos[1]*540)));im=im.resize((640,360));x=(j%3)*640;y=(j//3)*384;sheet.paste(im.convert('RGB'),(x,y+24));d.text((x+4,y+5),f'{cue["id"]} {cue["scene_id"]} frame {a+t} opacity {alpha:.2f}',fill='white')
 sheet.save(file,quality=95)
print(json.dumps({'ready_scenes':len(ready),'scene_sheets':len(list(out.glob('scenes_*.jpg'))),'cue_sheets':len(list(out.glob('C*_path_v02.jpg')))}))
