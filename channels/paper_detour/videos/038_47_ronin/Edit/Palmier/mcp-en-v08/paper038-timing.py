from pathlib import Path
import json,collections,array,math
p=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/038_47_ronin');sc=json.loads((p/'Storyboard/SCENE_ALIGNMENT_EN_v01.json').read_text())['scenes'];total=18426;n=len(sc)
raw=[('C01','S008',32.82,34.62,"someone else's fight"),('C02','S009',36.66,37.02,'a crime'),('C03','S010',41.88,43.02,'two sword strikes'),('C04','S024',108.54,109.44,'seppuku'),('C05','S031',140.04,141.48,'masterless samurai'),('C06','S060',263.52,265.14,'restore the house has failed'),('C07','S075',325.5,326.88,'forty-seven men remain'),('C08','S098',425.28,426.42,'revenge is complete'),('C09','S103',445.2,446.46,'forty-six surrender'),('C10','S128',548.22,549.18,'seventeen forty-eight'),('C11','S139',597.78,599.16,'paid for it with their lives'),('C12','S141',607.2,608.34,'remains unanswered')]
cues=[];lower={};upper={}
for id,s,a,b,phrase in raw:
 start=round(a*30)-4;end=max(start+36,round(b*30)+9);i=int(s[1:]);upper[i-1]=min(upper.get(i-1,total),start);lower[i]=max(lower.get(i,0),end)
 cues.append(dict(cue=id,scene=s,trigger=phrase,speech_start=a,speech_end=b,startFrame=start,endFrame=end,timing_source='Palmier inspect_media full EN ASR word timestamps; selected against current script. Not listening validation.'))
prev=[float('inf')]*(total+1);prev[0]=0;backs=[]
for i in range(1,n+1):
 lo=max(i*120,total-(n-i)*180,lower.get(i,0));hi=min(i*180,total-(n-i)*120,upper.get(i,total));cur=[float('inf')]*(total+1);bp=array.array('i',[-1])*(total+1);q=collections.deque();target=round(sc[i]['speech_start']*30)if i<n else total
 for t in range(lo,hi+1):
  candidates=range(max(0,t-180),t-119)if t==lo else [t-120]
  for x in candidates:
   while q and prev[q[-1]]>=prev[x]:q.pop()
   q.append(x)
  while q and q[0]<t-180:q.popleft()
  if q and math.isfinite(prev[q[0]]):cur[t]=prev[q[0]]+(t-target)**2;bp[t]=q[0]
 backs.append(bp);prev=cur
assert math.isfinite(prev[total]);bounds=[total];t=total
for bp in reversed(backs):t=bp[t];bounds.append(t)
bounds.reverse();plan=[]
for i,s in enumerate(sc):plan.append({'scene':s['scene'],'startFrame':bounds[i],'endFrame':bounds[i+1],'speech_start':s['speech_start'],'speech_end':s['speech_end'],'cut_offset_seconds':round(bounds[i]/30-s['speech_start'],3)})
for id in ['ES01','ES02']:plan.append({'scene':id,'startFrame':total,'endFrame':total+150});total+=150
for c in cues:
 s=next(x for x in plan if x['scene']==c['scene']);assert s['startFrame']<=c['startFrame']<c['endFrame']<=s['endFrame'],(c,s)
(p/'Edit/Palmier/mcp-en-v08/scene-frame-plan-en-draft.json').write_text(json.dumps({'status':'ASSEMBLY_DRAFT; 4–6s bound, voice-guided cuts; semantic cut review pending','scenes':plan},indent=2))
(p/'Source/Graphics/captions_en_v02/CUE_TIMING_EN_v02.json').write_text(json.dumps({'fps':30,'source':'Edit/Palmier/mcp-en-v08/voice-full-inspection.json','cues':cues},indent=2))
print('planned',len(plan),'scenes',total,'frames; maxcut offset',max(abs(x.get('cut_offset_seconds',0))for x in plan))
