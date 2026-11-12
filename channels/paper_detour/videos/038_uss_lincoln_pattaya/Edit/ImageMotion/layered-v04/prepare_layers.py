from pathlib import Path
from PIL import Image,ImageFilter,ImageChops,ImageDraw
base=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/038_uss_lincoln_pattaya')
gen=Path('/Users/diplomat/.codex/generated_images/01a19e92-58c1-7d10-9da8-7626efa8e45c')
out=base/'Work/layered-motion-v04/layers';out.mkdir(parents=True,exist_ok=True)
items=[
('S07','paper_v03/S07_v04.png','da5f26e8-129a-4fa2-b672-0d739ab9dbcf','a5f8f543-04f9-4e5d-8c03-4903b641fa0b'),
('S02','paper_v02/S02_v03.png','b45e24fb-d95b-456a-9aba-c3c4cc8ea79f','4a803110-2de8-4253-b8ad-f7da6f91b267'),
('S06','paper_v03/S06_v03.png','8bd291ce-924e-411d-84aa-9257bd04e679','b087a555-125b-41e0-a31b-686e6c73b2f2'),
('S04','paper_v02/S04_v02.png','0c5255ca-699b-4e97-a962-3321f430d459','c2e655df-a226-458a-8c85-a5500487d00f'),
('S12a','paper_v02/S12_v02.png','37ffc07c-a5da-4d57-871c-f01d8f5e88cf','a8ba1d51-5e95-49cc-bd36-afd46e3a943e'),
('S12b','paper_v03/S12_v03.png','7933977e-74f0-4e9d-becd-1d56fab1f009','8bb43110-547e-48b2-9ad7-48b4df0635de'),
('S09','paper_v02/S09_v02.png','f648e99f-16d2-4bd6-ab72-40275f5c644e','7a399abd-038d-4ca8-9439-354921bd0991'),
('S10','paper_v03/S10_v04.png','b05920c0-aa1d-422b-adfa-255a2d35ca0e','1ce48d5c-c5b3-42fe-9e73-6f888eb8f22e'),
('S13','paper_v02/S13_v02.png','13b6b814-c9fb-4e11-83c4-a57c4060a8a3','45b08406-4ef4-4bd3-ab1f-cc37103b7a82'),
('S14','paper_v02/S14_v03.png','968c630d-7b66-40c8-89ab-0554215d78e8','df40d0cf-3dcc-486f-adf2-cc5ec19f9aa3')]
for name,p,f,b in items:
 d=out/name;d.mkdir(exist_ok=True)
 im=Image.open(base/'Source/Images'/p).convert('RGBA');fggen=Image.open(gen/f'exec-{f}.png').convert('RGBA').resize(im.size);bggen=Image.open(gen/f'exec-{b}.png').convert('RGBA').resize(im.size)
 a=fggen.getchannel('A');fg=im.copy();fg.putalpha(a);fg.save(d/'foreground.png')
 hole=a.filter(ImageFilter.MaxFilter(21)).filter(ImageFilter.GaussianBlur(2));bg=Image.composite(bggen,im,hole);bg.save(d/'background.png')
 for dx in [-7,0,7]:
  shifted=Image.new('RGBA',im.size);shifted.paste(fg,(dx,0));Image.alpha_composite(bg,shifted).convert('RGB').save(d/f'check_{dx}.jpg',quality=90)
print('created',len(items))
