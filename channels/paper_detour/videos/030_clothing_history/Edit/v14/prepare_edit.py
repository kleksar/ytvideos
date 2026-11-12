from pathlib import Path
import sys,json,copy,math
ROOT=Path('/Users/diplomat/ytvideos');sys.path.insert(0,str(ROOT))
from automation.image_motion.run import Palmier,fingerprint,save
P=ROOT/'channels/paper_detour/videos/030_clothing_history';E=P/'Edit/v14';c=Palmier(E);pid='B1BA2D18';src='82684371'
assert not (E/'target.json').exists()
base=c.call('get_timeline',{'projectId':pid,'timelineId':src});save(E/'baseline.json',base)
snapshot=c.call('manage_snapshots',{'projectId':pid,'timelineId':src,'action':'save','name':'Accepted v13 before v14 cue repairs and 2K delivery'},True);save(E/'baseline_snapshot.json',snapshot)
created=c.call('create_timeline',{'projectId':pid,'from':src,'name':'Clothing History v14 — corrected accents, final 2K'},True);save(E/'target.json',created);print('created',created,flush=True)
tid=created['timelineId'];scope={'projectId':pid,'timelineId':tid};state=c.call('get_timeline',scope);save(E/'cloned.json',state)
assert fingerprint(base)==fingerprint(state)
c.call('set_project_settings',{**scope,'width':2560,'height':1440,'outputColorSpace':'rec709'},True)
sheet=json.loads((P/'Storyboard/CUE_SHEET_v13.json').read_text());audit=json.loads((P/'Edit/ComplianceAudit_20261102/CUE_TIMING_AUDIT.json').read_text());ar={x['id']:x for x in audit['rows']}
oldtr=next(x for x in base['tracks'] if x['name']=='Accents');newtr=next(x for x in state['tracks'] if x['name']=='Accents');oldby={x['id']:x for x in oldtr['clips']};newby={(x['frames'][0],x['mediaRef']):x for x in newtr['clips']};changes=[]
for q in sheet:
 old=oldby[q['clipId']];clip=newby[(old['frames'][0],old['mediaRef'])];q['clipId']=clip['id']
 if ar[q['id']]['status']=='FAIL':
  fade=math.ceil((ar[q['id']]['speech_end']+0.005)*30);end=fade+5;start=q['startFrame'];D=end-start
  c.call('set_clip_properties',{**scope,'clipIds':[clip['id']],'durationFrames':D},True)
  keys=copy.deepcopy(clip['keyframes']);keys['opacity'][-2][0]=D-5;keys['opacity'][-1][0]=D-1;keys['position'][-2][0]=D-5;keys['position'][-1][0]=D-1
  for prop in ('position','opacity'):c.call('set_keyframes',{**scope,'clipId':clip['id'],'property':prop,'keyframes':keys[prop]},True)
  changes.append({'cue':q['id'],'before_frames':old['frames'],'after_frames':[start,end],'fade_start':fade,'speech_end':ar[q['id']]['speech_end'],'spill_scenes':[x['id'] for x in json.loads((P/'Storyboard/SHOTLIST_v13.json').read_text()) if x['startFrame']<end and x['endFrame']>start]})
  q['endFrame']=end;q['opacity_keys']=keys['opacity'];q['position_keys']=keys['position']
 q['status']='IMPLEMENTED_v14; final QA pending';q['current_timing_audit']='Edit/v14/CUE_REPAIRS.json';q['v13_preflight']='Historical v13; current review in Edit/v14'
# D13 exit now ends2436. Delay neighbouring D16 two frames to prevent superimposed labels.
q=next(x for x in sheet if x['id']=='D16');clip=next(x for x in newtr['clips'] if x['id']==q['clipId']);print('move schema',c.schemas['move_clips']['inputSchema'],flush=True)
save(E/'cue_sheet_before_neighbor.json',sheet);save(E/'CUE_REPAIRS.json',changes);save(E/'neighbor_pending.json',{'cue':'D16','clipId':q['clipId'],'from':2434,'to':2436,'keep_end':2558})
save(E/'after_seven.json',c.call('get_timeline',scope));print('target',tid,flush=True)
