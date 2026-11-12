import pathlib,json,bisect,math,hashlib
from PIL import Image,ImageOps,ImageDraw,ImageFont
w=pathlib.Path('Work');o=w/'sequence_b_review_v01';o.mkdir(exist_ok=True);plan=json.load(open(w/'mix_word_safe_prefer_b_draft_v02.json'));cg=json.load(open(w/'word_safe_b_subtitles_v02/caption_groups.json'));events=cg['word_events'];frames=[x['frame'] for x in events];ent=[];thumbs=[]
for i,s in enumerate(plan['scenes']):
 mid=(s['start_frame']+s['end_frame'])//2;idx=bisect.bisect_right(frames,mid)-1
 if idx<0:raise ValueError(i)
 caption=events[idx]['path'];im=ImageOps.fit(Image.open(s['image']).convert('RGBA'),(2560,1440),Image.Resampling.LANCZOS);im.alpha_composite(Image.open(caption).convert('RGBA'),(0,1193));im=im.convert('RGB').resize((384,216),Image.Resampling.LANCZOS);thumbs.append(im)
 ent.append({'scene':f'S{i+1:03}','image':s['image'],'image_sha256':hashlib.sha256(pathlib.Path(s['image']).read_bytes()).hexdigest(),'midpoint_frame':mid,'caption_state':caption})
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',14)
for start in range(0,len(thumbs),20):
 page=Image.new('RGB',(384*4,238*5),'#1a1a1a');d=ImageDraw.Draw(page)
 for j,im in enumerate(thumbs[start:start+20]):
  e=ent[start+j];x=j%4*384;y=j//4*238;d.text((x+3,y+2),e['scene']+' '+pathlib.Path(e['image']).name,font=font,fill='white');page.paste(im,(x,y+20))
 page.save(o/f'contact_{start//20+1:02}.jpg',quality=88)
(o/'manifest.json').write_text(json.dumps({'status':'DRAFT_NO_ACCEPTANCE','scope':'One estimated caption state at midpoint of each selected scene; no motion or audible sync.','plan':str((w/'mix_word_safe_prefer_b_draft_v02.json').resolve()),'entries':ent},indent=2)+'\n');print('created',len(ent),'composites')
