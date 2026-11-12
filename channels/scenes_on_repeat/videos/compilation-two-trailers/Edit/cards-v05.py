import hashlib, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ep = Path('/Users/diplomat/ytvideos/channels/scenes_on_repeat/videos/compilation-two-trailers')
other = Path('/Users/diplomat/.codex/worktrees/ad59/ytvideos/channels/scenes_on_repeat/videos')
edge = other/'edge-of-tomorrow-2014/Edit/trailer-v03'
home = other/'home-alone-1990/Edit/trailer-v02'
out = ep/'Work/v05'; out.mkdir(parents=True, exist_ok=True)
font = '/System/Library/Fonts/Avenir Next.ttc'
films = [(edge,'EDGE OF TOMORROW','2014','SCI-FI  /  ACTION'), (home,'HOME ALONE','1990','FAMILY  /  COMEDY')]
for i,(base,title,year,genre) in enumerate(films):
    handoff=json.loads((base/'compilation-handoff.json').read_text())
    poster=Path(handoff['poster']['path']).expanduser()
    if not poster.is_absolute(): poster=base/poster
    assert hashlib.sha256(poster.read_bytes()).hexdigest()==handoff['poster']['sha256']
    image=Image.open(poster).convert('RGB')
    bg=image.resize((1280,720),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(42))
    bg=ImageEnhance.Brightness(bg).enhance(.48)
    sharp=image.copy(); sharp.thumbnail((335,560),Image.Resampling.LANCZOS)
    x=105+(335-sharp.width)//2; y=(720-sharp.height)//2
    bg.paste(sharp,(x,y))
    d=ImageDraw.Draw(bg); big=ImageFont.truetype(font,48,index=0); sub=ImageFont.truetype(font,31,index=0)
    d.text((510,265),title,font=big,fill='#F9EED6',stroke_width=1,stroke_fill='#171923')
    d.text((512,346),year,font=sub,fill='#F9EED6',stroke_width=1,stroke_fill='#171923')
    d.text((512,399),genre,font=sub,fill='#F9EED6',stroke_width=1,stroke_fill='#171923')
    bg.save(out/f'card-{i}.png')
