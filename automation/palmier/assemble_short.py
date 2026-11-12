#!/usr/bin/env python3
"""Assemble one prechecked, explicitly supplied short in the open Palmier project.

Not resumable. If a request or process fails, inspect the current timeline and
media before any retry; a second execution could create duplicate content.
"""
import argparse, json, sys
from pathlib import Path
from inspect_connection import PalmierConnection
EXPECTED_PROJECT=Path('/Users/diplomat/ytvideos/channels/nuviko_stories/videos/1/1.palmier').resolve()

def main():
 p=argparse.ArgumentParser();p.add_argument('manifest'); a=p.parse_args()
 path=Path(a.manifest).resolve();m=json.loads(path.read_text()); root=path.parents[1].resolve()
 if root.parent != Path('/Users/diplomat/ytvideos/archive/legacy_stories/videos').resolve():raise ValueError('Unexpected release directory')
 for k in ('voice','captions'):
  f=Path(m[k]).resolve();assert f.is_file() and f.is_relative_to(root)
 scenes=m['scenes']; assert scenes and scenes[0]['start']==0 and scenes[-1]['end']==m['frames']
 for i,x in enumerate(scenes):
  f=Path(x['path']).resolve();assert f.is_file() and f.is_relative_to(root)
  assert x['start']<x['end'] and (i==0 or scenes[i-1]['end']==x['start'])
 c=PalmierConnection();c.connect()
 def call(n,a):
  r=c.request('tools/call',{'name':n,'arguments':a})
  if r.get('isError'):raise RuntimeError(f'{n} failed: {r}')
  return json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))
 t=call('get_timeline',{}); pr=call('manage_project',{'action':'list'});assert Path(pr['active']['path']).resolve()==EXPECTED_PROJECT and Path(pr['visible']['path']).resolve()==EXPECTED_PROJECT
 if any(x['name']==m['timeline'] for x in t['timelines']):raise RuntimeError('Timeline name already exists; inspect rather than retry')
 if (t['width'],t['height'],t['fps'])!=(1080,1920,30):
  call('set_active_timeline',{'timelineId':'513CD38A'});t=call('get_timeline',{})
 assert (t['width'],t['height'],t['fps'])==(1080,1920,30)
 created=call('create_timeline',{'name':m['timeline']});tid=created['timelineId'];print('timeline',tid,flush=True)
 t=call('get_timeline',{});assert t['id']==tid and not t['tracks'] and (t['width'],t['height'],t['fps'])==(1080,1920,30)
 receipt={'timelineId':tid,'media':{}}
 for fp in dict.fromkeys([m['voice']]+[x['path'] for x in scenes]+[m['captions']]):
  r=call('import_media',{'source':{'path':fp},'folder':m['timeline']});receipt['media'][fp]=r['mediaRef'];print('import',Path(fp).name,r['mediaRef'],flush=True)
 call('get_media',{'ids':list(receipt['media'].values())})
 imgs=call('add_clips',{'entries':[{'mediaRef':receipt['media'][x['path']],'startFrame':x['start'],'endFrame':x['end']} for x in scenes]})
 for i,cl in enumerate(imgs['clips']):
  n=cl['frames'][1]-cl['frames'][0];a,b=(1.02,1.07) if i%2==0 else (1.07,1.02)
  call('set_keyframes',{'clipId':cl['id'],'property':'scale','keyframes':[[0,a,a],[n-1,b,b]]})
 audio=call('add_clips',{'entries':[{'mediaRef':receipt['media'][m['voice']],'startFrame':0}]})
 for clip in audio['clips']:
  if clip['frames'][1] > m['frames']:
   call('set_clip_properties',{'clipIds':[clip['id']],'durationFrames':m['frames']})
 call('add_clips',{'entries':[{'mediaRef':receipt['media'][m['captions']],'startFrame':0,'endFrame':m['frames'],'includeAudio':False}]})
 t=call('get_timeline',{});assert t['id']==tid and t['totalFrames']==m['frames'];receipt['durationSeconds']=t['durationSeconds'];receipt['tracks']=t['tracks']
 (root/'Edit/palmier_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'ready':True,'timelineId':tid,'frames':m['frames'],'tracks':len(t['tracks'])}),flush=True)
if __name__=='__main__':main()
