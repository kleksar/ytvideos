#!/usr/bin/env python3
"""Upload an owned private video's single manual RU or EN SRT track safely.

Before POST reserve one exclusive receipt for channel/video/language. If a
previous write has an unknown outcome, stop and reconcile on YouTube; never
retry blindly. This program only writes on an explicit `upload` command.
"""
import argparse,json,sys,time,uuid
from pathlib import Path
from upload_caption import (API, UPLOAD, SCOPE, STATE, CaptionError, valid_ids,
                            srt_data, get_items, verify, verify_upload_receipt,
                            reserve, save)


def manual_tracks(session,video,language):
    tracks=get_items(session,'captions',{'part':'snippet','videoId':video})
    return [x for x in tracks if x.get('snippet',{}).get('language','').lower().split('-')[0]==language
            and x.get('snippet',{}).get('trackKind','').lower()!='asr']


def wait_serving(session,video,language,caption_id,sleep=time.sleep):
    for attempt in range(6):
        matches=[x for x in manual_tracks(session,video,language) if x.get('id')==caption_id]
        if len(matches)==1:
            data=matches[0].get('snippet',{})
            if data.get('videoId')!=video or data.get('isDraft') is not False:
                raise CaptionError('Caption identity or draft state differs')
            if data.get('status')=='serving': return
            if data.get('status')=='failed': raise CaptionError('Caption processing failed; inspect Studio')
        if attempt<5: sleep(2)
    raise CaptionError('Caption not confirmed serving; inspect before retry')


def upload(session,channel,video,language,srt,upload_receipt,state_dir=STATE,sleep=time.sleep):
    valid_ids(channel,video)
    if language not in ('ru','en'):raise CaptionError('Language must be ru or en')
    data,raw=srt_data(srt)
    verify_upload_receipt(upload_receipt,channel,video)
    verify(session,channel,video)
    items=manual_tracks(session,video,language)
    state=Path(state_dir)/(channel+'_'+video+'_'+language+'.json')
    if len(items)>1:raise CaptionError('Multiple manual tracks of this language; inspect before proceeding')
    if state.exists():
        try:record=json.loads(state.read_text())
        except Exception:raise CaptionError('Caption receipt unreadable') from None
        if (record.get('channel_id')!=channel or record.get('video_id')!=video
                or record.get('srt_sha256')!=data['sha256'] or record.get('language')!=language):
            raise CaptionError('Existing receipt does not match video, language and SRT')
        if record.get('state') not in ('uploaded','confirmed') or not record.get('caption_id'):
            raise CaptionError('Previous upload outcome unknown; inspect before retry')
        if len(items)!=1 or items[0].get('id')!=record['caption_id']:
            raise CaptionError('Receipt track not uniquely visible; inspect before retry')
        wait_serving(session,video,language,record['caption_id'],sleep);verify(session,channel,video)
        if record['state']!='confirmed': record['state']='confirmed';save(state,record)
        return {'result':'existing_confirmed','channel_id':channel,'video_id':video,
                'caption_id':record['caption_id'],'status':'serving','srt_sha256':data['sha256'],'receipt':str(state)}
    if items:raise CaptionError('An existing manual track is not tied to a verified receipt')
    record={'state':'outcome_unknown','channel_id':channel,'video_id':video,'language':language,
            'srt_path':data['path'],'srt_sha256':data['sha256']}
    reserve(state,record)
    verify(session,channel,video)
    if manual_tracks(session,video,language):raise CaptionError('A track appeared before upload; inspect receipt')
    boundary='ytcap_'+uuid.uuid4().hex
    metadata={'snippet':{'videoId':video,'language':language,'name':{'ru':'Русский','en':'English'}[language],'isDraft':False}}
    body=(f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()+json.dumps(metadata,ensure_ascii=False).encode()+f'\r\n--{boundary}\r\nContent-Type: application/octet-stream\r\n\r\n'.encode()+raw+f'\r\n--{boundary}--\r\n'.encode())
    try:
        response=session.post(UPLOAD,params={'part':'snippet','uploadType':'multipart'},
                              headers={'Content-Type':f'multipart/related; boundary={boundary}'},data=body,
                              timeout=60,allow_redirects=False)
    except Exception:raise CaptionError('Caption upload outcome unknown; inspect before retry') from None
    if response.status_code not in (200,201):raise CaptionError(f'Caption upload HTTP {response.status_code}; inspect before retry')
    try:caption_id=response.json()['id']
    except Exception:raise CaptionError('Caption response missing ID; inspect before retry') from None
    if not isinstance(caption_id,str) or not caption_id:raise CaptionError('Invalid caption ID')
    record.update({'state':'uploaded','caption_id':caption_id});save(state,record)
    wait_serving(session,video,language,caption_id,sleep);verify(session,channel,video)
    items=manual_tracks(session,video,language)
    if len(items)!=1 or items[0].get('id')!=caption_id:raise CaptionError('Manual track not uniquely confirmed')
    record['state']='confirmed';save(state,record)
    return {'result':'uploaded','channel_id':channel,'video_id':video,'caption_id':caption_id,
            'status':'serving','srt_sha256':data['sha256'],'receipt':str(state)}


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    dry=sub.add_parser('prepare');dry.add_argument('--srt',required=True)
    up=sub.add_parser('upload')
    for arg in ('srt','token','channel-id','video-id','language','upload-receipt'):up.add_argument('--'+arg,required=True)
    args=p.parse_args()
    try:
        if args.command=='prepare':result=srt_data(args.srt)[0]
        else:
            from google.auth.transport.requests import AuthorizedSession
            from google.oauth2.credentials import Credentials
            credentials=Credentials.from_authorized_user_file(args.token,[SCOPE])
            with AuthorizedSession(credentials) as session:
                result=upload(session,args.channel_id,args.video_id,args.language,args.srt,args.upload_receipt)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except Exception as ex:
        print('Error:',str(ex) if isinstance(ex,CaptionError) else type(ex).__name__,file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
