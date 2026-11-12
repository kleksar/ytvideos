#!/usr/bin/env python3
"""Render the reviewed 007 timeline to a temporary file through Palmier."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

EPISODE = Path(__file__).resolve().parents[2]
ROOT = EPISODE.parents[2]
AUTOMATION = EPISODE / "Edit" / "Automation"
RECEIPT = AUTOMATION / "render_v04_receipt.json"
OUTPUT = AUTOMATION / "Renders" / "007_joshua_jessica_short_20261101_palmier_v04_raw.mp4"
PROJECT_ID = "652FD175"
TIMELINE_ID = "221D8873"
PROJECT_PATH = "/Users/diplomat/Documents/Palmier Pro/Paper Detour 007 Joshua Jessica Short Render 20261101.palmier"


def save(data: dict) -> None:
    temp = RECEIPT.with_suffix(".json.tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    temp.replace(RECEIPT)


def main() -> None:
    if RECEIPT.exists():
        raise RuntimeError(f"Render receipt already exists; inspect it before retrying: {RECEIPT}")
    if OUTPUT.exists():
        raise RuntimeError(f"Render output already exists; refusing overwrite: {OUTPUT}")

    sys.path.insert(0, str(ROOT / "stories" / "automation" / "palmier"))
    from inspect_connection import PalmierConnection

    client = PalmierConnection()
    client.connect()

    def call(name: str, args: dict) -> dict:
        response = client.request("tools/call", {"name": name, "arguments": args})
        if response.get("isError"):
            raise RuntimeError(f"Palmier {name}: {response.get('content')}")
        texts = [x["text"] for x in response.get("content", []) if x.get("type") == "text"]
        if len(texts) != 1:
            raise RuntimeError(f"Unexpected Palmier response for {name}")
        return json.loads(texts[0])

    projects = call("manage_project", {"action": "list"}).get("projects", [])
    project = next((p for p in projects if p.get("id") == PROJECT_ID), None)
    if not project or not project.get("isAccessible") or not project.get("isOpen") or project.get("path") != PROJECT_PATH:
        raise RuntimeError("Exact 007 project is not open at its expected path")
    timeline = call("get_timeline", {"projectId": PROJECT_ID, "timelineId": TIMELINE_ID})
    if (timeline.get("width"), timeline.get("height"), timeline.get("fps"), timeline.get("totalFrames")) != (1080, 1920, 30, 1344):
        raise RuntimeError("Exact 007 timeline no longer matches 1080x1920/30/1344")
    tracks = timeline.get("tracks", [])
    video = [t for t in tracks if t.get("type") == "video"]
    audio = [t for t in tracks if t.get("type") == "audio"]
    expected_video = ["Grain", "Foreground", "Middle", "Accents P12", "Accents", "Background", "Support"]
    expected_audio = ["Narration", "SFX"]
    if [t.get("name") or t.get("label") for t in video] != expected_video:
        raise RuntimeError("007 video track order changed")
    if [t.get("name") or t.get("label") for t in audio] != expected_audio:
        raise RuntimeError("007 audio track order changed")
    if not any(c.get("id") == "DE6DAB40" for t in video for c in t.get("clips", [])):
        raise RuntimeError("Reviewed 55% accent is absent")
    if not any(c.get("id") == "41761724" for t in audio for c in t.get("clips", [])):
        raise RuntimeError("Reviewed paper gesture is absent")

    receipt = {
        "version": 1,
        "status": "starting",
        "project_id": PROJECT_ID,
        "timeline_id": TIMELINE_ID,
        "project_path": PROJECT_PATH,
        "snapshot_id": "E7B112CE",
        "independent_visual_review": {
            "reviewer": "/root/av_review_007_final",
            "status": "PASS for P12 timeline composition and alignment; export still pending",
            "scope": "inspect_timeline samples f1028–1164; phone-size Palmier preview 288x512",
            "limitations": ["No handset test", "No listening", "No continuous full-short playback"],
        },
        "video_track_order": expected_video,
        "audio_track_order": expected_audio,
        "output_path": str(OUTPUT),
        "settings": {"mode": "video", "codec": "H.264", "resolution": "Match Timeline", "fps": 30},
    }
    save(receipt)
    result = call("export_project", {
        "projectId": PROJECT_ID,
        "timelineId": TIMELINE_ID,
        "mode": "video",
        "codec": "H.264",
        "resolution": "Match Timeline",
        "outputPath": str(OUTPUT),
        "overwrite": False,
    })
    receipt["export"] = result
    receipt["status"] = result.get("status", "started")
    save(receipt)
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
