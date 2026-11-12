from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from PIL import Image,ImageDraw,ImageFont
import json,math,subprocess,time
EP=Path('/Users/diplomat/ytvideos/stories/videos/016_marseille_1720'); W=Path(__file__).parent
D=W/'states'; C=W/'clips'; D.mkdir(exist_ok=True); C.mkdir(exist_ok=True)
scenes=json.loads((EP/'Edit/ImageMotion/sources.json').read_text()); ranges=json.loads((EP/'Work/layered_motion_v01/scene_ranges.json').read_text())
old=json.loads((EP/'Edit/Captions/word_states_manifest_source_v01.json').read_text()); info={x['id']:x for x in old['stateFiles']}; timeline=old['timeline']
fontpath='/System/Library/Fonts/Supplemental/Georgia Bold.ttf'; ss=2
font=ImageFont.truetype(fontpath,round(54*1080/941*ss)); space=font.getlength(' '); pad=round(25*1080/941); bottom=round(871*1080/941); height=140; top=bottom-height
# Original approved width in 1920x1080 coordinates.
max_text=1180*1080/941-2*pad
cues=[]
for t in timeline:
 item=info[t['image_id']]; cue=t['cue']
 if not cues or cues[-1]['cue']!=cue:cues.append({'cue':cue,'text':item['text'],'states':[]})
 cues[-1]['states'].append((t,item['active_index']))
groups=[]
for cue in cues:
 if groups and not groups[-1]['text'].rstrip().endswith(('.', '?', '!')) and font.getlength(groups[-1]['text']+' '+cue['text'])/ss<=max_text:
  g=groups[-1]; offset=len(g['text'].split()); g['text']+=' '+cue['text']; g['states'] += [(t,i+offset) for t,i in cue['states']]
 else: groups.append({'text':cue['text'],'states':list(cue['states'])})
# Fixed geometry for every cue, derived from font metrics including ascenders and descenders.
asc,desc=font.getmetrics(); pad_y=round(15*1080/941); panel_h=math.ceil((asc+desc)/ss+2*pad_y); panel_top=height-panel_h
blank=D/'blank.png'; Image.new('RGBA',(1920,height)).save(blank,compress_level=1)
parts=[]
if timeline[0]['startFrame']>0:parts.append((blank,0,timeline[0]['startFrame']))
for gi,g in enumerate(groups):
 text=g['text']; tokens=text.split(); width=font.getlength(text)/ss; panel_w=math.ceil(width+2*pad); x0=round(960-panel_w/2)
 for t,active in g['states']:
  p=D/f'{gi:04}_{active:02}.png'
  if not p.exists():
   im=Image.new('RGBA',(1920*ss,height*ss)); dr=ImageDraw.Draw(im)
   dr.rectangle((x0*ss,panel_top*ss,(x0+panel_w)*ss-1,height*ss-1),fill='#F3E9D5')
   baseline=(panel_top+pad_y)*ss+asc; pen=(960-width/2)*ss
   for i,word in enumerate(tokens):
    dr.text((round(pen),baseline),word,font=font,anchor='ls',fill=('#AD6900' if i==active else '#302D27'),stroke_width=0); pen+=font.getlength(word)+space
   im.resize((1920,height),Image.Resampling.LANCZOS).save(p,compress_level=1)
  parts.append((p,t['startFrame'],t['endFrame']))
concat=W/'subtitles.ffconcat'; lines=['ffconcat version 1.0']
for p,a,b in parts: lines += [f"file '{p}'",'option framerate 30',f'duration {(b-a)/30:.9f}']
lines += [f"file '{parts[-1][0]}'",'option framerate 30']; concat.write_text('\n'.join(lines)+'\n')
print(json.dumps({'stage':'subtitles_ready','old_cues':len(cues),'new_cues':len(groups),'panel_height':panel_h,'highlight':'#AD6900'}),flush=True)
start=time.monotonic()
def make(i):
 s=scenes[i]; n=ranges[i]['frames']; out=C/f'{i+1:03}.mp4'; mode=i%4
 if mode<2:
  sign=1 if mode==0 else -1; e=f'{sign}*(-28.944+57.888*on/{n-1})'
  vf=f"scale=2112:1188:flags=lanczos,perspective=x0='{e}':y0=0:x1='W+({e})':y1=0:x2='{e}':y2=H:x3='W+({e})':y3=H:interpolation=cubic:eval=frame,crop=1920:1080:96:54,setsar=1,format=yuv420p"
 else:
  # output frames are calculated in one continuous linear progression
  z=f'1.035+0.035*on/{n-1}' if mode==2 else f'1.07-0.035*on/{n-1}'
  vf=f"scale=2560:1440:flags=lanczos,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,setsar=1,format=yuv420p"
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-loop','1','-framerate','30','-i',s['image'],'-vf',vf,'-frames:v',str(n),'-an','-c:v','h264_videotoolbox','-b:v','14M','-pix_fmt','yuv420p',str(out)]
 subprocess.run(cmd,check=True); return out
with ThreadPoolExecutor(max_workers=2) as pool:
 for k,f in enumerate(as_completed([pool.submit(make,i) for i in range(len(scenes))]),1):
  f.result()
  if k%20==0 or k==len(scenes):print(json.dumps({'stage':'scenes','done':k,'elapsed':round(time.monotonic()-start)}),flush=True)
cl=W/'clips.ffconcat';cl.write_text('ffconcat version 1.0\n'+''.join(f"file '{C/f'{i+1:03}.mp4'}'\n" for i in range(len(scenes))))
picture=W/'picture.mp4'; subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n','-f','concat','-safe','0','-i',str(cl),'-c','copy',str(picture)],check=True)
for p in C.iterdir():p.unlink()
out=EP/'Deliverables/NuvikoHistory_016_Marseille_ffmpeg_v03.mp4'; audio=EP/'Source/Audio/original_narration.m4a'
filt=f'[1:v]fps=30,format=rgba[sub];[0:v][sub]overlay=0:{top}:shortest=1:format=auto,scale=2560:1440:flags=lanczos,setsar=1,format=yuv420p[v]'
cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-i',str(picture),'-f','concat','-safe','0','-i',str(concat),'-i',str(audio),'-filter_complex',filt,'-map','[v]','-map','2:a:0','-c:v','h264_videotoolbox','-b:v','20M','-pix_fmt','yuv420p','-c:a','copy','-t','537.5','-movflags','+faststart',str(out)]
print(json.dumps({'stage':'final_render','elapsed':round(time.monotonic()-start)}),flush=True);subprocess.run(cmd,check=True)
print(json.dumps({'stage':'complete','output':str(out),'elapsed':round(time.monotonic()-start)}),flush=True)
