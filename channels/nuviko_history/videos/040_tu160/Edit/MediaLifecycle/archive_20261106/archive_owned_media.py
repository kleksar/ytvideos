from pathlib import Path
import os,json,hashlib,datetime,subprocess
root=Path(__file__).resolve().parents[3];out=Path(__file__).resolve().parent
ext={'.mp4','.mov','.mkv','.webm','.png','.jpg','.jpeg','.webp','.wav','.mp3','.m4a','.aac','.flac','.pyc'}
now=lambda:datetime.datetime.now().astimezone().isoformat()
free_before=os.statvfs(root).f_bavail*os.statvfs(root).f_frsize
files=[]; holds=[]
for d,dirs,names in os.walk(root,followlinks=False):
 dirs[:]=[x for x in dirs if not (Path(d)/x).is_symlink()]
 for name in names:
  p=Path(d)/name
  if p.suffix.lower() not in ext:continue
  if p.is_symlink():holds.append({'path':str(p),'reason':'symlink'});continue
  s=p.stat()
  if s.st_nlink!=1:holds.append({'path':str(p),'reason':'hardlink'});continue
  h=hashlib.sha256()
  with p.open('rb') as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
  s2=p.stat()
  if (s.st_size,s.st_mtime_ns,s.st_ino)!=(s2.st_size,s2.st_mtime_ns,s2.st_ino):holds.append({'path':str(p),'reason':'changed during inventory'});continue
  files.append({'path':str(p),'size':s.st_size,'mtime_ns':s.st_mtime_ns,'inode':s.st_ino,'sha256':h.hexdigest()})
print('INVENTORY',len(files),sum(x['size'] for x in files), 'holds',len(holds),flush=True)
plan={'stage':'planned','created':now(),'scope':str(root),'reason':'user-directed cleanup of accepted published episode','remote_video':'aqPKvN6dh2o','remote_channel':'UCbyLx6Rf3iWww4bPZJ2oo2A','free_before':free_before,'files':files,'holds':holds,'previous_hold':'v01 QuickLook hold rechecked; lsof no open descriptors','external_rejected_trash':'recorded ~/.Trash/040_tu160_rejected_images path absent at check'}
(out/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
print('PLAN_SAVED',flush=True)
lsof=subprocess.run(['lsof','+D',str(root)],capture_output=True,text=True)
if lsof.returncode not in (0,1) or lsof.stdout.strip():raise SystemExit('Open files or lsof error; no deletion performed')
removed=[]
for i,item in enumerate(files):
 p=Path(item['path'])
 try:
  st=p.stat()
  if p.is_symlink() or (st.st_size,st.st_mtime_ns,st.st_ino,st.st_nlink)!=(item['size'],item['mtime_ns'],item['inode'],1):holds.append({'path':str(p),'reason':'changed before deletion'});continue
  p.unlink();removed.append(item)
 except OSError as e:holds.append({'path':str(p),'reason':str(e)})
 if (i+1)%3000==0:print('REMOVED',i+1,flush=True)
free_after=os.statvfs(root).f_bavail*os.statvfs(root).f_frsize
receipt={'stage':'completed','time':now(),'count':len(removed),'logical_bytes':sum(x['size'] for x in removed),'free_before':free_before,'free_after':free_after,'free_change':free_after-free_before,'holds':holds,'removed':removed,'plan':str(out/'plan.json')}
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('DONE',len(removed),receipt['logical_bytes'],'holds',len(holds),'free_change',receipt['free_change'],flush=True)
