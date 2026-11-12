"""Build isolated five-shot church edit from reviewed, persistent still inputs."""
import json
from pathlib import Path
import numpy as np
from palmier_client import call, ROOT

episode = ROOT.parent.parent
pid = '25533909'
state_path = ROOT / 'editorial_pilot_state.json'
if state_path.exists():
    raise SystemExit('Existing pilot state: inspect live target before resuming mutations')
created = call('create_timeline', {'projectId': pid, 'name': 'Galveston church editorial v02 — still baseline'}, 'create_editorial_pilot')
tid = created['timelineId']
state = {'project_id': pid, 'timeline_id': tid, 'status': 'building', 'frames': 668, 'audio_source_frames': [14173, 14841]}
state_path.write_text(json.dumps(state, indent=2))
call('set_project_settings', {'projectId': pid, 'timelineId': tid, 'width': 2560, 'height': 1440, 'outputColorSpace': 'rec709'}, 'editorial_pilot_canvas')
paths = [episode/'Source/Images/church_v02/CH01_actual_archive_v02.png', episode/'Source/Images/paper_v01/scene_107_v01.png', episode/'Source/Images/church_v02/CH03_v01.png', episode/'Source/Images/church_v02/CH04_v01.png', episode/'Source/Images/paper_v01/scene_110_v01.png']
refs = []
for i, path in enumerate(paths):
    existing = {0:'E2BCF1CF',1:'E3BFAE06',4:'A6F9ADD7'}.get(i)
    refs.append(existing or call('import_media', {'projectId': pid, 'source': {'path': str(path)}, 'folder': 'Church editorial v02', 'name': f'CH{i+1:02d}'}, f'editorial_import_CH{i+1:02d}')['mediaRef'])
bounds = [0,134,267,395,534,668]
call('add_clips', {'projectId':pid,'timelineId':tid,'entries':[{'mediaRef':r,'startFrame':bounds[i],'endFrame':bounds[i+1]} for i,r in enumerate(refs)]}, 'editorial_add_scenes')
live = call('get_timeline', {'projectId':pid,'timelineId':tid}, 'editorial_initial_scenes')
st = live['tracks'][0]
call('manage_tracks', {'projectId':pid,'timelineId':tid,'set':[{'trackId':st['trackId'],'name':'Scenes'}]}, 'editorial_scene_track')
# Explicit, composition-specific two-point camera paths; helper bakes gentle-aligned deviations.
camera = [((-.01,-.01,1.02),(-.02,-.02,1.04)), ((-.03,0,1.06),(-.01,0,1.02)), ((-.04,-.02,1.04),(0,-.02,1.04)), ((-.03,-.03,1.06),(-.01,-.01,1.02)), ((-.04,0,1.04),(0,0,1.04))]
for i,c in enumerate(st['clips']):
    a,b = camera[i]; end = bounds[i+1]-bounds[i]-1
    for prop,keys in [('position',[[0,a[0],a[1],'linear'],[end,b[0],b[1],'linear']]),('scale',[[0,a[2],a[2],'linear'],[end,b[2],b[2],'linear']])]:
        call('set_keyframes',{'projectId':pid,'timelineId':tid,'clipId':c['id'],'property':prop,'keyframes':keys},f'editorial_camera_{i}_{prop}')
call('add_clips',{'projectId':pid,'timelineId':tid,'entries':[{'mediaRef':'666A8A59','startFrame':0,'source':[14173/30,14841/30]}]},'editorial_existing_voice')
cmroot = episode/'Assets/Generated/church-captions-v03'
cm = json.loads((cmroot/'manifest.json').read_text())
cues=[]
for cue,pair,(start,end) in zip(cm['cues'],cm['pairs'],[(325,390),(570,660)]):
    src=cmroot/cue['png']
    ref=call('import_media',{'projectId':pid,'source':{'path':str(src)},'folder':'Church editorial accents v02','name':cue['id']},'editorial_import_'+cue['id'])['mediaRef']
    geom=next(x for x in pair['comparisons'] if x['anchor']==pair['anchor'])
    x,y=geom['layer_top_left_px'];w,h=cue['metrics']['size_px'];
    cues.append({'id':cue['id'],'mediaRef':ref,'start':start,'end':end,'x':x/1672,'y':y/941,'width':w/1672,'height':h/941,'anchor':pair['anchor']})
call('add_clips',{'projectId':pid,'timelineId':tid,'entries':[{'mediaRef':c['mediaRef'],'startFrame':c['start'],'endFrame':c['end']} for c in cues]},'editorial_add_accents')
live=call('get_timeline',{'projectId':pid,'timelineId':tid},'editorial_before_cue_motion')
ct=next(t for t in live['tracks'] if t['type']=='video' and t['trackId']!=st['trackId'])
at=next(t for t in live['tracks'] if t['type']=='audio')
call('manage_tracks',{'projectId':pid,'timelineId':tid,'set':[{'trackId':ct['trackId'],'name':'Accents'},{'trackId':at['trackId'],'name':'Dialogue'}],'reorder':[{'trackId':ct['trackId'],'to':0}]},'editorial_track_order')
for clip,cue in zip(ct['clips'],cues):
    x,y,w,h=[cue[k] for k in ('x','y','width','height')];d=cue['end']-cue['start']
    call('set_clip_properties',{'projectId':pid,'timelineId':tid,'clipIds':[clip['id']],'transform':{'centerX':x+w/2,'centerY':y+h/2,'width':w,'height':h,'rotation':0}},'editorial_transform_'+cue['id'])
    for prop,keys in [('position',[[0,x,y+.02,'linear'],[4,x,y,'hold'],[d-5,x,y,'linear'],[d-1,x,y-.02,'linear']]),('opacity',[[0,0,'linear'],[4,1,'hold'],[d-5,1,'linear'],[d-1,0,'linear']])]:
        call('set_keyframes',{'projectId':pid,'timelineId':tid,'clipId':clip['id'],'property':prop,'keyframes':keys},'editorial_motion_'+cue['id']+'_'+prop)
# The documentary print remains a single plane: no estimated relief within its photograph.
y=np.linspace(0,1,1440,dtype=np.float32)[:,None]
depth=np.broadcast_to(.5+.3*np.clip((y-.91)/.09,0,1),(1440,2560)).copy()
dp=episode/'Assets/Generated/church-document-plane-depth-v02.npy';np.save(dp,depth)
sources=[{'mediaRef':r,'image':str(path),'camera':'existing','depth_zoom':z} for r,path,z in zip(refs,paths,[1,.95,1,1,.95])]
sources[0]['depth']=str(dp)
(ROOT/'editorial_sources_v02.json').write_text(json.dumps(sources,indent=2))
(ROOT/'editorial_motion_v02.json').write_text(json.dumps({'episode_dir':str(episode),'project_id':pid,'timeline_id':tid,'source_manifest':'editorial_sources_v02.json','scene_track':'Scenes','preset':'gentle-aligned','grain':'g08','camera':'existing','depth_zoom':1},indent=2))
live=call('get_timeline',{'projectId':pid,'timelineId':tid},'editorial_still_baseline_final')
assert live['totalFrames']==668
state.update(status='still_baseline_ready',scene_refs=refs,scene_bounds=bounds,cues=cues)
state_path.write_text(json.dumps(state,indent=2))
print(json.dumps(state))
