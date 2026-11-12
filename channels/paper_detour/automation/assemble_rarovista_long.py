#!/usr/bin/env python3
"""Build a Rarovista long-form from a validated episode manifest in a NEW timeline.

The default validates files locally only; --execute mutates Palmier. No rendering
is performed. A prior receipt, ambiguous response, active export, or any change
of project or timeline stops execution. Review and resolve manually; never retry
an uncertain mutation automatically.


--execute must be run only when the specified project is already active and
visible with a 1920x1080/30 active timeline. Does not switch the user's project
or timeline. Every side effect is journaled; a timeout means stop, inspect, and
never automatically retry. Audio is the supplied WAV; no speed
operation is applied. Subtitles remain a separate SRT; export is not performed.
The target media folder is inspected with an unfiltered inventory; if absent,
its creation is journaled before calling organize_media and verified afterwards.
"""
import argparse, hashlib, json, math, os, re, shutil, subprocess, sys
from pathlib import Path

FPS=30
MIN_FREE=8*1024**3

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def probe(p):return json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],capture_output=True,text=True,check=True).stdout)

def folder_preflight(call, target):
 """Return whether the target folder exists, rejecting populated or malformed inventories."""
 inventory=call('get_media',{})
 folders=inventory.get('folders');assets=inventory.get('assets')
 if not isinstance(folders,list) or not all(isinstance(x,str) for x in folders) or not isinstance(assets,list):
  raise RuntimeError('Unfiltered media inventory is malformed')
 if target not in folders:
  if any(isinstance(a,dict) and isinstance(a.get('folder'),str) and (a['folder']==target or a['folder'].startswith(target+'/')) for a in assets):
   raise RuntimeError('Target folder missing from inventory but contains assets; inspect')
  return False
 filtered=call('get_media',{'folder':target})
 if not isinstance(filtered.get('assets'),list):raise RuntimeError('Filtered media inventory is malformed')
 if filtered['assets']:raise RuntimeError('Target media folder is already populated; inspect before assembly')
 return True

def ensure_media_folder(call,target,existed,guard,begin,done):
 """Create a missing folder only after the caller has written a receipt."""
 guard()
 current=folder_preflight(call,target)
 if current!=existed:raise RuntimeError('Target media folder changed since preflight; inspect')
 if existed:return
 begin('create_media_folder',folder=target)
 result=call('organize_media',{'createFolders':[target]})
 if not isinstance(result.get('createdFolders'),list) or target not in result['createdFolders']:
  raise RuntimeError('Folder creation was not confirmed; inspect receipt and inventory')
 guard()
 if not folder_preflight(call,target):raise RuntimeError('Created folder is not present in inventory')
 done(createdFolders=result['createdFolders'])

def validate_srt(path,duration):
 """Check actual SubRip cue order and boundaries against the final WAV."""
 data=path.read_text(encoding='utf-8-sig').strip()
 if not data:raise ValueError('SRT is empty')
 stamp=re.compile(r'^(\d{2,}):(\d{2}):(\d{2}),(\d{3})$')
 def seconds(text):
  match=stamp.fullmatch(text)
  if not match:raise ValueError('Malformed SRT timestamp')
  h,m,s,ms=map(int,match.groups())
  if m>=60 or s>=60:raise ValueError('Malformed SRT timestamp')
  return h*3600+m*60+s+ms/1000
 last_end=0
 for i,block in enumerate(re.split(r'\n\s*\n',data.replace('\r\n','\n')),1):
  lines=block.splitlines()
  if len(lines)<3 or lines[0].strip()!=str(i) or not any(line.strip() for line in lines[2:]):raise ValueError('Malformed SRT cue')
  times=lines[1].split(' --> ')
  if len(times)!=2:raise ValueError('Malformed SRT timing')
  start,end=map(seconds,times)
  if start<last_end or end<=start or end>duration+.001:raise ValueError('SRT cue overlap or outside audio')
  last_end=end

def validate(manifest_path,series,inspect=probe,free_space=None):
 series=Path(series).resolve();mp=Path(manifest_path).resolve()
 if mp!=series/'Edit/Long/manifest.json':raise ValueError('Expected Edit/Long/manifest.json')
 m=json.loads(mp.read_text())
 if m.get('status')!='ready' or m.get('missing') or m.get('missing_assets'):raise ValueError('Manifest must be explicitly ready, with no missing assets')
 timeline=m.get('timeline')
 if not isinstance(timeline,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,96}',timeline) or type(m.get('fps')) is not int or m['fps']!=FPS:raise ValueError('Invalid timeline name or fps')
 speed=m.get('voice_speed_applied')
 if not isinstance(speed,(int,float)) or isinstance(speed,bool) or not math.isfinite(speed) or not .5<=speed<=2:raise ValueError('Manifest must declare finite speed already applied to the voice (0.5–2.0)')
 frames=m.get('frames')
 if type(frames)!=int or frames<=0:raise ValueError('Invalid total frame count')
 def asset(p):
  if not isinstance(p,str) or not Path(p).is_absolute():raise ValueError('Asset paths must be absolute')
  original=Path(p);p=original.resolve()
  if original!=p:raise ValueError(f'Asset paths must be canonical to avoid duplicate imports: {original}')
  if not p.is_file() or not p.is_relative_to(series/'Source'):raise ValueError(f'Missing or external source asset: {p}')
  return p
 voice=asset(m['voice']);srt=asset(m['srt'])
 if voice.suffix.lower()!='.wav' or srt.suffix.lower()!='.srt':raise ValueError('Expected PCM WAV and SRT')
 if m.get('sha256',{}).get('voice')!=sha(voice) or m.get('sha256',{}).get('srt')!=sha(srt):raise ValueError('Voice or SRT hash mismatch')
 pv=inspect(voice);stream=next((x for x in pv['streams'] if x.get('codec_type')=='audio'),None)
 if not stream or not stream.get('codec_name','').startswith('pcm_'):raise ValueError('WAV must contain PCM audio')
 duration=float(stream.get('duration') or pv['format']['duration'])
 if not math.isfinite(duration) or duration<=0 or math.ceil(duration*FPS)!=frames:raise ValueError('Frame count must cover exact WAV duration')
 validate_srt(srt,duration)
 scenes=m.get('scenes');seen=set();seen_names={voice.stem:voice};last=0
 if not isinstance(scenes,list) or not scenes:raise ValueError('Missing scenes')
 for scene in scenes:
  start,end=scene.get('start'),scene.get('end')
  if type(start)!=int or type(end)!=int or start!=last or end-start<2 or end>frames:raise ValueError('Scenes must cover every frame once without gaps or overlap and last at least two frames')
  image=asset(scene['path'])
  if image.stem in seen_names and seen_names[image.stem]!=image:raise ValueError('Duplicate asset name in Palmier media folder')
  seen.add(image);seen_names[image.stem]=image
  if scene.get('sha256')!=sha(image):raise ValueError(f'Image hash mismatch: {image}')
  iv=next((x for x in inspect(image)['streams'] if x.get('codec_type')=='video'),None)
  if not iv or iv.get('width',0)<1 or iv.get('height',0)<1 or abs(iv['width']/iv['height']-16/9)>.006:raise ValueError(f'Expected 16:9 image: {image}')
  if not isinstance(scene.get('cue'),str) or not scene['cue'].strip():raise ValueError('Each scene needs a narrative cue')
  last=end
 if last!=frames:raise ValueError('Scenes do not cover the complete voice track')
 receipt=mp.parent/'palmier_receipt.json'
 if receipt.exists():raise ValueError('Receipt exists; inspect previous attempt before doing anything')
 free=shutil.disk_usage(series).free if free_space is None else free_space
 return {'manifest':m,'manifestPath':mp,'manifestSha256':sha(mp),'receipt':receipt,'timeline':timeline,'frames':frames,'duration':duration,'sceneCount':len(scenes),'freeBytes':free,'minimumFreeBytes':MIN_FREE,'series':series}

def execute(info,project):
 if info['freeBytes']<MIN_FREE:raise RuntimeError('Less than 8 GiB free; assembly blocked')
 project=Path(project).resolve()
 if project.suffix!='.palmier' or not project.is_dir():raise ValueError('Explicit existing .palmier project path required')
 sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'automation/palmier'))
 from inspect_connection import PalmierConnection
 c=PalmierConnection();c.connect()
 def call(name,args):
  x=c.request('tools/call',{'name':name,'arguments':args})
  if x.get('isError'):raise RuntimeError(f'{name}: {x}')
  return json.loads(next(y['text'] for y in x['content'] if y['type']=='text'))
 m=info['manifest'];rp=info['receipt'];tid=None;expected_clips={};timeline=info['timeline'];series=info['series']
 def guard(allow_extra=False):
  pr=call('manage_project',{'action':'list'});tl=call('get_timeline',{})
  if any(not isinstance(pr.get(k),dict) or not pr[k].get('path') or Path(pr[k]['path']).resolve()!=project for k in ('active','visible')):raise RuntimeError('Project changed or is not visible')
  exports=call('manage_exports',{'action':'list'}).get('exports')
  if not isinstance(exports,list):raise RuntimeError('Malformed exports inventory')
  if any(e.get('status') not in ('completed','failed','cancelled','canceled') for e in exports if isinstance(e,dict)):raise RuntimeError('Palmier export in progress or unknown state')
  if any(not isinstance(e,dict) for e in exports):raise RuntimeError('Malformed export entry')
  if (tl['width'],tl['height'],tl['fps'])!=(1920,1080,FPS):raise RuntimeError('Active timeline is not 1920x1080/30')
  if tid and (tl['id']!=tid or tl['name']!=timeline):raise RuntimeError('Active timeline changed')
  if sha(info['manifestPath'])!=info['manifestSha256']:raise RuntimeError('Manifest changed during assembly')
  if sha(Path(m['srt']))!=m['sha256']['srt']:raise RuntimeError('SRT changed during assembly')
  if shutil.disk_usage(series).free<MIN_FREE:raise RuntimeError('Free space fell below safety threshold')
  if tid:
   actual={x['id']:x for tr in tl['tracks'] for x in tr.get('clips',[])}
   if not allow_extra and set(actual)!=set(expected_clips):raise RuntimeError('Unexpected clip added or removed')
   for cid,want in expected_clips.items():
    current=actual.get(cid)
    if not current or current['frames']!=want['frames'] or current.get('mediaRef')!=want['mediaRef'] or current.get('keyframes',{}).get('scale')!=want.get('scale') or current.get('keyframes',{}).get('position')!=want.get('position'):raise RuntimeError(f'Clip {cid} changed during assembly')
  return tl
 state=guard()
 if any(x['name']==timeline for x in state['timelines']):raise RuntimeError('Named timeline already exists; stop')
 folder_exists=folder_preflight(call,timeline)
 receipt={'status':'started','timeline':timeline,'project':str(project),'manifestSha256':info['manifestSha256'],'media':{},'steps':[]}
 def sync_receipt_dir():
  fd=os.open(str(rp.parent),os.O_RDONLY)
  try:os.fsync(fd)
  finally:os.close(fd)
 with rp.open('x') as f:json.dump(receipt,f,indent=2);f.flush();os.fsync(f.fileno())
 sync_receipt_dir()
 def save():
  tmp=rp.with_suffix('.tmp')
  with tmp.open('w') as f:
   json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
  tmp.replace(rp)
  sync_receipt_dir()
 def begin(name,**kw):receipt['pending']={'action':name,**kw};save()
 def done(**kw):receipt['steps'].append({**receipt.pop('pending'),**kw});save()
 ensure_media_folder(call,timeline,folder_exists,guard,begin,done)
 begin('create_timeline',timelineName=timeline);created=call('create_timeline',{'name':timeline});tid=created['timelineId'];receipt['timelineId']=tid
 tl=guard()
 if tl['tracks'] or tl['totalFrames']!=0:raise RuntimeError('New timeline is not empty')
 done(timelineId=tid);receipt['status']='timeline_created';save()
 assets=list(dict.fromkeys([m['voice']]+[x['path'] for x in m['scenes']]))
 expected={m['voice']:m['sha256']['voice'],**{s['path']:s['sha256'] for s in m['scenes']}}
 for fp in assets:
  guard()
  if sha(Path(fp))!=expected[fp]:raise RuntimeError(f'Source file changed: {fp}')
  inventory=call('get_media',{'folder':timeline})['assets']
  if any(x['name']==Path(fp).stem for x in inventory):raise RuntimeError('Same-named media already exists; stop')
  begin('import_media',path=fp);result=call('import_media',{'source':{'path':fp},'folder':timeline});ref=result['mediaRef'];guard();ready=call('get_media',{'ids':[ref]})['assets']
  if len(ready)!=1 or ready[0].get('generationStatus'):raise RuntimeError('Import not confirmed ready')
  receipt['media'][fp]=ref;done(mediaRef=ref)
 receipt['status']='media_ready';save()
 # Small batches ensure a failed call cannot obscure a long list of operations.
 clips=[]
 for i in range(0,len(m['scenes']),8):
  guard();subset=m['scenes'][i:i+8];entries=[{'mediaRef':receipt['media'][s['path']],'startFrame':s['start'],'endFrame':s['end']} for s in subset]
  begin('add_clips',sceneIndexes=list(range(i,i+len(subset))));result=call('add_clips',{'entries':entries});added=result['clips'];tl=guard(allow_extra=True);actual={c['id']:c for tr in tl['tracks'] for c in tr.get('clips',[])}
  if len(added)!=len(subset):raise RuntimeError('Batch returned unexpected clip count')
  for s,cl in zip(subset,added):
   v=actual.get(cl['id'])
   if not v or v['frames']!=[s['start'],s['end']] or v['mediaRef']!=receipt['media'][s['path']]:raise RuntimeError('Added scene did not match plan')
   expected_clips[cl['id']]={'frames':[s['start'],s['end']],'mediaRef':receipt['media'][s['path']]}
  guard();clips.extend(added);done(clipIds=[x['id'] for x in added])
 receipt['imageClipIds']=[x['id'] for x in clips];receipt['status']='images_added';save()
 for i,(s,cl) in enumerate(zip(m['scenes'],clips)):
  guard();span=s['end']-s['start'];start,end=(1.04,1.08) if i%2==0 else (1.08,1.04);keyframes=[[0,start,start],[span-1,end,end]]
  begin('set_keyframes',clipId=cl['id']);call('set_keyframes',{'clipId':cl['id'],'property':'scale','keyframes':keyframes});expected_clips[cl['id']]['scale']=keyframes;tl=guard();actual=[c for tr in tl['tracks'] for c in tr.get('clips',[]) if c['id']==cl['id']]
  if len(actual)!=1 or actual[0].get('keyframes',{}).get('scale')!=keyframes:raise RuntimeError('Motion verification failed')
  done(keyframes=keyframes)
  # Counter-position compensates scaling, keeping edges covered while adding a
  # restrained alternating lateral drift. Image movement is not character animation.
  drift=.008 if i%2==0 else -.008
  pos=[[0,round((1-start)/2+drift,4),round((1-start)/2,4)],[span-1,round((1-end)/2-drift,4),round((1-end)/2,4)]]
  begin('set_position_keyframes',clipId=cl['id']);call('set_keyframes',{'clipId':cl['id'],'property':'position','keyframes':pos});expected_clips[cl['id']]['position']=pos;tl=guard();actual=[c for tr in tl['tracks'] for c in tr.get('clips',[]) if c['id']==cl['id']]
  if len(actual)!=1 or actual[0].get('keyframes',{}).get('position')!=pos:raise RuntimeError('Position verification failed')
  done(keyframes=pos)
 guard();begin('add_voice',path=m['voice']);res=call('add_clips',{'entries':[{'mediaRef':receipt['media'][m['voice']],'startFrame':0}]});tl=guard(allow_extra=True);added=res['clips'];actual=[c for tr in tl['tracks'] for c in tr.get('clips',[]) if c.get('mediaRef')==receipt['media'][m['voice']]]
 # Audio may round to the nearest frame; it may be up to one frame shorter than the ceiling-sized image timeline.
 if len(added)!=1 or len(actual)!=1 or actual[0]['frames'][0]!=0 or abs(actual[0]['frames'][1]-info['frames'])>1:raise RuntimeError('Voice placement differs by more than a frame')
 expected_clips[added[0]['id']]={'frames':actual[0]['frames'],'mediaRef':receipt['media'][m['voice']]}
 done(clipId=added[0]['id']);tl=guard()
 if tl['totalFrames']!=info['frames']:raise RuntimeError('Final timeline duration differs from manifest')
 receipt.update({'status':'assembled','tracks':tl['tracks'],'durationSeconds':tl['durationSeconds']});save()
 return {'timelineId':tid,'receipt':str(rp)}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--series',type=Path,required=True,help='Episode directory containing Source and Edit/Long');p.add_argument('--execute',action='store_true');p.add_argument('--project',type=Path,help='Explicit already active and visible Palmier project')
 a=p.parse_args()
 if a.execute and not a.project:p.error('--execute requires --project')
 if a.project and not a.execute:p.error('--project is only used with --execute')
 info=validate(a.manifest,a.series);summary={k:info[k] for k in ('timeline','frames','duration','sceneCount','freeBytes','minimumFreeBytes')};summary.update({'mode':'execute' if a.execute else 'offline-dry-run','enoughSpaceForAssembly':info['freeBytes']>=MIN_FREE})
 if a.execute:summary.update(execute(info,a.project))
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
