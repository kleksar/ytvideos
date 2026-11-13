"""Read-only, evidence-bound promotion planning for already uploaded videos.

A plan never performs a YouTube write or certifies a Studio action. A guarded
host must recheck current provider state before each mutation and read it back.
"""
from __future__ import annotations

from datetime import datetime
import re

from .release import ReleaseSpec


class PromotionError(ValueError):
    """Invalid or untrusted provider inventory."""


VIDEO_ID = re.compile(r"[A-Za-z0-9_-]{11}\Z")


def _inventory_map(rows, *, label, key):
    if type(rows) is not list:
        raise PromotionError(f"{label} inventory must be a list")
    values = {}
    for row in rows:
        if type(row) is not dict or type(row.get(key)) is not str or not row[key]:
            raise PromotionError(f"{label} inventory has an invalid identity")
        if row[key] in values:
            raise PromotionError(f"duplicate {label} identity: {row[key]}")
        values[row[key]] = row
    return values


def build_plan(spec: ReleaseSpec, *, video_id: str, inventory: dict) -> dict:
    """Check explicit editorial targets against observed provider inventory.

    Inventory schema: channel_id, observed_at (offset-aware), source
    (api_readback or studio_readback), videos[] and playlists[]. A video entry
    has id/channel_id/privacy/format; playlist entry has id/channel_id/privacy,
    and optionally a COMPLETE video_ids snapshot plus members_complete=true.

    A read-only plan is never a write permit, and cannot replace later
    operation reservation, fresh provider checks or exact Studio read-back.
    """
    if not isinstance(spec, ReleaseSpec):
        raise PromotionError("a validated ReleaseSpec is required")
    if not isinstance(video_id, str) or not VIDEO_ID.fullmatch(video_id):
        raise PromotionError("invalid published video_id")
    if type(inventory) is not dict or inventory.get("channel_id") != spec.channel_id:
        raise PromotionError("inventory channel differs from the release")
    if inventory.get("source") not in {"api_readback", "studio_readback"}:
        raise PromotionError("inventory requires observed provider provenance")
    try:
        timestamp = datetime.fromisoformat(inventory["observed_at"].replace("Z", "+00:00"))
    except (TypeError, ValueError, KeyError, AttributeError):
        raise PromotionError("inventory needs an ISO 8601 observed_at timestamp") from None
    if timestamp.utcoffset() is None:
        raise PromotionError("inventory timestamp must have a UTC offset")
    videos = _inventory_map(inventory.get("videos"), label="video", key="id")
    playlists = _inventory_map(inventory.get("playlists"), label="playlist", key="id")

    def video_problem(target_id: str, *, related: bool = False) -> str | None:
        if target_id == video_id:
            return "target cannot be the same video"
        target = videos.get(target_id)
        if not target:
            return "target video is missing from the observed inventory"
        if target.get("channel_id") != spec.channel_id:
            return "target video belongs to another channel"
        if target.get("privacy") not in {"public", "unlisted"}:
            return "target video is neither Public nor Unlisted"
        if related and target.get("format") not in ("short", "long"):
            return "target must be verified as a Short or long-form video"
        return None

    def playlist_problem(playlist_id: str) -> str | None:
        target = playlists.get(playlist_id)
        if not target:
            return "playlist is missing from the observed inventory"
        if target.get("channel_id") != spec.channel_id:
            return "playlist belongs to another channel"
        if target.get("privacy") not in {"public", "unlisted", "private"}:
            return "playlist privacy is not verified"
        return None

    source = videos.get(video_id)
    source_problem = None
    if not source:
        source_problem = "published video is missing from the observed inventory"
    elif source.get("channel_id") != spec.channel_id:
        source_problem = "published video belongs to another channel"
    elif source.get("privacy") != "public":
        source_problem = "published video has not been verified Public"
    elif source.get("format") != spec.format:
        source_problem = "observed source format differs from the release"

    data = spec.to_dict()
    actions = []

    def add(kind: str, provider: str, payload: dict | None, problem: str | None = None):
        actions.append({
            "kind": kind, "provider": provider,
            "status": "blocked" if problem else "ready_for_host",
            "reason": problem, "payload": payload,
            "requires": "fresh read-back, live authorization, reserved operation and verified result",
        })

    if spec.format == "short" and "related_video_id" in data:
        target_id = data["related_video_id"]
        problem = source_problem or video_problem(target_id, related=True)
        if videos.get(target_id, {}).get("format") == "short":
            add("shorts_to_short", "studio", {"short_id": video_id, "target_short_id": target_id}, problem)
        else:
            # Preserve the v1 long action, including blocked unverified targets.
            add("shorts_to_long", "studio", {"short_id": video_id, "long_id": target_id}, problem)
    if spec.format == "long" and "end_screen" in data:
        errors = []
        for element in data["end_screen"]["elements"]:
            if element["type"] == "video":
                error = video_problem(element["target_id"])
            elif element["type"] == "playlist":
                error = playlist_problem(element["target_id"])
            else:
                error = None if element["target_id"] == spec.channel_id else "subscribe target is a different channel"
            if error:
                errors.append(error)
        add("end_screen", "studio", {"video_id": video_id, "end_screen": data["end_screen"]},
            source_problem or ("; ".join(sorted(set(errors))) if errors else None))
    if "playlist_id" in data:
        playlist_id = data["playlist_id"]
        error = source_problem or playlist_problem(playlist_id)
        playlist = playlists.get(playlist_id, {})
        if not error and (playlist.get("members_complete") is not True or
                          type(playlist.get("video_ids")) is not list):
            error = "complete playlist membership read-back is required"
        if not error and video_id in playlist["video_ids"]:
            actions.append({"kind": "playlist", "provider": "api", "status": "already_present",
                            "reason": "verified playlist membership", "payload": {"video_id": video_id, "playlist_id": playlist_id},
                            "requires": "no write"})
        else:
            add("playlist", "api", {"video_id": video_id, "playlist_id": playlist_id}, error)
    if "community_post" in data:
        add("community_post", "studio",
            {"linked_video_id": video_id, "text": data["community_post"]["text"]},
            source_problem or ("posts are not applicable to made-for-kids videos"
                               if data["metadata"]["made_for_kids"] else None))

    return {
        "schema": "ytv-cross-promotion-plan-v1",
        "channel_id": spec.channel_id, "video_id": video_id,
        "release_sha256": spec.sha256,
        "inventory_observed_at": timestamp.isoformat(),
        "inventory_source": inventory["source"],
        "actions": actions,
        "blockers": sorted({item["reason"] for item in actions if item["status"] == "blocked"}),
        "execution": "read_only_plan; no YouTube mutation or Studio result",
    }
