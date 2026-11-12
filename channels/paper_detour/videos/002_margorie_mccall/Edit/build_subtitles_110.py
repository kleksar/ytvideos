#!/usr/bin/env python3
"""Create external English SRT from the alignment at 1.10×; still needs listening."""
from pathlib import Path
import json,re
from decimal import Decimal, ROUND_HALF_UP
root=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/002_margorie_mccall')
src=root/'Source/Voice/script_en.txt'
words=json.loads((root/'Source/Voice/voice_en_lawrence.words.json').read_text())['words']
tokens=src.read_text().split()
# Hand-edited semantic groups. Newlines indicate comfortable two-line layout.
groups=[
'When they buried Margorie McCall,\nan expensive ring was still on her finger.',
'Her husband had tried to take it off,\nbut her finger was too swollen.',
'Margorie had died of a fever,',
'and her family rushed the burial,\nafraid the illness might spread.',
'That very night, while the earth\non her grave was still loose,',
'thieves came to the graveyard.',
'They knew about the ring.',
"They opened the coffin and tried\nto pull it off, but it wouldn't budge.",
'So one of them pulled out a knife:',
"if he couldn't remove the ring,\nhe would cut off her finger.",
'The blade touched her skin.',
'And at that very moment,',
'the woman they believed was dead\nsat up in the coffin and screamed.',
'The thieves ran for their lives,',
'while Margorie climbed out of the grave\nand walked home in her burial clothes.',
'Her husband was sitting with their\nchildren when someone knocked at the door.',
'He froze and said,',
'“If your mother were still alive,\nI\'d swear that was her knock.”',
'He opened the door.',
'There stood Margorie,\nin the clothes she\'d been buried in,',
'with blood on her hand.',
'When he saw his wife, he clutched\nhis chest and dropped dead.',
'A few days later, they buried him\nin the very coffin',
'Margorie had climbed out of.',
'She lived for many more years,\nmarried again, and had children.',
'And when her own time came,\nthese words were carved on her headstone:',
'“Lived once, buried twice.”'
]
all_group_tokens=' '.join(groups).split()
if all_group_tokens!=tokens:
 for n,(a,b) in enumerate(zip(all_group_tokens,tokens)):
  if a!=b: raise ValueError(f'token {n}: {a!r} != {b!r}')
 raise ValueError('token lengths differ')
if len(tokens)!=len(words): raise ValueError('word count mismatch')
speed=Decimal('1.10'); max_seconds=Decimal(2296)/Decimal(30)
def ms(v): return int((Decimal(str(v))*1000/speed).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
def fmt(n):
 h,n=divmod(n,3600000); m,n=divmod(n,60000); s,n=divmod(n,1000)
 return f'{h:02}:{m:02}:{s:02},{n:03}'
index=0; cues=[]
for i,group in enumerate(groups):
 n=len(group.split()); first=words[index]; last=words[index+n-1]
 start=ms(first['start_seconds']); end=ms(last['end_seconds'])
 # A small linger improves readability if the following speech leaves time.
 proposed=end+120
 if index+n<len(words): proposed=min(proposed,ms(words[index+n]['start_seconds'])-30)
 end=max(end,proposed)
 end=min(end,int(max_seconds*1000))
 if end<=start: raise ValueError(f'invalid interval {i+1}')
 cues.append((start,end,group))
 index+=n
# Extend short cues into adjacent silence when available, up to 250 ms each side.
# Never obscure the neighbouring cue or shift a speech word outside its cue.
for i,(start,end,text) in enumerate(cues):
 target=round(len(text.replace('\n',' '))/20*1000)
 need=max(0,target-(end-start))
 if need:
  previous_end=cues[i-1][1] if i else 0
  take=min(need,250,max(0,start-previous_end-30)); start-=take; need-=take
  next_start=cues[i+1][0] if i+1<len(cues) else int(max_seconds*1000)
  take=min(need,250,max(0,next_start-end-30)); end+=take
  cues[i]=(start,end,text)
for i in range(len(cues)-1):
 if cues[i][1]>cues[i+1][0]: raise ValueError(f'overlap {i+1}')
for i,(a,b,text) in enumerate(cues):
 chars=max(map(len,text.splitlines()))
 cps=len(text.replace('\n',' '))/((b-a)/1000)
 if chars>42: print(f'cue {i+1} line {chars} chars')
 if cps>22: print(f'cue {i+1} reading rate {cps:.1f} chars/s')
out=root/'Edit/voice_lawrence_110_readable_draft.en.srt'
if out.exists(): raise FileExistsError(out)
out.write_text('\n\n'.join(f'{i}\n{fmt(a)} --> {fmt(b)}\n{t}' for i,(a,b,t) in enumerate(cues,1))+'\n')
print(f'Saved {len(cues)} cues, {index} words, last {fmt(cues[-1][1])}; timeline {fmt(int(max_seconds*1000))}')
