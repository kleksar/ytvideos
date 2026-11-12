import hashlib
import json
from pathlib import Path

p = Path(__file__).resolve().parents[1]
a = p / 'Source/Audio/v01'
e = p / 'Edit'
h = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
w = json.loads((a / 'word_times.json').read_text())['words']
fr = lambda n: round(w[n]['start'] * 30)
n = json.loads((a / 'audio_build.json').read_text())['frames']
bounds = [0, fr(7), fr(23), fr(39), fr(68), fr(100), fr(109), fr(122), fr(137), fr(148), fr(160), fr(174), n]
names = ['hook','introduce','point','first_cut_v2','bad_result','hook','smart_first','smart_first','success_v2','success_v2','point','hook']
assert min(y-x for x,y in zip(bounds,bounds[1:])) >= 45
scenes = []
for name,x,y in zip(names,bounds,bounds[1:]):
    scenes.append({'image':f'../Source/Images/v01/{name}.png','start_frame':x,'end_frame':y,
        'direction':'none','zoom':'none','camera':{'focus':[.5,.5],'subject':name,
        'reason':'Consistent complete gift-wrapping state',
        'start':{'center':[.5,.5],'scale':1.0},'end':{'center':[.5,.5],'scale':1.0}}})
phrases = [
 'Three gifts and two rolls','of ribbon.','Can you wrap them all?',
 'The big gift needs four meters.','Each small one needs three.',
 'One roll has six meters,','the other has four.',"That's ten meters altogether.","Surely that's enough!",
 'You take the big roll','and cut four meters','for the big gift.','Two meters left.',
 'Then you cut three meters','from the other roll','for a small gift.','One meter left.',
 'Two gifts are ready.','But the last one needs','a single three-meter piece.',
 'You only have two meters','and one meter left,',"and you can't tie",'the pieces together.',
 'Did you run out of ribbon?',"Let's try again.",
 'For the big gift,','use the short roll.','It has exactly four meters.',
 'Now split the long roll','in half:','two three-meter pieces,','one for each small gift.',
 'Done!','All three gifts are wrapped,',"and there's no ribbon left.",
 'Next time, before you cut,','check which pieces fit','on each roll.',
 'Having enough ribbon in total',"isn't always enough.",'It matters how you divide it.',
 'What would you do','if you had...'
]
assert ' '.join(phrases).split() == (a/'narration.txt').read_text().split()
t = {'channel':'two_ways_lab','format':'short','fps':30,'canvas':[1080,1920],
     'source_transfer':'srgb','audio':'../Source/Audio/v01/mix.wav',
     'audio_contract':{'final_audio_sha256':h(a/'mix.wav'),'applied_speed':1.0,'speed_evidence':'../Source/Audio/v01/mix-evidence.md'},
     'scenes':scenes,'overlays':[],
     'subtitles':{'mode':'words','transcript':'../Source/Audio/v01/narration.txt','words':'../Source/Audio/v01/word_times.json','phrases':phrases},
     'minimum_scene_frames':45}
f=e/'timeline_v01.json';f.write_text(json.dumps(t,indent=2)+'\n')
c=json.loads((p.parent/'TWL_E001_checkout/Edit/export_contract_v23.json').read_text())
c['episode_id']='TWL_E005';c['edit']={'timeline_id':str(f),'revision':'v01','source':{'path':str(f),'sha256':h(f)}}
c['timeline']['frame_count']=n;c['timeline']['duration_seconds']=n/30
c['required_delivery']['audio_contract']['owner_handoff']={'path':str(a/'mix-evidence.md'),'sha256':h(a/'mix-evidence.md')}
c['required_delivery']['audio_contract']['accepted_complete_mix']={'path':str(a/'mix.wav'),'sha256':h(a/'mix.wav')}
c['preflight']['output_path']=str(p/'Deliverables/TWL_E005_review_v01.mp4')
(e/'export_contract_v01.json').write_text(json.dumps(c,indent=2)+'\n')
cues=[];j=0
for phrase in phrases:
    count=len(phrase.split());group=w[j:j+count]
    cues.append({'start_seconds':group[0]['start'],'end_seconds':group[-1]['end'],'text':phrase});j+=count
assert j==len(w)
(e/'srt_cues_v01.json').write_text(json.dumps({'cues':cues},indent=2)+'\n')
print('boundaries:',bounds,'frames:',n)
