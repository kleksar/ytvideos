import json
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history')
out = ROOT/'Source/Graphics/v06'
shots = json.loads((ROOT/'Storyboard/SHOTLIST_v06.json').read_text())
new = json.loads((ROOT/'Storyboard/ACCENT_PLAN_v06.json').read_text())
old = json.loads((ROOT/'Storyboard/CUE_SHEET_v05.json').read_text())
old_input = json.loads((ROOT/'Source/Graphics/v05/caption_input.json').read_text())
old_sources = {c['id']:c for c in old_input['cues']}
scenes=[];cues=[];pairs=[]
prepared=out/'preflight_scenes';prepared.mkdir(exist_ok=True)

def line_boxes(path, count):
    a=np.array(Image.open(path).convert('RGBA'))
    r,g,b,alpha=[a[:,:,i].astype(float) for i in range(4)]
    m=(alpha>30)&(r>160)&(g>110)&(b>70)&(g>.58*r)&(b>.50*g)
    ys,xs=np.where(m);top,bottom=int(ys.min()),int(ys.max())+1
    if count==1:return [[int(xs.min()),top,int(xs.max())+1,bottom]]
    hist=m.sum(axis=1);h=bottom-top
    middle=range(top+int(h*.30),top+int(h*.70))
    # Both rows are broad uppercase paper letters. Choose the least occupied
    # interline row, then retain every face pixel in one authored line box.
    split=min(middle,key=lambda y:(hist[y],abs(y-(top+bottom)/2)))
    boxes=[]
    for ya,yb in [(top,split),(split,bottom)]:
        yy,xx=np.where(m[ya:yb]);boxes.append([int(xx.min()),int(yy.min()+ya),int(xx.max())+1,int(yy.max()+ya)+1])
    return boxes

for cue in old+new:
    scene=next(s for s in shots if s['id']==cue['scene'])
    if cue['id'].startswith('C'):
        item=json.loads(json.dumps(old_sources[cue['id']]))
    else:
        path=out/f"{cue['id']}_raw.png"
        item={'id':cue['id'],'lines':cue['lines'],
              'backend':{'type':'existingPNG','path':str(path),
                         'face':{'mode':'creamOrange','line_boxes':line_boxes(path,len(cue['lines']))},
                         'reference':str(ROOT.parent.parent/'videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png'),
                         'status':'Author inspected all28 raw PNGs: spelling, broad rounded glyphs, paper texture and alpha; final composite pending'},
              'provenance':{'method':'built-in imagegen','record':str(ROOT/'Storyboard/DECISIONS_v06.md')}}
    item['timing']={'status':'measured Lawrence v05 alignment, audible sync UNVERIFIED',
                    'startFrame':cue['startFrame'],'endFrame':cue['endFrame']}
    cues.append(item)
    a,b=cue['startFrame'],cue['endFrame']
    frames=[a+4,(a+b)//2,b-5]
    source=Image.open(scene['framed_path']).convert('RGB')
    for suffix,f in zip(['A','B','C'],frames):
        progress=(f-scene['startFrame'])/(scene['endFrame']-scene['startFrame']-1)
        progress=min(1,max(0,progress))
        k=scene['scale_keys'];z=k[0][1]+(k[1][1]-k[0][1])*progress
        k=scene['position_keys'];x=k[0][1]+(k[1][1]-k[0][1])*progress;y=k[0][2]+(k[1][2]-k[0][2])*progress
        im=source.transform((1920,1080),Image.Transform.AFFINE,(1/z,0,-x*1920/z,0,1/z,-y*1080/z),resample=Image.Resampling.BICUBIC)
        sid=cue['scene']+'_'+cue['id']+'_'+suffix;path=prepared/(sid+'.png');im.save(path)
        scenes.append({'id':sid,'path':str(path)})
        pairs.append({'scene':sid,'cue':cue['id'],'anchor':cue['anchor']})
manifest={k:v for k,v in old_input.items() if k not in ['scenes','cues','pairs']}
manifest.update(scenes=scenes,cues=cues,pairs=pairs)
(out/'caption_input_v06.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(f'{len(cues)} cues, {len(pairs)} actual camera-position composites prepared.')
