import json
from pathlib import Path
import numpy as np
from PIL import Image

E=Path(__file__).resolve().parents[2]
q=E/'Storyboard/storyboard_v02.json';story=json.loads(q.read_text())
story['accent_plan']=[c for c in story['accent_plan'] if c['id']!='C09']
for r in story['scenes']:
    if r['scene_id']=='R074':
        r['accent_cue_ids']=[];r['caption_status']='NO TEXT: the newly visible raised ground and spoken turning point already explain the second defense; preserve the wall crest and fill surface.'
q.write_text(json.dumps(story,ensure_ascii=False,indent=2))
oldroot=E/'Storyboard/accent_preflight_v04';old=json.loads((oldroot/'manifest.json').read_text());oldc={c['id']:c for c in old['cues']}
d={'version':1,'canvas':[1672,941],'face_height_px':88,'min_face_height_px':72,'anchors':{'primary':{'center':[.5,.2],'max_width_px':1300,'max_height_px':300},'alternate':{'center':[.22,.2],'max_width_px':670,'max_height_px':300}},'scenes':[],'cues':[],'pairs':[]}
byid={r['scene_id']:r for r in story['scenes']};used=set()
for c in story['accent_plan']:
    cid=c['id'];lines=c['lines']
    if cid.startswith('C'):
        oc=oldc[cid];backend={'type':'existingPNG','path':str(oldroot/oc['png']),'face':{'mode':'mask','path':str(oldroot/oc['face_mask']),'line_boxes':oc['metrics']['face_line_boxes']},'reference':str(E/'Source/Images/church_v02/T01_v01.png'),'status':'Retained accepted exact glyph PNG; new timing and paired composites require recheck'};lines=oc['lines']
    else:
        src=E/('Source/Images/church_v02' if cid.startswith('T') else 'Source/Images/revision_v02')/(cid+'_v01.png')
        a=np.asarray(Image.open(src).convert('RGBA')).astype(float);r,g,b,alpha=a.transpose(2,0,1);m=(alpha>30)&(r>160)&(g>110)&(b>70)&(g>.58*r)&(b>.50*g)
        counts=m.sum(1);h,w=m.shape;lo=int(h*.35);hi=int(h*.65)
        # Select a low-density separator near the middle; line boxes retain all small face flecks.
        cut=min(range(lo,hi),key=lambda y:(counts[max(0,y-2):y+3].sum(),abs(y-h/2)))
        backend={'type':'existingPNG','path':str(src),'face':{'mode':'creamOrange','line_boxes':[[0,0,w,cut],[0,cut,w,h]]},'reference':'/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png','status':'Imagegen glyphs individually viewed: exact spelling, cream face/orange cut layers; measured mask and composites pending'}
    d['cues'].append({'id':cid,'lines':lines,'backend':backend,'provenance':{'record':str(q),'decision':c['decision']},'timing':{'status':'ALIGNMENT_BASED_UNLISTENED','global_frames':[c['in_frame'],c['out_frame_exclusive']]}})
    scene_ids=[c['scene_id']]+(['R056'] if cid=='C06' else [])
    for sid in scene_ids:
        if sid not in used:
            d['scenes'].append({'id':sid,'path':str(E/byid[sid]['image_path'])});used.add(sid)
        d['pairs'].append({'scene':sid,'cue':cid,'anchor':c['anchor']})
out=E/'Edit/ChurchDemo_v01/full_caption_input_v02.json';out.write_text(json.dumps(d,ensure_ascii=False,indent=2));print(out)
