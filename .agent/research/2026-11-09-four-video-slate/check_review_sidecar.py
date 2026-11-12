"""Independently check serialized SRT against the exact conformed word intervals."""
from build_review_edit import setup, ref, read, dump
from decimal import Decimal, ROUND_HALF_UP
import re,sys

def millis(seconds):
 return int((Decimal(str(seconds))*1000).quantize(Decimal('1'),rounding=ROUND_HALF_UP))

def parse(s):
 h,m,sec,ms=map(int,re.split('[:,]',s))
 return (h*3600+m*60+sec)*1000+ms

for name in sys.argv[1:]:
 ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
 sub=out.with_suffix('.srt')
 cues=read(w/'srt-cues-v01.json')['cues']
 blocks=re.split(r'\n{2,}',sub.read_text().strip())
 cur=0
 assert len(blocks)==len(cues)
 for i,(block,cue) in enumerate(zip(blocks,cues),1):
  num,times,*lines=block.splitlines(); assert num==str(i)
  observed=' '.join(lines).split()
  words=wm['words'][cur:cur+len(observed)]
  assert observed==[x['text'] for x in words]
  assert cue['start_seconds']==words[0]['start'] and cue['end_seconds']==words[-1]['end']
  assert list(map(parse,times.split(' --> ')))==[millis(words[0]['start']),millis(words[-1]['end'])]
  cur+=len(words)
 assert cur==len(wm['words'])
 dump(w/'srt-mapping-v01.json',dict(status='PASS',srt=ref(sub),audio=ref(media),word_map=ref(word),text=ref(transcript),
   alignment='Final-time provider word map; 1.10x applied once at zero, no cuts',
   all_cues=len(cues),all_words=cur,comparison='literal and exact first/last word bounds; rounding HALF_UP to ms',
   playback='UNVERIFIED'))
 print(name,len(cues),cur)
