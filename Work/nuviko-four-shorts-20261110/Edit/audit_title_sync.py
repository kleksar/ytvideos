"""Check every word interval and every accent against the new mask and the exact MP4."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

edit = Path(__file__).resolve().parent
repo = edit.parents[2]
sys.path.insert(0, str(repo/'automation/captions'))
from music_lyrics import load_words

name = sys.argv[1]
variant = 'hold' if '--hold' in sys.argv[2:] else 'sync'
spec = json.loads((edit/f'{name}-{variant}-input.json').read_text())
revision = spec['new_revision']
prefix = f'{name}-review-{revision}'
contract = json.loads((edit/f'{prefix}-contract.json').read_text())
prior = json.loads((edit/f"{name}-review-{spec['old_revision']}-contract.json").read_text())
receipt = edit/f'{prefix}-qa.json'
qa = json.loads(receipt.read_text())
mp4 = Path(qa['file'])
assert hashlib.sha256(mp4.read_bytes()).hexdigest() == qa['sha256']
for key in ('clips','motion','transition_centres','transition_seconds','source','source_sha256','frames','fps','offset'):
    assert contract[key] == prior[key], key
fps, frames = contract['fps'], contract['frames']
caption = json.loads((edit/f'{prefix}-caption-plan.json').read_text())
beat_map = json.loads((edit/f'{prefix}-caption-beats.json').read_text())
beats = {x['frame'] for x in beat_map['candidates']}
cuts = set(contract['transition_centres'])
source = load_words(json.loads(Path(spec['caption_source_words']).read_text()), contract['offset'], fps, frames,
                    keep_source_times=(variant == 'hold'))
groups = caption['groups']
assert len(source) == len(groups)
mask = Path(contract['mask'])
assert hashlib.sha256(mask.read_bytes()).hexdigest() == contract['mask_sha256']

raw = subprocess.check_output(['ffmpeg','-v','error','-i',str(mask),'-vf','format=gbrp,extractplanes=g,scale=112:48',
                               '-pix_fmt','gray','-f','rawvideo','-'])
activity = np.frombuffer(raw,np.uint8).reshape(frames,-1).max(axis=1)>20
expected = np.zeros(frames,dtype=bool)
frame_samples = []
pulse_at_cuts = set()
by_word = []
held_gap_samples, blank_gap_samples = set(), set()
if variant == 'hold':
    assert caption['hold_gap_lt_ms'] == 500
for index,(src,group) in enumerate(zip(source,groups)):
    start,stop = group['start_frame'],group['end_frame_exclusive']
    word, = group['words']
    assert word['text'] == src['text']
    assert start == word['start_frame'] and abs(start-src['start_frame'])<=1
    assert 0 <= start < stop <= frames and not expected[start:stop].any()
    assert start == src['start_frame'] or start in beats
    assert set(group['pulse_beats']) <= beats
    assert all(start<=f<stop for f in group['pulse_beats'])
    if variant == 'hold':
        next_group = groups[index+1] if index+1<len(groups) else None
        next_start = next_group['start_frame'] if next_group else frames
        natural_stop = min(word['end_frame_exclusive'],next_start)
        assert natural_stop == group['natural_end_frame_exclusive']
        gap_ms = round(1000*(source[index+1]['source_start_seconds']-src['source_end_seconds']),6) if next_group else None
        short = gap_ms is not None and 0 <= gap_ms < 500
        assert stop == (next_start if short else natural_stop), (index,gap_ms,natural_stop,stop,next_start)
        assert group['held_gap_frames'] == stop-natural_stop
        if stop>natural_stop:
            held_gap_samples.add((natural_stop+stop-1)//2)
        if next_group and stop<next_start:
            blank_gap_samples.add((stop+next_start-1)//2)
    expected[start:stop]=True
    pulse_at_cuts.update(cuts.intersection(group['pulse_beats']))
    frame_samples.append((start+stop-1)//2)
    by_word.append({'source_start_frame':src['start_frame'],'screen_start_frame':start,
                    'screen_end_exclusive_frame':stop,'pulse_frames':group['pulse_beats']})
assert np.array_equal(activity,expected)
assert pulse_at_cuts=={f for f in cuts if activity[f]}
chosen = sorted(set(frame_samples) | pulse_at_cuts | held_gap_samples | blank_gap_samples)
terms=[f'eq(n,{f})' for f in chosen]
expr='+'.join('('+'+'.join(terms[i:i+10])+')' for i in range(0,len(terms),10))
raw = subprocess.check_output(['ffmpeg','-v','error','-threads','2','-i',str(mp4),'-an','-vf',
                               f"select='{expr}',crop=720:240,scale=162:54",
                               '-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','-'])
samples=np.frombuffer(raw,np.uint8).reshape(len(chosen),54,162,3)
columns=6
sheet=Image.new('RGB',(162*columns,70*((len(chosen)+columns-1)//columns)),'#202020')
draw=ImageDraw.Draw(sheet)
for i,(frame,sample) in enumerate(zip(chosen,samples)):
    x,y=162*(i%columns),70*(i//columns)
    sheet.paste(Image.fromarray(sample),(x,y))
    draw.text((x+3,y+55),str(frame)+(' beat' if frame in pulse_at_cuts else '')+(' held' if frame in held_gap_samples else ' blank' if frame in blank_gap_samples else ''),fill='white')
sheet_path=edit/f'{prefix}-vocal-beat-frames.jpg'
sheet.save(sheet_path,quality=92)

qa['vocal_sync']={'verified_mask_frames':frames,'words':len(groups),
                   'starts_moved':sum(x['source_start_frame']!=x['screen_start_frame'] for x in by_word),
                   'starts_on_measured_beat':sum(x['screen_start_frame'] in beats for x in by_word),
                   'cut_accents_with_visible_word':len(pulse_at_cuts),'total_cut_accents':len(cuts),
                   'on_screen_words':by_word,'samples':str(sheet_path)}
if variant == 'hold':
    qa['vocal_sync'].update(
        held_gaps=sum(g['held_gap_frames']>0 for g in groups),
        held_gap_frames=sum(g['held_gap_frames'] for g in groups),
        blank_gaps=len(blank_gap_samples),
        gap_threshold_ms_exclusive=caption['hold_gap_lt_ms'],
        word_map=str(spec['caption_source_words']))
receipt.write_text(json.dumps(qa,indent=2)+'\n')
print(name, {k:v for k,v in qa['vocal_sync'].items() if isinstance(v,int)},flush=True)
