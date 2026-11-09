#!/usr/bin/env python3
"""Inspect local release packages and reconcile them with a saved YouTube read-back."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from tempfile import NamedTemporaryFile


CHANNEL = Path(__file__).resolve().parents[1]
ROOT = CHANNEL.parents[1]
QUEUE = CHANNEL / 'ReleaseQueue'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def refresh_snapshot(path, token, channel_id, registered_ids):
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2.credentials import Credentials

    def fetch(resource, **params):
        response = session.get('https://www.googleapis.com/youtube/v3/' + resource,
                               params=params, timeout=30, allow_redirects=False)
        if response.status_code != 200:
            raise ValueError(f'YouTube {resource}: HTTP {response.status_code}')
        return response.json()

    with AuthorizedSession(Credentials.from_authorized_user_file(str(token))) as session:
        channels = fetch('channels', part='contentDetails', mine='true')['items']
        if len(channels) != 1 or channels[0]['id'] != channel_id:
            raise ValueError('OAuth channel differs from Scenes on Repeat')
        uploads = channels[0]['contentDetails']['relatedPlaylists']['uploads']
        ids = set(registered_ids)
        page = fetch('playlistItems', part='contentDetails', playlistId=uploads, maxResults=50)
        while True:
            ids.update(item['contentDetails']['videoId'] for item in page['items'])
            if not page.get('nextPageToken'):
                break
            page = fetch('playlistItems', part='contentDetails', playlistId=uploads, maxResults=50,
                         pageToken=page['nextPageToken'])
        ids = sorted(ids)
        videos = []
        for offset in range(0, len(ids), 50):
            items = fetch('videos', part='snippet,status', id=','.join(ids[offset:offset + 50]))['items']
            for video in items:
                if video['snippet']['channelId'] != channel_id:
                    raise ValueError('A registered video belongs to another channel')
                videos.append({'id': video['id'], 'title': video['snippet']['title'],
                               'privacy': video['status']['privacyStatus'],
                               'publish_at': video['status'].get('publishAt')})
    snapshot = {'channel_id': channel_id, 'observed_at': datetime.now(timezone.utc).isoformat(timespec='seconds'),
                'videos': videos, 'unavailable_ids': sorted(set(ids) - {v['id'] for v in videos})}
    with NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as stream:
        json.dump(snapshot, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    Path(stream.name).replace(path)


def file_matches(path, expected):
    path = (ROOT / path).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        return False
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest() == expected


def stage(clip, receipt, remote):
    if not receipt or receipt.get('mp4_sha256') != clip['mp4_sha256']:
        return 'CHECK_RECORD'
    video_id = receipt.get('video_id')
    if video_id:
        video = remote.get(video_id)
        if not video:
            return 'CHECK_YOUTUBE'
        if video['privacy'] == 'public':
            return 'PUBLISHED'
        if video['privacy'] == 'private' and video.get('publish_at'):
            when = datetime.fromisoformat(video['publish_at'].replace('Z', '+00:00'))
            return 'CHECK_SCHEDULE' if when <= datetime.now(when.tzinfo) else 'SCHEDULED'
        return {'private': 'UPLOADED_PRIVATE', 'unlisted': 'UPLOADED_UNLISTED'}.get(
            video['privacy'], 'CHECK_YOUTUBE'
        )
    if receipt.get('upload') not in {'not_started', 'rejected_before_transfer'}:
        return 'CHECK_UPLOAD'
    if any(video['title'] == clip['metadata']['title'] for video in remote.values()):
        return 'POSSIBLE_DUPLICATE'
    return 'LOCAL'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', type=Path, default=QUEUE / 'YOUTUBE.json')
    parser.add_argument('--refresh-token', type=Path, help='Refresh the snapshot using a local OAuth token')
    parser.add_argument('--verify-files', action='store_true', help='Verify the hashes of local MP4 and SRT files')
    args = parser.parse_args()
    channel_id = read(ROOT / 'automation/channels.json')['scenes_on_repeat']['channel_id']
    folders = sorted(path for path in QUEUE.iterdir() if path.is_dir())
    packages = {}
    for folder in folders:
        episode = CHANNEL / 'videos' / folder.name
        package_path = episode / 'RELEASE.json'
        state_path = episode / 'RELEASE_STATE.json'
        if not package_path.is_file() or not state_path.is_file():
            continue
        package, state = read(package_path), read(state_path)
        if package['channel_id'] != channel_id or state['channel_id'] != channel_id:
            parser.error(f'{folder.name} belongs to another channel')
        packages[folder.name] = (package, state['clips'])
    if args.refresh_token:
        registered = set()
        for _, receipts in packages.values():
            registered.update(record['video_id'] for record in receipts.values() if record.get('video_id'))
        try:
            refresh_snapshot(args.snapshot, args.refresh_token, channel_id, registered)
        except Exception as exc:
            if isinstance(exc, ValueError) and str(exc).startswith(('OAuth channel', 'YouTube ', 'A registered')):
                parser.error(str(exc))
            parser.error(f'YouTube refresh failed ({type(exc).__name__}). Check access and token.')
    snapshot = read(args.snapshot)
    if snapshot['channel_id'] != channel_id:
        parser.error('YouTube snapshot belongs to another channel')
    remote = {v['id']: v for v in snapshot['videos']}
    if len(remote) != len(snapshot['videos']):
        parser.error('YouTube snapshot contains duplicate IDs')
    print(f"YouTube snapshot {snapshot['observed_at']} | {len(remote)} videos")
    if snapshot.get('unavailable_ids'):
        print(f"YouTube videos not readable: {len(snapshot['unavailable_ids'])}")

    counts = Counter()
    roles = Counter()
    registered_ids = set()
    hashes = set()
    invalid = False
    for folder in folders:
        if folder.name not in packages:
            print(f'{folder.name} | UNREGISTERED')
            invalid = True
            continue
        package, receipts = packages[folder.name]
        clip_ids = [clip['id'] for clip in package['clips']]
        if len(clip_ids) != len(set(clip_ids)) or set(clip_ids) != set(receipts):
            parser.error(f'{folder.name} has duplicate clip IDs or mismatched release records')
        film_roles = Counter(record.get('release_role', 'unassigned') for record in receipts.values())
        if set(film_roles) - {'lead', 'reserve', 'unassigned'} or film_roles['lead'] > 1:
            parser.error(f'{folder.name} has invalid release roles or more than one lead')
        roles.update(film_roles)
        for clip in package['clips']:
            receipt = receipts[clip['id']]
            current = stage(clip, receipt, remote)
            video_id = receipt.get('video_id')
            media_hash = clip['mp4_sha256']
            if media_hash in hashes or video_id and video_id in registered_ids:
                parser.error(f'Duplicate media or YouTube ID for {folder.name}/{clip["id"]}')
            hashes.add(media_hash)
            if video_id:
                registered_ids.add(video_id)
            notes = []
            if args.verify_files and (current == 'LOCAL' or (ROOT / clip['mp4']).is_file()):
                kinds = ['mp4', 'srt'] if clip.get('srt') else ['mp4']
                verified = all(file_matches(clip[k], clip[k + '_sha256']) for k in kinds)
                notes.append('files verified' if verified else 'FILE CHECK FAILED')
                invalid |= not verified
            if receipt.get('reason'):
                notes.append(receipt['reason'])
            if current != 'PUBLISHED' and receipt.get('publication_rights') != 'cleared':
                notes.append('publication rights unverified')
            video = remote.get(video_id, {})
            if video.get('publish_at'):
                notes.append(video['publish_at'])
            counts[current] += 1
            print(' | '.join([f'{folder.name}/{clip["id"]}', receipt.get('release_role', 'unassigned'),
                              current, video_id or '—', *notes]))
    print('Queue:', ', '.join(f'{key}={count}' for key, count in sorted(counts.items())) or 'empty')
    print('Release roles:', ', '.join(f'{key}={count}' for key, count in sorted(roles.items())) or 'empty')
    print('YouTube videos outside queue:', len(remote.keys() - registered_ids))
    return int(invalid)


if __name__ == '__main__':
    raise SystemExit(main())
