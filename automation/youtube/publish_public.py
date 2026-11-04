#!/usr/bin/env python3
"""Publish one verified owned private upload after explicit user request.

Before changing visibility, require the original private upload receipt, exact
SRT and confirmed manual caption receipt, channel ownership, finished video
processing, and exactly one membership in the expected owned playlist. A
per-operation receipt is reserved before PUT. A timeout or ambiguous result
requires manual reconciliation; never blindly repeat the write.
"""
import argparse, json, sys
from pathlib import Path
from add_to_playlist import read_items
from schedule import API, SCOPE, WRITABLE, ScheduleError, valid_ids, read, reserve, mark_done, verify_upload_receipt
from upload_caption import srt_data


def verify_assets(session, channel, video, playlist, language, srt, caption_receipt):
    info, _ = srt_data(srt)
    try:
        receipt = json.loads(Path(caption_receipt).read_text())
    except Exception:
        raise ScheduleError('Caption receipt cannot be read') from None
    if (receipt.get('state') != 'confirmed' or receipt.get('channel_id') != channel
            or receipt.get('video_id') != video or receipt.get('srt_sha256') != info['sha256']
            or not receipt.get('caption_id')):
        raise ScheduleError('Caption receipt does not prove this SRT was uploaded for this video')
    captions = read_items(session, 'captions', {'part':'snippet', 'videoId':video})
    matching = [x for x in captions if x.get('id') == receipt['caption_id']]
    if len(matching) != 1:
        raise ScheduleError('Caption track not uniquely found')
    snippet = matching[0].get('snippet', {})
    if (snippet.get('videoId') != video or snippet.get('language','').lower().split('-')[0] != language
            or snippet.get('isDraft') is not False or snippet.get('status') != 'serving'):
        raise ScheduleError('Caption language, video, draft or serving status unconfirmed')
    lists = read_items(session,'playlists',{'part':'id,snippet','mine':'true'})
    owned = [x for x in lists if x.get('id') == playlist and x.get('snippet',{}).get('channelId') == channel]
    if len(owned) != 1:
        raise ScheduleError('Playlist not uniquely owned by expected channel')
    entries = read_items(session,'playlistItems',{'part':'snippet,contentDetails','playlistId':playlist})
    matching = [x for x in entries if x.get('contentDetails',{}).get('videoId') == video]
    if len(matching) != 1:
        raise ScheduleError('Video is not uniquely in expected playlist')
    return {'srt_sha256':info['sha256'], 'caption_id':receipt['caption_id'],
            'playlist_id':playlist, 'playlist_item_id':matching[0].get('id')}


def publish(session, channel, video, playlist, language, srt, upload_receipt, caption_receipt, state):
    valid_ids(channel,video)
    if language not in ('ru','en') or not playlist:
        raise ScheduleError('Invalid language or playlist')
    verify_upload_receipt(upload_receipt,channel,video)
    state=Path(state)
    if state.exists():
        raise ScheduleError('Publication receipt exists; inspect YouTube state before any retry')
    v=read(session,channel,video); status=v.get('status',{})
    if status.get('privacyStatus')!='private' or status.get('publishAt'):
        raise ScheduleError('Video is not an unscheduled private upload')
    if v.get('processingDetails',{}).get('processingStatus')!='succeeded':
        raise ScheduleError('Video processing has not succeeded')
    for field in ('embeddable','license','publicStatsViewable'):
        if field not in status: raise ScheduleError('Missing status.'+field)
    etag=v.get('etag')
    if not isinstance(etag,str) or not etag: raise ScheduleError('Missing video ETag')
    evidence=verify_assets(session,channel,video,playlist,language,srt,caption_receipt)
    original=json.loads(Path(upload_receipt).read_text())
    disclosed=original.get('fingerprint',{}).get('body',{}).get('status',{}).get('containsSyntheticMedia')
    intended={k:status[k] for k in WRITABLE if k in status}
    if disclosed is True:
        if intended.get('containsSyntheticMedia', True) is not True:
            raise ScheduleError('Synthetic media disclosure differs from original upload')
        intended['containsSyntheticMedia']=True
    intended['privacyStatus']='public'
    reserve(state,{'state':'outcome_unknown','action':'publish_public','channel_id':channel,
                   'video_id':video,'etag':etag,'before':status,'intended':intended,'evidence':evidence})
    fresh=read(session,channel,video)
    if fresh.get('etag')!=etag or fresh.get('status')!=status or fresh.get('processingDetails',{}).get('processingStatus')!='succeeded':
        raise ScheduleError('Video changed before publication; inspect receipt and state')
    # Re-read accompanying tracks and membership immediately before publishing.
    if verify_assets(session,channel,video,playlist,language,srt,caption_receipt)!=evidence:
        raise ScheduleError('Caption or playlist changed before publication; inspect receipt')
    try:
        response=session.put(API+'videos',params={'part':'status'},json={'id':video,'status':intended},
                             headers={'If-Match':etag},timeout=60,allow_redirects=False)
    except Exception:
        raise ScheduleError('Publication outcome unknown; inspect YouTube before retrying') from None
    if response.status_code!=200:
        raise ScheduleError(f'Publication HTTP {response.status_code}; inspect state before retrying')
    final=read(session,channel,video); after=final.get('status',{})
    if after.get('privacyStatus')!='public' or final.get('processingDetails',{}).get('processingStatus')!='succeeded':
        raise ScheduleError('Public status or processing not confirmed; inspect before retrying')
    for key,value in intended.items():
        if key=='containsSyntheticMedia' and key not in after: continue
        if key not in after or after[key]!=value:
            raise ScheduleError('Status field not confirmed: '+key)
    verify_assets(session,channel,video,playlist,language,srt,caption_receipt)
    result={'state':'confirmed','action':'publish_public','channel_id':channel,'video_id':video,
            'privacy':'public','processing':'succeeded','evidence':evidence,
            'synthetic_media_readback':after.get('containsSyntheticMedia','not_returned')}
    mark_done(state,result)
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for arg in ('token','channel-id','video-id','playlist-id','language','srt','upload-receipt','caption-receipt','state'):
        p.add_argument('--'+arg,required=True)
    p.add_argument('--confirm-public',action='store_true',help='User explicitly requested public release')
    a=p.parse_args()
    try:
        if not a.confirm_public: raise ScheduleError('Explicit public request must be confirmed')
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2.credentials import Credentials
        creds=Credentials.from_authorized_user_file(a.token,[SCOPE])
        with AuthorizedSession(creds) as session:
            result=publish(session,a.channel_id,a.video_id,a.playlist_id,a.language,a.srt,a.upload_receipt,a.caption_receipt,a.state)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except Exception as exc:
        print('Error:',str(exc) if isinstance(exc,(ScheduleError,RuntimeError)) else type(exc).__name__,file=sys.stderr);return 1

if __name__=='__main__':sys.exit(main())
