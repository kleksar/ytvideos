#!/usr/bin/env python3
"""Rebuild reference collages from unmodified ffmpeg-extracted PNGs. Pillow required."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parent
ORIG=ROOT/'originals'; OUT=ROOT/'collages';OUT.mkdir(exist_ok=True)
try: font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',21)
except OSError: font=ImageFont.load_default()
# Boxes in original 1920x1080 coordinates. Never AI generated.
groups={
'01_character_poses_emotions':[
('Mind_12s.png',(0,0,1020,1080),'MIND | hero: confident, thin stick body, NO clothing'),
('Mind_23s.png',(0,0,650,1080),'MIND | hero: surprised, scarf + circular black hands'),
('Mind_43s.png',(0,180,770,1080),'MIND | hero: seated, calm; no hoodie'),
('Everyone_16s.png',(200,60,850,1080),'EVERYONE | hero: alone; muted blue-gray hoodie'),
('Everyone_46s.png',(200,60,850,1080),'EVERYONE | hero: seated reaction; ochre patches'),
('Everyone_82s.png',(680,50,1920,1080),'EVERYONE | hero: close expression, hoodie + scarf')],
'02_objects_visual_language':[
('Mind_23s.png',(550,350,850,650),'MIND | simple coffee machine; flat blue-gray'),
('Mind_105s.png',(650,650,1100,1080),'MIND | poker chips/cards; flat ochre + blue-gray'),
('Mind_43s.png',(600,650,1400,1080),'MIND | desk and document; sparse geometry'),
('Everyone_16s.png',(1050,400,1700,800),'EVERYONE | birthday cake/tray; minimal warm props'),
('Everyone_190s.png',(0,0,650,1080),'EVERYONE | door and wall; warm ochre lines'),
('Everyone_28s.png',(450,700,1350,1080),'EVERYONE | cups, vase, table; matte flat shapes')],
'03_scene_compositions':[
('Mind_12s.png',None,'MIND | window: large negative space'),
('Mind_23s.png',None,'MIND | cafe: foreground hero + simple queue'),
('Mind_43s.png',None,'MIND | office: readable thought balloon + sparse set'),
('Mind_105s.png',None,'MIND | poker: two figures, clean visual hierarchy'),
('Mind_178s.png',None,'MIND | dialogue: black uppercase in speech balloon'),
('Mind_62s.png',None,'MIND | reaction: cyan subjective-thought mark'),
('Everyone_16s.png',None,'EVERYONE | bar: sparse cream interior, warm ochre'),
('Everyone_28s.png',None,'EVERYONE | two-person dialogue, simple furniture'),
('Everyone_46s.png',None,'EVERYONE | arrival: separated silhouettes'),
('Everyone_82s.png',None,'EVERYONE | close-up; limited palette and linework'),
('Everyone_130s.png',None,'EVERYONE | night exterior: muted navy, ochre lights'),
('Everyone_190s.png',None,'EVERYONE | bathroom: restrained perspective')]
}
records=[]
for group,items in groups.items():
 cols=3;cw=640;ch=430;rows=(len(items)+cols-1)//cols
 sheet=Image.new('RGB',(cols*cw,rows*ch),(247,239,222));draw=ImageDraw.Draw(sheet)
 for i,(name,box,caption) in enumerate(items):
  im=Image.open(ORIG/name).convert('RGB')
  if box:im=im.crop(box)
  im.thumbnail((620,350),Image.Resampling.LANCZOS)
  x=(i%cols)*cw;y=(i//cols)*ch
  sheet.paste(im,(x+(cw-im.width)//2,y+(350-im.height)//2))
  stamp=name.replace('_',' @ ').replace('s.png',' sec')
  draw.text((x+40,y+355),stamp,fill='#222222',font=font)
  # wrap labels manually to fit width
  words=caption.split();lines=['']
  for w in words:
   if draw.textlength((lines[-1]+' '+w).strip(),font=font)>560:lines.append(w)
   else:lines[-1]= (lines[-1]+' '+w).strip()
  for j,line in enumerate(lines):draw.text((x+40,y+382+j*23),line,fill='#222222',font=font)
  records.append(dict(sheet=group,source=name,crop_box=box,caption=caption))
 sheet.save(OUT/(group+'.jpg'),quality=94,subsampling=0)
(ROOT/'crop_manifest.json').write_text(json.dumps(records,indent=2))
