"""Runtime-only migration preserves episode state and has no provider path."""
import copy
from concurrent.futures import ThreadPoolExecutor
import json
import shutil
import unittest
from unittest.mock import patch

import test_pool_service
from ytvideos.cli import dispatch, parser
from ytvideos.errors import Conflict, WorkflowError
from ytvideos.util import canonical, digest
from ytvideos.workflow import valid_approval


class RuntimeMigrationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_pool_service.PoolServiceTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.service = self.fixture.production
        self.store = self.fixture.store
        channel_doc = self.service.project / "channels/test_channel/PROFILE.md"
        channel_doc.write_text("Exact channel identity remains frozen.\n")
        run = self.service.create("test_channel", "synthetic migration fixture")
        self.run_id = run["id"]
        path = self.fixture.root / "script.txt"
        path.write_text("Synthetic accepted script used only by this contract test.\n")
        artifact = self.service.artifacts.put(path, "script")
        self.operation = {"key": "fixture-existing-result", "run_id": self.run_id,
                          "kind": "external_video", "input_hash": "e" * 64,
                          "status": "confirmed", "legacy_field": "preserved verbatim"}

        def accepted_fixture(tx, value):
            value["artifacts"][artifact["id"]] = artifact
            value["tasks"]["script"].update(status="complete", outputs=[artifact["id"]])
            value["approvals"]["script"] = {"artifact_id": artifact["id"], "sha256": artifact["sha256"],
                                           "revision": value["revision"], "source": "fixture-approved-input"}
            value["motion_batch"] = {"legacy_saved_result": True, "spent": 9}
            tx.create_operation(self.operation)
        self.store.mutate(self.run_id, accepted_fixture)
        self.source = self.fixture.root / "source-checkout"
        shutil.copytree(self.service.project, self.source)
        (self.service.project / "src/ytvideos/pin.py").write_text("# changed target runtime\n")
        (self.service.project / "skills/ytv-produce-video/SKILL.md").write_text("Target production instructions.\n")
        (self.service.project / "docs/standards/visual.md").write_text("Target visual requirements.\n")

    def state(self):
        with self.store.transaction() as tx:
            operations = [json.loads(row[0]) for row in tx.execute(
                "SELECT doc FROM operations WHERE run_id=? ORDER BY key", (self.run_id,)).fetchall()]
        return self.store.get(self.run_id), self.store.events(self.run_id), operations

    def plan(self):
        return self.service.plan_runtime_migration(self.run_id, self.source,
                                                  expected_version=self.store.get(self.run_id)["version"])

    def apply(self, plan, **overrides):
        return self.service.apply_runtime_migration(self.run_id, self.source, plan,
            **{"source": "fixture-owner-message", "message": "Migrate this exact episode locally.", **overrides})

    def test_plan_is_read_only_and_cli_round_trip_is_explicit(self):
        before = self.state()
        artifacts = sorted(self.service.artifacts.root.rglob("*"))
        args = parser().parse_args(["migrate-runtime", "plan", "--run", self.run_id,
                                   "--source-root", str(self.source), "--expected-version", str(before[0]["version"])])
        plan = dispatch(self.service, args)
        self.assertEqual(plan["plan_sha256"], digest({k: v for k, v in plan.items() if k != "plan_sha256"}))
        self.assertFalse(plan["external_dispatch"])
        self.assertEqual(self.state(), before)
        self.assertEqual(sorted(self.service.artifacts.root.rglob("*")), artifacts)
        target = self.fixture.root / "migration-plan.json"
        target.write_text(canonical(plan))
        args = parser().parse_args(["migrate-runtime", "apply", "--run", self.run_id,
            "--source-root", str(self.source), "--plan", str(target), "--source", "fixture-owner-message",
            "--message", "Migrate this exact episode locally."])
        self.assertFalse(dispatch(self.service, args)["duplicate"])

    def test_apply_preserves_exact_episode_and_archives_restorable_source_state(self):
        before, events, operations = self.state()
        result = self.apply(self.plan())
        after, next_events, next_operations = self.state()
        self.assertEqual(after["version"], before["version"] + 1)
        mutable = {"version", "pins", "skills", "reference_snapshot", "artifacts", "runtime_migrations"}
        self.assertEqual({k: v for k, v in before.items() if k not in mutable},
                         {k: v for k, v in after.items() if k not in mutable})
        self.assertEqual({k: v for k, v in before["pins"].items() if k not in {"code", "skills", "references"}},
                         {k: v for k, v in after["pins"].items() if k not in {"code", "skills", "references"}})
        self.assertEqual({key: after["artifacts"][key] for key in before["artifacts"]}, before["artifacts"])
        self.assertEqual(next_operations, operations)
        self.assertEqual(len(next_events), len(events) + 1)
        self.assertTrue(valid_approval(after, "script"))
        self.service._runtime(after)
        snapshot = result["receipt"]["snapshot_artifact"]
        restored = json.loads(self.service.artifacts.resolve(snapshot).read_text())
        self.assertEqual(restored["run"], before)
        self.assertEqual(restored["operations"], operations)
        self.assertEqual(restored["state_sha256"], digest(restored["run"]))
        self.assertEqual(restored["run"]["pins"], result["receipt"]["source"]["pins"])
        self.assertFalse(result["receipt"]["approval_and_qa_evidence_created"])
        self.assertEqual(result["receipt"]["source"]["root"], str(self.source.resolve()))
        self.assertEqual(result["receipt"]["target"]["root"], str(self.service.project.resolve()))

    def test_pending_unapproved_script_migrates_without_creating_evidence(self):
        def pending(tx, run):
            run["approvals"].pop("script")
            run["tasks"]["script"].update(status="pending", outputs=[])
        self.store.mutate(self.run_id, pending)
        before, _, operations = self.state()
        plan = self.plan()
        self.assertIsNone(plan["preserved"]["script_artifact_id"])
        self.assertIsNone(plan["preserved"]["script_sha256"])
        result = self.apply(plan)
        after, _, after_operations = self.state()
        for key in ("revision", "tasks", "approvals", "budget", "profile"):
            self.assertEqual(after[key], before[key])
        self.assertEqual({key: after["artifacts"][key] for key in before["artifacts"]}, before["artifacts"])
        self.assertEqual(after_operations, operations)
        self.assertFalse(result["receipt"]["approval_and_qa_evidence_created"])
        self.assertEqual(json.loads(self.service.artifacts.resolve(result["receipt"]["snapshot_artifact"]).read_text())["run"], before)

    def test_unapproved_nonpending_or_output_script_cannot_migrate(self):
        for status, outputs in (("complete", []), ("pending", ["unaccepted-output"])):
            with self.subTest(status=status, outputs=outputs):
                def change(tx, run):
                    run["approvals"].pop("script", None)
                    run["tasks"]["script"].update(status=status, outputs=outputs)
                self.store.mutate(self.run_id, change)
                before = self.state()
                with self.assertRaisesRegex(WorkflowError, "pending script without outputs"):
                    self.plan()
                self.assertEqual(self.state(), before)

    def test_identical_retry_is_read_only_and_decision_replay_is_rejected(self):
        plan = self.plan()
        result = self.apply(plan)
        before = self.state()
        duplicate = self.apply(plan)
        self.assertTrue(duplicate["duplicate"])
        self.assertEqual(duplicate["receipt"], result["receipt"])
        self.assertEqual(self.state(), before)
        with self.assertRaisesRegex(Conflict, "decision"):
            self.apply(plan, message="A different decision")
        self.assertEqual(self.state(), before)

    def test_concurrent_delivery_applies_once(self):
        plan = self.plan()
        before = self.state()
        with ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(lambda _: self.apply(plan), range(2)))
        self.assertEqual(sorted(result["duplicate"] for result in results), [False, True])
        self.assertEqual(results[0]["receipt"], results[1]["receipt"])
        after = self.state()
        self.assertEqual(after[0]["version"], before[0]["version"] + 1)
        self.assertEqual(len(after[1]), len(before[1]) + 1)
        self.assertEqual(after[2], before[2])
    def test_snapshot_corruption_is_detected_on_retry(self):
        plan = self.plan()
        result = self.apply(plan)
        path = self.service.artifacts.resolve(result["receipt"]["snapshot_artifact"])
        path.write_text("corrupted archive")
        before = self.state()
        with self.assertRaisesRegex(WorkflowError, "corrupt"):
            self.apply(plan)
        self.assertEqual(self.state(), before)

    def test_stale_version_and_modified_plan_leave_state_unchanged(self):
        plan = self.plan()
        changed = copy.deepcopy(plan)
        changed["target"]["pins"]["code"] = "0" * 64
        before = self.state()
        with self.assertRaisesRegex(WorkflowError, "modified"):
            self.apply(changed)
        self.assertEqual(self.state(), before)
        self.store.mutate(self.run_id, lambda tx, run: run.update(intent="concurrent user edit"))
        before = self.state()
        with self.assertRaisesRegex(Conflict, "stale"):
            self.apply(plan)
        self.assertEqual(self.state(), before)

    def test_changed_source_pin_or_checkout_is_rejected_without_state_changes(self):
        plan = self.plan()
        (self.source / "src/ytvideos/pin.py").write_text("# modified source snapshot\n")
        before = self.state()
        with self.assertRaisesRegex(Conflict, "source checkout"):
            self.apply(plan)
        self.assertEqual(self.state(), before)

    def test_same_version_changed_pins_are_rejected(self):
        plan = self.plan()
        # Model an out-of-contract store edit; normal mutations also advance version.
        with self.store.transaction() as tx:
            run = tx.get_run(self.run_id)
            run["pins"]["code"] = "0" * 64
            tx.execute("UPDATE runs SET doc=? WHERE id=?", (canonical(run), self.run_id))
        before = self.state()
        with self.assertRaisesRegex(Conflict, "source checkout"):
            self.apply(plan)
        self.assertEqual(self.state(), before)

    def test_target_code_and_rules_change_invalidates_exact_plan(self):
        plan = self.plan()
        (self.service.project / "skills/ytv-produce-video/SKILL.md").write_text("Later target rule.\n")
        before = self.state()
        with self.assertRaisesRegex(Conflict, "changed since"):
            self.apply(plan)
        self.assertEqual(self.state(), before)

    def test_changed_target_code_invalidates_plan(self):
        plan = self.plan()
        (self.service.project / "src/ytvideos/pin.py").write_text("# later code edit\n")
        before = self.state()
        with self.assertRaisesRegex(Conflict, "changed since"):
            self.apply(plan)
        self.assertEqual(self.state(), before)

    def test_reusing_decision_for_new_migration_and_noop_migration_are_rejected(self):
        self.apply(self.plan())
        current = self.store.get(self.run_id)
        with self.assertRaisesRegex(WorkflowError, "already matches"):
            self.service.plan_runtime_migration(self.run_id, self.service.project, expected_version=current["version"])
        second_source = self.fixture.root / "second-source-checkout"
        shutil.copytree(self.service.project, second_source)
        (self.service.project / "src/ytvideos/pin.py").write_text("# next runtime version\n")
        plan = self.service.plan_runtime_migration(self.run_id, second_source, expected_version=current["version"])
        before = self.state()
        with self.assertRaisesRegex(Conflict, "already used"):
            self.service.apply_runtime_migration(self.run_id, second_source, plan,
                source="fixture-owner-message", message="Migrate this exact episode locally.")
        self.assertEqual(self.state(), before)

    def test_unknown_operation_is_never_migrated_or_repaired(self):
        with self.store.transaction() as tx:
            operation = tx.operation(self.operation["key"])
            operation["status"] = "unknown"
            tx.put_operation(operation)
        before = self.state()
        with self.assertRaisesRegex(Conflict, "unknown external"):
            self.plan()
        self.assertEqual(self.state(), before)

    def _prepare_continuation(self):
        first_plan = self.plan()
        first = self.apply(first_plan)
        second_source = self.fixture.root / "continuation-source-checkout"
        shutil.copytree(self.service.project, second_source)
        (self.service.project / "src/ytvideos/pin.py").write_text("# verified local runtime repair\n")
        plan = self.service.plan_runtime_migration(self.run_id, second_source,
                                                   expected_version=self.store.get(self.run_id)["version"])
        return first_plan, first, second_source, plan

    def test_explicit_continuation_preserves_state_and_retries_without_writes(self):
        first_plan, first, source_root, plan = self._prepare_continuation()
        before = self.state()
        path = self.fixture.root / "continuation-plan.json"
        path.write_text(canonical(plan))
        args = parser().parse_args(["migrate-runtime", "apply", "--run", self.run_id,
            "--source-root", str(source_root), "--plan", str(path), "--source", "fixture-owner-message",
            "--message", "Migrate this exact episode locally.",
            "--continue-receipt", first["receipt_artifact"]["sha256"]])
        result = dispatch(self.service, args)
        after = self.state()
        self.assertFalse(result["duplicate"])
        self.assertEqual(result["receipt"]["continued_from_receipt_sha256"], first["receipt_artifact"]["sha256"])
        self.assertEqual(after[0]["runtime_migrations"][-1]["continued_from_receipt_sha256"],
                         first["receipt_artifact"]["sha256"])
        self.assertEqual(result["receipt"]["decision"], first["receipt"]["decision"])
        self.assertEqual(after[0]["version"], before[0]["version"] + 1)
        for key in ("id", "revision", "profile", "tasks", "approvals", "budget", "motion_batch"):
            self.assertEqual(after[0][key], before[0][key])
        self.assertEqual(after[2], before[2])
        self.assertEqual({key: after[0]["artifacts"][key] for key in before[0]["artifacts"]}, before[0]["artifacts"])
        retry = dispatch(self.service, args)
        self.assertTrue(retry["duplicate"])
        self.assertEqual(retry["receipt"], result["receipt"])
        self.assertEqual(self.state(), after)
        for receipt_hash in (None, "0" * 64, result["receipt_artifact"]["sha256"]):
            with self.subTest(receipt_hash=receipt_hash):
                with self.assertRaisesRegex(Conflict, "retry differs"):
                    self.service.apply_runtime_migration(self.run_id, source_root, plan,
                        source="fixture-owner-message", message="Migrate this exact episode locally.",
                        continue_receipt=receipt_hash)
                self.assertEqual(self.state(), after)
        with self.assertRaisesRegex(Conflict, "historical migration"):
            self.apply(first_plan)
        self.assertEqual(self.state(), after)

    def test_continuation_rejects_unknown_receipt_or_changed_owner_decision(self):
        _, first, source_root, plan = self._prepare_continuation()
        before = self.state()
        defaults = {"source": "fixture-owner-message", "message": "Migrate this exact episode locally.",
                    "continue_receipt": first["receipt_artifact"]["sha256"]}
        for overrides, error in (({"continue_receipt": "0" * 64}, "latest migration"),
                                 ({"message": "Different authorization"}, "exact owner decision"),
                                 ({"source": "different-owner-source"}, "exact owner decision")):
            with self.subTest(overrides=overrides):
                with self.assertRaisesRegex(Conflict, error):
                    self.service.apply_runtime_migration(self.run_id, source_root, plan, **(defaults | overrides))
                self.assertEqual(self.state(), before)

    def test_continuation_rejects_nonlatest_receipt(self):
        _, first, source_root, plan = self._prepare_continuation()
        self.service.apply_runtime_migration(self.run_id, source_root, plan,
            source="fixture-owner-message", message="Migrate this exact episode locally.",
            continue_receipt=first["receipt_artifact"]["sha256"])
        third_source = self.fixture.root / "third-source-checkout"
        shutil.copytree(self.service.project, third_source)
        (self.service.project / "src/ytvideos/pin.py").write_text("# third verified runtime\n")
        plan = self.service.plan_runtime_migration(self.run_id, third_source,
                                                   expected_version=self.store.get(self.run_id)["version"])
        before = self.state()
        with self.assertRaisesRegex(Conflict, "latest migration"):
            self.service.apply_runtime_migration(self.run_id, third_source, plan,
                source="fixture-owner-message", message="Migrate this exact episode locally.",
                continue_receipt=first["receipt_artifact"]["sha256"])
        self.assertEqual(self.state(), before)

    def test_continuation_rejects_changed_revision_and_missing_history(self):
        plan = self.plan()
        before = self.state()
        with self.assertRaisesRegex(Conflict, "latest recorded"):
            self.apply(plan, continue_receipt="0" * 64)
        self.assertEqual(self.state(), before)
        _, first, source_root, plan = self._prepare_continuation()
        self.store.mutate(self.run_id, lambda tx, run: run.update(revision=run["revision"] + 1))
        before = self.state()
        with self.assertRaisesRegex(Conflict, "pins or revision"):
            self.service.apply_runtime_migration(self.run_id, source_root, plan,
                source="fixture-owner-message", message="Migrate this exact episode locally.",
                continue_receipt=first["receipt_artifact"]["sha256"])
        self.assertEqual(self.state(), before)

    def test_continuation_rejects_intervening_run_transition(self):
        _, first, source_root, _ = self._prepare_continuation()
        self.store.mutate(self.run_id, lambda tx, run: run.update(intent="an intervening task"))
        plan = self.service.plan_runtime_migration(self.run_id, source_root,
                                                   expected_version=self.store.get(self.run_id)["version"])
        before = self.state()
        with self.assertRaisesRegex(Conflict, "state version"):
            self.service.apply_runtime_migration(self.run_id, source_root, plan,
                source="fixture-owner-message", message="Migrate this exact episode locally.",
                continue_receipt=first["receipt_artifact"]["sha256"])
        self.assertEqual(self.state(), before)

    def test_uncertain_motion_batch_and_unsettled_reservations_block_migration(self):
        for batch in ({"scenes": {"shot": {"status": "unknown"}}, "reserved": 0},
                      {"scenes": {"shot": {"status": "dispatched"}}, "reserved": 0},
                      {"scenes": {"shot": {"status": "generated"}}, "reserved": 20}):
            with self.subTest(batch=batch):
                self.store.mutate(self.run_id, lambda tx, run: run.update(motion_batch=batch))
                before = self.state()
                with self.assertRaisesRegex(Conflict, "saved motion batch"):
                    self.plan()
                self.assertEqual(self.state(), before)
        self.store.mutate(self.run_id, lambda tx, run: run.update(motion_batch=None))
        self.store.mutate(self.run_id, lambda tx, run: run["budget"].update(unknown_reserved=2))
        before = self.state()
        with self.assertRaisesRegex(Conflict, "budget"):
            self.plan()
        self.assertEqual(self.state(), before)

    def test_changes_during_receipt_archival_do_not_commit(self):
        from ytvideos import migration
        real_put = migration._put_json
        run = self.store.get(self.run_id)
        artifact = run["artifacts"][run["approvals"]["script"]["artifact_id"]]
        paths = [self.source / "src/ytvideos/pin.py", self.service.project / "src/ytvideos/pin.py",
                 self.service.artifacts.resolve(artifact)]
        for path in paths:
            with self.subTest(path=path):
                plan = self.plan()
                before = self.state()
                original = path.read_bytes()

                def change_after_receipt(service, value, kind):
                    result = real_put(service, value, kind)
                    if kind == "runtime_migration":
                        path.write_bytes(original + b"changed during receipt archival")
                    return result

                try:
                    with patch("ytvideos.migration._put_json", side_effect=change_after_receipt):
                        with self.assertRaises((Conflict, WorkflowError)):
                            self.apply(plan)
                    self.assertEqual(self.state(), before)
                finally:
                    path.write_bytes(original)

    def test_active_task_claim_blocks_even_if_expired(self):
        def active(tx, run):
            run["tasks"]["audio"].update(status="running", claim={"expires_at": 0})
        self.store.mutate(self.run_id, active)
        before = self.state()
        with self.assertRaisesRegex(Conflict, "task claims"):
            self.plan()
        self.assertEqual(self.state(), before)

    def test_queued_pool_or_active_slot_blocks_migration(self):
        self.store.mutate(self.run_id, lambda tx, run: run.update(pool={
            "backend": {"requests": {"job": {"status": "queued"}}}, "scheduler": {"records": []}}))
        before = self.state()
        with self.assertRaisesRegex(Conflict, "pool work"):
            self.plan()
        self.assertEqual(self.state(), before)
        self.store.mutate(self.run_id, lambda tx, run: run.update(pool=None))
        with self.store.transaction() as tx:
            tx.execute("INSERT INTO runtime_slots VALUES (?,?,?,?,?)", ("slot", "runtime", self.run_id, "op", "unknown"))
        before = self.state()
        with self.assertRaisesRegex(Conflict, "runtime slots"):
            self.plan()
        self.assertEqual(self.state(), before)

    def test_changed_profile_or_channel_document_is_not_silently_adopted(self):
        profile_path = self.service.project / "channels/test_channel/channel.json"
        profile = json.loads(profile_path.read_text())
        profile["name"] = "Changed policy"
        profile_path.write_text(json.dumps(profile))
        before = self.state()
        with self.assertRaisesRegex(Conflict, "exact channel profile"):
            self.plan()
        self.assertEqual(self.state(), before)
        shutil.copyfile(self.source / "channels/test_channel/channel.json", profile_path)
        (self.service.project / "channels/test_channel/PROFILE.md").write_text("Changed channel identity.\n")
        with self.assertRaisesRegex(Conflict, "channel document"):
            self.plan()
        self.assertEqual(self.state(), before)

    def test_missing_artifact_or_stale_script_approval_cannot_migrate(self):
        run = self.store.get(self.run_id)
        artifact = run["artifacts"][run["approvals"]["script"]["artifact_id"]]
        path = self.service.artifacts.resolve(artifact)
        original = path.read_bytes()
        path.write_bytes(b"changed script bytes")
        before = self.state()
        with self.assertRaisesRegex(WorkflowError, "corrupt"):
            self.plan()
        self.assertEqual(self.state(), before)
        path.write_bytes(original)
        self.store.mutate(self.run_id, lambda tx, value: value["approvals"]["script"].update(sha256="0" * 64))
        before = self.state()
        with self.assertRaisesRegex(Conflict, "accepted script"):
            self.plan()
        self.assertEqual(self.state(), before)

    def test_schema_upgrade_and_incomplete_target_routes_are_rejected(self):
        path = self.service.project / ".agents/skills/ytv-produce-video/references/video-clips.md"
        path.unlink()
        before = self.state()
        with self.assertRaisesRegex(WorkflowError, "missing.*reference"):
            self.plan()
        self.assertEqual(self.state(), before)
        shutil.copyfile(self.source / path.relative_to(self.service.project), path)
        self.store.mutate(self.run_id, lambda tx, value: value["pins"].update(workflow=999))
        before = self.state()
        with self.assertRaisesRegex(WorkflowError, "workflow version"):
            self.plan()
        self.assertEqual(self.state(), before)


if __name__ == "__main__":
    unittest.main()
