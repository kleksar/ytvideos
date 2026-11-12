from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFont
import json,bisect,math,hashlib
EP=Path(__file__).resolve().parents[3];HERE=Path(__file__).resolve().parent
RUN=EP/'Work/production-20261104-v02';OUT=RUN/'preflight_frames';OUT.mkdir(exist_ok=True)
p=json.loads((HERE/'montage_en_v02.json').read_text());c=json.loads((RUN/'captions_prepare_v04/caption_groups.json').read_text());events=c['word_events'];starts=[v['frame'] for v in events]
W,H=p['canvas'];band_top=1288-(17+ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf',84).getmetrics()[0]);records=[];thumbs=[]
for s in p['scenes']:
 im=ImageOps.fit(Image.open(s['image']).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS)
 for mark,k in [('start',0),('mid',.5),('end',1)]:
  cam=s['camera'];a,b=cam['start'],cam['end'];z=a['scale']+(b['scale']-a['scale'])*k;cx=a['center'][0]+(b['center'][0]-a['center'][0])*k;cy=a['center'][1]+(b['center'][1]-a['center'][1])*k
  box=((cx-.5/z)*W,(cy-.5/z)*H,(cx+.5/z)*W,(cy+.5/z)*H)
  assert min(box)>=-1e-5 and box[2]<=W+1e-5 and box[3]<=H+1e-5
  result=im.resize((W,H),Image.Resampling.BICUBIC,box=box).convert('RGBA');frame=round(s['start_frame']+(s['end_frame']-s['start_frame']-1)*k)
  cap=Image.open(events[bisect.bisect_right(starts,frame)-1]['path']);result.alpha_composite(cap,(0,band_top));path=OUT/(s['id']+'_'+mark+'.jpg');result.convert('RGB').save(path,quality=88)
  records.append({'scene':s['id'],'sample':mark,'frame':frame,'path':str(path),'crop_box':box})
  if mark=='mid':
   thumb=result.convert('RGB').resize((640,360));d=ImageDraw.Draw(thumb);d.rectangle((0,0,120,30),fill='black');d.text((7,6),s['id'],fill='white');thumbs.append(thumb)
for i in range(0,len(thumbs),12):
 sheet=Image.new('RGB',(1920,1440),'#090f19')
 for j,t in enumerate(thumbs[i:i+12]):sheet.paste(t,((j%3)*640,(j//3)*360))
 sheet.save(OUT/f'contact_{i//12+1:02d}.jpg',quality=92)
(HERE/'preflight_frame_coverage.json').write_text(json.dumps({'method':'Pillow endpoint/midpoint composition using saved camera bounds and exact shared-renderer caption PNG states; these are pre-render composites, not exported MP4 frames','samples':records,'all_image_edges_contained':True,'baseline':1288,'band_top':band_top},indent=2)+'\n');print(len(records),'pre-render composites')
