import json,sys
from pathlib import Path
root=Path('/Users/diplomat/ytvideos'); sys.path.insert(0,str(root/'automation/image_motion'))
from run import prepare_finished
r=root/'channels/paper_detour/videos/001_radio_game/Edit/ImageMotion/cf5381cee9947236be07'; out=root/'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Edit/renewal_20261102'; config=json.loads((out/'motion.json').read_text()); scenes=json.loads((r/'plan.json').read_text()); scratch=root/'channels/paper_detour/videos/001_radio_game/Work/image-motion-short02-renewal/scratch';scratch.mkdir(parents=True,exist_ok=True);run=out/'motion';run.mkdir(exist_ok=True)
for i,s in enumerate(scenes,1):
 s['video']=prepare_finished(s,config,run,scratch_dir=scratch)
 (out/'motion_prepared.json').write_text(json.dumps(scenes,indent=2,ensure_ascii=False))
 print(f'Prepared {i}/{len(scenes)}',flush=True)
