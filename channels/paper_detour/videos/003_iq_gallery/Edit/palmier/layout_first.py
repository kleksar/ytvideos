import json,pathlib,sys,base64
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];ids=json.loads((out/'first_ids.json').read_text())
def call(name,args):
 assert '/root/paper_edit' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text();res=c.request('tools/call',{'name':name,'arguments':args})
 if res.get('isError'):raise RuntimeError((name,res))
 texts=[v['text'] for v in res.get('content',[]) if v.get('type')=='text']
 try:obj=json.loads(texts[0]) if len(texts)==1 else {'texts':texts}
 except ValueError:obj={'texts':texts}
 if name=='inspect_timeline':
  for i,v in enumerate(res.get('content',[])):
   if v.get('type')=='image':(out/f'first_layout_{args.get("startFrame")}_{i}.png').write_bytes(base64.b64decode(v['data']))
 with (out/'edit_receipt.jsonl').open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n');return obj
def key(cid,prop,rows):return call('set_keyframes',{'clipId':cid,'property':prop,'keyframes':rows})
assert call('get_timeline',{}).get('id')=='19F2B39F'
key('B9BB3090','scale',[[0,.74,.625]]);key('B9BB3090','position',[[0,.13,.15,'smooth'],[93,.13,.15,'smooth'],[113,-.87,.15,'smooth']])
# Main name is printed on the front stage, above the Shorts bottom controls.
key(ids['name'],'scale',[[0,.70,.134]]);key(ids['name'],'position',[[0,.15,.645,'smooth'],[93,.15,.645,'smooth'],[113,-.85,.645,'smooth']])
for n,x in [('9',.26),('7',.50)]:key(ids['digit_'+n],'position',[[0,x,.78,'hold'],[15,x,.78,'smooth'],[43,x,.50,'smooth'],[93,x,.50,'smooth'],[113,x-1,.50,'smooth']])
key(ids['note'],'scale',[[0,.39,.124]]);key(ids['note'],'position',[[0,.015,.14,'smooth'],[93,.015,.14,'smooth'],[113,-.985,.14,'smooth']])
for f in [30,60,100]:call('inspect_timeline',{'startFrame':f})
