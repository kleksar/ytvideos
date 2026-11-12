#!/usr/bin/env python3
import json, sys, re, math
from pathlib import Path
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[2]
CAP=Path(__file__).resolve().parent
sys.path.insert(0,'/Users/diplomat/ytvideos/automation/palmier')
from inspect_connection import PalmierConnection
FPS=30;SPEED=1.1
segments=[('female_before',0),('male_line',3359),('female_after',3522)]
words=[]
for name,start in segments:
 for w in json.loads((ROOT/'Source/Voice'/f'{name}.words.json').read_text())['words']:
  words.append({'text':w['display'],'start':start+round(w['start_seconds']/SPEED*FPS),'end':start+round(w['end_seconds']/SPEED*FPS),'segment':name})
lines=(CAP/'013_ru_caption_plan.txt').read_text().splitlines()
font=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',92,index=9)
def width(w): return font.getlength(w)+1.5*(len(w)-1)
groups=[]; i=0
for line in lines:
 toks=line.split(); assert 1<=len(toks)<=3
 assert toks==[w['text'] for w in words[i:i+len(toks)]], (i,toks,[w['text'] for w in words[i:i+len(toks)]])
 group=words[i:i+len(toks)]; i+=len(toks)
 assert len(set(w['segment'] for w in group))==1
 widths=[width(w) for w in toks]
 total=sum(widths)+32.5*(len(toks)-1)
 assert total+.05*max(widths)+10<=996,(line,total)
 groups.append({'text':line,'words':group,'widths':widths,'start':group[0]['start']})
assert i==len(words)
for k,g in enumerate(groups):
 g['end']=groups[k+1]['start'] if k+1<len(groups) else max(g['words'][-1]['end'],g['start']+1)
 assert g['end']>g['start'],g
 # Keep captions through brief pauses between segments, but final word ends at actual speech.
 x=(1080-sum(g['widths'])-32.5*(len(g['words'])-1))/2
 for w,wd in zip(g['words'],g['widths']):
  w['x']=round((x+wd/2)/1080,6);x+=wd+32.5
style={'fontName':'HelveticaNeue-CondensedBlack','fontSize':52,'alignment':'center','color':'#FFFFFF','tracking':1.5,'outline':{'enabled':True,'color':'#000000D2','width':5}}
y=0.40
base=[]; high=[]
for g in groups:
 for w in g['words']:
  b={'startFrame':g['start'],'endFrame':g['end'],'content':w['text'],'transform':{'x':w['x'],'y':y},'style':style}
  base.append(b)
  start=max(g['start'],w['start']); end=min(g['end'],max(w['end'],start+1))
  if end>start:
   high.append({'startFrame':start,'endFrame':end,'content':w['text'],'transform':{'x':w['x'],'y':y},'style':{**style,'color':'#FFD54F'}})
(CAP/'013_native_caption_map.json').write_text(json.dumps({'fps':FPS,'speed':SPEED,'segments':segments,'groups':groups},ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 n=round(t*1000/FPS);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,n=divmod(n,1000);return f'{h:02d}:{m:02d}:{s:02d},{n:03d}'
(CAP/'013_ru_captions_110.srt').write_text(''.join(f"{n+1}\n{stamp(g['start'])} --> {stamp(g['end'])}\n{g['text']}\n\n" for n,g in enumerate(groups)))
print('groups',len(groups),'base',len(base),'highlight',len(high),'minimum frames',min(g['end']-g['start'] for g in groups))
print('short',[(g['text'],g['end']-g['start']) for g in groups if g['end']-g['start']<8])
print('cps',[(g['text'],round(len(g['text'])*FPS/(g['end']-g['start']),1)) for g in groups if len(g['text'])*FPS/(g['end']-g['start'])>20])
if len(sys.argv)<2:sys.exit()
p=PalmierConnection(); p.connect()
def check():
 pr=p.read_tool('manage_project',{'action':'list'}); t=p.read_tool('get_timeline',{})
 assert pr['active']['path']=='/Users/diplomat/ytvideos/channels/nuviko_stories/videos/1/1.palmier'
 assert pr['visible']['path']==pr['active']['path']
 assert t['id']=='6FB7B8EE' and t['name']=='013_ru_shorts_110'
def call(entries):
 check();r=p.request('tools/call',{'name':'add_texts','arguments':{'entries':entries}})
 if r.get('isError'): raise RuntimeError(r)
 print(json.dumps(r,ensure_ascii=False)[:4000]);check()
if sys.argv[1]=='test':call(base[:2]+high[:2])
elif sys.argv[1]=='remaining':call(base[2:]+high[2:])
