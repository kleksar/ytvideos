"""Regressions at cancellation, approval replay and packaging/image boundaries."""
import unittest

from test_release import payload
import test_workflow
from ytvideos.errors import Conflict
from ytvideos.workflow import input_hash


class ControlPlaneEdges(unittest.TestCase):
    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.service = self.fixture.service
        self.run_id = self.fixture.run_id

    def test_old_approval_event_cannot_approve_a_revised_identical_file(self):
        fixture = self.fixture
        fixture.script_ready()
        event = fixture.signed()
        self.service.approve(event)
        self.service.revise(self.run_id, "script", "explicit revision")
        fixture.complete("script", test_workflow.SCRIPT)
        with self.assertRaisesRegex(Conflict, "earlier revision"):
            self.service.approve(event)
        self.service.approve(fixture.signed())

    def test_cancelled_external_cost_is_settled_without_requeue(self):
        fixture = self.fixture
        fixture.production_ready()
        claim = self.service.claim(self.run_id, "audio", "fixture-worker", estimated_units=3)
        operation = self.service.begin_operation(self.run_id, "audio", claim["token"], "tts",
                                                  self.service.operation_payload(self.run_id, "audio", "tts"))
        self.service.cancel(self.run_id, "user cancel")
        receipt = fixture.output({"operation_key": operation["key"], "attempt_id": operation["attempt_id"],
                                  "task_input_hash": operation["task_input_hash"], "status": "confirmed",
                                  "provider_evidence": {"method": "provider_job_readback", "observation_id": "fixture-job-result",
                                                        "observed": {"fixture_only": True, "actual_units": 2}}})
        self.service.observe_operation(self.run_id, operation["key"], "confirmed", receipt, event_id="fixture-cancel-result")
        result = self.service.settle_cancelled(self.run_id, "audio", evidence="fixture-cancel-result", actual_units=2)
        self.assertEqual(result["budget"]["reserved"], 0)
        self.assertEqual(result["budget"]["spent"], 2)
        self.assertEqual(self.service.next(self.run_id)["tasks"], [])
        self.service.settle_cancelled(self.run_id, "audio", evidence="same result", actual_units=2)
        self.assertEqual(fixture.store.get(self.run_id)["budget"]["spent"], 2)

    def test_thumbnail_generation_does_not_wait_for_storyboard_or_block_render(self):
        fixture = self.fixture
        fixture.production_ready()
        data = payload()
        data.update(run_id=self.run_id, channel_id=fixture.run["profile"]["youtube_channel_id"], format="short")
        data.pop("end_screen")
        fixture.complete("packaging", data)
        task = self.service.add_thumbnail_task(self.run_id, {"id": "main", "prompt": "An exact fixture thumbnail brief",
                                                            "visual_intent": "The selected story promise"})
        self.assertEqual(task["dependencies"], ["packaging"])
        run = fixture.store.get(self.run_id)
        self.assertIn("thumbnail:main", run["tasks"]["upload"]["dependencies"])
        self.assertNotIn("thumbnail:main", run["tasks"]["render"]["dependencies"])
        canonical = self.service.operation_payload(self.run_id, "thumbnail:main", "image")
        self.assertEqual(canonical["scene"]["purpose"], "thumbnail")
        self.assertIn("brief_sha256", canonical)
        before = input_hash(run, task)
        self.service.add_thumbnail_task(self.run_id, {"id": "main", "prompt": "A revised fixture brief",
                                                    "visual_intent": "The same exact story promise"})
        current = fixture.store.get(self.run_id)
        self.assertNotEqual(before, input_hash(current, current["tasks"]["thumbnail:main"]))

    def test_same_bytes_can_have_distinct_artifact_roles_without_overwriting(self):
        fixture = self.fixture
        path = fixture.output("evidence fixture")
        reference = self.service.attach(self.run_id, path, kind="reference", source="fixture://reference")
        rights = self.service.attach(self.run_id, path, kind="rights", source="fixture://rights")
        self.assertNotEqual(reference["id"], rights["id"])
        self.assertEqual(reference["sha256"], rights["sha256"])
        self.assertEqual(fixture.store.get(self.run_id)["artifacts"][reference["id"]]["kind"], "reference")


if __name__ == "__main__":
    unittest.main()
