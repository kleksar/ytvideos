import concurrent.futures
import json
import os
from pathlib import Path
import struct
import tempfile
import threading
import unittest
import zlib
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit
import uuid

from ytvideos.errors import Conflict, WorkflowError
from ytvideos.pool_service import PoolService
from ytvideos.service import Production
from ytvideos.store import Store
from ytvideos.util import file_digest
from ytvideos.workflow import REQUIRED_CHECKS


def png_bytes():
    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    pixels = b"\x00" + b"\xff\x88\x00" * 2
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 2, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(pixels * 2)) + chunk(b"IEND", b""))


class PoolServiceTests(unittest.TestCase):
    postgres = False

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        project = self.root / "project"
        (project / "src" / "ytvideos").mkdir(parents=True)
        (project / "src" / "ytvideos" / "pin.py").write_text("# stable source identity for fixture\n")
        (project / ".agent").mkdir()
        entries = []
        for name in ["ytv-write-script", "ytv-produce-video", "ytv-release-video", "ytv-review-video"]:
            path = project / "skills" / name / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(f"# {name}\nFixture skill.\n")
            entries.append({"name": name, "path": str(path.relative_to(project))})
        (project / ".agent" / "skill-catalog.json").write_text(json.dumps({"skills": entries}))
        profile_dir = project / "channels" / "test_channel"
        profile_dir.mkdir(parents=True)
        (profile_dir / "channel.json").write_text(json.dumps({
            "schema_version": 1, "id": "test_channel", "name": "Test channel", "status": "active",
            "language": "en", "recipe": "illustrated", "youtube_channel_id": "TEST_ONLY_CHANNEL", "visual_profile": "test",
            "release_policy": {}, "budget": {"max_paid_units": 20, "max_task_attempts": 3, "max_editorial_passes": 2},
        }))
        self.db = str(self.root / "state.db")
        if self.postgres:
            import psycopg
            from psycopg import sql
            url = os.environ["YTV_TEST_POSTGRES_URL"]
            schema = "ytv_pool_test_" + uuid.uuid4().hex
            with psycopg.connect(url, autocommit=True) as connection:
                connection.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema)))

            def cleanup_schema():
                with psycopg.connect(url, autocommit=True) as connection:
                    connection.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))

            self.addCleanup(cleanup_schema)
            parts = urlsplit(url)
            query = parse_qsl(parts.query, keep_blank_values=True)
            options = " ".join(value for key, value in query if key == "options")
            query = [(key, value) for key, value in query if key != "options"]
            query.append(("options", (options + " -csearch_path=" + schema + " -cstatement_timeout=10000").strip()))
            self.db = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query, quote_via=quote), parts.fragment))
        self.store = Store(self.db)
        self.now = 1000.0
        self.production = Production(self.store, self.root / "work", project, clock=lambda: self.now)
        self.pools = PoolService(self.production)
        self.image = self.root / "fixture.png"
        self.image.write_bytes(png_bytes())

    def make_run(self, *, capacity=2, review_capacity=3, count=2, billing="included", channel="test_channel"):
        if channel != "test_channel":
            template = json.loads((self.production.project / "channels" / "test_channel" / "channel.json").read_text())
            template.update(id=channel, name=channel)
            directory = self.production.project / "channels" / channel
            directory.mkdir(exist_ok=True)
            (directory / "channel.json").write_text(json.dumps(template))
        run = self.production.create(channel, "test scene production", capabilities={
            "sessions.independent": {"available": True, "evidence": "fixture runtime exposes fresh sessions",
                                     "runtime_key": "fixture-runtime", "max_sessions": capacity},
            "image.generate": {"available": True, "evidence": "fixture image generator", "billing": billing},
        })
        script = self.root / (run["id"] + "-script.txt")
        script.write_text("A verified synthetic fixture narration. " * 15)
        board = self.root / (run["id"] + "-board.json")
        board.write_text(json.dumps({"scenes": [{"id": f"s{n}", "prompt": f"Fixture {n}", "visual_intent": "test"}
                                                 for n in range(count)]}))
        script_artifact = self.production.artifacts.put(script, "script")
        board_artifact = self.production.artifacts.put(board, "storyboard")
        # This fixture starts from previously approved input; approval cryptography
        # belongs to separate tests. Real operation entry still uses the same guards.
        def prepare(tx, value):
            for key, artifact in (("script", script_artifact), ("storyboard", board_artifact)):
                value["artifacts"][artifact["id"]] = artifact
                value["tasks"][key].update(status="complete", outputs=[artifact["id"]])
            value["approvals"]["script"] = {"artifact_id": script_artifact["id"], "revision": value["revision"]}
            self.production._expand_scenes(value, board_artifact)
        self.store.mutate(run["id"], prepare)
        self.pools.operate(run["id"], "initialize", {"runtime_key": "fixture-runtime", "max_sessions": capacity,
            "review_capacity": review_capacity, "evidence": "fixture runtime verified shared capacity"})
        self.pools.operate(run["id"], "enqueue")
        result = self.pools.operate(run["id"], "tick")
        return run["id"], result["pending"][0] if result["pending"] else None

    def claim(self, run_id, request, *, estimated_units=0):
        return self.pools.operate(run_id, "claim", {"operation_id": request["operation_id"],
            "worker": "native-worker", "estimated_units": estimated_units})

    def native_complete(self, run_id, granted):
        request = granted["request"]
        self.pools.operate(run_id, "submitted", {"operation_id": request["operation_id"],
            "claim_token": request["claim_token"], "provider": {"tool": "fixture-native", "session_id": run_id + "-session"}})
        return self.pools.operate(run_id, "result", {"operation_id": request["operation_id"],
            "claim_token": request["claim_token"], "receipt_id": "native-result", "status": "completed",
            "artifact_path": str(self.image), "generation_seconds": 20,
            "evidence": {"tool_result_id": "fixture-image-result"}})

    def qa_complete(self, run_id, task_id, claim):
        receipt = self.root / (run_id + "-qa.json")
        receipt.write_text(json.dumps({"run_id": run_id, "task_id": task_id, "input_hash": claim["input_hash"],
            "output_sha256": file_digest(self.image), "worker": claim["worker"],
            "checks": [{"name": name, "status": "pass", "method": "fixture local check",
                        "observed": {"fixture": True, "sha256": file_digest(self.image)}}
                       for name in REQUIRED_CHECKS["scene_image"]]}))
        return self.production.complete(run_id, task_id, claim["token"], self.image, receipt, actual_units=0)

    def test_claim_reserves_budget_and_dispatch_intent_atomically(self):
        run_id, request = self.make_run(billing="metered")
        granted = self.claim(run_id, request, estimated_units=3)
        run = self.store.get(run_id)
        self.assertEqual(run["budget"]["reserved"], 3)
        self.assertEqual(run["tasks"]["image:s0"]["status"], "running")
        with self.store.transaction() as tx:
            self.assertEqual(tx.operation(granted["operation"]["key"])["status"], "dispatched")
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM runtime_slots WHERE state='reserved'").fetchone()[0], 1)
        with self.assertRaises(Conflict):
            self.claim(run_id, request, estimated_units=3)
        self.assertEqual(self.store.get(run_id)["budget"]["reserved"], 3)

    def test_accept_requires_production_checks_for_same_image(self):
        run_id, request = self.make_run()
        granted = self.claim(run_id, request)
        self.native_complete(run_id, granted)
        accept = {"job_id": request["packet"]["job_id"], "review_id": "verified-image", "service_seconds": 4}
        with self.assertRaises(Conflict):
            self.pools.operate(run_id, "accept", accept)
        self.qa_complete(run_id, "image:s0", granted["task_claim"])
        self.assertEqual(self.pools.operate(run_id, "accept", accept)["status"], "accepted")
        self.assertEqual(self.pools.operate(run_id, "accept", accept)["status"], "accepted")

    def test_global_capacity_applies_across_runs_and_releases_on_result(self):
        first, first_request = self.make_run(capacity=1, count=1)
        second, second_request = self.make_run(capacity=1)
        granted = self.claim(first, first_request)
        with self.assertRaises(Conflict):
            self.claim(second, second_request)
        self.assertEqual(self.store.get(second)["tasks"]["image:s0"]["status"], "pending")
        self.native_complete(first, granted)
        self.assertTrue(self.claim(second, second_request)["task_claim"]["token"])

    def test_ten_channels_receive_round_robin_dispatch_turns(self):
        for n in range(10):
            self.make_run(capacity=1, channel=f"channel_{n:02d}")
        served = []
        for _ in range(10):
            candidate = self.pools.candidates("fixture-runtime")["candidates"][0]
            granted = self.claim(candidate["run_id"], candidate)
            served.append(candidate["channel_id"])
            self.native_complete(candidate["run_id"], granted)
            same_channel = self.pools.operate(candidate["run_id"], "pending")["requests"]
            if len(served) < 10:
                with self.assertRaises(Conflict):
                    self.claim(candidate["run_id"], same_channel[0])
        self.assertEqual(served, [f"channel_{n:02d}" for n in range(10)])
        self.assertEqual(self.pools.candidates("fixture-runtime")["candidates"][0]["channel_id"], "channel_00")

    def test_concurrent_claims_cannot_overbook_shared_runtime(self):
        first, first_request = self.make_run(capacity=1)
        second, second_request = self.make_run(capacity=1)
        barrier = threading.Barrier(2)
        def attempt(pair):
            barrier.wait(timeout=5)
            try:
                return self.claim(*pair)["task_claim"]["token"]
            except Conflict:
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            results = list(executor.map(attempt, [(first, first_request), (second, second_request)]))
        self.assertEqual(sum(result is not None for result in results), 1)

    def test_unknown_keeps_global_capacity_and_recovery_never_dispatches(self):
        run_id, request = self.make_run(capacity=1)
        granted = self.claim(run_id, request)
        self.pools.operate(run_id, "submitted", {"operation_id": request["operation_id"],
            "claim_token": granted["request"]["claim_token"],
            "provider": {"tool": "native-fixture", "session_id": "observed-session"}})
        status = self.pools.operate(run_id, "status")
        self.assertEqual(status["jobs"][0]["status"], "running")  # Normal reload is not a crash.
        recovered = self.pools.operate(run_id, "recover")
        self.assertEqual(recovered["jobs"][0]["status"], "unknown")
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "unknown")
        self.assertEqual(recovered["pending"], [])
        other, other_request = self.make_run(capacity=1)
        with self.assertRaises(Conflict):
            self.claim(other, other_request)

    def test_reconciled_existing_result_can_complete_without_new_generation(self):
        run_id, request = self.make_run(capacity=1)
        granted = self.claim(run_id, request)
        self.pools.operate(run_id, "recover")
        self.pools.operate(run_id, "result", {"operation_id": request["operation_id"],
            "claim_token": granted["request"]["claim_token"], "receipt_id": "read-back-result", "status": "completed",
            "artifact_path": str(self.image), "evidence": {"tool_read_back": "existing image"}})
        self.pools.operate(run_id, "reconcile", {"job_id": request["packet"]["job_id"]})
        recovered_claim = self.production.reconcile_task(run_id, "image:s0", worker="reconciler",
            outcome="completed", evidence="native read-back of the already generated image")
        self.qa_complete(run_id, "image:s0", recovered_claim)
        result = self.pools.operate(run_id, "accept", {"job_id": request["packet"]["job_id"],
            "review_id": "recovered-review", "service_seconds": 4})
        self.assertEqual(result["status"], "accepted")
        with self.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM operations WHERE run_id=?", (run_id,)).fetchone()[0], 1)

    def test_old_unknown_receipt_replay_cannot_regress_confirmed_operation(self):
        run_id, request = self.make_run(capacity=1, count=1)
        granted = self.claim(run_id, request)
        unknown = {"operation_id": request["operation_id"],
                   "claim_token": granted["request"]["claim_token"], "receipt_id": "first-timeout",
                   "status": "unknown", "evidence": {"tool_result_id": "fixture-timeout"}}
        self.pools.operate(run_id, "result", unknown)
        self.pools.operate(run_id, "result", {**unknown, "receipt_id": "later-read-back", "status": "completed",
            "artifact_path": str(self.image), "evidence": {"tool_result_id": "fixture-existing-image"}})

        # Simulate an out-of-order redelivery after the dispatcher restarts.
        restarted = PoolService(Production(Store(self.db), self.root / "work",
                                          self.production.project, clock=lambda: self.now))
        replay = restarted.operate(run_id, "result", unknown)
        self.assertTrue(replay["duplicate"])
        self.assertEqual(replay["status"], "completed")
        run = self.store.get(run_id)
        self.assertEqual(run["pool"]["backend"]["requests"][request["operation_id"]]["status"], "completed")
        with self.store.transaction() as tx:
            self.assertEqual(tx.operation(granted["operation"]["key"])["status"], "confirmed")
            self.assertEqual(tx.execute("SELECT state FROM runtime_slots WHERE id=?",
                                       (granted["operation"]["key"],)).fetchone()[0], "released")

    def test_old_failed_receipt_cannot_settle_a_new_task_generation(self):
        run_id, request = self.make_run(capacity=1, count=1, billing="metered")
        first = self.claim(run_id, request, estimated_units=3)
        failed = {"operation_id": request["operation_id"], "claim_token": first["request"]["claim_token"],
                  "receipt_id": "first-failure", "status": "failed", "actual_units": 2,
                  "detail": "observed provider failure", "evidence": {"tool_result_id": "fixture-failure"}}
        self.pools.operate(run_id, "result", failed)
        self.production.revise(run_id, "image:s0", "retry the known failed image")
        self.pools.operate(run_id, "enqueue", {"task_ids": ["image:s0"]})
        pending = self.pools.operate(run_id, "tick")["pending"]
        second = self.claim(run_id, pending[0], estimated_units=4)
        self.assertNotEqual(first["task_claim"]["input_hash"], second["task_claim"]["input_hash"])

        self.assertTrue(self.pools.operate(run_id, "result", failed)["duplicate"])
        with self.assertRaises(Conflict):
            self.pools.operate(run_id, "result", {**failed, "actual_units": 4})
        with self.assertRaises(ValueError):
            self.pools.operate(run_id, "result", {**failed, "receipt_id": "different-late-failure"})
        run = self.store.get(run_id)
        self.assertEqual(run["tasks"]["image:s0"]["status"], "running")
        self.assertEqual(run["tasks"]["image:s0"]["claim"]["token"], second["task_claim"]["token"])
        self.assertEqual((run["budget"]["spent"], run["budget"]["reserved"], run["budget"]["unknown_reserved"]),
                         (2, 4, 0))
        with self.store.transaction() as tx:
            self.assertEqual(tx.operation(second["operation"]["key"])["status"], "dispatched")
            self.assertEqual(tx.execute("SELECT state FROM runtime_slots WHERE id=?",
                                       (second["operation"]["key"],)).fetchone()[0], "reserved")

    def test_stale_expected_version_is_rejected(self):
        run_id, _ = self.make_run()
        before = self.store.get(run_id)["version"]
        self.pools.operate(run_id, "tick", expected_version=before)
        with self.assertRaises(Conflict):
            self.pools.operate(run_id, "tick", expected_version=before)

    def test_cancelled_run_cannot_issue_dispatch_grant(self):
        run_id, request = self.make_run()
        self.production.cancel(run_id, "cancel the fixture")
        with self.assertRaises(Conflict):
            self.claim(run_id, request)
        with self.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM runtime_slots").fetchone()[0], 0)

    def test_cancel_queued_scene_removes_outbox_and_prevents_task_dispatch(self):
        run_id, request = self.make_run()
        result = self.pools.operate(run_id, "cancel", {"job_id": request["packet"]["job_id"]})
        self.assertEqual(result["status"], "cancelled")
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "cancelled")
        self.assertEqual(self.pools.operate(run_id, "pending")["requests"], [])

    def test_cancel_old_review_job_cannot_cancel_revised_task(self):
        run_id, request = self.make_run(count=1)
        granted = self.claim(run_id, request)
        self.native_complete(run_id, granted)
        self.qa_complete(run_id, "image:s0", granted["task_claim"])
        self.production.revise(run_id, "image:s0", "change the image before enqueuing its replacement")
        revised = self.store.get(run_id)["tasks"]["image:s0"]
        self.assertEqual(revised["status"], "pending")
        self.pools.operate(run_id, "cancel", {"job_id": request["packet"]["job_id"]})
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"], revised)
        self.pools.operate(run_id, "enqueue")
        pending = self.pools.operate(run_id, "tick")["pending"]
        self.assertNotEqual(pending[0]["packet"]["job_id"], request["packet"]["job_id"])

    def test_cancel_inflight_keeps_slot_until_observation_then_settles_cost(self):
        run_id, request = self.make_run(capacity=1, billing="metered")
        granted = self.claim(run_id, request, estimated_units=3)
        self.pools.operate(run_id, "cancel", {"job_id": request["packet"]["job_id"]})
        with self.assertRaises(Conflict):
            self.production.revise(run_id, "image:s0", "cannot abandon an outstanding native claim")
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["claim"]["token"],
                         granted["task_claim"]["token"])
        with self.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM runtime_slots WHERE state='reserved'").fetchone()[0], 1)
        self.native_complete(run_id, granted)
        run = self.store.get(run_id)
        self.assertEqual(run["tasks"]["image:s0"]["status"], "cancelled")
        self.assertEqual(run["budget"]["reserved"], 0)
        self.assertEqual(run["budget"]["unknown_reserved"], 3)
        with self.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM runtime_slots WHERE state='reserved'").fetchone()[0], 0)
        self.production.revise(run_id, "image:s0", "native work finished; a new version is safe")
        revised = self.store.get(run_id)["tasks"]["image:s0"]
        self.assertEqual(revised["status"], "pending")
        self.assertIsNone(revised["claim"])

    def test_licensed_recipe_enqueues_only_thumbnail_generation(self):
        profile_path = self.production.project / "channels" / "test_channel" / "channel.json"
        profile = json.loads(profile_path.read_text())
        profile["recipe"] = "licensed_clips"
        profile_path.write_text(json.dumps(profile))
        run_id, request = self.make_run(count=1)
        self.assertIsNone(request)
        self.assertEqual(self.pools.operate(run_id, "enqueue")["jobs"], [])
        with self.assertRaises(WorkflowError):
            self.pools.operate(run_id, "enqueue", {"task_ids": ["image:s0"]})

        # A previously accepted packaging brief is a fixture input, like the
        # accepted script/storyboard above. Thumbnail planning/dispatch are real.
        brief = self.root / "packaging-fixture.json"
        brief.write_text(json.dumps({"title": "Synthetic thumbnail brief"}))
        artifact = self.production.artifacts.put(brief, "release_spec")
        def prepared_packaging(tx, run):
            run["artifacts"][artifact["id"]] = artifact
            run["tasks"]["packaging"].update(status="complete", outputs=[artifact["id"]])
        self.store.mutate(run_id, prepared_packaging)
        task = self.production.add_thumbnail_task(run_id, {
            "id": "cover", "prompt": "Synthetic cover image", "visual_intent": "fixture test"})
        jobs = self.pools.operate(run_id, "enqueue")["jobs"]
        self.assertEqual(len(jobs), 1)
        pending = self.pools.operate(run_id, "tick")["pending"]
        self.assertEqual(pending[0]["packet"]["context"]["task_id"], task["id"])
        granted = self.claim(run_id, pending[0])
        self.assertEqual(granted["request"]["packet"]["context"]["scene"]["purpose"], "thumbnail")
        self.assertEqual(self.store.get(run_id)["tasks"]["image:s0"]["status"], "pending")

    def test_exhausted_candidate_does_not_starve_another_channel(self):
        exhausted, request = self.make_run(capacity=1, channel="a_exhausted")
        healthy, healthy_request = self.make_run(capacity=1, channel="b_healthy")
        def exhaust(tx, run):
            run["tasks"]["image:s0"]["attempt"] = run["budget"]["max_task_attempts"]
        self.store.mutate(exhausted, exhaust)
        self.assertEqual(self.pools.candidates("fixture-runtime")["candidates"][0]["run_id"], healthy)
        self.assertTrue(self.claim(healthy, healthy_request)["task_claim"]["token"])
        with self.assertRaises(WorkflowError):
            self.claim(exhausted, request)

    def test_cancel_after_completed_result_settles_outstanding_claim(self):
        for actual_units in (None, 2):
            with self.subTest(actual_units=actual_units):
                run_id, request = self.make_run(capacity=1, count=1, billing="metered")
                granted = self.claim(run_id, request, estimated_units=3)
                result = {"operation_id": request["operation_id"],
                    "claim_token": granted["request"]["claim_token"], "receipt_id": "ready-before-cancel",
                    "status": "completed", "artifact_path": str(self.image), "actual_units": actual_units,
                    "evidence": {"tool_result_id": "existing-image"}}
                self.pools.operate(run_id, "result", result)
                cancel = {"job_id": request["packet"]["job_id"]}
                self.pools.operate(run_id, "cancel", cancel)
                self.pools.operate(run_id, "cancel", cancel)
                self.assertTrue(self.pools.operate(run_id, "result", result)["duplicate"])
                run = self.store.get(run_id)
                self.assertEqual(run["tasks"]["image:s0"]["status"], "cancelled")
                self.assertIsNone(run["tasks"]["image:s0"]["claim"])
                self.assertEqual((run["budget"]["reserved"], run["budget"]["spent"], run["budget"]["unknown_reserved"]),
                                 (0, actual_units or 0, 3 if actual_units is None else 0))
                self.production.revise(run_id, "image:s0", "replace the finished cancelled result")

    def test_concurrent_cancel_and_result_settle_once(self):
        run_id, request = self.make_run(capacity=1, count=1, billing="metered")
        granted = self.claim(run_id, request, estimated_units=3)
        barrier = threading.Barrier(2)
        def finish(action):
            barrier.wait(timeout=5)
            payload = ({"job_id": request["packet"]["job_id"]} if action == "cancel" else {
                "operation_id": request["operation_id"], "claim_token": granted["request"]["claim_token"],
                "receipt_id": "concurrent-finished", "status": "completed", "artifact_path": str(self.image),
                "actual_units": 2, "evidence": {"tool_result_id": "concurrent-fixture"}})
            return self.pools.operate(run_id, action, payload)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            list(executor.map(finish, ["cancel", "result"]))
        run = self.store.get(run_id)
        self.assertEqual(run["tasks"]["image:s0"]["status"], "cancelled")
        self.assertIsNone(run["tasks"]["image:s0"]["claim"])
        self.assertEqual((run["budget"]["reserved"], run["budget"]["spent"], run["budget"]["unknown_reserved"]), (0, 2, 0))
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 0)

    def test_removed_unknown_scene_with_confirmed_result_recovers_as_stale(self):
        run_id, request = self.make_run(capacity=1, count=1)
        granted = self.claim(run_id, request)
        self.pools.operate(run_id, "recover")
        with self.assertRaises(Conflict):
            self.production.revise(run_id, "storyboard", "an unresolved native call cannot be removed")
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)
        self.pools.operate(run_id, "result", {"operation_id": request["operation_id"],
            "claim_token": granted["request"]["claim_token"], "receipt_id": "recovered-completed-image",
            "status": "completed", "artifact_path": str(self.image), "evidence": {"tool_readback": "existing image"}})
        recovered = self.production.reconcile_task(run_id, "image:s0", worker="reconciler", outcome="completed",
                                                     evidence="native read-back of the already generated image")
        self.qa_complete(run_id, "image:s0", recovered)
        self.production.revise(run_id, "storyboard", "replace the scene list after production reconciliation")
        # The task is gone, while the scheduler still needs to consume the
        # already confirmed result. Real unknown outcomes must keep their slot.
        result = self.pools.operate(run_id, "recover")
        self.assertEqual(result["jobs"][0]["status"], "stale")
        self.assertEqual(result["pending"], [])
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 0)
        other, pending = self.make_run(capacity=1, count=1)
        self.assertTrue(self.claim(other, pending)["task_claim"]["token"])

    def test_removed_scene_does_not_block_recovery_or_replacement(self):
        run_id, request = self.make_run(capacity=1, count=1)
        self.production.revise(run_id, "storyboard", "replace the scene list before any native dispatch")
        self.now += 1000
        self.pools.operate(run_id, "recover")
        board = self.root / "replacement-board.json"
        board.write_text(json.dumps({"scenes": [{"id": "replacement", "prompt": "New fixture", "visual_intent": "test"}]}))
        artifact = self.production.artifacts.put(board, "storyboard")
        def replace(tx, run):
            run["artifacts"][artifact["id"]] = artifact
            run["tasks"]["storyboard"].update(status="complete", outputs=[artifact["id"]])
            self.production._expand_scenes(run, artifact)
        self.store.mutate(run_id, replace)
        self.pools.operate(run_id, "enqueue")
        pending = self.pools.operate(run_id, "tick")["pending"]
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]["packet"]["context"]["task_id"], "image:replacement")
        self.assertTrue(self.claim(run_id, pending[0])["task_claim"]["token"])
        with self.assertRaises((Conflict, WorkflowError)):
            self.claim(run_id, request)

    def test_not_started_reconciliation_allows_only_new_generation(self):
        run_id, request = self.make_run(capacity=1, count=1, billing="metered")
        granted = self.claim(run_id, request, estimated_units=3)
        self.pools.operate(run_id, "recover")
        observed = {"operation_id": request["operation_id"], "claim_token": granted["request"]["claim_token"],
            "receipt_id": "confirmed-no-dispatch", "status": "not_started", "detail": "dispatcher did not invoke tool",
            "evidence": {"dispatcher_readback": "fixture request absent"}}
        self.pools.operate(run_id, "result", observed)
        self.pools.operate(run_id, "reconcile", {"job_id": request["packet"]["job_id"]})
        self.production.reconcile_task(run_id, "image:s0", worker="reconciler", outcome="not_performed",
                                       evidence="dispatcher did not invoke the native tool")
        self.pools.operate(run_id, "enqueue")
        replacement = self.pools.operate(run_id, "tick")["pending"][0]
        retry = self.claim(run_id, replacement, estimated_units=3)
        self.assertNotEqual(retry["operation"]["key"], granted["operation"]["key"])
        self.assertTrue(self.pools.operate(run_id, "result", observed)["duplicate"])
        self.assertEqual(self.store.get(run_id)["budget"]["reserved"], 3)
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)

    def test_qa_cannot_complete_before_native_result_confirmation(self):
        run_id, request = self.make_run(capacity=1, count=1)
        granted = self.claim(run_id, request)
        with self.assertRaises(WorkflowError):
            self.qa_complete(run_id, "image:s0", granted["task_claim"])
        run = self.store.get(run_id)
        self.assertEqual(run["tasks"]["image:s0"]["status"], "running")
        with self.assertRaises(Conflict):
            self.production.revise(run_id, "image:s0", "provider outcome is still unknown")
        self.native_complete(run_id, granted)
        # A different valid image must not be attached while the native result
        # and its global session accounting refer to the original exact file.
        from PIL import Image
        original = self.image.read_bytes()
        Image.new("RGB", (2, 2), "blue").save(self.image)
        with self.assertRaises(Conflict):
            self.qa_complete(run_id, "image:s0", granted["task_claim"])
        self.image.write_bytes(original)
        self.qa_complete(run_id, "image:s0", granted["task_claim"])

    def test_concurrent_duplicate_claims_grant_exactly_once(self):
        run_id, request = self.make_run(capacity=2, count=1, billing="metered")
        barrier = threading.Barrier(6)
        def attempt(_):
            barrier.wait(timeout=5)
            try:
                return self.claim(run_id, request, estimated_units=3)
            except Conflict:
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            results = list(executor.map(attempt, range(6)))
        self.assertEqual(sum(result is not None for result in results), 1)
        run = self.store.get(run_id)
        self.assertEqual((run["tasks"]["image:s0"]["attempt"], run["budget"]["reserved"]), (1, 3))
        with self.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM runtime_slots WHERE state='reserved'").fetchone()[0], 1)
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM operations WHERE run_id=?", (run_id,)).fetchone()[0], 1)

    def test_concurrent_result_and_other_run_claim_do_not_deadlock_or_overbook(self):
        first, first_request = self.make_run(capacity=1, count=1)
        second, second_request = self.make_run(capacity=1, count=1)
        granted = self.claim(first, first_request)
        barrier = threading.Barrier(2)
        def finish():
            barrier.wait(timeout=5)
            return self.native_complete(first, granted)
        def claim_other():
            barrier.wait(timeout=5)
            try:
                return self.claim(second, second_request)
            except Conflict:
                return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            finished = executor.submit(finish)
            claimed = executor.submit(claim_other)
            finished.result(timeout=15)
            second_grant = claimed.result(timeout=15)
        if second_grant is None:
            second_grant = self.claim(second, second_request)
        self.assertTrue(second_grant["task_claim"]["token"])
        self.assertEqual(self.pools.candidates("fixture-runtime")["active"], 1)

    def test_budget_rejection_does_not_claim_bridge_or_slot(self):
        run_id, request = self.make_run(billing="metered")
        with self.assertRaises(WorkflowError):
            self.claim(run_id, request, estimated_units=25)
        self.assertEqual(len(self.pools.operate(run_id, "pending")["requests"]), 1)
        self.assertEqual(self.store.get(run_id)["budget"]["reserved"], 0)
        with self.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM runtime_slots").fetchone()[0], 0)

    def test_review_credit_applies_until_verified_task_acceptance(self):
        run_id, request = self.make_run(capacity=1, review_capacity=1)
        granted = self.claim(run_id, request)
        self.native_complete(run_id, granted)
        self.assertEqual(self.pools.operate(run_id, "pending")["requests"], [])
        self.qa_complete(run_id, "image:s0", granted["task_claim"])
        self.pools.operate(run_id, "accept", {"job_id": request["packet"]["job_id"],
            "review_id": "accepted", "service_seconds": 4})
        self.assertEqual(len(self.pools.operate(run_id, "tick")["pending"]), 1)


@unittest.skipUnless(os.environ.get("YTV_TEST_POSTGRES_URL"), "set YTV_TEST_POSTGRES_URL for real PostgreSQL pools")
class PostgresPoolServiceTests(PoolServiceTests):
    postgres = True


if __name__ == "__main__":
    unittest.main()
