import json
import re
from pathlib import Path

from .errors import WorkflowError
from .util import digest, require_text


def read_profile(root, channel):
    """Read an identity for diagnosis without admitting it to production."""
    if not re.fullmatch(r"[a-z][a-z0-9_]{1,63}", channel):
        raise WorkflowError("channel must be a registered slug")
    path = Path(root) / channel / "channel.json"
    if not path.is_file():
        raise WorkflowError(f"channel profile is missing: {path}; do not substitute another channel")
    profile = json.loads(path.read_text())
    if profile.get("id") != channel or profile.get("schema_version") != 1:
        raise WorkflowError("invalid channel profile identity or schema")
    for field in ("name", "language"):
        require_text(profile.get(field), field)
    if profile.get("status") not in {"active", "frozen", "unconfigured"}:
        raise WorkflowError("profile status must be active, frozen or unconfigured")
    return profile


def load_profile(root, channel):
    profile = read_profile(root, channel)
    if profile["status"] != "active":
        raise WorkflowError(f"channel {channel} is {profile['status']}; an explicit profile change is required")
    for field in ("recipe", "youtube_channel_id"):
        require_text(profile.get(field), field)
    if profile.get("recipe") not in {"illustrated", "licensed_clips"}:
        raise WorkflowError("unknown production recipe")
    if not isinstance(profile.get("release_policy"), dict):
        raise WorkflowError("channel release_policy is required")
    return profile


def profile_identity(profile):
    return {"id": profile["id"], "sha256": digest(profile)}


def inspect_profiles(root, *, channel=None, format=None, project=None):
    """Describe configuration, not live readiness, before creating or funding a run."""
    from .context import snapshot_references
    from .production_contract import production_requirements

    root = Path(root)
    def policy_summary(requirements):
        return {key: requirements[key] for key in ("configured", "sha256", "unresolved", "available_variants")} | {
            "canvas": requirements["video"].get("canvas"), "fps": requirements["video"].get("fps")}

    channels = [channel] if channel else sorted(path.parent.name for path in root.glob("*/channel.json"))
    result = []
    for name in channels:
        row = {"channel": name, "configuration_ready": False, "blockers": [], "formats": {}}
        result.append(row)
        try:
            profile = read_profile(root, name)
        except (WorkflowError, ValueError, OSError) as exc:
            row["blockers"].append(str(exc))
            continue
        row.update(name=profile["name"], status=profile["status"], recipe=profile.get("recipe"),
                   profile_sha256=digest(profile), youtube_channel_id=profile.get("youtube_channel_id"))
        blockers = profile.get("readiness_blockers", [])
        if not isinstance(blockers, list) or any(not isinstance(value, str) for value in blockers):
            row["blockers"].append("readiness_blockers must be a list of explanations")
        else:
            row["blockers"].extend(blockers)
        try:
            load_profile(root, name)
        except WorkflowError as exc:
            row["blockers"].append(str(exc))
        for selected in ([format] if format else ["short", "long"]):
            entry = {"configuration_ready": False, "blockers": [], "variants": {}}
            row["formats"][selected] = entry
            try:
                requirements = production_requirements(profile, selected)
                entry["requirements"] = policy_summary(requirements)
                variants = requirements["available_variants"]
                policies = []
                for variant in variants:
                    resolved = production_requirements(profile, selected, variant=variant)
                    policies.append(resolved)
                    entry["variants"][variant] = policy_summary(resolved)
                for policy in policies or [requirements]:
                    if not policy["configured"]:
                        entry["blockers"].append({"variant": policy["variant"], "unresolved": policy["unresolved"]})
                if project is not None:
                    snapshot = snapshot_references(project, profile, selected)
                    entry["reference_documents"] = len(snapshot["documents"])
            except (WorkflowError, ValueError, OSError, KeyError, TypeError) as exc:
                entry["blockers"].append(str(exc))
            entry["configuration_ready"] = not row["blockers"] and not entry["blockers"]
        row["configuration_ready"] = all(value["configuration_ready"] for value in row["formats"].values())
    return {"schema_version": 1, "channels": result,
            "live_readiness": "unverified",
            "scope": "Saved channel configuration and current references only. No run, provider call or approval is created. "
                     "A ready configuration still requires doctor, actual capabilities, source rights and exact output review."}
