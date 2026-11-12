from pathlib import Path
import json,subprocess,hashlib
from PIL import Image,ImageDraw,ImageFont
E=Path('/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900');D=E/'Packaging/Metadata';Q=E/'Edit/QA/full-v04';V=E/'Deliverables/032_galveston_en_final_v02.mp4';T=json.loads((E/'Edit/ChurchDemo_v01/final_asr_unwrapped_v04.json').read_text())['transcription'];R=json.loads((Q/'report.json').read_text());F={x['index']:(Q/x['path']).resolve() for x in R['frame_map']};out=D/'chapter_boundary_v04';out.mkdir(exist_ok=True)
chapters=(D/'chapters_draft_v02.txt').read_text().replace('00:25 A Prosperous','00:26 A Prosperous');(D/'chapters_final_v02.txt').write_text(chapters)
records=[];font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
for line in chapters.strip().splitlines():
 stamp,title=line.split(' ',1);mm,ss=map(int,stamp.split(':'));sec=mm*60+ss;fs=sorted(set(max(0,sec*30+i) for i in [-1,0,1]));paths=[]
 for f in fs:
  p=F.get(f)
  if p is None:
   p=out/f'f{f:05}.png';subprocess.run(['ffmpeg','-v','error','-i',str(V),'-vf',f'select=eq(n\\,{f})','-frames:v','1','-fps_mode','passthrough','-y',str(p)],check=True)
  paths.append(str(p))
 records.append({'timestamp':stamp,'seconds':sec,'title':title,'frames':fs,'paths':paths,'asr_before_after':[x for x in T['segments'] if x[2]>max(0,sec-6) and x[1]<sec+7],'precision':'whole second topic boundary; ASR leading silence is not a phoneme onset','review':'PENDING'})
for i in range(0,len(records),5):
 group=records[i:i+5];im=Image.new('RGB',(1536,len(group)*313),(22,22,22));draw=ImageDraw.Draw(im)
 for j,r in enumerate(group):
  for k,(f,p) in enumerate(zip(r['frames'],r['paths'])):
   im.paste(Image.open(p).convert('RGB').resize((512,288),Image.Resampling.LANCZOS),(k*512,j*313+25));draw.text((k*512+3,j*313+2),f'{r["timestamp"]} f{f} {r["title"][:30]}',font=font,fill='white')
 im.save(out/f'boundaries_{i+1:02}_{i+len(group):02}.jpg',quality=93,subsampling=0)
evidence={'media':str(V),'media_sha256':R['sha256'],'timeline_id':'02A15052','duration_seconds':574.433333,'asr_source':'Edit/ChurchDemo_v01/final_asr_unwrapped_v04.json actual final MP4 mediaRef4D3F8EDA','asr_coverage':{'segments':len(T['segments']),'words':len(T['words']),'first':T['segments'][0],'last':T['segments'][-1]},'records':records,'status':'PENDING_FRAME_REVIEW','subjective_listening':'UNVERIFIED','player_chapters':'UNVERIFIED'};(D/'chapters_evidence_v02.json').write_text(json.dumps(evidence,indent=2,ensure_ascii=False));print('Created two boundary boards and complete final-MP4 ASR evidence')
