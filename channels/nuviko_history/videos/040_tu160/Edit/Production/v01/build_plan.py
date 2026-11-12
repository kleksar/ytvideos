from pathlib import Path
import re, json, hashlib
ROOT=Path(__file__).resolve().parents[3]
# Production/040_tu160/Edit/Production/v01 -> episode root
ROOT=Path(__file__).resolve().parents[3]
voice=ROOT/'Source/Audio/word_map_mix_v01.json'
words=json.loads(voice.read_text())['words']
visual=(ROOT/'Storyboard/visual_score_v03.md').read_text()
scenes=[]
for sid,title in re.findall(r'^### (\d{3}) · (.+)$',visual,re.M):
    m=re.search(r'“(.*?)”\s*(?:→\s*“(.*?)”)?',title)
    if not m: raise SystemExit(f'no range scene {sid}')
    start_phrase,end_phrase=m.groups()
    def norm(s): return [re.sub(r"[^\w'-]",'',x.lower()) for x in re.findall(r"[\w’'-]+",s) if re.sub(r"[^\w'-]",'',x)]
    toks=[re.sub(r"[^\w'-]",'',w['text'].lower()) for w in words]
    def find(seq,after):
        for i in range(after,len(toks)-len(seq)+1):
            if toks[i:i+len(seq)]==seq:return i
        return None
    a=norm(start_phrase); b=norm(end_phrase) if end_phrase else a
    si=find(a,0)
    if si is None: raise SystemExit(f'missing start phrase {sid}: {start_phrase}')
    ei=find(b,si)
    if ei is None: raise SystemExit(f'missing end phrase {sid}: {end_phrase}')
    purpose=re.search(r'\*\*Purpose/situation:\*\* (.+)',visual[visual.index(f'### {sid} ·'):],re.S)
    purpose=(purpose.group(1).split('\n')[0].strip() if purpose else 'Narrative scene')
    candidates=list((ROOT/'Source/Images').glob(f'scene_{sid}_v*.*'))
    image=max(candidates,key=lambda p:int(re.search(r'_v(\d+)',p.stem).group(1))) if candidates else None
    if image is None: raise SystemExit(f'missing image {sid}')
    scenes.append({'id':sid,'image':image,'start':words[si]['start'],'phrase_end':words[ei+len(b)-1]['end'],'purpose':purpose})
if len(scenes)!=119: raise SystemExit(f'expected 119 scenes got {len(scenes)}')
# Voice-aligned holds: each visual brief enters at its trigger and holds through the next trigger.
frame_count=21773
fps=30
moves=[]
for i,s in enumerate(scenes):
    start=0 if i==0 else round(scenes[i]['start']*fps)
    end=round(scenes[i+1]['start']*fps) if i+1<len(scenes) else frame_count
    direction='left_to_right' if i%2==0 else 'right_to_left'
    zoom='in' if i%2==0 else 'out'
    if direction=='left_to_right': c0,c1=.506,.494
    else: c0,c1=.494,.506
    if zoom=='in': z0,z1=1.025,1.045
    else: z0,z1=1.045,1.025
    moves.append({'image':str(s['image']),'start_frame':start,'end_frame':end,'direction':direction,'zoom':zoom,'camera':{'focus':[.5,.5],'subject':s['purpose'],'reason':f"Hold the scene's stated purpose in frame through its narration beat; restrained whole-image motion.",'start':{'center':[c0,.5],'scale':z0},'end':{'center':[c1,.5],'scale':z1}}})
plan={'channel':'nuviko','format':'long','fps':30,'canvas':[2560,1440],'source_transfer':'srgb','enforce_scene_duration':False,'audio':'../../../Source/Audio/mix_en_v01.wav','audio_contract':{'final_audio_sha256':hashlib.sha256((ROOT/'Source/Audio/mix_en_v01.wav').read_bytes()).hexdigest(),'applied_speed':1.1,'speed_evidence':'../../../Source/Voice/voice_mix_v02.json'},'scenes':moves,'subtitles':{'mode':'words','words':'../../../Source/Audio/word_map_mix_v01.json','transcript':'../../../Source/Voice/voice_en_text_v01.txt','end_frame':frame_count}}
# Use the exact one-line phrases built from the accepted spoken transcript.
cues=json.loads((ROOT/'Work/production-20261105-v01/subtitles/cues_v01.json').read_text())['cues']
plan['subtitles']['phrases']=[cue['text'] for cue in cues]
plan['subtitles']['boundary_exceptions']=[{'left':'speeds of more than','right':'two thousand kilometers','reason':'User approved this one forced line boundary because the exact spoken sentence has no syntax-safe one-line grouping at the fixed Nuviko 84 px long-video style.','user_approved':True,'approval_evidence':'../../../Research/USER_DECISIONS_v01.md','approval_sha256':'6a9410b1553ab7124b62f464753cce387959b9ec819b594ef2066fd4a3264d14'}]
# Paths are relative to plan directory, so adjust to be correct from Edit/Production/v01
plan['audio']='../../../Source/Audio/mix_en_v01.wav'
plan['subtitles']['words']='../../../Source/Audio/word_map_mix_v01.json'
plan['subtitles']['transcript']='../../../Source/Voice/voice_en_text_v01.txt'
(ROOT/'Edit/Production/v01/plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print(f'wrote {len(moves)} scenes, {frame_count} frames ({frame_count/fps:.3f}s)')
print('duration range',min(x['end_frame']-x['start_frame'] for x in moves),max(x['end_frame']-x['start_frame'] for x in moves))
