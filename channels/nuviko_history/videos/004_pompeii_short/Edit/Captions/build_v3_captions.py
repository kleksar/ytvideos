#!/usr/bin/env python3
import bisect, importlib.util, json, math, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[2]
CAP=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('base',str(ROOT.parent/'003_gus/Edit/Captions/003_build_and_render_captions.py'))
base=importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
script=(ROOT/'Source/Voice/v2/004_en_script.txt').read_text().strip()
data=json.loads((ROOT/'Source/Voice/v2/voice_en.alignment.json').read_text())['alignment']
chars=data['characters']; starts=data['character_start_times_seconds']; ends=data['character_end_times_seconds']
text=''.join(chars)
if text.strip()!=script: raise ValueError('Alignment characters do not match script')
raw,clean=base.tokenize(script,'en')
spans=list(re.finditer(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*[.,!?;:…]*[\"”»]*",text))
if [m.group() for m in spans]!=raw: raise ValueError('Alignment token mismatch')
words=[{'word':w,'start':starts[m.start()],'end':ends[m.start()+len(w)-1]} for m,w in zip(spans,clean)]
plan="POMPEII WASN'T | DESTROYED BY LAVA | THE REAL DANGER | WAS FAR | MORE DEADLY | IN AD 79 | VESUVIUS ERUPTED | BUT INSTEAD | OF RIVERS | OF MOLTEN ROCK | PUMICE | LIGHT VOLCANIC STONES | BEGAN RAINING DOWN | ON THE CITY | AT FIRST | THEY MAY NOT | HAVE SEEMED | LIKE MUCH | OF A THREAT | BUT THE | STONE RAIN CONTINUED | FOR HOURS | STREETS SLOWLY | DISAPPEARED | BENEATH THE DEBRIS | IN SOME PLACES | THE LAYER | OF PUMICE | REACHED AROUND | THREE METRES DEEP | UNDER ITS WEIGHT | ROOFS COLLAPSED | THE NEXT MORNING | BROUGHT | A NEW DANGER | PYROCLASTIC FLOWS | SWEPT | INTO THE CITY | FAST-MOVING CLOUDS | OF SEARING GAS | ASH AND | VOLCANIC PARTICLES | POMPEII WAS BURIED | BENEATH THE ERUPTION | DISCOVER HOW | THE CITY ENDURED | THAT TERRIBLE NIGHT | IN THE | FULL DOCUMENTARY | ON NUVIKO HISTORY".split(' | ')
cues=[]
i=0
for line in plan:
 n=len(line.split());
 if not 1 <= n <= 3: raise ValueError('Caption exceeds 3 words: '+line)
 cues.append((i,i+n)); i+=n
if [x for line in plan for x in line.split()] != [x.upper() for x in clean]: raise ValueError('Caption text mismatch')
cs=[words[a]['start'] for a,b in cues]
ce=cs[1:]+[words[-1]['end']]
if min(b-a for a,b in zip(cs,ce))<.26: raise ValueError(f'Caption duration too short: {[(line, round(b-a,3)) for line,a,b in zip(plan,cs,ce) if b-a<.26]}')
font=ImageFont.truetype(base.FONT,92,index=base.FONT_INDEX)
def width(s,f): return f.getlength(s)+base.TRACKING*max(0,len(s)-1)
peak=max(sum(width(w,font) for w in line.split())+base.WORD_GAP*(len(line.split())-1)+.05*max(width(w,font) for w in line.split()) for line in plan)
if peak>1020: raise ValueError(f'Text too wide: {peak}')
def stamp(sec):
 ms=round(sec*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000); return f'{h:02}:{m:02}:{s:02},{ms:03}'
srt='\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{line}\n' for i,(a,b,line) in enumerate(zip(cs,ce,plan)))
# SRT unchanged from v2.
# Caption plan unchanged from v2.
# Word timings unchanged from v2.
print('WORDS',len(words),'CUES',len(cues),'MAX WIDTH',round(peak),'MIN DURATION',round(min(b-a for a,b in zip(cs,ce)),3),flush=True)
print('\n'.join(plan),flush=True)
duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(ROOT/'Source/Voice/v2/voice_en.mp3')]))
frames=math.ceil(duration*30)
out=CAP/'004_en_v3_caption_overlay.mov'
if out.exists(): raise FileExistsError(out)
cmd=['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgba','-video_size','1080x1920','-framerate','30','-i','pipe:0','-an','-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le',str(out)]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
cache={92:font}
def font_at(size):
 if size not in cache: cache[size]=ImageFont.truetype(base.FONT,size,index=base.FONT_INDEX)
 return cache[size]
for frame in range(frames):
 t=frame/30; ci=bisect.bisect_right(cs,t)-1; im=Image.new('RGBA',(1080,1920),(0,0,0,0))
 if ci>=0 and t<ce[ci]:
  a,b=cues[ci]; w=words[a:b]; shown=[x.upper() for x in clean[a:b]]; widths=[width(x,font) for x in shown]; x=(1080-sum(widths)-base.WORD_GAP*(len(widths)-1))/2
  active=next((j for j,v in enumerate(w) if v['start']<=t<v['end']),-1); draw=ImageDraw.Draw(im)
  for j,word in enumerate(w):
   f=font; color=(255,255,255,255)
   if j==active:
    dur=max(.001,word['end']-word['start']); ramp=min(.12,dur*.45); q=min(1,(t-word['start'])/ramp,(word['end']-t)/ramp); q=max(0,q); eased=q*q*(3-2*q); f=font_at(round(92*(1+.05*eased))); color=(255,213,79,255)
   charx=x+widths[j]/2-width(shown[j],f)/2
   for ch in shown[j]:
    cw=f.getlength(ch); draw.text((charx+cw/2,round(1920 * (0.27 if 19 <= t < 22 or 42 <= t <= ce[-1] else 0.40))),ch,font=f,fill=color,anchor='mm',stroke_width=5,stroke_fill=(0,0,0,210)); charx+=cw+base.TRACKING
   x+=widths[j]+base.WORD_GAP
 p.stdin.write(im.tobytes())
p.stdin.close(); rc=p.wait()
if rc: raise SystemExit(rc)
print(f'Overlay saved: {out}, frames {frames}',flush=True)
