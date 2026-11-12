import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
shots = json.loads((ROOT.parent.parent / 'Storyboard/SHOTLIST_v06.json').read_text())
for i, row in enumerate(shots[1:], 2):
    source = ROOT / f'scene_{i:02}.mp4'
    target = ROOT / f'padded_{i:02}.mp4'
    frames = row['endFrame'] - row['startFrame']
    subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', str(source),
                    '-vf', 'tpad=stop_mode=clone:stop_duration=0.1',
                    '-frames:v', str(frames + 2), '-an', '-c:v', 'libx264',
                    '-preset', 'veryfast', '-crf', '12', '-pix_fmt', 'yuv420p',
                    '-movflags', '+faststart', str(target)], check=True)
    probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                            '-show_entries', 'stream=width,height,r_frame_rate,nb_frames',
                            '-of', 'json', str(target)], capture_output=True, text=True, check=True)
    v = json.loads(probe.stdout)['streams'][0]
    if (int(v['nb_frames']), v['r_frame_rate'], v['width'], v['height']) != (frames + 2, '30/1', 1920, 1080):
        raise RuntimeError(f'Bad padded clip: {i}: {v}')
    print(f'padded {i:02}', flush=True)
