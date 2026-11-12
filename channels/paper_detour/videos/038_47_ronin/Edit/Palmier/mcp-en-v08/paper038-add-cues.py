import sys,json
from pathlib import Path
sys.path.insert(0,'automation/palmier');from inspect_connection import PalmierConnection
p=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/038_47_ronin');o=p/'Edit/Palmier/mcp-en-v08';base={'projectId':'FE6B0E4C','timelineId':'AC510A6E'};c=PalmierConnection();c.connect()
def call(n,args,label):
 r=c.request('tools/call',{'name':n,'arguments':args});(o/(label+'.json')).write_text(json.dumps({'arguments':args,'result':r},indent=2));assert not r.get('isError'),r
 return json.loads(next(x['text']for x in r['content']if x['type']=='text'))
read=c.read_tool('get_timeline',base);assert len(read['tracks'])==2
call('manage_snapshots',{**base,'action':'save','name':'EN v08 voice scenes before English accents'},'snapshot-before-cues')
manroot=p/'Assets/Generated/captions-en-v03-preflight-r01';m=json.loads((manroot/'manifest.json').read_text());timing=json.loads((p/'Source/Graphics/captions_en_v02/CUE_TIMING_EN_v02.json').read_text())['cues'];eroot=p/'Assets/Generated/endscreen-en-v02-preflight-r03';em=json.loads((eroot/'manifest.json').read_text());items=[]
for cue in m['cues']:
 pair=next(x for x in m['pairs']if x['cue']==cue['id']);s=next(x for x in timing if x['cue']==cue['id']);items.append((cue,pair,manroot,s))
items.append((em['cues'][0],em['pairs'][0],eroot,{'cue':'END','startFrame':18426,'endFrame':18726}))
entries=[];geometry={}
for cue,pair,root,t in items:
 id=cue['id'];r=call('import_media',{'projectId':'FE6B0E4C','folder':'EnglishAccents_v02','name':id+'_EN_v02','source':{'path':str(root/cue['png'])}},'import-'+id)
 ref=r['mediaRef'];entries.append({'mediaRef':ref,'startFrame':t['startFrame'],'endFrame':t['endFrame'],'includeAudio':False});w,h=cue['metrics']['size_px'];x,y=pair['comparisons'][0]['layer_top_left_px'];geometry[ref]={'cue':id,'width':w/2560,'height':h/1440,'x':x/2560,'y':y/1440,'frames':[t['startFrame'],t['endFrame']]}
a=c.read_tool('get_media',{'projectId':'FE6B0E4C'});(o/'EnglishAccents-media.json').write_text(json.dumps(a,indent=2));assert all(e['mediaRef']in {x['id']for x in a['assets']}for e in entries)
call('add_clips',{**base,'entries':entries},'add-English-accents13')
read=c.read_tool('get_timeline',base);track=next(t for t in read['tracks']if len(t['clips'])==13);mapping=[]
for clip in track['clips']:
 g=geometry[clip['mediaRef']];w,h,x,y=[g[k]for k in ['width','height','x','y']];assert clip['frames']==g['frames'];D=clip['frames'][1]-clip['frames'][0];id=g['cue'];
 call('set_clip_properties',{**base,'clipIds':[clip['id']],'transform':{'width':w,'height':h,'centerX':x+w/2,'centerY':y+h/2}},'geometry-'+id)
 if id!='END':
  call('set_keyframes',{**base,'clipId':clip['id'],'property':'opacity','keyframes':[[0,0,'linear'],[4,1,'linear'],[D-5,1,'linear'],[D-1,0,'linear']]},'opacity-'+id)
  call('set_keyframes',{**base,'clipId':clip['id'],'property':'position','keyframes':[[0,x,y+.02,'smooth'],[4,x,y,'smooth'],[D-5,x,y,'smooth'],[D-1,x,y-.02,'smooth']]},'position-'+id)
 mapping.append({**g,'clipId':clip['id'],'mediaRef':clip['mediaRef']})
read=c.read_tool('get_timeline',base);(o/'English-assembly-readback.json').write_text(json.dumps(read,indent=2));(o/'cue-clip-map.json').write_text(json.dumps(mapping,indent=2))
call('manage_tracks',{**base,'set':[{'trackId':t['trackId'],'name':('Accents'if len(t['clips'])==13 else 'Main'if t['type']=='video'else 'Narration')}for t in read['tracks']]},'track-names')
print('English assembly',read['totalFrames'],read['durationSeconds'],'tracks',[(t['type'],len(t['clips']))for t in read['tracks']])
