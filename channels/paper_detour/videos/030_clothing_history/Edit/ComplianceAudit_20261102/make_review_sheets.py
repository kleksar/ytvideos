"""Offline contact sheets from exact native decoded frames; no production media edits."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
report=json.loads((HERE/'video-v13-fixed-helper/report.json').read_text());plan=report['plan'];frames={x['index']:HERE/'video-v13-fixed-helper'/x['path'] for x in report['frame_map']};out=HERE/'VisualReview';out.mkdir(exist_ok=False);sheets=[]
def make(name,rows,w=384,h=216):
 cols=max(len(r) for r in rows);im=Image.new('RGB',(cols*w,len(rows)*(h+24)),'#e2ddcd');d=ImageDraw.Draw(im);indices=[]
 for y,row in enumerate(rows):
  for x,(frame,label) in enumerate(row):
   with Image.open(frames[frame]) as src:im.paste(src.resize((w,h)),(x*w,y*(h+24)))
   d.text((x*w+4,y*(h+24)+h+3),label+' f'+str(frame),fill='black');indices.append(frame)
 im.save(out/(name+'.jpg'));sheets.append({'sheet':name+'.jpg','frame_indices':indices,'cell_width':w,'cell_height':h})
for start in range(0,39,13):
 make('SCENES_'+str(start//13+1),[[(f,s['id']) for f in [s['start'],(s['start']+s['end']-1)//2,s['end']-1]] for s in plan['scenes'][start:start+13]])
for start in range(0,33,9):
 rows=[]
 for c in plan['cues'][start:start+9]:
  samples=[c['start']-1,c['entry_end'],c.get('exit_start',(c['start']+c['end']-1)//2),c['end']-1,min(c['end'],5699)]
  rows.append([(f,c['id']) for f in samples])
 make('CUES_'+str(start//9+1),rows,w=320,h=180)
for n in [16,17,27,29,31]:
 s=plan['scenes'][n-1];indices=sorted({s['start'],s['end']-1}|{f for f in plan['extra_frames'] if s['start']<=f<s['end']});make(f'RISK_V{n:02}',[[(f,s['id']) for f in indices[i:i+4]] for i in range(0,len(indices),4)])
(out/'manifest.json').write_text(json.dumps({'sheets':sheets,'unique_frames':len(set(f for s in sheets for f in s['frame_indices'])),'not_inspected':True},indent=2)+'\n');print('sheets',len(sheets),'unique frames',len(set(f for s in sheets for f in s['frame_indices'])))
