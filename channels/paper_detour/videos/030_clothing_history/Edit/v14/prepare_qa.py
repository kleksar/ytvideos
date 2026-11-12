from pathlib import Path
import json,math
P=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history');E=P/'Edit/v14';shots=json.loads((P/'Storyboard/SHOTLIST_v14.json').read_text());cues=json.loads((P/'Storyboard/CUE_SHEET_v14.json').read_text());sr=json.loads((E/'SRT_CUES_v14.json').read_text())['cues'];extra=set();srtmap=[]
for no,q in enumerate(sr,1):
 start=math.ceil(float(q['start_seconds'])*30-1e-7);end=math.ceil(float(q['end_seconds'])*30-1e-7)
 frames=[start,(start+end-1)//2,end-1];edges=[max(0,start-1),min(5699,end)]
 cuts=[]
 for s in shots[1:]:
  f=s['startFrame']
  if start<=f<end:cuts.extend([f-1,f])
 extra.update(frames+edges+cuts);srtmap.append({'cue':no,'start_frame':start,'end_frame_exclusive':end,'phases':frames,'adjacent_frames':edges,'scene_cut_frames':cuts,'text':q['text']})
for s in shots:
 if s['id'] in ['V16','V17','V27','V29','V31']:extra.update(range(s['startFrame'],s['endFrame'],10))
for change in json.loads((E/'CUE_REPAIRS.json').read_text()):extra.update(range(change['fade_start']-1,change['after_frames'][1]+1))
plan={'frame_count':5700,'fps':'30/1','scene_seconds':[4,6],'freshness':{'status':'CURRENT','evidence':'Edit/v14/EXPORT_CONTRACT_v14.json and POST_EDIT.json; freshlivebinding rechecked after export'},'expected':{'video':{'width':2560,'height':1440,'codec_name':'h264','pix_fmt':'yuv420p','color_space':'bt709'},'audio':{'required':True,'codec_name':'aac','channels':2,'sample_rate':48000}},'scenes':[{'id':s['id'],'start':s['startFrame'],'end':s['endFrame']} for s in shots],'cues':[],'extra_frames':sorted(extra)}
for q in cues:
 k=q['opacity_keys'];row={'id':q['id'],'start':q['startFrame'],'end':q['endFrame'],'entry_end':q['startFrame']+k[1][0]}
 if q['id']!='C06':row['exit_start']=q['startFrame']+k[-2][0]
 plan['cues'].append(row)
(E/'qa-plan-v14.json').write_text(json.dumps(plan,indent=2));(E/'SRT_FRAME_PLAN.json').write_text(json.dumps(srtmap,indent=2));print('extra',len(extra))
