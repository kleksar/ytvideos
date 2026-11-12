#!/usr/bin/env python3
"""Compare every encoded frame's active word and band to the caption plan."""
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

OUT=Path(__file__).resolve().parent
plan=json.loads((OUT/'caption_plan_upper_scene05_v2.json').read_text())
override=plan['shot_position_overrides'][0]
begin,end=override['start_frame'],override['end_frame']
expected=[None]*plan['frames']
for i,group in enumerate(plan['groups']):
    for j,word in enumerate(group['words']):
        for upper in (False,True):
            a=max(word['start_frame'],begin) if upper else word['start_frame']
            b=min(word['end_frame'],end) if upper else word['end_frame']
            if upper and a>=b: continue
            if not upper and a>=begin and b<=end: continue
            directory='frames_upper_scene05' if upper else 'frames'
            image=Image.open(OUT/directory/f'{i:02}_{j}.png')
            # Compare alpha geometry and fixed x positions for each caption state.
            bounds=image.getchannel('A').getbbox()
            assert bounds and abs((bounds[0]+bounds[2])/2-540)<5, (i,j,bounds)
            cropped=image.crop((0,740 if upper else 1400,1080,850 if upper else 1510))
            arr=np.asarray(cropped.resize((270,28),Image.Resampling.NEAREST))
            mask=(arr[:,:,0]>180)&(arr[:,:,1]>140)&(arr[:,:,2]<120)&(arr[:,:,3]>20)
            y,x=np.where(mask)
            assert len(x)>1,(i,j)
            for frame in range(a,b):
                if upper or not begin<=frame<end:
                    expected[frame]=(float(x.mean()),upper)
assert expected[514] and expected[514][1] is False
assert expected[515] and expected[515][1] is True
assert expected[754] and expected[754][1] is True
assert expected[755] and expected[755][1] is False
source=OUT/'captions_105_upper_scene05_v2.mov'
vf='[0:v]split=2[a][b];[a]crop=1080:110:0:740,scale=270:28:flags=neighbor[u];[b]crop=1080:110:0:1400,scale=270:28:flags=neighbor[l];[u][l]vstack,format=rgba'
proc=subprocess.Popen(['ffmpeg','-v','error','-i',str(source),'-filter_complex',vf,'-f','rawvideo','-pix_fmt','rgba','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
size=270*56*4; bad=[];seen=0
while True:
    raw=proc.stdout.read(size)
    if not raw: break
    assert len(raw)==size
    arr=np.frombuffer(raw,np.uint8).reshape(56,270,4)
    mask=(arr[:,:,0]>180)&(arr[:,:,1]>140)&(arr[:,:,2]<120)&(arr[:,:,3]>20)
    y,x=np.where(mask); target=expected[seen]
    if (target is None and len(x)>3) or (target is not None and (len(x)<2 or abs(float(x.mean())-target[0])>5 or (y.mean()<28)!=target[1])):
        bad.append({'frame':seen,'expected':target,'actual_x':round(float(x.mean()),1) if len(x) else None})
    seen+=1
stderr=proc.stderr.read().decode(); rc=proc.wait()
print(json.dumps({'frames_read':seen,'frames_planned':plan['frames'],'mismatches':len(bad),'examples':bad[:15],'returncode':rc,'stderr':stderr[:200]}))
assert rc==0 and seen==plan['frames'] and not bad
