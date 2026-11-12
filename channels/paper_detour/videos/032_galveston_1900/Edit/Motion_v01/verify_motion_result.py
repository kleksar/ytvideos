"""Verify the canonical motion run against live Palmier state and original baseline."""
import collections,importlib.util,json
from pathlib import Path
ROOT=Path('/Users/diplomat/ytvideos');EP=ROOT/'channels/paper_detour/videos/032_galveston_1900';W=EP/'Edit/Motion_v01'
spec=importlib.util.spec_from_file_location('m',ROOT/'automation/image_motion/run.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
R=EP/'Edit/ImageMotion/77fd09462902d1474398';run=json.loads((R/'run.json').read_text())
assert run['status']=='complete',run['status']
c=m.Palmier(W);target=c.call('get_timeline',{'projectId':'25533909','timelineId':run['target_timeline_id']})
baseline=c.call('get_timeline',{'projectId':'25533909','timelineId':'137B5BA9'})
original=json.loads((W/'baseline_live.json').read_text())
assert m.fingerprint(baseline)==m.fingerprint(original),'Static baseline changed'
source=json.loads((R/'target_before.json').read_text())
m.verify(source,target,run['scenes'],'Main')
counts=collections.Counter();rows=[]
actual={tuple(x['frames']):x for x in m.track(target,'Main')['clips']}
for i,s in enumerate(run['scenes']):
    a=actual[tuple(s['source']['frames'])];k=a['keyframes'];p=k['position'];z=k['scale']
    dx=p[-1][1]-p[0][1];dy=p[-1][2]-p[0][2];dz=z[-1][1]-z[0][1]
    if abs(dz)>.002:mode='push-in' if dz>0 else 'pull-out'
    elif abs(dx)>.002:mode='pan-right' if dx>0 else 'pan-left'
    elif abs(dy)>.002:mode='pan-down' if dy>0 else 'pan-up'
    else:raise AssertionError(f'S{i+1:03}: missing whole-image camera motion')
    counts[mode]+=1;m.probe(Path(s['video']),s)
    rows.append({'scene':f'S{i+1:03}','mode':mode,'frames':a['frames'],'camera_verified':True,
        'parallax_sign':s['sign'],'video':s['video'],'video_sha256':m.file_hash(Path(s['video']))})
cues=json.loads((W/'cue_motion_applied_v02.json').read_text());acc={tuple(x['frames']):x for x in m.track(target,'Accents')['clips']}
assert len(acc)==14
for cue in cues:
    a=acc[(cue['start_frame'],cue['end_frame_exclusive'])]
    assert m.equal(a['keyframes'],cue['keyframes']),cue['id']
    # Position keys are authoritative; Palmier retains the original static center.
    # C14/C15 deliberately use the alternate anchor in those keys.
    assert m.equal({k:a['transform'][k] for k in ['width','height']},
                   {k:cue['transform'][k] for k in ['width','height']}),cue['id']
assert m.equal(m.canonical(m.track(baseline,'Dialogue')),m.canonical(m.track(target,'Dialogue'))),'Dialogue changed'
assert not any('grain' in t['name'].lower() for t in target['tracks'])
voice=ROOT/'channels/nuviko_history/videos/017_galveston_1900/Source/Voice/odom_5vsg/film/voice_en_105.wav'
assert m.file_hash(voice)=='ddfe274d2a67c1250053192a0ef3b28f41cdd49e3120404a0fa9f8700ce5cd52'
m.save(W/'final_live_timeline.json',target)
m.save(W/'structural_motion_qa.json',{'status':'PASS','project_id':'25533909','target_timeline_id':run['target_timeline_id'],
    'target_name':target['name'],'static_baseline_unchanged':True,'scene_count':len(rows),'camera_modes':dict(counts),
    'scenes':rows,'animated_cues_verified':len(cues),'dialogue_unchanged':True,'voice_sha256':m.file_hash(voice),
    'grain_tracks':0,'total_frames':target['totalFrames'],'fps':target['fps'],
    'visual_qa':'separate sampled inspection; not established by structural pass','audio_listening':'UNVERIFIED','independent_review':'UNVERIFIED'})
print(json.dumps({'status':'PASS','timeline':run['target_timeline_id'],'name':target['name'],'modes':dict(counts),'cues':len(cues)},ensure_ascii=False))
