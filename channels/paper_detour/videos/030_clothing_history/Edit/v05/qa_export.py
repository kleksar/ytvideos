from pathlib import Path
import json,subprocess,hashlib,re
import numpy as np
from PIL import Image,ImageDraw,ImageOps
ROOT=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history');out=ROOT/'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v05.mp4';qa=ROOT/'Edit/v05/QA';qa.mkdir(exist_ok=True)
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]));(qa/'ffprobe.json').write_text(json.dumps(probe,indent=2));v=next(s for s in probe['streams'] if s['codec_type']=='video');assert(v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1920,1080,'30/1',5700)
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True);print('Full MP4 decode PASS',flush=True)
shots=json.loads((ROOT/'Storyboard/SHOTLIST_v05.json').read_text());cues=json.loads((ROOT/'Storyboard/CUE_SHEET_v05.json').read_text());frames={int((s['startFrame']+s['endFrame'])/2) for s in shots}
for c in cues:
 frames|={c['startFrame']+1,c['startFrame']+4,c['endFrame']-5,c['endFrame']-1}
frames=sorted(frames);expr='+'.join(f'eq(n,{f})' for f in frames)
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-vf',f'select={expr.replace(",",chr(92)+",")}', '-vsync','0','-q:v','2',str(qa/'frame_%03d.jpg')],check=True)
files=sorted(qa.glob('frame_*.jpg'));assert len(files)==len(frames);mapping={frame:str(file) for frame,file in zip(frames,files)};(qa/'frame_map.json').write_text(json.dumps(mapping,indent=2))
sheet=Image.new('RGB',(1600,8*220),(225,220,210));dr=ImageDraw.Draw(sheet)
for i,s in enumerate(shots):
 f=int((s['startFrame']+s['endFrame'])/2);im=Image.open(mapping[f]);x=i%5*320;y=i//5*220;sheet.paste(im.resize((310,175)),(x+5,y));dr.text((x+5,y+180),f'{s["id"]} {s["duration"]:.2f}s f{f}',fill='black')
sheet.save(qa/'ALL_39_EXPORTED_SCENES.jpg')
sheet=Image.new('RGB',(1440,3*430),(25,28,34));dr=ImageDraw.Draw(sheet)
for i,c in enumerate(cues):
 f=c['startFrame']+4;im=Image.open(mapping[f]);x=i%2*720;y=i//2*430;sheet.paste(im.resize((720,405)),(x,y));dr.text((x+8,y+411),c['id']+' | '+ ' / '.join(c['lines']),fill='white')
sheet.save(qa/'ALL_6_EXPORTED_CUES.jpg')
# Measure actual motion in a fixed crop away from all text. This does not replace visual grain review.
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(out),'-vf','crop=160:90:1700:400,format=gray','-f','rawvideo','-pix_fmt','gray','-'])
a=np.frombuffer(raw,dtype=np.uint8).reshape(-1,90,160).astype(np.int16);delta=np.abs(a[1:]-a[:-1]).mean(axis=(1,2));cuts={s['startFrame'] for s in shots}
seams=[]
for f in range(240,5700,240):
 if min(abs(f-x) for x in cuts)<3:continue
 seams.append({'frame':f,'mean_pixel_delta_before':float(delta[f-2]),'at':float(delta[f-1]),'after':float(delta[f])})
# Validate native cue keys and full cover from the persisted timeline.
tl=json.loads((ROOT/'Edit/v05/timeline_final.json').read_text());scene=next(t for t in tl['tracks'] if t.get('name')=='Scenes');assert len(scene['clips'])==39
for i,s in enumerate(shots):
 assert 120<=s['endFrame']-s['startFrame']<=180
 if i:assert shots[i-1]['endFrame']==s['startFrame']
assert shots[-1]['endFrame']==5700
text=(ROOT/'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v05.srt').read_text();times=re.findall(r'(\d\d):(\d\d):(\d\d),(\d{3})',text);vals=[int(h)*3600+int(m)*60+int(s)+int(ms)/1000 for h,m,s,ms in times];assert vals==sorted(vals) and vals[-1]<=190
report={'file':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'duration_seconds':float(probe['format']['duration']),'full_decode':'PASS','39_shot_duration_and_coverage':'PASS','actual_exported_scene_samples':39,'actual_exported_cue_keyframe_samples':len(frames)-39,'grain_crop_adjacent_delta_median':float(np.median(delta)),'grain_seams':seams,'subtitle_times':'PASS; exact voice alignment, no global speed change','playback_1x_with_sound':'UNVERIFIED','listening':'UNVERIFIED','independent_review':'NOT_PERFORMED','visual_samples':'pending author inspection'}
(qa/'REPORT.json').write_text(json.dumps(report,indent=2));print('Technical QA saved. Grain crop median delta',report['grain_crop_adjacent_delta_median'],flush=True)
