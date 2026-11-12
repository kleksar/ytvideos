#!/usr/bin/env python3
"""Build the separate Paper Detour Short 02 trial using Palmier MCP operations."""
import json, pathlib, sys, time
ROOT=pathlib.Path('/Users/diplomat/ytvideos')
sys.path.insert(0,str(ROOT/'automation/palmier'))
from inspect_connection import PalmierConnection
c=PalmierConnection(); c.connect()

def call(name, args):
    result=c.request('tools/call', {'name':name,'arguments':args})
    if result.get('isError'):
        raise RuntimeError(f'{name}: {result}')
    text=[x['text'] for x in result.get('content',[]) if x.get('type')=='text']
    try: obj=json.loads(text[0]) if len(text)==1 else result
    except ValueError: obj=result
    print(json.dumps({'tool':name,'response':obj},ensure_ascii=False),flush=True)
    return obj

name='Paper Detour 001 Short 02 Director Trial 20261031'
projects=call('manage_project',{'action':'list'})
if any(p.get('name')==name for p in projects.get('projects',[])):
    raise SystemExit('Project exists; refusing to create a duplicate')
project=call('manage_project',{'action':'create','name':name,'aspectRatio':'9:16','quality':'1080p','fps':30})
paths=[
'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Storyboard/director_pilot_20261031/concept_B_researcher_waveform.png',
'channels/paper_detour/videos/001_radio_game/Shorts/01_radio_signal/Source/Images/rework_v3/researcher/researcher_master.png',
'channels/paper_detour/videos/001_radio_game/Shorts/01_radio_signal/Source/Images/rework_v3/03_radio_MASTER.png',
'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Source/Images/director_trial_20261031/04_waveform_selection.png',
'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Source/Images/director_trial_20261031/05_six_cards.png',
'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Source/Images/director_trial_20261031/06_reported_comparison.png',
'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Source/Audio/Director_trial_20261031/preview_mix_36p6_no_sfx_stereo.wav',
]
refs=[]
for p in paths:
    if not (ROOT/p).is_file(): raise FileNotFoundError(p)
    imp=call('import_media',{'source':{'path':str(ROOT/p)}})
    refs.append(imp['mediaRef'])
bounds=[0,186,446,544,781,923,1098]
entries=[{'mediaRef':refs[i],'startFrame':bounds[i],'endFrame':bounds[i+1]} for i in range(6)]
entries.append({'mediaRef':refs[6],'startFrame':0,'endFrame':1098})
call('add_clips',{'entries':entries})
timeline=call('get_timeline',{})
visual=[]
for t in timeline.get('tracks',[]):
    for clip in t.get('clips',[]):
        if clip.get('mediaRef') in refs[:6]: visual.append(clip)
visual.sort(key=lambda x:x['frames'][0])
if len(visual)!=6: raise RuntimeError(f'Expected 6 visual clips; found {len(visual)}')
for i,clip in enumerate(visual):
    duration=bounds[i+1]-bounds[i]
    # gentle centered camera move for four shots, held shots give visual breathing room
    if i in (0,1,3,5):
        end=1.035 if i != 3 else 1.025
        call('set_keyframes',{'clipId':clip['id'],'property':'scale','keyframes':[[0,1.0,1.0,'smooth'],[duration-1,end,end,'smooth']]})
        call('set_keyframes',{'clipId':clip['id'],'property':'position','keyframes':[[0,0,0,'smooth'],[duration-1,-(end-1)/2,-(end-1)/2,'smooth']]})
call('get_timeline',{})
