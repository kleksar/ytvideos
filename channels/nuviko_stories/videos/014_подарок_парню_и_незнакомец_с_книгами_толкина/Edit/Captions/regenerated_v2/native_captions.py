#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
from PIL import ImageFont
CAP=Path(__file__).resolve().parent
PREV=CAP.parent
sys.path.insert(0,'/Users/diplomat/ytvideos/automation/palmier')
from inspect_connection import PalmierConnection
p=argparse.ArgumentParser();p.add_argument('--timeline',required=True);p.add_argument('--audio-start',type=int,required=True);p.add_argument('--audio-end',type=int,required=True);p.add_argument('--ad-intro-end',type=int,required=True);p.add_argument('--ad-outro-start',type=int,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
FPS=30;SPEED=1.1
words=json.loads((CAP/'014_words.json').read_text())['words']
words=[{'text':w['display'],'start':a.audio_start+round(w['start_seconds']/SPEED*FPS),'end':min(a.audio_end,a.audio_start+round(w['end_seconds']/SPEED*FPS))} for w in words]
font=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',88,index=9)
def width(w):return font.getlength(w)+1.5*(len(w)-1)
groups=[];i=0
for line in (PREV/'014_ru_caption_plan.txt').read_text().splitlines():
 toks=line.split(); assert 1<=len(toks)<=3
 assert toks==[w['text'] for w in words[i:i+len(toks)]],(line,i); ws=words[i:i+len(toks)];i+=len(toks)
 widths=[width(w) for w in toks];total=sum(widths)+32.5*(len(toks)-1)
 assert total+.05*max(widths)+10<=996,(line,total)
 groups.append({'text':line,'words':ws,'widths':widths,'start':ws[0]['start']})
assert i==len(words)
for k,g in enumerate(groups):
 g['end']=groups[k+1]['start'] if k+1<len(groups) else min(a.audio_end,max(g['words'][-1]['end'],g['start']+1))
 assert g['end']>g['start'],g
 x=(1080-sum(g['widths'])-32.5*(len(g['words'])-1))/2
 for w,wd in zip(g['words'],g['widths']):w['x']=round((x+wd/2)/1080,6);x+=wd+32.5
style={'fontName':'HelveticaNeue-CondensedBlack','fontSize':49.7,'alignment':'center','color':'#FFFFFF','tracking':1.5,'outline':{'enabled':True,'color':'#000000D2','width':5}}
base=[];high=[];visible=[]
for g in groups:
 start=max(g['start'],a.ad_intro_end); end=min(g['end'],a.ad_outro_start)
 if end-start<8:continue  # short clipped groups at the ad boundary would flash
 visible.append({**g,'start':start,'end':end})
 for w in g['words']:
  base.append({'startFrame':start,'endFrame':end,'content':w['text'],'transform':{'x':w['x'],'y':.40},'style':style})
  hs=max(start,w['start']);he=min(end,w['end'])
  if he-hs>=2:high.append({'startFrame':hs,'endFrame':he,'content':w['text'],'transform':{'x':w['x'],'y':.40},'style':{**style,'color':'#FFD54F'}})
map={'fps':FPS,'speed':SPEED,'audio_range':[a.audio_start,a.audio_end],'ad_exclusions':[[0,a.ad_intro_end],[a.ad_outro_start,a.audio_end]],'groups':groups,'visible_groups':visible,'base_count':len(base),'highlight_count':len(high)}
(CAP/'014_native_caption_map.json').write_text(json.dumps(map,ensure_ascii=False,indent=2)+'\n')
def stamp(t):
 n=round(t*1000/FPS);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,n=divmod(n,1000);return f'{h:02d}:{m:02d}:{s:02d},{n:03d}'
def srt(name,arr):
 (CAP/name).write_text(''.join(f"{n+1}\n{stamp(g['start'])} --> {stamp(g['end'])}\n{g['text']}\n\n" for n,g in enumerate(arr)))
srt('014_ru_captions_110_full.srt',groups);srt('014_ru_captions_110_no_ad.srt',visible)
print(json.dumps({'groups':len(groups),'words':i,'base':len(base),'highlight':len(high),'audio_range':[a.audio_start,a.audio_end],'exclusions':map['ad_exclusions'],'last':groups[-1],'under8frames':[(g['text'],g['end']-g['start']) for g in groups if g['end']-g['start']<8],'cps_over20':[(g['text'],round(len(g['text'])*FPS/(g['end']-g['start']),1)) for g in groups if len(g['text'])*FPS/(g['end']-g['start'])>20]},ensure_ascii=False))
if not a.apply:sys.exit()
palm=PalmierConnection();palm.connect()
def check():
 pr=palm.read_tool('manage_project',{'action':'list'});t=palm.read_tool('get_timeline',{})
 assert pr['active']['path']=='/Users/diplomat/ytvideos/channels/nuviko_stories/videos/1/1.palmier',pr['active']
 assert pr['visible']['path']==pr['active']['path']
 assert t['id']==a.timeline,t['id']
check()
old_t=palm.read_tool('get_timeline',{})
old_text=[]
for tr in old_t['tracks']:
 clips=tr['clips']
 text_clips=[c for c in clips if c.get('mediaType')=='text']
 if text_clips and len(text_clips)!=len(clips):
  raise RuntimeError('Unexpected mixed text track; refusing to delete')
 old_text.extend(c['id'] for c in text_clips)
if not old_text:
 raise RuntimeError('No original native captions found; refusing to add duplicate captions')
(CAP/'before_caption_replace.json').write_text(json.dumps(old_t,ensure_ascii=False,indent=2)+'\n')
r=palm.request('tools/call',{'name':'remove_clips','arguments':{'clipIds':old_text}})
(CAP/'remove_caption_receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
if r.get('isError'):raise RuntimeError(r)
check()
remaining=[c['id'] for tr in palm.read_tool('get_timeline',{})['tracks'] for c in tr['clips'] if c.get('mediaType')=='text']
if remaining:raise RuntimeError('Original text remains: '+str(remaining[:10]))
for name,entries in [('base',base),('highlight',high)]:
 check()
 r=palm.request('tools/call',{'name':'add_texts','arguments':{'entries':entries}})
 (CAP/f'014_native_{name}_receipt.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 if r.get('isError'):raise RuntimeError(r)
 print(name,'OK')
 check()

check()
(CAP/'after_caption_replace.json').write_text(json.dumps(palm.read_tool('get_timeline',{}),ensure_ascii=False,indent=2)+'\n')
