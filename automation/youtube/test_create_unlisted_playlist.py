import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import create_unlisted_playlist as module

CHANNEL = 'UCqct_dth0WSCwiDZx1WMfgg'

class Response:
    status_code = 200
    def json(self):
        return {'id': 'playlist_id'}

class Session:
    def __init__(self, timeout=False):
        self.posts = 0
        self.timeout = timeout
    def post(self, *args, **kwargs):
        self.posts += 1
        if self.timeout:
            raise TimeoutError()
        return Response()

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.state = Path(self.tmp.name) / 'receipt.json'
    def test_success_records_confirmed_state(self):
        s = Session()
        playlist = {'id': 'playlist_id', 'snippet': {'channelId': CHANNEL, 'title': 'Marseille Plague 1720'}, 'status': {'privacyStatus': 'unlisted'}}
        with patch.object(module, 'read_items', side_effect=[[{'id': CHANNEL}], [], [], [playlist]]):
            result = module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(s.posts, 1)
        self.assertEqual(result['playlist_id'], 'playlist_id')
        self.assertEqual(json.loads(self.state.read_text())['state'], 'confirmed')
    def test_timeout_reserves_receipt_and_blocks_retry(self):
        s = Session(timeout=True)
        with patch.object(module, 'read_items', side_effect=[[{'id': CHANNEL}], [], []]):
            with self.assertRaises(module.ScheduleError):
                module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(json.loads(self.state.read_text())['state'], 'outcome_unknown')
        with self.assertRaises(module.ScheduleError):
            module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(s.posts, 1)
    def test_delayed_visibility_retries_reads_without_second_post(self):
        s = Session()
        playlist = {'id': 'playlist_id', 'snippet': {'channelId': CHANNEL, 'title': 'Marseille Plague 1720'}, 'status': {'privacyStatus': 'unlisted'}}
        with patch.object(module, 'read_items', side_effect=[[{'id': CHANNEL}], [], [], [], [], [playlist]]) as reads, patch.object(module.time, 'sleep') as sleep:
            result = module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(result['state'], 'confirmed')
        self.assertEqual(s.posts, 1)
        self.assertEqual(reads.call_count, 6)
        self.assertEqual(sleep.call_count, 2)
    def test_never_visible_preserves_unknown_receipt_and_blocks_retry(self):
        s = Session()
        with patch.object(module, 'read_items', side_effect=[[{'id': CHANNEL}], [], [], [], [], [], [], []]), patch.object(module.time, 'sleep') as sleep:
            with self.assertRaises(module.ScheduleError):
                module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(s.posts, 1)
        self.assertEqual(sleep.call_count, 4)
        receipt = json.loads(self.state.read_text())
        self.assertEqual(receipt['state'], 'outcome_unknown')
        self.assertEqual(receipt['playlist_id'], 'playlist_id')
        with self.assertRaises(module.ScheduleError):
            module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(s.posts, 1)
    def test_unexpected_visibility_is_not_retried_or_confirmed(self):
        s = Session()
        playlist = {'id': 'playlist_id', 'snippet': {'channelId': CHANNEL, 'title': 'Marseille Plague 1720'}, 'status': {'privacyStatus': 'public'}}
        with patch.object(module, 'read_items', side_effect=[[{'id': CHANNEL}], [], [], [playlist]]), patch.object(module.time, 'sleep') as sleep:
            with self.assertRaises(module.ScheduleError):
                module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(s.posts, 1)
        sleep.assert_not_called()
        self.assertEqual(json.loads(self.state.read_text())['state'], 'outcome_unknown')
    def test_duplicate_stops_without_write(self):
        s = Session()
        with patch.object(module, 'read_items', side_effect=[[{'id': CHANNEL}], [{'snippet': {'title': 'marseille plague 1720'}}]]):
            with self.assertRaises(module.ScheduleError):
                module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(s.posts, 0)
        self.assertFalse(self.state.exists())
    def test_channel_mismatch_stops_without_write(self):
        s = Session()
        with patch.object(module, 'read_items', return_value=[{'id': 'wrong'}]):
            with self.assertRaises(module.ScheduleError):
                module.create(s, CHANNEL, 'Marseille Plague 1720', self.state)
        self.assertEqual(s.posts, 0)
        self.assertFalse(self.state.exists())

if __name__ == '__main__':
    unittest.main()
