from pathlib import Path
from PIL import Image, ImageFilter
import subprocess,sys
p=Path(__file__).resolve().parent
src=Image.open(p.parent/'source.png').convert('RGB')
mask=Image.open(p/'mask_filled_v3.png').convert('L')
paint=Image.open(p/'background_v3.png').convert('RGB')
bgmask=mask.filter(ImageFilter.MaxFilter(49)).filter(ImageFilter.GaussianBlur(2))
bg=Image.composite(paint,src,bgmask).convert('RGBA')
fg=Image.open(p/'foreground_v3.png').convert('RGBA')
w,h=src.size; out=p/'layered_outline_fix_v04.mp4'
cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',f'{w}x{h}','-r','30','-i','pipe:0','-vf','scale=1920:1080:flags=lanczos,setsar=1','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-an',str(out)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
 for i in range(180):
  dx=12.0*i/179
  moved=fg.transform((w,h),Image.Transform.AFFINE,(1,0,dx,0,1,0),resample=Image.Resampling.BICUBIC)
  frame=Image.alpha_composite(bg,moved)
  if i in (0,90,179):frame.convert('RGB').save(p/f'layered_v04_frame_{i:03}.png')
  proc.stdin.write(frame.tobytes())
 proc.stdin.close()
 if proc.wait()!=0:raise RuntimeError('encode failed')
except:
 proc.kill();raise
