#!/usr/bin/env python3
import sys,json,base64
from pathlib import Path
R=Path('/Users/diplomat/ytvideos'); E=R/'channels/paper_detour/videos/027_doomscrolling_short';O=E/'Edit/Palmier';L=R/'channels/paper_detour/.rarovista-timeline-lock/owner.md';P='/Users/diplomat/Documents/Palmier Pro/Paper Detour 027 Doomscrolling 20261031.palmier';T='41B11E0F'
sys.path.insert(0,str(R/'automation/palmier'));from inspect_connection import PalmierConnection
out=O/'accent_trial_receipt.json'
if out.exists():raise RuntimeError('Existing receipt; inspect, never retry')
owner=L.read_text();assert '`/root/paper_editor`' in owner
c=PalmierConnection();c.connect();o=PalmierConnection();o.connect();result={'status':'started','steps':[]};
def save():out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
def call(c,n,a):
 x=c.request('tools/call',{'name':n,'arguments':a})
 if x.get('isError'):raise RuntimeError(f'{n}: {x.get("content")}')
 return json.loads(next(b['text'] for b in x['content'] if b['type']=='text'))
def guard():
 if L.read_text()!=owner:raise RuntimeError('Lost lock')
 a=call(c,'manage_project',{'action':'list'});t=call(c,'get_timeline',{});b=call(o,'manage_project',{'action':'list'});v=call(o,'get_timeline',{})
 if a.get('active',{}).get('path')!=P or b.get('visible',{}).get('path')!=P or t.get('id')!=T or v.get('id')!=T:raise RuntimeError('target changed')
 return t
def step(n,f):
 guard();result['pending']=n;save();x=f();result['steps'].append({'action':n,'result':x});result.pop('pending');save();return x
save()
try:
 t=guard(); assert t['totalFrames']==1132
 specs=[('1_MINUTE_v01.png',38,72,.52,.10,[.27,.46],[.24,.24]),('20_MINUTES_v02.png',72,118,.54,.10,[.27,.46],[.24,.24]),('1710_v01.png',251,294,.32,.08,[.46,.40],[.46,.23]),('SATIRE_v01.png',501,541,.42,.09,[.45,.48],[.49,.21])]
 entries=[]
 for file,a,b,w,h,s,e in specs:
  p=E/'Source/Typography'/file; z=step('import '+file,lambda p=p:call(c,'import_media',{'source':{'path':str(p)},'folder':'Paper027/Accents'})); ref=z['mediaRef']; assets=call(c,'get_media',{'ids':[ref]})['assets'];assert len(assets)==1 and not assets[0].get('generationStatus');entries.append({'mediaRef':ref,'startFrame':a,'endFrame':b})
 added=step('add accents',lambda:call(c,'add_clips',{'entries':entries}))['clips']; assert len(added)==len(specs)
 t=guard();tracks=t['tracks'];track=next(x for x in tracks if any(y['id']==added[0]['id'] for y in x['clips']));
 step('place accents behind figure/objects',lambda:call(c,'manage_tracks',{'reorder':[{'trackId':track['trackId'],'to':3}]}))
 for clip,(_,a,b,w,h,s,e) in zip(added,specs):
  cid=clip['id']; dur=b-a; intro=10
  step('accent scale '+cid,lambda cid=cid,w=w,h=h,dur=dur:call(c,'set_keyframes',{'clipId':cid,'property':'scale','keyframes':[[0,w,h],[dur-1,w,h]]}))
  step('accent position '+cid,lambda cid=cid,s=s,e=e,dur=dur,intro=intro:call(c,'set_keyframes',{'clipId':cid,'property':'position','keyframes':[[0,*s],[intro,*e],[dur-1,*e]]}))
  step('accent opacity '+cid,lambda cid=cid,dur=dur:call(c,'set_keyframes',{'clipId':cid,'property':'opacity','keyframes':[[0,0],[5,1],[dur-5,1],[dur-1,0]]}))
 result['timeline']=guard()
 for f in [38,40,43,47,51,65,72,76,82,88,108,251,254,257,261,270,290,501,505,510,514,525,540]:
  guard();x=c.request('tools/call',{'name':'inspect_timeline','arguments':{'startFrame':f}}); imgs=[q for q in x.get('content',[]) if q.get('type')=='image']
  if x.get('isError') or len(imgs)!=1:raise RuntimeError('Bad inspection '+str(f))
  (O/f'accent_{f:04d}.png').write_bytes(base64.b64decode(imgs[0]['data']))
 result['inspected_frames']=[38,40,43,47,51,65,72,76,82,88,108,251,254,257,261,270,290,501,505,510,514,525,540];result['status']='trial_added_not_yet_reviewed_or_saved';save();print('done')
except BaseException as e:
 result['status']='stopped_inspect_before_retry';result['error']=repr(e);save();raise
