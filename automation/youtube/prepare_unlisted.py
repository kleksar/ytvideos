#!/usr/bin/env python3
"""Safely update one owned video's unlisted status, description, or playlist.

Only explicit subcommands contact YouTube. An exclusive receipt precedes each
write. If a receipt exists or an outcome is uncertain, stop and reconcile.
"""
import argparse
import json
import sys
from pathlib import Path
from schedule import API, SCOPE, read, reserve, mark_done, valid_ids, ScheduleError
from add_to_playlist import read_items

STATUS_KEYS = ('embeddable', 'license', 'publicStatsViewable', 'selfDeclaredMadeForKids', 'containsSyntheticMedia')
SNIPPET_KEYS = ('title', 'categoryId', 'description', 'tags', 'defaultLanguage', 'defaultAudioLanguage')


def state_path(path):
    path = Path(path)
    if path.exists():
        raise ScheduleError('Receipt already exists: read YouTube state and inspect before any retry')
    return path


def existing_parts(obj, keys):
    return {k: obj[k] for k in keys if k in obj}


def verify_fields(actual, expected):
    for k, v in expected.items():
        if k not in actual or actual[k] != v:
            raise ScheduleError('Unconfirmed or changed field: ' + k + '; inspect manually')


def update(session, channel, video, state, mode, film=None):
    valid_ids(channel, video)
    state = state_path(state)
    v = read(session, channel, video)
    etag = v.get('etag')
    if not etag:
        raise ScheduleError('No ETag: cannot safely update')
    status = v.get('status', {})
    if status.get('publishAt'):
        raise ScheduleError('Video already scheduled; inspect manually')
    if status.get('privacyStatus') not in ('private', 'unlisted'):
        raise ScheduleError('Unexpected visibility; inspect before changing it')
    if mode == 'privacy':
        if status.get('privacyStatus') == 'unlisted':
            return {'result': 'already_unlisted', 'video_id': video}
        if v.get('processingDetails', {}).get('processingStatus') != 'succeeded':
            raise ScheduleError('Video processing is not complete')
        for k in ('embeddable', 'license', 'publicStatsViewable'):
            if k not in status:
                raise ScheduleError('Missing status.' + k)
        data = existing_parts(status, STATUS_KEYS)
        # Preserve the current disclosure when changing only visibility. Whether
        # synthetic media needs disclosure is episode-specific, not a property
        # of the privacy transition.
        data['privacyStatus'] = 'unlisted'
        part = 'status'
    else:
        valid_ids(channel, film)
        if film == video:
            raise ScheduleError('The full film must be a different video')
        film_v = read(session, channel, film)
        if film_v.get('status', {}).get('privacyStatus') != 'unlisted':
            raise ScheduleError('The full film is not confirmed unlisted')
        if film_v.get('processingDetails', {}).get('processingStatus') != 'succeeded':
            raise ScheduleError('Full film processing is not complete')
        snippet = v.get('snippet', {})
        if not all(k in snippet for k in ('title', 'categoryId', 'description')):
            raise ScheduleError('Missing snippet fields; cannot preserve metadata')
        url = 'https://www.youtube.com/watch?v=' + film
        if url in snippet['description']:
            return {'result': 'link_already_present', 'video_id': video}
        data = existing_parts(snippet, SNIPPET_KEYS)
        data['description'] = data['description'].rstrip() + '\n\nFull video: ' + url
        if len(data['description']) > 5000:
            raise ScheduleError('Description exceeds YouTube limit')
        part = 'snippet'
    reserve(state, {'state': 'outcome_unknown', 'action': mode, 'channel_id': channel,
                    'video_id': video, 'etag': etag, 'before': v.get(part), 'intended': data})
    fresh = read(session, channel, video)
    if fresh.get('etag') != etag or fresh.get(part) != v.get(part):
        raise ScheduleError('Video changed before update; inspect receipt and state')
    try:
        r = session.put(API + 'videos', params={'part': part}, json={'id': video, part: data},
                        headers={'If-Match': etag}, timeout=60, allow_redirects=False)
    except Exception:
        raise ScheduleError('Update outcome unknown; inspect before retrying') from None
    if r.status_code != 200:
        raise ScheduleError(f'Update HTTP {r.status_code}; inspect before retrying')
    final = read(session, channel, video)
    # Google may omit status.containsSyntheticMedia on reads. Require all other
    # requested fields, but report synthetic disclosure as unconfirmed if absent.
    checked = dict(data)
    if part == 'status' and 'containsSyntheticMedia' not in final.get(part, {}):
        checked.pop('containsSyntheticMedia', None)
    verify_fields(final.get(part, {}), checked)
    result = {'state': 'confirmed', 'action': mode, 'channel_id': channel,
              'video_id': video, 'after': final.get(part),
              'synthetic_media_readback': final.get('status', {}).get('containsSyntheticMedia', 'not_returned')}
    mark_done(state, result)
    return result


def add_playlist(session, channel, video, playlist, state):
    valid_ids(channel, video)
    state = state_path(state)
    v = read(session, channel, video)
    if v.get('status', {}).get('privacyStatus') not in ('private', 'unlisted'):
        raise ScheduleError('Unexpected visibility')
    lists = read_items(session, 'playlists', {'part': 'id,snippet', 'mine': 'true'})
    found = [x for x in lists if x.get('id') == playlist and x.get('snippet', {}).get('channelId') == channel]
    if len(found) != 1:
        raise ScheduleError('Playlist is not uniquely owned by expected channel')
    params = {'part': 'snippet,contentDetails', 'playlistId': playlist}
    def members():
        return [x for x in read_items(session, 'playlistItems', params)
                if x.get('contentDetails', {}).get('videoId') == video]
    items = members()
    if len(items) > 1:
        raise ScheduleError('Playlist already has duplicates; inspect')
    if items:
        return {'result': 'already_present', 'video_id': video, 'playlist_id': playlist}
    reserve(state, {'state': 'outcome_unknown', 'action': 'playlist', 'channel_id': channel,
                    'video_id': video, 'playlist_id': playlist})
    if members():
        raise ScheduleError('Membership changed before write; inspect receipt and playlist')
    body = {'snippet': {'playlistId': playlist,
                        'resourceId': {'kind': 'youtube#video', 'videoId': video}}}
    try:
        r = session.post(API + 'playlistItems', params={'part': 'snippet'}, json=body,
                         timeout=60, allow_redirects=False)
    except Exception:
        raise ScheduleError('Playlist outcome unknown; inspect before retrying') from None
    if r.status_code not in (200, 201):
        raise ScheduleError(f'Playlist update HTTP {r.status_code}; inspect before retrying')
    items = members()
    if len(items) != 1:
        raise ScheduleError('Playlist membership not confirmed; inspect before retrying')
    result = {'state': 'confirmed', 'channel_id': channel, 'video_id': video,
              'playlist_id': playlist, 'playlist_item_id': items[0]['id']}
    mark_done(state, result)
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=('privacy', 'description', 'playlist'))
    p.add_argument('--token', required=True)
    p.add_argument('--channel-id', required=True)
    p.add_argument('--video-id', required=True)
    p.add_argument('--state', required=True)
    p.add_argument('--film-id')
    p.add_argument('--playlist-id')
    a = p.parse_args()
    try:
        if a.action == 'description' and not a.film_id:
            raise ScheduleError('description requires --film-id')
        if a.action == 'playlist' and not a.playlist_id:
            raise ScheduleError('playlist requires --playlist-id')
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(a.token, [SCOPE])
        with AuthorizedSession(creds) as session:
            result = (add_playlist(session, a.channel_id, a.video_id, a.playlist_id, a.state)
                      if a.action == 'playlist' else
                      update(session, a.channel_id, a.video_id, a.state, a.action, a.film_id))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print('Error:', str(exc) if isinstance(exc, (ScheduleError, RuntimeError)) else type(exc).__name__, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
