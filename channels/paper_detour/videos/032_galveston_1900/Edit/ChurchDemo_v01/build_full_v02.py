"""Single writer: build full revised 129-scene still baseline, ready for canonical motion."""
import json,hashlib
from pathlib import Path
from palmier_client import call,ROOT

E=ROOT.parent.parent;pid='25533909';statepath=ROOT/'full_v02_state.json'
resuming=statepath.exists()
story=json.loads((E/'Storyboard/storyboard_v02.json').read_text());rows=story['scenes']
oldplan=json.loads((E/'Edit/ImageMotion/77fd09462902d1474398/plan.json').read_text())
oldraw=json.loads((ROOT/'full_still_source_fresh.json').read_text());old=json.loads(oldraw['result']['content'][0]['text'])
oldscenes=next(t for t in old['tracks'] if t['name']=='Main')['clips']
pilot=json.loads((ROOT/'editorial_pilot_state.json').read_text())
ps=json.loads((ROOT/'editorial_sources_v02.json').read_text())
known={Path(x['image']).resolve():x['source']['mediaRef'] for x in oldplan}
known.update({Path(x['image']).resolve():x['mediaRef'] for x in ps})
selected=[]
for r in rows:
    path=(E/r['image_path']).resolve()
    if not path.is_file():raise RuntimeError('Missing selected PNG '+str(path))
    selected.append({'id':r['scene_id'],'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'review':'Retained prior exact-file visual acceptance or current full-image reference review; new final composite QA required.'})
(ROOT/'full_selected_sources_v02.json').write_text(json.dumps(selected,indent=2))
if resuming:
    state=json.loads(statepath.read_text());tid=state['timeline_id']
    check=call('get_timeline',{'projectId':pid,'timelineId':tid},'full_v02_resume_reconcile')
    if state['status']!='building' or len(check['tracks'])!=1 or len(check['tracks'][0]['clips'])!=129:
        raise SystemExit('Resume is limited to reconciled scene-only target; inspect any audio/cue state')
else:
    call('manage_snapshots',{'projectId':pid,'timelineId':'6C26D0C3','action':'save','name':'Before full editorial Galveston v02; preserve old full review'},'full_v02_source_snapshot')
    tid=call('create_timeline',{'projectId':pid,'name':'Galveston 032 — editorial full v02 still baseline'},'create_full_v02')['timelineId']
    state={'project_id':pid,'timeline_id':tid,'status':'building','frames':17233,'scene_count':129,'caption_count':16,'voice':'original Odom 1.05x WAV; editor speed1; no cuts/new audio','private_upload_authorized':True}
    statepath.write_text(json.dumps(state,indent=2))
    call('set_project_settings',{'projectId':pid,'timelineId':tid,'width':2560,'height':1440,'outputColorSpace':'rec709'},'full_v02_canvas')
refs=[]
for r in rows:
    path=(E/r['image_path']).resolve()
    if path not in known:
        if resuming:
            existing=next(c for c in check['tracks'][0]['clips'] if c['frames']==[r['in_frame'],r['out_frame_exclusive']]);known[path]=existing['mediaRef']
        else:known[path]=call('import_media',{'projectId':pid,'source':{'path':str(path)},'folder':'Galveston editorial v02','name':r['scene_id']},'full_import_'+r['scene_id'])['mediaRef']
    refs.append(known[path])
if not resuming:call('add_clips',{'projectId':pid,'timelineId':tid,'entries':[{'mediaRef':ref,'startFrame':r['in_frame'],'endFrame':r['out_frame_exclusive']} for ref,r in zip(refs,rows)]},'full_add_129_stills')
live=call('get_timeline',{'projectId':pid,'timelineId':tid},'full_initial_scenes');st=live['tracks'][0]
call('manage_tracks',{'projectId':pid,'timelineId':tid,'set':[{'trackId':st['trackId'],'name':'Scenes'}]},'full_scene_track')
pilotkeys=[((-.01,-.01,1.02),(-.02,-.02,1.04)),((-.03,0,1.06),(-.01,0,1.02)),((-.04,-.02,1.04),(0,-.02,1.04)),((-.03,-.03,1.06),(-.01,-.01,1.02)),((-.04,0,1.04),(0,0,1.04))]
sources=[]
for r,clip,ref in zip(rows,st['clips'],refs):
    sid=r['scene_id'];dur=r['out_frame_exclusive']-r['in_frame'];end=dur-1
    path=(E/r['image_path']).resolve();z=1.0;depth=None
    if sid.startswith('CH'):
        j=int(sid[2:])-1;a,b=pilotkeys[j];z=[1,.95,1,1,.95][j]
        if j==0:depth=ps[0]['depth']
        keys={'position':[[0,a[0],a[1],'linear'],[end,b[0],b[1],'linear']],'scale':[[0,a[2],a[2],'linear'],[end,b[2],b[2],'linear']]}
    elif sid in ('R072','R074','R125','R055','R102'):
        push=sid=='R125';s0,s1=(1.02,1.05) if push else (1.05,1.02)
        if sid=='R055':s0,s1=1.04,1.01
        keys={'position':[[0,(1-s0)/2,(1-s0)/2,'linear'],[end,(1-s1)/2,(1-s1)/2,'linear']],'scale':[[0,s0,s0,'linear'],[end,s1,s1,'linear']]}
        if sid in ('R072','R074'):z=.98
    else:
        idx=int(r['source_history_shot_id'])-1
        # Reconstruct authored endpoints from the recorded gentle-aligned plan (factor .75).
        # The saved still timeline no longer contains these source camera tracks.
        base=oldplan[idx];keys={}
        for prop in ('position','scale'):
            ks=base.get('keyframes',{}).get(prop)
            if not ks:raise RuntimeError('Missing source camera '+sid+' '+prop)
            if len(ks)!=2:raise RuntimeError('Non-endpoint camera requires review '+sid)
            original=[]
            for k in (ks[0],ks[-1]):
                values=[(ks[0][axis]+ks[-1][axis])/2+(k[axis]-(ks[0][axis]+ks[-1][axis])/2)/.75 for axis in (1,2)]
                original.append(values)
            keys[prop]=[[0,*original[0],'linear'],[end,*original[-1],'linear']]
        z=oldplan[idx]['depth_zoom']
    for prop,ks in keys.items():
        call('set_keyframes',{'projectId':pid,'timelineId':tid,'clipId':clip['id'],'property':prop,'keyframes':ks},f'full_{sid}_{prop}')
    item={'clipId':clip['id'],'mediaRef':ref,'image':str(path),'camera':'existing','depth_zoom':z}
    if depth:item['depth']=depth
    sources.append(item)
call('add_clips',{'projectId':pid,'timelineId':tid,'entries':[{'mediaRef':'666A8A59','startFrame':0,'source':[0,574.402608]}]},'full_original_dialogue')
cr=E/'Assets/Generated/full-captions-v04';cm=json.loads((cr/'manifest.json').read_text());cueby={c['id']:c for c in cm['cues']};cues=[]
for c in story['accent_plan']:
    pc=cueby[c['id']];ref=call('import_media',{'projectId':pid,'source':{'path':str(cr/pc['png'])},'folder':'Galveston editorial accents v02','name':c['id']},'full_import_cue_'+c['id'])['mediaRef']
    pair=next(p for p in cm['pairs'] if p['cue']==c['id']);g=next(a for a in pair['comparisons'] if a['anchor']==pair['anchor']);x,y=g['layer_top_left_px'];w,h=pc['metrics']['size_px']
    cues.append({**c,'mediaRef':ref,'x':x/1672,'y':y/941,'width':w/1672,'height':h/941,'png':str(cr/pc['png'])})
call('add_clips',{'projectId':pid,'timelineId':tid,'entries':[{'mediaRef':c['mediaRef'],'startFrame':c['in_frame'],'endFrame':c['out_frame_exclusive']} for c in cues]},'full_add_16_accents')
live=call('get_timeline',{'projectId':pid,'timelineId':tid},'full_before_cue_motion');ct=next(t for t in live['tracks'] if t['type']=='video' and t['trackId']!=st['trackId']);at=next(t for t in live['tracks'] if t['type']=='audio')
call('manage_tracks',{'projectId':pid,'timelineId':tid,'set':[{'trackId':ct['trackId'],'name':'Accents'},{'trackId':at['trackId'],'name':'Dialogue'}],'reorder':[{'trackId':ct['trackId'],'to':0}]},'full_track_order')
for clip,c in zip(ct['clips'],cues):
    x,y,w,h=[c[k] for k in ('x','y','width','height')];dur=c['out_frame_exclusive']-c['in_frame']
    call('set_clip_properties',{'projectId':pid,'timelineId':tid,'clipIds':[clip['id']],'transform':{'centerX':x+w/2,'centerY':y+h/2,'width':w,'height':h,'rotation':0}},'full_cue_transform_'+c['id'])
    for prop,ks in [('position',[[0,x,y+.02,'linear'],[4,x,y,'hold'],[dur-5,x,y,'linear'],[dur-1,x,y-.02,'linear']]),('opacity',[[0,0,'linear'],[4,1,'hold'],[dur-5,1,'linear'],[dur-1,0,'linear']])]:call('set_keyframes',{'projectId':pid,'timelineId':tid,'clipId':clip['id'],'property':prop,'keyframes':ks},'full_cue_motion_'+c['id']+'_'+prop)
(ROOT/'full_sources_v02.json').write_text(json.dumps(sources,indent=2));(ROOT/'full_cues_v02.json').write_text(json.dumps(cues,ensure_ascii=False,indent=2))
config={'episode_dir':str(E),'project_id':pid,'timeline_id':tid,'source_manifest':'full_sources_v02.json','scene_track':'Scenes','preset':'gentle-aligned','grain':'g08','camera':'existing','depth_zoom':1}
(ROOT/'full_motion_v02.json').write_text(json.dumps(config,indent=2))
live=call('get_timeline',{'projectId':pid,'timelineId':tid},'full_still_baseline_final');assert live['totalFrames']==17233
call('manage_snapshots',{'projectId':pid,'timelineId':tid,'action':'save','name':'Full editorial v02 baseline — 129 scenes,16 cues,original narration'},'full_v02_baseline_snapshot')
state.update(status='still_baseline_ready',scene_track=st['trackId'],cue_track=ct['trackId']);statepath.write_text(json.dumps(state,indent=2));print(json.dumps(state))
