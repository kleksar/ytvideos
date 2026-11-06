import json
import tempfile
import unittest
from pathlib import Path

from upload import upload, upload_result, UploadError, private_write, video_status, VIDEO_URL

CHANNEL = 'UC' + 'x' * 22
OTHER = 'UC' + 'y' * 22
URL = 'https://www.googleapis.com/upload/youtube/v3/videos?upload_id=secret'
META = {'title': 'Story', 'description': 'Description', 'category_id': '22', 'language': 'ru', 'made_for_kids': False}

class Response:
    def __init__(self, status, body=None, headers=None):
        self.status_code = status
        self.body = body or {}
        self.headers = headers or {}
    def json(self):
        return self.body

class Session:
    def __init__(self, channel=CHANNEL, puts=()):
        self.channel = channel
        self.puts = list(puts)
        self.calls = []
    def get(self, url, **kwargs):
        self.calls.append(('GET', url, kwargs))
        return Response(200, {'items': [{'id': self.channel}]})
    def post(self, url, **kwargs):
        self.calls.append(('POST', url, kwargs))
        return Response(200, headers={'Location': URL})
    def put(self, url, **kwargs):
        self.calls.append(('PUT', url, kwargs))
        result = self.puts.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

class TestUpload(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.video = self.base / 'video.mp4'
        self.video.write_bytes(b'0123456789')
        self.state = self.base / 'state.json'
    def tearDown(self):
        self.tmp.cleanup()
    def run_upload(self, session):
        return upload(session, self.video, META, CHANNEL, self.state, sleep=lambda _: None)
    def test_private_and_idempotent(self):
        s = Session(puts=[Response(308), Response(201, {'id': 'abc'})])
        self.assertEqual(self.run_upload(s), 'abc')
        post = next(c for c in s.calls if c[0] == 'POST')
        self.assertEqual(post[2]['json']['status']['privacyStatus'], 'private')
        repeat = Session()
        self.assertEqual(self.run_upload(repeat), 'abc')
        self.assertEqual([c[0] for c in repeat.calls], ['GET'])
        self.assertNotIn('session_url', json.loads(self.state.read_text()))
        self.assertEqual(self.state.stat().st_mode & 0o777, 0o600)
    def test_completed_state_checks_current_channel_before_returning(self):
        self.run_upload(Session(puts=[Response(308), Response(201, {'id': 'abc'})]))
        before = self.state.read_bytes()
        wrong = Session(channel=OTHER)
        with self.assertRaises(UploadError): self.run_upload(wrong)
        self.assertEqual([c[0] for c in wrong.calls], ['GET'])
        self.assertEqual(self.state.read_bytes(), before)
    def test_result_does_not_claim_current_privacy(self):
        result = upload_result('abc')
        self.assertEqual(result['requested_privacy'], 'private')
        self.assertIsNone(result['current_privacy'])
        self.assertNotIn('privacy', result)
    def test_wrong_channel_before_creation(self):
        s = Session(channel=OTHER)
        with self.assertRaises(UploadError): self.run_upload(s)
        self.assertFalse(self.state.exists())
        self.assertEqual([c[0] for c in s.calls], ['GET'])
    def test_audio_and_metadata_languages_are_independent(self):
        s = Session(puts=[Response(308), Response(201, {'id': 'abc'})])
        upload(s, self.video, {**META, 'audio_language': 'en'}, CHANNEL, self.state)
        snippet = next(c for c in s.calls if c[0] == 'POST')[2]['json']['snippet']
        self.assertEqual(snippet['defaultLanguage'], 'ru')
        self.assertEqual(snippet['defaultAudioLanguage'], 'en')
    def test_empty_audio_language_is_rejected(self):
        s = Session()
        with self.assertRaises(UploadError):
            upload(s, self.video, {**META, 'audio_language': ' '}, CHANNEL, self.state)
        self.assertEqual(s.calls, [])
    def test_resume_uses_server_position_after_failure(self):
        s = Session(puts=[Response(308), OSError(), Response(308, headers={'Range': 'bytes=0-3'}), Response(201, {'id': 'abc'})])
        self.assertEqual(self.run_upload(s), 'abc')
        puts = [c for c in s.calls if c[0] == 'PUT']
        self.assertEqual(puts[-1][2]['headers']['Content-Range'], 'bytes 4-9/10')
        self.assertEqual(puts[-1][2]['data'], b'456789')
    def test_interrupted_restart_queries_status(self):
        s = Session(puts=[Response(308)] + [OSError()] * 7)
        with self.assertRaises(UploadError): self.run_upload(s)
        s = Session(puts=[Response(201, {'id': 'done'})])
        self.assertEqual(self.run_upload(s), 'done')
        self.assertEqual([c[0] for c in s.calls], ['GET', 'PUT'])
    def test_changed_file_rejected(self):
        s = Session(puts=[Response(308)] + [OSError()] * 7)
        with self.assertRaises(UploadError): self.run_upload(s)
        self.video.write_bytes(b'changed')
        with self.assertRaises(UploadError): self.run_upload(Session())
    def test_lost_creation_response_blocks_retry(self):
        class Failed(Session):
            def post(self, *a, **k): raise OSError()
        with self.assertRaises(UploadError): self.run_upload(Failed())
        s = Session()
        with self.assertRaises(UploadError): self.run_upload(s)
        self.assertEqual([c[0] for c in s.calls], ['GET'])
    def test_unexpected_session_host_blocked(self):
        class Failed(Session):
            def post(self, *a, **k): return Response(200, headers={'Location': 'https://evil.example/upload'})
        with self.assertRaises(UploadError): self.run_upload(Failed())
    def test_no_progress_is_bounded(self):
        s = Session(puts=[Response(308)] * 5)
        with self.assertRaises(UploadError): self.run_upload(s)
    def test_no_silent_overwrite_of_changed_metadata(self):
        s = Session(puts=[Response(308), Response(201, {'id': 'abc'})])
        self.run_upload(s)
        with self.assertRaises(UploadError):
            upload(Session(), self.video, {**META, 'title': 'Other'}, CHANNEL, self.state)

class TestVideoStatus(unittest.TestCase):
    VIDEO_ID = 'abc123_XY-z'

    class StatusSession(Session):
        def __init__(self, item, channel=CHANNEL, http_status=200):
            super().__init__(channel=channel)
            self.item = item
            self.http_status = http_status
        def get(self, url, **kwargs):
            if url != VIDEO_URL:
                return super().get(url, **kwargs)
            self.calls.append(('GET', url, kwargs))
            return Response(self.http_status, {'items': [] if self.item is None else [self.item]})

    def item(self, channel=CHANNEL):
        return {'id': self.VIDEO_ID, 'snippet': {'channelId': channel},
                'status': {'privacyStatus': 'private', 'uploadStatus': 'processed'},
                'processingDetails': {'processingStatus': 'succeeded'}}

    def test_reads_privacy_and_processing_after_channel_verification(self):
        s = self.StatusSession(self.item())
        result = video_status(s, CHANNEL, self.VIDEO_ID)
        self.assertEqual(result['privacy'], 'private')
        self.assertEqual(result['processing_status'], 'succeeded')
        self.assertEqual([c[0] for c in s.calls], ['GET', 'GET'])
        self.assertEqual(s.calls[1][2]['params']['id'], self.VIDEO_ID)

    def test_wrong_authorized_channel_never_reads_video(self):
        s = self.StatusSession(self.item(), channel=OTHER)
        with self.assertRaises(UploadError): video_status(s, CHANNEL, self.VIDEO_ID)
        self.assertEqual(len(s.calls), 1)

    def test_other_channel_video_and_missing_video_rejected(self):
        for item in (self.item(OTHER), None):
            with self.subTest(item=item):
                with self.assertRaises(UploadError):
                    video_status(self.StatusSession(item), CHANNEL, self.VIDEO_ID)

    def test_invalid_video_id_rejected_before_network(self):
        s = self.StatusSession(self.item())
        with self.assertRaises(UploadError): video_status(s, CHANNEL, 'bad id')
        self.assertEqual(s.calls, [])

if __name__ == '__main__': unittest.main()
