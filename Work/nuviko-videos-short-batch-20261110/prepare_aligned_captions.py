import json
from pathlib import Path
w=Path(__file__).parent
for name in ('notion','atlantis'):
 words=json.loads((w/f'{name}-forced-alignment.json').read_text())
 if name=='notion': words[0]['text']='Riiiiiseeeeee'
 else:
  first=next(i for i,x in enumerate(words) if x['text']=='no')
  second=next(i for i,x in enumerate(words) if i>first and x['text']=='no')
  words[first]['size_multiplier']=1
  word=words[second]; word['size_multiplier']=1.15
  mid=(word['start_seconds']+word['end_seconds'])/2
  extra=dict(word,start_seconds=mid,size_multiplier=1.30)
  word['end_seconds']=mid
  words.insert(second+1,extra)
 (w/f'{name}-aligned-captions.json').write_text(json.dumps({'words':words,'note':'Forced alignment, musical vocal timings require listening review; third no is a visual repeat within the held second no.'},indent=2))
