from build_review_edit import setup, read, ref
import sys,json,shutil
from pathlib import Path
name=sys.argv[1]
ep,ch,fmt,filename,d,w,canvas,word,wm,transcript,frames,speech,media,speed,out,manifest=setup(name)
pickups=read(Path(__file__).parent/f'{name}-pickups-v02.json')
imgs=ep/'Source/Images/v02'; imgs.mkdir(exist_ok=True)
p=read(manifest)
m=w/'shot-map-v01.json'; shot=read(m)
archive=w/'before-pickups-v01'; archive.mkdir()
shutil.copy2(manifest,archive/manifest.name)
shutil.copy2(m,archive/m.name)
if (w/'sub-prep-v01').exists(): (w/'sub-prep-v01').rename(archive/'sub-prep-v01')
for item in pickups:
 i=item['i']; src=Path(item['path'])
 dest=imgs/f'S{i:03d}.png'; assert not dest.exists()
 shutil.copy2(src,dest)
 p['scenes'][i-1]['image']=str(dest)
 shot[i-1].update(image=ref(dest),prompt=item['prompt'],generation_path=str(src),reference=item.get('ref'),
      revision='v02 correction following contact-sheet review')
manifest.write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
m.write_text(json.dumps(shot,indent=2,ensure_ascii=False)+'\n')
