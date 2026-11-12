import json,pathlib,sys
root=pathlib.Path('/Users/diplomat/ytvideos');out=root/'channels/paper_detour/videos/003_iq_gallery/Edit/palmier';sys.path.insert(0,str(root/'automation/palmier'));from inspect_connection import PalmierConnection
s=json.loads((out/'session.json').read_text());c=PalmierConnection();c.headers=s['headers'];c.seq=s['seq']
def call(name,args):
 assert '/root/paper_edit' in (root/'channels/paper_detour/.rarovista-timeline-lock/owner.md').read_text();res=c.request('tools/call',{'name':name,'arguments':args})
 if res.get('isError'):raise RuntimeError((name,res))
 txt=[v['text'] for v in res.get('content',[]) if v.get('type')=='text'];obj=json.loads(txt[0]) if len(txt)==1 else txt
 with (out/'edit_receipt.jsonl').open('a') as f:f.write(json.dumps({'tool':name,'args':args,'response':obj},ensure_ascii=False)+'\n')
 (out/'session.json').write_text(json.dumps({'headers':c.headers,'seq':c.seq},indent=2)+'\n');return obj
print('before',call('manage_project',{'action':'list'}));print('close',call('manage_project',{'action':'close'}));print('open',call('manage_project',{'action':'open','path':'/Users/diplomat/Documents/Palmier Pro/Paper Detour 003 IQ Gallery 20261031.palmier'}));t=call('get_timeline',{});assert t['id']=='19F2B39F' and t['totalFrames']==912
(out/'saved_state.json').write_text(json.dumps(t,ensure_ascii=False,indent=2));print('verified',t['id'],len(t['tracks']),sum(len(x['clips']) for x in t['tracks']))
