import json, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ep=Path('/Users/diplomat/ytvideos/channels/scenes_on_repeat/videos/compilation-two-trailers')
w=ep/'Work/v01'; out=ep/'Deliverables/movie-trailers-compilation-v02.mp4'
assert not out.exists()
def time(s):
    h,m,rest=s.split(':');sec,ms=rest.split(',');return (int(h)*3600+int(m)*60+int(sec))*24+round(int(ms)*24/1000)
cues=[]
for block in (ep/'Deliverables/movie-trailers-compilation-v01.en.srt').read_text().strip().split('\n\n'):
    lines=block.splitlines(); a,b=lines[1].split(' --> '); cues.append((time(a),time(b),' '.join(lines[2:])))
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',38)
blank=Image.new('RGBA',(1280,150),(0,0,0,0)).tobytes(); cache={}
for _,_,text in cues:
    im=Image.new('RGBA',(1280,150),(0,0,0,0));d=ImageDraw.Draw(im)
    d.text((640,65),text,font=font,anchor='mm',fill=(249,238,214,255),stroke_width=3,stroke_fill=(12,16,23,255))
    cache[text]=im.tobytes()
cmd=['ffmpeg','-v','error','-n','-f','concat','-safe','0','-i',str(w/'list.txt'),'-f','f32le','-ar','48000','-ac','2','-i',str(w/'edge-mix.f32le'),'-f','f32le','-ar','48000','-ac','2','-i',str(w/'home-mix.f32le'),'-f','rawvideo','-pixel_format','rgba','-video_size','1280x150','-framerate','24','-i','pipe:0','-filter_complex','[0:v]setpts=N/(24*TB)[base];[base][3:v]overlay=0:570:shortest=1:format=auto,format=yuv420p[v];anullsrc=r=48000:cl=stereo:d=3[s0];anullsrc=r=48000:cl=stereo:d=3[s1];[1:a][s0][2:a][s1]concat=n=4:v=0:a=1[a]','-map','[v]','-map','[a]','-frames:v','2448','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-b:a','256k','-movflags','+faststart',str(out)]
(ep/'Edit/render-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
with open(w/'render.log','wb') as log:
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
    try:
        for frame in range(2448):
            matches=[text for a,b,text in cues if a<=frame<b]
            p.stdin.write(cache[matches[-1]] if matches else blank)
    finally:
        p.stdin.close()
    code=p.wait()
if code: raise RuntimeError('FFmpeg failed: '+(w/'render.log').read_text())
print('Final render completed',flush=True)
