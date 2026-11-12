import json
from pathlib import Path
from PIL import Image,ImageDraw

ROOT=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history')
g=ROOT/'Source/Graphics/v06/production_final'
m=json.loads((g/'manifest.json').read_text())
assert m['shared_face_height_px']==72,m['shared_face_height_px']
shots=json.loads((ROOT/'Storyboard/SHOTLIST_v06.json').read_text())
cues=sorted(json.loads((ROOT/'Storyboard/CUE_SHEET_v05.json').read_text())+json.loads((ROOT/'Storyboard/ACCENT_PLAN_v06.json').read_text()),key=lambda c:c['startFrame'])
out=ROOT/'Edit/v06/Preflight';out.mkdir(exist_ok=True)
geometries={}
for index in range(0,len(cues),9):
    group=cues[index:index+9];contact=Image.new('RGB',(1440,len(group)*294),'#ddd9cc');dr=ImageDraw.Draw(contact)
    for row,cue in enumerate(group):
        shot=next(s for s in shots if s['id']==cue['scene']);meta=next(c for c in m['cues'] if c['id']==cue['id']);pair=next(p for p in m['pairs'] if p['cue']==cue['id']);geo=next(c for c in pair['comparisons'] if c['anchor']==pair['anchor'])
        geometries[cue['id']]=geo
        bounds=geo['checks']['alpha_bbox_on_canvas']
        up=4.32 if cue['id']=='D03' else (0 if cue['id']=='C06' else 21.6)
        assert 0<=bounds[0] and bounds[2]<=1920 and bounds[1]-up>=0 and bounds[3]+21.6<=1080,(cue['id'],bounds)
        overlay=Image.open(g/meta['png']).convert('RGBA');source=Image.open(shot['framed_path']).convert('RGB')
        for col,frame in enumerate([cue['startFrame'],(cue['startFrame']+cue['endFrame'])//2,cue['endFrame']-1]):
            progress=(frame-shot['startFrame'])/(shot['endFrame']-shot['startFrame']-1)
            k=shot['scale_keys'];z=k[0][1]+(k[1][1]-k[0][1])*progress
            k=shot['position_keys'];x=k[0][1]+(k[1][1]-k[0][1])*progress;y=k[0][2]+(k[1][2]-k[0][2])*progress
            im=source.transform((1920,1080),Image.Transform.AFFINE,(1/z,0,-x*1920/z,0,1/z,-y*1080/z),resample=Image.Resampling.BICUBIC).convert('RGBA')
            left,top=geo['layer_top_left_px'];offset=22 if col==0 else ((-4 if cue['id']=='D03' else -22) if col==2 and cue['id']!='C06' else 0)
            im.alpha_composite(overlay,(left,top+offset))
            contact.paste(im.convert('RGB').resize((480,270),Image.Resampling.LANCZOS),(col*480,row*294))
            dr.text((col*480+5,row*294+273),f"{cue['id']} {cue['scene']} {' / '.join(cue['lines'])} f{frame}",fill='black')
    contact.save(out/f'ALL_CUES_CAMERA_POSITIONS_{index//9+1}.jpg',quality=90)
(out/'geometry.json').write_text(json.dumps(geometries,indent=2))
print('102 real PNG/background camera-position geometry samples, including vertical motion extremes;4 compact contact sheets.')
