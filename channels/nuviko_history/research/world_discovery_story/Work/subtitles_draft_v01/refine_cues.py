import json,textwrap
from pathlib import Path
p=Path(__file__).parent
old=json.loads((p/'cues_source_DRAFT.json').read_text())['cues']
new=[]
for c in old:
 c=dict(c)
 if new and c['end_seconds']-c['start_seconds']<0.9 and len(new[-1]['text'])+len(c['text'])+1<=78 and c['end_seconds']-new[-1]['start_seconds']<=6:
  new[-1]['text']+=' '+c['text'];new[-1]['end_seconds']=c['end_seconds']
 else:new.append(c)
for c in new:
 lines=textwrap.wrap(c['text'],width=42,break_long_words=False,break_on_hyphens=False)
 c['text']='\n'.join(lines)
(p/'cues_source_v02_DRAFT.json').write_text(json.dumps({'cues':new},ensure_ascii=False,indent=2)+'\n')
print('cues',len(old),'->',len(new))
