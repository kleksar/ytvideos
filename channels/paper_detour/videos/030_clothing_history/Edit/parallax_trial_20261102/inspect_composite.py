import base64
import importlib.util
import io
import json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
CLIENT = Path('/Users/diplomat/ytvideos/automation/palmier/inspect_connection.py')
spec = importlib.util.spec_from_file_location('palmier_read', CLIENT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
conn = module.PalmierConnection()
conn.connect()
state = json.loads((ROOT / 'timeline_after.json').read_text())
scenes = next(t for t in state['tracks'] if t['name'] == 'Scenes')['clips']
for first in range(0, len(scenes), 10):
    subset = scenes[first:first + 10]
    canvas = Image.new('RGB', (1536, 308 * len(subset)), 'black')
    draw = ImageDraw.Draw(canvas)
    for row, clip in enumerate(subset):
        begin, end = clip['frames']
        result = conn.request('tools/call', {'name': 'inspect_timeline', 'arguments': {
            'projectId': 'B1BA2D18', 'timelineId': '58E4A048',
            'startFrame': begin, 'endFrame': end, 'maxFrames': 3}})
        if result.get('isError'):
            raise RuntimeError(result)
        images = [b for b in result['content'] if b.get('type') == 'image']
        if len(images) != 3:
            raise RuntimeError(f'Unexpected image count for scene {first + row + 1}')
        draw.text((4, row * 308 + 2), f'Scene {first + row + 1:02}  frames {begin}-{end}', fill='white')
        for col, block in enumerate(images):
            image = Image.open(io.BytesIO(base64.b64decode(block['data']))).convert('RGB')
            canvas.paste(image, (col * 512, row * 308 + 20))
    output = ROOT / f'composite_review_{first + 1:02}_{first + len(subset):02}.jpg'
    canvas.save(output, quality=88)
    print(str(output), flush=True)
