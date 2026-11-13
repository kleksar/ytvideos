import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('delivery_reupload_test', ROOT / 'automation/ffmpeg_montage/delivery.py')
delivery = importlib.util.module_from_spec(spec)
spec.loader.exec_module(delivery)
sys.path.insert(0, str(ROOT / 'automation/youtube'))
import schedule
CHANNEL = 'UCMVfdfaNxV3ZkI3_J3Eejzw'

class OwnedReuploadTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.p = Path(self.tmp.name)
        self.video = self.p / 'copy.mp4'; self.video.write_bytes(b'video copy')
        self.snapshot = self.p / 'snapshot.json'
        self.snapshot.write_text(json.dumps({'items': [{'id': 'Bfgcq4rxQT8', 'snippet': {'channelId': CHANNEL}, 'status': {'privacyStatus': 'public'}}]}))
        self.evidence = self.p / 'evidence.txt'; self.evidence.write_text('synthetic test evidence')
        self.receipt = self.p / 'receipt.json'
        self.data = {'schema': delivery.REUPLOAD_SCHEMA, 'channel_id': CHANNEL, 'media': delivery.file_record(self.video),
                     'source': {'video_id': 'Bfgcq4rxQT8', 'api_snapshot': delivery.file_record(self.snapshot), 'download_evidence': delivery.file_record(self.evidence)},
                     'technical_review': {'full_decode': 'PASS', 'media_sha256': delivery.sha256(self.video), 'evidence': delivery.file_record(self.evidence)}}
        self.save()
    def tearDown(self): self.tmp.cleanup()
    def save(self): self.receipt.write_text(json.dumps(self.data))
    def test_published_copy_passes_without_production_render(self):
        for stage in (False, True):
            delivery.validate_release(self.video, CHANNEL, self.receipt, private_staging=stage)
    def test_stale_copy_wrong_channel_or_failed_decode_rejected(self):
        self.video.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'does not match'): delivery.validate_release(self.video, CHANNEL, self.receipt)
        self.video.write_bytes(b'video copy')
        with self.assertRaisesRegex(ValueError, 'does not match'): delivery.validate_release(self.video, 'UC0000000000000000000000', self.receipt)
        self.data['technical_review']['full_decode'] = 'FAIL'; self.save()
        with self.assertRaisesRegex(ValueError, 'full decode'): delivery.validate_release(self.video, CHANNEL, self.receipt)
    def test_source_must_be_owned_public_and_snapshot_unchanged(self):
        self.snapshot.write_text(json.dumps({'items': [{'id': 'Bfgcq4rxQT8', 'snippet': {'channelId': 'UC0000000000000000000000'}, 'status': {'privacyStatus': 'public'}}]}))
        with self.assertRaisesRegex(ValueError, 'Stale'): delivery.validate_release(self.video, CHANNEL, self.receipt)
        self.data['source']['api_snapshot'] = delivery.file_record(self.snapshot); self.save()
        with self.assertRaisesRegex(ValueError, 'public source'): delivery.validate_release(self.video, CHANNEL, self.receipt)
    def test_schedule_requires_bound_caption(self):
        caption = self.p / 'captions.srt'; caption.write_text('test caption')
        self.data['srt_review'] = {'media_sha256': delivery.sha256(self.video), 'language': 'en',
                                   'srt': delivery.file_record(caption), 'structure': 'PASS',
                                   'origin': 'reconstructed', 'evidence': delivery.file_record(self.evidence)}
        self.save()
        upload = {'staging_delivery_receipt': str(self.receipt), 'fingerprint': {'video': str(self.video), 'sha256': delivery.sha256(self.video)}}
        schedule.verify_staged_media(upload, CHANNEL, str(caption), 'en')
        caption.write_text('changed')
        with self.assertRaisesRegex(schedule.ScheduleError, 'SRT identity'):
            schedule.verify_staged_media(upload, CHANNEL, str(caption), 'en')

if __name__ == '__main__': unittest.main()
