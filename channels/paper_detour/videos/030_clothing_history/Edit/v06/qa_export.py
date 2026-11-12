import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter

ROOT=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history')
film=ROOT/'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v06.mp4'
qa=ROOT/'Edit/v06/QA';qa.mkdir(exist_ok=True)
staging=json.loads((ROOT/'Edit/v06/RAM_STAGING.json').read_text())
raw=qa/'Frames';raw.mkdir(exist_ok=True)
shots=json.loads((ROOT/'Storyboard/SHOTLIST_v06.json').read_text())
cues=json.loads((ROOT/'Storyboard/CUE_SHEET_v06.json').read_text())
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(film)]))
(qa/'ffprobe.json').write_text(json.dumps(probe,indent=2))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert (v['width'],v['height'],v['r_frame_rate'],v['nb_frames'])==(1920,1080,'30/1','5700')
assert float(probe['format']['duration'])==190
assert a['channels']==2 and a['sample_rate']=='48000'
assert all(120<=s['endFrame']-s['startFrame']<=180 for s in shots)
assert shots[0]['startFrame']==0 and shots[-1]['endFrame']==5700
assert all(x['endFrame']==y['startFrame'] for x,y in zip(shots,shots[1:]))
frames=set()
for s in shots:frames.update([s['startFrame']+2,s['endFrame']-3])
for c in cues:frames.update([c['startFrame']+1,c['startFrame']+4,(c['startFrame']+c['endFrame'])//2,c['endFrame']-5,c['endFrame']-1])
frames=sorted(frames)
def balanced_sum(terms):
    if len(terms)==1:return terms[0]
    middle=len(terms)//2
    return '('+balanced_sum(terms[:middle])+'+'+balanced_sum(terms[middle:])+')'
expr=balanced_sum(['eq(n,%d)'%f for f in frames]).replace(',',r'\,')
subprocess.run(['ffmpeg','-y','-v','error','-xerror','-i',str(film),'-vf','select='+expr,'-fps_mode','vfr','-q:v','3','-an',str(raw/'frame_%03d.jpg')],check=True)
files=sorted(raw.glob('frame_*.jpg'));assert len(files)==len(frames)
fmap={str(f):str(p) for f,p in zip(frames,files)}
(qa/'frame_map.json').write_text(json.dumps(fmap,indent=2))

def thumb(canvas,filename,x,y,label,w=480,h=270):
    im=Image.open(filename).resize((w,h),Image.Resampling.LANCZOS)
    canvas.paste(im,(x,y));ImageDraw.Draw(canvas).text((x+5,y+h+3),label,fill='black')

motion=[]
for index in range(0,39,13):
    group=shots[index:index+13];sheet=Image.new('RGB',(960,len(group)*294),'#ddd9cc')
    for row,s in enumerate(group):
        x,y=s['startFrame']+2,s['endFrame']-3
        thumb(sheet,fmap[str(x)],0,row*294,s['id']+' first')
        thumb(sheet,fmap[str(y)],480,row*294,s['id']+' last '+s['camera_motion'])
        aa=np.asarray(Image.open(fmap[str(x)]).convert('L').filter(ImageFilter.GaussianBlur(5)),dtype=float)
        bb=np.asarray(Image.open(fmap[str(y)]).convert('L').filter(ImageFilter.GaussianBlur(5)),dtype=float)
        motion.append({'scene':s['id'],'first_last_blurred_mean_abs_difference':float(np.abs(aa-bb).mean())})
    sheet.save(qa/f'SCENE_MOTION_{index//13+1}.jpg')
for index in range(0,34,9):
    group=cues[index:index+9];sheet=Image.new('RGB',(1536,len(group)*240),'#ddd9cc')
    for row,c in enumerate(group):
        fs=[c['startFrame']+1,c['startFrame']+4,c['endFrame']-5,c['endFrame']-1]
        for col,f in enumerate(fs):thumb(sheet,fmap[str(f)],384*col,row*240,c['id']+' f'+str(f),384,216)
    sheet.save(qa/f'CUE_MOTION_{index//9+1}.jpg')

def stream_hash(path,selector):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map',selector,'-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
video_native=stream_hash(ROOT/'Edit/v06/Palmier_export.mp4','0:v:0');video_final=stream_hash(film,'0:v:0')
audio_old=stream_hash(ROOT/'Source/Audio/v06/accepted_v05_mix.m4a','0:a:0');audio_new=stream_hash(film,'0:a:0')
assert video_native==video_final and audio_old==audio_new
srt=ROOT/'Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v06.srt'
assert srt.read_bytes()==(ROOT/'Edit/v05/Accepted_delivery_v05.srt').read_bytes()
report={'file':str(film),'sha256':hashlib.sha256(film.read_bytes()).hexdigest(),'duration':190,
        'full_video_decode':'PASS with -xerror; all5700frames traversed while selecting actual export samples',
        'scenes':39,'shot_duration_coverage':'PASS, unchanged4–6seconds,190s total',
        'paper_accents':34,'actual_exported_frames_sampled':len(frames),
        'camera_motion':motion,'new_video_payload_identical_to_native':video_final,
        'accepted_v05_audio_payload_preserved':audio_new,'srt':'Identical to accepted v05 speech timing; no voice/speed/cut changes',
        'audio_actual_bitrate':int(a['bit_rate']),'audio_48k_stereo':True,
        'visual_author_review':'PENDING actual samples inspection','full_1x_with_sound':'UNVERIFIED',
        'subjective_listening':'UNVERIFIED; accepted v05 audio reused bit-for-bit',
        'independent_review':'NOT_PERFORMED'}
(qa/'REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['duration','scenes','paper_accents','actual_exported_frames_sampled','audio_actual_bitrate']},ensure_ascii=False))
