#!/usr/bin/env python3
"""Resume the already-applied 55% correction; do not re-import or duplicate it."""

from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path

EPISODE = Path(__file__).resolve().parents[2]
ROOT = EPISODE.parents[2]
AUTOMATION = EPISODE / "Edit" / "Automation"
RECEIPT = AUTOMATION / "add_55_percent_accent_v01_receipt.json"
FRAMES = AUTOMATION / "review_frames_55_percent_v01"
PROJECT_ID = "652FD175"
TIMELINE_ID = "221D8873"
ACCENT_CLIP_ID = "DE6DAB40"
ACCENT_TRACK_ID = "017F50BD"
SFX_CLIP_ID = "41761724"
SFX_TRACK_ID = "7AF6393B"


def save(state: dict) -> None:
    temp = RECEIPT.with_suffix(".json.tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    temp.replace(RECEIPT)


def call(client, state: dict, name: str, args: dict, label: str) -> dict:
    state["pending"] = {"label": label, "tool": name, "args": args}
    save(state)
    result = client.request("tools/call", {"name": name, "arguments": args})
    if result.get("isError"):
        raise RuntimeError(f"Palmier {name}: {result.get('content')}")
    texts = [item["text"] for item in result.get("content", []) if item.get("type") == "text"]
    parsed = json.loads(texts[0]) if texts else {}
    state["steps"].append({"label": label, "tool": name, "result": parsed})
    state.pop("pending", None)
    save(state)
    return parsed


def main() -> None:
    state = json.loads(RECEIPT.read_text(encoding="utf-8"))
    if state.get("project_id") != PROJECT_ID or state.get("timeline_id") != TIMELINE_ID:
        raise RuntimeError("Receipt targets a different project or timeline")
    if state.get("status") != "interrupted_pending_inspection":
        raise RuntimeError(f"Unexpected receipt status: {state.get('status')}")

    sys.path.insert(0, str(ROOT / "stories" / "automation" / "palmier"))
    from inspect_connection import PalmierConnection

    client = PalmierConnection()
    client.connect()
    timeline = json.loads(next(x["text"] for x in client.request("tools/call", {
        "name": "get_timeline", "arguments": {"projectId": PROJECT_ID, "timelineId": TIMELINE_ID}
    }).get("content", []) if x.get("type") == "text"))
    if timeline.get("totalFrames") != 1344:
        raise RuntimeError("Timeline frame count changed; stop and inspect")
    if not any(c.get("id") == ACCENT_CLIP_ID for t in timeline.get("tracks", []) for c in t.get("clips", [])):
        raise RuntimeError("The existing 55% clip is missing; do not duplicate it")
    if not any(c.get("id") == SFX_CLIP_ID for t in timeline.get("tracks", []) for c in t.get("clips", [])):
        raise RuntimeError("The existing paper SFX is missing; do not duplicate it")

    call(client, state, "manage_tracks", {"projectId": PROJECT_ID, "timelineId": TIMELINE_ID,
         "set": [{"trackId": ACCENT_TRACK_ID, "name": "Accents P12"}]}, "name P12 accent track")
    call(client, state, "manage_tracks", {"projectId": PROJECT_ID, "timelineId": TIMELINE_ID,
         "reorder": [{"trackId": ACCENT_TRACK_ID, "to": 3}]}, "place P12 accent below foreground and middle")

    FRAMES.mkdir(parents=True, exist_ok=True)
    review_frames = [1028, 1032, 1036, 1050, 1090, 1144, 1154, 1163]
    for frame in review_frames:
        result = client.request("tools/call", {"name": "inspect_timeline", "arguments": {
            "projectId": PROJECT_ID, "timelineId": TIMELINE_ID, "startFrame": frame
        }})
        if result.get("isError"):
            raise RuntimeError(f"Palmier inspect_timeline at {frame}: {result.get('content')}")
        images = [item for item in result.get("content", []) if item.get("type") == "image"]
        if len(images) != 1:
            raise RuntimeError(f"Expected one rendered frame at {frame}, got {len(images)}")
        (FRAMES / f"frame_{frame:04d}.png").write_bytes(base64.b64decode(images[0]["data"]))

    timeline = json.loads(next(x["text"] for x in client.request("tools/call", {
        "name": "get_timeline", "arguments": {"projectId": PROJECT_ID, "timelineId": TIMELINE_ID}
    }).get("content", []) if x.get("type") == "text"))
    state["review_frames"] = review_frames
    state["after"] = {
        "video_track_order": [t.get("name") or t.get("label") for t in timeline.get("tracks", []) if t.get("type") == "video"],
        "audio_track_order": [t.get("name") or t.get("label") for t in timeline.get("tracks", []) if t.get("type") == "audio"],
        "total_frames": timeline.get("totalFrames"),
    }
    state["status"] = "trial_added_pending_visual_and_audio_review"
    save(state)
    print(json.dumps({"status": state["status"], "frames": str(FRAMES), "tracks": state["after"],
                      "receipt": str(RECEIPT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        state = json.loads(RECEIPT.read_text(encoding="utf-8")) if RECEIPT.exists() else {}
        state["status"] = "interrupted_pending_inspection"
        state["resume_error"] = repr(exc)
        save(state)
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
