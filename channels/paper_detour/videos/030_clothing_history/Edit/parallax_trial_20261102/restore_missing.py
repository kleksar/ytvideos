import json
import subprocess
import time
from pathlib import Path

from depthflow.scene import DepthState
from render_scene import ROOT, SHOTLIST, StrongParallax

shots = json.loads(SHOTLIST.read_text())
scene = StrongParallax(backend='headless')
started = time.monotonic()
for i in range(1, 11):
    shot = shots[i - 1]
    output = ROOT / f'scene_{i:02}.mp4'
    expected = shot['endFrame'] - shot['startFrame']
    scene.input(image=shot['framed_path'])
    scene.state = DepthState()
    scene.main(output=str(output), fps=30, time=expected / 30,
               width=1920, height=1080, quality=80, ssaa=1, turbo=False)
    probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                            '-show_entries', 'stream=width,height,r_frame_rate,nb_frames',
                            '-of', 'json', str(output)], capture_output=True, text=True, check=True)
    data = json.loads(probe.stdout)['streams'][0]
    if int(data['nb_frames']) != expected or data['r_frame_rate'] != '30/1':
        raise ValueError(f'Incorrect output for scene {i}: {data}')
    print(json.dumps({'restored': i, 'elapsed': round(time.monotonic() - started, 1)}), flush=True)
