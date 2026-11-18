"""Synthetic owner decisions: import exact source, never fabricate editorial QA."""
import contextlib
from concurrent.futures import ThreadPoolExecutor
import io
import json
import os
import unittest
from unittest.mock import patch

import test_workflow
from ytvideos.doctor import inspect
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.service import Production
from ytvideos.source_script import accept_source, main
from ytvideos.store import Store
from ytvideos.util import file_digest
from ytvideos.workflow import valid_approval


class SourceScriptTests(unittest.TestCase):
    postgres = False

    def setUp(self):
        self.fixture = test_workflow.WorkflowContract()
        self.fixture.postgres = self.postgres
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.addCleanup(self.fixture.tearDown)
        self.service = self.restarted()
        self.script_path = self.fixture.output(test_workflow.SCRIPT + "\n", "selected.en.txt")
        self.run = self.new_run()
        self.run_id = self.run["id"]

    def restarted(self):
        return Production(Store(self.fixture.db), self.fixture.directory / "workspace", test_workflow.ROOT,
                          clock=lambda: self.fixture.clock)

    def new_run(self, **changes):
        args = {"format": "long", "source_script": self.script_path,
                "capabilities": {"model.text": {"available": True, "evidence": "software fixture"}}}
        args.update(changes)
        return self.service.create("paper_detour", "Produce the owner-selected PR script", **args)

    def decision(self, **changes):
        return {"revision": self.run["revision"], "sha256": file_digest(self.script_path),
                "source": "fixture://conversation/production-instruction",
                "message": "Бери этот готовый сценарий в производство.",
                "origin": "fixture://repo/commit-123/script.en.txt", **changes}

    def accept(self, **changes):
        return accept_source(self.service, self.run_id, **self.decision(**changes))

    def approved_events(self):
        return [e for e in self.fixture.store.events(self.run_id) if e["kind"] == "user.approved"]

    def test_source_file_alone_does_not_grant_approval(self):
        self.assertFalse(valid_approval(self.fixture.store.get(self.run_id), "script"))
        self.assertEqual([t["id"] for t in self.service.next(self.run_id)["tasks"]], ["research"])

    def test_selected_source_enters_production_without_research_or_independent_review(self):
        budget = self.run["budget"].copy()
        approval = self.accept()
        saved = self.fixture.store.get(self.run_id)
        self.assertEqual(saved["tasks"]["research"]["status"], "skipped")
        self.assertEqual(saved["tasks"]["script"]["dependencies"], [])
        self.assertTrue(valid_approval(saved, "script"))
        self.assertIsNone(saved["tasks"]["script"].get("receipt"))
        self.assertFalse(saved["tasks"]["script"]["source_import"]["review_performed"])
        self.assertEqual(self.service.artifacts.resolve(saved["artifacts"][approval["artifact_id"]]).read_bytes(),
                         self.script_path.read_bytes())
        self.assertEqual(saved["budget"], budget)
        self.assertEqual({t["id"] for t in self.service.next(self.run_id)["tasks"]},
                         {"storyboard", "audio", "packaging"})
        self.assertEqual(self.service.next(self.run_id)["approval_requests"], [])
        self.assertEqual(self.service.plan(self.run_id)["source_script"]["sha256"], file_digest(self.script_path))
        packet = self.service.context(self.run_id, "storyboard")
        self.assertEqual(packet["inputs"][0]["sha256"], file_digest(self.script_path))
        self.assertEqual(saved["approvals"]["script"]["scope"], "produce_video")
        self.assertNotIn("mp4", saved["approvals"])
        with self.fixture.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM operations WHERE run_id=?", (self.run_id,)).fetchone()[0], 0)
        self.service.claim(self.run_id, "storyboard", "storyboard-fixture")

    def test_imported_plan_and_doctor_do_not_request_editorial_tools(self):
        self.accept()
        plan = self.service.plan(self.run_id)
        steps = {step["id"]: step for step in plan["steps"]}
        for name in ("research", "script"):
            self.assertEqual(steps[name]["required_checks"], [])
            self.assertIsNone(steps[name]["completion_command"])
        self.assertNotIn("independent_review", steps["script"])
        self.assertFalse(steps["script"]["source_import"]["review_performed"])
        gaps = {gap["capability"] for gap in plan["capability_gaps"]}
        self.assertNotIn("web.search", gaps)
        self.assertNotIn("sessions.independent", gaps)
        capabilities = {check["capability"] for check in inspect(self.service, self.run_id)["checks"]}
        self.assertNotIn("web.search", capabilities)
        self.assertNotIn("sessions.independent", capabilities)
        self.assertIn("audio.produce", capabilities)
        self.assertIn("image.generate", capabilities)

    def test_audio_production_can_complete_with_explicit_unverified_listening(self):
        self.accept()
        self.service.capabilities(self.run_id, {
            "audio.produce": {"available": True, "billing": "included"}, "audio.listen": False,
            "subtitle.align": True,
        }, evidence="synthetic provider only, no listening available")
        guide = self.service.context(self.run_id, "audio")["task_guide"]
        self.assertEqual(guide["execution_capabilities"], ["audio.produce"])
        self.assertNotIn("audio.listen", guide["completion_capabilities"])
        self.assertIn("listening", guide["required_checks"])
        claim = self.service.claim(self.run_id, "audio", "synthetic-producer")
        path = self.fixture.output("synthetic audio bytes", "audio.bin")
        checks = [{"name": name, "status": "pass", "method": "synthetic contract test",
                   "observed": {"fixture": True}} for name in guide["required_checks"]]
        listening = next(c for c in checks if c["name"] == "listening")
        listening.update(status="unverified", observed={"artifact_sha256": file_digest(path),
                         "reason": "No listening interface in synthetic fixture"})
        exact = next(c for c in checks if c["name"] == "exact_text")
        exact.update(status="unverified", observed={"artifact_sha256": file_digest(path),
                     "script_sha256": file_digest(self.script_path), "reason": "No listening interface"})
        receipt = {"run_id": self.run_id, "task_id": "audio", "worker": claim["worker"],
                   "input_hash": claim["input_hash"], "output_sha256": file_digest(path), "checks": checks}
        run = self.service.store.get(self.run_id)
        artifact = {"sha256": file_digest(path)}
        self.service._validate_receipt(run, run["tasks"]["audio"], claim, artifact, receipt)
        for defect in ("wrong_hash", "empty_reason", "pass", "other_check", "irrelevant_no_speech"):
            bad = json.loads(json.dumps(receipt))
            check = next(c for c in bad["checks"] if c["name"] == "listening")
            if defect == "wrong_hash":
                check["observed"]["artifact_sha256"] = "0" * 64
            if defect == "empty_reason":
                check["observed"]["reason"] = ""
            if defect == "pass":
                check["status"] = "pass"
            if defect == "other_check":
                bad["checks"].append({"name": "rights", "status": "unverified", "method": "fixture", "observed": {"reason": "missing"}})
            if defect == "irrelevant_no_speech":
                bad["checks"].append({**check, "name": "no_speech"})
            with self.subTest(defect=defect), self.assertRaises(WorkflowError):
                self.service._validate_receipt(run, run["tasks"]["audio"], claim, artifact, bad)
        # Media decoding/provenance has its own suite; only replace it in this state-transition fixture.
        def measured(run, task, artifact, receipt=None):
            task["media_validation"] = {"fixture": True}
        with patch.object(self.service, "_validate_output", side_effect=measured):
            result = self.service.complete(self.run_id, "audio", claim["token"], path,
                                           self.fixture.output(receipt, "audio-receipt.json"), actual_units=0)
        self.assertEqual(result["unverified_checks"], [exact, listening])
        step = next(x for x in self.service.plan(self.run_id)["steps"] if x["id"] == "audio")
        self.assertEqual(step["unverified_checks"], [exact, listening])
        packet = self.service.context(self.run_id, "subtitles")
        self.assertEqual(packet["unverified_production_checks"], {"audio": [exact, listening]})
        self.service.claim(self.run_id, "subtitles", "synthetic-aligner")
        self.assertFalse(valid_approval(self.service.store.get(self.run_id), "mp4"))
        review_task = {**run["tasks"]["review"]}
        # Review never accepts the production-only deferred status.
        bad = {**receipt, "task_id": "review"}
        with self.assertRaises(WorkflowError):
            self.service._validate_receipt(run, review_task, claim, artifact, bad)

    def test_preview_exact_text_is_unverified_not_source_identity_or_final_qa(self):
        self.accept()
        self.service.capabilities(self.run_id, {
            "audio.produce": {"available": True, "billing": "included"}, "audio.listen": False,
        }, evidence="synthetic unavailable hearing")
        claim = self.service.claim(self.run_id, "audio", "synthetic-producer")
        run = self.service.store.get(self.run_id)
        task = run["tasks"]["audio"]
        artifact = {"sha256": "1" * 64}
        checks = [{"name": name, "status": "pass", "method": "synthetic fixture",
                   "observed": {"fixture": True}}
                  for name in self.service.context(self.run_id, "audio")["required_checks"]]
        for check in checks:
            if check["name"] in {"listening", "exact_text"}:
                check.update(status="unverified", observed={"artifact_sha256": artifact["sha256"],
                    "reason": "No hearing; provider alignment is not audible speech evidence"})
            if check["name"] == "exact_text":
                check["observed"]["script_sha256"] = file_digest(self.script_path)
        receipt = {"run_id": self.run_id, "task_id": "audio", "worker": claim["worker"],
                   "input_hash": claim["input_hash"], "output_sha256": artifact["sha256"], "checks": checks}
        self.service._validate_receipt(run, task, claim, artifact, receipt)
        for defect in ("source", "audio", "missing_source", "failed", "false_pass", "identity", "listening_available", "review"):
            bad = json.loads(json.dumps(receipt))
            exact = next(c for c in bad["checks"] if c["name"] == "exact_text")
            changed_run, changed_task = json.loads(json.dumps(run)), task
            if defect == "source":
                exact["observed"]["script_sha256"] = "0" * 64
            if defect == "audio":
                exact["observed"]["artifact_sha256"] = "0" * 64
            if defect == "missing_source":
                del exact["observed"]["script_sha256"]
            if defect == "failed":
                exact["status"] = "fail"
            if defect == "false_pass":
                exact["status"] = "pass"
            if defect == "identity":
                next(c for c in bad["checks"] if c["name"] == "voice_identity")["status"] = "unverified"
            if defect == "listening_available":
                changed_run["capabilities"]["audio.listen"] = {"available": True, "evidence": "synthetic hearing available"}
            if defect == "review":
                changed_task = run["tasks"]["review"]
                bad["task_id"] = "review"
            with self.subTest(defect=defect), self.assertRaises(WorkflowError):
                self.service._validate_receipt(changed_run, changed_task, claim, artifact, bad)

    def test_no_speech_production_defers_listening_but_not_identity(self):
        self.accept()
        self.service.capabilities(self.run_id, {"audio.listen": False}, evidence="synthetic unavailable hearing")
        run = self.service.store.get(self.run_id)
        artifact = self.service.artifacts.put(self.script_path, "audio")
        for stage, names in (("audio", ["source_identity", "listening", "no_speech"]),
                             ("subtitles", ["no_speech"])):
            task = run["tasks"][stage]
            claim = {"worker": "synthetic-producer", "input_hash": "fixture"}
            checks = [{"name": name, "status": "pass" if name == "source_identity" else "unverified",
                       "method": "synthetic contract test", "observed": {"fixture": True} if name == "source_identity" else
                       {"artifact_sha256": artifact["sha256"], "reason": "No listening interface"}} for name in names]
            receipt = {"run_id": self.run_id, "task_id": stage, "worker": claim["worker"],
                       "input_hash": "fixture", "output_sha256": artifact["sha256"], "checks": checks}
            with self.subTest(stage=stage), patch.object(self.service, "requirements", return_value={"speech": {"mode": "none"}}), \
                 patch.object(self.service, "_artifact", return_value=artifact), \
                 patch("ytvideos.media_checks.probe_media", return_value={"duration_seconds": 1}):
                self.service._validate_receipt(run, task, claim, artifact, receipt)
                checks[0]["status"] = "fail"
                with self.assertRaises(WorkflowError):
                    self.service._validate_receipt(run, task, claim, artifact, receipt)

    def test_audio_generation_still_requires_provider_and_budget(self):
        self.accept()
        with self.assertRaisesRegex(WorkflowError, "audio.produce"):
            self.service.claim(self.run_id, "audio", "synthetic-producer")
        self.service.capabilities(self.run_id, {
            "audio.produce": {"available": True, "billing": "metered"}, "audio.listen": False,
        }, evidence="synthetic metered provider")
        with self.assertRaisesRegex(WorkflowError, "reserve the observed provider cost"):
            self.service.claim(self.run_id, "audio", "synthetic-producer")

    def test_audio_listening_capability_does_not_replace_evidence(self):
        self.accept()
        self.service.capabilities(self.run_id, {
            "audio.produce": {"available": True, "billing": "included"}, "audio.listen": True,
        }, evidence="synthetic QA fixture")
        claim = self.service.claim(self.run_id, "audio", "synthetic-producer")
        run = self.service.store.get(self.run_id)
        artifact = {"sha256": "1" * 64}
        receipt = {"run_id": self.run_id, "task_id": "audio", "worker": claim["worker"],
                   "input_hash": claim["input_hash"], "output_sha256": artifact["sha256"], "checks": []}
        with self.assertRaisesRegex(WorkflowError, "missing checks:.*listening"):
            self.service._validate_receipt(run, run["tasks"]["audio"], claim, artifact, receipt)

    def test_short_source_import_preserves_production_loop_policy(self):
        short = self.new_run(format="short")
        accept_source(self.service, short["id"], **self.decision())
        self.assertEqual(self.service.requirements(self.fixture.store.get(short["id"]))["narrative_loop"], "required")
        self.assertEqual({t["id"] for t in self.service.next(short["id"])["tasks"]},
                         {"storyboard", "audio", "packaging"})
        self.assertFalse(valid_approval(self.fixture.store.get(short["id"]), "mp4"))

    def test_retry_restart_and_concurrent_delivery_keep_one_original_decision(self):
        def deliver(_):
            return accept_source(self.restarted(), self.run_id, **self.decision())
        with ThreadPoolExecutor(max_workers=2) as pool:
            first, second = pool.map(deliver, range(2))
        self.assertEqual(first, second)
        self.assertEqual(len(self.approved_events()), 1)
        claim = self.service.claim(self.run_id, "storyboard", "storyboard-fixture")
        self.assertEqual(self.accept(), first)
        self.assertEqual(self.fixture.store.get(self.run_id)["tasks"]["storyboard"]["claim"], claim)

    def test_wrong_revision_hash_or_missing_provenance_does_not_change_run(self):
        before = self.fixture.store.get(self.run_id)
        for changes in ({"revision": 99}, {"revision": True}, {"sha256": "0" * 64},
                        {"sha256": "bad"}, {"source": ""}, {"message": ""}, {"origin": ""}):
            with self.subTest(changes=changes), self.assertRaises(WorkflowError):
                self.accept(**changes)
            self.assertEqual(self.fixture.store.get(self.run_id), before)

    def test_same_message_cannot_accept_another_origin_or_run(self):
        self.accept()
        with self.assertRaises(Conflict):
            self.accept(origin="fixture://repo/a-different-commit/script.en.txt")
        other = self.new_run()
        before = self.fixture.store.get(other["id"])
        with self.assertRaises(Conflict):
            accept_source(self.service, other["id"], **self.decision())
        self.assertEqual(self.fixture.store.get(other["id"]), before)

    def test_outline_missing_source_and_signed_only_host_are_not_bypassed(self):
        missing = self.new_run(source_script=None)
        with self.assertRaisesRegex(WorkflowError, "no pinned source"):
            accept_source(self.service, missing["id"], **self.decision())
        outline = self.fixture.output("A short topic, not a production script.", "outline.txt")
        small = self.new_run(source_script=outline)
        with self.assertRaisesRegex(WorkflowError, "complete narration"):
            accept_source(self.service, small["id"], **self.decision(sha256=file_digest(outline)))
        with self.assertRaisesRegex(WorkflowError, "signed"):
            accept_source(self.fixture.service, self.run_id, **self.decision())

    def test_active_or_blocked_tasks_require_real_recovery(self):
        for state in ("blocked", "unknown", "running"):
            run = self.new_run()
            self.fixture.store.mutate(run["id"], lambda tx, doc: doc["tasks"]["script"].update(
                status=state, blocker="fixture issue"))
            before = self.fixture.store.get(run["id"])
            with self.assertRaises(Conflict):
                accept_source(self.service, run["id"], **self.decision())
            self.assertEqual(self.fixture.store.get(run["id"]), before)
        self.service.cancel(self.run_id, "fixture cancel")
        with self.assertRaisesRegex(Conflict, "cancelled"):
            self.accept()

    def test_resolved_editorial_blocker_continues_same_source_run(self):
        self.fixture.store.mutate(self.run_id, lambda tx, run: run["tasks"]["script"].update(
            status="blocked", blocker="fixture: repeated editorial review was not requested"))
        self.service.unblock(self.run_id, "script", "fixture: original owner instruction and exact source verified")
        self.accept()
        self.assertEqual(self.fixture.store.get(self.run_id)["id"], self.run_id)
        self.assertEqual(self.service.next(self.run_id)["blockers"], [])

    def test_revised_script_cannot_reuse_old_acceptance(self):
        self.accept()
        self.service.revise(self.run_id, "script", "fixture: owner requests different text")
        with self.assertRaisesRegex(Conflict, "revision"):
            self.accept()
        self.assertFalse(valid_approval(self.fixture.store.get(self.run_id), "script"))

    def test_cli_returns_production_tasks_not_an_editorial_pass(self):
        decision = self.decision()
        output = io.StringIO()
        argv = ["--db", self.fixture.db, "--workspace", str(self.fixture.directory / "workspace"),
                "--project-root", str(test_workflow.ROOT), "--run", self.run_id]
        for key, value in decision.items():
            argv += ["--" + key, str(value)]
        with patch.dict(os.environ, {}, clear=True), contextlib.redirect_stdout(output):
            self.assertEqual(main(argv), 0)
        result = json.loads(output.getvalue())
        self.assertFalse(result["review_performed"])
        self.assertFalse(result["providers_called"])
        self.assertEqual({t["id"] for t in result["next"]["tasks"]}, {"storyboard", "audio", "packaging"})


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "PostgreSQL integration not configured")
class PostgreSQLSourceScriptTests(SourceScriptTests):
    postgres = True
