#!/usr/bin/env python3
"""Upload one English SRT track to an owned private video safely.

`prepare` is offline. `upload` requires explicit IDs, a matching upload receipt
and a manage token. An exclusive per-channel/video English receipt is reserved
before POST; timeout or uncertain response never causes an automatic retry.
Existing manual English track contents cannot be verified from the listing, so
an unrelated pre-existing track stops the operation for manual review.
"""
import argparse,hashlib,json,os,re,sys,time,uuid
from pathlib import Path
API='https://www.googleapis.com/youtube/v3/'
UPLOAD='https://www.googleapis.com/upload/youtube/v3/captions'
SCOPE='https://www.googleapis.com/auth/youtube.force-ssl'
STATE=Path.home()/'.local/share/story-youtube/caption-receipts'

class CaptionError(Exception):pass

def valid_ids(channel,video):
 if not re.fullmatch(r'UC[A-Za-z0-9_-]{22}',channel or '') or not re.fullmatch(r'[A-Za-z0-9_-]{11}',video or ''):raise CaptionError('Invalid channel or video ID')

def srt_data(path):
 p=Path(path).resolve(strict=True)
 if not p.is_file() or p.suffix.lower()!='.srt' or p.stat().st_size>10_000_000:raise CaptionError('Invalid or oversized SRT')
 raw=p.read_bytes()
 try:text=raw.decode('utf-8-sig')
 except UnicodeDecodeError:raise CaptionError('SRT must be UTF-8') from None
 lines=re.findall(r'(?m)^\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*$',text)
 if not lines:raise CaptionError('No valid SRT timecodes')
 def ms(x):
  h,m,s,q=map(int,x)
  if m>=60 or s>=60:raise CaptionError('Invalid SRT timecode')
  return ((h*60+m)*60+s)*1000+q
 last=-1
 for line in lines:
  start,end=ms(line[:4]),ms(line[4:])
  if start<last or end<=start:raise CaptionError('SRT cues overlap or are invalid')
  last=end
 return {'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'cues':len(lines)},raw

def get_items(session,resource,params):
 items=[];params=dict(params)
 while True:
  try:r=session.get(API+resource,params=params,timeout=30,allow_redirects=False)
  except Exception:raise CaptionError('Read failed; check connection') from None
  if r.status_code!=200:raise CaptionError(f'{resource} read failed (HTTP {r.status_code})')
  data=r.json();items.extend(data.get('items',[]));token=data.get('nextPageToken')
  if not token:return items
  if resource=='videos':raise CaptionError('Unexpected video pagination')
  params['pageToken']=token

def verify(session,channel,video):
 valid_ids(channel,video)
 cs=get_items(session,'channels',{'part':'id','mine':'true'})
 if len(cs)!=1 or cs[0].get('id')!=channel:raise CaptionError('Authorized channel does not match')
 vids=get_items(session,'videos',{'part':'id,snippet,status,processingDetails','id':video})
 if len(vids)!=1 or vids[0].get('id')!=video or vids[0].get('snippet',{}).get('channelId')!=channel:raise CaptionError('Video is not owned by expected channel')
 v=vids[0]
 if v.get('status',{}).get('privacyStatus')!='private':raise CaptionError('Video is not private')
 if v.get('processingDetails',{}).get('processingStatus')!='succeeded':raise CaptionError('Video processing is not confirmed succeeded')
 return v

def captions(session,video):return get_items(session,'captions',{'part':'snippet','videoId':video})
def english_manual(items):return [x for x in items if x.get('snippet',{}).get('language','').lower().split('-')[0]=='en' and x.get('snippet',{}).get('trackKind','').lower()!='asr']

def verify_upload_receipt(path,channel,video):
 try:r=json.loads(Path(path).read_text())
 except Exception:raise CaptionError('Upload receipt cannot be read') from None
 f=r.get('fingerprint',{})
 if r.get('phase')!='complete' or r.get('video_id')!=video or f.get('channel_id')!=channel or f.get('body',{}).get('status',{}).get('privacyStatus')!='private':raise CaptionError('Upload receipt does not match a private video upload')

def reserve(path,payload):
 path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
 try:fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
 except FileExistsError:raise CaptionError('Another caption upload already has a receipt; inspect before retrying') from None
 with os.fdopen(fd,'w') as f:json.dump(payload,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())

def save(path,payload):
 tmp=path.with_name(path.name+'.tmp')
 try:fd=os.open(tmp,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
 except FileExistsError:raise CaptionError('Temporary caption receipt exists; inspect state') from None
 with os.fdopen(fd,'w') as f:json.dump(payload,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)

def wait_serving(session,video,caption_id,sleep=time.sleep):
 for attempt in range(6):
  matches=[x for x in captions(session,video) if x.get('id')==caption_id]
  if len(matches)==1:
   s=matches[0].get('snippet',{})
   if s.get('videoId')!=video or s.get('language','').lower().split('-')[0]!='en' or s.get('isDraft'):raise CaptionError('Caption identity, language or draft state differs')
   if s.get('status')=='serving':return
   if s.get('status')=='failed':raise CaptionError('Caption processing failed; inspect Studio')
  if attempt<5:sleep(2)
 raise CaptionError('Caption not confirmed serving; inspect Studio before retrying')

def upload(session,channel,video,srt,upload_receipt,state_dir=STATE,sleep=time.sleep):
 valid_ids(channel,video);data,raw=srt_data(srt);verify_upload_receipt(upload_receipt,channel,video);verify(session,channel,video)
 items=english_manual(captions(session,video));state=Path(state_dir)/(channel+'_'+video+'_en.json')
 if len(items)>1:raise CaptionError('Multiple manual English tracks; inspect before proceeding')
 if state.exists():
  try:r=json.loads(state.read_text())
  except Exception:raise CaptionError('Caption receipt unreadable; inspect manually') from None
  if r.get('channel_id')!=channel or r.get('video_id')!=video or r.get('srt_sha256')!=data['sha256']:raise CaptionError('Existing receipt does not match this video and SRT')
  if r.get('state') not in ('uploaded','confirmed') or not r.get('caption_id'):raise CaptionError('Previous upload outcome unknown; inspect captions and receipt before retry')
  if len(items)!=1 or items[0].get('id')!=r['caption_id']:raise CaptionError('Receipt track not uniquely visible; inspect before retry')
  wait_serving(session,video,r['caption_id'],sleep);verify(session,channel,video)
  if r['state']!='confirmed':r['state']='confirmed';save(state,r)
  return {'result':'existing_confirmed','channel_id':channel,'video_id':video,'caption_id':r['caption_id'],'status':'serving','srt_sha256':data['sha256']}
 if items:raise CaptionError('An English manual track already exists; its contents are not verified; inspect manually')
 record={'state':'outcome_unknown','channel_id':channel,'video_id':video,'srt_path':data['path'],'srt_sha256':data['sha256']};reserve(state,record)
 verify(session,channel,video)
 if english_manual(captions(session,video)):raise CaptionError('English track appeared before upload; inspect receipt and Studio')
 boundary='ytcap_'+uuid.uuid4().hex
 meta={'snippet':{'videoId':video,'language':'en','name':'English','isDraft':False}}
 body=(f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()+json.dumps(meta).encode()+f'\r\n--{boundary}\r\nContent-Type: application/octet-stream\r\n\r\n'.encode()+raw+f'\r\n--{boundary}--\r\n'.encode())
 try:r=session.post(UPLOAD,params={'part':'snippet','uploadType':'multipart'},headers={'Content-Type':f'multipart/related; boundary={boundary}'},data=body,timeout=60,allow_redirects=False)
 except Exception:raise CaptionError('Caption upload outcome unknown; inspect Studio and receipt before retry') from None
 if r.status_code not in (200,201):raise CaptionError(f'Caption upload HTTP {r.status_code}; inspect Studio and receipt before retry')
 try:cid=r.json()['id']
 except Exception:raise CaptionError('Caption response missing ID; inspect Studio and receipt') from None
 if not isinstance(cid,str) or not cid:raise CaptionError('Invalid caption ID; inspect Studio and receipt')
 record.update({'state':'uploaded','caption_id':cid});save(state,record)
 wait_serving(session,video,cid,sleep);verify(session,channel,video)
 items=english_manual(captions(session,video))
 if len(items)!=1 or items[0].get('id')!=cid:raise CaptionError('English track not uniquely confirmed; inspect Studio')
 record['state']='confirmed';save(state,record)
 return {'result':'uploaded','channel_id':channel,'video_id':video,'caption_id':cid,'status':'serving','srt_sha256':data['sha256']}

def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
 dry=sub.add_parser('prepare');dry.add_argument('--srt',required=True)
 up=sub.add_parser('upload');up.add_argument('--srt',required=True);up.add_argument('--token',required=True);up.add_argument('--channel-id',required=True);up.add_argument('--video-id',required=True);up.add_argument('--upload-receipt',required=True)
 a=p.parse_args()
 try:
  if a.command=='prepare':result=srt_data(a.srt)[0]
  else:
   from google.auth.transport.requests import AuthorizedSession
   from google.oauth2.credentials import Credentials
   cred=Credentials.from_authorized_user_file(a.token,[SCOPE])
   with AuthorizedSession(cred) as session:result=upload(session,a.channel_id,a.video_id,a.srt,a.upload_receipt)
  print(json.dumps(result,ensure_ascii=False,indent=2));return 0
 except Exception as ex:
  print('Error:',str(ex) if isinstance(ex,CaptionError) else type(ex).__name__,file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
