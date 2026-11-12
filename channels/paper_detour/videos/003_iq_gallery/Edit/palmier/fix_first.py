import json,pathlib,sys,base64
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];ids=json.loads((out/'first_ids.json').read_text())
def call(name,args):
 assert '/root/paper_edit' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text()
 res=c.request('tools/call',{'name':name,'arguments':args})
 if res.get('isError'):raise RuntimeError((name,res))
 texts=[v['text'] for v in res.get('content',[]) if v.get('type')=='text']
 try: obj=json.loads(texts[0]) if len(texts)==1 else {'texts':texts}
 except ValueError:obj={'texts':texts}
 if name=='inspect_timeline':
  for i,v in enumerate(res.get('content',[])):
   if v.get('type')=='image':(out/f'first_fixed_{args.get("startFrame")}_{i}.png').write_bytes(base64.b64decode(v['data']))
 with (out/'edit_receipt.jsonl').open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n');return obj
def key(cid,prop,rows):return call('set_keyframes',{'clipId':cid,'property':prop,'keyframes':rows})
assert call('get_timeline',{}).get('id')=='19F2B39F'
key('B9BB3090','position',[[0,.18,.19,'smooth'],[93,.18,.19,'smooth'],[113,-.82,.19,'smooth']])
key(ids['name'],'scale',[[0,.62,.119]]);key(ids['name'],'position',[[0,.19,.02,'smooth'],[93,.19,.02,'smooth'],[113,-.81,.02,'smooth']])
for n,x in [('9',.26),('7',.50)]:key(ids['digit_'+n],'position',[[0,x,.78,'hold'],[15,x,.78,'smooth'],[43,x,.56,'smooth'],[93,x,.56,'smooth'],[113,x-1,.56,'smooth']])
key(ids['note'],'position',[[0,.165,.75,'smooth'],[93,.165,.75,'smooth'],[113,-.835,.75,'smooth']])
key('8BC0C92A','scale',[[0,1.04,1.04]]);key('8BC0C92A','position',[[0,-.02,-.02,'smooth'],[911,-.04,-.02,'smooth']])
for f in [30,60,100]:call('inspect_timeline',{'startFrame':f})
