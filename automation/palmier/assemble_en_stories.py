#!/usr/bin/env python3
"""Assemble one EN Story in Palmier; manifest and exact source paths required.

This is a one-shot operation, not resumable. It creates no VPN graphics. Call
only after reviewing the manifest and after other Palmier operations have stopped.
If interrupted, inspect project and receipt; never blindly run again.
"""
import argparse, glob, json, math, subprocess, sys
from pathlib import Path
from inspect_connection import PalmierConnection

PROJECT = Path('/Users/diplomat/ytvideos/channels/nuviko_stories/videos/1/1.palmier').resolve()
ROOT = Path('/Users/diplomat/ytvideos/archive/legacy_stories/videos').resolve()
FPS = 30

def duration(path):
    data = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(path)]))
    return float(data['format']['duration'])

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path)
    p.add_argument('--apply', action='store_true', help='actually change Palmier')
    opt = p.parse_args()
    m = json.loads(opt.manifest.read_text())
    root = Path(m['episode_root']).resolve()
    assert root.parent == ROOT and root.is_dir()
    name = m['timeline']
    assert name.startswith(root.name[:3]+'_en_')
    segments = m['segments']
    assert 1 <= len(segments) <= 3
    for s in segments:
        for k in ('audio','text','alignment'):
            f=Path(s[k]).resolve()
            assert f.is_file() and f.is_relative_to(root),f
        assert duration(s['audio']) > 0
    recipe = m['broll']
    assert recipe and all(x['mediaRef'] and int(x['frames'])>0 for x in recipe)
    estimated = sum(math.ceil(duration(s['audio'])*FPS/1.1) for s in segments)+max(0,len(segments)-1)*3
    if sum(int(x['frames']) for x in recipe)<estimated+30:
        raise ValueError('B-roll recipe too short: extend using checked clips before creating a timeline')
    print(json.dumps({'dry_run':not opt.apply,'timeline':name,'estimated_frames':estimated,'recipe_frames':sum(int(x['frames']) for x in recipe),'segments':len(segments)},ensure_ascii=False),flush=True)
    if not opt.apply:return
    receipt_path=Path(m['receipt']).resolve()
    assert receipt_path.is_relative_to(root) and not receipt_path.exists(),receipt_path
    c=PalmierConnection();c.connect()
    def call(n,a):
        r=c.request('tools/call',{'name':n,'arguments':a})
        if r.get('isError'):raise RuntimeError((n,r))
        return json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))
    def check(tid=None):
        pr=call('manage_project',{'action':'list'})
        assert Path(pr['active']['path']).resolve()==PROJECT and Path(pr['visible']['path']).resolve()==PROJECT
        t=call('get_timeline',{})
        assert (t['width'],t['height'],t['fps'])==(1080,1920,FPS)
        if tid:assert t['id']==tid,(tid,t['id'])
        return t
    t=check();assert not any(tl['name']==name for tl in t['timelines']), 'timeline already exists'
    receipt={'timeline_name':name,'project':str(PROJECT),'status':'creating','segments':[],'broll':recipe}
    def save():
        receipt_path.parent.mkdir(parents=True,exist_ok=True)
        receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    save()
    created=call('create_timeline',{'name':name});tid=created['timelineId'];receipt['timeline_id']=tid;receipt['status']='created';save()
    t=check(tid);assert not t['tracks']
    cursor=0
    for i,s in enumerate(segments):
        check(tid)
        imp=call('import_media',{'source':{'path':s['audio']},'folder':f'Stories/{root.name[:3]}/English/Voice','name':f'{root.name[:3]}_en_{i+1}'})
        receipt['segments'].append({**s,'mediaRef':imp['mediaRef'],'status':'imported'});save()
        inserted=call('add_clips',{'entries':[{'mediaRef':imp['mediaRef'],'startFrame':cursor}]})
        clip=inserted['clips'][0];receipt['segments'][-1]['clipId']=clip['id'];receipt['segments'][-1]['status']='placed';save()
        altered=call('edit_speed',{'clipId':clip['id'],'action':'uniform','rate':1.1})
        result=next(x for x in altered['clips'] if x['id']==clip['id'])
        assert result['frames'][0]==cursor and result['speed']==1.1
        receipt['segments'][-1].update({'frames':result['frames'],'speed':1.1,'status':'ready'});save()
        cursor=result['frames'][1]+(3 if i+1<len(segments) else 0)
    frames=cursor;receipt['totalFrames']=frames;receipt['status']='audio_ready';save()
    entries=[];cursor=0
    for x in recipe:
        length=min(int(x['frames']),frames-cursor)
        if length<=0:break
        entries.append({'mediaRef':x['mediaRef'],'startFrame':cursor,'endFrame':cursor+length,'includeAudio':False});cursor+=length
    assert cursor==frames
    check(tid);receipt['status']='adding_broll';receipt['broll_entries']=entries;save()
    res=call('add_clips',{'entries':entries});receipt['broll_result']=res;receipt['status']='awaiting_captions';save()
    t=check(tid);assert t['totalFrames']==frames;receipt['timeline_snapshot']=t;save()
    print(json.dumps({'timeline_id':tid,'frames':frames,'segments':receipt['segments'],'status':receipt['status']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
