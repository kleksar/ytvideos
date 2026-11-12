#!/usr/bin/env python3
"""Check active caption and location across every frame of the v3 overlay."""
import json
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image

OUT=Path(__file__).resolve().parent
plan=json.loads((OUT/'caption_plan_scenes05_06_v3.json').read_text())
expected=[None]*plan['frames']
bands=[(0,515,'frames',1400,2),(515,755,'frames_upper_scene05',740,0),(755,979,'frames_middle_scene06',990,1),(979,plan['frames'],'frames',1400,2)]
for i,group in enumerate(plan['groups']):
    for j,word in enumerate(group['words']):
        for lo,hi,directory,top,band in bands:
            begin=max(word['start_frame'],lo);end=min(word['end_frame'],hi)
            if begin>=end:continue
            image=Image.open(OUT/directory/f'{i:02}_{j}.png')
            bounds=image.getchannel('A').getbbox()
            assert bounds and abs((bounds[0]+bounds[2])/2-540)<5,(i,j,bounds)
            arr=np.asarray(image.crop((0,top,1080,top+110)).resize((270,28),Image.Resampling.NEAREST))
            mask=(arr[:,:,0]>180)&(arr[:,:,1]>140)&(arr[:,:,2]<120)&(arr[:,:,3]>20)
            y,x=np.where(mask);assert len(x)>1,(i,j,band)
            for frame in range(begin,end):expected[frame]=(float(x.mean()),band)
for f,band in [(514,2),(515,0),(754,0),(755,1),(978,1),(979,2)]:
    assert expected[f] and expected[f][1]==band,(f,expected[f])
vf='[0:v]split=3[a][b][c];[a]crop=1080:110:0:740,scale=270:28:flags=neighbor[u];[b]crop=1080:110:0:990,scale=270:28:flags=neighbor[m];[c]crop=1080:110:0:1400,scale=270:28:flags=neighbor[l];[u][m][l]vstack=inputs=3,format=rgba'
source=OUT/'captions_105_scenes05_06_v3.mov'
proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-filter_complex',vf,'-f','rawvideo','-pix_fmt','rgba','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
size=270*84*4;bad=[];seen=0
while True:
    raw=proc.stdout.read(size)
    if not raw:break
    assert len(raw)==size
    arr=np.frombuffer(raw,np.uint8).reshape(84,270,4)
    mask=(arr[:,:,0]>180)&(arr[:,:,1]>140)&(arr[:,:,2]<120)&(arr[:,:,3]>20)
    y,x=np.where(mask);target=expected[seen]
    if (target is None and len(x)>3) or (target is not None and (len(x)<2 or abs(float(x.mean())-target[0])>5 or int(y.mean()//28)!=target[1])):
        bad.append({'frame':seen,'expected':target,'actual_x':round(float(x.mean()),1) if len(x) else None,'actual_band':int(y.mean()//28) if len(x) else None})
    seen+=1
err=proc.stderr.read().decode();rc=proc.wait()
print(json.dumps({'frames_read':seen,'frames_planned':plan['frames'],'mismatches':len(bad),'examples':bad[:15],'returncode':rc,'stderr':err[:200]}))
assert rc==0 and seen==plan['frames'] and not bad
