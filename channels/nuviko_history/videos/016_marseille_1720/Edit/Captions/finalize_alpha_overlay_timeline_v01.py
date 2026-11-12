#!/usr/bin/env python3
"""Replace the five-second alpha preview with the full word-highlight layer."""
from pathlib import Path
import hashlib,json,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from stories.automation.palmier.inspect_connection import PalmierConnection

EP=Path(__file__).resolve().parents[2];PROJECT='3C0B4689';TIMELINE='6A17B61A'
MOV=EP/'Assets/Generated/subtitle_overlay_v01.mov';OVR=EP/'Edit/Captions/subtitle_overlay_video_v01.json'
OUT=EP/'Edit/Captions/final_alpha_overlay_timeline_v01.json';PENDING=EP/'Edit/Captions/final_alpha_overlay_timeline_v01.pending.json'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def parse(r,n):
 if r.get('isError'):raise RuntimeError(f'{n} failed; pending receipt remains')
 xs=[x.get('text','') for x in r.get('content',[]) if x.get('type')=='text']
 if len(xs)!=1:raise RuntimeError(f'{n} returned ambiguous response')
 return json.loads(xs[0])
if PENDING.exists():raise SystemExit('Unreconciled pending operation exists')
receipt=json.loads(OVR.read_text())
if receipt.get('status')!='rendered_alpha_layer' or receipt.get('videoSha256')!=sha(MOV):raise SystemExit('Overlay video identity changed')
c=PalmierConnection();c.connect()
def read(n,a):return parse(c.request('tools/call',{'name':n,'arguments':a}),n)
state=json.loads(OUT.read_text()) if OUT.exists() else {'status':'started','projectId':PROJECT,'timelineId':TIMELINE,'videoSha256':sha(MOV)}
def save():
 t=OUT.with_suffix('.tmp');t.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');t.replace(OUT)
def mutate(n,a,op):
 if PENDING.exists():raise RuntimeError('Pending operation exists')
 PENDING.write_text(json.dumps({'tool':n,'arguments':a,'operation':op,'time':time.time()},indent=2)+'\n')
 result=parse(c.request('tools/call',{'name':n,'arguments':a}),n)
 state.setdefault('operations',[]).append({'tool':n,'operation':op,'arguments':a,'result':result})
 save();PENDING.unlink();return result
if state.get('projectId')!=PROJECT or state.get('timelineId')!=TIMELINE or state.get('videoSha256')!=sha(MOV):raise SystemExit('Timeline receipt identity mismatch')
args={'projectId':PROJECT,'timelineId':TIMELINE};timeline=read('get_timeline',args)
if (timeline.get('fps'),timeline.get('width'),timeline.get('height'),timeline.get('totalFrames'))!=(30,1920,1080,16125):raise SystemExit('Final overlay target settings changed')
scenes=[t for t in timeline['tracks'] if t.get('name',t.get('label'))=='Scenes']
voices=[t for t in timeline['tracks'] if t.get('name',t.get('label'))=='Narration']
subs=[t for t in timeline['tracks'] if t.get('name',t.get('label'))=='Subtitles']
if len(scenes)!=1 or len(scenes[0].get('clips',[]))!=127 or len(voices)!=1 or len(voices[0].get('clips',[]))!=1 or len(subs)!=1:raise SystemExit('Unexpected tracks on final overlay timeline')
if not state.get('beforeReplaceSnapshot'):
 state['beforeReplaceSnapshot']=mutate('manage_snapshots',{**args,'action':'save','name':'Before full subtitle overlay replacement'},'snapshot 5-second alpha preview before full replacement');save()
assets=read('get_media',{'projectId':PROJECT}).get('assets',[])
asset=next((a for a in assets if a.get('name')=='subtitle_overlay_v01' and a.get('type')=='video'),None)
if not asset:
 imported=mutate('import_media',{'projectId':PROJECT,'source':{'path':str(MOV)},'folder':'SubtitleOverlay','name':'subtitle_overlay_v01'},'import full alpha subtitle layer')
 asset_id=imported.get('mediaRef')
else:asset_id=asset['id']
asset=next((a for a in read('get_media',{'projectId':PROJECT,'ids':[asset_id]}).get('assets',[]) if a.get('id')==asset_id),None)
if not asset or asset.get('type')!='video' or asset.get('generationStatus'):raise SystemExit('Full alpha subtitle layer is not ready')
subs=next(t for t in timeline['tracks'] if t.get('name',t.get('label'))=='Subtitles')
matching=[cl for cl in subs.get('clips',[]) if cl.get('mediaRef')==asset_id]
if not matching:
 mutate('add_clips',{**args,'entries':[{'mediaRef':asset_id,'startFrame':0,'source':[0,537.5],
                                       'trackIndex':subs['index'],'includeAudio':False}]},'replace preview with full alpha subtitle movie')
timeline=read('get_timeline',args)
subs=next(t for t in timeline['tracks'] if t.get('name',t.get('label'))=='Subtitles')
clips=[cl for cl in subs.get('clips',[]) if cl.get('mediaRef')==asset_id]
if len(clips)!=1 or clips[0]['frames']!=[0,16125] or clips[0].get('mediaType','video')!='video':raise RuntimeError(f'Full overlay clip readback mismatch: {[cl.get("frames") for cl in clips]}')
scenes=next(t for t in timeline['tracks'] if t.get('name',t.get('label'))=='Scenes')
voices=next(t for t in timeline['tracks'] if t.get('name',t.get('label'))=='Narration')
if len(scenes['clips'])!=127 or len(voices['clips'])!=1 or [t.get('name',t.get('label')) for t in timeline['tracks']]!=['Subtitles','Scenes','Narration']:
 raise RuntimeError('Final overlay timeline track order/content mismatch')
snapshot=mutate('manage_snapshots',{**args,'action':'save','name':'Full alpha word-highlight subtitles v01'},'snapshot full subtitle overlay timeline')
state.update({'status':'final_alpha_overlay_ready','mediaRef':asset_id,'clipId':clips[0]['id'],
              'snapshot':snapshot,'timelineSummary':{'fps':timeline['fps'],'width':timeline['width'],'height':timeline['height'],
              'totalFrames':timeline['totalFrames'],'durationSeconds':timeline['durationSeconds'],
              'tracks':[(t.get('name',t.get('label')),t['type'],len(t.get('clips',[]))) for t in timeline['tracks']]}})
save();print(json.dumps({'status':state['status'],'projectId':PROJECT,'timelineId':TIMELINE,'subtitleClip':clips[0]['id'],
                         'snapshot':snapshot,'summary':state['timelineSummary']},ensure_ascii=False))
