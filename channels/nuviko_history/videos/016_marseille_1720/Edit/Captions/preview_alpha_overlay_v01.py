#!/usr/bin/env python3
"""Check the subtitle alpha-video path on a disposable timeline clone."""
from pathlib import Path
import base64, hashlib, json, os, sys, time
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from stories.automation.palmier.inspect_connection import PalmierConnection

EP=Path(__file__).resolve().parents[2]
PROJECT="3C0B4689"; SOURCE="E9ACC2D3"
PREVIEW=EP/"Work/preexport_composite_samples_v01/overlay_test_5s/overlay_test.mov"
OUT=EP/"Edit/Captions/alpha_overlay_preview_v01.json"
PENDING=EP/"Edit/Captions/alpha_overlay_preview_v01.pending.json"

def parse(r,n):
    if r.get('isError'): raise RuntimeError(f'{n} failed; preserve pending operation')
    texts=[x.get('text','') for x in r.get('content',[]) if x.get('type')=='text']
    if len(texts)!=1: raise RuntimeError(f'{n} returned ambiguous response')
    return json.loads(texts[0])

if PENDING.exists(): raise SystemExit('Unreconciled pending preview operation exists')
c=PalmierConnection();c.connect()
def read(n,a): return parse(c.request('tools/call',{'name':n,'arguments':a}),n)
state=json.loads(OUT.read_text()) if OUT.exists() else {'status':'started','projectId':PROJECT,'sourceTimelineId':SOURCE}
def save():
    tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n');tmp.replace(OUT)
def mutate(n,a,op):
    PENDING.write_text(json.dumps({'tool':n,'arguments':a,'operation':op,'time':time.time()},indent=2)+'\n')
    result=parse(c.request('tools/call',{'name':n,'arguments':a}),n)
    state.setdefault('operations',[]).append({'tool':n,'operation':op,'arguments':a,'result':result})
    save();PENDING.unlink();return result

if state.get('projectId')!=PROJECT or state.get('sourceTimelineId')!=SOURCE: raise SystemExit('Receipt identity mismatch')
if not state.get('timelineId'):
    prior_clone=next((x for x in state.get('operations',[]) if x.get('tool')=='create_timeline' and
                      x.get('result',{}).get('timelineId')),None)
    if prior_clone:
        state['timelineId']=prior_clone['result']['timelineId'];save()
if not state.get('timelineId'):
    created=mutate('create_timeline',{'projectId':PROJECT,'from':SOURCE,'name':'Marseille Alpha Overlay Preview v01'},'clone subtitle timeline for alpha preview')
    state['timelineId']=created['timelineId'];save()
tid=state['timelineId'];args={'projectId':PROJECT,'timelineId':tid}
timeline=read('get_timeline',args)
if (timeline.get('fps'),timeline.get('width'),timeline.get('height'),timeline.get('totalFrames'))!=(30,1920,1080,16125): raise SystemExit('Preview clone settings differ')
subtitle_tracks=[t for t in timeline['tracks'] if t.get('name',t.get('label'))=='Subtitles']
if subtitle_tracks:
    snap=mutate('manage_snapshots',{**args,'action':'save','name':'Before optimized subtitle overlay'},'snapshot alpha-preview clone before track replacement')
    state['beforeReplaceSnapshot']=snap;save()
    remove=mutate('manage_tracks',{**args,'remove':[{'trackId':subtitle_tracks[0]['trackId']}]},'remove word-state images from preview clone')
    timeline=read('get_timeline',args)

assets=read('get_media',{'projectId':PROJECT}).get('assets',[])
asset=next((a for a in assets if a.get('name')=='overlay_test' and a.get('type')=='video'),None)
if not asset:
    result=mutate('import_media',{'projectId':PROJECT,'source':{'path':str(PREVIEW)},'folder':'SubtitleOverlayPreview','name':'overlay_test'},'import 5-second transparent subtitle preview')
    asset_id=result.get('mediaRef')
else: asset_id=asset['id']
asset=next((a for a in read('get_media',{'projectId':PROJECT,'ids':[asset_id]}).get('assets',[]) if a.get('id')==asset_id),None)
if not asset or asset.get('type')!='video' or asset.get('generationStatus'): raise SystemExit('Alpha preview media is not ready')

timeline=read('get_timeline',args)
existing=[c for t in timeline['tracks'] for c in t.get('clips',[]) if c.get('mediaRef')==asset_id]
if not existing:
    result=mutate('add_clips',{**args,'entries':[{'mediaRef':asset_id,'startFrame':0,'source':[0,5.0]}]},'place 5-second alpha subtitle overlay preview')
timeline=read('get_timeline',args)
tracks=[t for t in timeline['tracks'] if t.get('type')=='video' and t.get('name',t.get('label')) not in ('Scenes',) and
        any(cl.get('mediaRef')==asset_id for cl in t.get('clips',[]))]
if len(tracks)!=1: raise RuntimeError('Could not uniquely identify alpha overlay preview track')
track=tracks[0]; clips=[cl for cl in track.get('clips',[]) if cl.get('mediaRef')==asset_id]
if len(clips)!=1 or clips[0]['frames']!=[0,150]: raise RuntimeError(f'Preview clip interval differs: {[cl.get("frames") for cl in clips]}')
if track.get('name',track.get('label'))!='Subtitles':
    mutate('manage_tracks',{**args,'set':[{'trackId':track['trackId'],'name':'Subtitles'}]},'name alpha overlay track Subtitles')
timeline=read('get_timeline',args)
state.update({'status':'alpha_preview_ready','timelineId':tid,'mediaRef':asset_id,'clipId':clips[0]['id'],
              'timelineSummary':{'fps':timeline['fps'],'width':timeline['width'],'height':timeline['height'],
                                 'totalFrames':timeline['totalFrames'],
                                 'tracks':[(t.get('name',t.get('label')),t['type'],len(t.get('clips',[]))) for t in timeline['tracks']]}})
save()
print(json.dumps({'status':state['status'],'timelineId':tid,'mediaRef':asset_id,'clipId':clips[0]['id'],'summary':state['timelineSummary']},ensure_ascii=False))
