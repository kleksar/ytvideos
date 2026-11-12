#!/usr/bin/env python3
"""Add approved paper-word cutouts to the isolated Paper Detour 009 timeline.

The script is deliberately receipt-driven and ID-scoped. It never opens, shows,
exports, or publishes a project. By default it validates only; --execute performs
the timeline mutations and captures review frames.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
EPISODE_ROOT = SCRIPT_DIR.parents[2]
BUILD_RECEIPT = SCRIPT_DIR / "build_paper_project_receipt.json"
PLAN_PATH = SCRIPT_DIR / "accent_plan.json"
REVIEW_DIR = SCRIPT_DIR / "Previews"
FPS = 30


def read_json(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"Required file does not exist: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected an object in {path}")
    return value


def save_json(path: Path, data: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def load_context() -> tuple[dict, dict, Path, Path]:
    build = read_json(BUILD_RECEIPT)
    if build.get("status") != "ready_for_review":
        raise ValueError(f"Base build is not ready_for_review: {build.get('status')}")
    if build.get("visible_project_switched") is True or build.get("exported") or build.get("published"):
        raise ValueError("Base build receipt reports a visible switch, export, or publication")
    project_id, timeline_id = build.get("project_id"), build.get("timeline_id")
    if not isinstance(project_id, str) or not isinstance(timeline_id, str):
        raise ValueError("Base build receipt is missing projectId or timelineId")
    visual_receipt_path = Path(build.get("visual_receipt", "")).resolve()
    visual_receipt = read_json(visual_receipt_path)
    if (visual_receipt.get("status") != "ready_for_review"
            or visual_receipt.get("project_id") != project_id
            or visual_receipt.get("timeline_id") != timeline_id):
        raise ValueError("Picture-layer receipt does not match the completed build receipt")
    plan = read_json(PLAN_PATH)
    if plan.get("version") != 1 or not plan.get("accents"):
        raise ValueError("Accent plan is missing or has an unsupported version")
    receipt_path = SCRIPT_DIR / "accent_pass_receipt.json"
    if receipt_path.exists():
        raise ValueError(f"Accent receipt already exists; inspect before retrying: {receipt_path}")
    for entry in plan["accents"]:
        path = (EPISODE_ROOT / plan["assets_root"] / entry["asset"]).resolve()
        if not path.is_relative_to(EPISODE_ROOT) or not path.is_file():
            raise ValueError(f"Accent asset is missing or outside the episode folder: {path}")
        if entry["end_frame"] - entry["start_frame"] != plan["animation"]["clip_duration_frames"]:
            raise ValueError(f"Unexpected duration for {entry['asset']}")
        if entry["end_frame"] > build.get("frames", 0):
            raise ValueError(f"Accent extends beyond the timeline: {entry['asset']}")
    return build, plan, receipt_path, visual_receipt_path


class Palmier:
    def __init__(self):
        connection_dir = EPISODE_ROOT.parents[2] / "automation/palmier"
        sys.path.insert(0, str(connection_dir))
        from inspect_connection import PalmierConnection

        self.client = PalmierConnection()
        self.client.connect()
        self.tools = {x["name"]: x for x in self.client.request("tools/list").get("tools", [])}
        for name, required in {
            "manage_project": {"action"},
            "get_timeline": {"projectId", "timelineId"},
            "get_media": {"projectId"},
            "import_media": {"projectId", "source"},
            "add_clips": {"projectId", "timelineId", "entries"},
            "manage_tracks": {"projectId", "timelineId"},
            "set_keyframes": {"projectId", "timelineId", "clipId", "property", "keyframes"},
            "manage_snapshots": {"projectId", "timelineId", "action"},
            "inspect_timeline": {"projectId", "timelineId"},
        }.items():
            tool = self.tools.get(name)
            if not tool or not required.issubset(set(tool.get("inputSchema", {}).get("required", []))):
                raise RuntimeError(f"Palmier API no longer satisfies the ID-scoped {name} schema")
        keyframes = self.tools["set_keyframes"].get("description", "")
        if "TOP-LEFT" not in keyframes or "smooth" not in keyframes:
            raise RuntimeError("Palmier keyframe coordinate contract changed; no edits attempted")

    def call(self, name: str, args: dict) -> dict:
        response = self.client.request("tools/call", {"name": name, "arguments": args})
        if response.get("isError"):
            raise RuntimeError(f"Palmier {name} failed: {response.get('content')}")
        texts = [x["text"] for x in response.get("content", []) if x.get("type") == "text"]
        if len(texts) != 1:
            raise RuntimeError(f"Palmier {name} returned an unexpected response")
        return json.loads(texts[0])

    def raw(self, name: str, args: dict) -> dict:
        response = self.client.request("tools/call", {"name": name, "arguments": args})
        if response.get("isError"):
            raise RuntimeError(f"Palmier {name} failed: {response.get('content')}")
        return response


def journal_call(palmier: Palmier, path: Path, receipt: dict,
                 label: str, tool: str, args: dict) -> dict:
    receipt["pending"] = {"label": label, "tool": tool, "arguments": args}
    save_json(path, receipt)
    result = palmier.call(tool, args)
    receipt.setdefault("steps", []).append({
        "label": label,
        "tool": tool,
        "actionId": result.get("actionId"),
        "result": result,
    })
    receipt.pop("pending", None)
    save_json(path, receipt)
    return result


def validate_timeline(timeline: dict, build: dict) -> list[dict]:
    if (timeline.get("width"), timeline.get("height"), timeline.get("fps"),
            timeline.get("totalFrames")) != (1080, 1920, FPS, build["frames"]):
        raise ValueError("The target timeline metadata differs from the prepared 1080x1920/30 manifest")
    tracks = [x for x in timeline.get("tracks", []) if x.get("type") == "video"]
    audio = [x for x in timeline.get("tracks", []) if x.get("type") == "audio"]
    if audio:
        raise ValueError("Unexpected audio track present; this authorized draft is silent")
    if len(tracks) != 4:
        raise ValueError(f"Expected exactly the BG/MG/FG/Film Grain tracks before accents; saw {len(tracks)}")
    names = [(x.get("name") or x.get("label") or "").lower() for x in tracks]
    if names != ["film grain", "foreground", "middle", "background"]:
        raise ValueError(f"Unexpected pre-accent stack order: {names}")
    return tracks


def capture_frames(palmier: Palmier, receipt_path: Path, receipt: dict,
                   project_id: str, timeline_id: str, plan: dict) -> list[Path]:
    REVIEW_DIR.mkdir(exist_ok=True)
    saved = []
    for accent in plan["accents"]:
        for label, relative in (("entry", 6), ("hold", 27), ("exit", 47)):
            frame = accent["start_frame"] + relative
            response = palmier.raw("inspect_timeline", {
                "projectId": project_id,
                "timelineId": timeline_id,
                "startFrame": frame,
            })
            images = [x for x in response.get("content", []) if x.get("type") == "image"]
            if len(images) != 1:
                raise RuntimeError(f"Palmier returned no unique review frame at {frame}")
            path = REVIEW_DIR / f"accent_{accent['asset'][:-4]}_{label}_f{frame:04d}.png"
            path.write_bytes(base64.b64decode(images[0]["data"]))
            saved.append(path)
    receipt["review_frames"] = [str(x) for x in saved]
    save_json(receipt_path, receipt)
    return saved


def execute(build: dict, plan: dict, receipt_path: Path,
            visual_receipt_path: Path) -> dict:
    visual_receipt = read_json(visual_receipt_path)
    project_id, timeline_id = build["project_id"], build["timeline_id"]
    receipt = {
        "version": 1,
        "status": "preparing",
        "project_id": project_id,
        "timeline_id": timeline_id,
        "accent_plan": str(PLAN_PATH),
        "visible_project_before": None,
        "exported": False,
        "published": False,
        "steps": [],
    }
    save_json(receipt_path, receipt)
    try:
        palmier = Palmier()
        projects = palmier.call("manage_project", {"action": "list"})
        project = next((x for x in projects.get("projects", []) if x.get("id") == project_id), None)
        if not project or not project.get("isAccessible"):
            raise ValueError("The exact target project is missing or inaccessible")
        receipt["visible_project_before"] = (projects.get("visible") or {}).get("id")
        if receipt["visible_project_before"] != build.get("visible_project_before"):
            raise ValueError("Visible Palmier project changed since base assembly; stop without timeline edits")
        inventory = palmier.call("get_media", {"projectId": project_id})
        folder = f"PaperLayers/{build['timeline_name']}/Accents"
        if folder in inventory.get("folders", []):
            raise ValueError(f"Target media folder already exists; inspect before retrying: {folder}")
        timeline = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
        validate_timeline(timeline, build)

        media_refs = {}
        for accent in plan["accents"]:
            path = (EPISODE_ROOT / plan["assets_root"] / accent["asset"]).resolve()
            imported = journal_call(palmier, receipt_path, receipt,
                                    f"import {accent['asset']}", "import_media",
                                    {"projectId": project_id, "source": {"path": str(path)},
                                     "folder": folder})
            media_ref = imported.get("mediaRef") or imported.get("assetId") or imported.get("id")
            if not isinstance(media_ref, str) or not media_ref:
                raise RuntimeError("Accent import did not return a stable media ID; inspect before retrying")
            media_refs[accent["asset"]] = media_ref
            receipt.setdefault("media", {})[accent["asset"]] = media_ref
            save_json(receipt_path, receipt)

        entries = [{
            "mediaRef": media_refs[accent["asset"]],
            "startFrame": accent["start_frame"],
            "endFrame": accent["end_frame"],
            "includeAudio": False,
        } for accent in plan["accents"]]
        added = journal_call(palmier, receipt_path, receipt, "place paper accent cutouts",
                             "add_clips", {"projectId": project_id,
                                           "timelineId": timeline_id,
                                           "entries": entries})
        if len(added.get("clips", [])) != len(entries):
            raise RuntimeError("Unexpected number of accent clips; inspect receipt before retrying")
        new_tracks = added.get("createdTracks", [])
        if len(new_tracks) != 1 or not new_tracks[0].get("trackId"):
            raise RuntimeError("Could not identify the single new accent track")
        accent_track_id = new_tracks[0]["trackId"]
        receipt["accent_track_id"] = accent_track_id
        clips = added["clips"]
        receipt["clips"] = {accent["asset"]: clip["id"]
                            for accent, clip in zip(plan["accents"], clips)}
        save_json(receipt_path, receipt)

        journal_call(palmier, receipt_path, receipt, "stack accents between BG and MG",
                     "manage_tracks", {"projectId": project_id, "timelineId": timeline_id,
                                       "reorder": [{"trackId": accent_track_id, "to": 3}]})
        journal_call(palmier, receipt_path, receipt, "name accent track",
                     "manage_tracks", {"projectId": project_id, "timelineId": timeline_id,
                                       "set": [{"trackId": accent_track_id, "name": "Accents"}]})

        animation = plan["animation"]
        fade = animation["entrance_frames"]
        end = animation["clip_duration_frames"] - 1
        hold_last = end - animation["exit_frames"]
        for accent, clip in zip(plan["accents"], clips):
            clip_id = clip.get("id")
            if not isinstance(clip_id, str) or not clip_id:
                raise RuntimeError("Palmier omitted an accent clip ID")
            x0, y0 = accent["entry_position"]
            x1, y1 = accent["final_position"]
            width, height = accent["normalized_size"]
            for prop, keyframes in (
                ("position", [[0, x0, y0, "smooth"], [fade, x1, y1, "smooth"],
                              [hold_last, x1, y1, "smooth"], [end, x0, y0, "smooth"]]),
                ("scale", [[0, width, height, "linear"], [end, width, height, "linear"]]),
                ("opacity", [[0, 0.0, "smooth"], [fade, 1.0, "smooth"],
                             [hold_last, 1.0, "smooth"], [end, 0.0, "smooth"]]),
            ):
                journal_call(palmier, receipt_path, receipt,
                             f"animate {accent['asset']} {prop}", "set_keyframes",
                             {"projectId": project_id, "timelineId": timeline_id,
                              "clipId": clip_id, "property": prop,
                              "keyframes": keyframes})

        final_timeline = palmier.call("get_timeline", {"projectId": project_id,
                                                          "timelineId": timeline_id})
        tracks = [x for x in final_timeline.get("tracks", []) if x.get("type") == "video"]
        expected_names = ["Film Grain", "Foreground", "Middle", "Accents", "Background"]
        actual_names = [x.get("name") or x.get("label") for x in tracks]
        if actual_names != expected_names:
            raise RuntimeError(f"Final video stack does not match layer order: {actual_names}")
        audio = [x for x in final_timeline.get("tracks", []) if x.get("type") == "audio"]
        if audio:
            raise RuntimeError("An unexpected audio track appeared in the visual-only draft")
        receipt["tracks"] = [{"trackId": x.get("trackId"), "name": n}
                             for x, n in zip(tracks, actual_names)]
        receipt["status"] = "capturing_accent_review_frames"
        save_json(receipt_path, receipt)
        frames = capture_frames(palmier, receipt_path, receipt,
                                project_id, timeline_id, plan)
        projects_after = palmier.call("manage_project", {"action": "list"})
        receipt["visible_project_after"] = (projects_after.get("visible") or {}).get("id")
        if receipt["visible_project_after"] != receipt["visible_project_before"]:
            raise RuntimeError("Visible project changed during accent pass; inspect before retrying")
        snapshot = journal_call(palmier, receipt_path, receipt, "save accent pass snapshot",
                                "manage_snapshots", {"projectId": project_id,
                                                     "timelineId": timeline_id,
                                                     "action": "save",
                                                     "name": "Paper accent pass ready for review"})
        receipt["snapshot"] = snapshot
        receipt.update({"status": "ready_for_review", "review_frame_count": len(frames),
                        "exported": False, "published": False,
                        "existing_timelines_modified": False})
        save_json(receipt_path, receipt)
        return receipt
    except Exception as exc:
        receipt["status"] = "stopped_inspect_before_retry"
        receipt["error"] = str(exc)
        save_json(receipt_path, receipt)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Add the planned accent clips")
    args = parser.parse_args()
    try:
        build, plan, receipt_path, visual_receipt_path = load_context()
        summary = {"valid": True, "project_id": build["project_id"],
                   "timeline_id": build["timeline_id"],
                   "accents": [x["asset"] for x in plan["accents"]],
                   "audio_tracks_added": 0, "exported": False, "published": False,
                   "receipt": str(receipt_path)}
        if args.execute:
            result = execute(build, plan, receipt_path, visual_receipt_path)
            summary.update({"status": result["status"],
                            "review_frames": result["review_frame_count"],
                            "track_order": [x["name"] for x in result["tracks"]]})
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(f"Accent pass stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
