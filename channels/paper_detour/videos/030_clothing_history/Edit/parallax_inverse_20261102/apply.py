import importlib.util,json,time
from pathlib import Path
R=Path(__file__).resolve().parent;P='B1BA2D18';SRC='57A71C61';s=importlib.util.spec_from_file_location('p','/Users/diplomat/ytvideos/automation/palmier/inspect_connection.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);c=m.PalmierConnection();c.connect()
def call(name,args):
 res=c.request('tools/call',{'name':name,'arguments':args})
 with (R/'receipts.jsonl').open('a') as f:f.write(json.dumps({'name':name,'arguments':args,'response':res},ensure_ascii=False)+'\n')
 if res.get('isError'):raise RuntimeError(str(res))
 return json.loads(res['content'][0]['text'])
def timeline(t):return c.read_tool('get_timeline',{'projectId':P,'timelineId':t})
source=timeline(SRC);sc=next(t for t in source['tracks'] if t['name']=='Scenes')['clips'];assert len(sc)==15
new=call('create_timeline',{'projectId':P,'from':SRC,'name':'Clothing History — 15 scenes opposite parallax'});T=new['timelineId'];(R/'timeline_id.txt').write_text(T+'\n');state=timeline(T);(R/'before.json').write_text(json.dumps(state,ensure_ascii=False,indent=2));snap=call('manage_snapshots',{'projectId':P,'timelineId':T,'action':'save','name':'Before opposite-direction parallax'});print('TARGET',T,json.dumps(snap),flush=True)
clips=next(t for t in state['tracks'] if t['name']=='Scenes')['clips'];start=time.monotonic()
for i,(old,clip) in enumerate(zip(sc,clips),1):
 assert old['frames']==clip['frames'] and old['mediaRef']==clip['mediaRef'] and old['keyframes']==clip['keyframes']
 path=R/f'inverse_{i:02}.mp4'
 while not path.is_file():time.sleep(.5)
 imported=call('import_media',{'projectId':P,'source':{'path':str(path)},'folder':'Parallax opposite direction'})
 swapped=call('swap_clip_media',{'projectId':P,'timelineId':T,'clipId':clip['id'],'mediaRef':imported['mediaRef']});assert swapped.get('changed') is True
 print(json.dumps({'applied':i,'total':15,'elapsed':round(time.monotonic()-start,1)}),flush=True)
final=timeline(T);clips=next(t for t in final['tracks'] if t['name']=='Scenes')['clips'];assert len(clips)==15
for old,newclip in zip(sc,clips):
 assert old['frames']==newclip['frames'] and old['keyframes']==newclip['keyframes'] and old['mediaRef']!=newclip['mediaRef']
for name in ('Accents','Grain','Mix'):
 a=next(x for x in state['tracks'] if x['name']==name);b=next(x for x in final['tracks'] if x['name']==name)
 assert len(a['clips'])==len(b['clips']) and all({k:v for k,v in x.items() if k!='id'}=={k:v for k,v in y.items() if k!='id'} for x,y in zip(a['clips'],b['clips']))
(R/'final.json').write_text(json.dumps(final,ensure_ascii=False,indent=2));snap=call('manage_snapshots',{'projectId':P,'timelineId':T,'action':'save','name':'15 scenes opposite parallax directions'});print('DONE',T,json.dumps(snap),flush=True)
