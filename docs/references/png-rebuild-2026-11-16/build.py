from pathlib import Path
import json,subprocess,concurrent.futures,time
R=Path(__file__).resolve().parent; B=R.parent
def run(c): subprocess.run(c,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def shot(job):
 kind,x=job;p=B/('mind-reading-video/en-dialogue1.1' if kind=='mind' else 'desire-video');i=x['id'];n=x['frames'];f=p/'frames'/f'{i}.png'
 if kind=='mind' and i=='081':f=B/'mind-frame-fix/081-no-cyan.png'
 out=R/kind/f'{i}.mkv';out.parent.mkdir(exist_ok=True)
 if out.exists(): return
 if kind=='mind':
  m={z['id']:z for z in json.load(open(p/'motion-plan.json'))}[i];mode=m['mode'];amt=min(.02,n/30*.005);cx='iw/2-iw/zoom/2';cy='ih/2-ih/zoom/2'
  if mode=='pan':
   z='1.025';travel=min(.009,n/30*.003);direction=1 if m['direction']=='left_to_right' else -1;cx=f'(iw-iw/zoom)/2+({direction})*iw*{travel}*(on/{max(n-1,1)}-0.5)'
  else:z=(f'1+{amt}*on/' if mode=='zoom_in' else f'{1+amt}-{amt}*on/')+str(max(n-1,1))
  hold=mode=='hold'
  if i=='081':z='1+0.0055*on/32';hold=False
 else:
  s={z['id']:z for z in json.load(open(p/'storyboard.json'))}[i];hold=bool(s.get('image_text')) or n<30;amt=min(.024,n/30*.006);mode=int(i)%4;u=f'on/{max(1,n-1)}';z=f'1+{amt}*{u}' if mode in (0,1) else f'{1+amt}-{amt}*{u}';cx='iw/2-iw/zoom/2';cy='ih/2-ih/zoom/2'
  if mode==3:z='1.025';cx=f'(iw-iw/zoom)/2+iw*0.006*({u}-0.5)'
 vf=f'scale=1920:1080:flags=lanczos,zoompan=z=1:x=0:y=0:d={n}:s=1920x1080:fps=30,setsar=1,format=yuv420p' if hold else f"scale=15360:8640:force_original_aspect_ratio=increase:flags=lanczos,crop=15360:8640,zoompan=z='{z}':x='{cx}':y='{cy}':d={n}:s=1920x1080:fps=30,setsar=1,format=yuv420p"
 run(['ffmpeg','-v','error','-y','-threads','1','-i',str(f),'-vf',vf,'-filter_threads','1','-frames:v',str(n),'-an','-c:v','libx264','-threads','1','-preset','ultrafast','-crf','0',str(out)])
 print(kind,i,flush=True)
jobs=[]
for kind,sub in [('mind','mind-reading-video/en-dialogue1.1'),('everyone','desire-video')]:
 t=json.load(open(B/sub/'audio/timings.json'));jobs.extend((kind,x) for x in t)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:list(ex.map(shot,jobs))
for kind,sub,intro,master,frames in [
 ('mind','mind-reading-video/en-dialogue1.1','Removing_card_to_reveal_scene_7ca19ea2_720p.mp4','mind-sound-v2/MIND_READING_FINAL_SOUND_V2_1080p30.mp4',6252),
 ('everyone','desire-video','Woman_lowering_card_revealing_scene_4ced0759_720p(1).mp4','desire-sound-v9/EVERYONE_WANTS_YOU_SOUND_V9_1080p30.mp4',6198)]:
 t=json.load(open(B/sub/'audio/timings.json'));lst=R/kind/'concat.txt';lst.write_text(''.join(f"file '{R/kind/(x['id']+'.mkv')}'\n" for x in t))
 introf="[0:v]fps=30,scale=1920:1080:flags=lanczos,setsar=1,tpad=stop_mode=clone:stop_duration=1,"
 if kind=='mind':flt=introf+"trim=end_frame=150,setpts=N/(30*TB)[i];[1:v]trim=start_frame=60,setpts=N/(30*TB)[body];[i][body]concat=n=2:v=1:a=0[v]"
 else:flt=introf+"trim=end_frame=171,setpts=N/(30*TB)[i];[1:v]split[a][b];[a]trim=start_frame=81:end_frame=437,tpad=stop_mode=clone:stop=31,setpts=N/(30*TB)[body1];[b]trim=start_frame=437,setpts=N/(30*TB)[body2];[i][body1][body2]concat=n=3:v=1:a=0[v]"
 out=R/('MIND_READING_UPLOAD_READY_1080p30.mp4' if kind=='mind' else 'EVERYONE_WANTS_YOU_UPLOAD_READY_1080p30.mp4')
 cmd=['ffmpeg','-y','-v','error','-i',str(B/'new-intros'/intro),'-f','concat','-safe','0','-i',str(lst),'-i',str(B/master),'-filter_complex',flt,'-map','[v]','-map','2:a','-c:v','libx264','-threads','4','-preset',('slow' if kind=='mind' else 'fast'),'-crf','16','-pix_fmt','yuv420p','-r','30','-frames:v',str(frames),'-c:a','copy','-movflags','+faststart',str(out)]
 (R/(kind+'-command.json')).write_text(json.dumps(cmd,indent=2));run(cmd);print('DONE',out,flush=True)
