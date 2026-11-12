import json,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[1]
slug=sys.argv[1]
work=root/'Work'/slug
mp4=root/'Deliverables'/slug/(slug+'.mp4')
plan=json.loads((work/'timeline.json').read_text())
shots=plan['shots']
rows=[]
for shot in shots:
 a,b=shot['start_frame'],shot['end_frame']
 rows.append((f"Shot {shot['number']:02}: {shot['beat']}",[a,(a+b-1)//2,b-1]))
for i in range(1,len(shots)):
 j=shots[i]['start_frame']
 rows.append((f"Cut {i:02}",[max(shots[i-1]['start_frame'],j-7),j-1,j,min(shots[i]['end_frame']-1,j+6)]))
for i,group in enumerate(plan['groups'],1):
 frames=[round(w['start']*24) for w in group]
 for j in range(0,len(frames),4):
  rows.append((f"Caption {i}: {' '.join(w['text'] for w in group)}",frames[j:j+4]))
rows.append(('Card and end',[plan['frames']-121,plan['frames']-119,plan['frames']-90,plan['frames']-1]))
w,h=172,306
stride=w*h*3
wanted={f for _,row in rows for f in row}
samples={}
with subprocess.Popen(['ffmpeg','-v','error','-threads','2','-i',str(mp4),'-vf',f'scale={w}:{h}',
                       '-pix_fmt','rgb24','-an','-f','rawvideo','-threads','1','-'],stdout=subprocess.PIPE) as decoder:
 for i in range(plan['frames']):
  raw=decoder.stdout.read(stride)
  assert len(raw)==stride,i
  if i in wanted: samples[i]=Image.frombytes('RGB',(w,h),raw)
 assert not decoder.stdout.read(1)
 assert decoder.wait()==0
for k in range(0,len(rows),6):
 batch=rows[k:k+6]
 img=Image.new('RGB',(w*4,(h+35)*len(batch)),'#202125')
 draw=ImageDraw.Draw(img)
 for y,(label,indices) in enumerate(batch):
  y*=h+35
  draw.text((5,y+3),label,fill='white')
  for x,i in enumerate(indices):
   img.paste(samples[i],(x*w,y+16));draw.text((x*w+5,y+h+19),f'{i} ({i/24:.2f})',fill='white')
 img.save(work/f'qa-{1+k//6:02}.jpg',quality=86)
(work/'qa-frames.json').write_text(json.dumps(rows,indent=2))
