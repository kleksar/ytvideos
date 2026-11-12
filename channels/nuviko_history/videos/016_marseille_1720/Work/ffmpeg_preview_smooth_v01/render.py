from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,subprocess,time
EP=Path('/Users/diplomat/ytvideos/stories/videos/016_marseille_1720'); W=Path(__file__).parent; C=W/'clips';C.mkdir(exist_ok=True)
scenes=json.loads((EP/'Edit/ImageMotion/sources.json').read_text()); ranges=json.loads((EP/'Work/layered_motion_v01/scene_ranges.json').read_text()); items=[]
for s,r in zip(scenes,ranges):
 if r['start']>=1800:break
 items.append((s,min(r['frames'],1800-r['start'])))
def render(pair):
 i,(s,n)=pair; out=C/f'{i:03}.mp4'; mode=i%4
 if mode<2:
  sign=1 if mode==0 else -1; e=f'{sign}*(-28.944+57.888*on/{n-1})'
  vf=f"scale=2112:1188:flags=lanczos,perspective=x0='{e}':y0=0:x1='W+({e})':y1=0:x2='{e}':y2=H:x3='W+({e})':y3=H:interpolation=cubic:eval=frame,crop=1920:1080:96:54,setsar=1,format=yuv420p"
 else:
  # Perspective maps the same single image continuously at fractional pixel precision.
  e=f'2+24*on/{n-1}' if mode==2 else f'26-24*on/{n-1}'
  y=f'({e})*H/W'
  vf=f"scale=2112:1188:flags=lanczos,perspective=x0='-({e})':y0='-({y})':x1='W+({e})':y1='-({y})':x2='-({e})':y2='H+({y})':x3='W+({e})':y3='H+({y})':interpolation=cubic:eval=frame,crop=1920:1080:96:54,setsar=1,format=yuv420p"
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-loop','1','-framerate','30','-i',s['image'],'-vf',vf,'-frames:v',str(n),'-an','-c:v','h264_videotoolbox','-b:v','14M','-pix_fmt','yuv420p',str(out)],check=True)
 return out
start=time.monotonic()
with ThreadPoolExecutor(max_workers=2) as pool:
 for f in as_completed([pool.submit(render,x) for x in enumerate(items)]):f.result()
print('Scenes rendered',round(time.monotonic()-start),flush=True)
listing=W/'clips.ffconcat';listing.write_text('ffconcat version 1.0\n'+''.join(f"file '{C/f'{i:03}.mp4'}'\n" for i in range(len(items))))
picture=W/'picture.mp4';subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(picture)],check=True)
sub=EP/'Work/ffmpeg_fast_v03/subtitles.ffconcat';audio=EP/'Source/Audio/original_narration.m4a';out=EP/'Deliverables/Nuviko_Marseille_60s_smooth_zoom_v01.mp4'
filt='[1:v]fps=30,format=rgba[sub];[0:v][sub]overlay=0:860:shortest=1:format=auto,scale=2560:1440:flags=lanczos,setsar=1,format=yuv420p[v]'
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-i',str(picture),'-f','concat','-safe','0','-i',str(sub),'-i',str(audio),'-filter_complex',filt,'-map','[v]','-map','2:a:0','-c:v','h264_videotoolbox','-b:v','20M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','60','-movflags','+faststart',str(out)],check=True)
print('COMPLETE',out,'elapsed',round(time.monotonic()-start),flush=True)
