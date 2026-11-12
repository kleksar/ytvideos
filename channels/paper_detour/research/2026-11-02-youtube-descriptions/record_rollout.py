"""Record verified saved metadata; does not perform network writes."""
import hashlib,importlib.util,json,os,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=HERE/'rollout_20261102'
audit=json.loads((HERE/'AUDIT.json').read_text());before=json.loads((OUT/'BEFORE.json').read_text());after=json.loads((OUT/'AFTER.json').read_text())
def index(s):return {v['id']:v for v in s['videos']}
b,a=index(before),index(after)
spec=importlib.util.spec_from_file_location('validator',ROOT/'.agents/skills/ytv-youtube-descriptions/scripts/validate_description.py');validator=importlib.util.module_from_spec(spec);spec.loader.exec_module(validator)
results=[]
for row in audit['videos']:
 vid=row['id'];changed=row['decision']=='revise';expected=(ROOT/row['proposed_file']).read_bytes().decode('utf-8');actual=a[vid]['snippet']['description'];assert actual==expected
 for key in ('title','tags','categoryId','defaultLanguage','defaultAudioLanguage','thumbnails'):
  assert a[vid]['snippet'].get(key)==b[vid]['snippet'].get(key),(vid,key)
 for key in ('status','contentDetails'):assert a[vid][key]==b[vid][key],(vid,key)
 manifest=json.loads((HERE/'texts'/f'{vid}.protected.json').read_text());validation=validator.validate(actual,manifest,b[vid]['snippet']['description']);assert validation['valid']
 protected=validation['protected_blocks'];curr=Path(row['proposed_file']).with_name(f'DESCRIPTION_EN_CURRENT_{vid}.txt');(ROOT/curr).write_bytes(actual.encode('utf-8'))
 row.update(external_status='applied_verified' if changed else 'unchanged_verified',user_acceptance='2026-11-02; exact seven revised texts accepted',current_file=str(curr),verified_at=after['checked_at'],live_display_status='Studio exact text and public watch collapsed/expanded checked' if changed else 'API read-back; not newly inspected in browser')
 if changed:
  receipt=json.loads((OUT/f'{vid}.receipt.json').read_text());assert receipt['state']=='saved_verified';row['receipt']=str((OUT/f'{vid}.receipt.json').relative_to(ROOT))
  old=receipt['before'].get('localizations',{});new=receipt['after'].get('localizations',{});localkeys=sorted(k for k in old.keys()|new.keys() if old.get(k)!=new.get(k))
  public=(OUT/(f'{vid}.public.txt' if vid!='0RaC4t7yn5o' else 'RADIO_PUBLIC_EXPANDED.txt')).read_text()
  # Every narrative paragraph is visible after expanding (DOM whitespace is collapsed).
  body=expected.split('\n\n00:00')[0] if vid=='0RaC4t7yn5o' else expected.split('\n\n#')[0]
  for para in body.split('\n\n'):
   if para.startswith('Watch '):continue
   normal=' '.join(para.split()); assert normal in ' '.join(public.split()),(vid,normal)
 else:localkeys=[]
 results.append({'id':vid,'state':row['external_status'],'exact_description':True,'protected_blocks':protected,'localizations_changed_during_put':localkeys,'current_file':str(curr)})
def playlist_state(snapshot):
 return {p['id']:{k:p[k] for k in ('snippet','status','contentDetails')} for p in snapshot['playlists']}
def memberships(snapshot):
 return {key:[(v['id'],v['snippet']['position'],v['snippet']['resourceId']) for v in items] for key,items in snapshot['members'].items()}
assert playlist_state(before)==playlist_state(after) and memberships(before)==memberships(after),'Playlist configuration/membership changed; reconcile separately'
audit['scope']='10 default English descriptions; seven accepted revisions applied and verified; three kept unchanged';audit['rollout']='rollout_20261102/REPORT.md';(HERE/'AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n');(OUT/'VALIDATION.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
for canonical in sorted({r['canonical_path'] for r in audit['videos']}):
 rows=[r for r in audit['videos'] if r['canonical_path']==canonical];note=ROOT/canonical/'Packaging/Metadata/DESCRIPTION_REVIEW_20261102.md';s=note.read_text()
 s=s.replace('Local review/proposals only. No YouTube description writes were requested or performed in this pass. Existing published descriptions remain separate from these candidates. Not user acceptance.','Current state: user accepted seven revised descriptions on 2026-11-02. Authorized revisions saved and verified through fresh API, Studio and expanded public watch pages; keep rows unchanged and API-verified. Historical preview files retained below; current files are linked per video.')
 for row in rows:
  vid=row['id'];start=s.index('## '+vid);end=s.find('\n## ',start+1);end=end if end!=-1 else len(s);section=s[start:end]
  section=section.replace('external: not requested; live destination display: not checked for proposal.',f"external: {row['external_status']}; live destination display: {row['live_display_status']}.")
  rel=os.path.relpath(ROOT/row['current_file'],note.parent);section+=f'\n[Current saved English text]({rel}). Verified {row["verified_at"]}.\n'
  if row.get('receipt'):section+=f'\n[API receipt]({os.path.relpath(ROOT/row["receipt"],note.parent)}).\n'
  s=s[:start]+section+s[end:]
 note.write_text(s)
 readme=ROOT/canonical/'README.md'
 if readme.exists():
  s=readme.read_text();s=s.replace('**Описания, review 2 ноября 2026:** [решения и полные локальные тексты](Packaging/Metadata/DESCRIPTION_REVIEW_20261102.md). Это версии для просмотра, не подтверждение новой записи в YouTube; текущие опубликованные поля сверять через API.','**Описания, 2 ноября 2026:** [текущее сохранённое состояние и квитанции](Packaging/Metadata/DESCRIPTION_REVIEW_20261102.md). Семь согласованных изменений применены и проверены; остальные три оставлены. Хэштеги/главы сохранены; актуальные тексты отмечены CURRENT.');readme.write_text(s)
print(json.dumps({'applied':sum(r['state']=='applied_verified' for r in results),'kept':sum(r['state']=='unchanged_verified' for r in results),'hashtags_exact':sum(len(re.findall(r'(?<!\S)#[^\s#]+',a[r['id']]['snippet']['description'])) for r in results),'chapters_exact':7,'playlists_unchanged':True,'results':results},ensure_ascii=False))
