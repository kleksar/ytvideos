#!/usr/bin/env python3
"""Build full phrase SRT using observed ASR spans, pending listening review."""
import csv
import difflib
import json
import re
import sys
import textwrap
from pathlib import Path

from align_script import HERE, SOURCE, TOKEN, pieces, stamp

data = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
src = [m.group(0) for m in TOKEN.finditer(SOURCE.read_text(encoding='utf-8'))]
raw = [w for seg in data['segments'] for w in seg.get('words', [])]
a = [(p, i) for i, s in enumerate(src) for p in pieces(s)]
b = [(p, i) for i, w in enumerate(raw) for p in pieces(w['word'])]
parent = list(range(len(src) + len(raw)))
def find(n):
    while parent[n] != n:
        parent[n] = parent[parent[n]]
        n = parent[n]
    return n
def union(nodes):
    if nodes:
        root = find(nodes[0])
        for n in nodes[1:]: parent[find(n)] = root

matcher = difflib.SequenceMatcher(None, [x[0] for x in a], [x[0] for x in b], autojunk=False)
replacements = []
for tag, i, j, k, l in matcher.get_opcodes():
    if tag == 'equal':
        for x, y in zip(range(i, j), range(k, l)):
            union([a[x][1], len(src)+b[y][1]])
    elif tag == 'replace':
        sids = sorted(set(x[1] for x in a[i:j]))
        aids = sorted(set(x[1] for x in b[k:l]))
        union(sids + [len(src)+z for z in aids])
        replacements.append({'approved': ' '.join(src[z] for z in sids), 'asr': ''.join(raw[z]['word'] for z in aids).strip(), 'start': min(raw[z]['start'] for z in aids), 'end': max(raw[z]['end'] for z in aids), 'review': 'ASR disagreement: review actual voice'})
    else:
        raise SystemExit(f'{tag}: source and/or ASR have unpaired words. Review before building a complete SRT.')

groups = {}
for i in range(len(src)):
    groups.setdefault(find(i), {'src': [], 'asr': []})['src'].append(i)
for i in range(len(raw)):
    if not pieces(raw[i]['word']):
        continue
    root = find(len(src)+i)
    if root not in groups:
        raise SystemExit(f'ASR word without source: {raw[i]}')
    groups[root]['asr'].append(i)
groups = sorted(groups.values(), key=lambda g: g['src'][0])
flatten = [i for g in groups for i in g['src']]
if flatten != list(range(len(src))):
    raise SystemExit('Source word order is not one-to-one or consecutive; review required.')
for g in groups:
    if not g['asr']:
        raise SystemExit(f"No observed ASR time for source words: {g['src']}")
    g['start'] = min(raw[i]['start'] for i in g['asr'])
    g['end'] = max(raw[i]['end'] for i in g['asr'])
    g['text'] = ' '.join(src[i] for i in g['src'])

# Merge zero-length units with adjacent measured speech; never assert a separate
# boundary for the degenerate word. Record the merged units for reviewer.
merged_zero = []
pos = 0
while pos < len(groups):
    g = groups[pos]
    if g['end'] <= g['start']:
        if pos == 0:
            other = groups[1]
            other['src'] = g['src'] + other['src']
            other['text'] = g['text'] + ' ' + other['text']
            other['start'] = min(g['start'], other['start'])
        else:
            other = groups[pos-1]
            other['src'] += g['src']
            other['text'] += ' ' + g['text']
            other['end'] = max(other['end'], g['end'])
        merged_zero.append({'word': g['text'], 'asr_time': g['start'], 'merged_with': other['text']})
        del groups[pos]
    else:
        pos += 1
for x, y in zip(groups, groups[1:]):
    if x['end'] > y['start']:
        raise SystemExit(f"Overlapping ASR spans: {x['text']} / {y['text']}")

cues, current = [], []
def flush():
    if current:
        cues.append(current[:]); current.clear()
for g in groups:
    combined = ' '.join(x['text'] for x in current+[g])
    lines = textwrap.wrap(combined, 42, break_long_words=False, break_on_hyphens=False)
    if current and (len(lines)>2 or g['end']-current[0]['start']>6 or g['start']-current[-1]['end']>.8):
        flush()
    current.append(g)
    if re.search(r'[.!?]$',g['text']) and g['end']-current[0]['start']>=1:
        flush()
flush()
# Rebalance a very short or fast final fragment with the preceding cue, using
# only already observed unit boundaries. This avoids a one-word flash at 06:16.
for i in range(1, len(cues)):
    prev, cur = cues[i-1], cues[i]
    def cps(cue):
        return len(' '.join(g['text'] for g in cue)) / max(.001, cue[-1]['end']-cue[0]['start'])
    while len(prev) > 1 and (cur[-1]['end']-cur[0]['start'] < .75 or cps(cur) > 20):
        candidate = [prev[-1]] + cur
        candidate_text = ' '.join(g['text'] for g in candidate)
        lines = textwrap.wrap(candidate_text, 42, break_long_words=False, break_on_hyphens=False)
        if len(lines) > 2 or candidate[-1]['end']-candidate[0]['start'] > 6 or prev[-2]['end']-prev[0]['start'] < 1:
            break
        cur.insert(0, prev.pop())
# Reviewed against 50 ms RMS windows of the *voice source*. In three cases
# the MPS subtitle switched inside the still-audible tail of the previous
# sentence. Move only the phrase boundary to the CPU estimate and extend the
# previous phrase into its measured tail. Two more start inside long digital
# silence; move closer to the measured onset. These are cue adjustments, never
# claims about exact individual word boundaries, and are NOT listening review.
waveform_adjustments = [
    {'cue': 24, 'boundary': 'end',   'expected': 'slavery.', 'new': 106.50, 'reason': 'voice tail remains measurable after 106.28; silence follows'},
    {'cue': 25, 'boundary': 'start', 'expected': 'Pompeii',  'new': 106.88, 'reason': 'CPU boundary; new voice onset after a silent gap'},
    {'cue': 61, 'boundary': 'end',   'expected': 'cross.',   'new': 269.94, 'reason': 'voice tail remains measurable after 269.72; silence follows'},
    {'cue': 62, 'boundary': 'start', 'expected': 'What',     'new': 270.24, 'reason': 'CPU boundary; new voice onset after a silent gap'},
    {'cue': 67, 'boundary': 'end',   'expected': 'structure.', 'new': 295.88, 'reason': 'voice tail remains measurable after 295.66; silence follows'},
    {'cue': 68, 'boundary': 'start', 'expected': 'In',       'new': 296.26, 'reason': 'CPU boundary; new voice onset after a silent gap'},
    {'cue': 102, 'boundary': 'start','expected': 'It',       'new': 446.48, 'reason': 'both ASR starts in digital silence; energy onset about 446.53'},
    {'cue': 166, 'boundary': 'start','expected': 'Life',     'new': 715.72, 'reason': 'CPU boundary; energy onset about 715.81'},
]
for change in waveform_adjustments:
    cue = cues[change['cue']-1]
    unit = cue[0] if change['boundary'] == 'start' else cue[-1]
    if change['expected'] not in unit['text'].split():
        raise SystemExit(f'Unexpected cue text for waveform adjustment: {change}')
    change['old'] = unit[change['boundary']]
    unit[change['boundary']] = change['new']
output = HERE / 'pompeii_en_full_REVIEW.srt'
rendered_tokens = []
with output.open('w', encoding='utf-8') as f:
    for n, cue in enumerate(cues, 1):
        text = ' '.join(x['text'] for x in cue)
        rendered_tokens.extend(m.group(0) for m in TOKEN.finditer(text))
        if cue[0]['start'] >= cue[-1]['end']:
            raise SystemExit(f'Invalid cue at {n}')
        f.write(f"{n}\n{stamp(cue[0]['start'])} --> {stamp(cue[-1]['end'])}\n{textwrap.fill(text, 42, break_long_words=False, break_on_hyphens=False)}\n\n")
if rendered_tokens != src:
    raise SystemExit('The rendered SRT does not exactly preserve all source words and punctuation.')
for x,y in zip(cues,cues[1:]):
    if x[-1]['end'] > y[0]['start']:
        raise SystemExit('Overlapping subtitle cues')

with (HERE / 'full_srt_differences_REVIEW.csv').open('w',encoding='utf-8',newline='') as f:
    out=csv.DictWriter(f,fieldnames=['start','end','approved','asr','review'])
    out.writeheader();out.writerows(replacements)
report = {
  'source_words': len(src), 'source_text_exactly_preserved': rendered_tokens == src,
  'cues': len(cues), 'asr_mismatch_spans': len(replacements),
  'zero_length_words_merged_into_adjacent_phrase': merged_zero,
  'waveform_cue_adjustments': waveform_adjustments,
  'cue_overlaps': 0,
  'method': 'Approved text is matched to Whisper ASR. Each disagreement uses the measured ASR span of the entire replacement, not invented per-word boundaries. Zero-duration ASR words were joined to adjacent groups. Eight cue boundaries were adjusted using CPU/MPS comparison and voice-source RMS/silence, as listed. Timing still needs listening review; waveform alone cannot identify spoken words.',
  'audio_review': 'Not performed by this script. Especially check towns/town and turned/turn, names, and replacement spans.',
}
(HERE / 'full_srt_report_REVIEW.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
