from pathlib import Path
import json,hashlib,datetime
root=Path(__file__).resolve().parents[3];plan=root/'Edit/Production/v03/plan.json';p=json.loads(plan.read_text());p['subtitles']['review']='../../../Work/production-text-v03/prepare/subtitle_review.json';plan.write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
h=lambda f:hashlib.sha256(Path(f).read_bytes()).hexdigest()
c=json.loads((root/'Edit/Export/EXPORT_CONTRACT_v02.json').read_text());c['purpose']='Review export with ten regenerated images containing text in-scene; existing mix, caption wording, timing and shot durations preserved; no publication authorized.'
e=c['edit'];e['timeline_id']=str(plan);e['timeline_read_path']=str(plan);e['timeline_read_sha256']=h(plan);e['saved_revision_evidence']={'path':str(plan),'sha256':h(plan)}
paths=[plan,root/'Source/Audio/mix_en_v01.wav',root/'Source/Audio/word_map_mix_v01.json',root/'Source/Voice/voice_en_text_v01.txt',root/'Work/production-text-v03/prepare/subtitle_review.json']+list(dict.fromkeys(Path(s['image']) for s in p['scenes']))
e['dependencies']=[{'path':str(x),'sha256':h(x)} for x in paths]
w=root/'Work/production-text-v03/settings';out=root/'Deliverables/NUVIKO_040_TU160_EN_REVIEW_v03.mp4'
c['preflight'].update({'time':datetime.datetime.now().astimezone().isoformat(),'authorization_references':['User approved the existing film and requested regenerative in-image text, preserving soundtrack.','User approved the subtitle break after more than.'],'fresh_settings_evidence':str(w/'settings_check.json'),'writer_and_export_state':'New v03 output, no known competing writer.','output_path':str(out),'overwrite':False,'media_lifecycle_receipt':'v02 is last user-approved baseline; v01 has active hold. Both retained, no cleanup claimed.','unresolved_required_fields':[]})
c['settings_check_receipt']=str(w/'settings_check.json');c['render_receipt']=None;c['qa_receipt']=None;c['render_provenance']=None
path=root/'Edit/Export/EXPORT_CONTRACT_v03.json';path.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n');print(path)
