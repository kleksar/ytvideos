import json,sys
from pathlib import Path
sys.path.insert(0,'automation/palmier')
from inspect_connection import PalmierConnection
c=PalmierConnection();c.connect();d=Path('channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Edit/renewal_20261102');scenes=json.loads((d/'motion_prepared.json').read_text()); assert len(scenes)==7 and all(x.get('video') for x in scenes)
args={'projectId':'31F93804','timelineId':'7537BAE9'}
def call(name,params):
 r=c.request('tools/call',{'name':name,'arguments':params});
 with (d/'motion_apply_receipts.jsonl').open('a') as f:f.write(json.dumps({'name':name,'args':params,'result':r})+'\n')
 if r.get('isError'):raise RuntimeError(r)
 return json.loads(r['content'][0]['text'])
before=call('get_timeline',args);(d/'before_motion_timeline.json').write_text(json.dumps(before,indent=2));track=next(t for t in before['tracks'] if t.get('name')=='Scenes');assert [(x['frames'],x['mediaRef']) for x in track['clips']]==[(s['source']['frames'],s['source']['mediaRef']) for s in scenes]
call('manage_snapshots',{**args,'action':'save','name':'Short 02 renewal before motion replacement'});entries=[]
for s in scenes:
 imp=call('import_media',{'projectId':args['projectId'],'source':{'path':s['video']},'folder':'Renewal 20261102 Motion'});entries.append({'mediaRef':imp['mediaRef'],'startFrame':s['source']['frames'][0],'endFrame':s['source']['frames'][1],'trackIndex':track['index'],'includeAudio':False})
call('add_clips',{**args,'entries':entries});after=call('get_timeline',args);(d/'after_motion_timeline.json').write_text(json.dumps(after,indent=2));
other=lambda a:[t for t in a['tracks'] if t.get('name')!='Scenes'];assert other(before)==other(after),'Non-scene track changed'
assert [(x['frames'],x['mediaRef']) for x in next(t for t in after['tracks'] if t.get('name')=='Scenes')['clips']]==[([e['startFrame'],e['endFrame']],e['mediaRef']) for e in entries]
print('Applied seven motion clips; other tracks exactly match baseline.')
