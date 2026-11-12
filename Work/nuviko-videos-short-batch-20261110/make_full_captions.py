import json
from pathlib import Path
w=Path(__file__).parent
notion=json.load(open('/private/tmp/nuviko-notion-extract.json'))
raw=[v for s in notion['segments'] for v in s.get('words',[])]
out=[]
for word,a,b in [
 ('Riiiiiseeeeee',0,.9),('Oh',.9,1.42),('back',1.42,1.85),
 ('when',1.85,2.2),('I',2.2,2.55),('was',2.55,3.1),
 ('younger',3.1,4.1),
]:
 out.append({'text':word,'start_seconds':a,'end_seconds':b})
def spaced(words,a,b):
 step=(b-a)/len(words)
 for i,word in enumerate(words):out.append({'text':word,'start_seconds':a+i*step,'end_seconds':a+(i+1)*step})
spaced('was told by other youngsters'.split(),8.94-4.84,11.84-4.84)
spaced('that my end will be torture beneath the earth'.split(),11.84-4.84,17.72-4.84)
for word,a,b in [('cause',17.72,18.18),('I',18.18,18.44),
                 ('dont',18.44,18.88),('see',18.88,19.52),
                 ('what',19.52,19.84)]:
 out.append({'text':word,'start_seconds':a-4.84,'end_seconds':b-4.84})
(w/'notion-rise-captions-v02.json').write_text(json.dumps({'words':out,'timing_note':'Manual correction against known lyric; timings after 4.10s estimated within model segment bounds'},indent=2))
raw=json.load(open('/private/tmp/nuviko-atlantis-extract.json'))
out=[]
for s in raw['segments']:
 for v in s.get('words',[]):
  if v['start']>=15 or v['end']<=v['start']:continue
  out.append({'text':v['word'].strip(),'start_seconds':v['start'],'end_seconds':min(v['end'],15)})
out.append({'text':'my','start_seconds':12.36,'end_seconds':13.58})
out.sort(key=lambda v:v['start_seconds'])
(w/'atlantis-captions-v02.json').write_text(json.dumps({'words':out,'timing_note':'Whisper medium; no independent listening verification'},indent=2))
