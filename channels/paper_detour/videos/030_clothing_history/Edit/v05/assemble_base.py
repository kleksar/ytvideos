from palmier_client import call,ROOT
import json
P='B1BA2D18';T='E69F8516';target={'projectId':P,'timelineId':T}
tl=call('get_timeline',target);assert not tl.get('tracks'),'Target must be empty before one-time assembly'
call('import_media',{'projectId':P,'source':{'path':str(ROOT/'Source/Images/v05/framed')},'folder':'Scenes/v05'})
media=call('get_media',{'projectId':P});assets={a['name']:a['id'] for a in media['assets']}
shots=json.loads((ROOT/'Storyboard/SHOTLIST_v05.json').read_text())
entries=[{'mediaRef':assets[s['id']+'_framing'],'startFrame':s['startFrame'],'endFrame':s['endFrame'],'includeAudio':False} for s in shots]
call('add_clips',{**target,'entries':entries});print('39 scenes placed',flush=True)
gr=call('import_media',{'projectId':P,'source':{'path':'/Users/diplomat/ytvideos/channels/paper_detour/Shared/Overlays/Film_Grain/paper_film_grain_visible_15min_270x480_30fps_v01.mov'},'name':'Continuous paper grain','folder':'Overlays'})
call('add_clips',{**target,'entries':[{'mediaRef':gr['mediaRef'],'startFrame':0,'endFrame':5700,'includeAudio':False}]})
tl=call('get_timeline',target)
clip=next(c for t in tl['tracks'] for c in t.get('clips',[]) if c.get('mediaRef')==gr['mediaRef'])
call('set_clip_properties',{**target,'clipIds':[clip['id']],'opacity':0.25,'transform':{'centerX':0.5,'centerY':0.5,'width':0.5625,'height':1.7777777778,'rotation':90},'blendMode':'normal'})
a=call('import_media',{'projectId':P,'source':{'path':str(ROOT/'Source/Audio/v05/full_mix.wav')},'name':'Full mix v05 — Lawrence music foley','folder':'Audio/v05'})
call('add_clips',{**target,'entries':[{'mediaRef':a['mediaRef'],'startFrame':0,'endFrame':5700}]})
tl=call('get_timeline',target);(ROOT/'Edit/v05/timeline_base.json').write_text(json.dumps(tl,ensure_ascii=False,indent=2));print('Base+continuous grain+full mix saved',flush=True)
