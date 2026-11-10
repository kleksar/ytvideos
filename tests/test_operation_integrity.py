"""Adversarial dispatch/recovery tests; no network calls or generated media."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import os
import threading
import unittest
from unittest.mock import patch
import uuid

import test_workflow as workflow_fixture
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.store import Transaction
from ytvideos.util import file_digest


class OperationIntegrity(unittest.TestCase):
    postgres = False

    def setUp(self):
        self.fixture = workflow_fixture.WorkflowContract()
        self.fixture.postgres = self.postgres
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service

    def audio(self):
        self.fixture.production_ready()
        claim = self.service.claim(self.fixture.run_id, "audio", "audio-worker", lease_seconds=30, estimated_units=2)
        payload = self.service.operation_payload(self.fixture.run_id, "audio", "tts")
        operation = self.service.begin_operation(self.fixture.run_id, "audio", claim["token"], "tts", payload)
        return claim, payload, operation

    def observe(self, operation, status="confirmed", observed=None):
        values = observed or {"provider_job_id": "fixture-job-1", "state": status}
        receipt = self.fixture.output({
            "operation_key": operation["key"], "attempt_id": operation["attempt_id"],
            "task_input_hash": operation["task_input_hash"], "status": status,
            "provider_evidence": {"method": "provider_job_readback", "observation_id": "fixture-observation-1",
                                  "observed": values},
        })
        self.service.observe_operation(self.fixture.run_id, operation["key"], status, receipt, event_id=str(uuid.uuid4()))
        return receipt

    def publication_ready(self, *, assets=True):
        """Start at an accepted media boundary. Media decoding is tested by montage suites."""
        fixture = self.fixture
        script = self.service.artifacts.put(fixture.output(workflow_fixture.SCRIPT), "script")
        media = self.service.artifacts.put(fixture.output("synthetic accepted MP4 identity fixture"), "mp4")
        thumbnail = fixture.output("synthetic thumbnail bytes")
        captions = fixture.output("1\n00:00:00,000 --> 00:00:01,000\nA fixture.\n")
        run = fixture.store.get(fixture.run_id)
        data = {
            "run_id": fixture.run_id, "revision": 1, "channel_id": run["profile"]["youtube_channel_id"],
            "format": "short", "has_speech": True,
            "metadata": {
                "title": "Fixture publication", "description": "Test fixture, never uploaded.", "tags": ["fixture"],
                "category_id": "27", "language": "en", "audio_language": "en", "made_for_kids": False,
                "contains_synthetic_media": True, "license": "youtube", "age_restricted": False, "paid_promotion": False,
            },
            "media_sha256": media["sha256"], "duration_seconds": 30,
            "publish_at": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
            "thumbnail_sha256": file_digest(thumbnail), "caption": {"sha256": file_digest(captions), "language": "en"},
            "playlist_na_reason": "Fixture inventory has no playlist.",
            "related_na_reason": "Fixture inventory has no related video.",
        }
        spec_path = fixture.output(data)
        packaging = self.service.artifacts.put(spec_path, "release_spec")
        review = self.service.artifacts.put(fixture.output({"fixture": "accepted review boundary"}), "review")

        def seed(tx, current):
            for task_id, artifact in (("script", script), ("render", media), ("review", review), ("packaging", packaging)):
                current["artifacts"][artifact["id"]] = artifact
                current["tasks"][task_id].update(status="complete", outputs=[artifact["id"]])

        fixture.store.mutate(fixture.run_id, seed)
        self.service.approve(fixture.signed("script"))
        self.service.approve(fixture.signed("mp4"))
        plan = self.service.prepare_release(fixture.run_id, spec_path, assets=[thumbnail, captions] if assets else [])
        return data, plan

    def upload(self):
        self.publication_ready()
        claim = self.service.claim(self.fixture.run_id, "upload", "uploader", lease_seconds=30)
        payload = self.service.operation_payload(self.fixture.run_id, "upload", "upload")
        operation = self.service.begin_operation(self.fixture.run_id, "upload", claim["token"], "upload", payload)
        return claim, payload, operation

    def test_claim_without_dispatch_expires_safely(self):
        self.fixture.production_ready()
        self.service.claim(self.fixture.run_id, "audio", "worker", lease_seconds=30, estimated_units=2)
        self.fixture.clock += 31
        self.service.resume(self.fixture.run_id)
        run = self.fixture.store.get(self.fixture.run_id)
        self.assertEqual(run["tasks"]["audio"]["status"], "pending")
        self.assertEqual(run["budget"]["reserved"], 0)
        self.service.claim(self.fixture.run_id, "audio", "replacement", estimated_units=2)

    def test_changed_tts_payload_cannot_create_a_second_charge(self):
        claim, payload, operation = self.audio()
        changed = {**payload, "script_sha256": "f" * 64}
        with self.assertRaisesRegex(WorkflowError, "payload differs"):
            self.service.begin_operation(self.fixture.run_id, "audio", claim["token"], "tts", changed)
        with self.fixture.store.transaction() as tx:
            self.assertEqual(tx.operation(operation["key"])["status"], "dispatched")
            self.assertEqual(tx.execute("SELECT count(*) FROM operations").fetchone()[0], 1)

    def test_known_not_sent_cannot_override_recorded_dispatch(self):
        claim, _, _ = self.audio()
        with self.assertRaisesRegex(Conflict, "provider reconciliation"):
            self.service.fail(self.fixture.run_id, "audio", claim["token"], "caller guesses it failed", known_not_sent=True)
        self.assertEqual(self.fixture.store.get(self.fixture.run_id)["budget"]["reserved"], 2)

    def test_reconciled_result_claim_cannot_dispatch_again(self):
        _, payload, operation = self.audio()
        self.observe(operation)
        self.fixture.clock += 31
        self.service.resume(self.fixture.run_id)
        claim = self.service.reconcile_task(self.fixture.run_id, "audio", worker="recovery", outcome="completed",
                                            evidence="Provider returned the previously created job.")
        with self.assertRaisesRegex(Conflict, "never dispatch"):
            self.service.begin_operation(self.fixture.run_id, "audio", claim["token"], "tts", payload)

    def test_provider_evidence_cannot_be_a_truthy_scalar(self):
        _, _, operation = self.audio()
        for value in (True, "verified", {"status": "pass"}):
            receipt = self.fixture.output({"operation_key": operation["key"], "attempt_id": operation["attempt_id"],
                                           "task_input_hash": operation["task_input_hash"], "status": "confirmed",
                                           "provider_evidence": value})
            with self.subTest(value=value), self.assertRaises(WorkflowError):
                self.service.observe_operation(self.fixture.run_id, operation["key"], "confirmed", receipt,
                                                event_id=str(uuid.uuid4()))

    def test_publication_payload_cannot_override_private_visibility_or_metadata(self):
        self.publication_ready()
        claim = self.service.claim(self.fixture.run_id, "upload", "uploader")
        payload = self.service.operation_payload(self.fixture.run_id, "upload", "upload")
        for changed in ({**payload, "privacy": "public"},
                        {**payload, "metadata": {**payload["metadata"], "title": "Unbound changed title"}}):
            with self.subTest(changed=changed), self.assertRaisesRegex(WorkflowError, "payload differs"):
                self.service.begin_operation(self.fixture.run_id, "upload", claim["token"], "upload", changed)

    def test_missing_release_asset_bytes_block_before_upload(self):
        _, plan = self.publication_ready(assets=False)
        self.assertTrue(any("asset bytes" in blocker for blocker in plan["blockers"]))
        with self.assertRaisesRegex(WorkflowError, "asset bytes"):
            self.service.claim(self.fixture.run_id, "upload", "uploader")

    def test_completed_upload_must_match_observed_provider_video(self):
        claim, payload, operation = self.upload()
        observed = {"channel_id": payload["channel_id"], "media_sha256": payload["media_sha256"],
                    "privacy": "private", "video_id": "abc123_XY-z"}
        self.observe(operation, observed=observed)
        path = self.fixture.output({**observed, "video_id": "xyz123_XY-z"})
        receipt = self.fixture.receipt("upload", claim, path)
        with self.assertRaisesRegex(WorkflowError, "differs from the confirmed"):
            self.service.complete(self.fixture.run_id, "upload", claim["token"], path, receipt, actual_units=0)

    def test_not_performed_upload_can_retry_but_stale_observation_is_fenced(self):
        _, payload, original = self.upload()
        stale = self.observe(original, "not_performed")
        self.fixture.clock += 31
        self.service.resume(self.fixture.run_id)
        claim = self.service.claim(self.fixture.run_id, "upload", "replacement")
        retry = self.service.begin_operation(self.fixture.run_id, "upload", claim["token"], "upload", payload)
        self.assertEqual(retry["key"], original["key"])
        self.assertNotEqual(retry["attempt_id"], original["attempt_id"])
        with self.assertRaisesRegex(Conflict, "obsolete operation attempt"):
            self.service.observe_operation(self.fixture.run_id, retry["key"], "not_performed", stale, event_id=str(uuid.uuid4()))
        dispatches = [event for event in self.fixture.store.events(self.fixture.run_id) if event["kind"] == "operation.dispatched"]
        self.assertEqual(len(dispatches), 2)

    def test_same_media_cannot_be_uploaded_again_from_another_run(self):
        _, _, first = self.upload()
        another = self.service.create("paper_detour", "independent request", capabilities=self.fixture.run["capabilities"])
        self.fixture.run_id = another["id"]
        self.publication_ready()
        claim = self.service.claim(another["id"], "upload", "second-uploader")
        payload = self.service.operation_payload(another["id"], "upload", "upload")
        with self.assertRaisesRegex(Conflict, "already dispatched"):
            self.service.begin_operation(another["id"], "upload", claim["token"], "upload", payload)
        with self.fixture.store.transaction() as tx:
            self.assertEqual(tx.operation(first["key"])["run_id"], first["run_id"])

    def test_topic_reservation_has_one_winner_across_run_locks(self):
        if not self.postgres:
            self.skipTest("PostgreSQL-specific different-row transaction race")
        first = self.fixture.run_id
        second = self.service.create("paper_detour", "competing research", capabilities=self.fixture.run["capabilities"])["id"]
        path = self.fixture.output({"selected_topic": {"title": "Same", "angle": "Same", "viewer_value": "Fixture"},
                                    "sources": [{"url": "https://example.com/fixture"}]})
        calls = []
        for run_id in (first, second):
            self.fixture.run_id = run_id
            claim = self.service.claim(run_id, "research", "researcher")
            calls.append((run_id, claim["token"], self.fixture.receipt("research", claim, path)))
        barrier = threading.Barrier(2, timeout=10)
        local = threading.local()
        execute = Transaction.execute

        def synchronized(transaction, statement, params=()):
            cursor = execute(transaction, statement, params)
            if statement.startswith("SELECT run_id FROM topics") and not getattr(local, "passed", False):
                local.passed = True
                barrier.wait()
            return cursor

        def finish(call):
            run_id, token, receipt = call
            try:
                self.service.complete(run_id, "research", token, path, receipt, actual_units=0)
                return "complete"
            except Conflict:
                return "conflict"

        with patch.object(Transaction, "execute", synchronized), ThreadPoolExecutor(max_workers=2) as pool:
            self.assertCountEqual(list(pool.map(finish, calls)), ["complete", "conflict"])


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "set YTV_TEST_POSTGRES_URL for real PostgreSQL contracts")
class PostgreSQLOperationIntegrity(OperationIntegrity):
    postgres = True


if __name__ == "__main__":
    unittest.main()
