from pathlib import Path
import json
p=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/038_47_ronin');o=p/'Edit/Palmier/mcp-en-v08';r=json.loads((o/'FINAL_READBACK_EN_v09.json').read_text());plan=json.loads((o/'scene-frame-plan-en-draft.json').read_text())['scenes'];main=next(t for t in r['tracks']if t.get('name')=='Main');cues=next(t for t in r['tracks']if t.get('name')=='Accents');audio=next(t for t in r['tracks']if t['type']=='audio');media=json.loads((o/'get_media-before.json').read_text());byid={a['id']:a['name']for a in media['assets']}
assert len(main['clips'])==144 and len(cues['clips'])==13 and len(audio['clips'])==1
for i,(c,s)in enumerate(zip(main['clips'],plan)):
 assert c['frames']==[s['startFrame'],s['endFrame']];assert byid[c['mediaRef']]==s['scene']+'_v01';assert 120<=c['frames'][1]-c['frames'][0]<=180
 if i:assert main['clips'][i-1]['frames'][1]==c['frames'][0]
for g in json.loads((o/'cue-clip-map.json').read_text()):
 c=next(x for x in cues['clips']if x['id']==g['clipId']);assert c['frames']==g['frames'];D=c['frames'][1]-c['frames'][0]
 if g['cue']!='END':
  assert c['keyframes']['opacity']==[[0,0,'linear'],[4,1,'linear'],[D-5,1,'linear'],[D-1,0,'linear']];assert D>=36
  assert [k[0]for k in c['keyframes']['position']]==[0,4,D-5,D-1]
  for key,dy in zip(c['keyframes']['position'],[.02,0,0,-.02]):assert abs(key[1]-g['x'])<=.00051 and abs(key[2]-g['y']-dy)<=.00051
assert audio['clips'][0]['mediaRef']=='59BF264D';assert audio['clips'][0]['frames']==[0,18424];assert main['clips'][-2]['frames'][0]==18426 and r['totalFrames']==18726
receipt={'projectId':'FE6B0E4C','timelineId':'AC510A6E','timelineName':r['name'],'source_script':'Source/Script/narration_en_v09.txt','scenes_in_order':144,'continuous_main':True,'scene_duration_range_seconds':[4,6],'cue_clips':13,'animated_story_cues_verified_keyframes':12,'English_voice_mediaRef':'59BF264D','voice_frames':[0,18424],'end_screen_frames':[18426,18726],'totalFrames':18726,'fps':30,'durationSeconds':624.2,'machine_readback':'PASS','visual_inspection':'16 MCP hold/opening/end frames, contact review;12 full scene-cue proofs and phone contact sheet. Motion in/out playback not reviewed.','listening':'NOT_PERFORMED','semantic_cuts':'DRAFT_REVIEW_REQUIRED; max displacement3.16sec from original fragment timing due4–6sec shot bounds. Final English beat grouping/cut review required.','subtitles':'NOT_ADDED','image_motion':'NOT_APPLIED','music_sfx_mix':'NOT_CREATED','export':'NOT_CREATED','native_end_screen':'NOT_CONFIGURED','independent_review':'NOT_PERFORMED'}
(o/'ASSEMBLY_CHECK_EN_v09.json').write_text(json.dumps(receipt,indent=2));print('PASS144 scene order/continuity,4–6seconds;12 cue keyframes;voicev09;10second tail624.2total')
