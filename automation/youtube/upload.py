#!/usr/bin/env python3
"""Private YouTube uploads. Network actions occur only via explicit CLI commands."""
import argparse
import fcntl
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import random
import re
import sys
import tempfile
import time
from urllib.parse import urlparse

UPLOAD_SCOPE = 'https://www.googleapis.com/auth/youtube.upload'
READ_SCOPE = 'https://www.googleapis.com/auth/youtube.readonly'
SCOPES = [UPLOAD_SCOPE, READ_SCOPE]
INIT_URL = 'https://www.googleapis.com/upload/youtube/v3/videos'
CHANNEL_URL = 'https://www.googleapis.com/youtube/v3/channels'
VIDEO_URL = 'https://www.googleapis.com/youtube/v3/videos'
THUMBNAIL_URL = 'https://www.googleapis.com/upload/youtube/v3/thumbnails/set'
CHUNK = 8 * 1024 * 1024
MAX_THUMBNAIL_BYTES = 50 * 1024 * 1024
RETRYABLE = {500, 502, 503, 504}

class UploadError(Exception):
    pass


def private_write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, name = tempfile.mkstemp(prefix='.upload-', dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(value, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def hash_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate_metadata(meta):
    if not isinstance(meta, dict) or set(meta) - {'title', 'description', 'category_id', 'language', 'audio_language', 'made_for_kids', 'tags', 'contains_synthetic_media'}:
        raise UploadError('Invalid metadata fields.')
    for key in ('title', 'description', 'category_id', 'language'):
        if not isinstance(meta.get(key), str) or not meta[key].strip():
            raise UploadError(f'Metadata must contain nonempty {key}.')
    if len(meta['title']) > 100 or len(meta['description'].encode('utf-8')) > 5000:
        raise UploadError('Title or description exceeds YouTube limits.')
    if not isinstance(meta.get('made_for_kids'), bool):
        raise UploadError('Explicit boolean made_for_kids is required.')
    if 'contains_synthetic_media' in meta and not isinstance(meta['contains_synthetic_media'], bool):
        raise UploadError('contains_synthetic_media must be boolean.')
    if 'audio_language' in meta and (not isinstance(meta['audio_language'], str) or not meta['audio_language'].strip()):
        raise UploadError('audio_language must be a nonempty string.')
    if 'tags' in meta and (not isinstance(meta['tags'], list) or any(not isinstance(t, str) for t in meta['tags'])):
        raise UploadError('tags must be a list of strings.')
    snippet = {'title': meta['title'], 'description': meta['description'],
               'categoryId': meta['category_id'], 'defaultLanguage': meta['language']}
    if 'audio_language' in meta:
        snippet['defaultAudioLanguage'] = meta['audio_language']
    if 'tags' in meta:
        snippet['tags'] = meta['tags']
    status = {'privacyStatus': 'private', 'selfDeclaredMadeForKids': meta['made_for_kids']}
    if 'contains_synthetic_media' in meta:
        status['containsSyntheticMedia'] = meta['contains_synthetic_media']
    return {'snippet': snippet, 'status': status}


def safe_url(url):
    p = urlparse(url)
    return p.scheme == 'https' and p.hostname == 'www.googleapis.com' and p.username is None and p.password is None and p.port in (None, 443) and p.path == '/upload/youtube/v3/videos'


def check_channel(session, expected):
    try:
        r = session.get(CHANNEL_URL, params={'part': 'id,snippet', 'mine': 'true'}, timeout=60, allow_redirects=False)
    except Exception:
        raise UploadError('Cannot verify authorized channel; check credentials and connection.') from None
    if r.status_code != 200:
        raise UploadError(f'Cannot verify authorized channel (HTTP {r.status_code}).')
    channels = r.json().get('items', [])
    if len(channels) != 1 or channels[0].get('id') != expected:
        raise UploadError('Authorized channel does not match expected channel ID; upload stopped.')


def video_status(session, expected_channel, video_id):
    """Read the server's current status for a video owned by the expected channel."""
    if not re.fullmatch(r'UC[A-Za-z0-9_-]{22}', expected_channel or ''):
        raise UploadError('Expected channel must be a YouTube channel ID (UC...).')
    if not re.fullmatch(r'[A-Za-z0-9_-]{11}', video_id or ''):
        raise UploadError('Video ID must be an 11-character YouTube video ID.')
    check_channel(session, expected_channel)
    try:
        r = session.get(VIDEO_URL, params={'part': 'snippet,status,processingDetails', 'id': video_id},
                        timeout=60, allow_redirects=False)
    except Exception:
        raise UploadError('Cannot retrieve video status; check credentials and connection.') from None
    if r.status_code != 200:
        raise UploadError(f'Cannot retrieve video status (HTTP {r.status_code}).')
    payload = r.json()
    items = payload.get('items', []) if isinstance(payload, dict) else []
    if len(items) != 1 or not isinstance(items[0], dict):
        raise UploadError('Video unavailable or not visible to the authorized account.')
    item = items[0]
    if item.get('id') != video_id or item.get('snippet', {}).get('channelId') != expected_channel:
        raise UploadError('Video does not belong to the expected channel.')
    status = item.get('status') or {}
    processing = item.get('processingDetails') or {}
    return {
        'video_id': video_id,
        'channel_id': expected_channel,
        'privacy': status.get('privacyStatus'),
        'upload_status': status.get('uploadStatus'),
        'failure_reason': status.get('failureReason'),
        'rejection_reason': status.get('rejectionReason'),
        'processing_status': processing.get('processingStatus'),
        'processing_failure_reason': processing.get('processingFailureReason'),
    }


def thumbnail_urls(value):
    """Collect thumbnail URLs from API responses without assuming one response shape."""
    urls = set()
    if isinstance(value, dict):
        url = value.get('url')
        if isinstance(url, str) and url.startswith('https://'):
            urls.add(url)
        for child in value.values():
            urls.update(thumbnail_urls(child))
    elif isinstance(value, list):
        for child in value:
            urls.update(thumbnail_urls(child))
    return urls


def read_thumbnail(path):
    path = Path(path)
    if not path.is_file():
        raise UploadError('Thumbnail file does not exist.')
    size = path.stat().st_size
    if size <= 0 or size > MAX_THUMBNAIL_BYTES:
        raise UploadError('Thumbnail must be between 1 byte and 50 MB.')
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if data.startswith(b'\x89PNG\r\n\x1a\n') and suffix == '.png':
        mime = 'image/png'
    elif data.startswith(b'\xff\xd8\xff') and suffix in ('.jpg', '.jpeg'):
        mime = 'image/jpeg'
    else:
        raise UploadError('Thumbnail must be a matching PNG or JPEG file.')
    return data, mime


def set_thumbnail(session, expected_channel, video_id, image_path):
    """Set one custom thumbnail, first proving that the video belongs to the channel."""
    video_status(session, expected_channel, video_id)
    data, mime = read_thumbnail(image_path)
    try:
        r = session.post(THUMBNAIL_URL, params={'videoId': video_id}, data=data,
                         headers={'Content-Type': mime}, timeout=60, allow_redirects=False)
    except Exception:
        raise UploadError('Thumbnail request failed; check the video in Studio before retrying.') from None
    if r.status_code != 200:
        raise UploadError(f'Thumbnail request failed (HTTP {r.status_code}); check Studio before retrying.')
    try:
        payload = r.json()
    except Exception:
        raise UploadError('YouTube accepted a response with an unreadable receipt; check Studio before retrying.') from None
    if not isinstance(payload, dict) or payload.get('kind') != 'youtube#thumbnailSetResponse' or not payload.get('items'):
        raise UploadError('YouTube returned an incomplete thumbnail receipt; check Studio before retrying.')

    set_urls = thumbnail_urls(payload.get('items'))
    try:
        verify = session.get(VIDEO_URL, params={'part': 'snippet', 'id': video_id},
                             timeout=60, allow_redirects=False)
    except Exception:
        verify = None
    verify_items = []
    if verify is not None and verify.status_code == 200:
        body = verify.json()
        verify_items = body.get('items', []) if isinstance(body, dict) else []
    if (len(verify_items) == 1 and isinstance(verify_items[0], dict)
            and verify_items[0].get('id') == video_id
            and verify_items[0].get('snippet', {}).get('channelId') == expected_channel):
        current_urls = thumbnail_urls(verify_items[0].get('snippet', {}).get('thumbnails', {}))
        readback = 'matched' if set_urls and set_urls.intersection(current_urls) else 'not_matched'
    else:
        current_urls = set()
        readback = 'unavailable'
    return {
        'video_id': video_id,
        'channel_id': expected_channel,
        'api_set_accepted': True,
        'readback': readback,
        'response_thumbnail_count': len(set_urls),
        'current_thumbnail_count': len(current_urls),
    }


def resume_offset(r, size):
    if r.status_code in (200, 201):
        data = r.json()
        if not isinstance(data.get('id'), str) or not data['id']:
            raise UploadError('YouTube response has no video ID; retain session and retry status.')
        return None, data['id']
    if r.status_code != 308:
        if r.status_code in (404, 410):
            raise UploadError('Session expired. Check YouTube Studio for a completed upload before clearing state and starting again.')
        raise UploadError(f'Upload failed (HTTP {r.status_code}); state retained.')
    header = r.headers.get('Range')
    if not header:
        return 0, None
    match = re.fullmatch(r'bytes=0-(\d+)', header)
    if not match or int(match.group(1)) >= size:
        raise UploadError('Invalid server Range; state retained.')
    return int(match.group(1)) + 1, None


def upload(session, video, meta, expected_channel, state_path, sleep=time.sleep,
           delivery_receipt=None, *, private_staging=False):
    video = Path(video).resolve(strict=True)
    size = video.stat().st_size
    if not video.is_file() or size == 0:
        raise UploadError('Video must be a nonempty regular file.')
    media_type, _ = mimetypes.guess_type(video.name)
    if media_type not in {'video/mp4', 'video/quicktime'}:
        raise UploadError('Video must be an MP4 or QuickTime MOV file.')
    if not expected_channel or not re.fullmatch(r'UC[A-Za-z0-9_-]{22}', expected_channel):
        raise UploadError('Expected channel must be a YouTube channel ID (UC...).')
    body = validate_metadata(meta)
    # Project readiness is checked locally before channel lookup or mutation.
    import importlib.util
    delivery_path = Path(__file__).resolve().parents[2] / 'automation/ffmpeg_montage/delivery.py'
    spec = importlib.util.spec_from_file_location('ytv_delivery', delivery_path)
    delivery = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(delivery)
    try:
        checked = delivery.validate_release(video, expected_channel, delivery_receipt,
                                            private_staging=private_staging)
    except (ValueError, KeyError, TypeError, IndexError, AttributeError, OSError) as error:
        raise UploadError('Delivery not ready: ' + str(error)) from None
    fingerprint = {'video': str(video), 'sha256': hash_file(video), 'size': size,
                   'channel_id': expected_channel, 'body': body}
    staging_receipt = None
    if private_staging and checked is not None:
        staging_receipt = str(Path(delivery_receipt or (str(video) + '.delivery.json')).resolve())
    state_path = Path(state_path)
    if state_path.resolve() == video:
        raise UploadError('State path must differ from the video file.')
    state_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock_path = state_path.with_name(state_path.name + '.lock')
    lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(lock_fd, 'w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise UploadError('Another process is using this upload state.')
        state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else None
        if state and state.get('fingerprint') != fingerprint:
            raise UploadError('File, metadata or channel differs from saved state; use a different state path.')
        if state and state.get('staging_delivery_receipt') != staging_receipt:
            raise UploadError('Private staging mode or delivery receipt differs from saved state.')
        check_channel(session, expected_channel)
        if state and state.get('phase') == 'complete':
            return state['video_id']
        if state and state.get('phase') == 'initiating':
            raise UploadError('Session creation outcome unknown. Check YouTube Studio before clearing this state; do not retry blindly.')
        if not state:
            state = {'phase': 'initiating', 'fingerprint': fingerprint}
            if staging_receipt:
                state['staging_delivery_receipt'] = staging_receipt
            private_write(state_path, state)
            # No blind retries: a lost response can hide a created session.
            try:
                r = session.post(INIT_URL, params={'uploadType': 'resumable', 'part': 'snippet,status'}, json=body,
                    headers={'X-Upload-Content-Length': str(size), 'X-Upload-Content-Type': media_type},
                    timeout=60, allow_redirects=False)
            except Exception:
                raise UploadError('Session creation outcome unknown; state retained for manual review.') from None
            if r.status_code != 200:
                # YouTube reason codes identify actionable account limits without
                # exposing server bodies, session URLs or credentials.
                reason = None
                try:
                    errors = r.json().get('error', {}).get('errors', [])
                    candidate = errors[0].get('reason') if errors else None
                    if isinstance(candidate, str) and re.fullmatch(r'[A-Za-z0-9_.-]{1,80}', candidate):
                        reason = candidate
                except (ValueError, TypeError, AttributeError, IndexError):
                    pass
                detail = f'; reason={reason}' if reason else ''
                raise UploadError(f'Session creation failed (HTTP {r.status_code}{detail}); state retained for review.')
            url = r.headers.get('Location', '')
            if not safe_url(url):
                raise UploadError('Unexpected session URL; state retained for review.')
            state.update(phase='uploading', session_url=url)
            private_write(state_path, state)
        url = state.get('session_url', '')
        if not safe_url(url):
            raise UploadError('Invalid session URL in state.')
        offset = 0
        need_status = True
        retries = 0
        stalled = 0
        with video.open('rb') as f:
            while True:
                try:
                    if need_status:
                        r = session.put(url, headers={'Content-Length': '0', 'Content-Range': f'bytes */{size}'}, data=b'', timeout=120, allow_redirects=False)
                    else:
                        f.seek(offset)
                        data = f.read(min(CHUNK, size - offset))
                        if not data:
                            raise UploadError('Server reported all bytes but did not complete upload; state retained.')
                        end = offset + len(data) - 1
                        r = session.put(url, data=data, headers={'Content-Type': media_type, 'Content-Length': str(len(data)), 'Content-Range': f'bytes {offset}-{end}/{size}'}, timeout=300, allow_redirects=False)
                except UploadError:
                    raise
                except Exception:
                    r = None
                if r is None or r.status_code in RETRYABLE:
                    retries += 1
                    if retries > 6:
                        raise UploadError('Upload interrupted after retries; state retained for resume.')
                    sleep(min(32, 2 ** (retries - 1)) + random.random())
                    need_status = True
                    continue
                previous_offset = offset
                was_status = need_status
                offset, video_id = resume_offset(r, size)
                if video_id is None and not was_status and offset <= previous_offset:
                    stalled += 1
                    if stalled > 3:
                        raise UploadError('Upload made no progress; state retained for resume.')
                else:
                    stalled = 0
                retries = 0
                if video_id:
                    state.pop('session_url', None)
                    state.update(phase='complete', video_id=video_id)
                    private_write(state_path, state)
                    return video_id
                need_status = False


def upload_result(video_id):
    # The original request specifies private, but later privacy changes are possible.
    # Only the status command checks the server's current value.
    return {'video_id': video_id, 'url': 'https://www.youtube.com/watch?v=' + video_id,
            'requested_privacy': 'private', 'current_privacy': None}


def main():
    p = argparse.ArgumentParser(description='Authorize or upload a private video to a specified YouTube channel.')
    sub = p.add_subparsers(dest='command', required=True)
    a = sub.add_parser('authorize')
    a.add_argument('--client-secrets', required=True)
    a.add_argument('--token', required=True, help='Separate token file per channel; keep outside the project.')
    u = sub.add_parser('upload')
    u.add_argument('--token', required=True)
    u.add_argument('--video', required=True)
    u.add_argument('--metadata', required=True)
    u.add_argument('--channel-id', required=True)
    u.add_argument('--state', required=True, help='Unique persistent state file per video/channel, outside project.')
    u.add_argument('--delivery-receipt', help='Paper/Nuviko readiness record; defaults to VIDEO.delivery.json.')
    u.add_argument('--stage-private', action='store_true', help='Allow pending playback and SRT after technical QA.')
    s = sub.add_parser('status', help='Read actual privacy, upload and processing status without modifying the video.')
    s.add_argument('--token', required=True)
    s.add_argument('--channel-id', required=True)
    s.add_argument('--video-id', required=True)
    t = sub.add_parser('set-thumbnail', help='Set and read back one custom video thumbnail.')
    t.add_argument('--token', required=True)
    t.add_argument('--channel-id', required=True)
    t.add_argument('--video-id', required=True)
    t.add_argument('--image', required=True)
    args = p.parse_args()
    try:
        if args.command == 'authorize':
            from google_auth_oauthlib.flow import InstalledAppFlow
            if Path(args.token).exists():
                raise UploadError('Token file already exists; choose another path or explicitly remove it first.')
            flow = InstalledAppFlow.from_client_secrets_file(args.client_secrets, scopes=SCOPES, autogenerate_code_verifier=True)
            creds = flow.run_local_server(host='127.0.0.1', port=0, access_type='offline', prompt='consent')
            if not creds.refresh_token:
                raise UploadError('Google returned no refresh token; no credentials saved.')
            private_write(args.token, json.loads(creds.to_json()))
            print('Credentials saved. Verify channel ID before upload.')
        else:
            from google.oauth2.credentials import Credentials
            from google.auth.transport.requests import AuthorizedSession
            creds = Credentials.from_authorized_user_file(args.token, SCOPES)
            if args.command == 'upload':
                with open(args.metadata, encoding='utf-8') as f:
                    meta = json.load(f)
                with AuthorizedSession(creds) as session:
                    video_id = upload(session, args.video, meta, args.channel_id, args.state,
                                      delivery_receipt=args.delivery_receipt, private_staging=args.stage_private)
                print(json.dumps(upload_result(video_id)))
            elif args.command == 'status':
                with AuthorizedSession(creds) as session:
                    result = video_status(session, args.channel_id, args.video_id)
                print(json.dumps(result, ensure_ascii=False))
            else:
                with AuthorizedSession(creds) as session:
                    result = set_thumbnail(session, args.channel_id, args.video_id, args.image)
                print(json.dumps(result, ensure_ascii=False))
    except (UploadError, OSError, ValueError, ImportError) as e:
        print(f'Error: {e}', file=sys.stderr)
        return 1
    except Exception as e:
        # Do not print exception payloads: HTTP errors can contain credentials or session URLs.
        print(f'Error: {type(e).__name__}; check setup and connection.', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
