#!/usr/bin/env python3
"""Attach the English SRT and publish one processed private Nuviko History video.

This is a one-off, explicitly requested publication operation. Run only after
verifying that --video-id belongs to the correct approved 004 export.
"""
import argparse
import json
import sys
import time
import uuid
from pathlib import Path

from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials


CHANNEL_ID = 'UCqct_dth0WSCwiDZx1WMfgg'
TOKEN = Path('/Users/diplomat/.local/share/story-youtube/history-manage-token.json')
SRT = Path(__file__).resolve().parent / 'Captions/004_en_v2_captions.srt'
SCOPE = 'https://www.googleapis.com/auth/youtube.force-ssl'
API = 'https://www.googleapis.com/youtube/v3/'
UPLOAD = 'https://www.googleapis.com/upload/youtube/v3/captions'
STATUS_FIELDS = ('embeddable', 'license', 'publicStatsViewable',
                 'selfDeclaredMadeForKids', 'containsSyntheticMedia')


def get_items(session, resource, params):
    response = session.get(API + resource, params=params, timeout=30, allow_redirects=False)
    if response.status_code != 200:
        raise RuntimeError(f'{resource} read failed: HTTP {response.status_code}')
    data = response.json()
    if data.get('nextPageToken'):
        raise RuntimeError(f'{resource} returned more than one page; inspect manually')
    return data.get('items', [])


def verify_channel(session):
    channels = get_items(session, 'channels', {'part': 'id', 'mine': 'true'})
    if len(channels) != 1 or channels[0].get('id') != CHANNEL_ID:
        raise RuntimeError('The authorized channel is not Nuviko History')


def read_video(session, video_id):
    videos = get_items(session, 'videos', {
        'part': 'snippet,status,processingDetails', 'id': video_id})
    if len(videos) != 1 or videos[0].get('snippet', {}).get('channelId') != CHANNEL_ID:
        raise RuntimeError('Video not found or belongs to another channel')
    return videos[0]


def check_video(video):
    status = video.get('status', {})
    if status.get('privacyStatus') != 'private':
        raise RuntimeError('Video is not private; no changes made')
    if status.get('publishAt'):
        raise RuntimeError('Video has a scheduled publication; inspect before changing it')
    if video.get('processingDetails', {}).get('processingStatus') != 'succeeded':
        raise RuntimeError('Video processing is not confirmed as succeeded')


def caption_items(session, video_id):
    return get_items(session, 'captions', {'part': 'snippet', 'videoId': video_id})


def english_manual(items):
    return [x for x in items
            if x.get('snippet', {}).get('language', '').lower().split('-')[0] == 'en'
            and x.get('snippet', {}).get('trackKind', '').lower() != 'asr']


def upload_caption(session, video_id, raw):
    boundary = 'ytcap_' + uuid.uuid4().hex
    metadata = {'snippet': {'videoId': video_id, 'language': 'en',
                            'name': 'English', 'isDraft': False}}
    body = (f'--{boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'.encode()
            + json.dumps(metadata).encode('utf-8')
            + f'\r\n--{boundary}\r\nContent-Type: application/octet-stream\r\n\r\n'.encode()
            + raw + f'\r\n--{boundary}--\r\n'.encode())
    try:
        response = session.post(UPLOAD, params={'part': 'snippet', 'uploadType': 'multipart'},
                                headers={'Content-Type': f'multipart/related; boundary={boundary}'},
                                data=body, timeout=60, allow_redirects=False)
    except Exception:
        raise RuntimeError('Caption upload outcome unknown; check captions.list before retrying') from None
    if response.status_code not in (200, 201):
        raise RuntimeError(f'Caption upload HTTP {response.status_code}; inspect captions.list before retrying')
    try:
        return response.json()['id']
    except (ValueError, KeyError):
        raise RuntimeError('Caption upload response lacks ID; inspect captions.list before retrying') from None


def serving_caption(session, video_id, caption_id):
    for attempt in range(6):
        matches = [x for x in caption_items(session, video_id) if x.get('id') == caption_id]
        if len(matches) == 1:
            snippet = matches[0].get('snippet', {})
            if snippet.get('videoId') != video_id or snippet.get('language', '').lower().split('-')[0] != 'en':
                raise RuntimeError('Caption belongs to a different video or language')
            if snippet.get('isDraft'):
                raise RuntimeError('Existing English caption is a draft; inspect manually')
            if snippet.get('status') == 'serving':
                return
            if snippet.get('status') == 'failed':
                raise RuntimeError('Caption processing failed: ' + str(snippet.get('failureReason', 'unknown')))
        if attempt < 5:
            time.sleep(2)
    raise RuntimeError('Caption not confirmed serving; inspect before continuing')


def publish(session, video_id, video):
    status = video['status']
    writable = {key: status[key] for key in STATUS_FIELDS if key in status}
    writable['privacyStatus'] = 'public'
    try:
        response = session.put(API + 'videos', params={'part': 'status'},
                               json={'id': video_id, 'status': writable},
                               timeout=60, allow_redirects=False)
    except Exception:
        raise RuntimeError('Publication outcome unknown; inspect videos.list before retrying') from None
    if response.status_code != 200:
        raise RuntimeError(f'Publication HTTP {response.status_code}; inspect videos.list before retrying')
    verified = read_video(session, video_id)
    if verified.get('status', {}).get('privacyStatus') != 'public':
        raise RuntimeError('Public visibility not confirmed; inspect videos.list before retrying')
    return verified


def run(session, video_id):
    raw = SRT.read_bytes()
    raw.decode('utf-8-sig')
    if not raw or len(raw) > 100_000_000:
        raise RuntimeError('Invalid or oversized SRT')
    verify_channel(session)
    video = read_video(session, video_id)
    check_video(video)
    existing = english_manual(caption_items(session, video_id))
    if len(existing) > 1:
        raise RuntimeError('Multiple existing English captions; inspect manually')
    if existing:
        caption_id = existing[0]['id']
    else:
        caption_id = upload_caption(session, video_id, raw)
    serving_caption(session, video_id, caption_id)
    # Refresh mutable status immediately before the only visibility update.
    video = read_video(session, video_id)
    check_video(video)
    publish(session, video_id, video)
    print(json.dumps({'video_id': video_id, 'channel_id': CHANNEL_ID,
                      'caption_id': caption_id, 'caption_status': 'serving',
                      'privacy': 'public'}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video-id', required=True)
    args = parser.parse_args()
    try:
        credentials = Credentials.from_authorized_user_file(str(TOKEN), [SCOPE])
        with AuthorizedSession(credentials) as session:
            run(session, args.video_id)
    except Exception as exc:
        # Never print HTTP body, credentials, or token-bearing URLs.
        print('Error:', str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
