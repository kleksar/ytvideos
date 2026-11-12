import importlib.util,json,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent; P='B1BA2D18'; T=(R/'timeline_id.txt').read_text().strip(); baseline=json.loads((R/'baseline.json').read_text()); prior=next(t for t in baseline['tracks'] if t['name']=='Scenes')['clips']
s=importlib.util.spec_from_file_location('p','/Users/diplomat/ytvideos/automation/palmier/inspect_connection.py'); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); c=m.PalmierConnection(); c.connect()
def call(name,args):
 res=c.request('tools/call',{'name':name,'arguments':args})
 with (R/'receipts.jsonl').open('a') as f: f.write(json.dumps({'name':name,'arguments':args,'response':res},ensure_ascii=False)+'\n')
 if res.get('isError'): raise RuntimeError(f'{name}: {res}')
 return json.loads(res['content'][0]['text'])
def timeline(): return c.read_tool('get_timeline',{'projectId':P,'timelineId':T})
def scaled_keys(clip):
 old=clip['keyframes']; p=old['position']; s=old['scale']; newp=[]; news=[]
 for i in range(2):
  values=[]; scales=[]
  for axis in (1,2):
   center0=p[0][axis]+s[0][axis]/2; center1=p[1][axis]+s[1][axis]/2
   center=(center0+center1)/2+.75*((center0 if i==0 else center1)-(center0+center1)/2)
   mid=(s[0][axis]+s[1][axis])/2; scale=mid+.75*(s[i][axis]-mid)
   values.append(round(center-scale/2,8)); scales.append(round(scale,8))
  newp.append([p[i][0],*values,*p[i][3:]]); news.append([s[i][0],*scales,*s[i][3:]])
 return {'position':newp,'scale':news}
start=time.monotonic(); intended=[]
for i,clip in enumerate(prior,1):
 out=R/f'parallax_{i:02}.mp4'; n=clip['frames'][1]-clip['frames'][0]; deadline=time.monotonic()+600
 while True:
  if out.exists():
   probe=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames','-of','json',str(out)],capture_output=True,text=True)
   try:
    v=json.loads(probe.stdout)['streams'][0]
    if (int(v['nb_frames']),v['r_frame_rate'],v['width'],v['height'])==(n+2,'30/1',1920,1080): break
   except (ValueError,KeyError,IndexError): pass
  if time.monotonic()>deadline: raise RuntimeError(f'Render timeout at scene {i}')
  time.sleep(3)
 actual=next(x for x in timeline()['tracks'] if x['name']=='Scenes')['clips'][i-1]
 if actual!=clip: raise RuntimeError(f'Scene {i} changed before edit')
 imported=call('import_media',{'projectId':P,'source':{'path':str(out)},'folder':'Parallax 75 percent alternating'})
 result=call('swap_clip_media',{'projectId':P,'timelineId':T,'clipId':clip['id'],'mediaRef':imported['mediaRef']})
 if result.get('changed') is not True: raise RuntimeError(f'Swap failed for scene {i}: {result}')
 keys=scaled_keys(clip)
 for prop in ('position','scale'): call('set_keyframes',{'projectId':P,'timelineId':T,'clipId':clip['id'],'property':prop,'keyframes':keys[prop]})
 intended.append({'id':clip['id'],'mediaRef':imported['mediaRef'],'frames':clip['frames'],'keyframes':keys,'direction':'forward' if i%2 else 'reverse'})
 (R/'intended.json').write_text(json.dumps(intended,ensure_ascii=False,indent=2))
 print(json.dumps({'applied':i,'total':39,'elapsed':round(time.monotonic()-start,1)}),flush=True)
final=timeline(); clips=next(t for t in final['tracks'] if t['name']=='Scenes')['clips']
for want,got in zip(intended,clips):
 for field in ('id','mediaRef','frames','keyframes'):
  if want[field]!=got[field]: raise RuntimeError(f'Final mismatch: {field} {want["id"]}: {want[field]} != {got[field]}')
for name in ('Accents','Grain','Mix'):
 if next(t for t in baseline['tracks'] if t['name']==name)!=next(t for t in final['tracks'] if t['name']==name): raise RuntimeError('Unexpected change to '+name)
(R/'timeline_final.json').write_text(json.dumps(final,ensure_ascii=False,indent=2))
snap=call('manage_snapshots',{'projectId':P,'timelineId':T,'action':'save','name':'Alternating parallax and camera movement 75%'}); print('DONE',json.dumps(snap,ensure_ascii=False),flush=True)
