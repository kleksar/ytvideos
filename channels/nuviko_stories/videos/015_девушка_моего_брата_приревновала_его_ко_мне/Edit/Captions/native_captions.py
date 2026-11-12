#!/usr/bin/env python3
import json,sys,argparse
from pathlib import Path
from PIL import ImageFont
CAP=Path(__file__).resolve().parent
ROOT=CAP.parents[1]
sys.path.insert(0,'/Users/diplomat/ytvideos/automation/captions')
sys.path.insert(0,'/Users/diplomat/ytvideos/automation/palmier')
from word_timings import convert
from inspect_connection import PalmierConnection
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
FPS=30; SPEED=1.10
segments=[('female_before',0,2848),('male_line',2852,2887),('female_after',2891,4672)]
words=[]
for name,start,end in segments:
 text=(ROOT/f'{name}.txt').read_text()
 data=json.loads((ROOT/'Source/Voice'/name/'voice_ru.alignment.json').read_text())
 wd=convert(text,data,'ru'); (CAP/f'{name}.words.json').write_text(json.dumps(wd,ensure_ascii=False,indent=2)+'\n')
 for w in wd['words']:
  words.append({'text':w['display'],'start':start+round(w['start_seconds']/SPEED*FPS),'end':min(end,start+round(w['end_seconds']/SPEED*FPS)),'segment':name})
font=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',88,index=9)
def width(w): return font.getlength(w)+1.5*(len(w)-1)
groups=[];i=0
for line in (CAP/'015_ru_caption_plan.txt').read_text().splitlines():
 toks=line.split(); assert 1<=len(toks)<=3,(line,toks)
 assert toks==[w['text'] for w in words[i:i+len(toks)]],(i,toks,[w['text'] for w in words[i:i+len(toks)]])
 ws=words[i:i+len(toks)];i+=len(toks); assert len({w['segment'] for w in ws})==1,line
 widths=[width(w) for w in toks]; total=sum(widths)+32.5*(len(toks)-1)
 assert total+.05*max(widths)+10<=996,(line,total)
 groups.append({'text':line,'words':ws,'widths':widths,'start':ws[0]['start']})
assert i==len(words)
for k,g in enumerate(groups):
 g['end']=groups[k+1]['start'] if k+1<len(groups) else min(segments[-1][2],max(g['words'][-1]['end'],g['start']+1))
 assert g['end']>g['start'],g
 x=(1080-sum(g['widths'])-32.5*(len(g['words'])-1))/2
 for w,wd in zip(g['words'],g['widths']):w['x']=round((x+wd/2)/1080,6); x+=wd+32.5
style={'fontName':'HelveticaNeue-CondensedBlack','fontSize':49.7,'alignment':'center','color':'#FFFFFF','tracking':1.5,'outline':{'enabled':True,'color':'#000000D2','width':5}}
base=[];high=[];visible=[]
for g in groups:
 start=max(g['start'],311);end=min(g['end'],4491)
 if end-start<8:continue
 visible.append({**g,'start':start,'end':end})
 for w in g['words']:
  base.append({'startFrame':start,'endFrame':end,'content':w['text'],'transform':{'x':w['x'],'y':.40},'style':style})
  hs=max(start,w['start']);he=min(end,w['end'])
  if he-hs>=2:high.append({'startFrame':hs,'endFrame':he,'content':w['text'],'transform':{'x':w['x'],'y':.40},'style':{**style,'color':'#FFD54F'}})
mp={'fps':FPS,'speed':SPEED,'segments':segments,'ad_exclusions':[[0,311],[4491,4672]],'groups':groups,'visible_groups':visible,'base_count':len(base),'highlight_count':len(high)}
(CAP/'015_native_caption_map.json').write_text(json.dumps(mp,ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 n=round(t*1000/FPS);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,n=divmod(n,1000);return f'{h:02d}:{m:02d}:{s:02d},{n:03d}'
def srt(name,arr):
 (CAP/name).write_text(''.join(f"{n+1}\n{stamp(g['start'])} --> {stamp(g['end'])}\n{g['text']}\n\n" for n,g in enumerate(arr)))
srt('015_ru_captions_110_full.srt',groups);srt('015_ru_captions_110_no_ad.srt',visible)
print(json.dumps({'words':len(words),'groups':len(groups),'base':len(base),'highlight':len(high),'under8frames':[(g['text'],g['end']-g['start']) for g in groups if g['end']-g['start']<8],'cps_over20':[(g['text'],round(len(g['text'])*FPS/(g['end']-g['start']),1)) for g in groups if len(g['text'])*FPS/(g['end']-g['start'])>20]},ensure_ascii=False))
if not a.apply:sys.exit()
palm=PalmierConnection();palm.connect()
def check():
 pr=palm.read_tool('manage_project',{'action':'list'});t=palm.read_tool('get_timeline',{})
 assert pr['active']['path']=='/Users/diplomat/ytvideos/channels/nuviko_stories/videos/1/1.palmier',pr['active']
 assert pr['visible']['path']==pr['active']['path']; assert t['id']=='14F294AD',t['id']
 return t
old=check()
assert not [c for tr in old['tracks'] for c in tr['clips'] if c.get('mediaType')=='text'], 'text exists: refusing duplicates'
(CAP/'before_caption_add.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
for name,entries in [('base',base),('highlight',high)]:
 check(); r=palm.request('tools/call',{'name':'add_texts','arguments':{'entries':entries}})
 (CAP/f'015_native_{name}_receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 if r.get('isError'): raise RuntimeError(r)
 print(name,'OK');check()
(CAP/'after_caption_add.json').write_text(json.dumps(check(),ensure_ascii=False,indent=2)+'\n')
