from pathlib import Path
import json,math
from PIL import Image,ImageFont,ImageDraw
P=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history');E=P/'Edit/v14';Q=E/'QA';V=Q/'VisualReview';V.mkdir(exist_ok=True)
r=json.loads((Q/'technical/report.json').read_text());frames={x['index']:(Q/'technical'/x['path']).resolve() for x in r['frame_map']};shots=json.loads((P/'Storyboard/SHOTLIST_v14.json').read_text());cues=json.loads((P/'Storyboard/CUE_SHEET_v14.json').read_text());srt=json.loads((E/'SRT_CUES_v14.json').read_text())['cues'];srtplan=json.loads((E/'SRT_FRAME_PLAN.json').read_text());font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',64);label=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',15);manifest=[];metrics=[]
def base(f):return Image.open(frames[f]).convert('RGB')
def subtitle(f):
 im=base(f);active=[(i+1,x) for i,x in enumerate(srt) if float(x['start_seconds'])-1e-8<=f/30<float(x['end_seconds'])-1e-8]
 assert len(active)<=1
 if active:
  no,x=active[0];text=x['text'];draw=ImageDraw.Draw(im);bbox=draw.multiline_textbbox((0,0),text,font=font,spacing=10,align='center',stroke_width=3);w=bbox[2]-bbox[0];h=bbox[3]-bbox[1];tx=(im.width-w)/2-bbox[0];ty=im.height*.95-h-bbox[1];draw.multiline_text((tx,ty),text,font=font,spacing=10,align='center',fill='white',stroke_width=3,stroke_fill='black')
  box=draw.multiline_textbbox((tx,ty),text,font=font,spacing=10,align='center',stroke_width=3);assert box[0]>.05*im.width and box[2]<.95*im.width and box[1]>0 and box[3]<im.height
  metrics.append({'frame':f,'cue':no,'bbox':box,'font_px':64,'canvas':[2560,1440]})
 return im

def sheet(name,rows,w=384,h=216,sub=False):
 cols=max(len(x) for x in rows);out=Image.new('RGB',(cols*w,len(rows)*(h+24)),'#ded8c7');d=ImageDraw.Draw(out)
 ids=[]
 for iy,row in enumerate(rows):
  for ix,(f,tag) in enumerate(row):
   im=subtitle(f) if sub else base(f);im=im.resize((w,h),Image.Resampling.LANCZOS);out.paste(im,(ix*w,iy*(h+24)));d.text((ix*w+3,iy*(h+24)+h+2),tag,font=label,fill='black');ids.append(f)
 out.save(V/(name+'.jpg'),quality=92);manifest.append({'file':name+'.jpg','indices':ids,'cell_size':[w,h],'srt_simulation':sub})
for page in range(3):sheet(f'SCENES_{page+1}',[[(s['startFrame'],s['id']+' start'),((s['startFrame']+s['endFrame']-1)//2,s['id']+' mid'),(s['endFrame']-1,s['id']+' end')] for s in shots[page*13:(page+1)*13]])
for page in range(4):
 rows=[]
 for q in cues[page*9:(page+1)*9]:
  k=q['opacity_keys'];fs=[max(0,q['startFrame']-1),q['startFrame']+k[1][0],q['startFrame']+k[-2][0],q['endFrame']-1,min(5699,q['endFrame'])]
  rows.append([(f,q['id']+f' f{f}') for f in fs])
 sheet(f'ACCENTS_{page+1}',rows,320,180)
for name in ['V16','V17','V27','V29','V31']:
 s=next(x for x in shots if x['id']==name);fs=sorted(set(range(s['startFrame'],s['endFrame'],10))|{s['endFrame']-1});sheet('RISK_'+name,[[(f,f'{name} f{f}') for f in fs[i:i+4]] for i in range(0,len(fs),4)])
for page in range(math.ceil(len(srtplan)/12)):
 sheet(f'SRT_{page+1}',[[(f,f"SRT{x['cue']:02} {phase} f{f}") for f,phase in zip(x['phases'],['start','hold','end'])] for x in srtplan[page*12:(page+1)*12]],320,180,True)
cutrows=[[(f,f"SRT{x['cue']:02} cut f{f}") for f in x['scene_cut_frames']] for x in srtplan if x['scene_cut_frames']]
# each cut pair side-by-side, normalized two per row
cutpairs=[row[i:i+2] for row in cutrows for i in range(0,len(row),2)]
for page in range(math.ceil(len(cutpairs)/12)):sheet(f'SRT_CUTS_{page+1}',cutpairs[page*12:(page+1)*12],384,216,True)
repairs=json.loads((E/'CUE_REPAIRS.json').read_text());rows=[]
for x in repairs:
 fs=list(range(x['fade_start']-1,x['after_frames'][1]+1));rows.extend([[(f,f"{x['cue']} f{f}") for f in fs[i:i+4]] for i in range(0,len(fs),4)])
for page in range(math.ceil(len(rows)/8)):sheet(f'REPAIRS_{page+1}',rows[page*8:(page+1)*8])
(V/'manifest.json').write_text(json.dumps({'sheets':manifest,'subtitle_style':'Offline generic viewer simulation: Arial64px on2560×1440, white/black3pxoutline, bottom95%; separate SRT remains unstyled and is not burned into MP4. Player/platform layout is not claimed.','srt_metrics':metrics,'inspected':False},indent=2));print('sheets',len(manifest),'frames',len(set(f for x in manifest for f in x['indices'])),'extracted',len(frames))
# Consequential long/tight frames for native inspection, no change to source.
for f in [2430,2433,3150,4101]:base(f).save(V/f'NATIVE_f{f}.png')
for no in [22,51,84,87]:
 x=srtplan[no-1];subtitle(x['phases'][1]).save(V/f'NATIVE_SRT{no}.png')
