import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parent; P='B1BA2D18'; T='58E4A048'
s=importlib.util.spec_from_file_location('p','/Users/diplomat/ytvideos/automation/palmier/inspect_connection.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); c=m.PalmierConnection(); c.connect()
def call(name,args):
 result=c.request('tools/call',{'name':name,'arguments':args})
 with (R/'receipts.jsonl').open('a') as f: f.write(json.dumps({'name':name,'arguments':args,'response':result},ensure_ascii=False)+'\n')
 if result.get('isError'): raise RuntimeError(str(result))
 return json.loads(result['content'][0]['text'])
a=c.read_tool('get_media',{'projectId':P}); t=c.read_tool('get_timeline',{'projectId':P,'timelineId':T}); sc=next(x for x in t['tracks'] if x['name']=='Scenes')['clips']; shots=json.loads((R.parent.parent/'Storyboard/SHOTLIST_v06.json').read_text()); assets={x['id']:x for x in a['assets']}; assert len(sc)==len(shots)==39
for i,(clip,shot) in enumerate(zip(sc,shots),1):
 assert clip['frames']==[shot['startFrame'],shot['endFrame']]
 k=clip['keyframes']; assert set(k)=={'position','scale'} and len(k['position'])==len(k['scale'])==2 and [x[0] for x in k['position']]==[x[0] for x in k['scale']]
 path=R.parent/'parallax_trial_20261102'/f"{assets[clip['mediaRef']]['name']}.mp4"; assert path.is_file(),path
(R/'source_timeline.json').write_text(json.dumps(t,ensure_ascii=False,indent=2))
new=call('create_timeline',{'projectId':P,'from':T,'name':'Clothing History — parallax 75% alternating'}); print('CREATE',json.dumps(new,ensure_ascii=False),flush=True)
newid=new['timelineId']; (R/'timeline_id.txt').write_text(newid+'\n')
copy=c.read_tool('get_timeline',{'projectId':P,'timelineId':newid}); assert len(next(x for x in copy['tracks'] if x['name']=='Scenes')['clips'])==39
(R/'baseline.json').write_text(json.dumps(copy,ensure_ascii=False,indent=2))
snapshot=call('manage_snapshots',{'projectId':P,'timelineId':newid,'action':'save','name':'Before gentler alternating parallax'}); print('SNAPSHOT',json.dumps(snapshot,ensure_ascii=False),flush=True)
