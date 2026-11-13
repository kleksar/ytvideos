"""Cost and partial-operation recovery; all external observations are synthetic."""
from datetime import datetime, timedelta, timezone
import unittest
import uuid

import test_operation_integrity as operation_fixtures
from test_release import payload
from ytvideos.cli import dispatch, parser
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.release import ReleasePolicy, requirement_matrix
from ytvideos.util import file_digest


class RecoveryEdges(unittest.TestCase):
    def setUp(self):
        self.fixture = operation_fixtures.OperationIntegrity()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.state = self.fixture.fixture
        self.service = self.fixture.service
        self.run_id = self.state.run_id

    def configuration(self):
        claim, _, upload = self.fixture.upload()
        observed = {key: upload["payload"][key] for key in ("channel_id", "media_sha256", "privacy")}
        observed["video_id"] = "abc123_XY-z"
        self.fixture.observe(upload, observed=observed)
        output = self.state.output(observed)
        self.service.complete(self.run_id, "upload", claim["token"], output,
                              self.state.receipt("upload", claim, output), actual_units=0)
        return self.service.claim(self.run_id, "configure_release", "synthetic-configurer",
                                  lease_seconds=30, estimated_units=2)

    def begin(self, claim, action):
        return self.service.begin_operation(self.run_id, "configure_release", claim["token"], action,
            self.service.operation_payload(self.run_id, "configure_release", action))

    def continue_configuration(self):
        return dispatch(self.service, parser().parse_args([
            "reconcile-task", "--run", self.run_id, "--task", "configure_release", "--worker", "synthetic-recovery",
            "--outcome", "continue", "--evidence", "Synthetic terminal operation observations, never live release evidence"]))

    def finish_configuration(self, claim):
        run = self.service.store.get(self.run_id)
        spec = self.service._release_spec(run)
        receipts, files = [], []
        for requirement in requirement_matrix(spec, ReleasePolicy.from_dict(run["profile"]["release_policy"])):
            if not requirement.applicable or requirement.phase != "pre_schedule":
                continue
            evidence = self.state.output({"fixture_only": True, "saved": {requirement.key: requirement.expected}})
            files.append(str(evidence))
            receipts.append({"key": requirement.key, "channel_id": spec.channel_id, "video_id": "abc123_XY-z",
                "release_sha256": spec.sha256, "method": "studio_readback" if requirement.provider == "studio" else "api_readback",
                "observation_id": "synthetic-readback-" + uuid.uuid4().hex, "evidence_sha256": file_digest(evidence),
                "observed_at": (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat(),
                "observed_value": requirement.expected})
        output = self.state.output({"receipts": receipts, "evidence_files": files})
        return self.service.complete(self.run_id, "configure_release", claim["token"], output,
                                     self.state.receipt("configure_release", claim, output), actual_units=0)

    def test_mixed_configuration_recovers_only_missing_or_proven_not_performed_actions(self):
        claim = self.configuration()
        metadata = self.begin(claim, "metadata")
        self.fixture.observe(metadata)
        thumbnail = self.begin(claim, "thumbnail")
        self.fixture.observe(thumbnail, "unknown")
        before = self.service.store.get(self.run_id)
        with self.service.store.transaction() as tx:
            accepted_metadata = tx.operation(metadata["key"])
        self.state.clock += 31
        self.service.resume(self.run_id)
        with self.assertRaisesRegex(Conflict, "all associated"):
            self.continue_configuration()
        old_receipt = self.fixture.observe(thumbnail, "not_performed")
        recovered = self.continue_configuration()
        after = self.service.store.get(self.run_id)
        self.assertEqual(before["budget"], after["budget"])
        self.assertEqual(claim["input_hash"], recovered["input_hash"])
        self.assertFalse(recovered["reconciled_existing_result"])
        with self.assertRaisesRegex(Conflict, "stale or missing"):
            self.begin(claim, "thumbnail")
        with self.assertRaisesRegex(Conflict, "associated operation"):
            self.begin(recovered, "metadata")
        retry = self.begin(recovered, "thumbnail")
        self.assertEqual(retry["key"], thumbnail["key"])
        self.assertNotEqual(retry["attempt_id"], thumbnail["attempt_id"])
        with self.assertRaisesRegex(Conflict, "obsolete operation attempt"):
            self.service.observe_operation(self.run_id, retry["key"], "not_performed", old_receipt,
                                           event_id="late-synthetic-observation-" + uuid.uuid4().hex)
        self.fixture.observe(retry)
        with self.assertRaisesRegex(Conflict, "associated operation"):
            self.begin(recovered, "thumbnail")
        # Captions were never dispatched; the current recovered lease may send them.
        captions = self.begin(recovered, "captions")
        self.assertEqual(captions["claim_token"], recovered["token"])
        with self.service.store.transaction() as tx:
            self.assertEqual(tx.operation(metadata["key"]), accepted_metadata)
        self.assertEqual(self.service.store.get(self.run_id)["budget"], before["budget"])
        self.assertEqual(self.service.store.get(self.run_id)["tasks"]["configure_release"]["attempt"], 2)
        self.fixture.observe(captions)
        self.assertEqual(self.finish_configuration(recovered)["status"], "complete")
        self.assertEqual(self.service.store.get(self.run_id)["budget"]["reserved"], 0)

    def test_active_configuration_retries_proven_non_dispatch_without_repeating_successes(self):
        claim = self.configuration()
        metadata = self.begin(claim, "metadata")
        self.fixture.observe(metadata)
        thumbnail = self.begin(claim, "thumbnail")
        self.fixture.observe(thumbnail, "not_performed")
        retry = self.begin(claim, "thumbnail")
        self.assertNotEqual(retry["attempt_id"], thumbnail["attempt_id"])
        with self.assertRaisesRegex(Conflict, "associated operation"):
            self.begin(claim, "thumbnail")
        self.assertEqual(self.service.store.get(self.run_id)["tasks"]["configure_release"]["attempt"], 2)
        self.fixture.observe(retry, "not_performed")
        last = self.begin(claim, "thumbnail")
        self.fixture.observe(last, "not_performed")
        before = self.service.store.get(self.run_id)
        self.assertEqual(before["tasks"]["configure_release"]["attempt"], before["budget"]["max_task_attempts"])
        with self.assertRaisesRegex(WorkflowError, "retry budget exhausted"):
            self.begin(claim, "thumbnail")
        self.assertEqual(self.service.store.get(self.run_id), before)
        with self.assertRaisesRegex(Conflict, "associated operation"):
            self.begin(claim, "metadata")

    def test_partial_configuration_with_only_confirmed_actions_can_finish_undispatched_work(self):
        claim = self.configuration()
        metadata = self.begin(claim, "metadata")
        self.fixture.observe(metadata)
        self.state.clock += 31
        self.service.resume(self.run_id)
        recovered = self.continue_configuration()
        self.assertEqual(self.begin(recovered, "thumbnail")["claim_token"], recovered["token"])

    def test_continue_does_not_reopen_provider_generation(self):
        _, _, operation = self.fixture.audio()
        self.fixture.observe(operation)
        self.state.clock += 31
        self.service.resume(self.run_id)
        with self.assertRaisesRegex(WorkflowError, "only.*configure_release"):
            self.service.reconcile_task(self.run_id, "audio", worker="recovery", outcome="continue",
                                        evidence="Synthetic confirmed provider operation")
        recovered = self.service.reconcile_task(self.run_id, "audio", worker="recovery", outcome="completed",
                                               evidence="Synthetic confirmed provider operation")
        with self.assertRaisesRegex(Conflict, "never dispatch"):
            self.service.begin_operation(self.run_id, "audio", recovered["token"], "tts",
                                         self.service.operation_payload(self.run_id, "audio", "tts"))

    def test_actual_overage_preserves_free_work_and_still_blocks_new_metered_cost(self):
        self.state.production_ready()
        claim = self.service.claim(self.run_id, "storyboard", "synthetic-editor", estimated_units=2)
        output = self.state.output({"scenes": [{"id": "one", "prompt": "Synthetic scene",
                                               "visual_intent": "Exercise accounting independently of provider execution"}]})
        self.service.complete(self.run_id, "storyboard", claim["token"], output,
                              self.state.receipt("storyboard", claim, output), actual_units=11)
        claim = self.service.claim(self.run_id, "packaging", "synthetic-free-editor", estimated_units=0)
        spec = payload()
        spec.update(run_id=self.run_id, channel_id=self.state.run["profile"]["youtube_channel_id"], format="short")
        spec.pop("end_screen")
        output = self.state.output(spec)
        self.service.complete(self.run_id, "packaging", claim["token"], output,
                              self.state.receipt("packaging", claim, output), actual_units=0)
        self.assertEqual(self.service.store.get(self.run_id)["budget"]["spent"], 11)
        self.service.capabilities(self.run_id, {"audio.produce": {"available": True, "billing": "metered"}},
                                  evidence="Synthetic billing observation for accounting contract only")
        with self.assertRaisesRegex(WorkflowError, "reserve the observed provider cost"):
            self.service.claim(self.run_id, "audio", "metered-worker", estimated_units=0)
        with self.assertRaisesRegex(WorkflowError, "paid budget exhausted"):
            self.service.claim(self.run_id, "audio", "metered-worker", estimated_units=1)


if __name__ == "__main__":
    unittest.main()
