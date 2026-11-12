#!/usr/bin/env python3
"""Reflow text *inside* each cue without changing text or any cue boundary."""
import csv
import json
import re
from pathlib import Path

D = Path(__file__).resolve().parent
SOURCE = D / 'pompeii_en_full_REVIEW.srt'
OUT = D / 'pompeii_en_readable_REVIEW.srt'
WEAK = set('a an the in of at to for from with by on as into about after before under over through between beneath toward along across and or nor but not is are was were be been being have has had do does did can could would should will may might must its their his her our your this that these those'.split())

def last_word(line):
    # A sentence-ending punctuation mark is a natural boundary.
    if re.search(r'[.!?:;]$', line): return ''
    return re.sub(r"[^a-z']", '', line.split()[-1].lower())

def wrap(line):
    if len(line) <= 42: return [line]
    words = line.split(' ')
    choices = []
    for n in range(1,len(words)):
        first, second = ' '.join(words[:n]), ' '.join(words[n:])
        if len(first)>42 or len(second)>42: continue
        weak = last_word(first)
        score = 200*(weak in WEAK) + abs(len(first)-len(second))
        if re.search(r'[,;:.!?]$',first): score -= 3
        choices.append((score,n,first,second))
    if not choices: raise SystemExit(f'Cannot fit into two 42-character lines: {line!r}')
    _,_,first,second=min(choices)
    return [first,second]

blocks = SOURCE.read_text(encoding='utf-8').strip().split('\n\n')
changes = []
intercue = []
result = []
before_bad = after_bad = 0
for pos,block in enumerate(blocks):
    lines=block.splitlines()
    old=lines[2:]
    text=' '.join(old)
    # Keep a pre-existing reasonable split when it has no weak ending.
    # Mechanical balance by itself must not split a phrase that was already
    # readable, such as "lightweight white stones" or "Bay of Naples".
    new=old if len(old)<2 or last_word(old[0]) not in WEAK else wrap(text)
    before_bad += sum(last_word(x) in WEAK for x in old[:-1])
    after_bad += sum(last_word(x) in WEAK for x in new[:-1])
    if old != new:
        changes.append({'cue':lines[0], 'old':' | '.join(old), 'new':' | '.join(new), 'time':lines[1]})
    if pos+1<len(blocks) and last_word(new[-1]) in WEAK:
        next_text=' '.join(blocks[pos+1].splitlines()[2:])
        intercue.append({'cue':lines[0], 'time':lines[1], 'last_word':last_word(new[-1]), 'cue_text':text, 'next_cue_text':next_text})
    result.append('\n'.join(lines[:2]+new))
OUT.write_text('\n\n'.join(result)+'\n',encoding='utf-8')
with (D/'srt_reflow_changes_REVIEW.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['cue','time','old','new']);writer.writeheader();writer.writerows(changes)
with (D/'intercue_weak_endings_REVIEW.csv').open('w',encoding='utf-8',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['cue','time','last_word','cue_text','next_cue_text']);writer.writeheader();writer.writerows(intercue)
# Preserve every cue's exact time boundaries and every character other than
# whitespace; do not assert more about word timing than the source SRT does.
after=OUT.read_text(encoding='utf-8').strip().split('\n\n')
assert len(after)==len(blocks)
for old,new in zip(blocks,after):
    o,n=old.splitlines(),new.splitlines()
    assert o[:2]==n[:2]
    assert ' '.join(o[2:])==' '.join(n[2:])
    assert len(n[2:])<=2 and all(len(line)<=42 for line in n[2:])
report={'cues':len(blocks),'changed_line_wraps':len(changes),'weak_intra_cue_line_endings_before':before_bad,'weak_intra_cue_line_endings_after':after_bad,'weak_intercue_endings':len(intercue),'cue_boundaries_changed':0,'source_text_changed':False,'note':'Inter-cue boundaries and all word positions within cue timing are unchanged; weak endings across cues are reported, not shuffled across observed times. Auditory sync has not been verified.'}
(D/'srt_reflow_report_REVIEW.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2,ensure_ascii=False))
