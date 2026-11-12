import json
from pathlib import Path
w=Path(__file__).parent
for name in ('notion','atlantis'):
 raw=json.loads((w/f'{name}-vocal-ctc-segmented.json').read_text())['word_segments']
 starts=[float(x['start']) for x in raw]
 if name=='notion':
  starts[0]=0;starts[4]=1.8;starts[20]=11.32;starts[21]=13.0
 else:
  starts[0]=0; starts[15]=9.7
 words=[]
 for i,x in enumerate(raw):
  start=starts[i]; end=starts[i+1] if i+1<len(starts) else 15.0
  if name=='atlantis' and i==12: end=5.34
  text='Riiiiiseeeeee' if name=='notion' and i==0 else x['word']
  row={'text':text,'start_seconds':start,'end_seconds':end,'alignment_score':x.get('score')}
  if name=='atlantis' and i==12: row['size_multiplier']=1.0
  if name=='atlantis' and i==14:
   row['size_multiplier']=1.15;row['end_seconds']=8.4
   words.append(row)
   words.append({'text':'no','start_seconds':8.4,'end_seconds':end,'size_multiplier':1.3,'note':'visual repetition during held no'})
  else: words.append(row)
 (w/f'{name}-vocal-caption-v02.json').write_text(json.dumps({'words':words,'note':'CTC alignment after vocal separation with context anchors and manual reconciliation; listening verification pending'},indent=2))
