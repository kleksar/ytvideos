"""Short geometry previews; production duration/resolution remain unchanged."""
import copy
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, '/Users/diplomat/ytvideos')
from automation.image_motion.run import prepare

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Edit/v13/FramingPreflight'
OUT.mkdir(exist_ok=True)
scenes = json.loads((ROOT / 'Edit/ImageMotion/c1b10a33e5622a7f2c7e/plan.json').read_text())
config = json.loads((ROOT / 'Edit/ImageMotion/motion.json').read_text())
changes = {16: 1.06, 17: 1.08, **{n: 1.03 for n in range(19, 31)}, 27: 1.08, 29: 1.15, 31: 1.08, 35: 1.03}
records = []
for n in range(16, 40):
    scene = copy.deepcopy(scenes[n - 1])
    scene.update(frames=12, width=960, height=540)
    scene['depth_zoom'] = changes.get(n, scene['depth_zoom'])
    video = prepare(scene, config, OUT)
    folder = OUT / f'V{n:02}'
    folder.mkdir(exist_ok=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', video,
                    '-vf', r'select=eq(n\,0)+eq(n\,6)+eq(n\,11)',
                    '-fps_mode', 'vfr', '-frames:v', '3', str(folder / '%02d.jpg')], check=True)
    records.append({'scene': n, 'depth_zoom': scene['depth_zoom'], 'video': video,
                    'files': [str(folder / f'{i:02}.jpg') for i in range(1, 4)]})
    print('framing preflight', n, flush=True)
for start in range(0, len(records), 8):
    group = records[start:start + 8]
    sheet = Image.new('RGB', (1440, len(group) * 294), '#ddd9cc')
    draw = ImageDraw.Draw(sheet)
    for row, record in enumerate(group):
        for col, file in enumerate(record['files']):
            with Image.open(file) as im:
                sheet.paste(im.resize((480, 270)), (col * 480, row * 294))
            draw.text((col * 480 + 5, row * 294 + 274),
                      f"V{record['scene']} zoom {record['depth_zoom']} {'start mid end'.split()[col]}", fill='black')
    sheet.save(OUT / f'FRAMING_{start // 8 + 1}.jpg')
(OUT / 'records.json').write_text(json.dumps(records, indent=2) + '\n')
(OUT / 'changes.json').write_text(json.dumps(changes, indent=2) + '\n')
