import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .errors import WorkflowError


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def require_text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise WorkflowError(f"{name}: expected non-empty text")
    return value


def parse_time(value):
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError, AttributeError) as exc:
        raise WorkflowError("timestamp must be ISO 8601 with an explicit timezone") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise WorkflowError("timestamp must include an explicit timezone")
    return parsed
