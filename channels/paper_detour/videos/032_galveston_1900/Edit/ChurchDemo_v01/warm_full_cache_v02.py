"""Read accepted immutable plan; warm only canonical locked caches. No Palmier calls or changes to render parameters."""
import importlib.util,json,concurrent.futures,sys
from pathlib import Path
ROOT=Path('/Users/diplomat/ytvideos');E=ROOT/'channels/paper_detour/videos/032_galveston_1900';R=E/'Edit/ImageMotion/66072d4dcbfcf7b06778'
spec=importlib.util.spec_from_file_location('canonical_motion',ROOT/'automation/image_motion/run.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=json.loads((E/'Edit/ChurchDemo_v01/full_motion_v02.json').read_text());plan=json.loads((R/'plan.json').read_text())
def work(item):
    n,scene=item;d=R/'cache-warm'/f'{n:03}';d.mkdir(parents=True,exist_ok=True)
    path=m.prepare_finished(scene,c,d,E/'Work/image-motion-66072d4dcbfcf7b06778/scratch'/f'warm-{n:03}')
    (d/'complete.json').write_text(json.dumps({'scene':n,'video':path,'scope':'canonical cache only; no timeline writes'}))
    print(json.dumps({'warm_scene':n,'status':'ready'}),flush=True)
tail='--tail' in sys.argv
selected=[(i+1,s) for i,s in enumerate(plan) if i>=79] if tail else [(i+1,s) for i,s in enumerate(plan) if i>=14]
if tail:selected.reverse()
with concurrent.futures.ThreadPoolExecutor(max_workers=2 if tail else 3) as pool:
    futures=[pool.submit(work,item) for item in selected]
    for f in concurrent.futures.as_completed(futures):f.result()
