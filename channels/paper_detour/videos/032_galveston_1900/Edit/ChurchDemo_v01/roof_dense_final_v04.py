import subprocess,json,math,hashlib
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Edit/QA/full-v04';r=json.loads((E/'Edit/Export/full_v04/render_receipt_v04.json').read_text());W=E/'Work/church-demo-v01/previews/roof-dense-final-v04';W.mkdir(exist_ok=False);B=D/'roof-dense';B.mkdir(exist_ok=False);out=[]
for name,a,b in [('CH02',14307,14440),('CH05',14707,14841)]:
 O=W/name;O.mkdir();subprocess.run(['ffmpeg','-v','error','-i',r['file'],'-an','-vf',f'select=between(n\,{a}\,{b-1}),crop=900:240:1300:0,scale=450:120','-fps_mode','vfr',str(O/'%03d.png')],check=True)
 fs=sorted(O.glob('*.png'));assert len(fs)==b-a
 for k in range(0,len(fs),70):
  q=fs[k:k+70];im=Image.new('RGB',(7*450,math.ceil(len(q)/7)*140),(20,20,20));draw=ImageDraw.Draw(im)
  for j,p in enumerate(q):x=(j%7)*450;y=(j//7)*140;im.paste(Image.open(p),(x,y+20));draw.text((x+5,y+2),f'{name} f{a+k+j}',fill='white')
  dest=B/f'{name}_{k:03}.jpg';im.save(dest,quality=93,subsampling=0);out.append({'file':str(dest),'frames':list(range(a+k,a+k+len(q))),'roi_native':[1300,0,900,240],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'actually_viewed':False})
(B/'manifest.json').write_text(json.dumps({'media_sha256':r['sha256'],'total_frames':267,'boards':out,'scope':'Every visible frame of repaired church scenes: roof/upper-border ROI only. Full scenes/cues reviewed separately.'},indent=2));print('All267 roof ROI frames ready')
