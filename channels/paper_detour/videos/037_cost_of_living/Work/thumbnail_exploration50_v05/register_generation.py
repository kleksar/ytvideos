import json, shutil, hashlib, sys, time
from pathlib import Path
from PIL import Image

BASE = Path('/Users/diplomat/ytvideos/new_channel/videos/037_cost_of_living/Packaging/Thumbnails/Exploration_50_v05')
GEN = Path('/Users/diplomat/.codex/generated_images/01a19949-1905-7443-ac14-b7437eb482ab')
STATE = BASE / 'generation_manifest.json'
if sys.argv[1] == 'init':
    if STATE.exists():
        raise SystemExit('Existing run: inspect instead of reinitializing')
    state = {'requested':50, 'status':'running', 'started_ns':time.time_ns(), 'baseline':[str(p) for p in GEN.glob('*.png')], 'records':[]}
else:
    state = json.loads(STATE.read_text())
    ident = sys.argv[1]
    if any(r['id']==ident for r in state['records']):
        raise SystemExit('ID already registered; do not regenerate blindly')
    known = set(state['baseline']) | {r['generated_source'] for r in state['records']}
    fresh = [p for p in GEN.glob('*.png') if str(p) not in known and p.stat().st_mtime_ns >= state['started_ns']]
    if len(fresh)!=1:
        raise SystemExit(f'Expected one new generated source, found {len(fresh)}')
    src = fresh[0]
    target = BASE / 'Masters' / f'PD037_v05_{ident}.png'
    target.parent.mkdir(exist_ok=True)
    shutil.copy2(src,target)
    with Image.open(target) as im:
        dimensions=list(im.size)
    state['records'].append({'id':ident,'generated_source':str(src),'master':str(target),'dimensions':dimensions,'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'visual_review':'pending'})
    if len(state['records'])==state['requested']:
        state['status']='generation_complete_review_pending'
STATE.write_text(json.dumps(state,indent=2)+'\n')
print(json.dumps({'registered':len(state['records']),'requested':state['requested'],'status':state['status'],'latest':state['records'][-1] if state['records'] else None}))
