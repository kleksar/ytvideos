from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import shutil,json
ROOT=Path('/Users/diplomat/ytvideos');p=ROOT/'channels/paper_detour/videos/030_clothing_history';d=p/'Source/Graphics/v05'
files=['exec-6d312a8b-da18-46bb-91a7-0c78d3c09ff9.png','exec-56cb9cb5-c479-4b83-a025-db148c8d570a.png','exec-42212c83-ccc7-4181-abea-227133809037.png','exec-f9e804f4-ff0b-4038-af3d-0e883580964f.png','exec-9494860c-9580-439b-a363-2ab07e475607.png','exec-7e4c8824-b906-442b-bed9-0182c5757db6.png']
sheet=Image.new('RGB',(1200,1200),(30,43,60));dr=ImageDraw.Draw(sheet)
for i,name in enumerate(files):
 src=Path('/Users/diplomat/.codex/generated_images/01a1981d-a870-7112-8979-ccd0e34cc760')/name;dest=d/f'C{i+1:02}_raw.png'
 if not dest.exists():shutil.copy2(src,dest)
 im=Image.open(dest).convert('RGBA');print(dest.name,im.size,'alpha',im.getchannel('A').getextrema())
 thumb=ImageOps.contain(im,(1140,165));x=(1200-thumb.width)//2;y=i*200+15;sheet.paste(thumb,(x,y),thumb);dr.text((15,i*200+180),f'C{i+1:02}',fill='white')
sheet.save(d/'TYPOGRAPHY_REVIEW.png')
# Technical still framing for timeline/preflight. No source image content is changed.
shots=json.loads((p/'Storyboard/SHOTLIST_v05.json').read_text());thumbs=[]
for sh in shots:
 im=Image.open(sh['path']).convert('RGB');z=sh['zoom'];w,h=im.size
 if z!=1:
  cw,ch=w/z,h/z;cx,cy=w/2,h/2;im=im.crop((round(cx-cw/2),round(cy-ch/2),round(cx+cw/2),round(cy+ch/2)))
 im=ImageOps.fit(im,(1920,1080),method=Image.Resampling.LANCZOS);dest=p/'Edit/v05'/f'{sh["id"]}_framing.png';im.save(dest)
 sh['framed_path']=str(dest);thumbs.append(im)
(p/'Storyboard/SHOTLIST_v05.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
sheet=Image.new('RGB',(1600,7*260),(225,220,210));draw=ImageDraw.Draw(sheet)
for i,(im,sh) in enumerate(zip(thumbs,shots)):
 x=(i%5)*320;y=(i//5)*260;sheet.paste(im.resize((310,175)),(x+5,y));draw.text((x+5,y+180),f'{sh["id"]} {sh["source_scene"]} {sh["duration"]:.2f}s',fill='black');draw.text((x+5,y+202),sh['spoken'][:42],fill='black')
sheet.save(p/'Storyboard/CONTACT_SHEET_v05.png')
