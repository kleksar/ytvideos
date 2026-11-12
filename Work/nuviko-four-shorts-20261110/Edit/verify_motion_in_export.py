"""Measure visible scale against the corresponding unzoomed source frames."""
from pathlib import Path
import json
import subprocess
import sys

import numpy as np
from PIL import Image

edit = Path(__file__).resolve().parent
name = sys.argv[1]
variant = 'hold' if '--hold' in sys.argv[2:] else 'sync' if '--sync' in sys.argv[2:] else 'unique' if '--unique' in sys.argv[2:] else 'dynamic'
dynamic = any(flag in sys.argv[2:] for flag in ('--dynamic','--unique','--sync','--hold'))
if dynamic:
    revision = json.loads((edit/f'{name}-{variant}-input.json').read_text())['new_revision']
else:
    revision = json.loads((edit/'beat-motion-accents.json').read_text())[name]['new_revision']
prefix = f'{name}-review-{revision}'
plan = json.loads((edit/f'{prefix}-contract.json').read_text())
qa_path = edit/f'{prefix}-qa.json'
qa = json.loads(qa_path.read_text())
width,height = 180,320

def fetch(path, frames, prefix='', seek=None):
    argv = ['ffmpeg','-v','error','-threads','1','-filter_threads','1']
    if seek is not None:
        argv += ['-ss',str(seek)]
    terms = [f'eq(n,{n})' for n in frames]
    selected = '+'.join('('+'+'.join(terms[i:i+12])+')' for i in range(0,len(terms),12))
    filters = f"{prefix}select='{selected}',scale={width}:{height}:flags=lanczos,format=gray"
    argv += ['-i',str(path),'-an','-vf',filters,'-frames:v',str(len(frames)),
             '-fps_mode','passthrough','-f','rawvideo','-']
    return np.frombuffer(subprocess.check_output(argv),np.uint8).reshape(len(frames),height,width)

def texture(data):
    data = data.astype(np.float32)
    horizontal = (data[:,2:]-data[:,:-2])[4:-4,4:-4]
    vertical = (data[2:]-data[:-2])[4:-4,5:-5]
    excluded = slice(height//2-25,height//2+25)
    horizontal[excluded] = 0
    vertical[excluded] = 0
    combined = np.concatenate((horizontal.ravel(),vertical.ravel()))
    return combined / max(np.linalg.norm(combined),1e-6)

def infer(reference, result):
    picture = Image.fromarray(reference)
    features = texture(result)
    scales = np.arange(.95,1.0601,.0025)
    scores = []
    for scale in scales:
        inv = .95 / scale
        candidate = picture.transform((width,height),Image.Transform.AFFINE,
                                      (inv,0,(1-inv)*width/2,0,inv,(1-inv)*height/2),
                                      Image.Resampling.BICUBIC)
        scores.append(float(features @ texture(np.asarray(candidate))))
    index = int(np.argmax(scores))
    return scales[index],scores[index]

frames = qa['motion_sample_frames']
final = fetch(plan['output'],frames)
measurements = []
for i,(clip,motion) in enumerate(zip(plan['clips'],plan['motion'])):
    indexes = frames[3*i:3*i+3]
    relative = [n-motion['first_frame'] for n in indexes]
    x = '(iw-ow)*0.60' if 'deer' in clip['path'] else '(iw-ow)/2'
    filters = (f"setpts=PTS-STARTPTS,{clip.get('pre_crop','')}fps=30,"
               f"scale=1440:2560:force_original_aspect_ratio=increase:flags=bicubic,"
               f"crop=1440:2560:x='{x}':y='(ih-oh)/2',format=yuv420p,eq=contrast=1.25:saturation=1.5,")
    source = fetch(clip['path'],relative,filters,clip['source_in'])
    start,end = motion['relative_scale']
    for j,(frame,n,raw) in enumerate(zip(indexes,relative,source)):
        u = n/(motion['frames']-1)
        expected = start+(end-start)*(.7*u+.3*u*u*(3-2*u))
        actual,score = infer(raw,final[3*i+j])
        measurements.append({'frame':frame,'expected':round(expected,4),'estimated':round(actual,4),'feature_match':round(score,3)})
qa['estimated_scale_samples'] = measurements
qa_path.write_text(json.dumps(qa,indent=2)+'\n')
print(name, 'max scale difference', round(max(abs(m['estimated']-m['expected']) for m in measurements),4),
      'min feature match',min(m['feature_match'] for m in measurements), flush=True)
