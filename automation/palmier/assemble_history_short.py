#!/usr/bin/env python3
"""Validate or assemble one reviewed historical Short in an idle Palmier project.

Default mode is local validation only. Execution requires an already active and
visible project with a 1080x1920/30 timeline. Every mutation is journaled; never
blindly retry an interrupted assembly. Audio is already at its final speed.
"""
import argparse, json, math, os, re, shutil, sys
from pathlib import Path
from assemble_history_long import sha, probe, validate_srt, folder_preflight, ensure_media_folder

FPS = 30
MIN_FREE = 8 * 1024**3

def validate(path, root):
    path, root = Path(path).resolve(), Path(root).resolve()
    if path.parent != root / 'Edit/Shorts': raise ValueError('Manifest must be in episode Edit/Shorts')
    m = json.loads(path.read_text())
    if m.get('status') != 'ready' or m.get('voice_speed_applied') != 1.05 or m.get('fps') != FPS: raise ValueError('Manifest not ready or incorrect voice speed/fps')
    name = m.get('timeline')
    if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,96}', name): raise ValueError('Invalid timeline name')
    frames = m.get('frames')
    if type(frames) is not int or frames <= 0: raise ValueError('Invalid duration')
    def asset(entry):
        p = Path(entry['path']).resolve()
        if not p.is_relative_to(root) or not p.is_file() or sha(p) != entry['sha256']: raise ValueError(f'Missing or changed asset {p}')
        return p
    voice, captions, srt = (asset(m[x]) for x in ('voice', 'captions', 'srt'))
    if voice.suffix.lower() != '.wav' or captions.suffix.lower() != '.mov' or srt.suffix.lower() != '.srt': raise ValueError('Expected WAV, MOV and SRT')
    vi = probe(voice); audio = next((x for x in vi['streams'] if x.get('codec_type') == 'audio'), None)
    if not audio or not audio.get('codec_name','').startswith('pcm_'): raise ValueError('Voice must be PCM')
    duration = float(audio.get('duration') or vi['format']['duration'])
    if not math.isfinite(duration) or math.ceil(duration * FPS) != frames: raise ValueError('WAV and frame duration disagree')
    validate_srt(srt, duration)
    ci = next((x for x in probe(captions)['streams'] if x.get('codec_type') == 'video'), None)
    if not ci or (ci.get('width'),ci.get('height')) != (1080,1920) or int(ci.get('nb_frames',0)) != frames or not ci.get('pix_fmt','').startswith('yuva'): raise ValueError('Caption MOV needs alpha and exact frame count')
    scenes = m.get('scenes'); last = 0; hashes=set(); names={voice.stem,captions.stem}
    if not isinstance(scenes,list) or not scenes: raise ValueError('No scenes')
    for x in scenes:
        if x.get('start') != last or type(x.get('end')) is not int or x['end']-last < 2: raise ValueError('Non-contiguous or short scene')
        p=asset(x)
        if p.stem in names or x['sha256'] in hashes: raise ValueError('Duplicate scene')
        names.add(p.stem);hashes.add(x['sha256']); last=x['end']
        im=next((i for i in probe(p)['streams'] if i.get('codec_type')=='video'),None)
        if not im or abs(im['width']/im['height']-9/16)>.006: raise ValueError(f'Image must be vertical: {p}')
        if not x.get('cue'): raise ValueError('Narrative cue required')
    if last != frames: raise ValueError('Scenes do not cover the voice')
    receipt=path.with_name(path.stem+'_palmier_receipt.json')
    if receipt.exists(): raise ValueError('Previous receipt exists; inspect before retrying')
    return m, receipt

def execute(path, root, project, m, receipt_path):
    project=Path(project).resolve(); root=Path(root).resolve()
    if project.suffix != '.palmier' or not project.is_dir(): raise ValueError('Explicit existing Palmier project required')
    from inspect_connection import PalmierConnection
    c=PalmierConnection();c.connect(); tid=None; expected={}; digest=sha(path)
    def call(name,args):
        r=c.request('tools/call',{'name':name,'arguments':args})
        if r.get('isError'): raise RuntimeError(f'{name}: {r}')
        return json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))
    def guard(allow_extra=False):
        pr=call('manage_project',{'action':'list'});tl=call('get_timeline',{})
        if any(not isinstance(pr.get(k),dict) or Path(pr[k].get('path','')).resolve()!=project for k in ('active','visible')): raise RuntimeError('Project changed or is not visible')
        ex=call('manage_exports',{'action':'list'}).get('exports')
        if not isinstance(ex,list) or any(not isinstance(e,dict) or e.get('status') not in ('completed','failed','cancelled','canceled') for e in ex): raise RuntimeError('Export in progress or unknown')
        if (tl['width'],tl['height'],tl['fps'])!=(1080,1920,FPS): raise RuntimeError('Expected active vertical 1080x1920/30 timeline')
        if tid and (tl['id']!=tid or tl['name']!=m['timeline']): raise RuntimeError('Active timeline changed')
        if sha(path)!=digest or shutil.disk_usage(root).free<MIN_FREE: raise RuntimeError('Manifest changed or disk space low')
        if tid:
            actual={x['id']:x for tr in tl['tracks'] for x in tr.get('clips',[])}
            if not allow_extra and set(actual)!=set(expected): raise RuntimeError('Unexpected clip added or removed')
            for cid,want in expected.items():
                got=actual.get(cid)
                if not got or got['frames']!=want['frames'] or got.get('mediaRef')!=want['mediaRef'] or got.get('keyframes',{}).get('scale')!=want.get('scale'): raise RuntimeError('Existing clip changed')
        return tl
    state=guard()
    if any(x['name']==m['timeline'] for x in state['timelines']): raise RuntimeError('Timeline already exists')
    existed=folder_preflight(call,m['timeline'])
    receipt={'status':'started','timeline':m['timeline'],'project':str(project),'manifestSha256':digest,'media':{},'steps':[]}
    def save():
        tmp=receipt_path.with_suffix('.tmp')
        with tmp.open('w') as f: json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        tmp.replace(receipt_path)
    with receipt_path.open('x') as f: json.dump(receipt,f);f.flush();os.fsync(f.fileno())
    def begin(action,**kwargs): receipt['pending']={'action':action,**kwargs};save()
    def done(**kwargs): receipt['steps'].append({**receipt.pop('pending'),**kwargs});save()
    ensure_media_folder(call,m['timeline'],existed,guard,begin,done)
    begin('create_timeline');tid=call('create_timeline',{'name':m['timeline']})['timelineId'];receipt['timelineId']=tid
    tl=guard()
    if tl['tracks'] or tl['totalFrames']: raise RuntimeError('New timeline not empty')
    done(timelineId=tid)
    for x in [m['voice'],*m['scenes'],m['captions']]:
        guard(); p=x['path']
        if sha(Path(p))!=x['sha256']: raise RuntimeError('Asset changed')
        if any(a['name']==Path(p).stem for a in call('get_media',{'folder':m['timeline']})['assets']): raise RuntimeError('Media name already exists')
        begin('import_media',path=p);ref=call('import_media',{'source':{'path':p},'folder':m['timeline']})['mediaRef'];guard()
        assets=call('get_media',{'ids':[ref]})['assets']
        if len(assets)!=1 or assets[0].get('generationStatus'): raise RuntimeError('Media import not confirmed')
        receipt['media'][p]=ref;done(mediaRef=ref)
    def add(entries, label):
        guard();begin(label);added=call('add_clips',{'entries':entries})['clips'];tl=guard(True)
        actual={x['id']:x for tr in tl['tracks'] for x in tr.get('clips',[])}
        if len(added)!=len(entries):raise RuntimeError('Unexpected clip count')
        for entry, clip in zip(entries,added):
            actual_clip=actual.get(clip['id'])
            if not actual_clip or actual_clip.get('mediaRef')!=entry['mediaRef'] or actual_clip['frames'][0]!=entry['startFrame']: raise RuntimeError('Unexpected clip placement')
            if 'endFrame' in entry and actual_clip['frames'][1]!=entry['endFrame']:raise RuntimeError('Unexpected clip end')
            expected[clip['id']]={'frames':actual_clip['frames'],'mediaRef':entry['mediaRef']}
        guard();done(clipIds=[x['id'] for x in added]);return added
    for i in range(0,len(m['scenes']),8):
        subset=m['scenes'][i:i+8]
        clips=add([{'mediaRef':receipt['media'][x['path']],'startFrame':x['start'],'endFrame':x['end']} for x in subset],'add_scenes')
        for j,(scene,clip) in enumerate(zip(subset,clips),start=i):
            guard();span=scene['end']-scene['start']; a,b=(1.02,1.07) if j%2==0 else (1.07,1.02);keys=[[0,a,a],[span-1,b,b]]
            begin('set_keyframes',clipId=clip['id']);call('set_keyframes',{'clipId':clip['id'],'property':'scale','keyframes':keys});expected[clip['id']]['scale']=keys;guard();done(keyframes=keys)
    voice=add([{'mediaRef':receipt['media'][m['voice']['path']],'startFrame':0}],'add_voice')[0]
    if abs(expected[voice['id']]['frames'][1]-m['frames'])>1: raise RuntimeError('Voice duration differs by more than one frame')
    add([{'mediaRef':receipt['media'][m['captions']['path']],'startFrame':0,'endFrame':m['frames'],'includeAudio':False}],'add_captions')
    tl=guard()
    if tl['totalFrames']!=m['frames']:raise RuntimeError('Unexpected timeline length')
    receipt.update(status='assembled',tracks=tl['tracks'],durationSeconds=tl['durationSeconds']);save()
    return tid

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--series',type=Path,required=True);p.add_argument('--execute',action='store_true');p.add_argument('--project',type=Path)
    a=p.parse_args();path=a.manifest.resolve();root=a.series.resolve();m,receipt=validate(path,root)
    if a.execute:
        if not a.project:raise ValueError('--project required for execution')
        print(json.dumps({'timelineId':execute(path,root,a.project,m,receipt),'receipt':str(receipt)}))
    else:print(json.dumps({'valid':True,'timeline':m['timeline'],'frames':m['frames'],'scenes':len(m['scenes'])}))
if __name__=='__main__':main()
