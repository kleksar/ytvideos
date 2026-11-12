"""Check the rendered MP4s against their accent, motion and caption contracts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image
from beat_motion_signal import analysis

sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'automation'))
from music_montage import accent_signal

edit = Path(__file__).resolve().parent
name = sys.argv[1]
variant = 'hold' if '--hold' in sys.argv[2:] else 'sync' if '--sync' in sys.argv[2:] else 'unique' if '--unique' in sys.argv[2:] else 'dynamic'
dynamic = any(flag in sys.argv[2:] for flag in ('--dynamic','--unique','--sync','--hold'))
if dynamic:
    spec = json.loads((edit / f'{name}-{variant}-input.json').read_text())
    revision = spec['new_revision']
else:
    revision = json.loads((edit / 'beat-motion-accents.json').read_text())[name]['new_revision']
prefix = f'{name}-review-{revision}'
contract = json.loads((edit / f'{prefix}-contract.json').read_text())
path = Path(contract['output'])

def command(*args):
    return subprocess.check_output([str(a) for a in args])

def audio_hash(file):
    return command('ffmpeg','-v','error','-i',file,'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-').decode().strip()

def sample(frames, resize=None, crop=None, file=path):
    terms = [f'eq(n,{n})' for n in frames]
    select = '+'.join('('+'+'.join(terms[i:i+12])+')' for i in range(0,len(terms),12))
    filters = [f"select='{select}'"]
    width, height = 1080, 1920
    if crop:
        filters.append(f'crop={crop[0]}:{crop[1]}')
        width, height = crop
    if resize:
        filters.append(f'scale={resize[0]}:{resize[1]}:flags=lanczos')
        width, height = resize
    raw = command('ffmpeg','-nostdin','-v','error','-threads','2','-i',file,'-an','-vf',','.join(filters),
                  '-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-')
    return np.frombuffer(raw,np.uint8).reshape(len(frames),height,width,3)

def sheet(samples, cols, file):
    count,h,w,_ = samples.shape
    image = Image.new('RGB',(cols*w,((count+cols-1)//cols)*h))
    for i, data in enumerate(samples):
        image.paste(Image.fromarray(data), (i%cols*w,i//cols*h))
    image.save(file,quality=91)

probe = json.loads(command('ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',path))
v,a = probe['streams']
assert (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_read_frames'])) == (1080,1920,'30/1',contract['frames'])
assert (v['color_space'],v['color_primaries'],v['color_transfer']) == ('bt709','bt709','bt709')
assert (a['codec_name'],a['channels'],a['sample_rate']) == ('aac',2,'44100')
reference = Path(contract['previous_review'])
if dynamic and not reference.is_file():
    reference = Path(spec['media'])
    assert hashlib.sha256(reference.read_bytes()).hexdigest() == contract['previous_sha256']
assert audio_hash(path) == audio_hash(reference)
subprocess.run(['ffmpeg','-nostdin','-v','error','-xerror','-threads','2','-i',path,'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True)
if dynamic:
    t,strength = accent_signal(path)
else:
    t,bands = analysis(path)
    strength = np.array([.55,.28,.10,.07])@bands
offsets = []
for mark in contract['accents']:
    n = mark['frame']
    region = np.where(abs(t-n/30)<=0.035)[0]
    if dynamic:
        j = int(np.argmin(abs(t-mark['attack_seconds'])))
        attack = float(t[j])
        assert strength[j] >= .45 and j in region
    else:
        attack = float(t[region[np.argmax(strength[region])]])
    assert abs(attack-mark['attack_seconds']) < .00001 and abs(attack-n/30) <= 1/30
    offsets.append(round(1000*(n/30-attack),2))

centres = contract['transition_centres']
total = contract['frames']
transition_frames = [n+d for n in centres for d in (-2,-1,0,1,3) if 0 <= n+d < total]
bounds = [0,*centres,total]
motion_frames = []
for i,(start,end) in enumerate(zip(bounds,bounds[1:])):
    motion_frames.extend((start+(5 if i else 0), (start+end)//2, end-(3 if i<len(centres) else 1)))
assert motion_frames == sorted(set(motion_frames))
frames = sorted(set(transition_frames + motion_frames))
samples = dict(zip(frames,sample(frames,resize=(90,160))))
sheet(np.stack([samples[n] for n in transition_frames]),5,edit/f'{prefix}-transitions.jpg')
sheet(np.stack([samples[n] for n in motion_frames]),3,edit/f'{prefix}-motion.jpg')

caption_plan = json.loads(Path(contract['mask']).with_name(Path(contract['mask']).name.replace('-mask.mov','-caption-plan.json')).read_text())
candidate_words = sorted((w for g in caption_plan['groups'] for w in g['words'] if len(w['text']) >= 3),
                         key=lambda w:len(w['text']),reverse=True)
caption_frames = []
for word in candidate_words:
    n=(word['start_frame']+word['end_frame_exclusive']-1)//2
    if all(abs(n-prev)>12 for prev in caption_frames):
        caption_frames.append(n)
    if len(caption_frames)==3:
        break
caption_frames.sort()
caption_samples = sample(caption_frames,crop=(640,240))
sheet(caption_samples,1,edit/f'{prefix}-titles.jpg')
receipt = {'file':str(path), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
           'duration_seconds':float(probe['format']['duration']), 'frames':total, 'fps':30,
           'dimensions':[1080,1920], 'full_decode':'PASS', 'audio_packet_identity':'PASS',
           'accent_frames':centres, 'frame_minus_attack_ms':offsets,
           'transition_sample_frames':transition_frames,'motion_sample_frames':motion_frames,
           'caption_sample_frames':caption_frames,'visual_inspection':'PENDING',
           'transition_duration_seconds':contract['transition_seconds'],
           'continuous_playback':'UNVERIFIED','subjective_audio_listening':'UNVERIFIED',
           'caption_status': ('full timed vocal excerpt' if dynamic and spec.get('caption_mask') else
                              'partial existing timing' if name=='super-funk' else 'existing timed lyrics')}
(edit/f'{prefix}-qa.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(path.name, offsets, flush=True)
