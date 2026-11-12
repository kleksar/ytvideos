import json,subprocess,concurrent.futures,pathlib
from PIL import Image,ImageDraw
p=pathlib.Path(__file__).resolve().parent
out=p/'qa_review_v02';out.mkdir(exist_ok=True)
a=json.loads((p/'qa_draft_v01/frame_map.json').read_text())
(out/'frame_map.json').write_text(json.dumps(a,indent=2)+'\n')
def part(k):
 group=a[k*27:(k+1)*27]
 expr='+'.join('eq(n\\,%d)'%r['frame'] for r in group)
 cmd=['ffmpeg','-v','error','-i',str(p/'Deliverables/review_v02.mp4'),'-vf','select='+expr+',scale=640:360','-vsync','0','-q:v','3',str(out/('part%d_%%03d.jpg'%k))]
 subprocess.run(cmd,check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as x: list(x.map(part,range(7)))
for i in range(9):
 canvas=Image.new('RGB',(1920,7*390),'#222'); draw=ImageDraw.Draw(canvas)
 for row in range(7):
  scene=i*7+row
  for col in range(3):
   idx=scene*3+col
   if idx>=len(a):continue
   img=Image.open(out/('part%d_%03d.jpg'%(idx//27,idx%27+1)))
   canvas.paste(img,(col*640,row*390+25))
   draw.text((col*640+8,row*390+5),f"Scene {a[idx]['scene']} {a[idx]['position']} frame {a[idx]['frame']}",fill='white')
 canvas.save(out/('contact_%02d.jpg'%(i+1)),quality=88)
print('Extracted',len(a),'frames and 9 contact sheets')
