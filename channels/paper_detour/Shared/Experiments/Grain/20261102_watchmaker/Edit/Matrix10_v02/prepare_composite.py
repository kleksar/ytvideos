"""Apply saved canonical camera keys to canonical depth render; inspect before grain."""
import json
import subprocess
from pathlib import Path
from PIL import Image

HERE=Path(__file__).resolve().parent
m=json.loads((HERE/'motion_receipt.json').read_text());k=m['camera_keys'];w,h=2560,1440
sw=round(w*k['scale'][0][1]);sh=round(h*k['scale'][0][2])
x0=-w*k['position'][0][1];x1=-w*k['position'][1][1];cy=-h*k['position'][0][2]
f=f"trim=end_frame=120,setpts=PTS-STARTPTS,scale={sw}:{sh}:flags=lanczos,crop=2560:1440:x='{x0:.6f}+({x1-x0:.6f})*n/119':y={cy:.6f},colorspace=iall=bt601-6-625:iprimaries=bt709:itrc=srgb:irange=tv:all=bt709:range=tv:format=yuv420p,setsar=1"
cmd=['ffmpeg','-v','error','-i',m['parallax_clip'],'-vf',f,'-frames:v','120','-pix_fmt','yuv420p','-f','rawvideo','pipe:1']
(HERE/'common_motion_decode.json').write_text(json.dumps({'command':cmd,'filter':f,'visible_camera_dx_pixels':x0-x1,'frames':120},indent=2)+'\n')
samples=[0,10,20,30,40,50,60,70,80,90,100,110,119]
select='+'.join(f'eq(n\\,{i})' for i in samples)
subprocess.run(['ffmpeg','-v','error','-n','-i',m['parallax_clip'],'-vf',f+',select='+select,'-fps_mode','passthrough',str(HERE/'motion_%02d.png')],check=True)
for group in range(2):
    sheet=Image.new('RGB',(1536,1296))
    for j in range(6):
        num=group*6+j+1
        if num>len(samples): break
        im=Image.open(HERE/f'motion_{num:02d}.png');im.thumbnail((768,432));sheet.paste(im,(j%2*768,j//2*432))
    sheet.save(HERE/f'MOTION_PREFLIGHT_{group+1}.jpg',quality=94)
Image.open(HERE/'motion_13.png').resize((1280,720)).save(HERE/'MOTION_END.jpg',quality=95)
print('Saved13common-motion samples plus contact sheets',flush=True)
