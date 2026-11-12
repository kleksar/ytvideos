"""Build a fresh title overlay on each approved video and audio timeline."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

edit = Path(__file__).resolve().parent
root = edit.parent
repo = root.parents[1]
sys.path.insert(0, str(repo/'automation'))
from music_montage import accent_signal, candidate_accents

name = sys.argv[1]
hold = '--hold' in sys.argv[2:]
variant = 'hold' if hold else 'sync'
spec = json.loads((edit/f"{name}-{'sync' if hold else 'unique'}-input.json").read_text())
old = spec['new_revision']
revision = f'v{int(old[1:])+1:02}'
prior = json.loads((edit/f'{name}-review-{old}-contract.json').read_text())
source_mask = Path(prior['mask'])
word_map = source_mask.with_name(source_mask.name.replace('-mask.mov','-words.json'))
if hold:
    word_map = (edit/f'{name}-review-{revision}-words.json') if name == 'bloodstream' else Path(spec['caption_source_words'])
prior_qa = json.loads((edit/f'{name}-review-{old}-qa.json').read_text())
source_plan = json.loads(source_mask.with_name(source_mask.name.replace('-mask.mov','-caption-plan.json')).read_text())
assert prior['output'] == prior_qa['file']
media = Path(prior['output'])
assert hashlib.sha256(media.read_bytes()).hexdigest() == prior_qa['sha256']
centres = prior['transition_centres']
fps = prior['fps']
frames = prior['frames']
prefix = f'{name}-review-{revision}'
cuts = edit/f'{prefix}-caption-cuts.json'
beats = edit/f'{prefix}-caption-beats.json'
mask = edit/f'{prefix}-mask.mov'
plan = edit/f'{prefix}-caption-plan.json'
timeline = edit/f'{name}-{variant}-timeline.json'
cuts.write_text(json.dumps({'fps':fps,'cut_frames':centres},indent=2)+'\n')
times, strength = accent_signal(media)
pulse = spec.get('pulse')
events = candidate_accents(times,strength,fps,pulse) if pulse else {}
events.update({m['frame']:m for m in prior['accents']})
beats.write_text(json.dumps({'fps':fps,'candidates':list(events.values())},indent=2)+'\n')
timeline.write_text(json.dumps({'accents':prior['accents'],'clips':prior['clips']},indent=2)+'\n')
subprocess.run([
    sys.executable,str(repo/'automation/captions/music_lyrics.py'),str(word_map),
    '--font','/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf',
    '--font-size',str(source_plan['font_size_px']),'--output',str(mask),'--plan',str(plan),
    '--offset',str(prior['offset']),'--frames',str(frames),'--fps',str(fps),
    '--invert-masks','--max-words','1','--tilt-every',str(source_plan['line_motion']['tilt_every']),
    '--motion-seed',str(source_plan['line_motion']['seed']),
    '--beats',str(beats),'--cuts',str(cuts),'--vocal-beat',
],check=True)
new_plan = json.loads(plan.read_text())
if not (hold and name == 'bloodstream'):
    assert [g['words'][0]['text'] for g in new_plan['groups']] == [g['words'][0]['text'] for g in source_plan['groups']]
spec.update(old_revision=old,new_revision=revision,media=str(media),media_sha256=prior_qa['sha256'],
            caption_mask=str(mask),caption_mask_sha256=hashlib.sha256(mask.read_bytes()).hexdigest(),
            caption_source_words=str(word_map),caption_source_plan=str(source_mask.with_name(source_mask.name.replace('-mask.mov','-caption-plan.json'))))
(edit/f'{name}-{variant}-input.json').write_text(json.dumps(spec,indent=2)+'\n')
print(name,len(new_plan['groups']),len(new_plan['beat_snaps']),sum(len(g['pulse_beats']) for g in new_plan['groups']),flush=True)
