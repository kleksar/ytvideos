#!/usr/bin/env python3
"""Test motion on two clips of a previously journaled Palmier TEST copy.

No Palmier changes without --apply. See test_recut_motion_on_copy.md.
"""
import argparse
import base64
import importlib.util
import json
import os
from pathlib import Path
import sys
from datetime import datetime, timezone
from uuid import uuid4

EDIT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('recut', EDIT / 'palmier_recut_105_provisional.py')
recut = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recut)


def read_journal(path):
    lines = [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
    pre = [x['data'] for x in lines if x.get('kind') == 'preflight']
    tests = [x['data'] for x in lines if x.get('kind') == 'test_stopped']
    batches = [x['data'] for x in lines if x.get('kind') == 'intent' and x.get('data', {}).get('operation') == 'add_clips']
    recut.check(len(pre) == len(tests) == len(batches) == 1, 'Expected one preflight, one batch and a completed test_stopped journal')
    recut.check(tests[0].get('complete') is False and tests[0].get('shots') == 2, 'Journal must describe precisely two test clips')
    entries = batches[0].get('entries')
    recut.check(batches[0].get('offset') == 0 and len(entries) == 2, 'Expected first two clips only')
    return pre[0], tests[0], entries


def target(t, track_id, entries):
    return recut.check_new_track(t, track_id, entries)


def other_tracks(t, track_id):
    return [x for x in t['tracks'] if x.get('trackId') != track_id]


def inspect_frame(c, frame, expected_id, output):
    r = c.request('tools/call', {'name':'inspect_timeline','arguments':{'startFrame':frame}})
    recut.check(not r.get('isError'), f'inspect_timeline refused frame {frame}')
    blocks = r.get('content', [])
    images = [x for x in blocks if x.get('type') == 'image' and x.get('mimeType') == 'image/jpeg']
    texts = [x.get('text') for x in blocks if x.get('type') == 'text']
    recut.check(len(images) == len(texts) == 1, 'Unexpected inspection response')
    info = json.loads(texts[0]); frames = info.get('frames', [])
    recut.check(len(frames) == 1 and frames[0].get('frame') == frame and expected_id in frames[0].get('clips', []), f'Frame {frame}: expected clip is not visible')
    with output.open('xb') as f:
        f.write(base64.b64decode(images[0]['data'], validate=True))
    return info


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--journal', required=True, help='journal.jsonl from --test-first-batch --batch-size 2')
    ap.add_argument('--map', required=True, help='Same CSV used by test copy')
    ap.add_argument('--keyframes', required=True, help='Same keyframes JSON used in test preflight')
    ap.add_argument('--copy-id', required=True, help='Exact currently active test copy ID from journal')
    ap.add_argument('--apply', action='store_true', help='Apply four keyframe tracks only to the two test clips; default is read-only preflight')
    args=ap.parse_args()
    journal_path=Path(args.journal); map_path=Path(args.map); key_path=Path(args.keyframes)
    recut.check(all(p.is_absolute() and p.is_file() for p in (journal_path,map_path,key_path)), 'Journal, map and keyframes must be existing absolute files')
    pre,test,entries=read_journal(journal_path)
    recut.check(pre.get('source_timeline_id') and args.copy_id == test.get('copy_id') and args.copy_id != pre['source_timeline_id'], 'Copy ID does not match test journal or equals source')
    recut.check(pre.get('map_sha256') == recut.sha256(map_path) and pre.get('keyframes_sha256') == recut.sha256(key_path), 'Map or keyframes differ from the test journal')
    rows=recut.read_map(map_path); keyframes=recut.read_keyframes(key_path,rows)
    recut.check(1 in keyframes and 2 in keyframes, 'Both test clips need keyframes')
    recut.check(all(set(keyframes[n]) == {'scale','position'} for n in (1,2)), 'Test accepts only scale + position on both clips')
    for r,e in zip(rows[:2],entries):
        recut.check((r['start_frame'],r['end_frame_exclusive']) == (e['startFrame'],e['endFrame']), 'Test entries do not match map boundaries')
        recut.check(recut.sha256(r['image_path']) == pre.get('image_hashes', {}).get(r['image_path']), 'Test image differs from preflight')
    track_id=test.get('track_id'); recut.check(isinstance(track_id,str) and track_id, 'Journal lacks test track ID')
    c=recut.PalmierConnection();c.connect()
    t=recut.state(c,args.copy_id)
    recut.check(recut.voice(t) == pre.get('voice_baseline'), 'Voice differs from test preflight')
    track=target(t,track_id,entries)
    clips=sorted(track['clips'],key=lambda x:x['frames'][0])
    recut.check(len(clips)==2, 'Test track must contain exactly two clips')
    for clip in clips:
        recut.check(not (clip.get('keyframes') or {}).get('scale') and not (clip.get('keyframes') or {}).get('position'), 'Test clip already has scale or position keyframes; refuse replacement')
    others=other_tracks(t,track_id)
    report={'mode':'apply' if args.apply else 'dry-run','source_timeline_id':pre['source_timeline_id'],'copy_id':args.copy_id,'track_id':track_id,'clips':[{'id':x['id'],'frames':x['frames'],'mediaRef':x['mediaRef']} for x in clips], 'map_sha256':pre['map_sha256'],'keyframes_sha256':pre['keyframes_sha256']}
    if not args.apply:
        print(json.dumps(report,ensure_ascii=False,indent=2)); return
    run=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'_'+uuid4().hex[:8]
    out=EDIT/'palmier_motion_tests'/run;out.mkdir(parents=True,exist_ok=False)
    logpath=out/'journal.jsonl'
    def log(kind,data):
        with logpath.open('a',encoding='utf-8') as f:
            f.write(json.dumps({'time':datetime.now(timezone.utc).isoformat(),'kind':kind,'data':data},ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
    log('preflight',report)
    try:
        for n,clip in enumerate(clips,1):
            for prop in ('scale','position'):
                t=recut.state(c,args.copy_id)
                recut.check(recut.voice(t)==pre['voice_baseline'] and other_tracks(t,track_id)==others, 'Voice or other copy tracks changed')
                track=target(t,track_id,entries)
                live=next(x for x in track['clips'] if x['id']==clip['id'])
                recut.check(not (live.get('keyframes') or {}).get(prop), f'{prop} already exists; refuse replacement')
                params={'clipId':clip['id'],'property':prop,'keyframes':keyframes[n][prop]}
                log('intent',{'operation':'set_keyframes','args':params})
                receipt=recut.tool(c,'set_keyframes',params)
                log('receipt',{'operation':'set_keyframes','result':receipt})
                t=recut.state(c,args.copy_id)
                recut.check(recut.voice(t)==pre['voice_baseline'] and other_tracks(t,track_id)==others, 'Voice or other copy tracks changed after mutation')
                track=target(t,track_id,entries);live=next(x for x in track['clips'] if x['id']==clip['id'])
                actual=(live.get('keyframes') or {}).get(prop)
                def normalized(points): return [p[:-1] if p and p[-1]=='smooth' else p for p in points]
                recut.check(actual is not None and normalized(actual)==normalized(keyframes[n][prop]), f'{prop} did not round-trip as expected')
        # Capture exact single frames, including both sides of the cut.
        for n,clip in enumerate(clips,1):
            start,end=clip['frames']
            for label,frame in (('start',start),('mid',(start+end-1)//2),('end',end-1)):
                t=recut.state(c,args.copy_id)
                recut.check(recut.voice(t)==pre['voice_baseline'] and other_tracks(t,track_id)==others, 'Copy changed before inspection')
                target(t,track_id,entries)
                name=f'clip_{n:02d}_{label}_frame_{frame}.jpg'
                info=inspect_frame(c,frame,clip['id'],out/name)
                log('inspected_frame',{'path':str(out/name),'metadata':info})
        log('complete',{'copy_id':args.copy_id,'frames':6,'review_required':True})
        print(json.dumps({'copy_id':args.copy_id,'frames':6,'directory':str(out),'review_required':True},ensure_ascii=False))
    except Exception as e:
        log('stopped',{'error':str(e),'note':'Do not retry blindly; inspect test copy and journal'})
        raise

if __name__=='__main__':
    try: main()
    except Exception as exc:
        print(f'STOP: {exc}',file=sys.stderr);sys.exit(1)
