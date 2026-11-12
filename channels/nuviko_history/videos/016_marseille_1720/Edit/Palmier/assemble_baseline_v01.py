#!/usr/bin/env python3
"""Assemble the authorized source-still + original-audio Nuviko baseline via explicit Palmier IDs."""
from pathlib import Path
import hashlib,json,time,os,sys,re
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from stories.automation.palmier.inspect_connection import PalmierConnection

EP=Path('channels/nuviko_history/videos/016_marseille_1720').resolve()
PROJECT='3C0B4689'; TIMELINE='66471479'
PROJECT_PATH=Path('/Users/diplomat/Documents/Palmier Pro/Nuviko 016 Marseille 1720.palmier').resolve()
MANIFEST=EP/'Edit/ImageMotion/source_manifest_v01.json'
SHOT=EP/'Storyboard/SHOT_MAP_v01.json'
VOICE=EP/'Source/Audio/original_narration.m4a'
OUT=EP/'Edit/Palmier'; RECEIPT=OUT/'baseline_assembly_v01.json'
PENDING=OUT/'baseline_assembly_v01.pending.json'


def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

def parse_result(r,name):
 if r.get('isError'): raise RuntimeError(f'{name} returned isError; pending write-ahead receipt remains')
 texts=[x.get('text','') for x in r.get('content',[]) if x.get('type')=='text']
 if len(texts)!=1: raise RuntimeError(f'{name} returned ambiguous result; pending receipt remains')
 try: return json.loads(texts[0])
 except Exception as e: raise RuntimeError(f'{name} returned non-JSON result; pending receipt remains') from e

if PENDING.exists(): raise SystemExit('Pending operation exists; reconcile before any retry')
manifest=json.loads(MANIFEST.read_text()); shot=json.loads(SHOT.read_text())
scenes=shot['scenes']; rows=manifest['scenes'];
if len(scenes)!=127 or len(rows)!=len(scenes): raise SystemExit('Expected exact 127-scene handoff')
if shot['total_frames']!=16125 or shot['fps']!=30: raise SystemExit('Unexpected source timing contract')
for s,r in zip(scenes,rows):
 if s['id']!=r['id'] or s['start_frame']!=r['startFrame'] or s['end_frame_exclusive']!=r['endFrame']: raise SystemExit('Shot map/manifest mismatch')
 if s['end_frame_exclusive']-s['start_frame'] not in range(120,181): raise SystemExit(f'4–6 second rule failed at {s["id"]}')
 if sha(r['image'])!=r['image_sha256']: raise SystemExit(f'Image changed: {s["id"]}')
if sha(VOICE)!='eb3e1b9ccd6c9c89577bbe4201914ff142e55f41220ff1e7c1cde50cd3a6a419': raise SystemExit('Original narration identity changed')

c=PalmierConnection(); c.connect()
project_list=c.read_tool('manage_project',{'action':'list'})
projects=project_list.get('projects',[])
project=next((p for p in projects if p.get('id')==PROJECT),None)
if not project or Path(project.get('path','')).resolve()!=PROJECT_PATH: raise SystemExit('Project ID/path mismatch')
before=c.read_tool('get_timeline',{'projectId':PROJECT,'timelineId':TIMELINE})
if RECEIPT.exists():
 state=json.loads(RECEIPT.read_text())
 identity=(state.get('projectId'),state.get('timelineId'),state.get('sourceManifestSha256'),state.get('shotMapSha256'),state.get('sourceAudioSha256'))
 if identity!=(PROJECT,TIMELINE,sha(MANIFEST),sha(SHOT),sha(VOICE)) or state.get('status')!='started': raise SystemExit('Existing receipt is not a resumable started run')
else:
 if (before.get('fps'),before.get('width'),before.get('height'),before.get('totalFrames'))!=(30,1920,1080,0) or before.get('tracks'):
  raise SystemExit('Baseline timeline is not the expected empty 1920x1080/30 target')
 media_before=c.read_tool('get_media',{'projectId':PROJECT})
 if media_before.get('assets'): raise SystemExit('New project already contains assets; inspect before assembly')
 state={'status':'started','projectId':PROJECT,'projectPath':str(PROJECT_PATH),'timelineId':TIMELINE,'timelineName':before['name'],
  'canvas':[1920,1080],'fps':30,'sourceAudio':str(VOICE),'sourceAudioSha256':sha(VOICE),'sourceManifestSha256':sha(MANIFEST),
  'shotMapSha256':sha(SHOT),'scenes':[],'mediaRefs':{},'steps':[]}

def save():
 tmp=RECEIPT.with_suffix('.tmp'); tmp.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n'); tmp.replace(RECEIPT)

def write_call(name,args,op):
 if PENDING.exists(): raise RuntimeError('Unreconciled pending operation exists')
 PENDING.write_text(json.dumps({'tool':name,'operation':op,'arguments':args,'time':time.time()},indent=2,ensure_ascii=False)+'\n')
 response=c.request('tools/call',{'name':name,'arguments':args})
 result=parse_result(response,name)
 state['steps'].append({'tool':name,'operation':op,'arguments':args,'result':result,'time':time.time()})
 save(); PENDING.unlink()
 return result

def read_api(name,args):
 return parse_result(c.request('tools/call',{'name':name,'arguments':args}),name)

# Persist pre-state before the first media-library mutation.
save()
# Reconcile successful media imports from receipts before resuming after interruption.
for step in state['steps']:
 if step.get('tool')!='import_media': continue
 ref=step.get('result',{}).get('mediaRef'); path=step.get('arguments',{}).get('source',{}).get('path')
 if not ref or not path: raise SystemExit('Malformed import receipt; reconcile manually')
 asset_list=read_api('get_media',{'projectId':PROJECT,'ids':[ref]}).get('assets',[])
 if len(asset_list)!=1 or asset_list[0].get('generationStatus'): raise SystemExit(f'Imported media not ready: {ref}')
 if Path(path)==VOICE.resolve():
  if asset_list[0].get('type')!='audio': raise SystemExit('Narration import type mismatch')
  state['voiceMediaRef']=ref
 else:
  found=next((r for r in rows if Path(r['image']).resolve()==Path(path).resolve()),None)
  if not found or asset_list[0].get('type')!='image' or asset_list[0].get('name')!=found['id']: raise SystemExit('Imported scene asset cannot be matched to the source manifest')
  state['mediaRefs'][found['id']]={'mediaRef':ref,'path':found['image'],'sha256':found['image_sha256']}
save()
for idx,(s,row) in enumerate(zip(scenes,rows),1):
 if s['id'] in state['mediaRefs']:
  ref=state['mediaRefs'][s['id']]['mediaRef']; assets=read_api('get_media',{'projectId':PROJECT,'ids':[ref]}).get('assets',[])
  if len(assets)!=1 or assets[0].get('type')!='image' or assets[0].get('name')!=s['id']: raise SystemExit(f'Reconciled scene asset mismatch: {s["id"]}')
  continue
 if PENDING.exists(): raise RuntimeError('Unexpected pending operation')
 args={'projectId':PROJECT,'source':{'path':row['image']},'folder':'MarseilleScenes','name':s['id']}
 result=write_call('import_media',args,f'import {s["id"]}')
 ref=result.get('mediaRef')
 if not ref: raise RuntimeError(f'Import of {s["id"]} returned no mediaRef; inspect receipt/live library')
 assets=read_api('get_media',{'projectId':PROJECT,'ids':[ref]}).get('assets',[])
 if len(assets)!=1 or assets[0].get('generationStatus') or assets[0].get('type')!='image': raise RuntimeError(f'Imported asset not ready: {s["id"]}')
 state['mediaRefs'][s['id']]={'mediaRef':ref,'path':row['image'],'sha256':row['image_sha256']}; save()

voice_ref=state.get('voiceMediaRef')
if voice_ref:
 voice_assets=read_api('get_media',{'projectId':PROJECT,'ids':[voice_ref]}).get('assets',[])
 if len(voice_assets)!=1 or voice_assets[0].get('type')!='audio': raise RuntimeError('Reconciled narration asset mismatch')
else:
 voice_result=write_call('import_media',{'projectId':PROJECT,'source':{'path':str(VOICE),'mimeType':'audio/mp4'},'folder':'Narration','name':'Original narration'},'import original narration')
 voice_ref=voice_result.get('mediaRef')
 if not voice_ref: raise RuntimeError('Narration import returned no mediaRef; inspect state')
 voice_assets=read_api('get_media',{'projectId':PROJECT,'ids':[voice_ref]}).get('assets',[])
 if len(voice_assets)!=1 or voice_assets[0].get('generationStatus') or voice_assets[0].get('type')!='audio': raise RuntimeError('Narration asset not ready')
 state['voiceMediaRef']=voice_ref; save()

# Add the image timeline in eight-clip atomic batches; first call creates one video track.
added_by_interval={}
for step in state['steps']:
 if step.get('tool')!='add_clips' or not step.get('operation','').startswith('add scene clips'): continue
 entries=step.get('arguments',{}).get('entries',[]); created=step.get('result',{}).get('clips',[])
 if len(entries)!=len(created): raise SystemExit('Scene clip receipt has mismatched entry/result counts')
 for entry,cl in zip(entries,created):
  s=next((x for x in scenes if x['start_frame']==entry.get('startFrame') and x['end_frame_exclusive']==entry.get('endFrame')),None)
  if not s or entry.get('mediaRef')!=state['mediaRefs'][s['id']]['mediaRef']: raise SystemExit('Scene clip receipt cannot map to source manifest')
  added_by_interval[s['id']]=cl['id']
live=c.read_tool('get_timeline',{'projectId':PROJECT,'timelineId':TIMELINE})
live_clips=[cl for tr in live.get('tracks',[]) for cl in tr.get('clips',[]) if cl.get('mediaType') in ('image',None)]
for s in scenes:
 matches=[cl for cl in live_clips if cl.get('frames')==[s['start_frame'],s['end_frame_exclusive']] and cl.get('mediaRef')==state['mediaRefs'][s['id']]['mediaRef']]
 if s['id'] in added_by_interval and (len(matches)!=1 or matches[0]['id']!=added_by_interval[s['id']]): raise SystemExit('Receipt/live scene clip mismatch; reconcile manually')
 if s['id'] not in added_by_interval and matches: raise SystemExit('Unreceipted scene clip exists; reconcile manually')
if len(live_clips)!=len(added_by_interval): raise SystemExit('Unexpected or unreceipted image clips exist on timeline')
for start in range(0,len(scenes),8):
 subset=scenes[start:start+8]
 if all(s['id'] in added_by_interval for s in subset): continue
 if any(s['id'] in added_by_interval for s in subset): raise SystemExit('Partially applied scene batch; reconcile manually')
 entries=[]
 for i,s in enumerate(subset):
  e={'mediaRef':state['mediaRefs'][s['id']]['mediaRef'],'startFrame':s['start_frame'],'endFrame':s['end_frame_exclusive']}
  if start>0: e['trackIndex']=0
  entries.append(e)
 result=write_call('add_clips',{'projectId':PROJECT,'timelineId':TIMELINE,'entries':entries},f'add scene clips {start+1}-{start+len(subset)}')
 added=result.get('clips',[])
 if len(added)!=len(subset): raise RuntimeError('Unexpected add_clips count; inspect live timeline before retry')
 live=c.read_tool('get_timeline',{'projectId':PROJECT,'timelineId':TIMELINE})
 clips=[cl for tr in live.get('tracks',[]) for cl in tr.get('clips',[])]
 for s,created in zip(subset,added):
  match=[cl for cl in clips if cl.get('frames')==[s['start_frame'],s['end_frame_exclusive']]]
  expected=state['mediaRefs'][s['id']]['mediaRef']
  if len(match)!=1 or match[0].get('mediaRef')!=expected: raise RuntimeError(f'Clip readback mismatch {s["id"]}; reconcile before retry')
  added_by_interval[s['id']]=match[0]['id']
 state['scenes']=[{'id':s['id'],'startFrame':s['start_frame'],'endFrame':s['end_frame_exclusive'],'clipId':added_by_interval[s['id']],'mediaRef':state['mediaRefs'][s['id']]['mediaRef']} for s in scenes if s['id'] in added_by_interval]
 save()

# Add the untouched source narration as its own audio track.
prior_voice=next((s for s in state['steps'] if s.get('tool')=='add_clips' and s.get('operation')=='place original narration at frame zero'),None)
if prior_voice:
 voice_clips=prior_voice.get('result',{}).get('clips',[])
 if len(voice_clips)!=1: raise RuntimeError('Narration placement receipt malformed')
else:
 voice_add=write_call('add_clips',{'projectId':PROJECT,'timelineId':TIMELINE,'entries':[{'mediaRef':voice_ref,'startFrame':0}]},'place original narration at frame zero')
 voice_clips=voice_add.get('clips',[])
 if len(voice_clips)!=1: raise RuntimeError('Unexpected voice clip count; reconcile live timeline')
# Name tracks via stable IDs from the actual timeline.
live=c.read_tool('get_timeline',{'projectId':PROJECT,'timelineId':TIMELINE})
scene_tracks=[t for t in live.get('tracks',[]) if t.get('type')=='video']
audio_tracks=[t for t in live.get('tracks',[]) if t.get('type')=='audio']
if len(scene_tracks)!=1 or len(scene_tracks[0].get('clips',[]))!=127 or len(audio_tracks)!=1 or len(audio_tracks[0].get('clips',[]))!=1:
 raise RuntimeError('Timeline track/clip inventory differs from expected baseline')
scene_track_id=scene_tracks[0]['trackId']; audio_track_id=audio_tracks[0]['trackId']
rename_step=next((s for s in state['steps'] if s.get('tool')=='manage_tracks' and s.get('operation')=='name source tracks'),None)
if not rename_step:
 renamed=write_call('manage_tracks',{'projectId':PROJECT,'timelineId':TIMELINE,'set':[{'trackId':scene_track_id,'name':'Scenes'},{'trackId':audio_track_id,'name':'Narration'}]},'name source tracks')
final=c.read_tool('get_timeline',{'projectId':PROJECT,'timelineId':TIMELINE})
if (final.get('fps'),final.get('width'),final.get('height'),final.get('totalFrames'))!=(30,1920,1080,16125): raise RuntimeError('Final baseline settings/duration mismatch')
tracks={t.get('name',t.get('label')):t for t in final['tracks']}
if set(tracks)!={'Scenes','Narration'} or len(tracks['Scenes']['clips'])!=127 or len(tracks['Narration']['clips'])!=1: raise RuntimeError('Final named tracks differ')
voice=tracks['Narration']['clips'][0]
if voice['frames'][0]!=0 or abs(voice['frames'][1]-16125)>3 or voice.get('mediaRef')!=voice_ref: raise RuntimeError('Original narration placement differs by more than three frames')
state['scenes']=[{'id':s['id'],'startFrame':s['start_frame'],'endFrame':s['end_frame_exclusive'],'clipId':added_by_interval[s['id']],'mediaRef':state['mediaRefs'][s['id']]['mediaRef']} for s in scenes]
state.update({'status':'baseline_assembled','sceneTrackId':scene_track_id,'audioTrackId':audio_track_id,'voiceClipId':voice['id'],'totalFrames':final['totalFrames'],'durationSeconds':final['durationSeconds'],'timelineFinal':final})
save()
snapshot_step=next((s for s in state['steps'] if s.get('tool')=='manage_snapshots' and s.get('operation')=='snapshot baseline before image motion'),None)
snapshot=snapshot_step.get('result',{}) if snapshot_step else write_call('manage_snapshots',{'projectId':PROJECT,'timelineId':TIMELINE,'action':'save','name':'Baseline source stills + original narration v01'},'snapshot baseline before image motion')
state['snapshot']=snapshot; state['status']='baseline_ready_for_image_motion'; save()
print(json.dumps({'status':state['status'],'projectId':PROJECT,'timelineId':TIMELINE,'scenes':len(state['scenes']),'audioClip':voice['id'],'snapshotId':snapshot.get('snapshotId'),'receipt':str(RECEIPT)},ensure_ascii=False))
