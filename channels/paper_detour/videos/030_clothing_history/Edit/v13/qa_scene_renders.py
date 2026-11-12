"""Extract actual depth-render samples without modifying production assets."""
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
RUN = Path(json.loads((ROOT / 'Edit/v13/TARGET_RUN.json').read_text())['run'])
OUT = ROOT / 'Edit/v13/QA'
OUT.mkdir(exist_ok=True)
plan = json.loads((RUN / 'plan.json').read_text())
videos = {}
for path in (ROOT / 'Edit/ImageMotion').glob('*/run.json'):
    record = json.loads(path.read_text())
    for row in record.get('scenes', []):
        if row.get('video') and Path(row['video']).is_file():
            key = (row['image'], row['frames'], row['sign'], row['depth_zoom'])
            videos[key] = row['video']
for path in (ROOT / 'Edit/ImageMotion').glob('*/*.job.json'):
    job = json.loads(path.read_text())
    video = Path('/Users/diplomat/ytvideos/Shared/Image_Motion/Cache/video') / (path.name.removesuffix('.job.json') + '.mp4')
    if video.is_file():
        videos[(job['image'], job['frames'], job['sign'], job['depth_zoom'])] = str(video)
records = []
for index, scene in enumerate(plan, 1):
    key = (scene['image'], scene['frames'], scene['sign'], scene['depth_zoom'])
    video = videos.get(key)
    if not video:
        continue
    folder = OUT / 'SceneRenders' / (f'V{index:02}_' + Path(video).stem[:12])
    folder.mkdir(parents=True, exist_ok=True)
    samples = [0, scene['frames'] // 2, scene['frames'] - 1]
    if not all((folder / f'{n:02}.jpg').is_file() for n in range(1, 4)):
        expression = '+'.join(f'eq(n\\,{n})' for n in samples)
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-xerror', '-i', video,
                        '-vf', 'select=' + expression, '-fps_mode', 'vfr', '-an',
                        '-q:v', '3', str(folder / '%02d.jpg')], check=True)
    records.append({'scene': f'V{index:02}', 'video': video, 'sample_frames': samples,
                    'files': [str(folder / f'{n:02}.jpg') for n in range(1, 4)]})
for start in range(0, 39, 13):
    group = [r for r in records if start < int(r['scene'][1:]) <= start + 13]
    if not group:
        continue
    sheet = Image.new('RGB', (1440, len(group) * 294), '#ddd9cc')
    draw = ImageDraw.Draw(sheet)
    for row, record in enumerate(group):
        for col, file in enumerate(record['files']):
            with Image.open(file) as im:
                sheet.paste(im.resize((480, 270)), (col * 480, row * 294))
            draw.text((col * 480 + 5, row * 294 + 274),
                      f"{record['scene']} frame {record['sample_frames'][col]}", fill='black')
    sheet.save(OUT / f'DEPTH_SCENES_{start // 13 + 1}.jpg')
(OUT / 'depth_sample_map.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps({'depth_scenes_sampled': len(records), 'frames_per_scene': 3}))
