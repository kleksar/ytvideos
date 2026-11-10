"""A bounded, checkpointed queue; backend calls must return without waiting for media.

One owner holds the application's lease for a pool. Checkpoint must atomically save
the snapshot using that lease's fencing token BEFORE an external submission.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import math
import time
from typing import Callable, Protocol


def _json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SceneJob:
    job_id: str
    run_id: str
    channel_id: str
    scene_id: str
    revision: str
    input_hash: str
    context_json: str

    def __post_init__(self) -> None:
        if not all((self.job_id, self.run_id, self.channel_id, self.scene_id, self.revision)):
            raise ValueError("job, run, channel, scene and revision are required")
        if not isinstance(json.loads(self.context_json), dict) or _hash(self.context_json) != self.input_hash:
            raise ValueError("context must be a JSON object matching input_hash")

    @classmethod
    def create(cls, *, job_id: str, run_id: str, channel_id: str, scene_id: str,
               revision: str, context: dict) -> SceneJob:
        frozen = _json(context)
        return cls(job_id, run_id, channel_id, scene_id, revision, _hash(frozen), frozen)

    @property
    def scene_key(self) -> str:
        return _json([self.run_id, self.scene_id])

    def packet(self) -> dict:
        # Every dispatch receives a fresh object, without another job's history.
        return {"job_id": self.job_id, "run_id": self.run_id, "channel_id": self.channel_id,
                "scene_id": self.scene_id, "revision": self.revision,
                "input_hash": self.input_hash, "context": json.loads(self.context_json)}


@dataclass(frozen=True)
class BackendCapabilities:
    backend_id: str
    max_sessions: int  # Verified runtime/provider limit after reserving the coordinator.
    supports_reset: bool = False
    durable_handles: bool = False

    def __post_init__(self) -> None:
        if not self.backend_id or self.max_sessions < 1:
            raise ValueError("an identified backend and verified positive session limit are required")


@dataclass(frozen=True)
class Submission:
    operation_id: str
    session_id: str

    def __post_init__(self) -> None:
        if not self.operation_id or not self.session_id:
            raise ValueError("provider operation and session IDs are required")


@dataclass(frozen=True)
class BackendResult:
    status: str  # pending, completed, failed, unknown, not_started (reconciliation only)
    artifact_uri: str = ""
    artifact_hash: str = ""
    detail: str = ""
    handle: Submission | None = None
    generation_seconds: float | None = None

    def __post_init__(self) -> None:
        if self.status not in {"pending", "completed", "failed", "unknown", "not_started"}:
            raise ValueError("invalid backend status")
        if self.status == "completed" and (
            not self.artifact_uri or len(self.artifact_hash) != 64
            or any(c not in "0123456789abcdef" for c in self.artifact_hash)
        ):
            raise ValueError("completed jobs require a persisted artifact URI and SHA256")
        if self.status == "not_started" and not self.detail:
            raise ValueError("not_started requires reconciliation evidence")
        if self.generation_seconds is not None and (
            not math.isfinite(self.generation_seconds) or self.generation_seconds <= 0
        ):
            raise ValueError("generation duration must be a measured positive finite number")


class BeforeSendError(Exception):
    """Adapter guarantees no provider request was sent; only these errors may retry."""

    def __init__(self, message: str, *, retry_after: float | None = None):
        super().__init__(message)
        if retry_after is not None and (not math.isfinite(retry_after) or retry_after < 0):
            raise ValueError("retry_after must be a nonnegative finite number")
        self.retry_after = retry_after


class SessionBackend(Protocol):
    capabilities: BackendCapabilities

    def submit(self, packet: dict, *, session_id: str | None) -> Submission: ...
    def poll(self, handle: Submission) -> BackendResult: ...
    def reconcile(self, job_id: str, handle: Submission | None) -> BackendResult: ...
    def reset(self, session_id: str) -> None: ...
    def close(self, session_id: str) -> None: ...


@dataclass(frozen=True)
class PoolConfig:
    review_capacity: int
    lease_seconds: float = 300
    max_attempts: int = 3
    warmup_reviews: int = 2
    ewma_alpha: float = 0.3
    min_probe_seconds: float = 5.0

    def __post_init__(self) -> None:
        if min(self.review_capacity, self.max_attempts, self.warmup_reviews) < 1:
            raise ValueError("capacities and attempt/review counts must be positive")
        if not math.isfinite(self.lease_seconds) or self.lease_seconds <= 0 or not 0 < self.ewma_alpha <= 1:
            raise ValueError("invalid lease duration or EWMA alpha")
        if not math.isfinite(self.min_probe_seconds) or self.min_probe_seconds <= 0:
            raise ValueError("startup probe interval must be a positive finite duration")


@dataclass
class _Record:
    job: SceneJob
    status: str = "queued"
    attempts: int = 0
    slot: int | None = None
    handle: Submission | None = None
    started_at: float = 0
    lease_until: float = 0
    retry_at: float = 0
    cancel_requested: bool = False
    artifact_uri: str = ""
    artifact_hash: str = ""
    detail: str = ""


class AdaptivePool:
    """Generation slots and bounded review credits are separate resources.

    ``checkpoint`` is required: a no-op is appropriate only for explicit tests.
    Backend exceptions without proof of pre-send failure leave the job UNKNOWN.
    """

    BUSY = {"submitting", "running", "unknown"}
    TERMINAL = {"accepted", "rejected", "failed", "cancelled", "stale"}

    def __init__(self, backend: SessionBackend, config: PoolConfig, *,
                 checkpoint: Callable[[dict], None], clock: Callable[[], float] = time.time):
        self.backend, self.config, self.checkpoint, self.clock = backend, config, checkpoint, clock
        self.records: dict[str, _Record] = {}
        self.current: dict[str, list[str]] = {}
        self.channels: list[str] = []
        self.cursor = 0
        self.slots: list[dict] = []
        self.target = 1
        self.generation_ewma: float | None = None
        self.service_ewma: float | None = None
        self.dispatch_service_ewma: float | None = None
        self.last_probe_at = self.clock()
        self.reviews_since_adjust = 0
        self.cooldown_until = 0.0
        self.review_receipts: dict[str, str] = {}
        self.events: list[dict] = []
        self.sequence = 0

    def _event(self, kind: str, **data: object) -> None:
        self.sequence += 1
        self.events.append({"sequence": self.sequence, "type": kind, **data})

    def _save(self) -> None:
        self.checkpoint(self.snapshot())

    def _matches(self, record: _Record) -> bool:
        return self.current[record.job.scene_key] == [record.job.revision, record.job.input_hash]

    def enqueue(self, job: SceneJob) -> None:
        old = self.records.get(job.job_id)
        if old:
            if old.job != job:
                raise ValueError("job_id already identifies different inputs")
            return
        self.current.setdefault(job.scene_key, [job.revision, job.input_hash])
        if self.current[job.scene_key] != [job.revision, job.input_hash]:
            raise ValueError("set the current scene revision before enqueuing changed inputs")
        self.records[job.job_id] = _Record(job)
        if job.channel_id not in self.channels:
            self.channels.append(job.channel_id)
        self._event("queued", job_id=job.job_id)
        self._save()

    def set_current_revision(self, run_id: str, scene_id: str, revision: str, input_hash: str) -> None:
        key = _json([run_id, scene_id])
        self.current[key] = [revision, input_hash]
        for record in self.records.values():
            if record.job.scene_key == key and not self._matches(record):
                if record.status in {"queued", "review", "accepted"}:
                    record.status = "stale"
                self._event("revision_changed", job_id=record.job.job_id)
        self._save()
        for record in self.records.values():
            if record.job.scene_key == key and not self._matches(record):
                self._stop_unsent(record, "stale")

    def _stop_unsent(self, record: _Record, terminal: str) -> None:
        cancel = getattr(self.backend, "cancel_before_send", None)
        if record.status in self.BUSY and record.handle and cancel and cancel(record.handle):
            record.status = terminal
            self._release(record)
            self._event(terminal, job_id=record.job.job_id, detail="cancelled before provider dispatch")
            self._save()

    def _close(self, session_id: str) -> None:
        try:
            self.backend.close(session_id)
        except Exception as exc:
            self._event("close_failed", session_id=session_id, detail=str(exc))

    def _release(self, record: _Record) -> None:
        if record.slot is None:
            return
        slot = self.slots[record.slot]
        slot["job_id"] = None
        if slot["session_id"] and not self.backend.capabilities.supports_reset:
            self._close(slot["session_id"])
            slot["session_id"] = None
        record.slot = None

    def _observe(self, old: float | None, sample: float) -> float:
        return sample if old is None else self.config.ewma_alpha * sample + (1 - self.config.ewma_alpha) * old

    def _apply_result(self, record: _Record, result: BackendResult, *, reconciliation: bool = False) -> None:
        if result.handle:
            record.handle = result.handle
            if record.slot is not None:
                self.slots[record.slot]["session_id"] = result.handle.session_id
        record.detail = result.detail
        if result.status == "pending" and record.handle:
            record.status = "running"
            record.lease_until = self.clock() + self.config.lease_seconds
        elif result.status == "completed":
            record.artifact_uri, record.artifact_hash = result.artifact_uri, result.artifact_hash
            record.status = ("cancelled" if record.cancel_requested else
                             "review" if self._matches(record) else "stale")
            generation = result.generation_seconds or max(0.001, self.clock() - record.started_at)
            self.generation_ewma = self._observe(self.generation_ewma, generation)
            self._release(record)
        elif result.status == "failed":
            record.status = "cancelled" if record.cancel_requested else "failed"
            self._release(record)
        elif result.status == "not_started" and reconciliation:
            self._release(record)
            record.status = ("cancelled" if record.cancel_requested else "stale" if not self._matches(record)
                             else "queued" if record.attempts < self.config.max_attempts else "failed")
            record.handle = None
        else:
            record.status = "unknown"
        self._event(record.status, job_id=record.job.job_id, detail=record.detail)
        self._save()

    def _next(self) -> _Record | None:
        for offset in range(len(self.channels)):
            index = (self.cursor + offset) % len(self.channels)
            channel = self.channels[index]
            for record in self.records.values():
                if record.status == "queued" and record.job.channel_id == channel and record.retry_at <= self.clock():
                    self.cursor = (index + 1) % len(self.channels)
                    return record
        return None

    def _dispatch(self, record: _Record) -> None:
        slot_id = next((i for i, slot in enumerate(self.slots) if slot["job_id"] is None), len(self.slots))
        if slot_id == len(self.slots):
            self.slots.append({"job_id": None, "session_id": None})
        slot = self.slots[slot_id]
        record.slot, record.status, slot["job_id"] = slot_id, "submitting", record.job.job_id
        record.attempts += 1
        record.started_at = self.clock()
        record.lease_until = record.started_at + self.config.lease_seconds
        self._event("submitting", job_id=record.job.job_id, attempt=record.attempts)
        self._save()  # The intent is durable before any external action.
        if slot["session_id"]:
            if not self.backend.capabilities.supports_reset:
                self._close(slot["session_id"])
                slot["session_id"] = None
            else:
                try:
                    self.backend.reset(slot["session_id"])
                except Exception:
                    self._close(slot["session_id"])
                    slot["session_id"] = None
        try:
            record.handle = self.backend.submit(record.job.packet(), session_id=slot["session_id"])
            slot["session_id"] = record.handle.session_id
            record.status = "running"
        except BeforeSendError as exc:
            record.detail = str(exc)
            self._release(record)
            if exc.retry_after is not None and record.attempts < self.config.max_attempts:
                self.cooldown_until = max(self.cooldown_until, self.clock() + exc.retry_after)
                record.retry_at, record.status = self.cooldown_until, "queued"
                self.target = max(1, self.target // 2)
            else:
                record.status = "failed"
        except Exception as exc:
            record.status, record.detail = "unknown", str(exc)
        self._event(record.status, job_id=record.job.job_id, detail=record.detail)
        self._save()

    def observe_dispatch_service(self, seconds: float) -> None:
        if not math.isfinite(seconds) or seconds <= 0:
            raise ValueError("dispatch service time must be measured and positive")
        self.dispatch_service_ewma = self._observe(self.dispatch_service_ewma, seconds)
        self._save()

    def _probe_startup(self, coordinator_idle: bool) -> None:
        if not coordinator_idle or self.generation_ewma is not None:
            return
        if any(r.status in {"review", "unknown", "submitting"} for r in self.records.values()):
            return
        busy = [r for r in self.records.values() if r.status == "running"]
        interval = max(self.config.min_probe_seconds, self.dispatch_service_ewma or 0)
        now = self.clock()
        if (len(busy) < self.target or not busy or now - min(r.started_at for r in busy) < interval
                or now - self.last_probe_at < interval or now < self.cooldown_until
                or not any(r.status == "queued" and r.retry_at <= now for r in self.records.values())):
            return
        ceiling = min(self.backend.capabilities.max_sessions, self.config.review_capacity)
        if self.target < ceiling:
            self.target += 1
            self.last_probe_at = now
            self._event("capacity_probe", target=self.target)
            self._save()

    def tick(self, *, dispatch: bool = True, coordinator_idle: bool = True) -> list[dict]:
        """Poll once, then refill available slots. Never wait for the slowest job."""
        start = self.sequence
        for record in list(self.records.values()):
            if record.status != "running":
                continue
            if self.clock() >= record.lease_until:
                self._apply_result(record, BackendResult("unknown", detail="lease expired; reconcile before reuse"))
                continue
            try:
                result = self.backend.poll(record.handle)  # type: ignore[arg-type]
            except Exception as exc:
                result = BackendResult("unknown", detail=str(exc))
            self._apply_result(record, result)
        if dispatch:
            self._probe_startup(coordinator_idle)
        limit = min(self.target, self.backend.capabilities.max_sessions)
        while dispatch and self.clock() >= self.cooldown_until:
            busy = sum(r.status in self.BUSY for r in self.records.values())
            credits = busy + sum(r.status == "review" for r in self.records.values())
            if busy >= limit or credits >= self.config.review_capacity:
                break
            record = self._next()
            if record is None:
                break
            self._dispatch(record)
            limit = min(self.target, self.backend.capabilities.max_sessions)
        return [dict(event) for event in self.events if event["sequence"] > start]

    def accept(self, job_id: str, *, revision: str, input_hash: str, artifact_hash: str,
               review_id: str, service_seconds: float, accepted: bool = True) -> None:
        """Record exact-file QA, not user MP4 approval. Review time excludes queue waiting."""
        if not review_id or not math.isfinite(service_seconds) or service_seconds <= 0:
            raise ValueError("review ID and measured positive coordinator service time required")
        receipt = _hash(_json([job_id, revision, input_hash, artifact_hash, accepted]))
        if review_id in self.review_receipts:
            if self.review_receipts[review_id] != receipt:
                raise ValueError("review ID was used for another decision")
            return
        record = self.records[job_id]
        if not self._matches(record) or [revision, input_hash] != [record.job.revision, record.job.input_hash]:
            raise ValueError("stale scene result cannot be accepted")
        if record.status != "review" or artifact_hash != record.artifact_hash:
            raise ValueError("review must target the exact completed artifact")
        record.status = "accepted" if accepted else "rejected"
        self.review_receipts[review_id] = receipt
        self.service_ewma = self._observe(self.service_ewma, service_seconds)
        self.reviews_since_adjust += 1
        if self.reviews_since_adjust >= self.config.warmup_reviews and self.generation_ewma is not None:
            desired = min(self.backend.capabilities.max_sessions, self.config.review_capacity,
                          max(1, math.floor(self.generation_ewma / self.service_ewma)))
            backlog = sum(r.status == "review" for r in self.records.values())
            if desired < self.target:
                self.target -= 1
            elif desired > self.target and backlog == 0:
                self.target += 1
            self.reviews_since_adjust = 0
        self._event(record.status, job_id=job_id, review_id=review_id, target=self.target)
        self._save()

    def cancel(self, job_id: str) -> None:
        record = self.records[job_id]
        if record.status in self.TERMINAL:
            return
        record.cancel_requested = True
        if record.status in {"queued", "review"}:
            record.status = "cancelled"
        self._event("cancel_requested", job_id=job_id)
        self._save()  # Inflight jobs may still finish; their results are never accepted.
        self._stop_unsent(record, "cancelled")

    def reconcile(self, job_id: str) -> None:
        record = self.records[job_id]
        if record.status != "unknown":
            raise ValueError("only unknown outcomes require reconciliation")
        try:
            result = self.backend.reconcile(job_id, record.handle)
        except Exception as exc:
            result = BackendResult("unknown", detail=str(exc))
        self._apply_result(record, result, reconciliation=True)

    def snapshot(self) -> dict:
        return json.loads(_json({"version": 1, "backend_id": self.backend.capabilities.backend_id,
            "config": asdict(self.config), "records": [asdict(r) for r in self.records.values()],
            "current": self.current, "channels": self.channels, "cursor": self.cursor,
            "slots": self.slots, "target": self.target, "generation_ewma": self.generation_ewma,
            "service_ewma": self.service_ewma, "dispatch_service_ewma": self.dispatch_service_ewma,
            "last_probe_at": self.last_probe_at, "reviews_since_adjust": self.reviews_since_adjust,
            "cooldown_until": self.cooldown_until, "review_receipts": self.review_receipts,
            "events": self.events, "sequence": self.sequence}))

    def acknowledge_events(self, through_sequence: int) -> None:
        """Prune only after the application has durably recorded these event IDs."""
        if not 0 <= through_sequence <= self.sequence:
            raise ValueError("event sequence is outside this pool")
        self.events = [event for event in self.events if event["sequence"] > through_sequence]
        self._save()

    @classmethod
    def restore(cls, backend: SessionBackend, snapshot: dict, *, checkpoint: Callable[[dict], None],
                clock: Callable[[], float] = time.time, recover: bool = True) -> AdaptivePool:
        if snapshot["version"] != 1 or snapshot["backend_id"] != backend.capabilities.backend_id:
            raise ValueError("snapshot version or backend differs; explicit migration required")
        pool = cls(backend, PoolConfig(**snapshot["config"]), checkpoint=checkpoint, clock=clock)
        for key in ("current", "channels", "cursor", "slots", "target", "generation_ewma", "service_ewma",
                    "reviews_since_adjust", "cooldown_until", "review_receipts", "events", "sequence"):
            setattr(pool, key, json.loads(_json(snapshot[key])))
        pool.dispatch_service_ewma = snapshot.get("dispatch_service_ewma")
        pool.last_probe_at = snapshot.get("last_probe_at", pool.clock())
        pool.target = min(pool.target, backend.capabilities.max_sessions)
        for data in snapshot["records"]:
            data = dict(data)
            data["job"] = SceneJob(**data["job"])
            data["handle"] = Submission(**data["handle"]) if data["handle"] else None
            record = _Record(**data)
            if recover and (record.status == "submitting" or (
                record.status == "running" and not backend.capabilities.durable_handles
            )):
                record.status = "unknown"
                record.detail = "restart requires provider reconciliation"
                pool._event("unknown", job_id=record.job.job_id, detail=record.detail)
            pool.records[record.job.job_id] = record
        pool._save()
        return pool
