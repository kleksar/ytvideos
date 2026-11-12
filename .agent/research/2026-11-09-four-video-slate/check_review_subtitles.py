"""Build inspection contact sheets from the actual caption states and timeline."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps
import math, sys, json
from build_review_edit import setup, read, ref, dump

mode,name=sys.argv[1:3]
ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
prep=w/'sub-prep-v01'
p=read(manifest); g=read(prep/'caption_groups.json'); groups=g['groups']; events=g['word_events']
assert [x['text'] for z in groups for x in z]==[x['text'] for x in wm['words']]
assert all(abs(z['frame']-math.ceil(x['start']*30-1e-7))<=0 for z,x in zip([z for z in events if not z['path'].endswith(('neutral.png','transparent.png'))],wm['words']))
if mode=='sheets':
 (prep/'phrases.txt').write_text('\n'.join(' '.join(x['text'] for x in z) for z in groups)+'\n')
 step=3 if fmt=='short' else 1
 tiles=[]
 for i,s in enumerate(p['scenes'],1):
  l,r=s['start_frame'],s['end_frame']
  base=ImageOps.fit(Image.open(s['image']).convert('RGB'),canvas,Image.Resampling.LANCZOS)
  camera=s['camera']
  ts=[l,(l+r)//2,r-1] if fmt=='short' else [(l+r)//2]
  for frame in ts:
   u=(frame-l)/(r-l-1)
   b=camera['start']; e=camera['end']
   z=b['scale']+(e['scale']-b['scale'])*u
   x,y=[j+(k-j)*u for j,k in zip(b['center'],e['center'])]
   width,height=canvas
   bg=base.transform(tuple(canvas),Image.Transform.AFFINE,(1/z,0,width*(x-.5/z),0,1/z,height*(y-.5/z)),Image.Resampling.BICUBIC).convert('RGBA')
   ev=next(x for x in reversed(events) if x['frame']<=frame)
   overlay=Image.open(ev['path'])
   if fmt=='short':top=round(height*g['shared_geometry']['center_y_ratio']-overlay.height/2)
   else:
    from PIL import ImageFont
    pr=g['profile']; font=ImageFont.truetype(pr['font'],g['resolved_font_size_px'],index=pr['font_index'])
    top=g['baseline']-pr['pad_y']-pr['outline_width']-font.getmetrics()[0]
   bg.alpha_composite(overlay,(0,top))
   size=(180,320) if fmt=='short' else (300,169)
   tiles.append((bg.convert('RGB').resize(size,Image.Resampling.LANCZOS),f'S{i:03d}  f{frame}'))
 n=9 if fmt=='short' else 20
 cols=3 if fmt=='short' else 4
 for j in range(0,len(tiles),n):
  part=tiles[j:j+n]; tw,th=part[0][0].size
  cw,chh=tw+10,th+24
  sheet=Image.new('RGB',(cols*cw,math.ceil(len(part)/cols)*chh),(19,24,31)); draw=ImageDraw.Draw(sheet)
  for k,(im,label) in enumerate(part):
   x,y=(k%cols)*cw,(k//cols)*chh
   sheet.paste(im,(x+5,y+4)); draw.text((x+5,y+th+7),label,fill='white')
  sheet.save(prep/f'composites-{j//n+1:02}.jpg',quality=93)
 print(len(groups),'groups;',len(g['boundary_warnings']),'warnings;',len(tiles),'composites')
elif mode=='accept':
 review=read(prep/'subtitle_review.json')
 report=d/'subtitle-preflight-v01.md'
 assert report.is_file()
 for check,coverage,method in [
 ('semantic_grouping',f'{len(groups)} groups; exact text/coverage and adjacent boundaries','Read the group sequence; cross-checked exact word map and renderer event boundaries'),
 ('visual_placement',f'{len(p["scenes"])} actual scenes; '+('start, middle and last frame of each' if fmt=='short' else 'midpoint of each'),'Inspected source and rendered-caption composites at review scale')]:
  review['checks'][check]=dict(status='PASS',reviewer='Codex',method=method,coverage=coverage,evidence=ref(report))
 dump(d/'subtitle-review-v01.json',review)
