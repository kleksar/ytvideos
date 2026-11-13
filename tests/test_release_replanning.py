"""Delayed private uploads must not strand an approved release; fake provider only."""
from datetime import datetime, timedelta, timezone
import shutil
import unittest
from unittest.mock import patch

import test_lifecycle
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.release import ReleaseSpec
from ytvideos.util import file_digest


@unittest.skipUnless(shutil.which("ffmpeg"), "ffmpeg is required for the synthetic MP4 fixture")
class ReleaseReplanningTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_lifecycle.SyntheticLifecycleTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        f = self.fixture
        self.video = f.produce_to_mp4_review()
        self.spec, self.path = f.bound_spec(self.video)
        f.service.approve(f.approval("mp4"))
        self.uploaded = {"channel_id": self.spec.channel_id, "video_id": test_lifecycle.VIDEO_ID,
                         "privacy": "private", "media_sha256": file_digest(self.video),
                         "processing_status": "succeeded"}

    def upload(self):
        f = self.fixture
        f.finish("upload", self.uploaded, action="upload", values=self.uploaded)

    def replacement(self, **changes):
        data = self.spec.to_dict()
        data.update(publish_at=(datetime.now(timezone.utc) + timedelta(days=4)).isoformat(), **changes)
        return ReleaseSpec.from_dict(data)

    def test_same_binding_can_be_replayed_after_upload_without_restarting_work(self):
        self.upload()
        f = self.fixture
        before = f.store.get(f.run_id)
        result = f.service.prepare_release(f.run_id, self.path)
        after = f.store.get(f.run_id)
        self.assertEqual(result["blockers"], [])
        self.assertEqual(after["publication"], before["publication"])
        self.assertEqual(after["tasks"], before["tasks"])

    def test_community_post_is_deferred_once_until_public_verification(self):
        f = self.fixture
        doc = self.spec.to_dict()
        doc['community_post'] = {'text': 'One new reason to watch the episode.'}
        post_spec = ReleaseSpec.from_dict(doc)
        f.service.prepare_release(f.run_id, f.write(post_spec.to_dict()))
        self.upload()
        f.finish('configure_release', f.readbacks(post_spec, 'pre_schedule'))
        f.finish('schedule', f.readbacks(post_spec, 'scheduled'), action='schedule')
        f.finish('verify_publication', f.readbacks(post_spec, 'scheduled'))
        actions = f.service.deferred_actions(f.run_id)
        self.assertEqual(actions, f.service.deferred_actions(f.run_id))
        post = next(item for item in actions if item['id'] == 'community_post')
        self.assertEqual(post['status'], 'pending')
        self.assertEqual(post['depends_on'], 'verify_public')
        self.assertEqual(post['video_id'], test_lifecycle.VIDEO_ID)
        self.assertEqual(post['expected']['linked_video_id'], test_lifecycle.VIDEO_ID)
        self.assertEqual(post['release_sha256'], post_spec.sha256)

    def test_expired_slot_can_replan_without_upload_or_approval_again(self):
        self.upload()
        f = self.fixture
        old_readbacks = f.readbacks(self.spec, "pre_schedule")
        f.finish("configure_release", old_readbacks)
        before = f.store.get(f.run_id)
        replacement = self.replacement()
        with patch("ytvideos.service.datetime") as clock:
            clock.now.return_value = datetime.now(timezone.utc) + timedelta(days=3)
            with self.assertRaisesRegex(WorkflowError, "future"):
                f.service.claim(f.run_id, "schedule", "too-late-for-old-slot")
            plan = f.service.prepare_release(f.run_id, f.write(replacement.to_dict()))
        self.assertEqual(plan["blockers"], [])
        current = f.store.get(f.run_id)
        self.assertEqual(current["approvals"], before["approvals"])
        self.assertEqual(current["tasks"]["upload"], before["tasks"]["upload"])
        self.assertEqual(current["publication"]["video_id"], test_lifecycle.VIDEO_ID)
        self.assertEqual(current["tasks"]["configure_release"]["status"], "pending")
        new_claim = f.service.claim(f.run_id, "configure_release", "replanned-configurator")
        with self.assertRaises(WorkflowError):
            f.finish("configure_release", old_readbacks, claim=new_claim)
        f.finish("configure_release", f.readbacks(replacement, "pre_schedule"), claim=new_claim)
        f.finish("schedule", f.readbacks(replacement, "scheduled"), action="schedule")
        f.finish("verify_publication", f.readbacks(replacement, "scheduled"))
        self.assertEqual(f.service.next(f.run_id)["status"], "scheduled")
        with f.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM operations WHERE run_id=? AND kind='upload'",
                                        (f.run_id,)).fetchone()[0], 1)
        self.assertEqual(len([e for e in f.store.events(f.run_id) if e["kind"] == "user.approved"]), 2)

    def test_replanning_cannot_change_content_or_metadata(self):
        self.upload()
        f = self.fixture
        data = self.replacement().to_dict()
        data["metadata"]["title"] = "A different publication promise"
        before = f.store.get(f.run_id)
        with self.assertRaises(Conflict):
            f.service.prepare_release(f.run_id, f.write(data))
        self.assertEqual(f.store.get(f.run_id)["publication"], before["publication"])

    def test_replanning_rejects_uncertain_upload_and_uncertain_schedule(self):
        f = self.fixture
        upload_claim = f.service.claim(f.run_id, "upload", "fixture-upload")
        operation = f.begin("upload", upload_claim, "upload")
        with self.assertRaises(Conflict):
            f.service.prepare_release(f.run_id, f.write(self.replacement().to_dict()))
        f.observe(operation, self.uploaded)
        f.finish("upload", self.uploaded, claim=upload_claim)
        f.finish("configure_release", f.readbacks(self.spec, "pre_schedule"))
        schedule_claim = f.service.claim(f.run_id, "schedule", "fixture-schedule")
        f.begin("schedule", schedule_claim, "schedule")
        with self.assertRaises(Conflict):
            f.service.prepare_release(f.run_id, f.write(self.replacement().to_dict()))

    def test_bad_replacement_keeps_existing_binding(self):
        self.upload()
        f = self.fixture
        data = self.spec.to_dict()
        data["publish_at"] = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        before = f.store.get(f.run_id)
        with self.assertRaises((Conflict, WorkflowError)):
            f.service.prepare_release(f.run_id, f.write(data))
        self.assertEqual(f.store.get(f.run_id)["publication"], before["publication"])
