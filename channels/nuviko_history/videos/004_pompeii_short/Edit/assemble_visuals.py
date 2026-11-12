import sys,json
from pathlib import Path
sys.path.insert(0,'automation/palmier')
from inspect_connection import PalmierConnection
c=PalmierConnection();c.connect()
def call(n,a):
 r=c.request('tools/call',{'name':n,'arguments':a})
 if r.get('isError'): raise RuntimeError(str(r))
 return json.loads(next(x['text'] for x in r['content'] if x['type']=='text'))
t=call('get_timeline',{}); assert t['id']=='513CD38A' and all(x['type']=='audio' for x in t['tracks'])
root=Path('/Users/diplomat/ytvideos/channels/nuviko_history/videos/004_pompeii_short'); folder=root/'Source/Images'
sequence=[('bg07.png',0,156),('bg08.png',156,255),('bg02.png',255,450),('bg03.png',450,570),('02.png',570,660),('bg09.png',660,840),('bg04.png',840,906),('bg07.png',906,1200),('06.png',1200,1260),('01.png',1260,1421)]
refs={}
for filename,_,_ in sequence:
 if filename not in refs:
  result=call('import_media',{'source':{'path':str(folder/filename)},'folder':'004_pompeii_short/Images'});refs[filename]=result['mediaRef'];print('imported',filename,refs[filename],flush=True)
call('get_media',{'ids':list(refs.values())})
entries=[{'mediaRef':refs[n],'startFrame':a,'endFrame':b} for n,a,b in sequence]
result=call('add_clips',{'entries':entries});print('added',json.dumps(result),flush=True)
clips=result['clips']
for i,clip in enumerate(clips):
 start,end=clip['frames']; first,last=(1.02,1.07) if i%2==0 else (1.07,1.02)
 call('set_keyframes',{'clipId':clip['id'],'property':'scale','keyframes':[[0,first,first],[end-start-1,last,last]]})
print('animated',len(clips),flush=True)
t=call('get_timeline',{}); print('tracks',json.dumps(t['tracks'],ensure_ascii=False),flush=True)
(root/'Edit/palmier_image_refs.json').write_text(json.dumps(refs,indent=2))
