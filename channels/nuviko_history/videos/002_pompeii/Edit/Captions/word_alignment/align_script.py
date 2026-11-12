#!/usr/bin/env python3
"""Compare approved script with Whisper word timing; output explicit REVIEW files.

Matched words are sourced from the approved text. No timestamps are invented for
unmatched words. The draft SRT intentionally omits unmatched spans and is not
a delivery subtitle file; discrepancies must be reviewed against the audio.
"""
import argparse
import csv
import difflib
import json
import re
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'approved_script_en.txt'
TOKEN = re.compile(r"[\w]+(?:['’\-][\w]+)*(?:[.,!?;:]+)?", re.UNICODE)

def pieces(token):
    # Hyphens may be separated by ASR. Keep the approved spelling for display.
    return [x.lower().replace('’', "'") for x in re.findall(r"[\w]+(?:['’][\w]+)*", token)]

def stamp(t):
    ms = round(t * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('whisper_json', type=Path)
    args = ap.parse_args()
    src = [m.group(0) for m in TOKEN.finditer(SOURCE.read_text(encoding='utf-8'))]
    data = json.loads(args.whisper_json.read_text(encoding='utf-8'))
    raw_words = [w for seg in data['segments'] for w in seg.get('words', [])]
    if not raw_words:
        raise SystemExit('No word timestamps: refusing to construct subtitles.')
    timing_problems = []
    for i, w in enumerate(raw_words):
        if w['end'] <= w['start']:
            timing_problems.append({'index': i, 'word': w['word'], 'start': w['start'], 'end': w['end'], 'problem': 'nonpositive duration'})
        if i and w['start'] < raw_words[i-1]['start']:
            timing_problems.append({'index': i, 'word': w['word'], 'start': w['start'], 'end': w['end'], 'problem': 'start before previous start'})
    (HERE / 'timing_problems_REVIEW.json').write_text(json.dumps(timing_problems, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    bad_indices = {v['index'] for v in timing_problems}
    a, b = [], []
    for i, word in enumerate(src):
        a.extend((part, i) for part in pieces(word))
    for i, word in enumerate(raw_words):
        b.extend((part, i) for part in pieces(word['word']))
    sm = difflib.SequenceMatcher(None, [x[0] for x in a], [x[0] for x in b], autojunk=False)
    matched = {}
    diffs = []
    for tag, i, j, k, l in sm.get_opcodes():
        if tag == 'equal':
            for x, y in zip(range(i, j), range(k, l)):
                matched[x] = b[y][1]
            continue
        src_ids = list(dict.fromkeys(x[1] for x in a[i:j]))
        asr_ids = list(dict.fromkeys(x[1] for x in b[k:l]))
        # A neighboring time is contextual only, never a timestamp for a missing word.
        left = raw_words[b[k-1][1]]['end'] if k else None
        right = raw_words[b[l][1]]['start'] if l < len(b) else None
        diffs.append({
            'type': tag,
            'approved': ' '.join(src[z] for z in src_ids),
            'asr': ''.join(raw_words[z]['word'] for z in asr_ids).strip(),
            'asr_start': raw_words[asr_ids[0]]['start'] if asr_ids else '',
            'asr_end': raw_words[asr_ids[-1]]['end'] if asr_ids else '',
            'left_neighbor_end': left if left is not None else '',
            'right_neighbor_start': right if right is not None else '',
            'approved_context': ' '.join(src[max(0, (src_ids[0] if src_ids else (a[i][1] if i < len(a) else len(src)))-6):min(len(src), (src_ids[-1]+7 if src_ids else (a[i][1] if i < len(a) else len(src))+6))]),
            'review': 'REVIEW AUDIO; ASR interval is candidate only; missing approved words have no assigned time',
        })
    with (HERE / 'mismatches_REVIEW.csv').open('w', encoding='utf-8', newline='') as f:
        out = csv.DictWriter(f, fieldnames=list(diffs[0]) if diffs else ['type','approved','asr','asr_start','asr_end','left_neighbor_end','right_neighbor_start','approved_context','review'])
        out.writeheader(); out.writerows(diffs)
    by_src = {}
    src_parts = {}
    for index, (_, sid) in enumerate(a):
        src_parts.setdefault(sid, []).append(index)
    for sid, ids in src_parts.items():
        if all(i in matched and matched[i] not in bad_indices for i in ids):
            indices = [matched[i] for i in ids]
            by_src[sid] = {'text': src[sid], 'start': min(raw_words[i]['start'] for i in indices), 'end': max(raw_words[i]['end'] for i in indices), 'asr_indices': indices}
    # A cue consists only of consecutive matched script words. Break at every
    # unresolved token so its absence is visible in the REVIEW subtitle file.
    cues, current, last_sid = [], [], None
    def flush():
        if current:
            cues.append(current[:]); current.clear()
    for sid in range(len(src)):
        item = by_src.get(sid)
        if not item:
            flush(); last_sid = None; continue
        text = ' '.join(x['text'] for x in current + [item])
        wrapped = textwrap.wrap(text, width=42, break_long_words=False, break_on_hyphens=False)
        if current and (sid != last_sid+1 or len(wrapped) > 2 or item['end']-current[0]['start'] > 6 or item['start']-current[-1]['end'] > .8):
            flush()
        current.append(item); last_sid = sid
        if re.search(r'[.!?]$', item['text']) and item['end']-current[0]['start'] >= 1:
            flush()
    flush()
    with (HERE / 'subtitles_MATCHED_ONLY_REVIEW.srt').open('w', encoding='utf-8') as f:
        for i, cue in enumerate(cues, 1):
            text = textwrap.fill(' '.join(x['text'] for x in cue), width=42, break_long_words=False, break_on_hyphens=False)
            f.write(f"{i}\n{stamp(cue[0]['start'])} --> {stamp(cue[-1]['end'])}\n{text}\n\n")
    result = {'approved_tokens': len(src), 'whisper_word_items': len(raw_words), 'fully_matched_approved_tokens': len(by_src), 'unmatched_or_bad_timing_approved_tokens': len(src)-len(by_src), 'mismatch_regions': len(diffs), 'timing_problems': len(timing_problems), 'draft_cues': len(cues), 'warning': 'Review SRT omits unresolved words; not a final subtitle track; word timestamps are ASR estimates.'}
    (HERE / 'alignment_summary_REVIEW.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (HERE / 'approved_matched_word_timings_REVIEW.json').write_text(json.dumps(by_src, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
