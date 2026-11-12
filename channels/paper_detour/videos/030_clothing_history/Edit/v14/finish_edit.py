from pathlib import Path
exec((Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history/Edit/v14/prepare_edit.py').read_text().split("assert not (E/'target.json').exists()")[0]))
tid=json.loads((E/'target.json').read_text())['timelineId'];scope={'projectId':pid,'timelineId':tid};n=json.loads((E/'neighbor_pending.json').read_text());sheet=json.loads((E/'cue_sheet_before_neighbor.json').read_text());q=next(x for x in sheet if x['id']=='D16')
c.call('move_clips',{**scope,'moves':[{'clipId':q['clipId'],'toFrame':2436}]},True)
D=2558-2436;c.call('set_clip_properties',{**scope,'clipIds':[q['clipId']],'durationFrames':D},True)
for prop,key in [('position','position_keys'),('opacity','opacity_keys')]:
 keys=q[key];keys[-2][0]=D-5;keys[-1][0]=D-1;c.call('set_keyframes',{**scope,'clipId':q['clipId'],'property':prop,'keyframes':keys},True)
q['startFrame']=2436;q['neighbor_change']='Delayed2frames to separate D13 exit; end2558 retained'
state=c.call('get_timeline',scope);save(E/'timeline_final.json',state)
for q in sheet:
 clip=next(x for tr in state['tracks'] for x in tr.get('clips',[]) if x['id']==q['clipId']);assert clip['frames']==[q['startFrame'],q['endFrame']];q['position_keys']=clip['keyframes']['position'];q['opacity_keys']=clip['keyframes']['opacity']
assert state['width']==2560 and state['height']==1440 and state['fps']==30 and state['totalFrames']==5700
save(P/'Storyboard/CUE_SHEET_v14.json',sheet)
shots=json.loads((P/'Storyboard/SHOTLIST_v13.json').read_text());tr=next(x for x in state['tracks'] if x['name']=='Scenes')
for s in shots:
 cl=next(x for x in tr['clips'] if x['frames'][0]==s['startFrame']);s['clipId']=cl['id'];s['camera_keyframes']=cl['keyframes'];s['state_evidence']='Edit/v14/timeline_final.json'
save(P/'Storyboard/SHOTLIST_v14.json',shots)
save(E/'final_snapshot.json',c.call('manage_snapshots',{**scope,'action':'save','name':'v14 corrected cue exits and 2K canvas — ready for offline QA'},True))
save(E/'OWNERSHIP.json',{'owner':'codex-030-v14','status':'active','projectId':pid,'timelineId':tid,'scope':'Seven cue repairs plus D16 two-frame deconfliction;2K delivery,SRT,QA,local promotion; preserve accepted audio and v13 timeline'})
save(E/'POST_EDIT.json',{'fingerprint':fingerprint(state),**scope,'source_timelineId':src,'width':2560,'height':1440,'fps':30,'frame_count':5700})
print('ready',tid,'tracks',[(x['name'],len(x.get('clips',[]))) for x in state['tracks']],flush=True)
# Preflight actual compositor on all newly crossed scene/cue pairs and neighbour.
import base64
pre=E/'Preflight';pre.mkdir(exist_ok=True)
for i in [553,555,973,975,1557,2431,2433,2436,2855,2857,3148,3150,4099,4101]:
 r=c.connection.request('tools/call',{'name':'inspect_timeline','arguments':{**scope,'startFrame':i}})
 (pre/f'{i}.json').write_text(json.dumps({k:v for k,v in r.items() if k!='content'}))
 imgs=[x for x in r.get('content',[]) if x.get('type')=='image']
 for j,x in enumerate(imgs):(pre/f'f{i}_{j}.png').write_bytes(base64.b64decode(x['data']))
 print('preflight',i,len(imgs),flush=True)
