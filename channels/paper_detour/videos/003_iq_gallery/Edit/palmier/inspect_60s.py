import json,pathlib,sys,base64
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session_60s_active.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq'];assert '/root/film_editor' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text()
starts=[139,278,417,556,695,834,972,1110,1248,1386,1524,1662]
frames=sorted({f for s in starts for f in [s-10,s-1,s,s+10,s+43] if 0<=f<1800}|{0,15,43,75,1799})
for f in frames:
 r=c.request('tools/call',{'name':'inspect_timeline','arguments':{'startFrame':f}})
 if r.get('isError'):raise RuntimeError(r)
 for j,a in enumerate(r.get('content',[])):
  if a['type']=='image':(out/f'minute_transition_f{f}_{j}.png').write_bytes(base64.b64decode(a['data']))
(out/'session_60s_active.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2));print('captured',len(frames),flush=True)
