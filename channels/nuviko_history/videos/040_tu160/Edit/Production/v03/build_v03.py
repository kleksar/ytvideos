from pathlib import Path
import json,hashlib,datetime,copy
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parents[3]
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
old=json.loads((root/'Edit/Production/v02/plan.json').read_text())
ids=['004','011','039','043','062','064','074','102','108','119']
labels=['TU-160 / WHITE SWAN','LONG RANGE / HIGH SPEED','A NEW DESIGN','WINGS EXTENDED','FORWARD / SWEPT','NK-32','SPEED COSTS FUEL','NOT ALONE','AIR • LAND • SEA','SERIAL PRODUCTION']
for n,l in zip(ids,labels):
 s=old['scenes'][int(n)-1]; s['image']=str(root/f'Source/Images/TextRevision/shot_{n}_text_v{"02" if n in {"062","102","108","119"} else "01"}.png');s['camera']['subject']+='; integrated scene text '+l;s['camera']['reason']='Preserve readable generated text and scene subject through the inherited restrained whole-image movement.'
old['subtitles'].pop('review',None)
p=root/'Edit/Production/v03/plan.json';p.write_text(json.dumps(old,indent=2,ensure_ascii=False)+'\n')
imgs=[]
for n in ids:
 i=int(n)-1
 for j in [i-1,i,i+1]:
  s=old['scenes'][j];im=Image.open(s['image']).convert('RGB');im=ImageOps.fit(im,(400,225));d=ImageDraw.Draw(im);d.rectangle((0,0,190,24),fill='black');d.text((4,4),f'shot {j+1:03} '+('TEXT v01' if j==i else 'neighbor'),fill='white');imgs.append(im)
out=Image.new('RGB',(1200,225*len(ids)))
for i,im in enumerate(imgs):out.paste(im,((i%3)*400,(i//3)*225))
out.save(root/'Edit/Production/v03/contact_text_neighbors_v01.jpg',quality=88)
print('plan',p,'contact saved, shots',len(ids))
for n,l in zip(ids,labels):
 q=root/f'Source/Images/TextRevision/shot_{n}_text_v{"02" if n in {"062","102","108","119"} else "01"}.png'; im=Image.open(q);print(n,im.size,h(q),l)
