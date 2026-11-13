#!/usr/bin/env python3
"""Schedule an owned, never-published private video, or read its schedule.

Network calls occur only via explicit `read` or `set`. `plan` is offline.
An uncertain write leaves a local state receipt and must not be retried blindly.
The caller must supply an upload receipt and attest the video has never been
public; current API privacy status alone does not establish publication history.
"""
import argparse, json, os, re, sys
import importlib.util
from datetime import datetime,timedelta,timezone
from pathlib import Path
from zoneinfo import ZoneInfo
API='https://www.googleapis.com/youtube/v3/'
SCOPE='https://www.googleapis.com/auth/youtube.force-ssl'
WRITABLE=('embeddable','license','publicStatsViewable','selfDeclaredMadeForKids','containsSyntheticMedia')

class ScheduleError(Exception):pass

def utc_time(value):
 try:x=datetime.fromisoformat(value.replace('Z','+00:00'))
 except ValueError:raise ScheduleError('Time must be ISO 8601 with UTC offset') from None
 if x.tzinfo is None or x.utcoffset() is None:raise ScheduleError('Time must include a UTC offset')
 return x.astimezone(timezone.utc)

def local_time(text,tz_name):
 try:
  dt=datetime.fromisoformat(text);zone=ZoneInfo(tz_name)
 except Exception:raise ScheduleError('Invalid local time or time zone') from None
 if dt.tzinfo is not None:raise ScheduleError('Local time must not include an offset')
 a=dt.replace(tzinfo=zone,fold=0);b=dt.replace(tzinfo=zone,fold=1)
 if a.utcoffset()!=b.utcoffset() or a.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None)!=dt:raise ScheduleError('Local time is ambiguous or nonexistent')
 return a

def plan(start,tz_name,days):
 if days<1 or days>31:raise ScheduleError('Days must be between 1 and 31')
 first=local_time(start,tz_name);out=[]
 for i in range(days):
  naive=first.replace(tzinfo=None)+timedelta(days=i);t=local_time(naive.isoformat(),tz_name)
  out.append({'local':t.isoformat(),'utc':t.astimezone(timezone.utc).isoformat().replace('+00:00','Z')})
 return {'timezone':tz_name,'slots':out,'status':'draft_not_scheduled'}

def valid_ids(channel,video):
 if not re.fullmatch(r'UC[A-Za-z0-9_-]{22}',channel or '') or not re.fullmatch(r'[A-Za-z0-9_-]{11}',video or ''):raise ScheduleError('Invalid channel or video ID')

def get_json(session,resource,params):
 try:r=session.get(API+resource,params=params,timeout=30,allow_redirects=False)
 except Exception:raise ScheduleError('Read failed; inspect connection') from None
 if r.status_code!=200:raise ScheduleError(f'{resource} read failed (HTTP {r.status_code})')
 return r.json()

def read(session,channel,video):
 valid_ids(channel,video)
 channels=get_json(session,'channels',{'part':'id','mine':'true'}).get('items',[])
 if len(channels)!=1 or channels[0].get('id')!=channel:raise ScheduleError('Authorized channel does not match')
 items=get_json(session,'videos',{'part':'snippet,status,processingDetails','id':video}).get('items',[])
 if len(items)!=1 or items[0].get('id')!=video or items[0].get('snippet',{}).get('channelId')!=channel:raise ScheduleError('Video not found in expected channel')
 return items[0]

def summary(v):
 return {'video_id':v['id'],'channel_id':v['snippet']['channelId'],'privacy':v.get('status',{}).get('privacyStatus'),'publishAt':v.get('status',{}).get('publishAt'),'processing':v.get('processingDetails',{}).get('processingStatus'),'containsSyntheticMedia':v.get('status',{}).get('containsSyntheticMedia')}

def verify_upload_receipt(path,channel,video):
 try:r=json.loads(Path(path).read_text())
 except Exception:raise ScheduleError('Upload receipt cannot be read') from None
 f=r.get('fingerprint',{});status=f.get('body',{}).get('status',{})
 if r.get('phase')!='complete' or r.get('video_id')!=video or f.get('channel_id')!=channel or status.get('privacyStatus')!='private':raise ScheduleError('Receipt does not prove a private upload to the expected channel')
 return r

def delivery_module():
    path = Path(__file__).resolve().parents[1] / 'ffmpeg_montage/delivery.py'
    spec = importlib.util.spec_from_file_location('ytv_delivery', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_staged_media(upload_receipt, channel, srt, language):
    receipt_path = upload_receipt.get('staging_delivery_receipt')
    if receipt_path is None:
        return
    if not srt or not language:
        raise ScheduleError('Staged release requires its verified SRT and language')
    delivery = delivery_module()
    try:
        identity = upload_receipt['fingerprint']
        receipt = delivery.validate_release(identity['video'], channel, receipt_path)
        if receipt is None or receipt['media']['sha256'] != identity['sha256']:
            raise ValueError('Delivery receipt does not match the uploaded MP4')
        srt_review = receipt['srt_review']
        if receipt.get('schema') == delivery.REUPLOAD_SCHEMA:
            if (srt_review['media_sha256'] != identity['sha256']
                    or srt_review['language'] != language
                    or srt_review['srt'] != delivery.file_record(srt)
                    or srt_review.get('structure') != 'PASS'
                    or srt_review.get('origin') not in ('source_track', 'reconstructed')):
                raise ValueError('Reupload SRT identity or provenance is unverified')
            delivery.check_record(srt_review['evidence'])
            return
        if (srt_review['media_sha256'] != identity['sha256']
                or srt_review['language'] != language
                or srt_review['srt'] != delivery.file_record(srt)
                or any(srt_review.get(key) != 'PASS'
                       for key in ('structure', 'text_coverage', 'timing_mapping'))):
            raise ValueError('SRT has not been verified against this exact MP4')
        delivery.check_record(srt_review['evidence'])
    except (ValueError, KeyError, TypeError, AttributeError, OSError) as error:
        raise ScheduleError(f'Staged release not ready: {error}') from None


def verify_serving_caption(session, channel, video, language, srt, caption_receipt):
    from upload_caption import srt_data

    if language not in ('ru', 'en') or not srt or not caption_receipt:
        raise ScheduleError('A verified manual caption receipt and SRT are required')
    info, _ = srt_data(srt)
    try:
        receipt = json.loads(Path(caption_receipt).read_text())
    except (OSError, ValueError):
        raise ScheduleError('Caption receipt cannot be read') from None
    if (receipt.get('state') != 'confirmed' or receipt.get('channel_id') != channel
            or receipt.get('video_id') != video or receipt.get('srt_sha256') != info['sha256']
            or not receipt.get('caption_id')):
        raise ScheduleError('Caption receipt does not prove this SRT was uploaded for this video')
    tracks = get_json(session, 'captions', {'part': 'snippet', 'videoId': video}).get('items', [])
    matching = [track for track in tracks if track.get('id') == receipt['caption_id']]
    if len(matching) != 1:
        raise ScheduleError('Caption track not uniquely found')
    snippet = matching[0].get('snippet', {})
    if (snippet.get('videoId') != video or snippet.get('language', '').lower().split('-')[0] != language
            or snippet.get('isDraft') is not False or snippet.get('status') != 'serving'
            or snippet.get('trackKind', '').lower() == 'asr'):
        raise ScheduleError('Manual caption language, video, draft or serving status unconfirmed')
    return {'srt_sha256': info['sha256'], 'caption_id': receipt['caption_id']}

def reserve(path,payload):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
 try:fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 except FileExistsError:raise ScheduleError('Schedule receipt exists; inspect status and receipt before retrying') from None
 with os.fdopen(fd,'w') as f:json.dump(payload,f,indent=2);f.flush();os.fsync(f.fileno())

def mark_done(path,payload):
 path=Path(path);tmp=path.with_name(path.name+'.tmp')
 try:fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
 except FileExistsError:raise ScheduleError('Temporary receipt exists; inspect status before retrying') from None
 with os.fdopen(fd,'w') as f:json.dump(payload,f,indent=2);f.flush();os.fsync(f.fileno())
 os.replace(tmp,path)

def set_schedule(session,channel,video,when,upload_receipt,state,never_public,now=None, *,
                 srt=None, language=None, caption_receipt=None):
 valid_ids(channel,video);target=utc_time(when);now=now or datetime.now(timezone.utc)
 if target<=now+timedelta(minutes=5):raise ScheduleError('Time must be at least five minutes in the future')
 if not never_public:raise ScheduleError('Must confirm the video has never been published')
 upload=verify_upload_receipt(upload_receipt,channel,video)
 verify_staged_media(upload,channel,srt,language)
 v=read(session,channel,video);st=v.get('status',{})
 if st.get('privacyStatus')!='private':raise ScheduleError('Video is not private')
 if v.get('processingDetails',{}).get('processingStatus')!='succeeded':raise ScheduleError('Video processing has not succeeded')
 existing=st.get('publishAt')
 if existing:
  if utc_time(existing)!=target:raise ScheduleError('Existing schedule differs; inspect manually')
  return {'result':'already_scheduled','video':summary(v)}
 for field in ('embeddable','license','publicStatsViewable'):
  if field not in st:raise ScheduleError(f'Missing status.{field}; cannot safely preserve settings')
 etag=v.get('etag')
 if not isinstance(etag,str) or not etag:raise ScheduleError('Missing video ETag; cannot guard concurrent changes')
 state=Path(state)
 if state.exists():raise ScheduleError('Schedule receipt exists; inspect server state before retrying')
 if upload.get('staging_delivery_receipt'):
  verify_serving_caption(session,channel,video,language,srt,caption_receipt)
 target_text=target.isoformat().replace('+00:00','Z')
 body_status={k:st[k] for k in WRITABLE if k in st};body_status.update({'privacyStatus':'private','publishAt':target_text})
 reserve(state,{'state':'outcome_unknown','channel_id':channel,'video_id':video,'publishAt':target_text})
 # Repeat status read immediately before writing; do not automatically retry PUT.
 fresh=read(session,channel,video)
 if fresh.get('etag')!=etag or fresh.get('status')!=st:raise ScheduleError('Video changed before scheduling; inspect receipt and state')
 if upload.get('staging_delivery_receipt'):
  verify_serving_caption(session,channel,video,language,srt,caption_receipt)
 if target<=datetime.now(timezone.utc)+timedelta(minutes=5):raise ScheduleError('Schedule is no longer safely in the future')
 try:r=session.put(API+'videos',params={'part':'status'},json={'id':video,'status':body_status},headers={'If-Match':etag},timeout=60,allow_redirects=False)
 except Exception:raise ScheduleError('Scheduling outcome unknown; read video status before any retry') from None
 if r.status_code!=200:raise ScheduleError(f'Schedule update HTTP {r.status_code}; inspect state before retrying')
 final=read(session,channel,video);new=final.get('status',{})
 if new.get('privacyStatus')!='private' or not new.get('publishAt') or utc_time(new['publishAt'])!=target:raise ScheduleError('Schedule not confirmed; inspect before retrying')
 # Preserve any status fields returned by YouTube and supplied to the update.
 if any(k in new and new[k]!=v for k,v in body_status.items() if k not in ('privacyStatus','publishAt')):raise ScheduleError('Other status fields changed; inspect manually')
 mark_done(state,{'state':'confirmed','channel_id':channel,'video_id':video,'publishAt':target_text})
 return {'result':'scheduled','video':summary(final)}

def main():
 p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
 z=sub.add_parser('plan');z.add_argument('--start',required=True);z.add_argument('--timezone',default='America/New_York');z.add_argument('--days',type=int,default=4)
 for name in ('read','set'):
  q=sub.add_parser(name);q.add_argument('--token',required=True);q.add_argument('--channel-id',required=True);q.add_argument('--video-id',required=True)
  if name=='set':
   q.add_argument('--when',required=True);q.add_argument('--upload-receipt',required=True);q.add_argument('--state',required=True);q.add_argument('--never-published',action='store_true')
   q.add_argument('--srt');q.add_argument('--language');q.add_argument('--caption-receipt')
 args=p.parse_args()
 try:
  if args.cmd=='plan':result=plan(args.start,args.timezone,args.days)
  else:
   from google.auth.transport.requests import AuthorizedSession
   from google.oauth2.credentials import Credentials
   creds=Credentials.from_authorized_user_file(args.token,[SCOPE])
   with AuthorizedSession(creds) as sess:
    result=summary(read(sess,args.channel_id,args.video_id)) if args.cmd=='read' else set_schedule(sess,args.channel_id,args.video_id,args.when,args.upload_receipt,args.state,args.never_published,srt=args.srt,language=args.language,caption_receipt=args.caption_receipt)
  print(json.dumps(result,ensure_ascii=False,indent=2));return 0
 except Exception as e:
  print('Error:',str(e) if isinstance(e,ScheduleError) else type(e).__name__,file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
