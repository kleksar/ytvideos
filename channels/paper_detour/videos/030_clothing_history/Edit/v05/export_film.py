from palmier_client import call,ROOT
import base64,json
P='B1BA2D18';T='E69F8516';target={'projectId':P,'timelineId':T}
for frame in [60,3360]:
 r=call('inspect_timeline',{**target,'startFrame':frame});imgs=[x for x in r.get('content',[]) if x.get('type')=='image']
 for i,b in enumerate(imgs):(ROOT/f'Edit/v05/native_preview_f{frame}_{i}.png').write_bytes(base64.b64decode(b['data']))
 print('Inspected frame',frame,'images',len(imgs),flush=True)
r=call('export_project',{**target,'mode':'video','codec':'H.264','resolution':'1080p','outputPath':str(ROOT/'Edit/v05/Palmier_export.mp4'),'overwrite':False})
(ROOT/'Edit/v05/export_job.json').write_text(json.dumps(r,indent=2));print(json.dumps(r),flush=True)
