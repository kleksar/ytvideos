import copy
import hashlib
import unittest

from ytvideos.workers import (
    AdaptivePool, BackendCapabilities, BackendResult, BeforeSendError,
    PoolConfig, SceneJob, Submission,
)
from ytvideos.workers.bridge import ToolBridgeBackend


ARTIFACT_HASH = hashlib.sha256(b"actual test image bytes").hexdigest()


class Clock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now

    def advance(self, seconds):
        self.now += seconds


class FakeBackend:
    def __init__(self, *, limit=6, reset=False, durable=True):
        self.capabilities = BackendCapabilities("test", limit, reset, durable)
        self.submissions, self.closed, self.resets = [], [], []
        self.results, self.reconciled = {}, {}
        self.errors = []

    def submit(self, packet, *, session_id):
        self.submissions.append((copy.deepcopy(packet), session_id))
        if self.errors:
            raise self.errors.pop(0)
        handle = Submission(packet["job_id"], session_id or f"session-{len(self.submissions)}")
        self.results[handle.operation_id] = BackendResult("pending")
        packet["context"]["adapter_mutation"] = True
        return handle

    def poll(self, handle):
        return self.results[handle.operation_id]

    def reconcile(self, job_id, handle):
        return self.reconciled.get(job_id, BackendResult("unknown"))

    def reset(self, session_id):
        self.resets.append(session_id)

    def close(self, session_id):
        self.closed.append(session_id)

    def complete(self, job_id):
        self.results[job_id] = BackendResult("completed", "artifact://" + job_id, ARTIFACT_HASH)


def job(number, *, channel="paper", scene=None, revision="r1", context=None):
    return SceneJob.create(job_id=f"job-{number}", run_id=f"run-{channel}", channel_id=channel,
                           scene_id=scene or f"scene-{number}", revision=revision,
                           context=context or {"prompt": f"scene {number}", "style_hash": "profile-a"})


class PoolTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.backend = FakeBackend()
        self.saved = []
        self.pool = AdaptivePool(self.backend, PoolConfig(review_capacity=8, lease_seconds=500),
                                 checkpoint=lambda s: self.saved.append(s), clock=self.clock)

    def accept(self, number, *, seconds=10, review_id=None):
        record = self.pool.records[f"job-{number}"]
        self.pool.accept(record.job.job_id, revision=record.job.revision, input_hash=record.job.input_hash,
                         artifact_hash=record.artifact_hash, review_id=review_id or f"review-{number}",
                         service_seconds=seconds)

    def test_immutable_packet_and_conflicting_id(self):
        context = {"prompt": "one", "nested": [1]}
        first = job(1, context=context)
        context["nested"].append(2)
        self.pool.enqueue(first)
        self.pool.tick()
        self.assertEqual(first.packet()["context"], {"prompt": "one", "nested": [1]})
        self.pool.enqueue(first)
        with self.assertRaises(ValueError):
            self.pool.enqueue(job(1, context={"prompt": "different"}))

    def test_default_single_slot_and_checkpoint_before_submit(self):
        self.pool.enqueue(job(1))
        self.pool.enqueue(job(2))
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 1)
        submitting = [s for s in self.saved if any(r["status"] == "submitting" for r in s["records"])]
        self.assertTrue(submitting)
        self.assertIsNone(submitting[0]["records"][0]["handle"])

    def test_second_job_starts_while_first_is_still_generating(self):
        for n in range(5):
            self.pool.enqueue(job(n))
        self.pool.tick()
        self.clock.advance(5)
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 2)
        self.assertEqual(self.pool.records["job-0"].status, "running")
        self.assertIsNone(self.pool.generation_ewma)
        for _ in range(30):
            self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 2)  # Poll frequency cannot force growth.

    def test_startup_obeys_review_credits_and_coordinator_load(self):
        self.pool = AdaptivePool(self.backend, PoolConfig(review_capacity=2), checkpoint=lambda s: None, clock=self.clock)
        for n in range(6):
            self.pool.enqueue(job(n))
        self.pool.tick()
        self.clock.advance(10)
        self.pool.tick(coordinator_idle=False)
        self.assertEqual(len(self.backend.submissions), 1)
        self.pool.tick()
        for _ in range(5):
            self.clock.advance(10)
            self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 2)
        self.backend.complete("job-0")
        self.pool.tick()
        self.clock.advance(10)
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 2)

    def test_startup_uses_observed_dispatch_service_interval(self):
        self.pool.observe_dispatch_service(12)
        self.pool.enqueue(job(1))
        self.pool.enqueue(job(2))
        self.pool.tick()
        self.clock.advance(6)
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 1)
        self.clock.advance(6)
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 2)

    def test_ready_slot_refills_without_batch_barrier(self):
        self.pool.target = 2
        for n in range(1, 4):
            self.pool.enqueue(job(n))
        self.pool.tick()
        self.clock.advance(30)
        self.backend.complete("job-2")
        self.pool.tick()
        self.assertEqual([r.status for r in self.pool.records.values()], ["running", "review", "running"])
        self.assertEqual(len(self.backend.submissions), 3)

    def test_backpressure_counts_review_and_inflight(self):
        self.pool = AdaptivePool(self.backend, PoolConfig(review_capacity=2), checkpoint=lambda s: None, clock=self.clock)
        self.pool.target = 5
        for n in range(1, 6):
            self.pool.enqueue(job(n))
        self.pool.tick()
        self.backend.complete("job-1")
        self.backend.complete("job-2")
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 2)
        self.accept(1)
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 3)

    def test_ramps_one_slot_and_stops_at_service_capacity(self):
        # Generation takes 50 s, coordinator takes 10 s: no reason to add a sixth worker.
        for n in range(1, 13):
            self.pool.enqueue(job(n))
            self.pool.tick()
            self.clock.advance(50)
            self.backend.complete(f"job-{n}")
            self.pool.tick()
            self.accept(n)
        self.assertEqual(self.pool.target, 5)
        self.assertEqual(self.pool.generation_ewma, 50)
        self.assertEqual(self.pool.service_ewma, 10)

    def test_provider_bound_is_enforced_even_with_large_target(self):
        self.backend.capabilities = BackendCapabilities("test", 2)
        self.pool.target = 99
        for n in range(10):
            self.pool.enqueue(job(n))
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 2)
        with self.assertRaises(ValueError):
            BackendCapabilities("test", 0)

    def test_round_robin_channels_does_not_starve_later_channel(self):
        for n in range(5):
            self.pool.enqueue(job(n))
        self.pool.enqueue(job(99, channel="films"))
        self.pool.target = 2
        self.pool.tick()
        self.assertEqual([p[0]["channel_id"] for p in self.backend.submissions], ["paper", "films"])

    def test_fresh_session_unless_reset_is_explicitly_supported(self):
        self.pool.enqueue(job(1))
        self.pool.enqueue(job(2))
        self.pool.tick()
        self.backend.complete("job-1")
        self.pool.tick()
        self.assertEqual([p[1] for p in self.backend.submissions], [None, None])
        self.assertEqual(self.backend.closed, ["session-1"])
        self.assertEqual(self.backend.resets, [])

    def test_supported_reset_precedes_session_reuse(self):
        self.backend.capabilities = BackendCapabilities("test", 6, supports_reset=True)
        self.pool.enqueue(job(1))
        self.pool.enqueue(job(2))
        self.pool.tick()
        self.backend.complete("job-1")
        self.pool.tick()
        self.assertEqual(self.backend.resets, ["session-1"])
        self.assertEqual(self.backend.submissions[1][1], "session-1")

    def test_unknown_submit_never_retries_or_frees_capacity(self):
        self.backend.errors.append(TimeoutError("response lost after send"))
        self.pool.enqueue(job(1))
        self.pool.enqueue(job(2))
        self.pool.tick()
        for _ in range(3):
            self.pool.tick()
        self.assertEqual(self.pool.records["job-1"].status, "unknown")
        self.assertEqual(len(self.backend.submissions), 1)
        self.backend.reconciled["job-1"] = BackendResult("not_started", detail="provider lookup confirmed absence")
        self.pool.reconcile("job-1")
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 2)

    def test_only_verified_before_send_error_retries_with_cooldown_and_bound(self):
        self.backend.errors = [BeforeSendError("local rate limiter", retry_after=5)] * 3
        self.pool.enqueue(job(1))
        self.pool.tick()
        self.pool.tick()
        self.assertEqual(len(self.backend.submissions), 1)
        self.clock.advance(5)
        self.pool.tick()
        self.clock.advance(5)
        self.pool.tick()
        self.assertEqual(self.pool.records["job-1"].status, "failed")
        self.assertEqual(len(self.backend.submissions), 3)

    def test_review_targets_exact_artifact_and_deduplicates(self):
        self.pool.enqueue(job(1))
        self.pool.tick()
        self.backend.complete("job-1")
        self.pool.tick()
        record = self.pool.records["job-1"]
        with self.assertRaises(ValueError):
            self.pool.accept("job-1", revision="r1", input_hash=record.job.input_hash,
                             artifact_hash="f" * 64, review_id="bad", service_seconds=10)
        self.accept(1)
        self.accept(1)
        self.assertEqual(self.pool.reviews_since_adjust, 1)
        with self.assertRaises(ValueError):
            self.pool.accept("job-1", revision="r1", input_hash=record.job.input_hash,
                             artifact_hash=ARTIFACT_HASH, review_id="review-1", service_seconds=10, accepted=False)

    def test_late_result_for_old_revision_is_stale(self):
        first, changed = job(1, scene="s"), job(2, scene="s", revision="r2")
        self.pool.enqueue(first)
        self.pool.tick()
        self.pool.set_current_revision(changed.run_id, changed.scene_id, changed.revision, changed.input_hash)
        self.pool.enqueue(changed)
        self.backend.complete("job-1")
        self.pool.tick()
        self.assertEqual(self.pool.records["job-1"].status, "stale")
        with self.assertRaises(ValueError):
            self.accept(1)
        self.assertEqual(self.pool.records["job-2"].status, "running")

    def test_cancel_inflight_collects_but_never_accepts_result(self):
        self.pool.enqueue(job(1))
        self.pool.tick()
        self.pool.cancel("job-1")
        self.assertEqual(self.pool.records["job-1"].status, "running")
        self.backend.complete("job-1")
        self.pool.tick()
        self.assertEqual(self.pool.records["job-1"].status, "cancelled")
        with self.assertRaises(ValueError):
            self.accept(1)

    def test_expired_lease_requires_reconciliation(self):
        self.pool.enqueue(job(1))
        self.pool.tick()
        self.clock.advance(501)
        self.pool.tick()
        self.assertEqual(self.pool.records["job-1"].status, "unknown")
        self.assertEqual(len(self.backend.submissions), 1)

    def test_restart_durable_job_does_not_resubmit(self):
        self.pool.enqueue(job(1))
        self.pool.tick()
        recovered = AdaptivePool.restore(self.backend, self.pool.snapshot(), checkpoint=lambda s: None, clock=self.clock)
        recovered.tick()
        self.assertEqual(len(self.backend.submissions), 1)
        self.backend.complete("job-1")
        recovered.tick()
        self.assertEqual(recovered.records["job-1"].status, "review")

    def test_restart_gap_and_nondurable_handle_become_unknown(self):
        self.pool.enqueue(job(1))
        self.pool.tick()
        intent = next(s for s in self.saved if s["records"][0]["status"] == "submitting")
        recovered = AdaptivePool.restore(self.backend, intent, checkpoint=lambda s: None, clock=self.clock)
        recovered.tick()
        self.assertEqual(recovered.records["job-1"].status, "unknown")
        self.backend.capabilities = BackendCapabilities("test", 6, durable_handles=False)
        recovered = AdaptivePool.restore(self.backend, self.pool.snapshot(), checkpoint=lambda s: None, clock=self.clock)
        self.assertEqual(recovered.records["job-1"].status, "unknown")
        self.assertEqual(len(self.backend.submissions), 1)

    def test_failed_checkpoint_does_not_submit(self):
        self.pool.enqueue(job(1))
        self.pool.checkpoint = lambda snapshot: (_ for _ in ()).throw(RuntimeError("lost DB lease"))
        with self.assertRaises(RuntimeError):
            self.pool.tick()
        self.assertEqual(self.backend.submissions, [])


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.clock, self.saved = Clock(), []
        self.bridge = ToolBridgeBackend(max_sessions=3, checkpoint=self.saved.append, clock=self.clock)
        self.handle = self.bridge.submit(job(1).packet(), session_id=None)

    def claim(self):
        return self.bridge.claim(self.handle.operation_id, owner="coordinator")

    def test_local_handle_is_outbox_only_and_claim_is_persisted(self):
        self.assertTrue(self.handle.operation_id.startswith("bridge-"))
        self.assertEqual(self.bridge.poll(self.handle).status, "pending")
        self.assertEqual(len(self.bridge.pending_requests()), 1)
        claimed = self.claim()
        self.assertEqual(self.saved[-1]["requests"][self.handle.operation_id]["claim_token"], claimed["claim_token"])
        with self.assertRaises(ValueError):
            self.claim()

    def test_completion_evidence_is_idempotent(self):
        claimed = self.claim()
        self.bridge.record_submission(self.handle.operation_id, claim_token=claimed["claim_token"],
                                      provider={"tool": "native-agent", "session_id": "observed-123"})
        kwargs = dict(claim_token=claimed["claim_token"], receipt_id="tool-result-1",
                      result=BackendResult("completed", "artifact://image", ARTIFACT_HASH),
                      evidence={"tool_result_id": "actual-1"})
        self.bridge.record_observation(self.handle.operation_id, **kwargs)
        self.bridge.record_observation(self.handle.operation_id, **kwargs)
        self.assertEqual(self.bridge.poll(self.handle).status, "completed")
        self.assertEqual(len(self.bridge.receipts), 1)

    def test_restart_unknown_native_call_is_not_redispatched(self):
        claimed = self.claim()
        self.bridge.record_submission(self.handle.operation_id, claim_token=claimed["claim_token"],
                                      provider={"tool": "native-agent", "session_id": "observed-123"})
        restored = ToolBridgeBackend.restore(self.bridge.snapshot(), max_sessions=3,
                                             checkpoint=lambda s: None, clock=self.clock)
        self.assertEqual(restored.poll(self.handle).status, "unknown")
        self.assertEqual(restored.pending_requests(), [])
        with self.assertRaises(ValueError):
            restored.claim(self.handle.operation_id, owner="new-coordinator")

    def test_expired_dispatch_and_stale_token(self):
        claimed = self.claim()
        self.clock.advance(301)
        self.assertEqual(self.bridge.poll(self.handle).status, "unknown")
        with self.assertRaises(ValueError):
            self.bridge.record_observation(self.handle.operation_id, claim_token="old-token", receipt_id="x",
                                           result=BackendResult("failed"), evidence={"observed": "failure"})
        self.bridge.record_observation(self.handle.operation_id, claim_token=claimed["claim_token"], receipt_id="read-back",
                                       result=BackendResult("not_started", detail="native tool confirmed no task"),
                                       evidence={"read_back": "not created"})
        self.assertEqual(self.bridge.reconcile("job-1", self.handle).status, "not_started")

    def test_pool_and_bridge_restart_preserves_queued_request(self):
        pool = AdaptivePool(self.bridge, PoolConfig(review_capacity=3), checkpoint=lambda s: None, clock=self.clock)
        pool.enqueue(job(1))
        pool.tick()
        backend_snapshot, pool_snapshot = self.bridge.snapshot(), pool.snapshot()
        restored_backend = ToolBridgeBackend.restore(backend_snapshot, max_sessions=3,
                                                      checkpoint=lambda s: None, clock=self.clock)
        restored_pool = AdaptivePool.restore(restored_backend, pool_snapshot,
                                             checkpoint=lambda s: None, clock=self.clock)
        restored_pool.tick()
        self.assertEqual(len(restored_backend.pending_requests()), 1)
        self.assertEqual(len(restored_backend.requests), 1)

    def test_cancel_before_native_dispatch_removes_pending_request(self):
        pool = AdaptivePool(self.bridge, PoolConfig(review_capacity=3), checkpoint=lambda s: None, clock=self.clock)
        pool.enqueue(job(1))
        pool.tick()
        pool.cancel("job-1")
        self.assertEqual(self.bridge.pending_requests(), [])
        self.assertEqual(pool.records["job-1"].status, "cancelled")


if __name__ == "__main__":
    unittest.main()
