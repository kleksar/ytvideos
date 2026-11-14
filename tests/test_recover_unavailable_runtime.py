"""Recovery preserves early episodes and rejects uncertain provider state."""

import json
import unittest

import test_pool_service
from ytvideos.errors import Conflict
from ytvideos.recover_unavailable_runtime import apply_recovery, plan_recovery


class UnavailableRuntimeRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_pool_service.PoolServiceTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.service = self.fixture.production
        self.store = self.fixture.store
        self.run = self.service.create("test_channel", "synthetic recovery")
        self.run_id = self.run["id"]
        (self.service.project / "src/ytvideos/pin.py").write_text("# changed target\n")

    def test_preserves_pending_approval_and_archives_unverified_source(self):
        before = self.store.get(self.run_id)
        plan = plan_recovery(self.service, self.run_id, expected_version=before["version"])
        self.assertEqual(plan["source"]["code_checkout"], "unavailable_unverified")
        result = apply_recovery(self.service, self.run_id, plan,
                                source="fixture-message", message="Recover this episode.")
        after = self.store.get(self.run_id)
        snapshot = json.loads(self.service.artifacts.resolve(result["snapshot"]).read_text())
        self.assertEqual(snapshot["run"], before)
        self.assertEqual(after["approvals"], before["approvals"])
        self.assertEqual(after["profile"], before["profile"])
        self.assertEqual(after["budget"], before["budget"])
        self.service._runtime(after)

    def test_rejects_saved_provider_operation(self):
        def add(tx, run):
            tx.create_operation({"key": "synthetic", "run_id": self.run_id, "kind": "image",
                                 "input_hash": "a" * 64, "status": "confirmed"})
        self.store.mutate(self.run_id, add)
        with self.assertRaisesRegex(Conflict, "no provider operations"):
            plan_recovery(self.service, self.run_id, expected_version=self.store.get(self.run_id)["version"])

    def test_rejects_stale_plan(self):
        plan = plan_recovery(self.service, self.run_id, expected_version=self.store.get(self.run_id)["version"])
        self.store.mutate(self.run_id, lambda tx, run: run.update(intent="changed after planning"))
        with self.assertRaises(Conflict):
            apply_recovery(self.service, self.run_id, plan, source="fixture-message", message="Recover.")
