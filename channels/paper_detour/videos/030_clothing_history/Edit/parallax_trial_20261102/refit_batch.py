"""Re-render with a wider DepthFlow view and swap into the isolated timeline."""
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT, TIMELINE = 'B1BA2D18', '58E4A048'
shots = json.loads((ROOT.parent.parent / 'Storyboard/SHOTLIST_v06.json').read_text())
before = json.loads((ROOT / 'timeline_after.json').read_text())
old = next(t for t in before['tracks'] if t['name'] == 'Scenes')['clips']
spec = importlib.util.spec_from_file_location('palmier_read', '/Users/diplomat/ytvideos/automation/palmier/inspect_connection.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
conn = m.PalmierConnection()
conn.connect()


def call(name, arguments):
    result = conn.request('tools/call', {'name': name, 'arguments': arguments})
    with (ROOT / 'refit_receipts.jsonl').open('a') as out:
        out.write(json.dumps({'name': name, 'arguments': arguments, 'response': result}, ensure_ascii=False) + '\n')
    if result.get('isError'):
        raise RuntimeError(f'{name}: {result}')
    return json.loads(result['content'][0]['text'])


start = time.monotonic()
for n, (shot, original) in enumerate(zip(shots, old), 1):
    if n == 18:
        continue  # already replaced and visually checked
    nframes = shot['endFrame'] - shot['startFrame']
    raw = ROOT / f'wide_{n:02}.mp4'
    padded = ROOT / f'widepad_{n:02}.mp4'
    if n != 1:
        with (ROOT / f'wide_{n:02}.log').open('w') as log:
            subprocess.run([sys.executable, str(ROOT / 'render_scene.py'), str(n), '1.15'],
                           stdout=log, stderr=subprocess.STDOUT, check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-y', '-i', str(raw),
                    '-vf', 'tpad=stop_mode=clone:stop_duration=0.1', '-frames:v', str(nframes + 2),
                    '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12',
                    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(padded)], check=True)
    probe = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                            'stream=width,height,r_frame_rate,nb_frames', '-of', 'json', str(padded)],
                           capture_output=True, text=True, check=True)
    stream = json.loads(probe.stdout)['streams'][0]
    if (int(stream['nb_frames']), stream['r_frame_rate'], stream['width'], stream['height']) != (nframes + 2, '30/1', 1920, 1080):
        raise ValueError(f'Wrong clip format: {n}, {stream}')
    current = conn.read_tool('get_timeline', {'projectId': PROJECT, 'timelineId': TIMELINE})
    clip = next(t for t in current['tracks'] if t['name'] == 'Scenes')['clips'][n-1]
    for field in ('id', 'frames', 'mediaRef', 'keyframes'):
        if clip.get(field) != original.get(field):
            raise RuntimeError(f'Scene {n} changed in {field}; inspect before continuing')
    imported = call('import_media', {'projectId': PROJECT, 'source': {'path': str(padded)}, 'folder': 'Parallax refit'})
    result = call('swap_clip_media', {'projectId': PROJECT, 'timelineId': TIMELINE,
                                      'clipId': clip['id'], 'mediaRef': imported['mediaRef']})
    if result.get('changed') is not True:
        raise RuntimeError(f'Swap did not change scene {n}')
    print(json.dumps({'completed': n, 'elapsed': round(time.monotonic()-start, 1)}), flush=True)

state = conn.read_tool('get_timeline', {'projectId': PROJECT, 'timelineId': TIMELINE})
final = next(t for t in state['tracks'] if t['name'] == 'Scenes')['clips']
for a, b in zip(old, final):
    if a['frames'] != b['frames'] or a.get('keyframes') != b.get('keyframes'):
        raise RuntimeError('Timing or camera keyframes changed')
for name in ('Accents', 'Grain', 'Mix'):
    if next(t for t in before['tracks'] if t['name'] == name) != next(t for t in state['tracks'] if t['name'] == name):
        raise RuntimeError(f'Unexpected change to {name}')
(ROOT / 'timeline_after_refit.json').write_text(json.dumps(state, ensure_ascii=False, indent=2))
print(json.dumps(call('manage_snapshots', {'projectId': PROJECT, 'timelineId': TIMELINE,
                                           'action': 'save', 'name': 'Parallax refit with original camera keys'})), flush=True)
