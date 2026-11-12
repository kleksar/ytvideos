#!/usr/bin/env python3
"""Place prepared Paper Detour stills or legacy BG/MG/FG sets on a fresh timeline.

Default mode only validates the image package and prints a plan. --execute uses
Palmier Pro 0.12+ MCP calls, each addressed by explicit projectId/timelineId.
It can clone a source timeline while preserving explicitly named audio/graphics
tracks, but never edits that source. It never switches the visible project or
timeline, closes a project, renders, or uses AI credits. An uncertain/failed MCP
mutation is journaled and stops; inspect the receipt and Palmier before retrying.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import os
import re
import sys
from pathlib import Path

FPS = 30
POSITION_EASING = "smooth"
TRACK_ORDER = ("foreground", "middle", "background")  # Palmier track 0 is top.
LAYER_SPEED = {"background": 0.35, "middle": 0.65, "foreground": 2.0}
MOTION_RATE = 0.016  # normalized canvas widths per second, before layer multiplier
EDGE_COVER_MARGIN = 0.005
MAX_OVERSCAN = 1.22
OVERSCAN_REFERENCE_SPEED = 1.0
MOTION_DIRECTIONS = {"left_to_right", "right_to_left"}
MOTION_DIRECTIONS_WITH_STATIC = MOTION_DIRECTIONS | {"static"}
ANCHOR_SIDES = {"left", "right", "center"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def png_info(path: Path) -> dict:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required to inspect PNG alpha channels") from exc
    try:
        with Image.open(path) as image:
            image.load()
            if image.format != "PNG":
                raise ValueError(f"Expected PNG: {path}")
            info = {"width": image.width, "height": image.height, "mode": image.mode}
            if "A" in image.getbands():
                low, high = image.getchannel("A").getextrema()
                info["alpha_min"], info["alpha_max"] = low, high
            else:
                info["alpha_min"], info["alpha_max"] = None, None
            return info
    except Exception as exc:
        raise ValueError(f"Cannot read PNG {path}: {exc}") from exc


def episode_root(manifest: Path, configured: str | None) -> Path:
    root = Path(configured).resolve() if configured else manifest.resolve().parents[2]
    if not root.is_dir():
        raise ValueError(f"Episode root does not exist: {root}")
    return root


def validate(manifest_path: Path, root: Path) -> tuple[dict, Path]:
    manifest_path = manifest_path.resolve()
    if not manifest_path.is_file():
        raise ValueError(f"Manifest does not exist: {manifest_path}")
    if not manifest_path.is_relative_to(root):
        raise ValueError("Manifest must be inside the episode directory")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("version") != 1:
        raise ValueError("Manifest version must be 1")
    direction_rules_version = data.get("direction_rules_version")
    if direction_rules_version not in (None, 1):
        raise ValueError("direction_rules_version must be 1 when supplied")
    timeline_name = data.get("timeline_name")
    if not isinstance(timeline_name, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", timeline_name):
        raise ValueError("timeline_name must use 1-80 letters, numbers, underscores, or hyphens")
    fps = data.get("fps", FPS)
    if fps != FPS:
        raise ValueError(f"This Paper Detour assembler currently expects {FPS} fps")
    canvas = data.get("canvas")
    if canvas != {"width": 1080, "height": 1920}:
        raise ValueError("Paper Detour Shorts manifest canvas must be 1080x1920")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("Manifest needs at least one scene")
    base_timeline_id = data.get("base_timeline_id")
    if base_timeline_id is not None and (
        not isinstance(base_timeline_id, str)
        or not re.fullmatch(r"[A-Za-z0-9-]{6,64}", base_timeline_id)
    ):
        raise ValueError("base_timeline_id must be an exact Palmier timeline ID")
    preserve_tracks = data.get("preserve_tracks", {})
    overlay_track_names = data.get("overlay_track_names", [])
    if base_timeline_id:
        if not isinstance(preserve_tracks, dict) or not preserve_tracks:
            raise ValueError("Cloning a timeline requires an explicit preserve_tracks name-to-type map")
        if any(not isinstance(name, str) or not name for name in preserve_tracks):
            raise ValueError("preserve_tracks names must be non-empty strings")
        if any(kind not in {"audio", "video"} for kind in preserve_tracks.values()):
            raise ValueError("preserve_tracks values must be 'audio' or 'video'")
        if (not isinstance(overlay_track_names, list)
                or any(name not in preserve_tracks for name in overlay_track_names)
                or any(preserve_tracks[name] != "video" for name in overlay_track_names)):
            raise ValueError("overlay_track_names must name preserved video tracks that stay above the new layers")
    elif preserve_tracks or overlay_track_names:
        raise ValueError("preserve_tracks and overlay_track_names require base_timeline_id")

    last_end = 0
    used_ids = set()
    resolved = []
    for scene in scenes:
        scene_id = scene.get("id")
        start, end = scene.get("start_frame"), scene.get("end_frame")
        if not isinstance(scene_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", scene_id):
            raise ValueError("Every scene needs a unique, safe id")
        if scene_id in used_ids:
            raise ValueError(f"Duplicate scene id: {scene_id}")
        used_ids.add(scene_id)
        motion_direction = scene.get("motion_direction")
        allowed_directions = (MOTION_DIRECTIONS_WITH_STATIC if direction_rules_version == 1
                              else MOTION_DIRECTIONS)
        if motion_direction not in allowed_directions:
            expected = "left_to_right, right_to_left, or static" if direction_rules_version == 1 else "left_to_right or right_to_left"
            raise ValueError(f"{scene_id} needs one explicit motion_direction: {expected}")
        speed_multipliers = scene.get("speed_multipliers", {})
        if (not isinstance(speed_multipliers, dict)
                or any(role not in TRACK_ORDER for role in speed_multipliers)
                or any(type(value) not in (int, float) or not math.isfinite(value) or value < 0 or value > 2
                       for value in speed_multipliers.values())):
            raise ValueError(f"{scene_id} speed_multipliers must be role values from 0 to 2")
        foreground_anchor_side = scene.get("foreground_anchor_side")
        direction_exception_reason = scene.get("direction_exception_reason")
        if direction_rules_version == 1:
            if foreground_anchor_side not in ANCHOR_SIDES:
                raise ValueError(f"{scene_id} needs foreground_anchor_side: left, right, or center")
            if (direction_exception_reason is not None
                    and (not isinstance(direction_exception_reason, str) or not direction_exception_reason.strip())):
                raise ValueError(f"{scene_id} direction_exception_reason must be a non-empty explanation")
            all_stationary = all(speed_multipliers.get(role, 1.0) == 0 for role in TRACK_ORDER)
            if motion_direction == "static":
                if any(speed_multipliers.get(role, 1.0) != 0 for role in TRACK_ORDER):
                    raise ValueError(f"{scene_id} static motion_direction requires zero speed for all three layers")
            elif all_stationary:
                raise ValueError(f"{scene_id} has zero movement; declare motion_direction='static'")
            expected_direction = {"left": "right_to_left", "right": "left_to_right"}.get(foreground_anchor_side)
            if (motion_direction != "static"
                    and expected_direction is not None
                    and motion_direction != expected_direction
                    and not direction_exception_reason):
                raise ValueError(
                    f"{scene_id} motion conflicts with its {foreground_anchor_side} FG anchor; "
                    "recompose or document direction_exception_reason"
                )
            if (motion_direction != "static" and foreground_anchor_side == "center"
                    and not direction_exception_reason):
                raise ValueError(f"{scene_id} centered FG anchor needs a direction_exception_reason")
        layer_framing = scene.get("layer_framing", {})
        if not isinstance(layer_framing, dict):
            raise ValueError(f"{scene_id} layer_framing must be an object")
        if layer_framing:
            if set(layer_framing) != set(TRACK_ORDER):
                raise ValueError(f"{scene_id} layer_framing must define background, middle, and foreground")
            for role, framing in layer_framing.items():
                if not isinstance(framing, dict) or set(framing) != {"scale", "x_px", "y_px"}:
                    raise ValueError(f"{scene_id} {role} layer_framing needs scale, x_px, y_px")
                if (type(framing["scale"]) not in (int, float)
                        or not math.isfinite(framing["scale"])
                        or not 0 < framing["scale"] <= MAX_OVERSCAN
                        or any(type(framing[key]) not in (int, float)
                               or not math.isfinite(framing[key])
                               for key in ("x_px", "y_px"))):
                    raise ValueError(f"{scene_id} {role} framing values must be finite; scale must be 0–{MAX_OVERSCAN}")
        framing_match_scene_id = scene.get("framing_match_scene_id")
        if framing_match_scene_id is not None and (
            not isinstance(framing_match_scene_id, str)
            or not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", framing_match_scene_id)
            or framing_match_scene_id == scene_id
        ):
            raise ValueError(f"{scene_id} framing_match_scene_id must name another scene")
        if type(start) is not int or type(end) is not int or start != last_end or end <= start:
            raise ValueError(f"Scenes must be contiguous [start_frame,end_frame): {scene_id}")
        master = resolve_asset(root, scene.get("master"), f"{scene_id} master")
        master_info = png_info(master)
        image_aspect = master_info["width"] / master_info["height"]
        if abs(image_aspect - 9 / 16) > 0.006:
            raise ValueError(f"Master is not a 9:16 image: {master}")
        layers = {}
        hashes = {str(master): sha256(master)}
        static_plate = scene.get("static_plate")
        layer_paths = scene.get("layers")
        if static_plate is not None:
            reason = scene.get("static_plate_reason")
            if motion_direction != "static" or not isinstance(reason, str) or not reason.strip():
                raise ValueError(f"{scene_id} static_plate requires static motion and a reason")
            if layer_paths is not None or layer_framing or framing_match_scene_id:
                raise ValueError(f"{scene_id} static_plate cannot also define layers, layer framing, or loop matching")
            plate = resolve_asset(root, static_plate, f"{scene_id} static_plate")
            plate_info = png_info(plate)
            if (plate_info["width"], plate_info["height"]) != (master_info["width"], master_info["height"]):
                raise ValueError(f"{scene_id} static plate canvas differs from its master")
            if plate_info["alpha_min"] is not None and plate_info["alpha_min"] < 255:
                raise ValueError(f"{scene_id} static plate must be fully opaque: {plate}")
            plate_hash = sha256(plate)
            if plate_hash != hashes[str(master)]:
                raise ValueError(f"{scene_id} static plate must reuse the exact master file")
            layers["background"] = {"path": plate, "info": plate_info}
            hashes[str(plate)] = plate_hash
        else:
            if not isinstance(layer_paths, dict) or set(layer_paths) != {"background", "middle", "foreground"}:
                raise ValueError(f"Scene {scene_id} must contain background, middle, foreground paths")
            for role, value in layer_paths.items():
                path = resolve_asset(root, value, f"{scene_id} {role}")
                info = png_info(path)
                if (info["width"], info["height"]) != (master_info["width"], master_info["height"]):
                    raise ValueError(f"{scene_id} {role} canvas differs from its master")
                if role == "background":
                    if info["alpha_min"] is not None and info["alpha_min"] < 255:
                        raise ValueError(f"Background must be fully opaque: {path}")
                elif (info["alpha_min"] is None or info["alpha_max"] is None
                      or info["alpha_min"] == 255 or info["alpha_max"] == 0):
                    raise ValueError(f"{role} must have actual transparent pixels: {path}")
                layers[role] = {"path": path, "info": info}
                hashes[str(path)] = sha256(path)
        resolved.append({
            "id": scene_id,
            "start_frame": start,
            "end_frame": end,
            "motion_direction": motion_direction,
            "foreground_anchor_side": foreground_anchor_side,
            "direction_exception_reason": direction_exception_reason,
            "speed_multipliers": speed_multipliers,
            "layer_framing": layer_framing,
            "framing_match_scene_id": framing_match_scene_id,
            "master": {"path": master, "info": master_info},
            "layers": layers,
            "is_static_plate": static_plate is not None,
            "static_plate_reason": scene.get("static_plate_reason"),
            "hashes": hashes,
        })
        last_end = end

    if direction_rules_version == 1:
        for previous, current in zip(resolved, resolved[1:]):
            if (previous["motion_direction"] != "static"
                    and current["motion_direction"] != "static"
                    and previous["motion_direction"] == current["motion_direction"]
                    and not current.get("direction_exception_reason")):
                raise ValueError(
                    f"{previous['id']} and {current['id']} repeat direction; "
                    f"recompose or document {current['id']} direction_exception_reason"
                )

    scenes_by_id = {scene["id"]: scene for scene in resolved}
    for scene in resolved:
        framing_scene = scenes_by_id.get(scene.get("framing_match_scene_id"), scene)
        framing_seconds = (framing_scene["end_frame"] - framing_scene["start_frame"]) / FPS
        height = (1.0 if scene["is_static_plate"] else
                  1 + 2 * (MOTION_RATE * framing_seconds * OVERSCAN_REFERENCE_SPEED + EDGE_COVER_MARGIN))
        if not scene["layer_framing"] and height > MAX_OVERSCAN:
            raise ValueError(f"Motion needs more than {(MAX_OVERSCAN - 1):.0%} overscan in {scene['id']}")
        match_id = scene.get("framing_match_scene_id")
        if match_id is None:
            continue
        reference = scenes_by_id.get(match_id)
        if reference is None or reference["start_frame"] >= scene["start_frame"]:
            raise ValueError(f"{scene['id']} must match the framing of an earlier scene")
        if scene["is_static_plate"] or reference["is_static_plate"]:
            raise ValueError("A static plate cannot be used as a layered loop match")
        if scene["hashes"] != reference["hashes"]:
            raise ValueError(f"{scene['id']} must reuse the exact master and three layers of {match_id}")
        if scene["layer_framing"] != reference["layer_framing"]:
            raise ValueError(f"{scene['id']} must reuse the exact layer framing of {match_id}")
        if any(scene["speed_multipliers"].get(role, 1.0) != 0 for role in TRACK_ORDER):
            raise ValueError(f"{scene['id']} must hold all three layers to close the visual loop")

    receipt_path = manifest_path.with_name(f"{timeline_name}_palmier_receipt.json")
    if receipt_path.exists():
        raise ValueError(f"Receipt already exists; inspect before retrying: {receipt_path}")
    track_roles = [role for role in TRACK_ORDER
                   if any(role in scene["layers"] for scene in resolved)]
    return {"version": 1, "direction_rules_version": direction_rules_version,
            "timeline_name": timeline_name, "fps": fps,
            "canvas": canvas,
            "frames": last_end, "scenes": resolved, "track_roles": track_roles,
            "manifest_path": manifest_path,
            "manifest_sha256": sha256(manifest_path),
            "base_timeline_id": base_timeline_id,
            "preserve_tracks": preserve_tracks,
            "overlay_track_names": overlay_track_names}, receipt_path


def resolve_asset(root: Path, value: str | None, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"Missing path for {label}")
    path = (root / value).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"Missing or outside-episode file for {label}: {path}")
    if path.suffix.lower() != ".png":
        raise ValueError(f"Paper layers must be PNG: {path}")
    return path


def save_receipt(path: Path, receipt: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)
    dir_fd = os.open(str(path.parent), os.O_RDONLY)
    try:
        os.fsync(dir_fd)
    finally:
        os.close(dir_fd)


class Palmier:
    def __init__(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "automation/palmier"))
        from inspect_connection import PalmierConnection
        self.client = PalmierConnection()
        self.client.connect()
        self.tools = {x["name"]: x for x in self.client.request("tools/list").get("tools", [])}
        self.require_current_api()

    def require_current_api(self):
        required = {
            "get_timeline": {"projectId", "timelineId"},
            "create_timeline": {"projectId"},
            "import_media": {"projectId", "source"},
            "add_clips": {"projectId", "timelineId", "entries"},
            "set_keyframes": {"projectId", "timelineId", "clipId", "property", "keyframes"},
            "manage_tracks": {"projectId", "timelineId"},
            "inspect_timeline": {"projectId", "timelineId"},
            "manage_snapshots": {"projectId", "timelineId", "action"},
        }
        for name, keys in required.items():
            tool = self.tools.get(name)
            if not tool:
                raise RuntimeError(f"Palmier MCP lacks {name}; refresh tool schemas")
            actual = set(tool.get("inputSchema", {}).get("required", []))
            if not keys.issubset(actual):
                raise RuntimeError(f"Palmier {name} schema is not 0.12+ ID-scoped; no edits attempted")
        description = self.tools["set_keyframes"].get("description", "")
        if "smooth" not in description or "TOP-LEFT" not in description:
            raise RuntimeError("Palmier keyframe schema changed; review motion coordinates before editing")

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


def journal_call(palmier: Palmier, receipt_path: Path, receipt: dict, label: str,
                 tool: str, args: dict) -> dict:
    receipt["pending"] = {"label": label, "tool": tool, "args": args}
    save_receipt(receipt_path, receipt)
    result = palmier.call(tool, args)
    receipt["steps"].append({"label": label, "tool": tool,
                             "actionId": result.get("actionId"), "result": result})
    receipt.pop("pending", None)
    save_receipt(receipt_path, receipt)
    return result


def execute(data: dict, receipt_path: Path, project_id: str, receipt: dict):
    if not re.fullmatch(r"[A-Za-z0-9-]{8,64}", project_id):
        raise ValueError("Pass an exact Palmier projectId from manage_project action=list")
    if sha256(data["manifest_path"]) != data["manifest_sha256"]:
        raise ValueError("Manifest changed after validation; no Palmier edits attempted")
    palmier = Palmier()
    project_list = palmier.call("manage_project", {"action": "list"})
    projects = project_list.get("projects", [])
    project = next((x for x in projects if x.get("id") == project_id), None)
    if not project or not project.get("isAccessible"):
        raise ValueError("Project ID was not found or is not accessible")
    if not project.get("isOpen"):
        journal_call(palmier, receipt_path, receipt, "open project in background",
                     "manage_project", {"action": "open", "id": project_id})

    inventory = palmier.call("get_media", {"projectId": project_id})
    if any(x.get("name") == data["timeline_name"] for x in inventory.get("timelines", [])):
        raise ValueError("A timeline with this name already exists; choose a fresh name")
    batch_id = data["timeline_name"]
    media_folder = f"PaperLayers/{batch_id}"
    if media_folder in inventory.get("folders", []):
        raise ValueError(f"Media folder already exists; inspect before retrying: {media_folder}")

    receipt.update({"status": "started", "project_id": project_id,
                    "project_name": project.get("name"), "timeline_name": data["timeline_name"],
                    "manifest": str(data["manifest_path"]),
                    "manifest_sha256": data["manifest_sha256"], "frames": data["frames"],
                    "base_timeline_id": data.get("base_timeline_id"),
                    "preserve_tracks": data.get("preserve_tracks", {}),
                    "scenes": [x["id"] for x in data["scenes"]], "media_folder": media_folder,
                    "media": {}, "clips": {}, "steps": []})
    save_receipt(receipt_path, receipt)

    create_args = {"projectId": project_id, "name": data["timeline_name"]}
    if data.get("base_timeline_id"):
        create_args["from"] = data["base_timeline_id"]
    created = journal_call(palmier, receipt_path, receipt, "create isolated timeline",
                           "create_timeline", create_args)
    timeline_id = created.get("timelineId")
    if not isinstance(timeline_id, str) or not timeline_id:
        raise RuntimeError("Timeline creation response omitted timelineId; inspect receipt and Palmier")
    receipt["timeline_id"] = timeline_id
    save_receipt(receipt_path, receipt)
    current = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
    if (current.get("width"), current.get("height"), current.get("fps")) != (1080, 1920, FPS):
        raise RuntimeError("New timeline is not 1080x1920/30; inspect before proceeding")
    if data.get("base_timeline_id"):
        if current.get("totalFrames", 0) != data["frames"]:
            raise RuntimeError("Cloned timeline duration differs from the manifest; inspect before proceeding")
    elif current.get("tracks") or current.get("totalFrames", 0) != 0:
        raise RuntimeError("New timeline is not empty; inspect before proceeding")
    snapshot_name = ("Before Paper layer rebuild" if data.get("base_timeline_id")
                     else "Before Paper layer build")
    journal_call(palmier, receipt_path, receipt, "snapshot source timeline copy",
                 "manage_snapshots", {"projectId": project_id, "timelineId": timeline_id,
                                      "action": "save", "name": snapshot_name})

    if data.get("base_timeline_id"):
        tracks = current.get("tracks", [])
        preserve = data["preserve_tracks"]
        preserved_by_name = {}
        for name, expected_type in preserve.items():
            matches = [track for track in tracks
                       if (track.get("name") or track.get("label")) == name]
            if len(matches) != 1 or matches[0].get("type") != expected_type:
                raise RuntimeError(
                    f"Expected exactly one preserved {expected_type} track named {name}; no tracks removed"
                )
            preserved_by_name[name] = matches[0]
        preserved_ids = {track["trackId"] for track in preserved_by_name.values()}
        if len(preserved_ids) != len(preserve) or any(not track_id for track_id in preserved_ids):
            raise RuntimeError("Could not identify stable IDs for all preserved tracks; no tracks removed")
        remove = [{"trackId": track["trackId"]} for track in tracks
                  if track.get("trackId") not in preserved_ids]
        if remove:
            journal_call(palmier, receipt_path, receipt, "remove old picture tracks from timeline copy",
                         "manage_tracks", {"projectId": project_id, "timelineId": timeline_id,
                                           "remove": remove})
        cleaned = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
        cleaned_tracks = cleaned.get("tracks", [])
        cleaned_ids = {track.get("trackId") for track in cleaned_tracks}
        if cleaned_ids != preserved_ids:
            raise RuntimeError("Timeline copy track IDs differ from the explicit preserved set")
        expected_type_by_id = {track["trackId"]: preserve[name]
                               for name, track in preserved_by_name.items()}
        if any(track.get("type") != expected_type_by_id.get(track.get("trackId"))
               for track in cleaned_tracks):
            raise RuntimeError("Timeline copy changed a preserved track type")
        cleaned_by_id = {track.get("trackId"): track for track in cleaned_tracks}
        restore_labels = [{"trackId": track_id, "name": name}
                          for name, original_track in preserved_by_name.items()
                          for track_id in [original_track["trackId"]]
                          if cleaned_by_id[track_id].get("name") != name
                          and cleaned_by_id[track_id].get("label") != name]
        if restore_labels:
            journal_call(palmier, receipt_path, receipt, "restore preserved track labels after renumbering",
                         "manage_tracks", {"projectId": project_id, "timelineId": timeline_id,
                                           "set": restore_labels})
            cleaned = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
        cleaned_names = {(track.get("name") or track.get("label")) for track in cleaned.get("tracks", [])}
        if cleaned_names != set(preserve):
            raise RuntimeError("Timeline copy does not contain exactly the preserved audio/graphics tracks")
        if cleaned.get("totalFrames", 0) != data["frames"]:
            raise RuntimeError("Removing picture tracks changed the preserved timeline duration")

    paths_by_role = {role: [] for role in TRACK_ORDER}
    for scene in data["scenes"]:
        for role, layer in scene["layers"].items():
            paths_by_role[role].append(layer["path"])
    unique_paths = list(dict.fromkeys(p for role in TRACK_ORDER for p in paths_by_role[role]))
    expected_hashes = {path: digest for scene in data["scenes"]
                       for path, digest in scene["hashes"].items()}
    for path in unique_paths:
        if sha256(path) != expected_hashes[str(path)]:
            raise RuntimeError(f"Source changed after validation: {path}")
        result = journal_call(palmier, receipt_path, receipt, f"import {path.name}",
                              "import_media", {"projectId": project_id,
                                               "source": {"path": str(path)},
                                               "folder": media_folder})
        media_ref = result.get("mediaRef") or result.get("assetId") or result.get("id")
        if not isinstance(media_ref, str) or not media_ref:
            raise RuntimeError("Import response omitted the asset ID; inspect receipt before retrying")
        receipt["media"][str(path)] = media_ref
        save_receipt(receipt_path, receipt)

    role_to_track = {}
    receipt["clip_by_scene"] = {}
    for role in ("background", "middle", "foreground"):
        scenes_with_role = [scene for scene in data["scenes"] if role in scene["layers"]]
        entries = [{"mediaRef": receipt["media"][str(scene["layers"][role]["path"])],
                    "startFrame": scene["start_frame"], "endFrame": scene["end_frame"],
                    "includeAudio": False} for scene in scenes_with_role]
        if not entries:
            continue
        result = journal_call(palmier, receipt_path, receipt, f"place {role} layer", "add_clips",
                              {"projectId": project_id, "timelineId": timeline_id, "entries": entries})
        expected = len(entries)
        if len(result.get("clips", [])) != expected:
            raise RuntimeError(f"Palmier placed an unexpected number of {role} clips")
        new_tracks = result.get("createdTracks", [])
        if len(new_tracks) != 1 or not new_tracks[0].get("trackId"):
            raise RuntimeError(f"Could not identify one new {role} track from Palmier's add_clips receipt")
        role_to_track[role] = new_tracks[0]["trackId"]
        receipt["clips"][role] = [x["id"] for x in result["clips"]]
        for scene, clip in zip(scenes_with_role, result["clips"]):
            receipt["clip_by_scene"].setdefault(scene["id"], {})[role] = clip["id"]
        receipt["tracks"] = role_to_track
        save_receipt(receipt_path, receipt)

    # Keep preserved overlay tracks  above the new layers.
    expected_video_order = []
    state = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
    for name in data.get("overlay_track_names", []):
        matches = [track for track in state.get("tracks", [])
                   if (track.get("name") or track.get("label")) == name and track.get("type") == "video"]
        if len(matches) != 1:
            raise RuntimeError(f"Expected one preserved overlay video track named {name}")
        expected_video_order.append(matches[0]["trackId"])
    expected_video_order.extend(role_to_track[role] for role in TRACK_ORDER if role in role_to_track)
    for target_index, expected_track_id in enumerate(expected_video_order):
        state = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
        video_tracks = [track for track in state.get("tracks", []) if track.get("type") == "video"]
        if len(video_tracks) != len(expected_video_order):
            raise RuntimeError("Unexpected video track count after placing Paper layers")
        current_index = next((i for i, track in enumerate(video_tracks)
                              if track.get("trackId") == expected_track_id), None)
        if current_index is None:
            raise RuntimeError(f"Track disappeared before stacking: {role}")
        if current_index != target_index:
            track_label = next(role for role, track_id in role_to_track.items()
                               if track_id == expected_track_id) if expected_track_id in role_to_track.values() else "overlay"
            journal_call(palmier, receipt_path, receipt, f"stack {track_label} at video index {target_index}",
                         "manage_tracks", {"projectId": project_id, "timelineId": timeline_id,
                                           "reorder": [{"trackId": expected_track_id,
                                                        "to": target_index}]})
    for role in TRACK_ORDER:
        if role not in role_to_track:
            continue
        state = palmier.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
        tracks = state.get("tracks", [])
        current_track = next((track for track in tracks if track.get("trackId") == role_to_track[role]), None)
        if current_track is None:
            raise RuntimeError(f"Track disappeared before naming: {role}")
        journal_call(palmier, receipt_path, receipt, f"name {role} track", "manage_tracks",
                     {"projectId": project_id, "timelineId": timeline_id,
                      "set": [{"trackId": role_to_track[role], "name": role.title()}]})

    canvas_aspect = 9 / 16
    for scene in data["scenes"]:
        duration = scene["end_frame"] - scene["start_frame"]
        seconds = duration / FPS
        # Keep the shared framing at the baseline scale. Faster transparent planes
        # can reveal lower layers as they travel; scaling every plane up would turn
        # foreground speed into an unwanted whole-frame zoom.
        framing_scene = next(
            (candidate for candidate in data["scenes"]
             if candidate["id"] == scene.get("framing_match_scene_id")),
            scene,
        )
        framing_seconds = (framing_scene["end_frame"] - framing_scene["start_frame"]) / FPS
        height = (1.0 if scene["is_static_plate"] else
                  1 + 2 * (MOTION_RATE * framing_seconds * OVERSCAN_REFERENCE_SPEED + EDGE_COVER_MARGIN))
        if not scene["layer_framing"] and height > MAX_OVERSCAN:
            raise RuntimeError(f"Motion needs more than {(MAX_OVERSCAN - 1):.0%} overscan in {scene['id']}")
        for role in TRACK_ORDER:
            if role not in scene["layers"]:
                continue
            info = scene["layers"][role]["info"]
            framing = scene["layer_framing"].get(role)
            if framing:
                layer_height = framing["scale"]
                width = layer_height * (info["width"] / info["height"]) / canvas_aspect
                left = framing["x_px"] / info["width"]
                top = framing["y_px"] / info["height"]
            else:
                layer_height = height
                width = height * (info["width"] / info["height"]) / canvas_aspect
                left, top = (1 - width) / 2, (1 - height) / 2
            drift = (MOTION_RATE * seconds * LAYER_SPEED[role]
                     * scene.get("speed_multipliers", {}).get(role, 1.0))
            end_left = (left if scene["motion_direction"] == "static"
                        else left + drift if scene["motion_direction"] == "left_to_right"
                        else left - drift)
            clip_id = receipt["clip_by_scene"][scene["id"]][role]
            last = duration - 1
            journal_call(palmier, receipt_path, receipt, f"scale {role} / {scene['id']}",
                         "set_keyframes", {"projectId": project_id, "timelineId": timeline_id,
                                           "clipId": clip_id, "property": "scale",
                                           "keyframes": [[0, width, layer_height, "linear"]]
                                           + ([[last, width, layer_height, "linear"]] if last else [])})
            journal_call(palmier, receipt_path, receipt, f"drift {role} / {scene['id']}",
                         "set_keyframes", {"projectId": project_id, "timelineId": timeline_id,
                                           "clipId": clip_id, "property": "position",
                                           "keyframes": [[0, left, top, POSITION_EASING]]
                                           + ([[last, end_left, top, POSITION_EASING]] if last else [])})

    # Inspect cut edges plus one-second samples so motion gaps are less likely to hide between thirds.
    review_dir = receipt_path.parent / f"{data['timeline_name']}_frames"
    review_dir.mkdir(exist_ok=False)
    inspected = []
    for scene in data["scenes"]:
        sample_frames = {scene["start_frame"], scene["end_frame"] - 1}
        sample_frames.update(range(scene["start_frame"] + FPS, scene["end_frame"], FPS))
        if scene["start_frame"] > 0:
            sample_frames.add(scene["start_frame"] - 1)
        for frame in sorted(sample_frames):
            response = palmier.raw("inspect_timeline", {"projectId": project_id,
                                                          "timelineId": timeline_id,
                                                          "startFrame": frame})
            images = [x for x in response.get("content", []) if x.get("type") == "image"]
            if len(images) != 1:
                raise RuntimeError(f"No single composited image returned at frame {frame}")
            output = review_dir / f"frame_{frame:06d}.png"
            output.write_bytes(base64.b64decode(images[0]["data"]))
            inspected.append(str(output))
    receipt.update({"status": "ready_for_review", "review_frames": inspected,
                    "visible_project_switched": False, "existing_timelines_modified": False,
                    "exported": False})
    save_receipt(receipt_path, receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--episode-root")
    parser.add_argument("--execute", action="store_true", help="Create a new isolated timeline in Palmier")
    parser.add_argument("--project-id", help="Exact project ID from Palmier manage_project/list")
    args = parser.parse_args()
    root = episode_root(args.manifest, args.episode_root)
    data, receipt_path = validate(args.manifest, root)
    if not args.execute:
        print(json.dumps({"valid": True, "timeline": data["timeline_name"],
                          "frames": data["frames"], "seconds": data["frames"] / FPS,
                          "canvas": data["canvas"],
                          "track_roles": data["track_roles"],
                          "scenes": [{"id": x["id"], "start": x["start_frame"],
                                      "end": x["end_frame"], "canvas": x["master"]["info"]}
                                     for x in data["scenes"]],
                          "receipt": str(receipt_path)}, ensure_ascii=False, indent=2))
        return
    if not args.project_id:
        parser.error("--project-id is required with --execute")
    receipt = {"status": "preparing", "manifest": str(data["manifest_path"]),
               "manifest_sha256": data["manifest_sha256"], "steps": []}
    # Exclusive create: a partial receipt must be inspected rather than overwritten.
    with receipt_path.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    try:
        final = execute(data, receipt_path, args.project_id, receipt)
        print(json.dumps({"status": final["status"], "project_id": final["project_id"],
                          "timeline_id": final["timeline_id"], "receipt": str(receipt_path),
                          "review_frames": final["review_frames"]}, ensure_ascii=False, indent=2))
    except BaseException as exc:
        receipt["status"] = "stopped_inspect_before_retry"
        receipt["error"] = repr(exc)
        save_receipt(receipt_path, receipt)
        raise


if __name__ == "__main__":
    main()
