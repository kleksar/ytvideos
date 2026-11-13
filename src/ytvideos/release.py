"""Release preparation and evidence contracts; no network or approval creation.

Adapters must obtain WriteGrant from the trusted workflow store, immediately
before a write. Parsing a spec or passing these checks does not authorize a write.
Read-back receipts describe observed values, not an agent's assertion of PASS.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import math
import re
from typing import Any, Mapping


class ReleaseError(ValueError):
    pass


def _object(value: Any, required: set[str], optional: set[str] = frozenset()) -> dict:
    if type(value) is not dict or required - value.keys() or value.keys() - required - optional:
        raise ReleaseError(f"Expected fields {sorted(required)}; optional {sorted(optional)}")
    return value


def _text(value: Any, name: str, pattern: str | None = None) -> str:
    if type(value) is not str or not value.strip() or (pattern and not re.fullmatch(pattern, value)):
        raise ReleaseError(f"Invalid {name}")
    return value


def _bool(value: Any, name: str) -> bool:
    if type(value) is not bool:
        raise ReleaseError(f"{name} must be a boolean")
    return value


def _number(value: Any, name: str, minimum: float = 0) -> float:
    if type(value) not in (int, float) or not math.isfinite(value) or value < minimum:
        raise ReleaseError(f"Invalid {name}")
    return float(value)


def _sha(value: Any) -> str:
    return _text(value, "sha256", r"[0-9a-f]{64}")


def _time(value: Any) -> datetime:
    _text(value, "timestamp")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise ReleaseError("Timestamp must be ISO 8601") from None
    if result.utcoffset() is None:
        raise ReleaseError("Timestamp must include a UTC offset")
    return result.astimezone(timezone.utc)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


@dataclass(frozen=True)
class ReleaseSpec:
    run_id: str
    revision: int
    channel_id: str
    format: str
    has_speech: bool
    data_json: str

    @classmethod
    def from_dict(cls, value: dict) -> "ReleaseSpec":
        required = {"run_id", "revision", "channel_id", "format", "has_speech", "metadata"}
        optional = {"media_sha256", "duration_seconds", "publish_at", "thumbnail_sha256", "caption",
                    "playlist_id", "playlist_na_reason", "related_video_id", "related_na_reason",
                    "end_screen", "ab_variants", "community_post"}
        _object(value, required, optional)
        # Own the JSON snapshot; subsequent caller mutations cannot alter the spec.
        value = json.loads(_canonical(value))
        _text(value["run_id"], "run_id")
        if type(value["revision"]) is not int or value["revision"] < 1:
            raise ReleaseError("revision must be a positive integer")
        _text(value["channel_id"], "channel_id", r"UC[A-Za-z0-9_-]{22}")
        if value["format"] not in ("long", "short"):
            raise ReleaseError("format must be long or short")
        _bool(value["has_speech"], "has_speech")
        meta = _object(value["metadata"], {
            "title", "description", "tags", "category_id", "language", "audio_language",
            "made_for_kids", "contains_synthetic_media", "license", "age_restricted", "paid_promotion"})
        for key in ("title", "description"):
            _text(meta[key], key)
            if "<" in meta[key] or ">" in meta[key]:
                raise ReleaseError(f"{key} contains forbidden angle brackets")
        if len(meta["title"]) > 100 or len(meta["description"].encode("utf-8")) > 5000:
            raise ReleaseError("Title or description exceeds YouTube limits")
        _text(meta["category_id"], "category_id", r"[1-9][0-9]*")
        for key in ("language", "audio_language"):
            _text(meta[key], key, r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*")
        for key in ("made_for_kids", "contains_synthetic_media", "age_restricted", "paid_promotion"):
            _bool(meta[key], key)
        if meta["license"] not in ("youtube", "creativeCommon"):
            raise ReleaseError("Unsupported license")
        tags = meta["tags"]
        if type(tags) is not list or not tags or any(type(x) is not str or not x.strip() for x in tags):
            raise ReleaseError("tags must be a nonempty list of relevant strings")
        if len(set(tags)) != len(tags):
            raise ReleaseError("Duplicate tags")
        # Spaces make a tag count as quoted in YouTube's 500-character limit.
        if sum(len(tag) + (2 if " " in tag else 0) for tag in tags) + len(tags) - 1 > 500:
            raise ReleaseError("Tags exceed YouTube's 500-character limit")
        for key in ("media_sha256", "thumbnail_sha256"):
            if key in value:
                _sha(value[key])
        if "duration_seconds" in value:
            _number(value["duration_seconds"], "duration_seconds", 0.001)
        if "publish_at" in value:
            value["publish_at"] = _time(value["publish_at"]).isoformat().replace("+00:00", "Z")
        if "caption" in value:
            cap = _object(value["caption"], {"sha256", "language"})
            _sha(cap["sha256"])
            if cap["language"] != meta["audio_language"]:
                raise ReleaseError("Caption language must match the accepted audio language")
        for key, pattern in (("playlist_id", r"[A-Za-z0-9_-]{10,100}"),
                             ("related_video_id", r"[A-Za-z0-9_-]{11}")):
            if key in value:
                _text(value[key], key, pattern)
        for key in ("playlist_na_reason", "related_na_reason"):
            if key in value:
                _text(value[key], key)
        if "playlist_id" in value and "playlist_na_reason" in value:
            raise ReleaseError("Playlist target and N/A reason conflict")
        if "related_video_id" in value and "related_na_reason" in value:
            raise ReleaseError("Related target and N/A reason conflict")
        if "end_screen" in value:
            end = _object(value["end_screen"], {"start_seconds", "end_seconds", "elements"})
            start = _number(end["start_seconds"], "end_screen.start_seconds")
            stop = _number(end["end_seconds"], "end_screen.end_seconds")
            duration = value.get("duration_seconds")
            if duration is None or duration < 25 or not 5 <= stop - start <= 20 or stop > duration or start < duration - 20:
                raise ReleaseError("End screen must occupy 5–20 seconds in the last 20 seconds of a video >=25 seconds")
            if type(end["elements"]) is not list or not 1 <= len(end["elements"]) <= 4:
                raise ReleaseError("End screen requires 1–4 elements")
            for item in end["elements"]:
                _object(item, {"type", "target_id"})
                _text(item["type"], "end-screen element type")
                pattern = {"video": r"[A-Za-z0-9_-]{11}", "subscribe": r"UC[A-Za-z0-9_-]{22}",
                           "playlist": r"[A-Za-z0-9_-]{10,100}"}.get(item["type"])
                if not pattern:
                    raise ReleaseError("Unsupported end-screen element")
                _text(item["target_id"], "end-screen target", pattern)
            if value["format"] == "short" or meta["made_for_kids"]:
                raise ReleaseError("End screens are not applicable to this video")
        if "community_post" in value:
            post = _object(value["community_post"], {"text"})
            _text(post["text"], "community_post.text")
            if len(post["text"]) > 500:
                raise ReleaseError("Community post exceeds the editorial limit (500 characters)")
            if meta["made_for_kids"]:
                raise ReleaseError("Community posts are not applicable to made-for-kids video")
        if "ab_variants" in value:
            variants = value["ab_variants"]
            if type(variants) is not list or not 2 <= len(variants) <= 3:
                raise ReleaseError("A/B testing requires 2–3 variants")
            for item in variants:
                _object(item, {"title", "thumbnail_sha256"})
                _text(item["title"], "A/B title")
                if len(item["title"]) > 100 or "<" in item["title"] or ">" in item["title"]:
                    raise ReleaseError("Invalid A/B title")
                _sha(item["thumbnail_sha256"])
            if value["format"] == "short" or meta["made_for_kids"] or meta["age_restricted"]:
                raise ReleaseError("A/B testing is not applicable to this video")
        return cls(value["run_id"], value["revision"], value["channel_id"], value["format"],
                   value["has_speech"], _canonical(value))

    def to_dict(self) -> dict:
        return json.loads(self.data_json)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data_json.encode()).hexdigest()


@dataclass(frozen=True)
class ReleasePolicy:
    end_screen: bool
    ab_test: bool
    shorts_related: bool
    min_schedule_lead_seconds: int = 300

    @classmethod
    def from_dict(cls, value: dict) -> "ReleasePolicy":
        _object(value, {"end_screen", "ab_test", "shorts_related"}, {"min_schedule_lead_seconds"})
        return cls(**value)

    def __post_init__(self):
        for key in ("end_screen", "ab_test", "shorts_related"):
            _bool(getattr(self, key), key)
        if type(self.min_schedule_lead_seconds) is not int or self.min_schedule_lead_seconds < 300:
            raise ReleaseError("Scheduling lead must be at least 300 seconds")


@dataclass(frozen=True)
class Requirement:
    key: str
    applicable: bool
    phase: str
    provider: str
    expected: Any = None
    reason: str | None = None


def requirement_matrix(spec: ReleaseSpec, policy: ReleasePolicy) -> tuple[Requirement, ...]:
    """Availability failures stay blockers; only content/policy decides N/A."""
    data = spec.to_dict()
    meta = data["metadata"]
    items = [Requirement(key, True, "pre_schedule", "studio" if key in {"age_restricted", "paid_promotion"} else "api", val)
             for key, val in meta.items()]
    items.extend((Requirement("visibility", True, "pre_schedule", "api", "private"),
                  Requirement("processing", True, "pre_schedule", "api", "succeeded"),
                  Requirement("thumbnail", True, "pre_schedule", "api", data.get("thumbnail_sha256")),
                  Requirement("captions", spec.has_speech, "pre_schedule", "api",
                              {**data["caption"], "status": "serving", "isDraft": False, "trackKind": "standard"}
                              if "caption" in data else None,
                              None if spec.has_speech else "Video has no speech"),
                  Requirement("playlist", "playlist_id" in data, "pre_schedule", "api", data.get("playlist_id"),
                              data.get("playlist_na_reason")),
                  Requirement("publish_at", True, "scheduled", "api", data.get("publish_at"))))
    end = policy.end_screen and spec.format == "long" and not meta["made_for_kids"] and data.get("duration_seconds", 25) >= 25
    end_reason = None if end else ("Disabled by channel policy" if not policy.end_screen else "Video format, audience or duration is ineligible")
    items.append(Requirement("end_screen", end, "pre_schedule", "studio", data.get("end_screen"), end_reason))
    related = policy.shorts_related and spec.format == "short" and "related_na_reason" not in data
    related_reason = None if related else (data.get("related_na_reason") or "Not a Short or disabled by channel policy")
    items.append(Requirement("related_video", related, "pre_schedule", "studio", data.get("related_video_id"), related_reason))
    ab = policy.ab_test and spec.format == "long" and not meta["made_for_kids"] and not meta["age_restricted"]
    items.append(Requirement("ab_test", ab, "after_publish", "studio", data.get("ab_variants"),
                             None if ab else "Disabled by policy or video ineligible"))
    post = "community_post" in data
    items.append(Requirement("community_post", post, "after_publish", "studio",
                             data.get("community_post"), None if post else "No independent post was selected"))
    return tuple(items)


def prepare_release_plan(spec: ReleaseSpec, policy: ReleasePolicy, *, now: datetime,
                         capabilities: Mapping[str, bool] | None = None) -> dict:
    """Prepare before MP4 approval. Never invent a time or claim a completed action."""
    if now.utcoffset() is None:
        raise ReleaseError("now must be timezone-aware")
    data = spec.to_dict()
    requirements = requirement_matrix(spec, policy)
    blockers = [f"Missing {key}" for key in ("media_sha256", "duration_seconds", "publish_at") if key not in data]
    for item in requirements:
        if item.phase == "after_publish":
            continue  # A/B cannot run on scheduled/private videos.
        if item.applicable and item.expected is None:
            blockers.append(f"Missing {item.key}")
        if not item.applicable and not item.reason:
            blockers.append(f"Missing N/A reason for {item.key}")
        if item.applicable and capabilities is not None and capabilities.get(item.provider) is not True:
            blockers.append(f"Capability unavailable or unverified: {item.provider} for {item.key}")
    if "publish_at" in data and _time(data["publish_at"]) <= now + timedelta(seconds=policy.min_schedule_lead_seconds):
        blockers.append("Schedule is not safely in the future")
    return {"release_sha256": spec.sha256, "requirements": [asdict(x) for x in requirements],
            "blockers": sorted(set(blockers)), "status": "prepared_not_published"}


@dataclass(frozen=True)
class ReadbackReceipt:
    key: str
    channel_id: str
    video_id: str
    release_sha256: str
    method: str
    observation_id: str
    evidence_sha256: str
    observed_at: datetime
    value_json: str

    @classmethod
    def from_dict(cls, value: dict) -> "ReadbackReceipt":
        _object(value, {"key", "channel_id", "video_id", "release_sha256", "method", "observation_id",
                        "evidence_sha256", "observed_at", "observed_value"})
        for key in ("key", "observation_id"):
            _text(value[key], key)
            if value[key].strip().lower() in {"true", "pass", "accepted", "verified"}:
                raise ReleaseError("Receipt requires a concrete observation identity")
        _text(value["channel_id"], "channel_id", r"UC[A-Za-z0-9_-]{22}")
        _text(value["video_id"], "video_id", r"[A-Za-z0-9_-]{11}")
        _sha(value["release_sha256"])
        _sha(value["evidence_sha256"])
        if value["method"] not in {"api_readback", "studio_readback"}:
            raise ReleaseError("Receipt method must be an actual read-back")
        return cls(value["key"], value["channel_id"], value["video_id"], value["release_sha256"],
                   value["method"], value["observation_id"], value["evidence_sha256"], _time(value["observed_at"]),
                   _canonical(value["observed_value"]))


def validate_receipts(spec: ReleaseSpec, policy: ReleasePolicy, receipts: tuple[ReadbackReceipt, ...], *,
                      video_id: str, phase: str = "pre_schedule") -> tuple[str, ...]:
    """Validate bindings and values. The caller must verify evidence bytes/provenance."""
    phases = {"pre_schedule": {"pre_schedule"}, "scheduled": {"pre_schedule", "scheduled"},
              "after_publish": {"after_publish"}}
    if phase not in phases:
        raise ReleaseError("Unknown receipt phase")
    _text(video_id, "video_id", r"[A-Za-z0-9_-]{11}")
    found: dict[str, ReadbackReceipt] = {}
    errors = []
    for item in receipts:
        if not isinstance(item, ReadbackReceipt):
            raise ReleaseError("Use parsed ReadbackReceipt objects")
        if item.key in found:
            errors.append(f"Duplicate receipt: {item.key}")
        found[item.key] = item
    for requirement in requirement_matrix(spec, policy):
        if requirement.phase not in phases[phase]:
            continue
        if not requirement.applicable:
            if not requirement.reason:
                errors.append(f"Missing N/A reason: {requirement.key}")
            continue
        receipt = found.get(requirement.key)
        expected = requirement.expected
        if requirement.key == "community_post" and expected is not None:
            expected = {**expected, "linked_video_id": video_id}
        if (receipt is None or receipt.channel_id != spec.channel_id or receipt.video_id != video_id
                or receipt.release_sha256 != spec.sha256 or expected is None
                or receipt.value_json != _canonical(expected)
                or (requirement.provider == "studio" and receipt.method != "studio_readback")):
            errors.append(f"Unverified saved value: {requirement.key}")
    return tuple(errors)


@dataclass(frozen=True)
class WriteGrant:
    """Construct only from a live trusted-store decision, never from LLM JSON."""
    run_id: str
    channel_id: str
    media_sha256: str
    approval_event_id: str
    release_sha256: str
    operation_id: str
    action: str

    @classmethod
    def from_dict(cls, value: dict) -> "WriteGrant":
        _object(value, {"run_id", "channel_id", "media_sha256", "approval_event_id", "release_sha256", "operation_id", "action"})
        for key in ("run_id", "approval_event_id", "operation_id", "action"):
            _text(value[key], key)
        _text(value["channel_id"], "channel_id", r"UC[A-Za-z0-9_-]{22}")
        _sha(value["media_sha256"])
        _sha(value["release_sha256"])
        return cls(**value)


def guard_write(spec: ReleaseSpec, grant: WriteGrant | dict, *, action: str, operation_state: str,
                policy: ReleasePolicy, now: datetime) -> None:
    """Additional local checks after store authorization; no substitute for it."""
    if action not in {"upload", "metadata", "thumbnail", "captions", "playlist", "end_screen", "related_video", "schedule", "ab_test"}:
        raise ReleaseError("Action is outside the scheduled-publication workflow")
    if type(grant) is dict:
        grant = WriteGrant.from_dict(grant)
    if not isinstance(grant, WriteGrant):
        raise ReleaseError("A trusted-store WriteGrant is required")
    data = spec.to_dict()
    if (grant.run_id != spec.run_id or grant.channel_id != spec.channel_id or grant.release_sha256 != spec.sha256
            or grant.media_sha256 != data.get("media_sha256") or grant.action != action):
        raise ReleaseError("Authorization does not match this release/action/media")
    for key in ("approval_event_id", "operation_id"):
        _text(getattr(grant, key), key)
    _sha(grant.media_sha256)
    if operation_state != "reserved":
        raise ReleaseError("Write requires a new reservation; pending/unknown outcomes require reconciliation")
    if action == "schedule":
        blockers = prepare_release_plan(spec, policy, now=now)["blockers"]
        if blockers:
            raise ReleaseError("; ".join(blockers))
