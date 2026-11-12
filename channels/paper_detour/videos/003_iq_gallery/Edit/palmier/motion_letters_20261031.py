"""Apply approved micro-motion to existing IQ Gallery layers via Palmier MCP.
Run only after atomically acquiring this agent's documented shared lock.
"""
import sys,json,pathlib,base64
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';lock=root/'channels/paper_detour/.rarovista-timeline-lock/owner.md';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
assert lock.exists() and '/root/motion_editor' in lock.read_text(),'shared lock not ours'
c=PalmierConnection();c.connect();journal=out/'receipt_text_motion_20261031.jsonl'
def call(name,args):
 assert lock.exists() and '/root/motion_editor' in lock.read_text(),'shared lock lost'
 r=c.request('tools/call',{'name':name,'arguments':args})
 if r.get('isError'):raise RuntimeError((name,r))
 texts=[x['text'] for x in r.get('content',[]) if x.get('type')=='text']
 try:o=json.loads(texts[0]) if len(texts)==1 else {'texts':texts}
 except ValueError:o={'texts':texts}
 if name=='inspect_timeline':
  for j,v in enumerate(r.get('content',[])):
   if v.get('type')=='image':(out/f'text_motion_f{args["startFrame"]}_{j}.png').write_bytes(base64.b64decode(v['data']))
 with journal.open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':o},ensure_ascii=False)+'\n')
 (out/'session_text_motion_20261031.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n')
 return o
project=call('manage_project',{'action':'list'});(out/'text_motion_projects_before.json').write_text(json.dumps(project,ensure_ascii=False,indent=2)+'\n')
# The owner has separately inspected visible UI and confirmed it is safely saved.
project=call('manage_project',{'action':'open','path':'/Users/diplomat/Documents/Palmier Pro/Paper Detour 003 IQ Gallery 20261031.palmier'})
t=call('get_timeline',{});assert t['id']=='19F2B39F' and t['totalFrames']==1800,t
(out/'text_motion_preedit.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
ids=json.loads((out/'built_60s_ids.json').read_text()); clips={v['id']:v for tr in t['tracks'] for v in tr['clips']};expected=[ids[f'name_{i}'] for i in range(13)]+[ids[f'glyph_{i}_{j}'] for i in range(13) for j in range(4)];assert all(i in clips for i in expected)
# Check unchanged audio tracks and actual clip count before mutations.
assert sum(len(tr['clips']) for tr in t['tracks'])==90
scores=['119','123','125','133','139','148','150','150','152','154','155','160','228']
def key(cid,prop,rows):call('set_keyframes',{'clipId':cid,'property':prop,'keyframes':rows})
def merge(old,new):
 data={int(row[0]):row for row in old};data.update({int(row[0]):row for row in new});return [data[x] for x in sorted(data)]
def animate(cid,i,is_name,j=0):
 clip=clips[cid];pos=clip['keyframes']['position'];scale=clip['keyframes']['scale'];assert len(scale)==1
 w,h=scale[0][1:3];off=0 if i==0 else 21; start=off if is_name else off+43;end=off+115;duration=clip['frames'][1]-clip['frames'][0]
 base=next((v for v in pos if v[0]==start),None)
 if base is None:
  # Name's settled position occurs at 0 for the first scene or frame 20 during preroll.
  candidates=[v for v in pos if v[0]<=start];base=max(candidates,key=lambda v:v[0]);assert is_name
 x,y=base[1:3];anchor=(x+w/2,y+h/2) if is_name else (.5,.55)
 if is_name:
  # Names begin breathing on arrival, so the word is alive while IQ rises.
  times=[start,start+22,start+44,start+66,start+88,end]
  ks=[1,1.04,.99,1.04,.99,1];angles=[0,1,-1,1,-1,0]
 else:
  times=[start,start+18,start+36,start+54,end]
  ks=[1,1.04,.99,1.04,1];angles=[0,1,-1,1,0]
 sign=-1 if (i+j)%2 else 1
 positions=[];scales=[[0,w,h,'smooth']];rots=[[0,0,'smooth']]
 for f,k,a in zip(times,ks,angles):
  assert f<duration,(cid,f,duration)
  xx=anchor[0]+(x-anchor[0])*k; yy=anchor[1]+(y-anchor[1])*k
  positions.append([f,round(xx,6),round(yy,6),'smooth']);scales.append([f,round(w*k,6),round(h*k,6),'smooth']);rots.append([f,round(a*sign,3),'smooth'])
 # The last character remains on screen; continue the same restrained motion until the last frame.
 if i==12:
  f=duration-1;k=1.03;xx=anchor[0]+(x-anchor[0])*k;yy=anchor[1]+(y-anchor[1])*k
  positions.append([f,round(xx,6),round(yy,6),'smooth']);scales.append([f,round(w*k,6),round(h*k,6),'smooth']);rots.append([f,sign,'smooth'])
 else:
  scales.append([duration-1,w,h,'smooth']);rots.append([duration-1,0,'smooth'])
 key(cid,'position',merge(pos,positions));key(cid,'scale',merge([],scales));key(cid,'rotation',merge([],rots))
for i in range(13):
 animate(ids[f'name_{i}'],i,True)
 for j in range(4):animate(ids[f'glyph_{i}_{j}'],i,False,j)
 print('DONE_SCENE',i+1,flush=True)
t=call('get_timeline',{});assert t['id']=='19F2B39F' and t['totalFrames']==1800
(out/'text_motion_built_state.json').write_text(json.dumps(t,ensure_ascii=False,indent=2)+'\n')
starts=[0,139,278,417,556,695,834,972,1110,1248,1386,1524,1662]
for i,s in enumerate(starts):
 for f in [s,s+15,s+30,s+43,s+61,s+79,s+97,s+115,min(s+137,1799)]:call('inspect_timeline',{'startFrame':f})
print('BUILT_AND_INSPECTED',flush=True)
