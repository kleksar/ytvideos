import json,pathlib,sys,time
root=pathlib.Path('/Users/diplomat/ytvideos'); out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier'; source=root/'channels/paper_detour/videos/003_iq_gallery/Source'
sys.path.insert(0,str(root/'automation/palmier'))
from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text()); c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq']
log=out/'imports.jsonl'
def call(name,args):
 res=c.request('tools/call',{'name':name,'arguments':args});texts=[v['text'] for v in res.get('content',[]) if v.get('type')=='text']
 if res.get('isError'): raise RuntimeError((name,res))
 try: obj=json.loads(texts[0]) if len(texts)==1 else res
 except ValueError: obj=res
 with log.open('a') as f: f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 return obj
if '/root/paper_edit' not in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text(): raise RuntimeError('lock ownership lost')
t=call('get_timeline',{})
if t.get('id')!='19F2B39F': raise RuntimeError('not target timeline: '+str(t.get('id')))
paths={'background':source/'Images/paper_v1/background.png','foreground':source/'Images/paper_v1/foreground.png','grain':root/'channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Source/Graphics/director_trial_20261031/film_grain_vertical_8s_prores4444.mov','music':root/'channels/paper_detour/legacy/025_iq_gallery/Source/Audio/music_bed_56s_synth_stereo.wav'}
people=['haha','kasparov','feynman','logan_paul','nolan_gould','kate_beckinsale','tarantino','marilyn']
for name in people:
 paths['person_'+name]=source/('Images/paper_v1/'+('haha_clean.png' if name=='haha' else name+'.png'))
 paths['name_'+name]=source/('Graphics/names/'+name+'.png')
for n in ['0','1','2','3','5','6','7','9','plus']:
 paths['digit_'+n]=source/('Graphics/digit_'+n+('_reference.png' if n in ['0','1'] else '_generated.png'))
if not all(p.is_file() for p in paths.values()): raise RuntimeError('missing source files: '+str([str(p) for p in paths.values() if not p.is_file()]))
refs={}
for key,p in paths.items():
 obj=call('import_media',{'source':{'path':str(p)},'name':key})
 refs[key]=obj['mediaRef']
(out/'refs.json').write_text(json.dumps(refs,indent=2)+'\n')
(out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n')
print(json.dumps({'imported':len(refs),'keys':list(refs)}))
