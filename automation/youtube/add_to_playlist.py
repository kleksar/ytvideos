#!/usr/bin/env python3
"""Add one owned video to an owned playlist; check exact privacy before and after."""
import argparse
import json
import sys
import time

API = 'https://www.googleapis.com/youtube/v3/'
SCOPE = 'https://www.googleapis.com/auth/youtube.force-ssl'


def read_items(session, resource, params):
    result = []
    params = dict(params)
    # videos.list with an id filter does not support maxResults.
    if resource != 'videos':
        params['maxResults'] = 50
    while True:
        r = session.get(API + resource, params=params, timeout=30, allow_redirects=False)
        if r.status_code != 200:
            raise RuntimeError(f'{resource} read failed (HTTP {r.status_code})')
        page = r.json()
        result.extend(page.get('items', []))
        if not page.get('nextPageToken'):
            return result
        params['pageToken'] = page['nextPageToken']


def run(session, channel_id, playlist_id, video_id, *, expected_privacy='private'):
    if expected_privacy not in ('private', 'public', 'unlisted'):
        raise RuntimeError('Недопустимое ожидаемое состояние доступа')
    channels = read_items(session, 'channels', {'part': 'id', 'mine': 'true'})
    if len(channels) != 1 or channels[0].get('id') != channel_id:
        raise RuntimeError('Авторизован не тот канал; изменений не сделано')
    videos = read_items(session, 'videos', {'part': 'snippet,status', 'id': video_id})
    if len(videos) != 1 or videos[0]['snippet']['channelId'] != channel_id:
        raise RuntimeError('Ролик не найден в указанном канале; изменений не сделано')
    if videos[0].get('status', {}).get('privacyStatus') != expected_privacy:
        raise RuntimeError('Ролик имеет неожиданный уровень доступа; изменений не сделано')
    playlists = read_items(session, 'playlists', {'part': 'id,snippet,status', 'mine': 'true'})
    matching = [p for p in playlists if p.get('id') == playlist_id]
    if len(matching) != 1 or matching[0].get('snippet', {}).get('channelId') != channel_id:
        raise RuntimeError('Плейлист не принадлежит указанному каналу; изменений не сделано')
    params = {'part': 'snippet,contentDetails', 'playlistId': playlist_id}
    def matching_items():
        return [x for x in read_items(session, 'playlistItems', params)
                if x.get('contentDetails', {}).get('videoId') == video_id]
    items = matching_items()
    if not items:
        body = {'snippet': {'playlistId': playlist_id,
                            'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}}
        try:
            r = session.post(API + 'playlistItems', params={'part': 'snippet'}, json=body,
                             timeout=60, allow_redirects=False)
        except Exception:
            raise RuntimeError('Исход добавления неизвестен; проверьте плейлист перед повтором') from None
        if r.status_code not in (200, 201):
            if r.status_code == 429 or r.status_code >= 500:
                raise RuntimeError(f'Исход добавления неизвестен (HTTP {r.status_code}); проверьте плейлист перед повтором')
            raise RuntimeError(f'YouTube отклонил добавление (HTTP {r.status_code})')
        # The insertion may be visible in playlistItems only after a short delay.
        # Poll reads only; never repeat POST because a missing read is inconclusive.
        for attempt in range(5):
            items = matching_items()
            if items:
                break
            if attempt < 4:
                time.sleep(2)
    if len(items) != 1:
        raise RuntimeError('Не удалось однозначно подтвердить добавление; проверьте плейлист перед повтором')
    return {'video_id': video_id, 'channel_id': channel_id, 'privacy': expected_privacy,
            'playlist_id': playlist_id, 'playlist_title': matching[0]['snippet']['title'],
            'playlist_privacy': matching[0].get('status', {}).get('privacyStatus'),
            'playlist_item_id': items[0]['id']}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--token', required=True)
    p.add_argument('--channel-id', required=True)
    p.add_argument('--playlist-id', required=True)
    p.add_argument('--video-id', required=True)
    p.add_argument('--expected-privacy', choices=('private', 'public', 'unlisted'), default='private',
                   help='Exact visibility; private default preserves guarded pre-release behavior')
    a = p.parse_args()
    try:
        from google.auth.transport.requests import AuthorizedSession
        from google.oauth2.credentials import Credentials
        credentials = Credentials.from_authorized_user_file(a.token, [SCOPE])
        with AuthorizedSession(credentials) as session:
            print(json.dumps(run(session, a.channel_id, a.playlist_id, a.video_id,
                                 expected_privacy=a.expected_privacy), ensure_ascii=False))
        return 0
    except Exception as exc:
        # Do not expose token data or HTTP request contents in error output.
        print('Ошибка:', str(exc) if isinstance(exc, RuntimeError) else type(exc).__name__, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
