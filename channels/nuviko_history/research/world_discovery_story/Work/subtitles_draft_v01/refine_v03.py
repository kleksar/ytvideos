import json,textwrap
from pathlib import Path
p=Path(__file__).parent
c=json.loads((p/'cues_source_v02_DRAFT.json').read_text())['cues'];w=json.loads((p/'word_map_source_DRAFT.json').read_text())['words']
# Reflow an orphaned ending at actual word boundaries, retaining all spoken words.
i=next(i for i,x in enumerate(c) if x['text']=='of the world.')
assert ' '.join((c[i-1]['text']+' '+c[i]['text']).split())=='Stories, journeys, and observations gradually built larger pictures of the world.'
a=next(k for k,x in enumerate(w) if x['text']=='Stories,' and 180<x['start']<190)
b=next(k for k in range(a,a+20) if w[k]['text']=='gradually')
z=next(k for k in range(b,b+20) if w[k]['text']=='world.')
new=[]
for block in (w[a:b],w[b:z+1]):
 text=' '.join(x['text'] for x in block)
 new.append({'start_seconds':block[0]['start'],'end_seconds':block[-1]['end'],'text':'\n'.join(textwrap.wrap(text,42,break_long_words=False,break_on_hyphens=False))})
c[i-1:i+1]=new
# Slightly hold three dense source-time cues into the following actual gap, never over next cue.
for needle in ['At a settlement there,','first arrival may have been earlier.','than the crew had expected.']:
 i=next(i for i,x in enumerate(c) if ' '.join(x['text'].split())==needle)
 gap=c[i+1]['start_seconds']-c[i]['end_seconds'];c[i]['end_seconds']=round(c[i]['end_seconds']+min(0.2,gap/2),3)
(p/'cues_source_v03_DRAFT.json').write_text(json.dumps({'cues':c},ensure_ascii=False,indent=2)+'\n')
