"""Optional signed ingress for hosts that isolate user decisions from workers.

The default single-owner path is Production.approve_local. Signing remains a host
capability, never a model tool; a failed signed request cannot become local input.
"""

import base64
from datetime import datetime, timezone

from .errors import WorkflowError
from .util import canonical, parse_time, require_text


class ApprovalVerifier:
    def __init__(self, public_key):
        self.public_key = public_key

    def verify(self, envelope):
        if not self.public_key:
            raise WorkflowError("approval bridge unavailable: configure its Ed25519 public verification key")
        if not isinstance(envelope, dict) or set(envelope) != {"event", "signature"}:
            raise WorkflowError("approval requires a signed user-event envelope")
        event = envelope["event"]
        if not isinstance(event, dict):
            raise WorkflowError("invalid approval event")
        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
            from cryptography.exceptions import InvalidSignature
            key = Ed25519PublicKey.from_public_bytes(base64.b64decode(self.public_key, validate=True))
            key.verify(base64.b64decode(envelope["signature"], validate=True), canonical(event).encode())
        except (ValueError, TypeError, InvalidSignature) as exc:
            raise WorkflowError("invalid approval signature or public key") from exc
        for field in ("event_id", "actor", "source", "run_id", "kind", "artifact_id", "sha256", "created_at", "scope"):
            require_text(event.get(field), field)
        if event["kind"] not in {"script", "mp4"}:
            raise WorkflowError("only script and mp4 are human approval gates")
        if parse_time(event["created_at"]) > datetime.now(timezone.utc):
            raise WorkflowError("approval event is in the future")
        expected_scope = "produce_video" if event["kind"] == "script" else "schedule_publication"
        if event["scope"] != expected_scope:
            raise WorkflowError(f"approval scope must be {expected_scope}")
        return event
