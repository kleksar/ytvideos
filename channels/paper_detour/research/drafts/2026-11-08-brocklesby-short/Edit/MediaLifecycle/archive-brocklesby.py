"""Retire this one published episode's owned local media after verified release."""
import datetime,hashlib,json,os,shutil,stat,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
life=Path(__file__).resolve().parent
plan_path=life/'text-only-plan-20261108.json'
receipt_path=life/'text-only-receipt-20261108.json'
proof_path=root/'Packaging/Metadata/RELEASE_RECEIPT_20261108.json'
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
 return h.hexdigest()
def ident(path):
 s=path.lstat()
 if not stat.S_ISREG(s.st_mode) or path.resolve()!=path: raise ValueError('not an owned regular file: '+str(path))
 return dict(path=str(path),bytes=s.st_size,inode=s.st_ino,device=s.st_dev,nlink=s.st_nlink,mtime_ns=s.st_mtime_ns,sha256=sha(path))
def dump(path, data):
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
release=json.loads(proof_path.read_text())
assert release['release']['state']=='confirmed' and release['release']['privacy']=='public' and release['release']['processing']=='succeeded'
assert release['release']['video_id']=='azhQEhV6ywg' and release['anonymous_oembed']['result']=='PASS'
suffixes={'.png','.jpg','.jpeg','.mp3','.mp4','.wav'}
if sys.argv[1]=='plan':
 assert not plan_path.exists()
 local=[ident(p) for p in sorted(root.rglob('*')) if p.suffix.lower() in suffixes and p.is_file()]
 for row in local:
  assert row['nlink']==1 and Path(row['path']).is_relative_to(root)
  row.update(owner='Brocklesby release azhQEhV6ywg',consumer='This episode only. No other local project references its output/episode path; release handoff complete.')
 generated=json.loads((root/'Source/Images/imagegen-requests.json').read_text())
 external=sorted({r['path'] for r in generated if Path(r['path']).exists() and not Path(r['path']).is_relative_to(root)})
 dump(plan_path,dict(created_at=now(),release_sha256=sha(proof_path),retired_timeline='edit-v01',local=local,external_holds=[dict(ident(Path(p)),reason='Generated original outside writable project. Retain source history in the tool export location pending separate storage access.') for p in external]))
 print(len(local),sum(x['bytes'] for x in local),'external holds:',len(external))
elif sys.argv[1]=='execute':
 plan=json.loads(plan_path.read_text())
 assert plan['release_sha256']==sha(proof_path) and not receipt_path.exists()
 before=shutil.disk_usage(root).free
 holds=[]; results=[]
 entries=plan['local']
 active=set()
 for offset in range(0,len(entries),80):
  names=[r['path'] for r in entries[offset:offset+80]]
  opened=subprocess.run(['/usr/sbin/lsof','-Fn','--',*names],capture_output=True,text=True)
  if opened.stderr or opened.returncode not in (0,1):
   active.update(names)
  else:
   active.update(line[1:] for line in opened.stdout.splitlines() if line.startswith('n'))
 for row in entries:
  path=Path(row['path'])
  expected={k:v for k,v in row.items() if k not in ('owner','consumer')}
  try:
   assert path.is_relative_to(root) and ident(path)==expected and path.suffix.lower() in suffixes
   if str(path) in active:
    holds.append(dict(path=str(path),reason='live writer or unknown lsof result'));continue
   assert path.stat().st_ino==row['inode'] and path.stat().st_mtime_ns==row['mtime_ns']
   path.unlink()
   if path.exists(): raise ValueError('still present after unlink')
   results.append(dict(path=str(path),sha256=row['sha256'],bytes=row['bytes'],result='deleted'))
  except (OSError,AssertionError,ValueError) as error:
   holds.append(dict(path=str(path),reason=type(error).__name__))
  if len(results)%40==0: dump(life/'text-only-journal-20261108.json',dict(results=results,holds=holds))
 for directory in sorted((p for p in root.rglob('*') if p.is_dir() and not p.is_symlink()),key=lambda p:-len(p.parts)):
  if directory.name!='Deliverables' and not any(directory.iterdir()): directory.rmdir()
 remains=[str(p) for p in root.rglob('*') if p.is_file() and p.suffix.lower() in suffixes]
 after=shutil.disk_usage(root).free
 state='PARTIAL_TEXT_ARCHIVE' if remains or holds or plan['external_holds'] else 'TEXT_ONLY'
 dump(receipt_path,dict(verified_at=now(),storage_state=state,remote_video_id='azhQEhV6ywg',remote_url=release['url'],remote_status='public / processed',plan_sha256=sha(plan_path),deleted_files=len(results),deleted_logical_bytes=sum(r['bytes'] for r in results),volume_free_before=before,volume_free_after=after,physical_reclaim='Not attributable to this cleanup alone',results=results,local_holds=holds,remaining_local_media=remains,external_holds=plan['external_holds']))
 print(state,len(results),sum(r['bytes'] for r in results),'local holds:',len(holds),'external holds:',len(plan['external_holds']))
else: raise ValueError('expected plan or execute')
