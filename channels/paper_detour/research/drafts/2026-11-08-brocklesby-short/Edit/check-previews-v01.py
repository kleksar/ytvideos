# Preview contact sheets for frame-accurate caption bounds on actual scene sources.
from pathlib import Path
import json,bisect
from PIL import Image,ImageDraw
ep=Path(__file__).resolve().parents[1]
work=ep/'Work/sub-prep-v02'
m=json.loads((ep/'Edit/montage-v01.json').read_text())
r=json.loads((work/'caption_groups.json').read_text())
ev=r['word_events']; times=[x['frame'] for x in ev]
g=r['display_intervals']
assert g[0]['start_frame']==0 and g[-1]['end_frame']==1080 and all(a['end_frame']==b['start_frame'] for a,b in zip(g,g[1:]))
sheet=Image.new('RGB',(216*4,408*3),'#30261f')
draw=ImageDraw.Draw(sheet)
for i,s in enumerate(m['scenes']):
 if i%4==0: draw.rectangle((0,0,sheet.width,sheet.height),fill="#30261f")
 w,h=m['canvas']; pic=Image.open(s['image']).convert('RGB')
 if pic.width/pic.height>w/h:
  d=(pic.width-pic.height*w/h)/2; pic=pic.crop((d,0,pic.width-d,pic.height))
 else:
  d=(pic.height-pic.width*h/w)/2; pic=pic.crop((0,d,pic.width,pic.height-d))
 camera=s['camera']
 for j,k in enumerate((s['start_frame'],(s['start_frame']+s['end_frame'])//2,s['end_frame']-1)):
  f=(k-s['start_frame'])/(s['end_frame']-s['start_frame']-1)
  a,b=camera['start'],camera['end']; z=a['scale']*(1-f)+b['scale']*f
  x,y=[u*(1-f)+v*f for u,v in zip(a['center'],b['center'])]
  sw,sh=pic.size; q=.5/z
  tile=pic.transform((216,384),Image.Transform.EXTENT,((x-q)*sw,(y-q)*sh,(x+q)*sw,(y+q)*sh),Image.Resampling.BICUBIC)
  caption=Image.open(ev[bisect.bisect_right(times,k)-1]['path'])
  reduced=caption.resize((216,round(caption.height*216/w)),Image.Resampling.LANCZOS)
  tile.paste(reduced,(0,round(384*.762-reduced.height/2)),reduced)
  xx=(i%4)*216;yy=j*408
  sheet.paste(tile,(xx,yy)); draw.text((xx+8,yy+387),f'S{i+1:03d} | frame {k}',fill='white')
  if i%4==3 and j==2: sheet.save(work/f'composites-{i//4+1}.jpg',quality=93)
