import unittest
from unittest.mock import patch

from add_to_playlist import run

CHANNEL = 'UC' + 'x' * 22
PLAYLIST = 'playlist'
VIDEO = 'abc123_XY-z'


class Response:
    def __init__(self, data, status=200):
        self.status_code = status
        self.data = data

    def json(self):
        return self.data


class Session:
    def __init__(self, channel=CHANNEL, video_channel=CHANNEL, privacy='private', reads=None):
        self.channel = channel
        self.video_channel = video_channel
        self.privacy = privacy
        self.reads = list(reads or [[]])
        self.posts = []
        self.video_params = None

    def get(self, url, params, **kwargs):
        resource = url.rsplit('/', 1)[-1]
        if resource == 'channels':
            items = [{'id': self.channel}]
        elif resource == 'videos':
            self.video_params = params
            items = [{'id': VIDEO, 'snippet': {'channelId': self.video_channel},
                      'status': {'privacyStatus': self.privacy}}]
        elif resource == 'playlists':
            items = [{'id': PLAYLIST, 'snippet': {'title': 'Stories', 'channelId': self.channel},
                      'status': {'privacyStatus': 'public'}}]
        elif resource == 'playlistItems':
            items = self.reads.pop(0) if len(self.reads) > 1 else self.reads[0]
        else:
            raise AssertionError(resource)
        return Response({'items': items})

    def post(self, url, **kwargs):
        self.posts.append((url, kwargs))
        return Response({}, 200)


ITEM = {'id': 'item', 'contentDetails': {'videoId': VIDEO}}


class TestPlaylist(unittest.TestCase):
    def test_guard_rejects_wrong_channel_or_video_owner_or_privacy(self):
        for kwargs in ({'channel': 'wrong'}, {'video_channel': 'wrong'}, {'privacy': 'public'}):
            with self.subTest(kwargs=kwargs):
                session = Session(**kwargs)
                with self.assertRaises(RuntimeError):
                    run(session, CHANNEL, PLAYLIST, VIDEO)
                self.assertEqual(session.posts, [])

    def test_public_playlist_membership_with_explicit_privacy(self):
        session = Session(privacy='public', reads=[[ITEM]])
        result = run(session, CHANNEL, PLAYLIST, VIDEO, expected_privacy='public')
        self.assertEqual(result['privacy'], 'public')
        self.assertEqual(result['playlist_privacy'], 'public')
        self.assertEqual(session.posts, [])
        with self.assertRaises(RuntimeError):
            run(Session(privacy='private'), CHANNEL, PLAYLIST, VIDEO, expected_privacy='public')

    def test_existing_item_is_not_posted(self):
        session = Session(reads=[[ITEM]])
        result = run(session, CHANNEL, PLAYLIST, VIDEO)
        self.assertEqual(result['playlist_item_id'], 'item')
        self.assertEqual(session.posts, [])
        self.assertNotIn('maxResults', session.video_params)

    def test_delayed_visibility_reads_again_without_second_post(self):
        session = Session(reads=[[], [], [ITEM]])
        with patch('add_to_playlist.time.sleep') as sleep:
            result = run(session, CHANNEL, PLAYLIST, VIDEO)
        self.assertEqual(result['playlist_item_id'], 'item')
        self.assertEqual(len(session.posts), 1)
        self.assertEqual(session.posts[0][1]['json']['snippet']['resourceId']['videoId'], VIDEO)
        sleep.assert_called_once_with(2)

    def test_visibility_never_confirmed_does_not_repeat_post(self):
        session = Session(reads=[[]])
        with patch('add_to_playlist.time.sleep'):
            with self.assertRaises(RuntimeError):
                run(session, CHANNEL, PLAYLIST, VIDEO)
        self.assertEqual(len(session.posts), 1)

    def test_server_error_reports_unknown_outcome_without_retry(self):
        class ServerError(Session):
            def post(self, url, **kwargs):
                self.posts.append((url, kwargs))
                return Response({}, 503)
        session = ServerError()
        with self.assertRaisesRegex(RuntimeError, 'Исход добавления неизвестен'):
            run(session, CHANNEL, PLAYLIST, VIDEO)
        self.assertEqual(len(session.posts), 1)


if __name__ == '__main__':
    unittest.main()
