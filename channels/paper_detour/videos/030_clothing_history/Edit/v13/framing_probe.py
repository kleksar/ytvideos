"""Addressed three-frame framing diagnosis using the existing motion renderer."""
import copy
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, '/Users/diplomat/ytvideos')
from automation.image_motion.run import prepare

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'Edit/v13/FramingProbe'
OUT.mkdir(exist_ok=True)
run = ROOT / 'Edit/ImageMotion/c1b10a33e5622a7f2c7e'
scenes = json.loads((run / 'plan.json').read_text())
config = json.loads((ROOT / 'Edit/ImageMotion/motion.json').read_text())
records = []
for n, zooms in [(16, [1.03, 1.08, 1.13]), (17, [1.03, 1.08, 1.13])]:
    for zoom in zooms:
        scene = copy.deepcopy(scenes[n - 1])
        scene['frames'] = 3
        scene['depth_zoom'] = zoom
        video = prepare(scene, config, OUT)
        image = OUT / f'V{n:02}_{zoom}.jpg'
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', video, '-frames:v', '1', str(image)], check=True)
        records.append({'scene': n, 'depth_zoom': zoom, 'video': video, 'image': str(image)})
sheet = Image.new('RGB', (1440, 588), '#ddd9cc')
draw = ImageDraw.Draw(sheet)
for i, record in enumerate(records):
    with Image.open(record['image']) as im:
        sheet.paste(im.resize((480, 270)), ((i % 3) * 480, (i // 3) * 294))
    draw.text(((i % 3) * 480 + 5, (i // 3) * 294 + 274),
              f"V{record['scene']} zoom {record['depth_zoom']}", fill='black')
sheet.save(OUT / 'FIGURE_FRAMING_OPTIONS.jpg')
(OUT / 'records.json').write_text(json.dumps(records, indent=2) + '\n')
