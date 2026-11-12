#!/usr/bin/env python3
import json,pathlib,sys
root=pathlib.Path('/Users/diplomat/ytvideos');sys.path.insert(0,str(root/'automation/palmier'))
from inspect_connection import PalmierConnection
c=PalmierConnection();c.connect()
def call(name,args):
 r=c.request('tools/call',{'name':name,'arguments':args})
 if r.get('isError'): raise RuntimeError(str(r))
 txt=[x['text'] for x in r.get('content',[]) if x.get('type')=='text']
 try:o=json.loads(txt[0]) if len(txt)==1 else r
 except ValueError:o=r
 print(json.dumps({'tool':name,'response':o},ensure_ascii=False),flush=True);return o
name='Paper Detour 001 Short 02 Director Trial 20261031'
call('manage_project',{'action':'open','name':name})
t=call('get_timeline',{})
if t.get('id')!='7537BAE9' or t.get('totalFrames')!=1098: raise RuntimeError('Unexpected timeline')
visual=sorted([x for tr in t['tracks'] for x in tr.get('clips',[]) if x.get('mediaType')=='image'],key=lambda x:x['frames'][0])
if [v['id'] for v in visual] != ['5BC8BE91','B8C8F5FB','0697CAE7','7FAAE43D','8493198A','391AE960']: raise RuntimeError('Unexpected visual clips')
for i,clip in enumerate(visual):
 if i in (0,1,3,5):
  d=clip['frames'][1]-clip['frames'][0];end=1.025 if i==3 else 1.035
  call('set_keyframes',{'clipId':clip['id'],'property':'scale','keyframes':[[0,1,1,'smooth'],[d-1,end,end,'smooth']]})
  call('set_keyframes',{'clipId':clip['id'],'property':'position','keyframes':[[0,0,0,'smooth'],[d-1,-(end-1)/2,-(end-1)/2,'smooth']]})
call('get_timeline',{})
call('export_project',{'mode':'video','codec':'H.264','resolution':'Match Timeline','outputPath':'/tmp/paper_detour_short02_palmier_20261031.mp4','overwrite':False,'timelineId':'7537BAE9'})
