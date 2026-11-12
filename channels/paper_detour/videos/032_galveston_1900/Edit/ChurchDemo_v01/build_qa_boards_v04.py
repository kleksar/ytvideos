from pathlib import Path
import json,math,importlib.util,hashlib
from PIL import Image,ImageDraw,ImageFont
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');Q=E/'Edit/QA/full-v04';R=json.loads((Q/'report.json').read_text());S=json.loads((E/'Storyboard/storyboard_v02.json').read_text())['scenes'];C=json.loads((E/'Edit/ChurchDemo_v01/full_cues_v02.json').read_text());spec=importlib.util.spec_from_file_location('srt_owner','/Users/diplomat/ytvideos/.agents/skills/ytv-srt/scripts/srt_tool.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);U=m.parse_srt((E/'Edit/Subtitles_v02/032_galveston_en_v07.srt').read_text())
F={x['index']:(Q/x['path']).resolve() for x in R['frame_map']};B=Q/'boards';B.mkdir(exist_ok=False);font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18);subfont=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',36);man=[];seen=set()
def get(f,sub=False):
 im=Image.open(F[f]).convert('RGB')
 if sub:
  im=im.resize((960,540),Image.Resampling.LANCZOS);active=[c for c in U if float(c['start_seconds'])<=f/30<float(c['end_seconds'])];d=ImageDraw.Draw(im)
  if active:
   lines=active[0]['text'].split('\n');y=510-len(lines)*42
   for line in lines:
    box=d.textbbox((0,0),line,font=subfont,stroke_width=2);w=box[2]-box[0];x=(960-w)//2;d.rectangle((x-6,y-2,x+w+6,y+41),fill=(15,15,15));d.text((x,y),line,font=subfont,fill='white',stroke_width=1,stroke_fill='black');y+=42
 return im

def board(name,items,cols=5,w=512,sub=False):
 h=round(w*9/16);pad=25;rows=math.ceil(len(items)/cols);im=Image.new('RGB',(cols*w,rows*(h+pad)),(25,25,25));d=ImageDraw.Draw(im)
 for j,(f,label) in enumerate(items):
  tile=get(f,sub).resize((w,h),Image.Resampling.LANCZOS);x=(j%cols)*w;y=(j//cols)*(h+pad);im.paste(tile,(x,y+pad));d.text((x+4,y+2),f'{label} f{f} {f/30:.3f}s',font=font,fill='white');seen.add(f)
 path=B/(name+'.jpg');im.save(path,quality=91,subsampling=0);man.append({'file':str(path),'frames':[x[0] for x in items],'subtitle_simulation':sub,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'inspected':False})
for i in range(0,len(S),4):
 items=[]
 for s in S[i:i+4]:
  a,b=s['in_frame'],s['out_frame_exclusive'];items.extend((f,s['scene_id']+'/'+ph) for f,ph in [(a,'start'),(a+(b-a)//4,'q1'),((a+b-1)//2,'mid'),(a+3*(b-a)//4,'q3'),(b-1,'last')])
 board(f'scenes_{i+1:03}_{min(i+4,len(S)):03}',items)
for i,c in enumerate(C):
 a,b=c['in_frame'],c['out_frame_exclusive'];fs=sorted(set([a-1,a,a+2,a+4,(a+b)//2,b-5,b-3,b-1,b]));items=[(f,c['id']) for f in fs if f in F];board(f'cue_{i+1:02}_{c["id"]}',items,cols=3,w=640)
subitems=[]
for i,c in enumerate(U,1):
 a=math.ceil(float(c['start_seconds'])*30);b=math.ceil(float(c['end_seconds'])*30);subitems.extend((f,f'SRT{i:03}/{phase}') for f,phase in [(a,'start'),((a+b)//2,'hold'),(b-1,'last')] if f in F)
for s in S[1:]:
 a=s['in_frame'];subitems.extend([(a-1,'SRTcut-before'),(a,'SRTcut-after')])
for i in range(0,len(subitems),30):board(f'srt_{i+1:04}_{min(i+30,len(subitems)):04}',subitems[i:i+30],cols=6,w=360,sub=True)
left=[(f,'extra') for f in sorted(set(F)-seen)]
for i in range(0,len(left),20):board(f'other_{i+1:03}_{min(i+20,len(left)):03}',left[i:i+20])
assert seen==set(F),(len(seen),len(F));(Q/'board_manifest.json').write_text(json.dumps({'media_sha256':R['sha256'],'all_extracted_frames':len(F),'all_boarded_frames':len(seen),'boards':man,'inspection_status':'PENDING_ACTUAL_AUTHOR_VIEW','srt_note':'Offline player-style overlay simulation on actual final-MP4 frames; not burned in, not live YouTube player proof'},indent=2));print('Boards',len(man),'frames',len(F))
