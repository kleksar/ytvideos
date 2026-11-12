#!/usr/bin/env python3
"""Normalize Paper phrase-overlay geometry in a Palmier timeline.

The tool reads one timeline and its media inventory through Palmier MCP, measures
visible alpha bounds in the approved PNG assets, and plans one cap height per
line. It changes only accent image transforms and position keyframes. Scene,
voice, timing, opacity curves, and image files remain untouched.

Requires Pillow. Run without --apply for a dry-run report. Palmier MCP URL and
session can be passed with --mcp-url/--session-id or PALMIER_MCP_URL /
PALMIER_MCP_SESSION_ID.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import subprocess
import sys
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Any

from PIL import Image

try:
    import numpy as np
except ImportError:  # Pillow-only fallback for minimal environments.
    np = None


DEFAULT_MCP_URL = "http://127.0.0.1:19789/mcp"
DEFAULT_SAFE_WIDTH_RATIO = 0.90
DEFAULT_ENTRY_Y = 0.20
DEFAULT_HOLD_Y = 0.18
DEFAULT_EXIT_Y = 0.16


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--timeline-id", required=True)
    parser.add_argument("--asset-root", required=True, type=Path)
    parser.add_argument("--mcp-url", default=os.environ.get("PALMIER_MCP_URL", DEFAULT_MCP_URL))
    parser.add_argument("--session-id", default=os.environ.get("PALMIER_MCP_SESSION_ID"))
    parser.add_argument("--safe-width-ratio", type=float, default=DEFAULT_SAFE_WIDTH_RATIO)
    parser.add_argument("--target-cap-height", type=float, help="Override the computed cap height in canvas pixels.")
    parser.add_argument("--line-counts-json", type=Path, help="JSON map of asset name to authored line count.")
    parser.add_argument("--entry-y", type=float, default=DEFAULT_ENTRY_Y)
    parser.add_argument("--hold-y", type=float, default=DEFAULT_HOLD_Y)
    parser.add_argument("--exit-y", type=float, default=DEFAULT_EXIT_Y)
    parser.add_argument("--apply", action="store_true", help="Save a timeline snapshot and apply the geometry changes.")
    parser.add_argument("--report", type=Path, help="Optional path for a JSON report.")
    return parser.parse_args()


def call_mcp(url: str, session_id: str, name: str, arguments: dict[str, Any], request_id: int) -> dict[str, Any]:
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    result = subprocess.run(
        [
            "curl",
            "-sS",
            "--max-time",
            "30",
            "-H",
            "Content-Type: application/json",
            "-H",
            "Accept: application/json, text/event-stream",
            "-H",
            f"Mcp-Session-Id: {session_id}",
            "-X",
            "POST",
            url,
            "--data-binary",
            json.dumps(payload),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    messages = [line[6:] for line in result.stdout.splitlines() if line.startswith("data: {")]
    if not messages:
        raise RuntimeError(f"Palmier MCP returned no message for {name}: {result.stdout[-500:]}")
    response = json.loads(messages[-1])
    if "error" in response:
        raise RuntimeError(f"Palmier MCP {name} failed: {response['error']}")
    tool_result = response.get("result", {})
    if tool_result.get("isError"):
        detail = "\n".join(item.get("text", "") for item in tool_result.get("content", []))
        raise RuntimeError(f"Palmier MCP {name} failed: {detail}")
    return tool_result


def result_text(result: dict[str, Any]) -> str:
    for item in result.get("content", []):
        if item.get("type") == "text":
            return item["text"]
    raise RuntimeError("Palmier MCP response did not contain text data")


@lru_cache(maxsize=1024)
def image_bounds(path: str) -> tuple[int, int, tuple[int, int, int, int], tuple[int, int, int, int]]:
    with Image.open(path) as source:
        rgba = source.convert("RGBA")
        alpha_bounds = rgba.getchannel("A").getbbox()
        if alpha_bounds is None:
            raise ValueError(f"PNG has no visible alpha pixels: {path}")
        # Paper accents use a warm, low-saturation cream face with a much more
        # saturated orange outline. Measure that face for type size, while the
        # full alpha box still constrains width and carries the outline.
        if np is not None:
            pixels = np.asarray(rgba)
            red, green, blue, alpha = (pixels[:, :, index] for index in range(4))
            face_mask = (
                (alpha > 30)
                & (red > 160)
                & (green > 110)
                & (blue > 70)
                & (green > red * 0.58)
                & (blue > green * 0.50)
            )
            ys, xs = np.where(face_mask)
            face_left, face_top = int(xs.min()), int(ys.min())
            face_right, face_bottom = int(xs.max()), int(ys.max())
        else:
            pixels = rgba.load()
            left, top, right, bottom = alpha_bounds
            face_left, face_top = rgba.width, rgba.height
            face_right = face_bottom = -1
            for y in range(top, bottom):
                for x in range(left, right):
                    red, green, blue, alpha = pixels[x, y]
                    if (
                        alpha > 30
                        and red > 160
                        and green > 110
                        and blue > 70
                        and green > red * 0.58
                        and blue > green * 0.50
                    ):
                        face_left = min(face_left, x)
                        face_top = min(face_top, y)
                        face_right = max(face_right, x)
                        face_bottom = max(face_bottom, y)
        if face_right < face_left or face_bottom < face_top:
            raise ValueError(f"No cream letter-face pixels were detected: {path}")
        return (
            rgba.width,
            rgba.height,
            alpha_bounds,
            (face_left, face_top, face_right + 1, face_bottom + 1),
        )


def get_asset_path(asset_root: Path, name: str) -> Path:
    matches = list(asset_root.rglob(f"{name}.png"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one PNG for {name}, found {len(matches)}")
    return matches[0]


def round_value(value: float) -> float:
    return round(value, 7)


def main() -> int:
    args = parse_args()
    if not args.session_id:
        print("Set PALMIER_MCP_SESSION_ID or pass --session-id.", file=sys.stderr)
        return 2
    if not 0 < args.safe_width_ratio <= 1:
        print("--safe-width-ratio must be in (0, 1].", file=sys.stderr)
        return 2
    if not args.asset_root.is_dir():
        print(f"Asset directory does not exist: {args.asset_root}", file=sys.stderr)
        return 2

    media_result = call_mcp(args.mcp_url, args.session_id, "get_media", {"projectId": args.project_id}, 1)
    timeline_result = call_mcp(
        args.mcp_url,
        args.session_id,
        "get_timeline",
        {"projectId": args.project_id, "timelineId": args.timeline_id},
        2,
    )
    media = json.loads(result_text(media_result))
    timeline = json.loads(result_text(timeline_result))
    if timeline.get("timelineId") != args.timeline_id:
        raise RuntimeError("Palmier returned a different timeline than requested")

    canvas_w, canvas_h = timeline["width"], timeline["height"]
    assets = {asset["id"]: asset for asset in media.get("assets", [])}
    accent_track = next((track for track in timeline.get("tracks", []) if track.get("name") == "Accents"), None)
    if accent_track is None:
        raise RuntimeError("Target timeline has no Accents track")

    clips: list[dict[str, Any]] = []
    for clip in accent_track.get("clips", []):
        asset = assets.get(clip.get("mediaRef"), {})
        if asset.get("type") != "image" or not asset.get("name", "").lower().startswith(("a", "n")):
            continue
        path = get_asset_path(args.asset_root, asset["name"])
        source_w, source_h, alpha_bounds, face_bounds = image_bounds(str(path))
        if (source_w, source_h) != (asset["width"], asset["height"]):
            raise RuntimeError(f"Local and Palmier dimensions differ for {asset['name']}")
        alpha_left, alpha_top, alpha_right, alpha_bottom = alpha_bounds
        face_left, face_top, face_right, face_bottom = face_bounds
        transform = clip.get("transform", {})
        position_keys = clip.get("keyframes", {}).get("position")
        if not position_keys or len(position_keys) < 2:
            raise RuntimeError(f"Accent has no usable position keyframes: {clip['id']}")
        visible_h = (alpha_bottom - alpha_top) / source_h * transform["height"] * canvas_h
        face_h = (face_bottom - face_top) / source_h * transform["height"] * canvas_h
        # Palmier omits default transform fields from get_timeline; the default width is 1.0.
        transform_width = transform.get("width", 1.0)
        visible_w = (alpha_right - alpha_left) / source_w * transform_width * canvas_w
        clips.append(
            {
                "clip": clip,
                "asset": asset,
                "path": path,
                "source_w": source_w,
                "source_h": source_h,
                "alpha_left": alpha_left,
                "alpha_top": alpha_top,
                "alpha_right": alpha_right,
                "alpha_bottom": alpha_bottom,
                "face_left": face_left,
                "face_top": face_top,
                "face_right": face_right,
                "face_bottom": face_bottom,
                "visible_h": visible_h,
                "face_h": face_h,
                "visible_w": visible_w,
            }
        )
    if not clips:
        raise RuntimeError("No image accents were found on the Accents track")

    # Older releases can be inferred from a previously normalized size cluster.
    # Prefer the authored manifest when the current PNGs have not been normalized.
    median_visible_h = statistics.median(item["visible_h"] for item in clips)
    single_line_reference = statistics.median(
        item["visible_h"] for item in clips if item["visible_h"] < 1.5 * median_visible_h
    )
    line_counts = None
    if args.line_counts_json:
        loaded_counts = json.loads(args.line_counts_json.read_text(encoding="utf-8"))
        if not isinstance(loaded_counts, dict):
            raise ValueError("--line-counts-json must contain an object mapping asset names to integers")
        line_counts = {str(name): int(count) for name, count in loaded_counts.items()}
        if any(count < 1 for count in line_counts.values()):
            raise ValueError("Line counts must be positive integers")
    for item in clips:
        asset_name = item["asset"]["name"]
        if line_counts is not None:
            if asset_name not in line_counts:
                raise ValueError(f"Line-count manifest has no entry for active accent {asset_name}")
            item["line_count"] = line_counts[asset_name]
            item["line_count_source"] = "explicit_manifest"
        else:
            item["line_count"] = max(1, round(item["visible_h"] / single_line_reference))
            item["line_count_source"] = "inferred_from_previous_scale"
        item["current_cap_height"] = item["face_h"] / item["line_count"]
        item["width_ratio"] = item["visible_w"] / item["current_cap_height"]

    max_ratio_item = max(clips, key=lambda item: item["width_ratio"])
    max_line_ratio = max_ratio_item["width_ratio"]
    max_cap_height = args.safe_width_ratio * canvas_w / max_line_ratio
    cap_height = args.target_cap_height if args.target_cap_height is not None else math.floor(max_cap_height / 10) * 10
    if cap_height <= 0 or cap_height > max_cap_height + 1e-6:
        raise RuntimeError(
            f"Requested {cap_height:.1f}px cap height exceeds the safe-width limit "
            f"{max_cap_height:.1f}px (widest cue: {max_ratio_item['asset']['name']})"
        )

    for item in clips:
        clip = item["clip"]
        transform = clip["transform"]
        total_target_face_h = cap_height * item["line_count"]
        factor = total_target_face_h / item["face_h"]
        new_w = transform.get("width", 1.0) * factor
        new_h = transform["height"] * factor
        face_cx = (item["face_left"] + item["face_right"]) / (2 * item["source_w"])
        face_cy = (item["face_top"] + item["face_bottom"]) / (2 * item["source_h"])
        new_keys = []
        old_keys = clip["keyframes"]["position"]
        for i, row in enumerate(old_keys):
            level = args.entry_y if i == 0 else args.exit_y if i == len(old_keys) - 1 else args.hold_y
            x = 0.5 - face_cx * new_w
            y = level - face_cy * new_h
            key = [row[0], round_value(x), round_value(y)]
            if len(row) > 3:
                key.append(row[3])
            new_keys.append(key)
        item["new_transform"] = {"width": round_value(new_w), "height": round_value(new_h)}
        item["new_keys"] = new_keys
        item["target_cap_height"] = cap_height
        item["target_width"] = item["width_ratio"] * cap_height

    unique_media: dict[tuple[str, float, float], list[dict[str, Any]]] = defaultdict(list)
    for item in clips:
        tr = item["new_transform"]
        key = (item["asset"]["id"], tr["width"], tr["height"])
        unique_media[key].append(item)

    plan = {
        "projectId": args.project_id,
        "timelineId": args.timeline_id,
        "canvas": [canvas_w, canvas_h],
        "safeWidthPx": round(args.safe_width_ratio * canvas_w, 1),
        "maxLineWidthRatio": round(max_line_ratio, 4),
        "widestCue": max_ratio_item["asset"]["name"],
        "maxSafeCapHeightPx": round(max_cap_height, 2),
        "targetCapHeightPx": cap_height,
        "lineCountSource": "explicit_manifest" if line_counts is not None else "inferred_from_previous_scale",
        "clipCount": len(clips),
        "uniqueAssetCount": len({item["asset"]["id"] for item in clips}),
        "maxRenderedLineWidthPx": round(max(item["target_width"] for item in clips), 1),
        "cues": [
            {
                "clipId": item["clip"]["id"],
                "assetName": item["asset"]["name"],
                "lineCount": item["line_count"],
                "lineCountSource": item["line_count_source"],
                "oldCapHeightPx": round(item["current_cap_height"], 2),
                "newCapHeightPx": cap_height,
                "newLineWidthPx": round(item["target_width"], 1),
                "newTransform": item["new_transform"],
                "positionKeyframes": item["new_keys"],
            }
            for item in clips
        ],
    }

    if not args.apply:
        print(json.dumps(plan, indent=2))
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        print("Dry run only; pass --apply to snapshot and edit this timeline.")
        return 0

    snapshot = call_mcp(
        args.mcp_url,
        args.session_id,
        "manage_snapshots",
        {
            "action": "save",
            "projectId": args.project_id,
            "timelineId": args.timeline_id,
            "name": f"Before accent normalization {args.timeline_id}",
        },
        3,
    )
    snapshot_data = json.loads(result_text(snapshot))["snapshot"]
    plan["snapshot"] = snapshot_data

    request_id = 10
    for (_, _, _), items in unique_media.items():
        clip_ids = [item["clip"]["id"] for item in items]
        transform = items[0]["new_transform"]
        call_mcp(
            args.mcp_url,
            args.session_id,
            "set_clip_properties",
            {
                "projectId": args.project_id,
                "timelineId": args.timeline_id,
                "clipIds": clip_ids,
                "transform": transform,
            },
            request_id,
        )
        request_id += 1
    for item in clips:
        call_mcp(
            args.mcp_url,
            args.session_id,
            "set_keyframes",
            {
                "projectId": args.project_id,
                "timelineId": args.timeline_id,
                "clipId": item["clip"]["id"],
                "property": "position",
                "keyframes": item["new_keys"],
            },
            request_id,
        )
        request_id += 1

    updated = json.loads(
        result_text(
            call_mcp(
                args.mcp_url,
                args.session_id,
                "get_timeline",
                {"projectId": args.project_id, "timelineId": args.timeline_id},
                request_id,
            )
        )
    )
    updated_clips = {clip["id"]: clip for track in updated.get("tracks", []) if track.get("name") == "Accents" for clip in track.get("clips", [])}
    expected_ids = {item["clip"]["id"] for item in clips}
    if not expected_ids.issubset(updated_clips):
        raise RuntimeError("Post-edit timeline read is missing one or more accent clips")
    max_cap_error = 0.0
    max_anchor_error = 0.0
    for item in clips:
        clip = updated_clips[item["clip"]["id"]]
        transform = clip["transform"]
        new_h = (item["face_bottom"] - item["face_top"]) / item["source_h"] * transform["height"] * canvas_h
        cap_error = abs(new_h / item["line_count"] - cap_height)
        max_cap_error = max(max_cap_error, cap_error)
        item["opacity_preserved"] = (
            clip.get("keyframes", {}).get("opacity")
            == item["clip"].get("keyframes", {}).get("opacity")
        )
        face_cx = (item["face_left"] + item["face_right"]) / (2 * item["source_w"])
        face_cy = (item["face_top"] + item["face_bottom"]) / (2 * item["source_h"])
        for i, row in enumerate(clip["keyframes"]["position"]):
            expected_y = args.entry_y if i == 0 else args.exit_y if i == len(clip["keyframes"]["position"]) - 1 else args.hold_y
            center_x = row[1] + face_cx * transform["width"]
            center_y = row[2] + face_cy * transform["height"]
            max_anchor_error = max(max_anchor_error, abs(center_x - 0.5), abs(center_y - expected_y))
    opacity_preserved = all(item["opacity_preserved"] for item in clips)
    if max_cap_error > 1.0 or max_anchor_error > 0.001 or not opacity_preserved:
        raise RuntimeError(
            f"Post-edit check failed: max cap-height error {max_cap_error:.3f}px, "
            f"max optical-anchor error {max_anchor_error:.6f}, "
            f"opacity curves preserved: {opacity_preserved}"
        )
    plan["verification"] = {
        "status": "passed",
        "maxCapHeightErrorPx": round(max_cap_error, 4),
        "maxOpticalAnchorError": round(max_anchor_error, 7),
        "opacityCurvesPreserved": opacity_preserved,
        "clipIdsVerified": len(expected_ids),
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in plan.items() if key != "cues"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
