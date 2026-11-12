#!/usr/bin/env python3
"""Create a separate Palmier project from a validated Paper Detour scene manifest.

The scene manifest remains authoritative for stills or legacy BG/MG/FG. This creates
an isolated project, delegates picture assembly to assemble_paper_layers.py, then
adds declared graphics, narration, music, or other approved media tracks. It never
exports or publishes. Every mutation is journaled before it is sent to Palmier.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
FPS = 30
SAFE_NAME = re.compile(r"[A-Za-z0-9 _-]{1,100}")


def fail(message: str) -> None:
    raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def probe_video(path: Path) -> dict:
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0",
               "-show_entries", "stream=codec_name,width,height,pix_fmt,duration,r_frame_rate",
               "-of", "json", str(path)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"Could not inspect video overlay with ffprobe: {path}")
    streams = json.loads(result.stdout).get("streams", [])
    if len(streams) != 1:
        fail(f"Expected exactly one video stream in overlay: {path}")
    stream = streams[0]
    pixel_format = stream.get("pix_fmt", "")
    stream["has_alpha"] = pixel_format.startswith(("yuva", "gbrap", "rgba", "bgra", "argb", "abgr"))
    if type(stream.get("width")) is not int or type(stream.get("height")) is not int:
        fail(f"Video overlay has no pixel dimensions: {path}")
    return stream


def cover_crop(width: int, height: int, target_width: int = 1080,
               target_height: int = 1920) -> list[float]:
    source_aspect = width / height
    target_aspect = target_width / target_height
    if source_aspect > target_aspect:
        side = (1 - target_aspect / source_aspect) / 2
        return [0.0, side, 0.0, side]
    if source_aspect < target_aspect:
        side = (1 - source_aspect / target_aspect) / 2
        return [side, 0.0, side, 0.0]
    return [0.0, 0.0, 0.0, 0.0]


def safe_file(root: Path, value: str, label: str) -> Path:
    if not isinstance(value, str) or not value:
        fail(f"Missing path for {label}")
    path = (root / value).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        fail(f"Missing or outside-episode file for {label}: {path}")
    return path


def resolve_config(manifest_path: Path) -> dict:
    manifest_path = manifest_path.resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        fail("Build manifest version must be 1")
    root_value = data.get("episode_root")
    if not isinstance(root_value, str) or not root_value:
        fail("episode_root must point to the episode directory")
    episode_root = (manifest_path.parent / root_value).resolve()
    if not episode_root.is_dir():
        fail(f"Episode root does not exist: {episode_root}")
    project_name = data.get("project_name")
    if not isinstance(project_name, str) or not SAFE_NAME.fullmatch(project_name.strip()):
        fail("project_name must be a plain, non-empty Palmier project name")
    visual_value = data.get("visual_manifest")
    visual_manifest = safe_file(episode_root, visual_value, "visual_manifest")
    visual = json.loads(visual_manifest.read_text(encoding="utf-8"))
    if not isinstance(visual, dict) or visual.get("version") != 1:
        fail("visual_manifest must use the assemble_paper_layers.py version 1 format")
    if visual.get("base_timeline_id") or visual.get("preserve_tracks") or visual.get("overlay_track_names"):
        fail("A new standalone project cannot clone or preserve tracks from another Palmier timeline")
    timeline_name = visual.get("timeline_name")
    if not isinstance(timeline_name, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", timeline_name):
        fail("visual_manifest needs a safe timeline_name")
    scenes = visual.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        fail("visual_manifest needs scenes")
    total_frames = scenes[-1].get("end_frame")
    if type(total_frames) is not int or total_frames <= 0:
        fail("Could not determine total duration from visual_manifest")

    tracks = data.get("auxiliary_tracks", [])
    if not isinstance(tracks, list):
        fail("auxiliary_tracks must be a list")
    seen_names: set[str] = set()
    resolved_tracks = []
    for track_index, track in enumerate(tracks):
        label = f"auxiliary_tracks[{track_index}]"
        if not isinstance(track, dict):
            fail(f"{label} must be an object")
        name = track.get("name")
        kind = track.get("type")
        if not isinstance(name, str) or not SAFE_NAME.fullmatch(name.strip()):
            fail(f"{label}.name must be a short plain track name")
        if name in seen_names:
            fail(f"Duplicate auxiliary track name: {name}")
        seen_names.add(name)
        if kind not in {"audio", "video"}:
            fail(f"{label}.type must be audio or video")
        media = safe_file(episode_root, track.get("media"), f"{label}.media")
        fit = track.get("fit")
        video_info = None
        fit_crop = None
        if fit is not None:
            if kind != "video" or fit != "cover":
                fail(f"{label}.fit currently supports only 'cover' on video tracks")
            video_info = probe_video(media)
            if track.get("require_alpha") is True and not video_info["has_alpha"]:
                fail(f"{label}.media must contain an alpha channel for a transparent overlay")
            fit_crop = cover_crop(video_info["width"], video_info["height"])
        elif track.get("require_alpha"):
            fail(f"{label}.require_alpha requires fit='cover' so the video stream can be inspected")
        clips = track.get("clips")
        if not isinstance(clips, list) or not clips:
            fail(f"{label}.clips must be a non-empty list")
        resolved_clips = []
        cursor = 0
        for clip_index, clip in enumerate(clips):
            clip_label = f"{label}.clips[{clip_index}]"
            if not isinstance(clip, dict):
                fail(f"{clip_label} must be an object")
            start_frame = clip.get("start_frame")
            source_start = clip.get("source_start_seconds")
            source_end = clip.get("source_end_seconds")
            if type(start_frame) is not int or start_frame != cursor:
                fail(f"{clip_label}.start_frame must continue the previous clip without a timeline gap")
            if (type(source_start) not in (int, float) or type(source_end) not in (int, float)
                    or not math.isfinite(source_start) or not math.isfinite(source_end)
                    or source_start < 0 or source_end <= source_start):
                fail(f"{clip_label} needs a valid source_start_seconds/source_end_seconds pair")
            duration_exact = (source_end - source_start) * FPS
            duration_frames = round(duration_exact)
            if abs(duration_exact - duration_frames) > 0.02:
                fail(f"{clip_label} source duration does not resolve to a whole 30 fps frame")
            end_frame = start_frame + duration_frames
            if end_frame > total_frames:
                fail(f"{clip_label} extends past the visual timeline")
            resolved_clips.append({
                "start_frame": start_frame,
                "end_frame": end_frame,
                "source": [float(source_start), float(source_end)],
                "include_audio": False if kind == "video" else True,
            })
            cursor = end_frame
        if cursor != total_frames:
            fail(f"{label} covers {cursor} frames; the video requires {total_frames}")
        resolved_tracks.append({
            "name": name,
            "type": kind,
            "media": media,
            "media_sha256": sha256(media),
            "fit": fit,
            "video_info": video_info,
            "fit_crop": fit_crop,
            "clips": resolved_clips,
        })
    video_aux = [x for x in resolved_tracks if x["type"] == "video"]
    if len(video_aux) > 1:
        fail("This build currently supports one full-frame overlay track for approved graphics")
    return {
        "manifest_path": manifest_path,
        "manifest_sha256": sha256(manifest_path),
        "episode_root": episode_root,
        "project_name": project_name.strip(),
        "visual_manifest": visual_manifest,
        "timeline_name": timeline_name,
        "total_frames": total_frames,
        "auxiliary_tracks": resolved_tracks,
        "raw": data,
    }


class Palmier:
    def __init__(self):
        connection_dir = REPO_ROOT / "automation/palmier"
        sys.path.insert(0, str(connection_dir))
        from inspect_connection import PalmierConnection

        self.client = PalmierConnection()
        self.client.connect()
        self.tools = {x["name"]: x for x in self.client.request("tools/list").get("tools", [])}

    def call(self, name: str, args: dict) -> dict:
        response = self.client.request("tools/call", {"name": name, "arguments": args})
        if response.get("isError"):
            raise RuntimeError(f"Palmier {name} failed: {response.get('content')}")
        text_items = [x["text"] for x in response.get("content", []) if x.get("type") == "text"]
        if len(text_items) != 1:
            raise RuntimeError(f"Palmier {name} returned an unexpected response")
        return json.loads(text_items[0])

    def raw(self, name: str, args: dict) -> dict:
        response = self.client.request("tools/call", {"name": name, "arguments": args})
        if response.get("isError"):
            raise RuntimeError(f"Palmier {name} failed: {response.get('content')}")
        return response

    def require(self, tool_name: str, keys: set[str]) -> None:
        tool = self.tools.get(tool_name)
        if not tool:
            raise RuntimeError(f"Palmier MCP lacks {tool_name}")
        required = set(tool.get("inputSchema", {}).get("required", []))
        if not keys.issubset(required):
            raise RuntimeError(f"Palmier {tool_name} schema changed; no build mutation attempted")


def save_receipt(path: Path, receipt: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def journal_call(palmier: Palmier, path: Path, receipt: dict, label: str,
                 tool: str, args: dict) -> dict:
    receipt["pending"] = {"label": label, "tool": tool, "arguments": args}
    save_receipt(path, receipt)
    result = palmier.call(tool, args)
    receipt.setdefault("steps", []).append({
        "label": label,
        "tool": tool,
        "actionId": result.get("actionId"),
        "result": result,
    })
    receipt.pop("pending", None)
    save_receipt(path, receipt)
    return result


def create_project(palmier: Palmier, path: Path, receipt: dict, project_name: str) -> str:
    palmier.require("manage_project", {"action"})
    listed = palmier.call("manage_project", {"action": "list"})
    existing = [x for x in listed.get("projects", []) if x.get("name") == project_name]
    if existing:
        fail("A project with this exact name already exists; inspect it instead of creating a duplicate")
    receipt.update({"status": "creating_project", "project_name": project_name,
                    "visible_project_before": (listed.get("visible") or {}).get("id")})
    save_receipt(path, receipt)
    try:
        created = journal_call(palmier, path, receipt, "create isolated Palmier project",
                               "manage_project", {"action": "create", "name": project_name,
                                                  "aspectRatio": "9:16", "quality": "1080p", "fps": FPS})
    except Exception as exc:
        receipt.update({"status": "project_creation_uncertain", "error": str(exc)})
        save_receipt(path, receipt)
        raise
    receipt["project_create_response"] = created
    save_receipt(path, receipt)
    listed_after = palmier.call("manage_project", {"action": "list"})
    candidates = [x for x in listed_after.get("projects", []) if x.get("name") == project_name]
    if len(candidates) != 1 or not candidates[0].get("isAccessible"):
        receipt.update({"status": "created_project_needs_inspection",
                        "projects_after_create": candidates})
        save_receipt(path, receipt)
        fail("Project creation returned an ambiguous or inaccessible project; do not retry")
    project_id = candidates[0].get("id")
    if not isinstance(project_id, str) or not project_id:
        receipt.update({"status": "created_project_needs_inspection",
                        "projects_after_create": candidates})
        save_receipt(path, receipt)
        fail("Palmier did not return a stable project ID; do not retry")
    receipt.update({
        "status": "project_created",
        "project_id": project_id,
        "project_path": candidates[0].get("path"),
        "project_open": candidates[0].get("isOpen"),
        "visible_project_after": (listed_after.get("visible") or {}).get("id"),
    })
    save_receipt(path, receipt)
    if receipt["visible_project_before"] != receipt["visible_project_after"]:
        receipt.update({"status": "visible_project_changed_after_create",
                        "visible_project_switched": True})
        save_receipt(path, receipt)
        fail("Project creation changed the visible Palmier project; stop before timeline assembly")
    return project_id


def run_visual_assembler(config: dict, project_id: str, receipt_path: Path,
                         receipt: dict) -> dict:
    visual = config["visual_manifest"]
    timeline_receipt = visual.with_name(f"{config['timeline_name']}_palmier_receipt.json")
    if timeline_receipt.exists():
        fail(f"Timeline receipt already exists; inspect before retrying: {timeline_receipt}")
    script = REPO_ROOT / "channels/paper_detour/automation/assemble_paper_layers.py"
    command = [sys.executable, str(script), str(visual), "--episode-root",
               str(config["episode_root"]), "--execute", "--project-id", project_id]
    receipt.update({"status": "assembling_picture_layers", "visual_command": command,
                    "visual_receipt": str(timeline_receipt)})
    save_receipt(receipt_path, receipt)
    completed = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    receipt["visual_stdout"] = completed.stdout[-12000:]
    receipt["visual_stderr"] = completed.stderr[-12000:]
    receipt["visual_exit_code"] = completed.returncode
    save_receipt(receipt_path, receipt)
    if completed.returncode != 0:
        receipt["status"] = "stopped_during_picture_assembly"
        save_receipt(receipt_path, receipt)
        fail(f"Picture-layer assembler stopped ({completed.returncode}); inspect both receipts")
    if not timeline_receipt.is_file():
        receipt["status"] = "picture_receipt_missing"
        save_receipt(receipt_path, receipt)
        fail("Picture-layer assembler finished without its receipt; inspect Palmier before retrying")
    result = json.loads(timeline_receipt.read_text(encoding="utf-8"))
    timeline_id = result.get("timeline_id")
    if not isinstance(timeline_id, str) or not timeline_id or result.get("status") != "ready_for_review":
        receipt["status"] = "picture_assembly_needs_inspection"
        receipt["visual_timeline_receipt_content"] = result
        save_receipt(receipt_path, receipt)
        fail("Picture-layer receipt is incomplete; inspect before retrying")
    receipt.update({"status": "picture_layers_ready", "timeline_id": timeline_id})
    save_receipt(receipt_path, receipt)
    return result


def add_auxiliary_tracks(config: dict, palmier: Palmier, receipt_path: Path,
                         receipt: dict, project_id: str, timeline_id: str) -> list[str]:
    if not config["auxiliary_tracks"]:
        return []
    palmier.require("import_media", {"projectId", "source"})
    palmier.require("add_clips", {"projectId", "timelineId", "entries"})
    palmier.require("manage_tracks", {"projectId", "timelineId"})
    folder = f"PaperLayers/{config['timeline_name']}/Auxiliary"
    video_track_ids = []
    for track in config["auxiliary_tracks"]:
        if sha256(track["media"]) != track["media_sha256"]:
            fail(f"Auxiliary media changed after preflight: {track['media']}")
        imported = journal_call(palmier, receipt_path, receipt, f"import {track['name']} media",
                                "import_media", {"projectId": project_id,
                                                 "source": {"path": str(track["media"])},
                                                 "folder": folder})
        media_ref = imported.get("mediaRef") or imported.get("assetId") or imported.get("id")
        if not isinstance(media_ref, str) or not media_ref:
            fail(f"Import of {track['name']} omitted a stable media ID; inspect receipt before retrying")
        receipt.setdefault("auxiliary_media", {})[track["name"]] = media_ref
        save_receipt(receipt_path, receipt)
        entries = [{
            "mediaRef": media_ref,
            "startFrame": clip["start_frame"],
            "source": clip["source"],
            "includeAudio": clip["include_audio"],
        } for clip in track["clips"]]
        added = journal_call(palmier, receipt_path, receipt, f"place {track['name']} track clips",
                             "add_clips", {"projectId": project_id,
                                           "timelineId": timeline_id, "entries": entries})
        created_tracks = added.get("createdTracks", [])
        if len(created_tracks) != 1 or not created_tracks[0].get("trackId"):
            fail(f"Could not identify exactly one track created for {track['name']}; inspect receipt")
        track_id = created_tracks[0]["trackId"]
        if len(added.get("clips", [])) != len(entries):
            fail(f"Palmier placed an unexpected clip count on {track['name']}")
        receipt.setdefault("auxiliary_tracks", {})[track["name"]] = {
            "trackId": track_id,
            "clipIds": [x.get("id") for x in added["clips"]],
            "type": track["type"],
            "fit": track["fit"],
            "video_info": track["video_info"],
            "fit_crop_top_right_bottom_left": track["fit_crop"],
            "clips": track["clips"],
        }
        save_receipt(receipt_path, receipt)
        if track["type"] == "video" and track["fit"] == "cover":
            palmier.require("set_keyframes", {"projectId", "timelineId", "clipId", "property", "keyframes"})
            top, right, bottom, left = track["fit_crop"]
            for clip, placed in zip(track["clips"], added["clips"]):
                clip_id = placed.get("id")
                if not isinstance(clip_id, str) or not clip_id:
                    fail(f"Palmier omitted a stable clip ID while fitting {track['name']}")
                last = clip["end_frame"] - clip["start_frame"] - 1
                for prop, keyframes in (
                    ("crop", [[0, top, right, bottom, left, "linear"],
                              [last, top, right, bottom, left, "linear"]]),
                    ("scale", [[0, 1.0, 1.0, "linear"], [last, 1.0, 1.0, "linear"]]),
                    ("position", [[0, 0.0, 0.0, "linear"], [last, 0.0, 0.0, "linear"]]),
                ):
                    journal_call(palmier, receipt_path, receipt,
                                 f"fit {track['name']} {prop} / clip {clip_id}",
                                 "set_keyframes", {"projectId": project_id,
                                                   "timelineId": timeline_id,
                                                   "clipId": clip_id,
                                                   "property": prop,
                                                   "keyframes": keyframes})
        journal_call(palmier, receipt_path, receipt, f"name track {track['name']}",
                     "manage_tracks", {"projectId": project_id, "timelineId": timeline_id,
                                       "set": [{"trackId": track_id, "name": track["name"]}]})
        if track["type"] == "video":
            video_track_ids.append(track_id)

    # Auxiliary video approved overlays sit above the three paper planes.
    for target_index, track_id in enumerate(video_track_ids):
        state = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
        video_tracks = [x for x in state.get("tracks", []) if x.get("type") == "video"]
        current_index = next((i for i, x in enumerate(video_tracks) if x.get("trackId") == track_id), None)
        if current_index is None:
            fail("An auxiliary video track disappeared before stack verification")
        if current_index != target_index:
            journal_call(palmier, receipt_path, receipt, f"stack overlay at video index {target_index}",
                         "manage_tracks", {"projectId": project_id, "timelineId": timeline_id,
                                           "reorder": [{"trackId": track_id, "to": target_index}]})
    return video_track_ids


def capture_review_frames(palmier: Palmier, receipt_path: Path, receipt: dict,
                          project_id: str, timeline_id: str, config: dict) -> list[str]:
    visual_data = json.loads(config["visual_manifest"].read_text(encoding="utf-8"))
    frames = set()
    for scene in visual_data["scenes"]:
        start, end = scene["start_frame"], scene["end_frame"]
        frames.update({start, (start + end - 1) // 2, end - 1})
        if start > 0:
            frames.add(start - 1)
        if end < config["total_frames"]:
            frames.add(end)
    frame_dir = receipt_path.parent / f"{config['timeline_name']}_final_frames"
    frame_dir.mkdir(exist_ok=False)
    saved = []
    for frame in sorted(frames):
        response = palmier.raw("inspect_timeline", {"projectId": project_id,
                                                      "timelineId": timeline_id,
                                                      "startFrame": frame})
        images = [x for x in response.get("content", []) if x.get("type") == "image"]
        if len(images) != 1:
            fail(f"Palmier did not return one final composite for frame {frame}")
        destination = frame_dir / f"frame_{frame:06d}.png"
        destination.write_bytes(base64.b64decode(images[0]["data"]))
        saved.append(str(destination))
    receipt["final_review_frames"] = saved
    save_receipt(receipt_path, receipt)
    return saved


def probe(config: dict, episode_root: Path) -> dict:
    command = [sys.executable, str(REPO_ROOT / "channels/paper_detour/automation/assemble_paper_layers.py"),
               str(config["visual_manifest"]), "--episode-root", str(episode_root)]
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        fail("Visual manifest preflight failed: " + (result.stderr or result.stdout)[-4000:])
    visual_plan = json.loads(result.stdout)
    return {
        "valid": True,
        "project_name": config["project_name"],
        "timeline_name": config["timeline_name"],
        "frames": config["total_frames"],
        "seconds": config["total_frames"] / FPS,
        "auxiliary_tracks": [{"name": x["name"], "type": x["type"],
                              "clips": len(x["clips"]), "media": str(x["media"]),
                              "fit": x["fit"], "video_info": x["video_info"],
                              "fit_crop_top_right_bottom_left": x["fit_crop"]}
                             for x in config["auxiliary_tracks"]],
        "visual_plan": visual_plan,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--execute", action="store_true", help="Create the separate project and timeline")
    parser.add_argument("--show", action="store_true", help="Show the project after it is ready for review")
    args = parser.parse_args()
    try:
        config = resolve_config(args.manifest)
        receipt_path = args.manifest.resolve().with_name("build_paper_project_receipt.json")
        # Validate the full picture plan and its actual assets before creating any
        # project, even in execute mode. resolve_config alone checks only the wrapper.
        plan = probe(config, config["episode_root"])
        if not args.execute:
            print(json.dumps(plan, ensure_ascii=False, indent=2))
            return 0
        if receipt_path.exists():
            fail(f"Build receipt already exists; inspect state before retrying: {receipt_path}")
        if sha256(config["manifest_path"]) != config["manifest_sha256"]:
            fail("Build manifest changed after preflight")
        receipt = {
            "version": 1,
            "status": "preparing",
            "build_manifest": str(config["manifest_path"]),
            "build_manifest_sha256": config["manifest_sha256"],
            "visual_manifest": str(config["visual_manifest"]),
            "visual_manifest_sha256": sha256(config["visual_manifest"]),
            "project_name": config["project_name"],
            "timeline_name": config["timeline_name"],
            "frames": config["total_frames"],
            "visual_track_roles": plan["visual_plan"]["track_roles"],
            "exported": False,
            "published": False,
            "steps": [],
        }
        save_receipt(receipt_path, receipt)
        try:
            palmier = Palmier()
            project_id = create_project(palmier, receipt_path, receipt, config["project_name"])
            visual_receipt = run_visual_assembler(config, project_id, receipt_path, receipt)
            timeline_id = visual_receipt["timeline_id"]
            if config["auxiliary_tracks"]:
                receipt["status"] = "adding_audio_and_overlay_tracks"
                save_receipt(receipt_path, receipt)
                palmier = Palmier()
                add_auxiliary_tracks(config, palmier, receipt_path, receipt, project_id, timeline_id)
            palmier = Palmier()
            timeline = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
            if (timeline.get("width"), timeline.get("height"), timeline.get("fps"),
                    timeline.get("totalFrames")) != (1080, 1920, FPS, config["total_frames"]):
                fail("Final Palmier timeline metadata differs from the manifest")
            video_tracks = [x for x in timeline.get("tracks", []) if x.get("type") == "video"]
            audio_tracks = [x for x in timeline.get("tracks", []) if x.get("type") == "audio"]
            expected_video = (len(plan["visual_plan"]["track_roles"])
                              + sum(x["type"] == "video" for x in config["auxiliary_tracks"]))
            expected_audio = sum(x["type"] == "audio" for x in config["auxiliary_tracks"])
            if len(video_tracks) != expected_video or len(audio_tracks) != expected_audio:
                fail(f"Final track counts differ from the manifest (video={len(video_tracks)}, audio={len(audio_tracks)})")
            snapshot = journal_call(palmier, receipt_path, receipt, "save complete montage snapshot",
                                    "manage_snapshots", {"projectId": project_id,
                                                         "timelineId": timeline_id,
                                                         "action": "save",
                                                         "name": "Paper layer automation draft ready for review"})
            receipt["final_snapshot"] = snapshot
            receipt["status"] = "capturing_final_review_frames"
            save_receipt(receipt_path, receipt)
            final_frames = capture_review_frames(palmier, receipt_path, receipt,
                                                 project_id, timeline_id, config)
            receipt.update({"status": "ready_for_review", "final_review_frames_count": len(final_frames),
                            "visible_project_switched": receipt.get("visible_project_switched", False),
                            "existing_timelines_modified": False,
                            "exported": False, "published": False})
            save_receipt(receipt_path, receipt)
            if args.show:
                journal_call(palmier, receipt_path, receipt, "show separate project for review",
                             "manage_project", {"action": "show", "id": project_id})
                receipt["shown_for_review"] = True
                save_receipt(receipt_path, receipt)
            print(json.dumps({"status": receipt["status"], "project_name": config["project_name"],
                              "project_id": project_id, "timeline_name": config["timeline_name"],
                              "timeline_id": timeline_id, "frames": config["total_frames"],
                              "seconds": config["total_frames"] / FPS,
                              "review_frames": len(final_frames), "receipt": str(receipt_path),
                              "exported": False, "published": False}, ensure_ascii=False, indent=2))
            return 0
        except Exception as exc:
            receipt.update({"status": "stopped_inspect_before_retry", "error": str(exc)})
            save_receipt(receipt_path, receipt)
            raise
    except Exception as exc:
        print(f"Paper project build stopped: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
