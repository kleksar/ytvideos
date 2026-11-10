import concurrent.futures
import json
from pathlib import Path
import struct
import tempfile
import unittest
import zlib

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
        self.store = Store(self.root / "state.db")
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
        return run["id"], result["pending"][0]

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
        def attempt(pair):
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

    def test_cancel_inflight_keeps_slot_until_observation_then_settles_cost(self):
        run_id, request = self.make_run(capacity=1, billing="metered")
        granted = self.claim(run_id, request, estimated_units=3)
        self.pools.operate(run_id, "cancel", {"job_id": request["packet"]["job_id"]})
        with self.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM runtime_slots WHERE state='reserved'").fetchone()[0], 1)
        self.native_complete(run_id, granted)
        run = self.store.get(run_id)
        self.assertEqual(run["tasks"]["image:s0"]["status"], "cancelled")
        self.assertEqual(run["budget"]["reserved"], 0)
        self.assertEqual(run["budget"]["unknown_reserved"], 3)
        with self.store.transaction() as tx:
            self.assertEqual(tx.execute("SELECT COUNT(*) FROM runtime_slots WHERE state='reserved'").fetchone()[0], 0)

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


if __name__ == "__main__":
    unittest.main()
