import json,pathlib,math,bisect
w=pathlib.Path('Work');plan=json.load(open(w/'mix_subtitle_preflight_prefer_b_v02.json'));words=json.load(open(w/'word_map_mix_prefer_b_draft_v02.json'))['words'];scenes=plan['scenes'];targets=[0]+[s['end_frame'] for s in scenes];N=len(scenes);end=targets[-1]; fps=30
# Mark estimated word interiors. Exact boundaries remain model estimates, not listening.
blocked=[False]*(end+1)
for x in words:
 for f in range(max(1,math.floor(x['start']*fps)+1),min(end,math.ceil(x['end']*fps))):
  if x['start'] < f/fps < x['end']:blocked[f]=True
for radius in [60,90,150,300]:
 dp={0:0}; history=[]
 for i in range(1,N+1):
  candidates=[end] if i==N else range(max(1,targets[i]-radius),min(end,targets[i]+radius)+1)
  nxt={};parents={}
  for c in candidates:
   if i<N and blocked[c]:continue
   if i==110 and not (15315 <= c <= 15328): continue
   options=[(dp[p],p) for p in range(c-180,c-119) if p in dp]
   if not options:continue
   val,prev=min(options);penalty=(c-targets[i])**2;nxt[c]=val+penalty;parents[c]=prev
  if not nxt:break
  dp=nxt;history.append(parents)
 if len(history)==N and end in dp:break
else:raise ValueError('no feasible sequence')
cuts=[end]; cur=end
for parents in reversed(history):cur=parents[cur];cuts.append(cur)
cuts.reverse(); assert cuts[0]==0 and all(120<=b-a<=180 for a,b in zip(cuts,cuts[1:])); assert all(not blocked[x] for x in cuts[1:-1])
new=json.loads(json.dumps(plan));changes=[]
for i,s in enumerate(new['scenes']):
 before=(s['start_frame'],s['end_frame']);s['start_frame']=cuts[i];s['end_frame']=cuts[i+1];
 if before!=(cuts[i],cuts[i+1]):changes.append({'scene':i+1,'old':before,'new':[cuts[i],cuts[i+1]]})
new['status']='DIAGNOSTIC_ONLY_NOT_FOR_RENDER';(w/'mix_word_safe_prefer_b_draft_v02.json').write_text(json.dumps(new,ensure_ascii=False,indent=2)+'\n')
report={'status':'DRAFT_REQUIRES_SEMANTIC_AND_AUDIBLE_REVIEW','reason':'Scene cuts mechanically moved outside estimated word intervals for prefer-B draft map. Word timestamps are not proven; changes may affect meaning and need review. S110 end is constrained to remain after Lunch O and before Then according to draft map.','radius_frames':radius,'scenes':N,'changed_scenes':len(changes),'max_cut_shift_frames':max(abs(cuts[i]-targets[i]) for i in range(len(cuts))),'changes':changes};(w/'CUT_RECOMPUTE_B_DRAFT_v02.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='changes'})
