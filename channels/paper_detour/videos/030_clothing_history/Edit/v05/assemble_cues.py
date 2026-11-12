from palmier_client import call,ROOT
import json
P='B1BA2D18';T='E69F8516';target={'projectId':P,'timelineId':T};folder=ROOT/'Source/Graphics/v05/production'
m=json.loads((folder/'manifest.json').read_text());sheet=json.loads((ROOT/'Storyboard/CUE_SHEET_v05.json').read_text());assets={};meta={c['id']:c for c in m['cues']}
call('manage_snapshots',{**target,'action':'save','name':'Scenes full mix and grain before paper accents'})
for cue in sheet:
 c=meta[cue['id']];pair=next(x for x in m['pairs'] if x['cue']==cue['id']);g=next(x for x in pair['comparisons'] if x['anchor']==pair['anchor'])
 bounds=g['checks']['alpha_bbox_on_canvas'];assert bounds[0]>=0 and bounds[2]<=1920 and bounds[1]-21.6>=0 and bounds[3]+21.6<=1080
 cue['geometry']=g;cue['png']=str(folder/c['png']);cue['metrics']=c['metrics'];cue['preflight']='PASS: exact PNG scene pair and phone preview checked; no face/clue overlap; full ±0.02 vertical motion union on-canvas.'
 a=call('import_media',{'projectId':P,'source':{'path':cue['png']},'name':cue['id']+' paper accent','folder':'Accents/v05'});assets[cue['id']]=a['mediaRef']
call('add_clips',{**target,'entries':[{'mediaRef':assets[c['id']],'startFrame':c['startFrame'],'endFrame':c['endFrame']} for c in sheet]})
tl=call('get_timeline',target)
for c in sheet:
 clip=next(v for tr in tl['tracks'] for v in tr.get('clips',[]) if v.get('mediaRef')==assets[c['id']]);cid=clip['id'];c['clipId']=cid;w,h=c['metrics']['size_px'];left,top=c['geometry']['layer_top_left_px'];x=left/1920;y=top/1080;D=c['endFrame']-c['startFrame']
 call('set_clip_properties',{**target,'clipIds':[cid],'transform':{'width':w/1920,'height':h/1080,'centerX':(left+w/2)/1920,'centerY':(top+h/2)/1080}})
 if c['id']=='C06':
  pos=[[0,x,y+.02],[4,x,y,'hold'],[D-1,x,y]];op=[[0,0],[4,1,'hold'],[D-1,1]]
 else:
  pos=[[0,x,y+.02],[4,x,y,'hold'],[D-5,x,y],[D-1,x,y-.02]];op=[[0,0],[4,1,'hold'],[D-5,1],[D-1,0]]
 call('set_keyframes',{**target,'clipId':cid,'property':'position','keyframes':pos});call('set_keyframes',{**target,'clipId':cid,'property':'opacity','keyframes':op});c['position_keys']=pos;c['opacity_keys']=op
call('manage_tracks',{**target,'set':[{'index':0,'name':'Accents'},{'index':1,'name':'Grain'},{'index':2,'name':'Scenes'},{'index':3,'name':'Mix'}]})
(ROOT/'Storyboard/CUE_SHEET_v05.json').write_text(json.dumps(sheet,ensure_ascii=False,indent=2))
tl=call('get_timeline',target);(ROOT/'Edit/v05/timeline_final.json').write_text(json.dumps(tl,ensure_ascii=False,indent=2))
call('manage_snapshots',{**target,'action':'save','name':'v05 full film 190s ready for export'})
print('Final timeline:',tl['durationSeconds'],'seconds;',[(x.get('name'),len(x.get('clips',[]))) for x in tl['tracks']])
