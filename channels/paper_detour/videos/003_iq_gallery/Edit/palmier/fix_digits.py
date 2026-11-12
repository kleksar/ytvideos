import json,pathlib,sys,base64
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];ids=json.loads((out/'remaining_ids.json').read_text());first=json.loads((out/'first_ids.json').read_text())
def call(name,args):
 assert '/root/paper_edit' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text();res=c.request('tools/call',{'name':name,'arguments':args})
 if res.get('isError'):raise RuntimeError((name,res))
 texts=[x['text'] for x in res.get('content',[]) if x.get('type')=='text'];obj=json.loads(texts[0]) if len(texts)==1 else {'texts':texts}
 if name=='inspect_timeline':
  for j,x in enumerate(res.get('content',[])):
   if x.get('type')=='image':(out/f'fixed_{args["startFrame"]}_{j}.png').write_bytes(base64.b64decode(x['data']))
 with (out/'edit_receipt.jsonl').open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n');return obj
assert call('get_timeline',{})['id']=='19F2B39F'
r=call('manage_exports',{'action':'list'});print('exports',r,flush=True)
for e in r.get('exports',[]):
 if e.get('jobId')=='F99E7940-E2EF-47EC-BAE5-B9C666F2FA5A' and e.get('status') in ['started','queued','exporting','inProgress','running']:
  print('cancel',call('manage_exports',{'action':'cancel','jobId':e['jobId']}),flush=True)
for n,x in [('9',.26),('7',.50)]:
 call('set_keyframes',{'clipId':first['digit_'+n],'property':'position','keyframes':[[0,x,.70,'hold'],[15,x,.70,'smooth'],[43,x,.50,'smooth'],[93,x,.50,'smooth'],[113,x-1,.50,'smooth']]})
scores=['97','123','125','139','150','152','160','220+']
for i in range(1,8):
 n=len(scores[i]);w=.20 if n==3 else .18
 for j in range(n):
  x=(1-w*n)/2+j*w;d=135
  rows=[[0,x+1,.72,'smooth'],[20,x,.72,'smooth'],[35,x,.72,'smooth'],[63,x,.50,'smooth'],[d-21,x,.50,'smooth'],[d-1,x-1 if i<7 else x,.50,'smooth']]
  call('set_keyframes',{'clipId':ids[f'digit_{i}_{j}'],'property':'position','keyframes':rows})
for f in [0,15,100,114,130,228,342,456,570,684,798]:call('inspect_timeline',{'startFrame':f})
print('DONE')
