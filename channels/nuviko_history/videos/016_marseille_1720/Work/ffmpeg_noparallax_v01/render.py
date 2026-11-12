from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
import json,subprocess,time,sys,hashlib
EP=Path('/Users/diplomat/ytvideos/stories/videos/016_marseille_1720'); WORK=Path(__file__).resolve().parent; CLIPS=WORK/'clips'; CLIPS.mkdir(exist_ok=True)
scenes=json.loads((EP/'Edit/ImageMotion/sources.json').read_text()); ranges=json.loads((EP/'Work/layered_motion_v01/scene_ranges.json').read_text())
assert len(scenes)==len(ranges)==127
for scene,r in zip(scenes,ranges):
 assert scene['mediaRef']==r['ref'] and scene['startFrame']==r['start'] and scene['endFrame']==r['end']
 assert Path(scene['image']).is_file(),scene['image']
assert ranges[-1]['end']==16125
contract={'purpose':'user review','film':'Nuviko 016 Marseille','stills_manifest':str(EP/'Edit/ImageMotion/sources.json'),'ranges':str(EP/'Work/layered_motion_v01/scene_ranges.json'),'subtitle_overlay':str(EP/'Assets/Generated/subtitle_overlay_v01.mov'),'audio':str(EP/'Source/Audio/original_narration.m4a'),'audio_handling':'copy AAC from supplied source; no new mix','frames':16125,'fps':30,'frame_size':[2560,1440],'codec':'H.264 videotoolbox','colour':'bt709 tv','motion':'whole image only, alternating linear horizontal pans; scale 1.1; travel 4.5% width','parallax':False,'grain':'not applied to this trial','source_still_dimensions':[1672,941],'sound_highlight_listening':'unverified','expected_output':str(EP/'Deliverables/NuvikoHistory_016_Marseille_ffmpeg_no_parallax_v01.mp4')}
(WORK/'export_contract.json').write_text(json.dumps(contract,indent=2)+'\n')
start=time.monotonic()
def make(i):
 s=scenes[i]; r=ranges[i]; n=r['frames']; out=CLIPS/f"{i+1:03d}.mp4"
 if out.exists(): raise RuntimeError(f'Already exists: {out}')
 sign=1 if i%2==0 else -1
 e=f'{sign}*(-43.2+86.4*on/{n-1})'
 vf=(f"scale=2112:1188:flags=lanczos,perspective=x0='{e}':y0=0:x1='W+({e})':y1=0:x2='{e}':y2=H:x3='W+({e})':y3=H:interpolation=cubic:eval=frame,crop=1920:1080:96:54,setsar=1,format=yuv420p")
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-loop','1','-framerate','30','-i',s['image'],'-vf',vf,'-frames:v',str(n),'-an','-c:v','h264_videotoolbox','-b:v','14M','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv',str(out)]
 subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL); return out
try:
 with ThreadPoolExecutor(max_workers=2) as pool:
  futures=[pool.submit(make,i) for i in range(127)]
  for completed,f in enumerate(as_completed(futures),1):
   f.result()
   if completed%10==0 or completed==127: print(json.dumps({'stage':'scene_render','completed':completed,'total':127,'seconds':round(time.monotonic()-start,1)}),flush=True)
 concat=WORK/'scenes.ffconcat'; concat.write_text('ffconcat version 1.0\n'+''.join("file 'clips/%03d.mp4'\n"%(i+1) for i in range(127)))
 video=WORK/'picture_concat.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(concat),'-c','copy','-an',str(video)],check=True)
 print(json.dumps({'stage':'concat_done','seconds':round(time.monotonic()-start,1)}),flush=True)
 out=Path(contract['expected_output']); assert not out.exists()
 overlay=Path(contract['subtitle_overlay']); audio=Path(contract['audio'])
 filt='[0:v][1:v]overlay=shortest=1:format=auto,scale=2560:1440:flags=lanczos,setsar=1,format=yuv420p[v]'
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-i',str(video),'-i',str(overlay),'-i',str(audio),'-filter_complex',filt,'-map','[v]','-map','2:a:0','-frames:v','16125','-c:v','h264_videotoolbox','-b:v','20M','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv','-c:a','copy','-movflags','+faststart',str(out)]
 (WORK/'final_command.json').write_text(json.dumps(cmd,indent=2)+'\n')
 subprocess.run(cmd,check=True)
 print(json.dumps({'stage':'complete','output':str(out),'seconds':round(time.monotonic()-start,1)}),flush=True)
except BaseException as e:
 print(json.dumps({'stage':'failed','error':str(e),'seconds':round(time.monotonic()-start,1)}),flush=True); raise
