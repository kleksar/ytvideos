from pathlib import Path
import json
import hashlib
from PIL import Image, ImageOps, ImageDraw, ImageFont

root = Path(__file__).resolve().parent
font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 24)
small = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)
scenes = json.loads((root/'storyboard.json').read_text())['scenes']
cell_w, image_h, label_h = 300, 534, 48
sheet = Image.new('RGB', (cell_w * 7, (image_h + label_h)*2), '#edece9')
draw = ImageDraw.Draw(sheet)
manifest=[]
for i, scene in enumerate(scenes):
    path = root/'scenes'/f"{scene['id']}.png"
    if not path.exists():
        raise FileNotFoundError(path)
    with Image.open(path) as im:
        preview = ImageOps.contain(im.convert('RGB'), (cell_w-8,image_h))
        x,y=(i%7)*cell_w,(i//7)*(image_h+label_h)
        sheet.paste(preview,(x+(cell_w-preview.width)//2,y+(image_h-preview.height)//2))
        draw.text((x+12,y+image_h+10),scene['id'],font=font,fill='#222222')
        manifest.append({'scene_id':scene['id'],'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'dimensions':list(im.size),'status':'PREPRODUCTION_DRAFT'})
sheet.save(root/'storyboard-collage.jpg',quality=94)
(root/'images-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
paths=[p for p in sorted((root/'sheets').glob('*.png')) if p.name not in {'museum-v01.png', 'assembly-hands-v01.png', 'filter-states.png'}]
w,h=640,480
refs=Image.new('RGB',(w*3,(h+44)*((len(paths)+2)//3)),'#edece9')
d=ImageDraw.Draw(refs)
for i,p in enumerate(paths):
    with Image.open(p) as im:
        preview=ImageOps.contain(im.convert('RGB'),(w-12,h))
        x,y=(i%3)*w,(i//3)*(h+44)
        refs.paste(preview,(x+(w-preview.width)//2,y+(h-preview.height)//2))
        d.text((x+12,y+h+10),p.stem,font=small,fill='#222222')
refs.save(root/'reference-sheets-collage.jpg',quality=94)
print('Saved both collages and exact scene hashes')
