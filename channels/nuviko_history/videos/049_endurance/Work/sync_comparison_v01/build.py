import json, pathlib, subprocess, hashlib
from PIL import Image, ImageDraw, ImageFont
root=pathlib.Path.cwd(); out=root/'Work/sync_comparison_v01'; mix=root/'Work/sound_draft_v01/mix_draft_v02.wav';
a=json.load(open(root/'Work/word_map_mix_draft_v01.json'))['words'];b=json.load(open(root/'Work/asr_check_v01/forced_word_map_draft_v01.json'))['words']
windows=[(15,23),(270,278),(550,559.8)];fps=30; w,h=960,540
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',54);small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',25)
flt=';'.join(f'[1:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS[a{i}]' for i,(s,e) in enumerate(windows))+';'+''.join(f'[a{i}]' for i in range(len(windows)))+f'concat=n={len(windows)}:v=0:a=1[aout]'
cmd=['ffmpeg','-hide_banner','-loglevel','error','-n','-f','rawvideo','-pix_fmt','rgb24','-s',f'{w}x{h}','-r',str(fps),'-i','pipe:0','-i',str(mix),'-filter_complex',flt,'-map','0:v','-map','[aout]','-c:v','h264_videotoolbox','-b:v','5M','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-shortest',str(out/'sync_comparison_v01.mp4')]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
cache={}
def word_at(words,t):
 for x in words:
  if x['start']<=t<x['end']:return x['text']
 return '—'
for n,(start,end) in enumerate(windows):
 for frame in range(round((end-start)*fps)):
  t=start+frame/fps; wa=word_at(a,t);wb=word_at(b,t);key=(n,wa,wb)
  if key not in cache:
   im=Image.new('RGB',(w,h),'#111820');d=ImageDraw.Draw(im);d.text((48,35),'TIMING CHECK  •  SAMPLE '+str(n+1)+'/3',font=small,fill='#b7c6d3');d.line((40,92,920,92),fill='#506070',width=2)
   d.text((60,142),'A',font=font,fill='#8db5ff');d.text((150,142),wa,font=font,fill='white');d.text((60,285),'B',font=font,fill='#ffd166');d.text((150,285),wb,font=font,fill='white')
   d.text((48,467),'Same audio. Words shown at two estimated timings.',font=small,fill='#c7d0d8');cache[key]=im.tobytes()
  proc.stdin.write(cache[key])
proc.stdin.close(); rc=proc.wait();
if rc: raise SystemExit(rc)
f=out/'sync_comparison_v01.mp4';(out/'README.md').write_text('Diagnostic only: A provider alignment, B WhisperX forced alignment; 15–23, 270–278, 550–559.8 seconds of user-approved mix. Each displayed word is an individual estimated interval, not the final grouped subtitle design. A/B maps are not verified; 30 fps, with no speed change. User mix SHA256 '+hashlib.sha256(mix.read_bytes()).hexdigest()+'. Output SHA256 '+hashlib.sha256(f.read_bytes()).hexdigest()+'.\n')
print(f)
