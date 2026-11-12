import json
from pathlib import Path

from PIL import Image, ImageDraw

EP = Path(__file__).resolve().parents[3]
QA = EP / 'Edit/QA/galveston-motion-v01'
OUT = QA / 'boards'
OUT.mkdir(exist_ok=False)
report = json.loads((QA / 'report.json').read_text())
paths = {r['index']: (QA / r['path']).resolve() for r in report['frame_map']}
coverage = json.loads((EP / 'Edit/Motion_v01/Palmier_QA/6C26D0C3/coverage.json').read_text())
view_map = {}


def cell(board, frame, label, x, y):
    with Image.open(paths[frame]) as im:
        im = im.convert('RGB').resize((512, 288), Image.Resampling.LANCZOS)
        board.paste(im, (x, y + 24))
    ImageDraw.Draw(board).text((x + 5, y + 5), f'{label} | final MP4 f{frame}', fill='white')


for n in range(32):
    scene_rows = coverage['scenes'][n * 4:(n + 1) * 4]
    board = Image.new('RGB', (2560, 1248), '#202020')
    indices = []
    for row, scene in enumerate(scene_rows):
        for col, frame in enumerate(scene['frames']):
            cell(board, frame, scene['id'], col * 512, row * 312)
            indices.append(frame)
    name = f'scenes_{n+1:02}.jpg'
    board.save(OUT / name, quality=94)
    view_map[name] = indices

for cue in coverage['cues']:
    board = Image.new('RGB', (1536, 1248), '#202020')
    for k, frame in enumerate(cue['frames']):
        cell(board, frame, cue['id'], k % 3 * 512, k // 3 * 312)
    # The last free cell contains the cue hold at phone scale.
    mid = cue['frames'][5]
    with Image.open(paths[mid]) as im:
        im = im.convert('RGB').resize((256, 144), Image.Resampling.LANCZOS)
        board.paste(im, (1152, 1000))
    ImageDraw.Draw(board).text((1030, 945), 'Phone-size hold, same decoded frame', fill='white')
    name = cue['id'] + '_path.jpg'
    board.save(OUT / name, quality=95)
    view_map[name] = cue['frames']

(OUT / 'board_frame_map.json').write_text(json.dumps(view_map, indent=2))
print(f'Created {len(view_map)} final-file review boards; extraction is not inspection.')
