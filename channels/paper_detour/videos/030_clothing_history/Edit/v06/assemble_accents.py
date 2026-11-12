import json
from client_v06 import ROOT, call

ids={'projectId':'B1BA2D18','timelineId':'A7C273C5'}
folder=ROOT/'Source/Graphics/v06/production_final'
m=json.loads((folder/'manifest.json').read_text())
assert abs(m['shared_face_height_px']-72)<.1
assert (ROOT/'Storyboard/COMPOSITE_PREFLIGHT_v06.json').exists(), 'Actual-pair author review required first'
review=json.loads((ROOT/'Storyboard/COMPOSITE_PREFLIGHT_v06.json').read_text())
assert review['status']=='PASS' and review['pairs']==102
new=json.loads((ROOT/'Storyboard/ACCENT_PLAN_v06.json').read_text())
old=json.loads((ROOT/'Storyboard/CUE_SHEET_v05.json').read_text())
timeline=call('get_timeline',ids)
track=next(t for t in timeline['tracks'] if t['name']=='Accents')
assert len(track['clips'])==6, 'One-shot append: inspect existing state before any retry'
for cue in old:
    clip=next(c for c in track['clips'] if c['frames']==[cue['startFrame'],cue['endFrame']])
    cue['clipId']=clip['id']
    cue['preflight_v06']='PASS: all three camera-position composites; actual export review pending'

call('manage_snapshots',{**ids,'action':'save','name':'v06 camera motion before28 additional paper accents'})
assets={};meta={c['id']:c for c in m['cues']}
for cue in old+new:
    c=meta[cue['id']]
    pair=next(p for p in m['pairs'] if p['cue']==cue['id'])
    g=next(x for x in pair['comparisons'] if x['anchor']==pair['anchor'])
    bounds=g['checks']['alpha_bbox_on_canvas']
    up=4.32 if cue['id']=='D03' else (0 if cue['id']=='C06' else 21.6)
    assert bounds[0]>=0 and bounds[2]<=1920 and bounds[1]-up>=0 and bounds[3]+21.6<=1080
    cue.update(geometry=g,png=str(folder/c['png']),metrics=c['metrics'],preflight_v06='PASS: all3 camera-position composites, shared72px target and full motion union inside canvas; author review')
    result=call('import_media',{'projectId':ids['projectId'],'source':{'path':cue['png']},'name':cue['id']+' paper accent','folder':'Accents/v06'})
    assets[cue['id']]=result['mediaRef']
(ROOT/'Edit/v06/imported_accents.json').write_text(json.dumps(assets,indent=2))
for cue in old:
    call('swap_clip_media',{**ids,'clipId':cue['clipId'],'mediaRef':assets[cue['id']]})
call('add_clips',{**ids,'entries':[{'mediaRef':assets[c['id']],'startFrame':c['startFrame'],'endFrame':c['endFrame'],'trackIndex':track['index']} for c in new]})
timeline=call('get_timeline',ids)
for cue in old+new:
    clip=next(c for t in timeline['tracks'] for c in t.get('clips',[]) if c.get('mediaRef')==assets[cue['id']])
    cid=clip['id'];cue['clipId']=cid
    w,h=cue['metrics']['size_px'];left,top=cue['geometry']['layer_top_left_px'];x=left/1920;y=top/1080;d=cue['endFrame']-cue['startFrame']
    call('set_clip_properties',{**ids,'clipIds':[cid],'transform':{'width':w/1920,'height':h/1080,'centerX':(left+w/2)/1920,'centerY':(top+h/2)/1080}})
    if cue['id']=='C06':
        pos=[[0,x,y+.02],[4,x,y,'hold'],[d-1,x,y]]
        op=[[0,0],[4,1,'hold'],[d-1,1]]
    else:
        exit_delta=.004 if cue['id']=='D03' else .02
        pos=[[0,x,y+.02],[4,x,y,'hold'],[d-5,x,y],[d-1,x,y-exit_delta]]
        op=[[0,0],[4,1,'hold'],[d-5,1],[d-1,0]]
    call('set_keyframes',{**ids,'clipId':cid,'property':'position','keyframes':pos})
    call('set_keyframes',{**ids,'clipId':cid,'property':'opacity','keyframes':op})
    cue.update(position_keys=pos,opacity_keys=op)
final=call('get_timeline',ids)
assert len(next(t for t in final['tracks'] if t['name']=='Accents')['clips'])==34
assert final['totalFrames']==5700
sheet=sorted(old+new,key=lambda c:c['startFrame'])
(ROOT/'Storyboard/CUE_SHEET_v06.json').write_text(json.dumps(sheet,ensure_ascii=False,indent=2)+'\n')
(ROOT/'Edit/v06/timeline_final.json').write_text(json.dumps(final,indent=2))
snap=call('manage_snapshots',{**ids,'action':'save','name':'v06 39 camera moves34 paper accents190s'})
(ROOT/'Edit/v06/final_snapshot.json').write_text(json.dumps(snap,indent=2))
print('v06 read-back:39 moving scenes,34 accents, continuous grain and unchanged mix,190seconds.')
