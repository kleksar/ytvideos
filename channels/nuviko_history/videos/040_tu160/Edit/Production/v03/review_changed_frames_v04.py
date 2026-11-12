from pathlib import Path
import json,subprocess
from PIL import Image,ImageDraw
r=Path(__file__).resolve().parents[3];p=json.load(open(r/'Edit/Production/v03/plan.json'));v=r/'Deliverables/NUVIKO_040_TU160_EN_REVIEW_v04.mp4';d=r/'Edit/Production/v03/qa_changed_frames_v04';d.mkdir(exist_ok=True)
ids=[4,11,39,43,62,64,74,102,108,119];out=Image.new('RGB',(1920,360*len(ids)))
for row,n in enumerate(ids):
 s=p['scenes'][n-1];a,b=s['start_frame'],s['end_frame']; fs=[a+2,(a+b)//2,b-3]
 for col,f in enumerate(fs):
  path=d/f'{n:03}_{f:05}.jpg';subprocess.run(['ffmpeg','-v','error','-ss',f'{f/30:.6f}','-i',str(v),'-frames:v','1','-vf','scale=640:-2','-q:v','2','-y',str(path)],check=True)
  im=Image.open(path).convert('RGB');draw=ImageDraw.Draw(im);draw.rectangle((0,0,230,25),fill='black');draw.text((4,5),f'shot {n:03} frame {f}',fill='white');out.paste(im,(col*640,row*360))
out.save(d/'changed_frames_contact.jpg',quality=87)
print('extracted 30 frames',d)
