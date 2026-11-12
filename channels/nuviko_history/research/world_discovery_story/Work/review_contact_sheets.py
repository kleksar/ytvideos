from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import re,json,hashlib
Image.MAX_IMAGE_PIXELS=300000000
base=Path(__file__).resolve().parents[1]
src=base/"Assets/Scenes"
out=base/"Work/contact_sheet_draft_v01"
out.mkdir(exist_ok=True)
selection={}
for n in range(1,90):
 matches=[]
 for f in src.glob(f"S{n:03}-v*"):
  m=re.fullmatch(r"S[0-9]{3}-v([0-9]+)[.](png|jpg|jpeg)",f.name,re.I)
  if m: matches.append((int(m.group(1)),f))
 if not matches: raise RuntimeError(f"missing S{n:03}")
 f=max(matches)[1]
 selection[f"S{n:03}"]={"path":str(f.relative_to(base)),"sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"status":"candidate only; latest version is not acceptance"}
for start in range(1,90,18):
 nums=range(start,min(start+18,90))
 canvas=Image.new("RGB",(1200,6*258),"#161b22")
 draw=ImageDraw.Draw(canvas)
 for offset,n in enumerate(nums):
  f=base/selection[f"S{n:03}"]["path"]
  with Image.open(f) as im:
   im.thumbnail((388,218))
   x=(offset%3)*400+(400-im.width)//2
   y=(offset//3)*258+22
   canvas.paste(im.convert("RGB"),(x,y))
  draw.text(((offset%3)*400+8,(offset//3)*258+2),f.name,fill="white")
 canvas.save(out/f"scenes_{start:03}_{min(start+17,89):03}.jpg",quality=88)
(out/"selection.json").write_text(json.dumps(selection,indent=2,ensure_ascii=False)+chr(10))
print("candidate scene count",len(selection),"contact sheets",len(list(out.glob("*.jpg"))))
