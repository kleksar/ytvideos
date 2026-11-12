from pathlib import Path
import json, hashlib
root=Path(__file__).resolve().parents[2]
p=json.loads((root/'Work/montage_trial_v01/edit_EXPERIMENT_v03.json').read_text())
# Preview-only substitutions: prioritize evidence-preserving figures and neutral illustrative scenes.
replacements={15:'S011-v01.png',16:'S017-v04.png',17:'S017-v04.png',18:'S018-v03.png',25:'S024-v05.png',32:'S031-v01.png',38:'S044-v01.png',40:'S042-v03.png',42:'S042-v03.png',43:'S039-v01.png',54:'S054-v03.png',55:'S054-v03.png',56:'S054-v03.png',59:'S058-v01.png',66:'S065-v01.jpg',68:'S067-v01.png',69:'S070-v01.png',72:'S073-v02.png',75:'S074-v02.png',81:'S083-v01.png',82:'S082-v03.png',84:'S083-v01.png',86:'S074-v02.png',87:'S074-v02.png',88:'S003-v03.png',89:'S047-v01.png'}
for n,name in replacements.items():
 f=root/'Assets/Scenes'/name
 if not f.exists():raise FileNotFoundError(f)
 p['scenes'][n-1]['image']=str(f)
# End card is intentionally free of held speech captions.
p['subtitles']['end_frame']=14513
out=root/'Work/preview_v01/edit_PREVIEW_v01.json';out.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(root/'Work/preview_v01/substitutions.json').write_text(json.dumps(replacements,indent=2)+'\n')
print(out,hashlib.sha256(out.read_bytes()).hexdigest())
