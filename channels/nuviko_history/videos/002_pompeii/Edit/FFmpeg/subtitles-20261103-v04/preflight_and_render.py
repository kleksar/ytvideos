from pathlib import Path
import json,subprocess,hashlib,math
from PIL import Image
ROOT=Path('/Users/diplomat/ytvideos');EP=ROOT/'channels/nuviko_history/videos/002_pompeii';EDIT=Path(__file__).resolve().parent;RUN=EP/'Work/subtitles-20261103-v04';WORK=RUN/'scratch/subtitle_render_final';PLAN=EDIT/'montage_plan_v04.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
plan=json.loads(PLAN.read_text());handoff=json.loads((EDIT/'caption_handoff.json').read_text());meta=json.loads((WORK/'caption_groups.json').read_text());groups=meta['groups'];total=handoff['total_frames'];picture=EP/'Work/remaster-nuviko-20261103-v03/scratch/ffmpeg_render_v03/picture.mp4';audio=Path(plan['audio']);out=RUN/'previews/NuvikoHistory_002_Pompeii_Final_Hours_review_v04.mp4'
assert not out.exists()
events=[(0,WORK/'caption_states/00000_neutral.png')]
for gi,g in enumerate(groups):
 for wi,w in enumerate(g):events.append((max(0,min(total-1,math.ceil(w['start']*30-1e-7))),WORK/f'caption_states/{gi:05d}_{wi}.png'))
events=sorted(dict(events).items());assert events[0][0]==0;assert all(p.is_file() for _,p in events)
frames=[1,17,21,1300,22300,25580];evidence=EDIT/'PreRender';evidence.mkdir(exist_ok=True)
for frame in frames:
 state=next(p for start,p in reversed(events) if start<=frame)
 dest=evidence/f'frame_{frame:05d}.png'
 if dest.exists():continue
 subprocess.run(['ffmpeg','-v','error','-ss',str(frame/30),'-i',str(picture),'-i',str(state),'-filter_complex',f'[0:v][1:v]overlay=0:{handoff["top"]},scale=1280:720','-frames:v','1',str(dest)],check=True)
record={'status':'PRE_RENDER_PREPARED','plan':str(PLAN),'plan_sha256':sha(PLAN),'audio_sha256':sha(audio),'clean_picture':str(picture),'clean_picture_sha256':sha(picture),'groups':len(groups),'words':sum(map(len,groups)),'frames':total,'duration_seconds':total/30,'subtitle_coverage':'0 to final frame; states held until next onset','geometry':meta['shared_geometry'],'pre_render_frames':frames,'alignment_comparison':str(EDIT/'ALIGNMENT_COMPARISON.json'),'audible_listening':'not_performed','srt':'new speech-time sidecar; distinct from continuous on-screen hold','test_note':'16/17 montage tests passed; pre-existing focus-camera fixture contradicts direction=none. Current episode plan passes validate().'}
(EDIT/'PRE_RENDER_RECEIPT.json').write_text(json.dumps(record,indent=2)+'\n')
cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-progress','pipe:1','-stats_period','15','-filter_complex_threads','2','-i',str(picture),'-f','concat','-safe','0','-i',handoff['ffconcat'],'-i',str(audio),'-filter_complex',f'[1:v]fps=30,format=rgba[subs];[0:v][subs]overlay=0:{handoff["top"]}:eof_action=pass:format=auto[vsub];[vsub]setsar=1,format=yuv420p[vout]','-map','[vout]','-map','2:a:0','-c:v','h264_videotoolbox','-b:v','16M','-pix_fmt','yuv420p','-r','30','-fps_mode','cfr','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-c:a','copy','-t',f'{total/30:.12f}','-frames:v',str(total),'-movflags','+faststart',str(out)]
(EDIT/'render_command_v04.json').write_text(json.dumps(cmd,indent=2)+'\n')
contract=json.loads((EP/'Edit/Export/EXPORT_CONTRACT_Nuviko_002_Pompeii_v03.json').read_text());contract['status']='READY_TO_RENDER';contract['purpose']='v04 current shared subtitle geometry and reviewed phrase grouping';contract['edit']['timeline_read_path']=str(PLAN);contract['edit']['timeline_read_sha256']=sha(PLAN);contract['edit']['saved_revision_evidence']='v04 subtitle reconstruction over unchanged clean picture/audio';contract['edit']['dependencies']=[{'path':str(p),'sha256':sha(p)} for p in [PLAN,audio,picture,Path(plan['subtitles']['words']),ROOT/'automation/ffmpeg_montage/montage.py',ROOT/'.agents/skills/ytv-paper-subtitles/scripts/semantic_grouping.py',ROOT/'automation/ffmpeg_montage/profiles/long.json']];contract['preflight']={'author':'Codex','output_path':str(out),'overwrite':False,'unresolved_required_fields':[],'receipt':str(EDIT/'PRE_RENDER_RECEIPT.json'),'media_lifecycle_receipt':str(EP/'Edit/MediaLifecycle/subtitles-v04-preflight/audit.json'),'authorization':'User requested rebuilding video with current subtitle rules/scripts'};contract['encoding']['requested_arguments']['command_file']=str(EDIT/'render_command_v04.json');contract['render_receipt']=None;contract['qa_receipt']=None;(EP/'Edit/Export/EXPORT_CONTRACT_Nuviko_002_Pompeii_v04.json').write_text(json.dumps(contract,indent=2)+'\n')
print('PREFLIGHT READY',flush=True)
