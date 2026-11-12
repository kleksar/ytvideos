import json,pathlib,sys,hashlib
root=pathlib.Path('/Users/diplomat/ytvideos'); out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';source=root/'channels/paper_detour/videos/003_iq_gallery/Source';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];refs=json.loads((out/'refs.json').read_text())
def call(name,args):
 res=c.request('tools/call',{'name':name,'arguments':args});texts=[v['text'] for v in res.get('content',[]) if v.get('type')=='text']
 if res.get('isError'):raise RuntimeError((name,res))
 try:obj=json.loads(texts[0]) if len(texts)==1 else res
 except ValueError:obj=res
 with (out/'imports.jsonl').open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 return obj
assert '/root/paper_edit' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text();assert call('get_timeline',{}).get('id')=='19F2B39F'
old=source/'Images/paper_v1/marilyn.png'; checksum=hashlib.sha256(old.read_bytes()).hexdigest()
obj=call('organize_media',{'deletes':[refs['person_marilyn']]})
if hashlib.sha256(old.read_bytes()).hexdigest()!=checksum:raise RuntimeError('Original source unexpectedly changed')
for key,rel in [('person_marilyn','Images/paper_v1/marilyn_photo_ref.png'),('note_marilyn','Graphics/marilyn_note.png'),('note_reported','Graphics/reported_note.png')]:
 p=source/rel
 if not p.is_file():raise FileNotFoundError(p)
 refs[key]=call('import_media',{'source':{'path':str(p)},'name':key})['mediaRef']
(out/'refs.json').write_text(json.dumps(refs,indent=2)+'\n');(out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n')
print(json.dumps({'old_removed':obj,'imported':['person_marilyn','note_marilyn','note_reported']}))
