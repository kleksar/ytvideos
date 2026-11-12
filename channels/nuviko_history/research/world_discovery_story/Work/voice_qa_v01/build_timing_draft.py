#!/usr/bin/env python3
"""Create review-only scene boundaries from forced alignment; do not assert accuracy."""
import hashlib, json, re
from pathlib import Path

root = Path(__file__).resolve().parents[2]
work = Path(__file__).resolve().parent
raw = json.loads((work / 'forced_blocks_raw.json').read_text())
audio = root / 'Source/Voice/voice_en.mp3'
source = root / 'Source/Voice/narration-en-v01.txt'
assert hashlib.sha256(audio.read_bytes()).hexdigest() == raw['audio_sha256']
assert hashlib.sha256(source.read_text().strip().encode()).hexdigest() == raw['text_sha256']
blocks = re.split(r'\n\s*\n', source.read_text().strip())
words = raw['result']['word_segments']
assert len(blocks) == 89 and len(words) == sum(len(x.split()) for x in blocks)
norm = lambda s: re.sub(r'[^\w]', '', s.casefold())
assert all(norm(a) == norm(b['word']) for a, b in zip(source.read_text().split(), words))
spans, cursor = [], 0
for idx, text in enumerate(blocks, 1):
    n = len(text.split()); selected = words[cursor:cursor+n]; cursor += n
    spans.append({'id': f'N{idx:03}', 'text': text, 'speech_start': selected[0]['start'], 'speech_end': selected[-1]['end']})
cuts = [0.0]
for a, b in zip(spans, spans[1:]):
    cuts.append(round((a['speech_end'] + b['speech_start']) / 2, 3))
cuts.append(483.76)
for i, block in enumerate(spans):
    block['cut_in'], block['cut_out'] = cuts[i:i+2]
    block['duration'] = round(cuts[i+1] - cuts[i], 3)
    block['status'] = 'REVIEW_OVERLAP' if i and spans[i-1]['speech_end'] > block['speech_start'] else ('RETIME' if not 4 <= block['duration'] <= 6 else 'DRAFT')
result = {'status': 'DRAFT: forced alignment and cut placement are not manually listened or accepted', 'audio_sha256': raw['audio_sha256'], 'text_sha256': raw['text_sha256'], 'method': 'midpoint between forced-aligned block endpoints; no sound or frames were edited', 'blocks': spans}
(work / 'scene_boundaries_forced_DRAFT.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print('scenes', len(spans), 'retime', sum(x['status']=='RETIME' for x in spans), 'overlap', sum(x['status']=='REVIEW_OVERLAP' for x in spans))
