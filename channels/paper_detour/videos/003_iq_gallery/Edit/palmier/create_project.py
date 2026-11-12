import json,pathlib,sys
root=pathlib.Path('/Users/diplomat/ytvideos'); out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier'
sys.path.insert(0,str(root/'automation/palmier'))
from inspect_connection import PalmierConnection
lock=root/'channels/paper_detour/.rarovista-timeline-lock/owner.md'
if not lock.exists() or '/root/paper_edit' not in lock.read_text(): raise RuntimeError('We do not own the lock')
c=PalmierConnection();c.connect()
def call(name,args):
 res=c.request('tools/call',{'name':name,'arguments':args})
 if res.get('isError'): raise RuntimeError((name,res))
 texts=[v['text'] for v in res.get('content',[]) if v.get('type')=='text']
 try: return json.loads(texts[0]) if len(texts)==1 else res
 except ValueError: return res
projects=call('manage_project',{'action':'list'})
name='Paper Detour 003 IQ Gallery 20261031'
if any(p.get('name')==name for p in projects.get('projects',[])): raise RuntimeError('Project exists; refuse duplicate')
project=call('manage_project',{'action':'create','name':name,'aspectRatio':'9:16','quality':'1080p','fps':30})
timeline=call('get_timeline',{})
(out/'project_receipt.json').write_text(json.dumps({'project':project,'timeline':timeline},ensure_ascii=False,indent=2)+'\n')
(out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n')
print(json.dumps({'project':project,'timeline_id':timeline.get('id'),'fps':timeline.get('fps'),'width':timeline.get('width'),'height':timeline.get('height')},ensure_ascii=False))
