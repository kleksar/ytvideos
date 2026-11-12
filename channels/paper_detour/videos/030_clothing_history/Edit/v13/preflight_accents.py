"""Actual depth samples plus authored camera/cue geometry; not native playback."""
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
HERE = ROOT / 'Edit/v13'
run = Path(json.loads((HERE / 'TARGET_RUN.json').read_text())['run'])
plan = json.loads((run / 'plan.json').read_text())
cuefile = ROOT / 'Storyboard/CUE_SHEET_v13.json'
cues = json.loads((cuefile if cuefile.exists() else ROOT / 'Storyboard/CUE_SHEET_v13_plan.json').read_text())
source = {r['scene']: r['files'] for r in json.loads((HERE / 'QA/depth_sample_map.json').read_text())}
for r in json.loads((HERE / 'FramingPreflight/records.json').read_text()):
    source[f"V{r['scene']:02}"] = r['files']
out = HERE / 'AccentPreflight'
out.mkdir(exist_ok=True)
def value(keys, fraction):
    return [keys[0][i] + fraction * (keys[-1][i] - keys[0][i]) for i in (1, 2)]
for start in range(0, len(cues), 9):
    group = cues[start:start + 9]
    sheet = Image.new('RGB', (1440, len(group) * 294), '#ddd9cc')
    draw = ImageDraw.Draw(sheet)
    for row, cue in enumerate(group):
        scene = plan[int(cue['scene'][1:]) - 1]
        for col, fraction in enumerate([0, .5, 1]):
            with Image.open(source[cue['scene']][col]) as im:
                background = im.convert('RGB').resize((1920, 1080))
            x, y = value(scene['keyframes']['position'], fraction)
            sx, sy = value(scene['keyframes']['scale'], fraction)
            background = background.transform((1920, 1080), Image.Transform.AFFINE,
                            (1 / sx, 0, -x * 1920 / sx, 0, 1 / sy, -y * 1080 / sy),
                            resample=Image.Resampling.BICUBIC)
            pos = cue['position_keys'][0 if col == 0 else 1 if col == 1 else -1]
            with Image.open(cue['png']) as accent:
                background.paste(accent, (round(pos[1] * 1920), round(pos[2] * 1080)), accent)
            if cue['id'] in ['D06', 'D12', 'D13', 'D17', 'D18', 'D22'] and col == 1:
                background.save(out / (cue['id'] + '_hold.jpg'))
            sheet.paste(background.resize((480, 270)), (col * 480, row * 294))
            draw.text((col * 480 + 5, row * 294 + 274), cue['id'] + ' ' + cue['scene'] + ' camera ' + str(fraction), fill='black')
    sheet.save(out / f'ALL_CUES_{start // 9 + 1}.jpg')
print(str(len(cues)) + ' cue pairs at3camera and accent-path positions; actual native export verification still required')
