#!/usr/bin/env python3
"""Validate semantic caption plan against EN word alignment; optionally add to Palmier.

First run without --apply. A human-created plan has 1-3 uppercase words per line
in exact source order; the speech clips and bounds are from the montage receipt.
Only use --apply after the live project is free, and never retry without inspection.
"""
import argparse,json,re,sys
from pathlib import Path
from PIL import ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'palmier'))
from inspect_connection import PalmierConnection
from word_timings import convert

PROJECT=Path('/Users/diplomat/ytvideos/channels/nuviko_stories/videos/1/1.palmier').resolve()
FPS=30

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('receipt',type=Path);p.add_argument('plan',type=Path);p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--apply',action='store_true')
 a=p.parse_args();r=json.loads(a.receipt.read_text());assert r['status']=='awaiting_captions'
 out=a.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
 words=[]
 for i,s in enumerate(r['segments']):
  assert s['speed']==1.1
  start,end=s['frames']; source=Path(s['text']).read_text(); wd=convert(source,json.loads(Path(s['alignment']).read_text()),'en')
  # word_timings strips terminal plural-possessive apostrophes. Restore them
  # only when confirmed in the actual source, never by trusting the plan.
  raw=re.findall(r"[^\W_]+(?:['’\-][^\W_]+)*(?:['’](?=\s|[.,!?;:]|$))?",source,re.UNICODE)
  assert len(raw)==len(wd['words']),(len(raw),len(wd['words']))
  for w,raw_word in zip(wd['words'],raw):
   assert raw_word.rstrip("'’")==w['text'],(raw_word,w['text'])
   display=raw_word.upper()
   wf=start+round(w['start_seconds']*FPS/1.1);we=min(end,start+round(w['end_seconds']*FPS/1.1))
   assert start<=wf<end and we>=wf,(s['text'],w)
   words.append({'text':display,'start':wf,'end':we,'segment':i})
 fonts={}
 def width(w,size):
  if size not in fonts:fonts[size]=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',size,index=9)
  return fonts[size].getlength(w)+1.5*(len(w)-1)
 groups=[];idx=0
 for line in a.plan.read_text().splitlines():
  if not line.strip():continue
  toks=line.split();assert 1<=len(toks)<=3,line
  actual=[w['text'] for w in words[idx:idx+len(toks)]]
  assert toks==actual,(idx,toks,actual)
  ws=words[idx:idx+len(toks)];idx+=len(toks)
  assert len({w['segment'] for w in ws})==1,line
  for size in range(88,71,-1):
   widths=[width(w,size) for w in toks];total=sum(widths)+32.5*(len(toks)-1)
   if total+0.05*max(widths)+10<=996:break
  else:raise ValueError(('Caption too wide even at 72px; change grouping',line))
  x=(1080-total)/2
  for w,wd in zip(ws,widths):w['x']=round((x+wd/2)/1080,6);x+=wd+32.5
  groups.append({'text':' '.join(toks),'words':ws,'start':ws[0]['start'],'font_size':size})
 assert idx==len(words),(idx,len(words))
 for i,g in enumerate(groups):
  g['end']=groups[i+1]['start'] if i+1<len(groups) else min(r['totalFrames'],max(g['words'][-1]['end'],g['start']+1))
  assert g['end']-g['start']>=2,('Merge this too-short cue',g)
 style={'fontName':'HelveticaNeue-CondensedBlack','fontSize':49.7,'alignment':'center','color':'#FFFFFF','tracking':1.5,'outline':{'enabled':True,'color':'#000000D2','width':5}}
 base=[];highlight=[]
 for g in groups:
  for w in g['words']:
   args={'content':w['text'],'transform':{'x':w['x'],'y':.40}}
   group_style={**style,'fontSize':round(style['fontSize']*g['font_size']/88,3)}
   base.append({'startFrame':g['start'],'endFrame':g['end'],**args,'style':group_style})
   hs=max(g['start'],w['start']);he=min(g['end'],w['end'])
   if he-hs>=2:highlight.append({'startFrame':hs,'endFrame':he,**args,'style':{**group_style,'color':'#FFD54F'}})
 def stamp(f):
  n=round(f*1000/FPS);h,n=divmod(n,3600000);m,n=divmod(n,60000);s,n=divmod(n,1000);return f'{h:02d}:{m:02d}:{s:02d},{n:03d}'
 mapfile=out/'en_native_caption_map.json';srt=out/'en_captions_110.srt'
 assert not a.apply or (not (out/'en_native_apply_receipt.json').exists())
 mapfile.write_text(json.dumps({'fps':FPS,'speed':1.1,'groups':groups,'base_count':len(base),'highlight_count':len(highlight)},ensure_ascii=False,indent=2)+'\n')
 srt.write_text(''.join(f"{i+1}\n{stamp(g['start'])} --> {stamp(g['end'])}\n{g['text']}\n\n" for i,g in enumerate(groups)))
 print(json.dumps({'words':len(words),'cues':len(groups),'short_under_8_frames':[g['text'] for g in groups if g['end']-g['start']<8],'over_20_cps':[g['text'] for g in groups if len(g['text'])*FPS/(g['end']-g['start'])>20], 'srt':str(srt)},ensure_ascii=False),flush=True)
 if not a.apply:return
 c=PalmierConnection();c.connect()
 def check():
  pr=c.read_tool('manage_project',{'action':'list'});t=c.read_tool('get_timeline',{})
  assert Path(pr['active']['path']).resolve()==PROJECT and Path(pr['visible']['path']).resolve()==PROJECT
  assert t['id']==r['timeline_id']
  return t
 old=check();assert not [clip for tr in old['tracks'] for clip in tr['clips'] if clip.get('mediaType')=='text'],'Existing text: inspect rather than add duplicates'
 apply_receipt=out/'en_native_apply_receipt.json';journal={'status':'adding_base'}
 def save():apply_receipt.write_text(json.dumps(journal,ensure_ascii=False,indent=2)+'\n')
 save()
 for label,entries in [('base',base),('highlight',highlight)]:
  check();result=c.request('tools/call',{'name':'add_texts','arguments':{'entries':entries}})
  journal[label]=result;journal['status']=label+'_attempted';save()
  if result.get('isError'):raise RuntimeError(result)
  check()
 journal['status']='added';journal['after']=check();save()
 print('Caption layers added. Inspect and listen before export.',flush=True)
if __name__=='__main__':main()
