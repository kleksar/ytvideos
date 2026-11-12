import importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parent; P='B1BA2D18'; source='B75DA155'
s=importlib.util.spec_from_file_location('p','/Users/diplomat/ytvideos/automation/palmier/inspect_connection.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);c=m.PalmierConnection();c.connect()
def call(name,args):
 res=c.request('tools/call',{'name':name,'arguments':args})
 with (R/'short_receipts.jsonl').open('a') as f:f.write(json.dumps({'name':name,'arguments':args,'response':res},ensure_ascii=False)+'\n')
 if res.get('isError'):raise RuntimeError(str(res))
 return json.loads(res['content'][0]['text'])
def timeline(t):return c.read_tool('get_timeline',{'projectId':P,'timelineId':t})
a=timeline(source);sc=next(x for x in a['tracks'] if x['name']=='Scenes')['clips']; intended=json.loads((R/'intended.json').read_text());assert len(intended)>=15
for i in range(15):
 assert all(sc[i][k]==intended[i][k] for k in ('id','frames','mediaRef'))
end=sc[14]['frames'][1]; assert end==2146
new=call('create_timeline',{'projectId':P,'from':source,'name':'Clothing History — 15 scenes gentle aligned parallax'});T=new['timelineId'];(R/'short_timeline_id.txt').write_text(T+'\n');print('CREATED',T,flush=True)
b=timeline(T);(R/'short_before.json').write_text(json.dumps(b,ensure_ascii=False,indent=2));print('SNAPSHOT',call('manage_snapshots',{'projectId':P,'timelineId':T,'action':'save','name':'Before 15-scene parallax direction alignment'}),flush=True)
sc=next(x for x in b['tracks'] if x['name']=='Scenes')['clips']; changed=[]
for n,clip in enumerate(sc[:15],1):
 p=clip['keyframes']['position'];s=clip['keyframes']['scale'];c0=p[0][1]+s[0][1]/2;c1=p[1][1]+s[1][1]/2;delta=c1-c0;desired=-1 if n%2 else 1
 if delta*desired < -0.002:
  newp=[row.copy() for row in p];newp[0][1]=round(c1-s[0][1]/2,8);newp[1][1]=round(c0-s[1][1]/2,8)
  call('set_keyframes',{'projectId':P,'timelineId':T,'clipId':clip['id'],'property':'position','keyframes':newp});changed.append(n)
print('DIRECTION_ADJUSTED',changed,flush=True)
cur=timeline(T);cross=[{'clipId':clip['id'],'atFrame':end} for track in cur['tracks'] for clip in track['clips'] if clip['frames'][0]<end<clip['frames'][1]];assert len(cross)==2
print('SPLIT',call('split_clips',{'projectId':P,'timelineId':T,'splits':cross}),flush=True)
cur=timeline(T);to_remove=[clip['id'] for track in cur['tracks'] for clip in track['clips'] if clip['frames'][0]>=end];assert len(to_remove)==47
print('REMOVE',call('remove_clips',{'projectId':P,'timelineId':T,'clipIds':to_remove}),flush=True)
final=timeline(T);tracks={x['name']:x for x in final['tracks']};assert len(tracks['Scenes']['clips'])==15 and len(tracks['Accents']['clips'])==13 and final['totalFrames']==end
assert all(x['frames'][1]<=end for track in final['tracks'] for x in track['clips'])
for n,clip in enumerate(tracks['Scenes']['clips'],1):
 want=intended[n-1];assert clip['frames']==want['frames'] and clip['mediaRef']==want['mediaRef'] and all(abs(a[1]-b[1]) < .001 for a,b in zip(clip['keyframes']['scale'],want['keyframes']['scale']))
 p=clip['keyframes']['position'];s=clip['keyframes']['scale'];d=(p[1][1]+s[1][1]/2)-(p[0][1]+s[0][1]/2);assert d*(-1 if n%2 else 1)>=-.002
(R/'short_final.json').write_text(json.dumps(final,ensure_ascii=False,indent=2));print('FINAL_SNAPSHOT',call('manage_snapshots',{'projectId':P,'timelineId':T,'action':'save','name':'15 scenes gentle alternating parallax aligned'}),flush=True)
print('DONE',json.dumps({'timeline':T,'frames':end,'scenes':15,'accents':13,'directionAdjusted':changed},ensure_ascii=False),flush=True)
