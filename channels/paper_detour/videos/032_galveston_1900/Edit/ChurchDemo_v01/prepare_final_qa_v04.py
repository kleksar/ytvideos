import json,math,hashlib,importlib.util
from pathlib import Path
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Edit/Export/full_v04';C=json.loads((D/'EXPORT_CONTRACT_v04.json').read_text());R=json.loads((D/'render_receipt_v04.json').read_text());S=json.loads((E/'Storyboard/storyboard_v02.json').read_text());Q=json.loads((E/'Edit/ChurchDemo_v01/full_cues_v02.json').read_text());spec=importlib.util.spec_from_file_location('srt_owner','/Users/diplomat/ytvideos/.agents/skills/ytv-srt/scripts/srt_tool.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);U=m.parse_srt((E/'Edit/Subtitles_v02/032_galveston_en_v07.srt').read_text());extra=set()
for s in S['scenes']:
 a,b=s['in_frame'],s['out_frame_exclusive'];extra.update([a+(b-a)//4,a+3*(b-a)//4,a+(b-a-1)//2])
for c in Q:
 a,b=c['in_frame'],c['out_frame_exclusive'];extra.update(range(a,min(a+5,b)));extra.update(range(max(a,b-5),b+1))
for c in U:
 a=math.ceil(float(c['start_seconds'])*30);b=math.ceil(float(c['end_seconds'])*30);extra.update([a,max(a,(a+b)//2),min(17232,b-1)])
chap=[0,25,76,129,218,296,341,472,511,547]
for t in chap:
 extra.update([f for f in [t*30-1,t*30,t*30+1] if 0<=f<17233])
plan={'frame_count':17233,'fps':'30/1','sha256':R['sha256'],'freshness':{'status':'CURRENT','evidence':'Edit/Export/full_v04/render_receipt_v04.json and target_read.json; freeze snapshot before native export, compare fresh timeline after render'},'expected':{'video':{'width':2560,'height':1440,'codec_name':'h264','pix_fmt':'yuv420p','color_space':'bt709'},'audio':{'required':True,'codec_name':'aac','channels':2,'sample_rate':48000}},'scene_seconds':[4,6],'scenes':[{'id':s['scene_id'],'start':s['in_frame'],'end':s['out_frame_exclusive']} for s in S['scenes']],'cues':[{'id':c['id'],'start':c['in_frame'],'end':c['out_frame_exclusive'],'entry_end':c['in_frame']+4,'exit_start':c['out_frame_exclusive']-5} for c in Q],'extra_frames':sorted(extra)}
p=E/'Edit/QA/full-v04-plan.json';p.parent.mkdir(exist_ok=True);assert not p.exists();p.write_text(json.dumps(plan,indent=2));print('QA plan ready',len(extra),'extra frames')
