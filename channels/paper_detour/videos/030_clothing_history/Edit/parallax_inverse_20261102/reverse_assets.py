import json,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent;src=R.parent/'parallax_75pct_20261102';t=json.loads((src/'short_final.json').read_text());clips=next(x for x in t['tracks'] if x['name']=='Scenes')['clips'];start=time.monotonic()
for i,c in enumerate(clips,1):
 inp=src/f'parallax_{i:02}.mp4';out=R/f'inverse_{i:02}.mp4';n=c['frames'][1]-c['frames'][0]+2
 subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',str(inp),'-vf','reverse','-an','-frames:v',str(n),'-c:v','libx264','-preset','veryfast','-crf','12','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
 r=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames','-of','json',str(out)],capture_output=True,text=True,check=True);v=json.loads(r.stdout)['streams'][0]
 if (int(v['nb_frames']),v['width'],v['height'],v['r_frame_rate'])!=(n,1920,1080,'30/1'):raise RuntimeError(f'{i} {v}')
 print(json.dumps({'scene':i,'frames':n,'elapsed':round(time.monotonic()-start,1)}),flush=True)
