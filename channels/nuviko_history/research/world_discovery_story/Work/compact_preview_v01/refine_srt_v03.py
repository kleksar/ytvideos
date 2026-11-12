import json,textwrap,math
from pathlib import Path
root=Path(__file__).resolve().parents[2];blocks=(root/'Edit/Subtitles/world_discovery_en_preview_v02_DRAFT.srt').read_text().strip().split('\n\n'); words=json.loads((root/'Work/montage_trial_v01/words_EXPERIMENT.json').read_text())['words'];gs=[];i=0
def parse(t):
 a,b,c=t.replace(',','.').split(':');return float(a)*3600+float(b)*60+float(c)
def stamp(t):
 m=round(t*1000);return f'{m//3600000:02}:{m//60000%60:02}:{m//1000%60:02},{m%1000:03}'
for block in blocks:
 ls=block.splitlines();t=' '.join(ls[2:]).split();n=len(t);assert t==[w['text'] for w in words[i:i+n]];start,end=ls[1].split(' --> ');gs.append({'text':t,'words':words[i:i+n],'start':parse(start),'end':parse(end)});i+=n
assert gs[166]['text'][-1]=='without'
gs[167]['text'].insert(0,gs[166]['text'].pop());gs[167]['words'].insert(0,gs[166]['words'].pop());gs[166]['end']=gs[166]['words'][-1]['end'];gs[167]['start']=gs[167]['words'][0]['start']
changed=[]
for n in (66,87,105,157,166,168):
 g=gs[n-1];chars=len(' '.join(g['text']));needed=chars/21-(g['end']-g['start'])+.012
 if needed>0:
  left=max(0,(g['start']-gs[n-2]['end'])*.45);right=max(0,(gs[n]['start']-g['end'])*.45);a=min(left,needed/2);b=min(right,needed-a);a=min(left,needed-b)
  if a+b+1e-5<needed: print('not enough room',n,needed,a+b)
  g['start']-=a;g['end']+=b;changed.append((n,round(a,3),round(b,3)))
out=[]
for k,g in enumerate(gs,1):
 lines=textwrap.wrap(' '.join(g['text']),width=42,break_long_words=False,break_on_hyphens=False);assert len(lines)<=2
 out.append(f'{k}\n{stamp(g["start"])} --> {stamp(g["end"])}\n'+'\n'.join(lines))
(root/'Edit/Subtitles/world_discovery_en_preview_v03_DRAFT.srt').write_text('\n\n'.join(out)+'\n');print('extended into bounded adjacent pauses:',changed)
