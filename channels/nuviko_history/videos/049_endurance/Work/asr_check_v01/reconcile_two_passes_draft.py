import json,pathlib,math
p=pathlib.Path(__file__).parent
A=json.load(open(p/'whisperx_chunks_raw_v01.json'))['result']['word_segments'];B=json.load(open(p/'whisperx_chunks_shifted_raw_v01.json'))['result']['word_segments']; assert len(A)==len(B) and all(x['word']==y['word'] for x,y in zip(A,B))
def cost(w,shift):
 t=w['start'];score=w.get('score',0);phase=(t-shift)%20;dist=min(phase,20-phase)
 return (1-score)*.5 + max(0,1.5-dist)*.7 + (1.5 if w['end']-t>1.5 else 0)
dp=[];back=[]
for i in range(len(A)):
 cur=[A[i],B[i]];row=[];parents=[]
 for j,w in enumerate(cur):
  c=cost(w,0 if j==0 else 10)
  if i==0:row.append(c);parents.append(None);continue
  choices=[]
  for k,prev in enumerate([A[i-1],B[i-1]]):
   overlap=max(0,prev['end']-w['start']); choices.append(dp[-1][k]+c+1000*overlap)
  k=min(range(2),key=choices.__getitem__);row.append(choices[k]);parents.append(k)
 dp.append(row);back.append(parents)
j=min(range(2),key=dp[-1].__getitem__); choices=[]
for i in reversed(range(len(A))):choices.append(j);j=back[i][j]
choices.reverse();out=[]
for i,j in enumerate(choices):
 w=(A if j==0 else B)[i];out.append({'text':w['word'],'start':w['start'],'end':w['end'],'score':w.get('score'),'chosen_pass':'original' if j==0 else 'shifted','start_disagreement_seconds':round(abs(A[i]['start']-B[i]['start']),3)})
over=[i for i in range(1,len(out)) if out[i]['start']<out[i-1]['end']]
report={'status':'DIAGNOSTIC_NOT_FOR_RENDER','method':'Dynamic programming chooses between estimates using local confidence and distance from 20-second chunk boundary; penalizes interval overlap. Heuristics do not establish actual speech timing. No user audio-sync or final edit acceptance. Punctuation/tokenization not conformed to transcript.','counts':{'words':len(out),'original_selected':choices.count(0),'shifted_selected':choices.count(1),'remaining_overlaps':len(over),'start_disagreement_gt_150ms':sum(x['start_disagreement_seconds']>.15 for x in out)},'overlap_indices':over,'words':out}
(p/'hybrid_alignment_diagnostic_v01.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(report['counts'])
