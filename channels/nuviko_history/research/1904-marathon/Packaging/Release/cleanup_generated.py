import os, json, pathlib, hashlib, datetime, shutil
b=pathlib.Path(__file__).resolve().parent; audit=json.loads((b/'IMAGEGEN_AUDIT_v01.json').read_text()); root=pathlib.Path('/Users/diplomat/.codex/generated_images/01a1bba2-5638-7823-9537-c8ac0c0016cd').resolve(); out=[]; errors=[];before=shutil.disk_usage(root).free
for entry in audit['matching']:
 p=pathlib.Path(entry['path'])
 try:
  if p.is_symlink() or p.parent.resolve()!=root or not p.name.startswith('exec-') or p.suffix!='.png': raise ValueError('path outside exact owned set')
  st=p.stat()
  if st.st_nlink!=1 or st.st_size!=entry['size']:raise ValueError('file identity changed')
  h=hashlib.sha256(p.read_bytes()).hexdigest()
  if h!=entry['sha256']:raise ValueError('content changed')
  p.unlink();out.append({'path':str(p),'sha256':h,'bytes':st.st_size})
 except Exception as exc: errors.append({'path':str(p),'error':str(exc)})
result={'completed_at':datetime.datetime.now().astimezone().isoformat(),'files_removed':len(out),'bytes_removed':sum(i['bytes'] for i in out),'removed':out,'errors':errors,'unmatched_preserved':audit['unknown_left_untouched'],'free_before':before,'free_after':shutil.disk_usage(root).free}
(b/'CLEANUP_GENERATED_RECEIPT_v01.json').write_text(json.dumps(result,indent=2)+'\n');print('Removed',len(out),'matched generated originals;',round(result['bytes_removed']/1048576,1),'MiB; errors',len(errors),'; unrelated/unmatched preserved',len(audit['unknown_left_untouched']))
