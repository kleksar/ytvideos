"""Compose still scene states from one immutable background and generated cutouts.

No text is created here. FFmpeg only scales and positions generated assets.
"""
from pathlib import Path
import subprocess

episode = Path(__file__).resolve().parent.parent
source = episode / 'Source/Images/v18'
out = episode / 'Assets/Generated/v18'
out.mkdir(parents=True, exist_ok=True)

slots = [(600, 510, 300), (640, 600, 320), (675, 690, 340),
         (710, 780, 360), (745, 870, 380), (785, 970, 400)]
states = {
    'hook': (['senior', 'woman', 'glasses', 'redhead', 'suit'], True, 'choice'),
    'join': (['senior', 'woman', 'glasses', 'redhead', 'suit'], True, 'queue'),
    'one': (['woman', 'glasses', 'redhead', 'suit'], True, 'queue'),
    'two': (['glasses', 'redhead', 'suit'], True, 'queue'),
    'payment': (['payment', 'redhead', 'suit'], True, 'queue'),
    'result': (['suit'], False, 'queue'),
}

for name, (queue, carts, hero) in states.items():
    layers = []
    if carts:
        layers.append(('left', 40, 500, 500))
    for index, person in enumerate(queue):
        x, y, height = slots[index]
        layers.append((person, x, y, height))
    layers.append(('hero', 400, 1040, 410) if hero == 'choice'
                  else ('hero', *slots[len(queue)]))
    cmd = ['ffmpeg', '-v', 'error', '-n', '-i', str(source / 'background.png')]
    for person, *_ in layers:
        cmd += ['-i', str(source / f'{person}.png')]
    filters = ['[0:v]scale=1080:1920:flags=lanczos[base]']
    previous = 'base'
    for i, (_, x, y, height) in enumerate(layers, 1):
        filters += [f'[{i}:v]scale=-1:{height}:flags=lanczos[layer{i}]',
                    f'[{previous}][layer{i}]overlay={x}:{y}:format=auto[state{i}]']
        previous = f'state{i}'
    cmd += ['-filter_complex', ';'.join(filters), '-map', f'[{previous}]',
            '-frames:v', '1', '-update', '1', str(out / f'{name}.png')]
    subprocess.run(cmd, check=True)
