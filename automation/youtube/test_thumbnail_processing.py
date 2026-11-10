import unittest
from unittest.mock import patch

import upload


CHANNEL = 'UC' + 'x' * 22
VIDEO = 'abc123_XY-z'


class ThumbnailProcessingTests(unittest.TestCase):
    def test_processing_must_succeed_before_thumbnail_write(self):
        for processing in ('processing', 'failed', 'terminated', None):
            with self.subTest(processing=processing), patch.object(upload, 'video_status', return_value={'processing_status': processing}), patch.object(upload, 'read_thumbnail') as read:
                session = unittest.mock.Mock()
                with self.assertRaises(upload.UploadError):
                    upload.set_thumbnail(session, CHANNEL, VIDEO, 'thumbnail.png')
                read.assert_not_called()
                session.post.assert_not_called()

    def test_completed_processing_preserves_response_and_readback_checks(self):
        class Response:
            status_code = 200
            def __init__(self, value):
                self.value = value
            def json(self):
                return self.value
        url = 'https://i.ytimg.com/vi/abc123_XY-z/default.jpg'
        session = unittest.mock.Mock()
        session.post.return_value = Response({'kind': 'youtube#thumbnailSetResponse', 'items': [{'url': url}]})
        session.get.return_value = Response({'items': [{'id': VIDEO, 'snippet': {'channelId': CHANNEL, 'thumbnails': {'default': {'url': url}}}}]})
        with patch.object(upload, 'video_status', return_value={'processing_status': 'succeeded'}), patch.object(upload, 'read_thumbnail', return_value=(b'png-data', 'image/png')):
            result = upload.set_thumbnail(session, CHANNEL, VIDEO, 'thumbnail.png')
        self.assertTrue(result['api_set_accepted'])
        self.assertEqual(result['readback'], 'matched')
        session.post.assert_called_once()


if __name__ == '__main__':
    unittest.main()
