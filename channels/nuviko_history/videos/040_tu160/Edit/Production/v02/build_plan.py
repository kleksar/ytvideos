import json, copy, hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[3]
v1=json.loads((root/'Edit/Production/v01/plan.json').read_text()); m=json.loads((root/'Edit/Production/v02/shot_map_draft_v01.json').read_text()); original=v1['scenes']; shots=[]
for shot in m['shots']:
 source=shot['source_scene']; s=copy.deepcopy(original[source-1] if source!=120 else original[26]);s['image']=shot['image'];s['start_frame']=shot['start_frame'];s['end_frame']=shot['end_frame']
 s['camera']['subject']=shot['purpose']
 # Preserve the existing image's movement unless it conflicts with the previous image.
 if shots and s['direction']==shots[-1]['direction']:
  s['direction']='right_to_left' if s['direction']=='left_to_right' else 'left_to_right'
  s['camera']['start']['center'][0],s['camera']['end']['center'][0]=s['camera']['end']['center'][0],s['camera']['start']['center'][0]
 if shots and s['zoom']==shots[-1]['zoom']:
  s['zoom']='out' if s['zoom']=='in' else 'in'
  s['camera']['start']['scale'],s['camera']['end']['scale']=s['camera']['end']['scale'],s['camera']['start']['scale']
 s['camera']['reason']='Keep the subject visible during the narrated beat; restrained whole-image movement, adjusted where necessary to alternate with the preceding shot.'
 shots.append(s)
v1['scenes']=shots;v1['enforce_scene_duration']=True;v1['subtitles'].pop('review',None)
p=root/'Edit/Production/v02/plan.json';p.write_text(json.dumps(v1,indent=2,ensure_ascii=False)+'\n')
assert len(shots)==145 and shots[-1]['end_frame']==21773
assert all(120<=x['end_frame']-x['start_frame']<=180 for x in shots)
assert all(a['end_frame']==b['start_frame'] and a['direction']!=b['direction'] and a['zoom']!=b['zoom'] for a,b in zip(shots,shots[1:]))
assert all(hashlib.sha256(Path(a['image']).read_bytes()).digest()!=hashlib.sha256(Path(b['image']).read_bytes()).digest() for a,b in zip(shots,shots[1:]))
print('Wrote',p,'with',len(shots),'shots')
