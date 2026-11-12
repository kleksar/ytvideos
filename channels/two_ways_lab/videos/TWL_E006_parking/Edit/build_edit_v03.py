import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parents[1];a=p/'Source/Audio/v01';e=p/'Edit'; h=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
w=json.loads((a/'word_times.json').read_text())['words'];fr=lambda n:round(w[n]['start']*30);n=json.loads((a/'audio_build.json').read_text())['frames']
b=[0,fr(14),fr(29),fr(50),fr(63),fr(71),fr(78),fr(92),830,876,922,fr(115),fr(130),fr(145),fr(169),fr(178),n]
names=['entry_fixed','interior','entry_fixed','far_park','far_close','far_finish','entry_fixed','search','white_backing','white_leaving','near_open','near_park','near_close','near_close','entry_fixed','entry_fixed']
assert min(y-x for x,y in zip(b,b[1:]))>=45
sc=[]
for name,x,y in zip(names,b,b[1:]):
 sc.append({'image':f'../Source/Images/v02/{name}.png','start_frame':x,'end_frame':y,'direction':'none','zoom':'none','camera':{'focus':[.5,.5],'subject':name,'reason':'Fixed lot geometry and sequential story state','start':{'center':[.5,.5],'scale':1.0},'end':{'center':[.5,.5],'scale':1.0}}})
phrases=['I pull into the store','parking lot and spot','an empty space right away.',"It's far from the entrance.",'Should I park here','or look for a closer one?',
 'I decide to compare both.','I start the clock','at the parking lot entrance','and stop it at the store doors.',
 'First, I take that open space.','Parking and getting out take','thirty seconds.','The walk takes another minute','and a half.',
 'I reach the entrance','in two minutes.','Now I go back to the start','and try to find a closer spot.',
 'I drive past one row.','Full.','Another row.','Full too.','Finally, after two minutes,','I see an empty spot','right by the door!',
 'I park, get out and reach','the entrance','after a thirty-second walk.',"That's definitely closer.",
 'But when I check the clock,','three minutes have passed','since I entered the lot.',
 'In this test,','parking right away','saved me a minute.',"But if I'd found",'that closer spot sooner,','the result could have been different.',
 "Next time, I'll consider",'the search time as well','as the walk.','And once again...']
assert ' '.join(phrases).split()==(a/'narration.txt').read_text().split()
t={'channel':'two_ways_lab','format':'short','fps':30,'canvas':[1080,1920],'source_transfer':'srgb','audio':'../Source/Audio/v01/mix.wav',
 'audio_contract':{'final_audio_sha256':h(a/'mix.wav'),'applied_speed':1.0,'speed_evidence':'../Source/Audio/v01/mix-evidence.md'},'scenes':sc,
 'overlays':[{'path':'../Source/Lettering/v01/2.png','start_frame':fr(75),'end_frame':fr(78),'y':15,'lettering_motion':{'scale_amplitude':.02,'rotation_degrees':2}},
             {'path':'../Source/Lettering/v01/3.png','start_frame':fr(136),'end_frame':fr(144),'y':15,'lettering_motion':{'scale_amplitude':.02,'rotation_degrees':2}}],
 'subtitles':{'mode':'words','transcript':'../Source/Audio/v01/narration.txt','words':'../Source/Audio/v01/word_times.json','phrases':phrases},'minimum_scene_frames':45}
f=e/'timeline_v03.json';f.write_text(json.dumps(t,indent=2)+'\n')
c=json.loads((p.parent/'TWL_E001_checkout/Edit/export_contract_v23.json').read_text());c['episode_id']='TWL_E006';c['edit']={'timeline_id':str(f),'revision':'v03','source':{'path':str(f),'sha256':h(f)}}
c['timeline']['frame_count']=n;c['timeline']['duration_seconds']=n/30
c['required_delivery']['audio_contract']['owner_handoff']={'path':str(a/'mix-evidence.md'),'sha256':h(a/'mix-evidence.md')};c['required_delivery']['audio_contract']['accepted_complete_mix']={'path':str(a/'mix.wav'),'sha256':h(a/'mix.wav')};c['preflight']['output_path']=str(p/'Deliverables/TWL_E006_review_v03.mp4')
(e/'export_contract_v03.json').write_text(json.dumps(c,indent=2)+'\n')
cues=[];j=0
for phrase in phrases:
 count=len(phrase.split());group=w[j:j+count];cues.append({'start_seconds':group[0]['start'],'end_seconds':group[-1]['end'],'text':phrase});j+=count
assert j==len(w);(e/'srt_cues_v03.json').write_text(json.dumps({'cues':cues},indent=2)+'\n');print('frames',n,'bounds',b)
