import hashlib,json
from pathlib import Path
ep=Path(__file__).resolve().parents[1]
root=next(p for p in ep.parents if (p/'automation/ffmpeg_montage').is_dir())
def p(relative): return str(ep/relative)
def load(relative): return json.loads((ep/relative).read_text())
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
audio=p('Assets/Audio/full-mix-v02.wav')
choices=[
 ('none','in',.5,.5,1.014,1.046,.49,.42,'two stacked Ansons','Move toward the aircraft contact without losing the two silhouettes'),
 ('left_to_right','out',.509,.491,1.056,1.024,.50,.50,'rural town and year card','Reveal the surrounding farmland and hold the date readable'),
 ('right_to_left','none',.489,.511,1.034,1.034,.47,.44,'three parachute canopies','Read across the three separated canopies with ample headroom'),
 ('none','in',.5,.5,1.007,1.020,.61,.34,'Fuller and name tab','Small approach to the eyes while protecting name and column'),
 ('left_to_right','out',.507,.493,1.042,1.022,.45,.47,'control column and lower airflow','Reveal both paired functions and keep the label margins'),
 ('none','in',.5,.5,1.012,1.058,.50,.40,'field visible through windshield','Bring the selected field toward the viewer'),
 ('right_to_left','none',.494,.506,1.021,1.021,.48,.49,'locked pair close above grass','Follow the joint descent with the horizon steady'),
 ('none','out',.5,.5,1.043,1.012,.50,.51,'locked airframes and survival label','Open the view on the resolved situation without touching the headline'),
]
scenes=[]
for row,choice in zip(load('Work/shot-map-v01.json')['scenes'],choices):
 ident=row.pop('id')
 d,z,x0,x1,s0,s1,fx,fy,subject,reason=choice
 scenes.append(dict(row,image=p(f'Source/Images/{ident}-v0{3 if ident=="S003" else 2 if ident=="S008" else 1}.png'),direction=d,zoom=z,camera=dict(focus=[fx,fy],subject=subject,reason=reason,start=dict(center=[x0,.5],scale=s0),end=dict(center=[x1,.5],scale=s1))))
sub=dict(mode='words',words=p('Work/word-times-final-v01.json'),transcript=p('Source/narration-en-v02.txt'),keep_together=['Leonard Fuller','ended up','up stuck','lower plane','still locked'])
review=ep/'Edit/subtitle-review-v01.json'
if review.exists(): sub['review']=str(review)
overlay=str(root/'channels/paper_detour/Shared/Overlays/Paper_Frame/masters/paper-border-9x16-16s-v03.mov')
plan=dict(channel='paper',format='short',fps=30,canvas=[1440,2560],source_transfer='srgb',audio=audio,audio_contract=dict(final_audio_sha256=sha(audio),applied_speed=1.1,speed_evidence=p('Assets/Audio/HANDOFF.md')),scenes=scenes,subtitles=sub,overlays=[dict(role='paper_frame',path=overlay,start_frame=0,end_frame=1080,x=0,y=0)])
(ep/'Edit/montage-v01.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
