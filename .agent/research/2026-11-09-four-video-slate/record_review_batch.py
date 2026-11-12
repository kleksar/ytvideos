"""Record only exact ready MP4s with their technical evidence."""
from build_review_edit import setup, read, ref, ROOT
from pathlib import Path
import json, subprocess as sp

titles=[
 ('cable','Paper Detour','Long','The First Atlantic Cable Worked. Then It Went Silent.'),
 ('neptune','Paper Detour','Short','How Math Led Astronomers to Neptune'),
 ('us','Nuviko History','Long','How America Grew and Nearly Broke Apart'),
 ('harrison','Nuviko History','Short','How a Watch Told Sailors Where They Were'),
]
batch=[]
for key,channel,form,title in titles:
 if key=='harrison':
  out=ROOT/'channels/nuviko_history/research/harrison-review-v02.mp4'
  qa=out.parent/'harrison-qa-v02/REPORT.md'
  r=read(out.with_suffix('.mp4.delivery.json'))
  assert r['media']==ref(out)
 else:
  ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(key)
  qa=w/'qa-v01/REPORT.md'
  r=read(out.with_suffix('.mp4.delivery.json'))
  assert r['media']==ref(out) and r['technical_review']['full_decode']=='PASS'
  assert r['technical_review']['media_sha256']==r['media']['sha256']
  assert r['technical_review']['evidence']==ref(qa)
 v=float(sp.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=duration','-of','csv=p=0',out]))
 batch.append(dict(channel=channel,format=form,title=title,video=ref(out),seconds=v,bytes=out.stat().st_size,
   quality_report=ref(qa),user_acceptance='PENDING',youtube='NOT_CHANGED'))
assert next(x for x in batch if x['title'].startswith('How America'))['seconds']<600
path=Path(__file__).parent/'review-mp4-batch-v01.json'
with path.open('x') as f: json.dump(batch,f,indent=2,ensure_ascii=False);f.write('\n')
print(json.dumps([(x['title'],x['seconds'],x['video']['sha256']) for x in batch],ensure_ascii=False,indent=2))
