from pathlib import Path
import json
from PIL import Image,ImageOps,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[3];run=root/'Work/montage_trial_v01/subtitle_run_v02b';out=Path(__file__).parent
plan=json.loads((root/'Work/montage_trial_v01/edit_EXPERIMENT_v03.json').read_text())
groups=json.loads((run/'caption_groups.json').read_text())['groups']
for scene_id in (1,14,23,24,63,82):
 s=plan['scenes'][scene_id-1];t=(s['start_frame']+s['end_frame'])/60
 idx=max(i for i,g in enumerate(groups) if g[0]['start']<=t)
 with Image.open(s['image']) as src:
  base=ImageOps.fit(src.convert('RGBA'),(2560,1440),method=Image.Resampling.LANCZOS)
 with Image.open(run/'caption_states'/f'{idx:05d}_0.png') as cap:
  font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Bold.ttf',84)
  y=1288-(17+font.getmetrics()[0])
  base.alpha_composite(cap.convert('RGBA'),(0,y))
 base.thumbnail((960,540),Image.Resampling.LANCZOS);base.convert('RGB').save(out/f'S{scene_id:03d}_static_probe.jpg',quality=90)
 print(scene_id,'group',idx,'time',round(t,2),'words',' '.join(w['text'] for w in groups[idx]))
