import json, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
shots=json.loads((ROOT.parent.parent/'Storyboard/SHOTLIST_v06.json').read_text())
t0=time.monotonic()
for i,row in enumerate(shots,1):
    frames=row['endFrame']-row['startFrame']; raw=ROOT/f'raw_{i:02}.mp4'; out=ROOT/f'parallax_{i:02}.mp4'
    if out.is_file(): raise RuntimeError(f'Refusing to overwrite {out}')
    with (ROOT/f'render_{i:02}.log').open('w') as log:
        subprocess.run(['/tmp/uv-depthflow-parallax-test/bin/python',str(ROOT/'render_scene.py'),str(i)],stdout=log,stderr=subprocess.STDOUT,check=True)
    subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',str(raw),'-vf','tpad=stop_mode=clone:stop_duration=0.1','-frames:v',str(frames+2),'-an','-c:v','libx264','-preset','veryfast','-crf','12','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
    p=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames','-of','json',str(out)],capture_output=True,text=True,check=True)
    stream=json.loads(p.stdout)['streams'][0]
    if (int(stream['nb_frames']),stream['r_frame_rate'],stream['width'],stream['height'])!=(frames+2,'30/1',1920,1080): raise RuntimeError(f'Wrong output {i}: {stream}')
    print(json.dumps({'completed':i,'total':len(shots),'elapsed':round(time.monotonic()-t0,1)}),flush=True)
