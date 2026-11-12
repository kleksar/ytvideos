import json,pathlib,sys
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];refs=json.loads((out/'refs.json').read_text());log=out/'edit_receipt.jsonl'
def call(name,args):
 if '/root/paper_edit' not in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text():raise RuntimeError('lock lost')
 res=c.request('tools/call',{'name':name,'arguments':args});texts=[v['text'] for v in res.get('content',[]) if v.get('type')=='text']
 if res.get('isError'):raise RuntimeError((name,res))
 try:obj=json.loads(texts[0]) if len(texts)==1 else res
 except ValueError:obj=res
 with log.open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n')
 return obj
assert call('get_timeline',{}).get('id')=='19F2B39F'
a=call('add_clips',{'entries':[{'mediaRef':refs['background'],'startFrame':0,'endFrame':912},{'mediaRef':refs['music'],'startFrame':0,'endFrame':912}]})
b=call('add_clips',{'entries':[{'mediaRef':refs['person_haha'],'startFrame':0,'endFrame':114}]})
t=call('get_timeline',{})
(out/'base_state.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'added_base':a,'added_person':b,'tracks':t.get('tracks')},ensure_ascii=False))
