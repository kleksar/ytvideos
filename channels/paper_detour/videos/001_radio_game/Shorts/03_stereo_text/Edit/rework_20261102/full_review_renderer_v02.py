import json,difflib,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Shorts/03_stereo_text');out=p/'Work/rework_20261102/full_review_forced_v02';out.mkdir(parents=True,exist_ok=True);scenes=json.loads((p/'Edit/rework_20261102/motion_prepared.json').read_text());audio=p/'Source/Voice/pro_v2/voice_en.mp3'
word_map=json.loads((p/'Edit/rework_20261102/timing_forced_draft.json').read_text())
import hashlib
if hashlib.sha256(audio.read_bytes()).hexdigest()!=word_map['audio_sha256']:raise ValueError('Recording hash mismatch')
words=word_map['words'];groups=[];n=0
for line in (p/'Edit/rework_20261102/subtitle_groups_draft.txt').read_text().splitlines():
 tokens=line.split(); selected=words[n:n+len(tokens)];n+=len(tokens)
 if len(selected)!=len(tokens) or any(re.sub(r'[^\w]','',a.casefold())!=re.sub(r'[^\w]','',b['text'].casefold()) for a,b in zip(tokens,selected)):raise ValueError('Transcript mismatch')
 groups.append([(token,w['start'],w['end']) for token,w in zip(tokens,selected)])
if n!=len(words):raise ValueError('Incomplete transcript')
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/ChalkboardSE.ttc',36,index=2)
blank=Image.new('RGBA',(540,120)).tobytes();cache={}
def frame(group,active):
 key=(tuple(x[0] for x in group),active)
 if key in cache:return cache[key]
 im=Image.new('RGBA',(540,120));d=ImageDraw.Draw(im);tokens=[x[0] for x in group];width=d.textlength(' '.join(tokens),font=font);x=(540-width)/2
 for i,word in enumerate(tokens):
  d.text((x+1,63),word,font=font,anchor='ls',fill=(0,0,0,160),stroke_width=2,stroke_fill=(0,0,0,160))
  d.text((x,62),word,font=font,anchor='ls',fill=(255,218,70,255) if i==active else (255,245,224,255),stroke_width=2,stroke_fill=(22,23,24,255));x+=d.textlength(word+' ',font=font)
 cache[key]=im.tobytes();return cache[key]
for name,start,dur in [('full',0,40.9)]:
 dest=out/f'{name}_REVIEW.mp4'
 inputs=[]
 for scene in scenes: inputs.extend(['-i',scene['video']])
 filters=''.join(f'[{i}:v]trim=end_frame={scenes[i]["frames"]},setpts=N/(30*TB),scale=540:960:flags=lanczos[v{i}];' for i in range(8))
 filters+=''.join(f'[v{i}]' for i in range(8))+'concat=n=8:v=1:a=0[bg];[bg][8:v]overlay=0:690:shortest=1[v]'
 cmd=['ffmpeg','-v','error','-y',*inputs,'-f','rawvideo','-pixel_format','rgba','-video_size','540x120','-framerate','30','-i','pipe:0','-i',str(audio),'-t',str(dur),'-filter_complex',filters,'-map','[v]','-map','9:a:0','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(dest)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 for k in range(round(dur*30)):
  t=start+k/30
  g=groups[0]
  for candidate in groups:
   if candidate[0][1]>t:break
   g=candidate
  active=None
  for j,(_,begin,end) in enumerate(g):
   stop=g[j+1][1] if j+1<len(g) else float('inf')
   if begin<=t<stop:active=j;break
  proc.stdin.write(frame(g,active))
 proc.stdin.close();err=proc.stderr.read();rc=proc.wait()
 if rc:raise RuntimeError(err.decode())
 print('prepared',dest,flush=True)
