import time,json,hashlib,subprocess,sys
from pathlib import Path
sys.path.insert(0,'/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900/Edit/ChurchDemo_v01')
from palmier_client import call
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');R=E/'Edit/ImageMotion/19fd8c3ec5f28ece170b';D=E/'Edit/Export/full_v04';D.mkdir(parents=True,exist_ok=True)
def digest(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def save(name,data):(D/name).write_text(json.dumps(data,indent=2,ensure_ascii=False))
assert not (D/'submission_state.json').exists(),'Existing submission; reconcile, do not repeat'
print('Waiting for canonical motion completion',flush=True)
while True:
 run=json.loads((R/'run.json').read_text())
 if run['status']=='complete':break
 if run['status'] not in ('rendering','applying'):raise RuntimeError(run)
 time.sleep(15)
P='25533909';T=run['target_timeline_id'];actual=call('get_timeline',{'projectId':P,'timelineId':T},'full_motion_export_fresh')
assert actual['fps']==30 and actual['width']==2560 and actual['height']==1440 and actual['totalFrames']==17233 and actual['outputColorSpace']=='rec709'
tracks={t['name']:t for t in actual['tracks']};assert len(tracks['Scenes']['clips'])==129 and len(tracks['Accents']['clips'])==16
scene_refs=sorted(set(c['mediaRef'] for c in tracks['Scenes']['clips']))
media=call('get_media',{'projectId':P,'ids':scene_refs},'full_motion_export_scene_media')
assets={a['id']:a for a in media['assets']}
for c in tracks['Scenes']['clips']:
 assert assets[c['mediaRef']]['type']=='video' and 120<=c['frames'][1]-c['frames'][0]<=180
voice=tracks['Dialogue']['clips'];assert len(voice)==1 and voice[0]['mediaRef']=='666A8A59' and voice[0]['frames']==[0,17232]
assert voice[0].get('speed',1)==1
save('target_read.json',actual)
# Fresh dependency audit immediately before heavy native export; this is read-only.
audit=E/'Edit/MediaLifecycle/audit-native-full-v04';assert not audit.exists()
subprocess.run(['python3','/Users/diplomat/ytvideos/.agents/skills/ytv-media-lifecycle/scripts/media_lifecycle.py','audit','--root','/Users/diplomat/ytvideos','--episode',str(E),'--policy',str(E/'Edit/MediaLifecycle/policy.json'),'--live-palmier','--output-dir',str(audit)],check=True,stdout=subprocess.DEVNULL)
settingsprofile=Path('/Users/diplomat/ytvideos/.agents/skills/ytv-video-export/references/paper-detour.md');audio=json.loads((E/'Edit/ChurchDemo_v01/accepted_audio_component_v02.json').read_text());assert digest(audio['file'])==audio['sha256']
output=E/'Work/church-demo-v01/previews/032_galveston_en_native_v04.mp4';output.parent.mkdir(parents=True,exist_ok=True);assert not output.exists()
snap=call('manage_snapshots',{'projectId':P,'timelineId':T,'action':'save','name':'Full v04 G08 frozen before native export'},'full_v04_export_snapshot')
args={'projectId':P,'timelineId':T,'mode':'video','codec':'H.264','resolution':'Match Timeline','outputPath':str(output),'overwrite':False}
contract={'version':4,'status':'READY_TO_RENDER','episode':'032 Galveston','language':'en','format':'longfilm','purpose':'Complete Private YouTube review release','project_id':P,'timeline_id':T,'saved_timeline':{'file':str(D/'target_read.json'),'sha256':digest(D/'target_read.json'),'snapshot':snap,'native_revision_id':'NOT_EXPOSED'},'profile':{'path':str(settingsprofile),'sha256':digest(settingsprofile)},'video':{'width':2560,'height':1440,'aspect':'16:9','sar':'1:1','fps':'30/1','frame_count':17233,'duration_seconds':17233/30,'container':'mp4','codec':'h264','pix_fmt':'yuv420p','progressive':True,'color_primaries':'bt709','color_transfer':'bt709','color_space':'bt709','color_range':'tv'},'audio':{'source_wav_sha256':audio['source_wav_sha256'],'editor_mediaRef':'666A8A59','source_start':0,'editor_speed':1,'retained_audio_seconds':574.402608,'native_frame_floor':17232,'native_encoding':'AUTO_ENGINE_MANAGED; mono44.1 permitted','final_component':audio,'final_routing':'stream copy previously accepted unchanged full narration AAC48k2ch; no new audio/encode'},'encoding':{'method':'one native Palmier H264 Match Timeline HighestQuality','bitrate_crf_gop_profile_bframes':'AUTO_ENGINE_MANAGED; not settable in live MCP','final_mux':'native video copied; accepted unchanged old-review audio copied; explicit container SAR1:1/DAR16:9 via -aspect 16:9 without re-encoding; faststart; verify both elementary stream hashes and exact cadence'},'submitted_args':args,'authorization':'User explicitly requested full production and Private YouTube upload; preserve voice/addG08; Extra High waiver032','writer':'codex-galveston-church','dependencies':['Storyboard/storyboard_v02.json','Edit/ChurchDemo_v01/full_cues_v02.json','Edit/ImageMotion/19fd8c3ec5f28ece170b/run.json','Assets/Generated/full-captions-v04/manifest.json'],'preflight_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
save('EXPORT_CONTRACT_v04.json',contract);save('submission_state.json',{'phase':'submitting','args':args})
r=call('export_project',args,'full_v04_export_submission');save('submission_state.json',{'phase':'submitted','args':args,'response':r});print(json.dumps(r),flush=True)
