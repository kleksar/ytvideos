"""Local owner decisions: exact targets, replay safety and optional signed-only hosts.

Messages/media below are software fixtures, not production user approvals or QA.
"""
import contextlib
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
import unittest
from unittest.mock import patch

import test_workflow
from ytvideos.cli import main
from ytvideos.doctor import inspect
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.service import Production
from ytvideos.store import Store


class LocalApprovalTests(unittest.TestCase):
    postgres = False

    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.postgres = self.postgres
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.signed_service = self.fixture.service
        self.service = self.restarted()
        self.fixture.service = self.service
        self.run_id = self.fixture.run_id
        self.fixture.script_ready()

    def restarted(self):
        return Production(Store(self.fixture.db), self.fixture.directory / "workspace", self.fixture.service.project,
                          clock=lambda: self.fixture.clock)

    def decision(self, **changes):
        run = self.fixture.store.get(self.run_id)
        gate = self.service.next(self.run_id)["approval_requests"][0]
        return {"revision": run["revision"], "sha256": gate["artifact"]["sha256"],
                "source": "fixture://conversation/user-turn-2", "message": "утвержда.", **changes}

    def approve(self, **changes):
        return self.service.approve_local(self.run_id, "script", **self.decision(**changes))

    def approved_events(self):
        return [event for event in self.fixture.store.events(self.run_id) if event["kind"] == "user.approved"]

    def test_owner_reply_without_key_or_hooks_opens_production_on_same_run(self):
        before = self.fixture.store.get(self.run_id)
        approved = self.approve()
        after = self.fixture.store.get(self.run_id)
        self.assertEqual(approved["authority"], "local_session")
        self.assertEqual(approved["message"], "утвержда.")
        self.assertEqual(approved["sha256"], before["artifacts"][approved["artifact_id"]]["sha256"])
        self.assertEqual(after["id"], before["id"])
        self.assertEqual(after["artifacts"], before["artifacts"])
        self.assertEqual(after["budget"], before["budget"])
        self.assertEqual(after["status"], "working")
        self.assertEqual({task["id"] for task in self.service.next(self.run_id)["tasks"]},
                         {"storyboard", "audio", "packaging"})
        self.assertEqual(len(self.approved_events()), 1)
        with self.fixture.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM operations").fetchone()[0], 0)

    def test_retry_and_restart_preserve_one_event_and_original_timestamp(self):
        decision = self.decision()
        first = self.service.approve_local(self.run_id, "script", **decision)
        second = self.restarted().approve_local(self.run_id, "script", **decision)
        self.assertEqual(first, second)
        self.assertEqual(len(self.approved_events()), 1)

    def test_concurrent_same_reply_is_idempotent_across_connections(self):
        decision = self.decision()
        def deliver(_):
            return self.restarted().approve_local(self.run_id, "script", **decision)
        with ThreadPoolExecutor(max_workers=2) as pool:
            first, second = pool.map(deliver, range(2))
        self.assertEqual(first, second)
        self.assertEqual(len(self.approved_events()), 1)

    def test_old_reply_cannot_be_retargeted_to_identical_bytes_in_a_new_revision(self):
        decision = self.decision()
        self.service.approve_local(self.run_id, "script", **decision)
        self.service.revise(self.run_id, "script", "fixture: revise even with the same final bytes")
        self.fixture.complete("script", test_workflow.SCRIPT)
        with self.assertRaisesRegex(Conflict, "revision"):
            self.service.approve_local(self.run_id, "script", **decision)
        with self.assertRaisesRegex(Conflict, "event ID"):
            self.approve()  # Same source but with the new revision is still the old decision.
        self.assertEqual(self.fixture.store.get(self.run_id)["approvals"], {})
        self.approve(source="fixture://conversation/user-turn-4")
        self.assertEqual(len(self.approved_events()), 2)

    def test_wrong_hash_revision_and_missing_evidence_leave_state_unchanged(self):
        before = self.fixture.store.get(self.run_id)
        for change in ({"sha256": "0" * 64}, {"sha256": "not-a-hash"}, {"revision": 999},
                       {"revision": 0}, {"revision": True}, {"source": " "}, {"message": ""}):
            with self.subTest(change=change), self.assertRaises(WorkflowError):
                self.approve(**change)
            self.assertEqual(self.fixture.store.get(self.run_id), before)
        self.assertEqual(self.approved_events(), [])

    def test_changed_message_under_same_source_is_not_a_new_decision(self):
        decision = self.decision()
        self.service.approve_local(self.run_id, "script", **decision)
        with self.assertRaisesRegex(Conflict, "event ID"):
            self.service.approve_local(self.run_id, "script", **{**decision, "message": "Different fixture message"})
        self.assertEqual(len(self.approved_events()), 1)

    def test_same_source_cannot_approve_a_different_run_with_the_same_script(self):
        decision = self.decision()
        self.service.approve_local(self.run_id, "script", **decision)
        other = self.service.create("paper_detour", "another software fixture")
        self.fixture.run_id = other["id"]
        self.service.capabilities(other["id"], self.fixture.run["capabilities"], evidence="synthetic fixture")
        self.fixture.complete("research", {"selected_topic": {"title": "Another fixture", "angle": "Another angle",
            "viewer_value": "Software test only"}, "sources": [{"url": "https://example.com/other-fixture"}]})
        self.fixture.complete("script", test_workflow.SCRIPT)
        with self.assertRaisesRegex(Conflict, "event ID"):
            self.service.approve_local(other["id"], "script", **decision)
        self.assertEqual(self.fixture.store.get(other["id"])["approvals"], {})

    def test_cancelled_run_and_changed_code_pin_still_refuse_approval(self):
        decision = self.decision()
        with patch("ytvideos.service.code_identity", return_value="unrelated-code"), self.assertRaisesRegex(Conflict, "pin"):
            self.service.approve_local(self.run_id, "script", **decision)
        self.service.cancel(self.run_id, "fixture: stop")
        with self.assertRaisesRegex(Conflict, "cancelled"):
            self.service.approve_local(self.run_id, "script", **decision)
        self.assertEqual(self.approved_events(), [])

    def test_corrupt_artifact_and_incomplete_script_do_not_pass(self):
        decision = self.decision()
        self.service.revise(self.run_id, "script", "fixture: not ready")
        with self.assertRaises(WorkflowError):
            self.service.approve_local(self.run_id, "script", **decision)
        self.fixture.complete("script", test_workflow.SCRIPT)
        decision = self.decision(source="fixture://conversation/new-decision")
        artifact = self.service.next(self.run_id)["approval_requests"][0]["artifact"]
        self.service.artifacts.resolve(artifact).write_text("fixture corruption")
        with self.assertRaisesRegex(WorkflowError, "corrupt"):
            self.service.approve_local(self.run_id, "script", **decision)
        self.assertEqual(self.approved_events(), [])

    def test_mp4_cannot_be_approved_before_review(self):
        # Intentionally incomplete fixture; no claim of a reviewed MP4.
        artifact = self.service.artifacts.put(self.fixture.output("not a reviewed movie"), "mp4")
        def seed(tx, run):
            run["artifacts"][artifact["id"]] = artifact
            run["tasks"]["render"].update(status="complete", outputs=[artifact["id"]])
        self.fixture.store.mutate(self.run_id, seed)
        with self.assertRaisesRegex(WorkflowError, "QA"):
            self.service.approve_local(self.run_id, "mp4", revision=1, sha256=artifact["sha256"],
                                       source="fixture://conversation/mp4", message="Approve fixture movie")
        self.assertEqual(self.approved_events(), [])

    def test_configured_signed_host_does_not_allow_local_bypass(self):
        with self.assertRaisesRegex(WorkflowError, "signed approvals"):
            self.signed_service.approve_local(self.run_id, "script", **self.decision())
        envelope = self.fixture.signed()
        with self.assertRaises(WorkflowError):
            self.signed_service.approve({**envelope, "signature": "bad"})
        self.assertEqual(self.approved_events(), [])
        self.signed_service.approve(envelope)
        self.assertEqual(len(self.approved_events()), 1)

    def test_signed_request_without_key_never_falls_back(self):
        with self.assertRaises(WorkflowError):
            self.service.approve(self.fixture.signed())
        self.assertEqual(self.approved_events(), [])

    def test_doctor_has_no_missing_bridge_or_key_in_local_mode(self):
        checks = {item["capability"]: item for item in inspect(self.service, self.run_id)["checks"]}
        self.assertTrue(checks["approval.local_session"]["available"])
        self.assertNotIn("approval.bridge", checks)
        self.assertNotIn("approval.verifier", checks)

    def test_cli_uses_exact_gate_command_and_returns_next_without_dispatch(self):
        gate = self.service.next(self.run_id)["approval_requests"][0]
        command = ["--db", self.fixture.db, "--workspace", str(self.fixture.directory / "workspace"),
                   "--project-root", str(self.service.project), *gate["approval_command"],
                   "--source", "fixture://conversation/cli-reply", "--message", "утвержда."]
        output = io.StringIO()
        with patch.dict(os.environ, {"YTV_APPROVAL_PUBLIC_KEY": ""}), contextlib.redirect_stdout(output):
            code = main(command)
        self.assertEqual(code, 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["approval"]["revision"], gate["revision"])
        self.assertEqual(result["next"]["run_id"], self.run_id)
        self.assertEqual(result["next"]["status"], "working")
        self.assertEqual(len(self.approved_events()), 1)

    def test_cli_rejects_missing_user_fields_and_mixed_signed_local_input(self):
        gate = self.service.next(self.run_id)["approval_requests"][0]
        prefix = ["--db", self.fixture.db, "--workspace", str(self.fixture.directory / "workspace")]
        for args in (gate["approval_command"], ["approve", "--event", "missing.json", "--message", "fixture"]):
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main(prefix + args), 2)
        self.assertEqual(self.approved_events(), [])


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "isolated PostgreSQL not configured")
class PostgreSQLLocalApprovalTests(LocalApprovalTests):
    postgres = True


if __name__ == "__main__":
    unittest.main()
