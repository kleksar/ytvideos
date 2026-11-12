import hashlib,json,re
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
ep=Path(__file__).resolve().parents[2]
wmap=ep/'Work/word-times-final-v01.json'
source=ep/'Work/word-times-source.json'
mix=ep/'Assets/Audio/full-mix-v02.wav'
alignment=ep/'Assets/Audio/voice_en.alignment.json'
text=ep/'Source/narration-en-v02.txt'
srt=ep/'Deliverables/Brocklesby-en-v01.srt'
mp4=ep/'Deliverables/Brocklesby-Paper-Detour-en-v01.mp4'
ev=json.loads((ep/'Edit/QA/exact-check-v01.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
w=json.loads(wmap.read_text())
assert w['audio_sha256']==sha(mix)
provider=json.loads(source.read_text())
ww=w['words']
for u,v in zip(provider['words'],ww):
 assert abs(u['start_seconds']/1.1-v['start'])<1e-7 and abs(u['end_seconds']/1.1-v['end'])<1e-7
assert len(ww)==len(provider['words'])==102
def to_ms(v): return int((Decimal(str(v))*1000).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
def ms(t):
 h,m,s,z=map(int,re.split('[:,]',t));return ((h*60+m)*60+s)*1000+z
i=0; log=[]
for index,block in enumerate(srt.read_text().strip().split('\n\n'),1):
 no,interval,*lines=block.splitlines(); t=' '.join(lines).split()
 assert no==str(index)
 a,b=map(ms,interval.split(' --> '))
 z=ww[i:i+len(t)]
 assert [k['text'] for k in z]==t
 assert (a,b)==(to_ms(z[0]['start']),to_ms(z[-1]['end']))
 i+=len(t)
 log.append(dict(index=index,start_ms=a,end_ms=b,words=len(t)))
assert i==102 and log[-1]['end_ms']<36000
assert ev['sha256']==sha(mp4)
payload=dict(language='en',media_sha256=sha(mp4),structure='PASS',text_coverage='PASS',timing_mapping='PASS',playback='UNVERIFIED',fps='30/1',duration_seconds=36,edit_revision='edit-v01',cue_boundaries=log,dependencies=[dict(path=str(x),sha256=sha(x)) for x in (text,srt,source,wmap,mix,alignment)],method='Compared every serialized cue first/last word and milliseconds to the final word map; one 1.10x conform from provider timing. Exact MP4 sound correlation proves no extra shift or speed change within PCM sample tolerance; subjective playback not performed.')
(ep/'Edit/QA/srt-review-v01.json').write_text(json.dumps(payload,indent=2)+'\n')
print(len(log),'cues; 102 exact tokens')
