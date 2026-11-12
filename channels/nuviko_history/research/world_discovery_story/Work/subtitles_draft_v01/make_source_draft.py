import json,hashlib,re
from pathlib import Path
base=Path(__file__).resolve().parents[2]; out=Path(__file__).parent
orig=json.loads((base/'Work/voice_qa_v01/forced_blocks_raw.json').read_text())
joint=json.loads((base/'Work/voice_qa_v01/joint_boundaries_3pairs_DRAFT.json').read_text())
segments=orig['result']['segments']; words=[dict(w) for s in segments for w in s['words']]
for seg in joint['result']['segments']:
 repl=seg['words']; tokens=[w['word'] for w in repl]
 locations=[i for i in range(len(words)-len(tokens)+1) if [w['word'] for w in words[i:i+len(tokens)]]==tokens]
 if len(locations)!=1: raise ValueError((tokens,locations))
 i=locations[0]; words[i:i+len(tokens)]=[dict(w) for w in repl]
text=(base/'Source/Voice/narration-en-v01.txt').read_text().strip()
if ' '.join(w['word'] for w in words).split()!=text.split(): raise ValueError('token mismatch')
for i,w in enumerate(words):
 if w['start']>=w['end'] or (i and w['start']<words[i-1]['end']): raise ValueError(('overlap',i,words[i-1:i+1]))
# Group within original sentences. Clause-aware grouping is a conservative initial heuristic, not editorial approval.
cues=[]; idx=0
for segment in segments:
 n=len(segment['words']); group=words[idx:idx+n]; idx+=n
 current=[]
 for w in group:
  current.append(w)
  txt=' '.join(x['word'] for x in current)
  if len(current)>=8 or (len(current)>=4 and re.search(r'[,;:.!?]$',txt)):
   cues.append({'start_seconds':current[0]['start'],'end_seconds':current[-1]['end'],'text':txt});current=[]
 if current: cues.append({'start_seconds':current[0]['start'],'end_seconds':current[-1]['end'],'text':' '.join(w['word'] for w in current)})
out.joinpath('word_map_source_DRAFT.json').write_text(json.dumps({'status':'DRAFT; audio listening and edit conform UNVERIFIED','audio_sha256':orig['audio_sha256'],'text_sha256':orig['text_sha256'],'words':[{'text':w['word'],'start':w['start'],'end':w['end']} for w in words]},ensure_ascii=False,indent=2)+'\n')
out.joinpath('cues_source_DRAFT.json').write_text(json.dumps({'cues':cues},ensure_ascii=False,indent=2)+'\n')
print('tokens',len(words),'cues',len(cues),'last end',words[-1]['end'])
