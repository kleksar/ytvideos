import json,pathlib,sys,base64
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];refs=json.loads((out/'refs.json').read_text());first=json.loads((out/'first_ids.json').read_text())
def call(name,args):
 assert '/root/paper_edit' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text()
 res=c.request('tools/call',{'name':name,'arguments':args})
 if res.get('isError'):raise RuntimeError((name,res))
 texts=[x['text'] for x in res.get('content',[]) if x.get('type')=='text']
 try: obj=json.loads(texts[0]) if len(texts)==1 else {'texts':texts}
 except ValueError:obj={'texts':texts}
 if name=='inspect_timeline':
  for j,x in enumerate(res.get('content',[])):
   if x.get('type')=='image':(out/f'gallery_{args["startFrame"]}_{j}.png').write_bytes(base64.b64decode(x['data']))
 with (out/'edit_receipt.jsonl').open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n');return obj
def key(cid,prop,rows):call('set_keyframes',{'clipId':cid,'property':prop,'keyframes':rows})
def add(entries):return call('add_clips',{'entries':entries})['clips']
assert call('get_timeline',{}).get('id')=='19F2B39F'
people=['haha','kasparov','feynman','logan_paul','nolan_gould','kate_beckinsale','tarantino','marilyn'];scores=['97','123','125','139','150','152','160','220+'];ids={}
key(first['note'],'scale',[[0,.49,.156]]);key(first['note'],'position',[[0,.005,.105,'smooth'],[93,.005,.105,'smooth'],[113,-.995,.105,'smooth']])
def span(i):return (i*114-21,(i+1)*114)
def motion(cid,i,x,y):
 start,end=span(i);d=end-start
 rows=[[0,x+1,y,'smooth'],[20,x,y,'smooth'],[d-21,x,y,'smooth']]
 if i<7:rows.append([d-1,x-1,y,'smooth'])
 else:rows.append([d-1,x,y,'smooth'])
 key(cid,'position',rows)
def create_batch(kind, parity, digit_index=None):
 indices=[i for i in range(1,8) if i%2==parity and (digit_index is None or digit_index<len(scores[i]))]
 if not indices:return
 entries=[]
 for i in indices:
  s,e=span(i);ref=kind+'_'+people[i] if digit_index is None else 'digit_'+('plus' if scores[i][digit_index]=='+' else scores[i][digit_index]);entries.append({'mediaRef':refs[ref],'startFrame':s,'endFrame':e})
 clips=add(entries)
 for i,clip in zip(indices,clips):
  cid=clip['id'];ids[f'{kind}_{i}' if digit_index is None else f'digit_{i}_{digit_index}']=cid
  if kind=='person':key(cid,'scale',[[0,.74,.625]]);motion(cid,i,.13,.15)
  elif kind=='name':key(cid,'scale',[[0,.70,.134]]);motion(cid,i,.15,.645)
  else:
   n=len(scores[i]);w=.20 if n==3 else .18;h=w*.565;x=(1-w*n)/2+digit_index*w;start,end=span(i);d=end-start
   key(cid,'scale',[[0,w,h]])
   rows=[[0,x+1,.78,'smooth'],[20,x,.78,'smooth'],[35,x,.78,'smooth'],[63,x,.50,'smooth'],[d-21,x,.50,'smooth']]
   rows.append([d-1,x-1 if i<7 else x,.50,'smooth']);key(cid,'position',rows)
for parity in (0,1):create_batch('person',parity)
for di in range(4):
 for parity in (0,1):create_batch('digit',parity,di)
# Restore opaque foreground above every number and subject before adding title placards.
t=call('get_timeline',{});track={v['id']:tr['trackId'] for tr in t['tracks'] for v in tr['clips']};call('manage_tracks',{'reorder':[{'trackId':track[first['fg']],'to':0},{'trackId':track[first['name']],'to':0},{'trackId':track[first['note']],'to':0}]})
for parity in (0,1):create_batch('name',parity)
s,e=span(7);note=add([{'mediaRef':refs['note_marilyn'],'startFrame':s,'endFrame':e}])[0]['id'];ids['marilyn_note']=note;key(note,'scale',[[0,.70,.222]]);motion(note,7,.15,.005)
# Moving grain has a continuous track, cut only at its 8s loop boundaries.
g=add([{'mediaRef':refs['grain'],'startFrame':s,'endFrame':min(s+240,912),'includeAudio':False} for s in (0,240,480,720)]);ids['grain']=[x['id'] for x in g];call('set_clip_properties',{'clipIds':ids['grain'],'opacity':.4})
(out/'remaining_ids.json').write_text(json.dumps(ids,indent=2)+'\n')
for frame in [60,114,175,289,403,517,631,745,859,911]:call('inspect_timeline',{'startFrame':frame})
print('DONE',len(ids),flush=True)
