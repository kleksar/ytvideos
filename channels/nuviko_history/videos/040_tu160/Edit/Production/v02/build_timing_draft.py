import json, numpy as np
from pathlib import Path
root=Path(__file__).resolve().parents[3]
p=json.loads((root/'Edit/Production/v01/plan.json').read_text()); scenes=p['scenes']; total=scenes[-1]['end_frame']
# Additional distinct existing views chosen for a second narrative beat, not another crop of the same image.
extra={81:2,100:86,85:24,17:23,2:7,59:51,103:44,5:21,39:43,98:97,70:68,29:68,64:58,48:52,67:70,27:120,24:85,13:33,84:18,62:60,71:81,89:86,43:14,95:93,79:78,6:10}
events=[]
for i,s in enumerate(scenes,1):
 events.append((s['start_frame'],i,{73:82,116:98}.get(i,i),'original' if i not in (73,116) else 'replacement_candidate'))
 if i in extra:events.append(((s['start_frame']+s['end_frame'])//2,i,extra[i],'supplementary'))
events.sort(); n=len(events); assert n==145
# Find a globally contiguous 4–6-second sequence closest to storyboard cue positions.
inf=1e30; prev=np.full(total+1,inf);prev[0]=0;backs=[]
for k in range(1,n+1):
 best=np.full(total+1,inf);choice=np.zeros(total+1,dtype=np.uint8)
 for d in range(120,181):
  v=prev[:total+1-d];m=v<best[d:];best[d:][m]=v[m];choice[d:][m]=d
 target=total if k==n else events[k][0]
 t=np.arange(total+1);best+=((t-target)/30)**2
 backs.append(choice);prev=best
if prev[total]>=inf:raise SystemExit('No feasible timeline')
bounds=[total];t=total
for ch in reversed(backs):t-=int(ch[t]);bounds.append(t)
bounds.reverse();assert bounds[0]==0
out=[]
for k,(target,beat,img,kind) in enumerate(events):
 src=scenes[img-1] if img != 120 else {'image':str(root/'Research/VisualReferences/tu22m_schleiffert_2014.jpg'),'camera':{'subject':'Tu-22M reference photograph: a different bomber, illustrating the range limitation'}}
 out.append({'shot_id':f'{k+1:03d}','narrative_scene':beat,'source_scene':img,'kind':kind,'image':src['image'],'start_frame':bounds[k],'end_frame':bounds[k+1],'duration_seconds':round((bounds[k+1]-bounds[k])/30,3),'target_start_frame':target,'purpose':src['camera']['subject']})
path=root/'Edit/Production/v02/shot_map_draft_v01.json';path.write_text(json.dumps({'status':'DRAFT_UNREVIEWED','fps':30,'total_frames':total,'audio':p['audio'],'subtitles_unchanged':True,'shots':out},ensure_ascii=False,indent=2)+'\n')
print('shots',n,'duration range frames',min(bounds[i+1]-bounds[i] for i in range(n)),max(bounds[i+1]-bounds[i] for i in range(n)),'maximum boundary shift seconds',round(max(abs(bounds[i]-events[i][0]) for i in range(n))/30,2))
print('saved',path)
