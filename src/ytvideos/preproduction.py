"""Validate a portable, text-only production handoff without granting approvals.

Narration offsets are Unicode character offsets in the exact UTF-8 master, not
word timings. A structural pass does not assess the artwork or claim real media.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

from .context import reference_path
from .errors import WorkflowError
from .util import digest, require_text

SCHEMA = "ytv-preproduction-v1"
STAGES = {"storyboard", "audio", "packaging", "subtitles", "render", "review"}


def _items(value, name, *, empty=False):
    if not isinstance(value, list) or (not value and not empty) or any(not isinstance(x, dict) for x in value):
        raise WorkflowError(f"{name} must be a list of objects")
    return value


def _id(value, name):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value):
        raise WorkflowError(f"invalid {name} id")
    return value


def _sha(value, name):
    if not isinstance(value, str) or not re.fullmatch(r"[a-f0-9]{64}", value):
        raise WorkflowError(f"{name} requires a SHA-256")


def read_package(path):
    try:
        value = json.loads(Path(path).read_bytes().decode("utf-8"))
    except (OSError, ValueError) as exc:
        raise WorkflowError("cannot read UTF-8 preproduction JSON") from exc
    if not isinstance(value, dict):
        raise WorkflowError("preproduction must be a JSON object")
    return value


def validate_package(data, *, script, profile, format):
    """Check identity, complete narration coverage and declared planning inputs.

    Existing-reference hashes are declarations until their bytes are opened by
    the local worker. Planned reference sheets are generation inputs, not assets.
    """
    if not isinstance(data, dict) or data.get("schema") != SCHEMA:
        raise WorkflowError("expected ytv-preproduction-v1")
    if profile.get("recipe") != "illustrated":
        raise WorkflowError("prepared image handoff currently supports the illustrated recipe only")
    expected = {"channel_id": profile["id"], "format": format,
                "script_sha256": hashlib.sha256(script.encode("utf-8")).hexdigest(),
                "profile_sha256": digest(profile)}
    for key, value in expected.items():
        if data.get(key) != value:
            raise WorkflowError(f"preproduction {key} differs from the selected source or pinned profile")
    require_text(script, "source script")
    assets = _items(data.get("assets"), "assets", empty=True)
    asset_ids = set()
    for asset in assets:
        key = _id(asset.get("id"), "asset")
        if key in asset_ids:
            raise WorkflowError("duplicate asset id")
        asset_ids.add(key)
        require_text(asset.get("kind"), "asset kind")
        if asset.get("mode") == "generate":
            require_text(asset.get("prompt"), "reference sheet prompt")
        elif asset.get("mode") == "existing":
            reference_path(asset.get("path"))
            _sha(asset.get("sha256"), "existing reference")
            require_text(asset.get("role"), "existing reference role")
        else:
            raise WorkflowError("asset mode must be generate or existing; missing references belong in open_items")
    scenes = _items(data.get("scenes"), "scenes")
    seen, prompts, cursor, flow_count = set(), set(), 0, 0
    # Eligibility comes from a declared channel recipe, not from the story title.
    flow_allowed = format == "short" and any(
        item.get("path", "").endswith("/docs/FLOW_PRODUCTION.md")
        and "storyboard" in item.get("stages", ["storyboard"])
        and format in item.get("formats", [format])
        for item in profile.get("context_references", []))
    for scene in scenes:
        key = _id(scene.get("id"), "scene")
        if key in seen:
            raise WorkflowError("duplicate scene id")
        seen.add(key)
        for field in ("visual_intent", "prompt", "continuity", "camera", "sound"):
            require_text(scene.get(field), f"{key}.{field}")
        normalized = " ".join(scene["prompt"].split())
        if normalized in prompts:
            raise WorkflowError("duplicate scene prompt; specify the independent composition")
        prompts.add(normalized)
        span = scene.get("narration")
        if not isinstance(span, dict):
            raise WorkflowError("scene needs exact narration character span")
        start, end = span.get("start"), span.get("end")
        if (type(start) is not int or type(end) is not int or start != cursor
                or not start < end <= len(script) or span.get("text") != script[start:end]):
            raise WorkflowError("narration spans must cover the exact source in order without gaps or rewrites")
        cursor = end
        if any(field in scene for field in ("start_frame", "end_frame", "start_seconds", "end_seconds")):
            raise WorkflowError("prepared text must not claim final timing; bind actual audio locally")
        references = scene.get("asset_ids")
        if (not isinstance(references, list) or any(not isinstance(x, str) for x in references)
                or len(references) != len(set(references)) or any(x not in asset_ids for x in references)):
            raise WorkflowError("scene asset_ids must resolve to distinct prepared assets")
        if not references:
            require_text(scene.get("reference_na_reason"), "scene reference_na_reason")
        motion = scene.get("motion")
        if not isinstance(motion, dict) or motion.get("method") not in {"hold", "pan_zoom", "flow_ingredients"}:
            raise WorkflowError("scene motion requires hold, pan_zoom or flow_ingredients")
        require_text(motion.get("brief"), "motion brief")
        if motion["method"] == "flow_ingredients":
            if not flow_allowed:
                raise WorkflowError("Flow is not declared for this channel and format")
            flow_count += 1
        checks = scene.get("checks")
        if not isinstance(checks, list) or not checks:
            raise WorkflowError("scene needs explicit visual acceptance checks")
        for check in checks:
            require_text(check, "scene acceptance check")
    if cursor != len(script):
        raise WorkflowError("narration coverage must include the full exact source")
    for field in ("audio_plan", "packaging_brief", "edit_plan"):
        require_text(data.get(field), field)
    for item in _items(data.get("open_items"), "open_items", empty=True):
        for field in ("stage", "reason", "resolution"):
            require_text(item.get(field), f"open_items.{field}")
    return {"schema": SCHEMA, "scene_count": len(scenes), "asset_count": len(assets),
            "flow_scene_count": flow_count, "open_items": data["open_items"],
            "structural_checks": "PASS", "content_review": "UNVERIFIED", "timing": "unmeasured",
            "production_authorized": False, "providers_called": False}


def guidance(run):
    """Keep an old plan available as a baseline after an explicit script revision."""
    key = run.get("source_preproduction_id")
    if not key:
        return None
    outputs = run["tasks"]["script"]["outputs"]
    changed = bool(outputs and run["artifacts"][outputs[0]]["sha256"] != run["pins"].get("source_script"))
    artifact = run["artifacts"].get(key)
    if not artifact or artifact["sha256"] != run["pins"].get("source_preproduction"):
        raise WorkflowError("source preproduction differs from its pin")
    return {"artifact_id": key, "artifact": artifact, "mode": "stale_baseline" if changed else "reuse",
            "instruction": (
                "The approved script changed. Keep this handoff as a historical baseline, not current scene instructions; "
                "prepare the affected plan through the normal authorized task."
                if changed else
                "Resolve this artifact through artifact_root and verify its hash. Read open_items and block affected "
                "tasks rather than inventing missing inputs. Reuse its scenes, full prompts, asset briefs, audio, "
                "editing and packaging decisions; do not design another film. Resolve planned reference sheets to "
                "real registered artifacts before scene dispatch. Bind timing only to actual recorded narration. "
                "Flow motion briefs remain drafts until the generated still is inspected and the exact batch approved. "
                "Normal coverage/continuity/rights checks and complete still apply; source input is not a receipt.")}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate prepared text; no run, approvals or providers")
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--script", type=Path, required=True)
    parser.add_argument("--channel", required=True)
    parser.add_argument("--format", choices=("short", "long"), required=True)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args(argv)
    from .profiles import read_profile
    try:
        result = validate_package(read_package(args.file), script=args.script.read_bytes().decode("utf-8"),
                                  profile=read_profile(args.project_root / "channels", args.channel), format=args.format)
        print(json.dumps(result, ensure_ascii=False))
    except (WorkflowError, OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
