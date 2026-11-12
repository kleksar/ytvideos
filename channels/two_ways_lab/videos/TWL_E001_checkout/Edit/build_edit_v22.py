import json,hashlib,math
from pathlib import Path
p=Path(__file__).resolve().parents[1]; e=p/'Edit'; a=p/'Source/Audio/v06'; h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
w=json.loads((a/'word_times.json').read_text())['words']; assert len(w)==90
t=json.loads((e/'timeline_v21.json').read_text()); t['audio']='../Source/Audio/v06/mix.wav';t['audio_contract']={'final_audio_sha256':h(a/'mix.wav'),'applied_speed':1.0,'speed_evidence':'../Source/Audio/v06/mix-evidence.md'}
# Cuts anticipate each depicted event slightly, keeping the brief first departure >= 45 frames.
bounds=[0,round(w[12]['start']*30),round((w[21]['start']-.32)*30),round(w[24]['start']*30),round(w[36]['start']*30),round(w[63]['start']*30),round(w[83]['start']*30),json.loads((a/'audio_build.json').read_text())['frames']]
assert min(b-a for a,b in zip(bounds,bounds[1:]))>=45
for s,x,y in zip(t['scenes'],bounds,bounds[1:]):s['start_frame']=x;s['end_frame']=y
for o,(x,y) in zip(t['overlays'],[(0,bounds[1]-2),(round(w[49]['start']*30),round(w[62]['end']*30)),(round(w[79]['start']*30),bounds[6]-1)]):o['start_frame']=x;o['end_frame']=y
t['subtitles']['transcript']='../Source/Audio/v06/narration.txt';t['subtitles']['words']='../Source/Audio/v06/word_times.json'
f=e/'timeline_v22.json';f.write_text(json.dumps(t,indent=2,ensure_ascii=False)+'\n')
contract=json.loads((e/'export_contract_v21.json').read_text());contract['edit']={'timeline_id':str(f),'revision':'v22','source':{'path':str(f),'sha256':h(f)}};contract['timeline']['frame_count']=bounds[-1];contract['timeline']['duration_seconds']=bounds[-1]/30;ac=contract['required_delivery']['audio_contract'];ac['owner_handoff']={'path':str(a/'mix-evidence.md'),'sha256':h(a/'mix-evidence.md')};ac['accepted_complete_mix']={'path':str(a/'mix.wav'),'sha256':h(a/'mix.wav')};contract['preflight']['output_path']=str(p/'Deliverables/TWL_E001_review_v22.mp4');(e/'export_contract_v22.json').write_text(json.dumps(contract,indent=2)+'\n')
# The existing approved subtitle phrase groups, timed on the conformed provider word map.
cues=[];j=0
for phrase in t['subtitles']['phrases']:
 parts=phrase.split();group=w[j:j+len(parts)];assert [z['text'] for z in group]==parts,(phrase,group);cues.append({'start_seconds':group[0]['start'],'end_seconds':group[-1]['end'],'text':phrase});j+=len(parts)
assert j==len(w);(e/'srt_cues_v22.json').write_text(json.dumps({'cues':cues},indent=2,ensure_ascii=False)+'\n')
print('frame boundaries',bounds,'duration',bounds[-1]/30)
