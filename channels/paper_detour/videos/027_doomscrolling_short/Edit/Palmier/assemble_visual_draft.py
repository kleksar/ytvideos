#!/usr/bin/env python3
"""One-shot silent rough assembly via Palmier MCP; no exports or sound."""
import sys,json,os,hashlib,base64
from pathlib import Path
R=Path('/Users/diplomat/ytvideos'); E=R/'channels/paper_detour/videos/027_doomscrolling_short'; OUT=E/'Edit/Palmier'; LOCK=R/'channels/paper_detour/.rarovista-timeline-lock/owner.md'; NAME='Paper Detour 027 Doomscrolling 20261031'
sys.path.insert(0,str(R/'automation/palmier'))
from inspect_connection import PalmierConnection
receipt_path=OUT/'assembly_receipt.json'
if receipt_path.exists(): raise RuntimeError('Receipt exists: inspect instead of retrying')
owner=LOCK.read_text(); assert '`/root/paper_editor`' in owner
p=E/'Source/Images'
scenes=[
(0,158,['scene01/background_v01.png','scene01/character_v02.png','scene01/foreground_v01.png']),
(158,249,['scene02/background_v01.png','scene02/phone_v01.png','scene02/foreground_leaves_v01.png']),
(249,379,['scene03/background_no_person_v02.png','scene03/press_no_person_cutout_v02.png','scene03/foreground_no_person_v02.png']),
(379,542,['scene04/background_v01.png','scene04/reader_table_v01.png','scene04/foreground_v01.png']),
(542,747,['scene05/background_v04.png','scene05/contact_group_v01.png','scene05/foreground_v01.png']),
(747,1011,['scene06/background_v01.png','scene06/contact_group_v01.png','scene06/foreground_v01.png']),
(1011,1132,['scene07/background_clean_v01.png','scene07/subject_desk_group_v01.png','scene07/foreground_plant_v01.png'])]
grain=R/'channels/paper_detour/videos/001_radio_game/Source/Graphics/film_grain_8s_prores4444.mov'
paths=[p/f for _,_,fs in scenes for f in fs]+[grain]
for f in paths:
 if not f.is_file(): raise RuntimeError(f'Missing {f}')
receipt={'status':'started','project_name':NAME,'steps':[],'input_paths':[str(f) for f in paths], 'warning':'draft only; 1132 frames provisional and no soundtrack or accent words; scene 06 to 07 lighting transition unresolved'}
def save():
 tmp=receipt_path.with_suffix('.tmp'); tmp.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n'); tmp.replace(receipt_path)
def call(c,name,args):
 x=c.request('tools/call',{'name':name,'arguments':args})
 if x.get('isError'):raise RuntimeError(f'{name}: {x.get("content")}')
 b=[t['text'] for t in x.get('content',[]) if t.get('type')=='text']
 if len(b)!=1:raise RuntimeError(f'{name}: non-text response')
 return json.loads(b[0])
def step(name,fn):
 receipt['pending']=name;save();result=fn();receipt['steps'].append({'action':name,'result':result});receipt.pop('pending');save();return result
save()
c=PalmierConnection();c.connect();o=PalmierConnection();o.connect()
try:
 prior=call(c,'manage_project',{'action':'list'}); initial=call(c,'get_timeline',{}); exports=call(c,'manage_exports',{'action':'list'}).get('exports')
 if not prior.get('active') or not prior.get('visible') or not isinstance(exports,list):raise RuntimeError('Cannot establish prior project/export state')
 if any(e.get('status') not in ('completed','failed','cancelled','canceled') for e in exports):raise RuntimeError('An export is active')
 if any(x.get('name')==NAME for x in prior.get('projects',[])):raise RuntimeError('Project already exists; inspect manually')
 receipt.update(prior_visible=prior['visible'],prior_timeline=initial.get('id'));save()
 created=step('create_project',lambda:call(c,'manage_project',{'action':'create','name':NAME,'aspectRatio':'9:16','fps':30,'quality':'1080p'}))
 own=call(c,'manage_project',{'action':'list'});tl=call(c,'get_timeline',{}); obs=call(o,'manage_project',{'action':'list'});otl=call(o,'get_timeline',{})
 if obs.get('visible')!=prior.get('visible') or otl.get('id')!=initial.get('id'):raise RuntimeError('Other visible state changed: stop')
 if own.get('active',{}).get('name')!=NAME:raise RuntimeError('Target not confirmed')
 if (tl.get('width'),tl.get('height'),tl.get('fps'))!=(1080,1920,30) or tl.get('totalFrames'):raise RuntimeError('Unexpected target timeline geometry')
 project=own['active']['path'];tid=tl['id'];receipt.update(project_path=project,timeline_id=tid,isolation_confirmed=True);save()
 def guard():
  if LOCK.read_text()!=owner:raise RuntimeError('Lost shared lock')
  now=call(c,'manage_project',{'action':'list'}); t=call(c,'get_timeline',{}); vv=call(o,'manage_project',{'action':'list'}); vt=call(o,'get_timeline',{})
  if now.get('active',{}).get('path')!=project or t.get('id')!=tid:raise RuntimeError('Wrong session target')
  if vv.get('visible')!=prior.get('visible') or vt.get('id')!=initial.get('id'):raise RuntimeError('Other visible state changed')
  return t
 refs={}
 for f in paths:
  guard(); z=step('import '+str(f),lambda f=f:call(c,'import_media',{'source':{'path':str(f)},'folder':'Paper027'}));ref=z['mediaRef']; z2=call(c,'get_media',{'ids':[ref]})['assets'];
  if len(z2)!=1 or z2[0].get('generationStatus'):raise RuntimeError('Asset not ready')
  refs[str(f)]=ref
  receipt.setdefault('refs',{})[str(f)]=ref;save()
 clips_by_layer=[]
 for layer in range(3):
  guard();entries=[{'mediaRef':refs[str(p/fs[layer])],'startFrame':start,'endFrame':end,'includeAudio':False} for start,end,fs in scenes]
  added=step('add layer '+str(layer),lambda entries=entries:call(c,'add_clips',{'entries':entries}))['clips']
  if len(added)!=7:raise RuntimeError('Unexpected count')
  clips_by_layer.append(added)
 # Put 03 and 07 contact groups at the statically inspected placement.
 for idx,tr in [(2,{'centerX':(192+339)/941,'centerY':(314+602)/1672,'width':678/941,'height':1204/1672}),(6,{'centerX':(100+423.5)/941,'centerY':(110+752.5)/1672,'width':847/941,'height':1505/1672})]:
  guard();cid=clips_by_layer[1][idx]['id'];step('set static contact transform '+cid,lambda cid=cid,tr=tr:call(c,'set_clip_properties',{'clipIds':[cid],'transform':tr}))
 # BG and foreground independent subtle motion; contact groups remain attached to their local scene supports.
 for layer in [0,2]:
  for i,(start,end,fs) in enumerate(scenes):
   cid=clips_by_layer[layer][i]['id'];span=end-start;d=.006 if layer==0 else -.007
   guard();step('scale '+cid,lambda cid=cid,span=span:call(c,'set_keyframes',{'clipId':cid,'property':'scale','keyframes':[[0,1.04,1.04],[span-1,1.04,1.04]]}))
   guard();step('position '+cid,lambda cid=cid,span=span,d=d:call(c,'set_keyframes',{'clipId':cid,'property':'position','keyframes':[[0,-.02,-.02],[span-1,-.02+d,-.02]]}))
 # One existing transparent grain clip is repeated; no linked audio.
 guard();entries=[{'mediaRef':refs[str(grain)],'startFrame':x,'endFrame':min(x+240,1132),'includeAudio':False} for x in range(0,1132,240)]
 g=step('add grain',lambda:call(c,'add_clips',{'entries':entries}))['clips'];ids=[x['id'] for x in g]
 guard();step('configure grain',lambda:call(c,'set_clip_properties',{'clipIds':ids,'opacity':.5,'transform':{'width':1.778,'height':.563,'rotation':90}}))
 final=guard();receipt['timeline']=final;receipt['status']='visual_rough_no_audio_no_words';save()
 # save composited samples without exposing foreign project; grid is inspector overlay.
 for f in [0,78,157,158,203,248,249,314,378,379,460,541,542,640,746,747,875,1010,1011,1070,1131]:
  guard();x=c.request('tools/call',{'name':'inspect_timeline','arguments':{'startFrame':f}})
  if x.get('isError'):raise RuntimeError('Frame inspect failed')
  imgs=[q for q in x.get('content',[]) if q.get('type')=='image']
  if len(imgs)!=1:raise RuntimeError(f'Frame inspect unexpected: {f}')
  (OUT/f'frame_{f:04d}.png').write_bytes(base64.b64decode(imgs[0]['data']))
 receipt['inspected_frames']=[0,78,157,158,203,248,249,314,378,379,460,541,542,640,746,747,875,1010,1011,1070,1131];save()
 guard();step('close_own_project',lambda:call(c,'manage_project',{'action':'close','path':project}))
 if call(o,'manage_project',{'action':'list'}).get('visible')!=prior.get('visible'):raise RuntimeError('Other visible state changed after close')
 receipt['status']='visual_rough_saved_no_audio_no_words';save();print(json.dumps({'status':receipt['status'],'project':project,'timeline':tid,'receipt':str(receipt_path)},ensure_ascii=False),flush=True)
except BaseException as e:
 receipt['status']='stopped_inspect_before_retry';receipt['error']=repr(e);save();raise
