import json
import re
from pathlib import Path

from .errors import WorkflowError
from .util import digest, require_text


def load_profile(root, channel):
    if not re.fullmatch(r"[a-z][a-z0-9_]{1,63}", channel):
        raise WorkflowError("channel must be a registered slug")
    path = Path(root) / channel / "channel.json"
    if not path.is_file():
        raise WorkflowError(f"channel profile is missing: {path}; do not substitute another channel")
    profile = json.loads(path.read_text())
    if profile.get("id") != channel or profile.get("schema_version") != 1:
        raise WorkflowError("invalid channel profile identity or schema")
    for field in ("name", "language", "recipe", "youtube_channel_id"):
        require_text(profile.get(field), field)
    if profile.get("status") not in {"active", "frozen", "unconfigured"}:
        raise WorkflowError("profile status must be active, frozen or unconfigured")
    if profile["status"] != "active":
        raise WorkflowError(f"channel {channel} is {profile['status']}; an explicit profile change is required")
    if profile.get("recipe") not in {"illustrated", "licensed_clips"}:
        raise WorkflowError("unknown production recipe")
    if not isinstance(profile.get("release_policy"), dict):
        raise WorkflowError("channel release_policy is required")
    return profile


def profile_identity(profile):
    return {"id": profile["id"], "sha256": digest(profile)}
