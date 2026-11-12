import json,time,datetime
from pathlib import Path
from api_inventory import session,get,CHANNEL,BASE,ROOT
D=ROOT/'new_channel/research/2026-11-02-expanded-metadata';plan=json.loads((D/'PLAN.json').read_text())
(D/'receipts').mkdir(exist_ok=True)
with session() as s:
 c=get(s,'channels',part='id',mine='true')['items'];assert len(c)==1 and c[0]['id']==CHANNEL
 for row in plan['rows']:
  id=row['video_id'];out=D/'receipts'/f'{id}.json'
  if out.exists():
   prior=json.loads(out.read_text())
   assert prior['state'] in ('applied_verified','unchanged_verified'),'Existing receipt: reconcile before another write'
   print(id,'already verified; no repeated write',flush=True);continue
  before=get(s,'videos',part='snippet,status,contentDetails,localizations',id=id)['items'][0]
  assert before['snippet']['channelId']==CHANNEL
  sn=before['snippet']
  if sn['title']!=row['before_title'] or sn['description']!=row['before_description']:
   out.write_text(json.dumps({'video_id':id,'status':'concurrent_change_needs_reconciliation','before':before},ensure_ascii=False,indent=2)+'\n');print(id,'CONCURRENT CHANGE; left untouched',flush=True);continue
  changes={k:row[k] for k in ('title','description') if row[k]!=sn[k]}
  receipt={'video_id':id,'channel_id':CHANNEL,'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'before':before,'requested_changes':changes,'state':'no_write_needed' if not changes else 'write_outcome_unknown'}
  out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
  if changes:
   mutable={k:sn[k] for k in ['title','description','tags','categoryId','defaultLanguage','defaultAudioLanguage'] if k in sn};mutable.update(changes)
   body={'id':id,'snippet':mutable};receipt['request']=body;out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
   response=s.put(BASE+'videos',params={'part':'snippet'},json=body,headers={'If-Match':before['etag']},timeout=45)
   receipt['http_status']=response.status_code
   out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
   if response.status_code!=200:
    receipt['reconciled']=get(s,'videos',part='snippet,status',id=id)['items'];out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');raise RuntimeError(f'{id} HTTP{response.status_code};no retry')
   receipt['response']=response.json()
  for attempt in range(4):
   after=get(s,'videos',part='snippet,status,contentDetails,localizations',id=id)['items'][0]
   if all(after['snippet'][k]==row[k] for k in ('title','description')):break
   if attempt<3:time.sleep(2)
  assert all(after['snippet'][k]==row[k] for k in ('title','description')),'Read-back unresolved; no repeated write'
  for key in ['tags','categoryId','defaultLanguage','defaultAudioLanguage']:
   assert after['snippet'].get(key)==sn.get(key),f'Unexpected {key} difference'
  assert after['status']==before['status'],'Unrequested status changed externally;needs reconciliation'
  localization_changes=[k for k in set(before.get('localizations',{}))|set(after.get('localizations',{})) if before.get('localizations',{}).get(k)!=after.get('localizations',{}).get(k)]
  receipt.update(state='applied_verified' if changes else 'unchanged_verified',after=after,preserved_fields=['tags','categoryId','defaultLanguage','defaultAudioLanguage','status'],unrequested_localization_changes={'languages':sorted(localization_changes),'origin':'unverified; no localizations part written; not overwritten to force preservation'},note='snippet-only update; covers and playlists not mutated. Before/after values compared, not inferred from ETag.')
  out.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
  local=Path(row['episode_path'])/'Packaging/Metadata';(local/'EXPANDED_METADATA_RECEIPT_20261102.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
  print(id,receipt['state'],','.join(changes) or 'no change',flush=True)
