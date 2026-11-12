from build_review_edit import DATA, dump, read, sha
from pathlib import Path
import shutil

for name, manifest in read(Path(__file__).parent/'long-generation-queue-v01.json').items():
 ep=DATA[name][0]
 images=ep/'Source/Images/v01'; images.mkdir(parents=True,exist_ok=True)
 missing=[]
 for i,rec in enumerate(manifest,1):
  if not rec['generation_path']:
   missing.append(i); continue
  src=Path(rec['generation_path']); dst=images/f'S{i:03d}.png'
  if not dst.exists():
   with src.open('rb') as a,dst.open('xb') as b: shutil.copyfileobj(a,b)
  else: assert sha(src)==sha(dst),dst
 path=ep/'Work/scene-prompt-manifest-v01.json'
 if not missing and not path.exists():dump(path,manifest)
 print(name,len(manifest)-len(missing),'/',len(manifest),'missing',missing)
