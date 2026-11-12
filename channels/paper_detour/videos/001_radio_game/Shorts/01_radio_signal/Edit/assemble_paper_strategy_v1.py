#!/usr/bin/env python3
"""Build distinct short timeline via Palmier. Refuse unexpected project/contents."""
import sys,json,time
from pathlib import Path
ROOT=Path('/Users/diplomat/ytvideos')
sys.path.insert(0,str(ROOT/'automation/palmier'))
from inspect_connection import PalmierConnection
project=Path('/Users/diplomat/Documents/Palmier Pro/Paper Detour 001 Short 01.palmier')
base=ROOT/'channels/paper_detour/videos/001_radio_game/Shorts/01_radio_signal/Source'
pics=base/'Images/paper_strategy_v1'; sound=base/'Audio/strategy_v1'; voice=base/'Voice/strategy_v1/generated/voice_en.mp3'
files={'study':pics/'study_bg.png','station':pics/'station_bg.png','tape':pics/'tape_deck_close_bg.png','screen':pics/'computer_close_bg.png','cassette':pics/'cassette_fg.png','radio':pics/'radio_fg.png','computer':pics/'computer_fg.png','wave':pics/'wave_fg.png','software':pics/'software_text_fg.png','data':pics/'data_text_fg.png','voice':voice,'music':sound/'music_bed_56s_synth_stereo.wav','motor':sound/'sfx_tape_motor_synth_5s.wav','grain':ROOT/'channels/paper_detour/videos/001_radio_game/Source/Graphics/film_grain_8s_prores4444.mov'}
receipt=Path(__file__).with_name('palmier_strategy_v1_receipt.json')
if receipt.exists(): raise SystemExit('Receipt exists; inspect it and timeline before any retry')
for f in files.values():
 if not f.exists(): raise ValueError(f'Missing: {f}')
c=PalmierConnection();c.connect()
def call(n,a):
 r=c.request('tools/call',{'name':n,'arguments':a})
 if r.get('isError'): raise RuntimeError(f'{n} {r}')
 return json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))
def guard():
 p=call('manage_project',{'action':'list'});t=call('get_timeline',{})
 if any(Path((p.get(k) or {}).get('path','')).resolve()!=project for k in ('active','visible')): raise RuntimeError('Wrong active/visible project')
 if t['id']!='7178D5B6' or (t['fps'],t['width'],t['height'])!=(30,1080,1920):raise RuntimeError('Wrong timeline')
 ex=call('manage_exports',{'action':'list'})['exports']
 if any(x.get('status') not in ('completed','failed','cancelled','canceled') for x in ex):raise RuntimeError('Export active')
 return t
# Session-target open affects visible window, requested/authorized after editor was freed.
call('manage_project',{'action':'open','id':'58F68144-6D3B-49F7-9B95-544EEF067CAB'})
t=guard()
if t['tracks'] or t['totalFrames']:raise RuntimeError('Timeline is not empty')
state={'project':str(project),'timeline':'7178D5B6','status':'in_progress','media':{},'clips':{},'steps':[]}
def save():receipt.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')
def mutate(n,a):
 guard();state['pending']={'tool':n,'args':a};save()
 result=call(n,a);state['steps'].append({'tool':n,'args':a,'result':result});state.pop('pending');save();return result
for key,path in files.items():
 r=mutate('import_media',{'source':{'path':str(path)},'folder':'Short01'})
 state['media'][key]=r['mediaRef'];save()
media=state['media']
def add(label,rows):
 r=mutate('add_clips',{'entries':[{'mediaRef':media[k],'startFrame':s,'endFrame':e,**({'includeAudio':False} if k=='grain' else {})} for k,s,e in rows]})
 state['clips'][label]=r['clips'];save();return r['clips']
def props(clip,**kw): return mutate('set_clip_properties',{'clipIds':[clip['id']],**kw})
def keys(clip,prop,values): return mutate('set_keyframes',{'clipId':clip['id'],'property':prop,'keyframes':values})
# Primary images; interrupted long/close shots are independent, no jump cuts.
bg=add('background',[('study',0,150),('station',150,350),('tape',350,480),('screen',480,660),('study',660,750),('station',750,885)])
for i,cl in enumerate(bg):
 # modest motion on alternate shots; scale/position use canvas coordinates
 span=cl['endFrame']-cl['startFrame'] if 'endFrame' in cl else [150,200,130,180,90,135][i]
 if i in (1,3,5): keys(cl,'scale',[[0,1.02,1.02],[span-1,1.06,1.06]])
# layer on desk at first close shot
cass=add('cassette',[('cassette',0,150)])[0]
props(cass,transform={'centerX':0.50,'centerY':0.64,'width':0.85,'height':0.32},fadeInFrames=5,fadeOutFrames=5)
keys(cass,'position',[[0,0.085,0.48],[149,0.105,0.48]])
# Discrete explanation wave emanating from tower. One coordinated gesture.
wave=add('wave',[('wave',280,340)])[0]
props(wave,transform={'centerX':0.52,'centerY':0.32,'width':0.78,'height':0.18},fadeInFrames=8,fadeOutFrames=9)
# later desk composite, computer resized to sit on tabletop
computer=add('computer',[('computer',660,750)])[0]
props(computer,transform={'centerX':0.50,'centerY':0.64,'width':0.80,'height':0.30})
# accents: one coherent graphic gesture, gentle fade on freely appearing text
texts=add('text',[('software',102,149),('data',589,650)])
props(texts[0],transform={'centerX':0.5,'centerY':0.32,'width':0.82,'height':0.15},fadeInFrames=6,fadeOutFrames=7)
props(texts[1],transform={'centerX':0.5,'centerY':0.25,'width':0.7,'height':0.14},fadeInFrames=5,fadeOutFrames=7)
# Voice ends naturally; background bed extends to matching final frame
v=add('voice',[('voice',0,883)])[0]
m=add('music',[('music',0,885)])[0]
props(m,volumeDb=-7,fadeInFrames=12,fadeOutFrames=18)
# Soft transport sound only while tape-deck is visible; attenuate source, trim.
motor=add('motor',[('motor',403,470)])[0]
props(motor,volumeDb=-22,fadeInFrames=6,fadeOutFrames=8)
# Repeat original 8 s grain rather than altering media; preserve established opacity.
grain=add('grain',[('grain',0,240),('grain',240,480),('grain',480,720),('grain',720,885)])
for cl in grain: props(cl,opacity=0.5)
t=guard();state.update(status='assembled',final=t);save();print(json.dumps({'status':'assembled','project':str(project),'timeline':'7178D5B6','tracks':len(t['tracks']),'frames':t['totalFrames'],'receipt':str(receipt)}))
