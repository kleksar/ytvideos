"""Assemble an exact-user-script review with generated-only scene text."""
from pathlib import Path
import json,hashlib,math,re
p=Path(__file__).resolve().parents[1];audio=p/'Source/Audio/v05';h=lambda q:hashlib.sha256(q.read_bytes()).hexdigest();text=(audio/'narration.txt').read_text().strip();tokens=text.split();raw=json.loads((p/'Edit/QA/forced_alignment_v11_raw.json').read_text())['word_segments'];assert len(tokens)==len(raw)==90
norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
words=[]
for label,x in zip(tokens,raw):
 assert norm(label)==norm(x['word']) and 'start' in x and 'end' in x
 words.append({'text':label,'start':float(x['start']),'end':float(x['end'])})
words_map={'status':'AUTO_ALIGNED_REVIEW_REQUIRED','method':'offline WhisperX alignment of voice.wav; exact user transcript, mapped to mix with identical timing','voice_sha256':h(audio/'voice.wav'),'audio_sha256':h(audio/'mix.wav'),'transcript_sha256':hashlib.sha256(text.encode()).hexdigest(),'words':words};(audio/'word_times.json').write_text(json.dumps(words_map,indent=2)+'\n')
ends=[4,7,12,16,19,21,24,26,31,36,40,45,48,53,58,63,65,69,75,79,83,85,90];starts=[0]+ends[:-1];phrases=[' '.join(x['text'] for x in words[a:b]) for a,b in zip(starts,ends)];assert sum(len(x.split()) for x in phrases)==90
srt=[]
def fmt(s):
 n=round(s*1000);a,n=divmod(n,3600000);b,n=divmod(n,60000);c,d=divmod(n,1000);return f'{a:02}:{b:02}:{c:02},{d:03}'
for i,(a,b,phrase) in enumerate(zip(starts,ends,phrases),1):
 start=0 if i==1 else words[a]['start'];end=words[b-1]['end'];srt.append(f'{i}\n{fmt(start)} --> {fmt(end)}\n{phrase}\n')
(p/'Deliverables/TWL_E001_review_v11.en.srt').write_text('\n'.join(srt))
frames=802
shots=[(0,'v04_hook.png','initial comparison A2 B5'),(110,'v11_select.png','protagonist joins five baskets'),(230,'v11_one.png','one basket shopper has left A2 B4'),(250,'v11_two.png','two basket shoppers have left A2 B3'),(369,'v11_payment.png','payment by a remaining basket shopper A2 B3'),(578,'v11_result.png','two carts clear and protagonist behind last basket A0 B1'),(752,'v04_hook.png','return to the same initial choice')]
scenes=[]
for (start,img,subject),(end,_,_) in zip(shots,shots[1:]+[(frames,None,None)]):
 scenes.append({'image':'../Source/Images/'+img,'start_frame':start,'end_frame':end,'direction':'none','zoom':'none','camera':{'focus':[.5,.5],'subject':subject,'reason':'preserve both queues, character and generated text safe area','start':{'center':[.5,.5],'scale':1.0},'end':{'center':[.5,.5],'scale':1.0}}})
def label(path,a,b):return {'path':path,'start_frame':a,'end_frame':b,'y':15,'lettering_motion':{'scale_amplitude':.02,'rotation_degrees':2}}
overlays=[label('../Source/Lettering/v04/hook_large.png',0,108),label('../Source/Lettering/v11/payment.png',458,561),label('../Source/Lettering/v11/loss.png',704,751)]
t={'channel':'two_ways_lab','format':'short','fps':30,'canvas':[1080,1920],'source_transfer':'srgb','audio':'../Source/Audio/v05/mix.wav','audio_contract':{'final_audio_sha256':h(audio/'mix.wav'),'applied_speed':1.0,'speed_evidence':'../Source/Audio/v05/mix-evidence.md'},'scenes':scenes,'overlays':overlays,'subtitles':{'mode':'words','transcript':'../Source/Audio/v05/narration.txt','words':'../Source/Audio/v05/word_times.json','phrases':phrases}}
m=p/'Edit/timeline_v11.json';m.write_text(json.dumps(t,indent=2)+'\n');c=json.loads((p/'Edit/export_contract_v10.json').read_text());c['edit'].update(timeline_id=str(m),revision='v11',source={'path':str(m),'sha256':h(m)});c['timeline'].update(frame_count=frames,duration_seconds=frames/30);c['required_delivery']['audio_contract']['owner_handoff']={'path':str(audio/'mix-evidence.md'),'sha256':h(audio/'mix-evidence.md')};c['required_delivery']['audio_contract']['accepted_complete_mix']={'path':str(audio/'mix.wav'),'sha256':h(audio/'mix.wav')};c['preflight']['output_path']=str(p/'Deliverables/TWL_E001_review_v11.mp4');(p/'Edit/export_contract_v11.json').write_text(json.dumps(c,indent=2)+'\n');print('frames',frames,'words',len(words),'groups',len(phrases))
