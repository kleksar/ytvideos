from pathlib import Path
import math,json
from PIL import Image,ImageDraw
ep=Path(__file__).resolve().parents[2]
qa=ep/'Edit/QA'
run=qa/'brocklesby-en-v01'
report=json.loads((run/'report.json').read_text())
framemap={x['index']:run/x['path'] for x in report['frame_map']}
plan=json.loads((qa/'qa-plan-v01.json').read_text())
pairs=json.loads((qa/'scene-cue-pairs-v01.json').read_text())
out=qa/'review-sheets-v01'; out.mkdir(exist_ok=True)
scenes=plan['scenes']
def sheet(path,items,width,height,cols):
 result=Image.new('RGB',(width*cols,(height+22)*math.ceil(len(items)/cols)),'#30261f');draw=ImageDraw.Draw(result)
 for k,(frame,label) in enumerate(items):
  with Image.open(framemap[frame]) as im:
   im.thumbnail((width,height),Image.Resampling.LANCZOS)
   xx=k%cols*width;yy=k//cols*(height+22)
   result.paste(im,(xx,yy))
  draw.text((xx+6,yy+height+3),f'{frame} {label}',fill='white')
 result.save(out/path,quality=92)
for part in range(2):
 items=[]
 for label,f in [('start',lambda s:s['start']),('mid',lambda s:s['start']+(s['end']-s['start']-1)//2),('end',lambda s:s['end']-1)]:
  items += [(f(s),s['id']+' '+label) for s in scenes[4*part:4*part+4]]
 sheet(f'scenes-{part+1}.jpg',items,216,384,4)
for part in range(math.ceil(len(pairs)/12)):
 sheet(f'cues-{part+1}.jpg',[(p['frame'],p['scene']+' '+p['cue']) for p in pairs[part*12:(part+1)*12]],180,320,4)
sheet('frame-loop.jpg',[(f,'Paper Frame') for f in [478,479,480,481,958,959,960,961]],216,384,4)
indices=report['requested_frame_indices']
for n in range(math.ceil(len(indices)/48)):
 batch=indices[n*48:(n+1)*48]
 canvas=Image.new('RGB',(864,64*math.ceil(len(batch)/4)),'#30261f')
 label=ImageDraw.Draw(canvas)
 for i,frame in enumerate(batch):
  with Image.open(framemap[frame]) as im:
   band=im.crop((0,1810,1440,2090)).resize((216,42),Image.Resampling.LANCZOS)
   x,y=(i%4)*216,(i//4)*64
   canvas.paste(band,(x,y));label.text((x+6,y+44),str(frame),fill='white')
 canvas.save(out/f'transitions-{n+1}.jpg',quality=92)
