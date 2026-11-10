"""Durable local outbox for an app-owned native-tool dispatcher.

This module never creates chats or calls an undocumented API. A dispatcher claims
a request, invokes an available runtime tool, and records the observed evidence.
Local operation IDs are NOT provider job IDs or proof that a tool has run.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import time
from typing import Callable
import uuid

from .pool import BackendCapabilities, BackendResult, Submission


class ToolBridgeBackend:
    def __init__(self, *, max_sessions: int, checkpoint: Callable[[dict], None],
                 clock: Callable[[], float] = time.time):
        self.capabilities = BackendCapabilities("native-tool-bridge-v1", max_sessions, durable_handles=True)
        self.checkpoint, self.clock = checkpoint, clock
        self.requests: dict[str, dict] = {}
        self.receipts: dict[str, str] = {}

    def snapshot(self) -> dict:
        return copy.deepcopy({"version": 1, "requests": self.requests, "receipts": self.receipts})

    def _save(self) -> None:
        self.checkpoint(self.snapshot())

    def submit(self, packet: dict, *, session_id: str | None) -> Submission:
        if session_id is not None:
            raise ValueError("native bridge requires a fresh independent session for every job")
        operation = "bridge-" + hashlib.sha256(packet["job_id"].encode()).hexdigest()
        old = self.requests.get(operation)
        if old and old["packet"] != packet:
            raise ValueError("job_id already identifies different scene inputs")
        if not old or old["status"] == "not_started":
            self.requests[operation] = {
                "operation_id": operation, "packet": copy.deepcopy(packet), "status": "queued",
                "claim_token": None, "owner": None, "lease_until": 0, "provider": None,
                "reconnectable": False, "result": None, "close_requested": False,
            }
            self._save()
        return Submission(operation, "local-" + operation)

    def pending_requests(self) -> list[dict]:
        return copy.deepcopy([r for r in self.requests.values() if r["status"] == "queued"])

    def claim(self, operation_id: str, *, owner: str, lease_seconds: float = 300) -> dict:
        if not owner or not math.isfinite(lease_seconds) or lease_seconds <= 0:
            raise ValueError("identified owner and positive lease required")
        request = self.requests[operation_id]
        if request["status"] != "queued":
            raise ValueError("request is not dispatchable; reconcile any unknown outcome")
        request.update(status="dispatching", claim_token=uuid.uuid4().hex, owner=owner,
                       lease_until=self.clock() + lease_seconds)
        self._save()  # Must commit before invoking spawn/image generation.
        return copy.deepcopy(request)

    def _claim(self, operation_id: str, claim_token: str) -> dict:
        request = self.requests[operation_id]
        if not claim_token or request["claim_token"] != claim_token:
            raise ValueError("stale or absent dispatch claim")
        return request

    def record_submission(self, operation_id: str, *, claim_token: str,
                          provider: dict, reconnectable: bool = False) -> None:
        """Store observed tool name/session ID; reconnectability must be verified."""
        if not provider.get("tool") or not provider.get("session_id"):
            raise ValueError("actual tool and session identifiers are required")
        request = self._claim(operation_id, claim_token)
        if request["provider"]:
            if request["provider"] != provider or request["reconnectable"] != reconnectable:
                raise ValueError("submission evidence cannot be replaced")
            return
        if request["status"] != "dispatching" or self.clock() >= request["lease_until"]:
            raise ValueError("claim expired or dispatch state changed; reconcile observed outcome")
        request.update(status="running", provider=copy.deepcopy(provider), reconnectable=reconnectable)
        self._save()

    def record_observation(self, operation_id: str, *, claim_token: str, receipt_id: str,
                           result: BackendResult, evidence: dict) -> bool:
        """An actual tool result or read-back is required; no inferred success."""
        request = self._claim(operation_id, claim_token)
        if not receipt_id or not evidence:
            raise ValueError("observation requires a unique receipt and actual evidence")
        payload = {"operation": operation_id, "status": result.status, "uri": result.artifact_uri,
                   "hash": result.artifact_hash, "detail": result.detail, "evidence": evidence,
                   "generation_seconds": result.generation_seconds}
        digest = hashlib.sha256(json.dumps(payload, sort_keys=True, allow_nan=False).encode()).hexdigest()
        if receipt_id in self.receipts:
            if self.receipts[receipt_id] != digest:
                raise ValueError("receipt ID already identifies another observation")
            return False
        if request["status"] in {"completed", "failed", "not_started"}:
            raise ValueError("terminal observations are immutable")
        if result.status == "not_started" and request["status"] not in {"dispatching", "unknown"}:
            raise ValueError("not_started requires reconciliation of an uncertain dispatch")
        request["result"] = {"status": result.status, "artifact_uri": result.artifact_uri,
                             "artifact_hash": result.artifact_hash, "detail": result.detail,
                             "generation_seconds": result.generation_seconds}
        request["status"] = "running" if result.status == "pending" else result.status
        request["last_evidence"] = copy.deepcopy(evidence)
        self.receipts[receipt_id] = digest
        self._save()
        return True

    def poll(self, handle: Submission) -> BackendResult:
        request = self.requests[handle.operation_id]
        if request["status"] == "dispatching" and self.clock() >= request["lease_until"]:
            request["status"] = "unknown"
            request["result"] = {"status": "unknown", "detail": "dispatcher lease expired"}
            self._save()
        if request["status"] in {"queued", "dispatching", "running"}:
            return BackendResult("pending")
        return BackendResult(**(request["result"] or {"status": "unknown", "detail": "outcome not observed"}))

    def reconcile(self, job_id: str, handle: Submission | None) -> BackendResult:
        operation = "bridge-" + hashlib.sha256(job_id.encode()).hexdigest()
        if operation not in self.requests:
            return BackendResult("not_started", detail="no durable bridge outbox entry exists")
        result = self.poll(Submission(operation, "local-" + operation))
        if result.status == "pending":
            return BackendResult("pending", handle=Submission(operation, "local-" + operation))
        return result

    def reset(self, session_id: str) -> None:
        raise NotImplementedError("native bridge never inherits another image's conversation")

    def cancel_before_send(self, handle: Submission) -> bool:
        request = self.requests[handle.operation_id]
        if request["status"] != "queued":
            return False
        request["status"] = "failed"
        request["result"] = {"status": "failed", "detail": "cancelled before native dispatch"}
        self._save()
        return True

    def close(self, session_id: str) -> None:
        operation = session_id.removeprefix("local-")
        if operation in self.requests:
            self.requests[operation]["close_requested"] = True
            self._save()  # Dispatcher may close its own observed session; no UI action here.

    @classmethod
    def restore(cls, snapshot: dict, *, max_sessions: int, checkpoint: Callable[[dict], None],
                clock: Callable[[], float] = time.time, recover: bool = True) -> ToolBridgeBackend:
        if snapshot["version"] != 1:
            raise ValueError("unsupported bridge snapshot")
        bridge = cls(max_sessions=max_sessions, checkpoint=checkpoint, clock=clock)
        bridge.requests, bridge.receipts = copy.deepcopy(snapshot["requests"]), dict(snapshot["receipts"])
        for request in bridge.requests.values():
            if recover and (request["status"] == "dispatching" or (
                request["status"] == "running" and not request["reconnectable"]
            )):
                request["status"] = "unknown"
                request["result"] = {"status": "unknown", "detail": "restart requires native-tool read-back"}
        bridge._save()
        return bridge
