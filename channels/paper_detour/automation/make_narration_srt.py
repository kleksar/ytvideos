#!/usr/bin/env python3
"""Build provisional punctuation-preserving SRT from ElevenLabs character timing.

This is a draft alignment, not a listening or transcript verification. Files are
created exclusively; callers must review actual speech before publication.
"""
import argparse, hashlib, json, math, re, subprocess, textwrap
from pathlib import Path

WORD = re.compile(r"[\w]+(?:[’'\-][\w]+)*", re.UNICODE)

def stamp(sec):
    ms = round(sec * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

def build(text_file, alignment_file, words_file, audio_file, out):
    text = text_file.read_text(encoding='utf-8')
    alignment = json.loads(alignment_file.read_text(encoding='utf-8'))['alignment']
    chars = alignment['characters']
    if ''.join(chars).strip() != text.strip():
        raise ValueError('Alignment does not match narration text')
    word_data = json.loads(words_file.read_text(encoding='utf-8'))
    if word_data.get('source_sha256') != hashlib.sha256(text.encode()).hexdigest():
        raise ValueError('Word timings were generated from different text')
    words = word_data['words']
    matches = list(WORD.finditer(''.join(chars)))
    if len(matches) != len(words) or any(m.group().casefold() != w['text'].casefold() for m, w in zip(matches, words)):
        raise ValueError('Words do not match character alignment')
    probe = json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','json',str(audio_file)],check=True,capture_output=True,text=True).stdout)
    duration = float(probe['format']['duration'])
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError('Invalid audio duration')
    source = ''.join(chars)
    pieces = []
    for i, match in enumerate(matches):
        next_start = matches[i+1].start() if i+1 < len(matches) else len(source)
        pieces.append(source[match.start():next_start].strip())
    # Globally balance neighboring cues; a greedy maximum-size grouping often
    # leaves a one-word or sub-second orphan at the end of a sentence.
    count=len(words); costs=[float('inf')]*(count+1); choice=[None]*count; costs[count]=0
    for first in range(count-1,-1,-1):
        for last in range(first,min(count,first+20)):
            if last>first and re.search(r'[.!?][\"”’\']?$',pieces[last-1]): break
            if last>first and float(words[last]['start_seconds'])-float(words[last-1]['end_seconds'])>.7: break
            content=' '.join(pieces[first:last+1])
            lines=textwrap.wrap(content,width=42,break_long_words=False,break_on_hyphens=False)
            span=float(words[last]['end_seconds'])-float(words[first]['start_seconds'])
            if len(lines)>2 or any(len(x)>42 for x in lines) or span>5.6: break
            sentence_end=bool(re.search(r'[.!?][\"”’\']?$',pieces[last]))
            count_words=last-first+1
            cost=1+max(0,1.4-span)*6+(2 if count_words==1 else 0)+(0 if sentence_end else .65)+costs[last+1]
            if cost < costs[first]: costs[first]=cost; choice[first]=last
    groups=[]; i=0
    while i<count:
        if choice[i] is None: raise ValueError('Cannot create readable subtitle groups')
        groups.append((i,choice[i])); i=choice[i]+1
    entries=[]
    for n,(first,last) in enumerate(groups,1):
        start=float(words[first]['start_seconds'])
        end=min(duration,float(words[last]['end_seconds'])+.12)
        if n<len(groups):
            end=min(end,float(words[groups[n][0]]['start_seconds']))
        if end<=start: raise ValueError('Invalid or overlapping timing')
        content='\n'.join(textwrap.wrap(' '.join(pieces[first:last+1]),width=42,break_long_words=False,break_on_hyphens=False))
        entries.append(f'{n}\n{stamp(start)} --> {stamp(end)}\n{content}')
    with out.open('x',encoding='utf-8') as f: f.write('\n\n'.join(entries)+'\n')
    return {'path':str(out),'duration':duration,'words':len(words),'cues':len(entries),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('text','alignment','words','audio','output'): p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(build(a.text,a.alignment,a.words,a.audio,a.output),indent=2))
if __name__=='__main__':main()
