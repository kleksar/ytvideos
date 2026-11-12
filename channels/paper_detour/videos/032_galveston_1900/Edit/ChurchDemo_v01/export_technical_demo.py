"""Freeze the technical comparison contract, validate saved edit, submit once."""
import hashlib
import json
from palmier_client import call, ROOT

episode=ROOT.parent.parent
run=json.loads((episode/'Edit/ImageMotion/ebff799b152ba8e9e947/run.json').read_text())
assert run['status']=='complete',run
tid=run['target_timeline_id'];pid='25533909'
if (ROOT/'native_export_start.json').exists():raise SystemExit('Export receipt exists; inspect job instead of resubmitting')
timeline=call('get_timeline',{'projectId':pid,'timelineId':tid},'motion_target_pre_export')
assert timeline['width']==2560 and timeline['height']==1440 and timeline['fps']==30 and timeline['totalFrames']==668
assert timeline['outputColorSpace']=='rec709'
scenes=next(t for t in timeline['tracks'] if t['name']=='Scenes')['clips']
assert [c['frames'] for c in scenes]==[[0,167],[167,334],[334,501],[501,668]]
assert all('position' not in c.get('keyframes',{}) and 'scale' not in c.get('keyframes',{}) for c in scenes)
speech=next(t for t in timeline['tracks'] if t['name']=='Dialogue')['clips']
assert len(speech)==1 and speech[0]['frames']==[0,668],speech
assert speech[0]['mediaRef']=='666A8A59' and speech[0]['trimStartFrame']==14173,speech
old=json.loads(json.loads((ROOT/'get_timeline_before.json').read_text())['result']['content'][0]['text'])
preserved=call('get_timeline',{'projectId':pid,'timelineId':'6C26D0C3'},'full_film_preserved_after_demo')
assert old['tracks']==preserved['tracks'] and old['totalFrames']==preserved['totalFrames']
exports=call('manage_exports',{'projectId':pid,'action':'list'},'exports_before_submission')
assert not any(x.get('status') in ('queued','exporting','running','processing') for x in exports.get('exports',[])),exports
contract_path=ROOT/'EXPORT_CONTRACT_technical_v01.json'
c=json.loads(contract_path.read_text());c['status']='READY_TO_RENDER';c['edit']['target_timeline_id']=tid
c['edit']['saved_timeline_receipt']='motion_target_pre_export.json'
c['edit']['saved_timeline_sha256']=hashlib.sha256((ROOT/'motion_target_pre_export.json').read_bytes()).hexdigest()
c['engine']['native_export']['timelineId']=tid
c['preflight']={'author':'codex-galveston-church','readback':'PASS','original_full_timeline_tracks_unchanged':True,'live_project_exports':'no active conflict','storage_audit':'../MediaLifecycle/audit-church-demo-v01/audit.json','date':'2026-11-02'}
contract_path.write_text(json.dumps(c,ensure_ascii=False,indent=2))
result=call('export_project',c['engine']['native_export'],'native_export_start')
print(json.dumps({'timeline_id':tid,'export':result},ensure_ascii=False))
