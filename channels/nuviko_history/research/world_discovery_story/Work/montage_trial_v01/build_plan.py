import json,hashlib,re
from pathlib import Path
root=Path(__file__).resolve().parents[2]; out=Path(__file__).parent
mix=root/'Work/audio_trial_v01/mix_v03_EXPERIMENT_NOT_REVIEWED.wav';text=root/'Source/Voice/narration-en-v01.txt'
orig=json.loads((root/'Work/subtitles_draft_v01/word_map_source_DRAFT.json').read_text()); words=orig['words']; mixhash=hashlib.sha256(mix.read_bytes()).hexdigest()
# 0.000-second speech offset is supported by five trial v02 correlation windows; source start, speed and edits are unchanged in v03 except end padding. Still draft.
wm={'status':'DRAFT; five sampled windows show no measurable delay; not auditioned or approved','audio_sha256':mixhash,'transcript_sha256':hashlib.sha256(text.read_text().strip().encode()).hexdigest(),'words':words}
(out/'words_EXPERIMENT.json').write_text(json.dumps(wm,ensure_ascii=False,indent=2)+'\n')
cuts=json.loads((root/'Work/voice_qa_v01/scene_cuts_optimized_EXPERIMENT.json').read_text())['blocks']
scenes=[]
for i,b in enumerate(cuts,1):
 candidates=[]
 for p in (root/'Assets/Scenes').glob('S%03d-v*'%i):
  m=re.search(r'-v(\d+)\.(png|jpg)$',p.name)
  if m:candidates.append((int(m.group(1)),p))
 if not candidates:raise ValueError(i)
 p=max(candidates)[1]
 scenes.append({'image':str(p),'start_frame':round(b['cut_in']*30),'end_frame':round(b['cut_out']*30),'direction':'left_to_right' if i%2 else 'right_to_left','zoom':'in' if i%2 else 'out'})
scenes.append({'image':str(root/'Assets/Scenes/END-v01.png'),'start_frame':14513,'end_frame':14813,'role':'end_screen','direction':'right_to_left','zoom':'out'})
plan={'channel':'nuviko','format':'long','source_transfer':'srgb','audio':str(mix),'audio_contract':{'final_audio_sha256':mixhash,'applied_speed':1.1,'speed_evidence':str(root/'Work/audio_trial_v01/REVIEW.md')},'scenes':scenes,'subtitles':{'mode':'words','words':str(out/'words_EXPERIMENT.json'),'transcript':str(text)}}
(out/'edit_EXPERIMENT.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print('experimental plan',len(scenes),'scenes',scenes[-1]['end_frame'],'frames; most selected source files unaccepted')
