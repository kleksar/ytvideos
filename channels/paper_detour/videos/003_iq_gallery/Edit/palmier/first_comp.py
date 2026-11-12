import json,pathlib,sys,base64
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];refs=json.loads((out/'refs.json').read_text());log=out/'edit_receipt.jsonl'
def call(name,args,inspect=False):
 if '/root/paper_edit' not in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text():raise RuntimeError('lock lost')
 res=c.request('tools/call',{'name':name,'arguments':args})
 if res.get('isError'):raise RuntimeError((name,res))
 texts=[v['text'] for v in res.get('content',[]) if v.get('type')=='text']
 try:obj=json.loads(texts[0]) if len(texts)==1 else {'texts':texts}
 except ValueError:obj={'texts':texts}
 if inspect:
  for i,v in enumerate(res.get('content',[])):
   if v.get('type')=='image':(out/f'first_inspect_{args.get("startFrame")}_{i}.png').write_bytes(base64.b64decode(v['data']))
 with log.open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n')
 return obj
def key(cid,prop,rows):return call('set_keyframes',{'clipId':cid,'property':prop,'keyframes':rows})
def add(keyname):return call('add_clips',{'entries':[{'mediaRef':refs[keyname],'startFrame':0,'endFrame':114}]})['clips'][0]['id']
assert call('get_timeline',{}).get('id')=='19F2B39F'
p='B9BB3090'; key(p,'scale',[[0,.64,.54]]);key(p,'position',[[0,.18,.13,'smooth'],[93,.18,.13,'smooth'],[113,-.82,.13,'smooth']])
ids={}
for n,x in [('9',.26),('7',.50)]:
 cid=add('digit_'+n);ids['digit_'+n]=cid;key(cid,'scale',[[0,.23,.13]]);key(cid,'position',[[0,x,.78,'hold'],[15,x,.78,'smooth'],[43,x,.56,'smooth'],[93,x,.56,'hold'],[113,x-1,.56,'smooth']])
fg=call('add_clips',{'entries':[{'mediaRef':refs['foreground'],'startFrame':0,'endFrame':912}]})['clips'][0]['id'];ids['fg']=fg;key(fg,'scale',[[0,1.12,.355]]);key(fg,'position',[[0,-.06,.50,'smooth'],[911,-.08,.50,'smooth']])
n=add('name_haha');ids['name']=n;key(n,'scale',[[0,.74,.142]]);key(n,'position',[[0,.13,.075,'smooth'],[93,.13,.075,'hold'],[113,-.87,.075,'smooth']])
note=add('note_reported');ids['note']=note;key(note,'scale',[[0,.67,.212]]);key(note,'position',[[0,.165,.75,'smooth'],[93,.165,.75,'hold'],[113,-.835,.75,'smooth']])
for f in [0,30,60,100]:call('inspect_timeline',{'startFrame':f},True)
(out/'first_ids.json').write_text(json.dumps(ids,indent=2)+'\n')
print(json.dumps(ids))
