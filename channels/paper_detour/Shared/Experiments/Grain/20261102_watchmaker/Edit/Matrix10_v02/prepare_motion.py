"""Reuse canonical image-motion depth/cache and camera presets for one test clip."""
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
PROJECT=next(p for p in HERE.parents if (p/'automation/image_motion/run.py').is_file())
spec=importlib.util.spec_from_file_location('canonical_motion',PROJECT/'automation/image_motion/run.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
image=ROOT/'Source/watchmaker_user.png'
scene={'image':str(image),'image_hash':hashlib.sha256(image.read_bytes()).hexdigest(),
       'depth_input':None,'depth_hash':None,'frames':120,'fps':30,'width':2560,'height':1440,
       'sign':-1,'depth_zoom':1.0,'preset':m.PRESETS['gentle-aligned']}
keys,delta=m.camera_keys({'frames':[0,120]},scene['preset']['camera_factor'],'pan-right',0)
assert delta>0
config={}  # Canonical uv invocation preserves the pinned virtual environment.
out=m.prepare(scene,config,HERE,scratch_dir=ROOT/'Work/matrix10-v02-motion/scratch')
receipt={'parallax_clip':out,'scene':scene,'camera_keys':keys,'visible_camera_dx_canvas':delta,
         'canonical_renderer_sha256':m.file_hash(PROJECT/'automation/image_motion/render.py'),
         'canonical_presets_sha256':m.file_hash(PROJECT/'automation/image_motion/presets.json'),
         'notes':'One4s source render plus2reserveframes from canonicalhelper; use first120only. Same source for all10presets.'}
(HERE/'motion_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2),flush=True)
