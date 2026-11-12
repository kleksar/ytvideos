#!/usr/bin/env python3
"""Add the approved 55% paper accent and its single page gesture to 007 via Palmier."""

from __future__ import annotations

import base64
import hashlib
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
EXPECTED_PATH = "/Users/diplomat/Documents/Palmier Pro/Paper Detour 007 Joshua Jessica Short Render 20261101.palmier"
FPS = 30
START = 1028
END = 1164

GRAPHIC = EPISODE / "Source" / "Graphics" / "Final_v01" / "55_PERCENT_v01.png"
FOLEY = EPISODE / "Source" / "Audio" / "book-page-02.wav"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def save() -> None:
    temp = RECEIPT.with_suffix(".json.tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    temp.replace(RECEIPT)


def call(name: str, args: dict) -> dict:
    result = palmier.request("tools/call", {"name": name, "arguments": args})
    if result.get("isError"):
        raise RuntimeError(f"Palmier {name}: {result.get('content')}")
    texts = [item["text"] for item in result.get("content", []) if item.get("type") == "text"]
    if len(texts) != 1:
        raise RuntimeError(f"Unexpected Palmier response for {name}")
    return json.loads(texts[0])


def guard() -> dict:
    projects = call("manage_project", {"action": "list"}).get("projects", [])
    project = next((p for p in projects if p.get("id") == PROJECT_ID), None)
    if not project or not project.get("isAccessible") or not project.get("isOpen"):
        raise RuntimeError("The exact 007 project is not open and accessible")
    if Path(project.get("path", "")).as_posix() != Path(EXPECTED_PATH).as_posix():
        raise RuntimeError("The opened 007 project path differs from the expected path")
    inventory = call("get_media", {"projectId": PROJECT_ID})
    if not any(t.get("timelineId") == TIMELINE_ID for t in inventory.get("timelines", [])):
        raise RuntimeError("The exact timeline is absent from the 007 project")
    timeline = call("get_timeline", {"projectId": PROJECT_ID, "timelineId": TIMELINE_ID})
    if (timeline.get("width"), timeline.get("height"), timeline.get("fps"), timeline.get("totalFrames")) != (1080, 1920, FPS, 1344):
        raise RuntimeError("The target timeline metadata changed")
    return timeline


def step(label: str, tool: str, args: dict) -> dict:
    guard()
    state["pending"] = {"label": label, "tool": tool, "args": args}
    save()
    result = call(tool, args)
    state["steps"].append({"label": label, "tool": tool, "result": result})
    state.pop("pending", None)
    save()
    return result


def add_media(path: Path, label: str) -> str:
    if not path.is_file():
        raise RuntimeError(f"Missing approved source asset: {path}")
    state["asset_sha256"][str(path)] = digest(path)
    result = step(f"import {label}", "import_media", {
        "projectId": PROJECT_ID,
        "source": {"path": str(path)},
        "folder": "PaperLayers/007_joshua_jessica_short_20261101/PostBuild",
    })
    ref = result.get("mediaRef") or result.get("assetId") or result.get("id")
    if not isinstance(ref, str) or not ref:
        raise RuntimeError(f"Palmier returned no mediaRef for {label}")
    return ref


def main() -> None:
    if RECEIPT.exists():
        raise RuntimeError(f"Receipt already exists; inspect it and Palmier before retrying: {RECEIPT}")
    if not GRAPHIC.is_file() or not FOLEY.is_file():
        raise RuntimeError("The approved 55% graphic or documented page sound is missing")

    sys.path.insert(0, str(ROOT / "stories" / "automation" / "palmier"))
    from inspect_connection import PalmierConnection

    global palmier, state
    palmier = PalmierConnection()
    palmier.connect()
    timeline = guard()
    tracks = timeline.get("tracks", [])
    video_names = [t.get("name") or t.get("label") for t in tracks if t.get("type") == "video"]
    audio_names = [t.get("name") or t.get("label") for t in tracks if t.get("type") == "audio"]
    if video_names != ["Grain", "Foreground", "Middle", "Accents", "Background", "Support"]:
        raise RuntimeError(f"Unexpected video track stack: {video_names}")
    if audio_names != ["Narration"]:
        raise RuntimeError(f"Unexpected audio tracks before correction: {audio_names}")
    accent_track = next(t for t in tracks if (t.get("name") or t.get("label")) == "Accents")
    if any(c.get("frames", [None, None])[0] < END and c.get("frames", [None, None])[1] > START for c in accent_track.get("clips", [])):
        raise RuntimeError("An accent already overlaps the requested P12 range")

    state = {
        "version": 1,
        "status": "preparing",
        "project_id": PROJECT_ID,
        "timeline_id": TIMELINE_ID,
        "project_path": EXPECTED_PATH,
        "before": {"video_track_order": video_names, "audio_track_order": audio_names},
        "asset_sha256": {},
        "steps": [],
        "planned_accent": {"frames": [START, END], "readable_target_frame": 1036,
                            "scale": [0.32, 0.0868], "position_start": [0.42, 0.30],
                            "position_hold": [0.42, 0.21], "motion": "rise from behind the laptop top edge"},
        "planned_foley": {"source": [0.0, 0.733], "start_frame": START,
                           "volume_db": [[0, -24, "hold"], [18, -24, "linear"], [21, -60, "linear"]]},
    }
    save()

    graphic_ref = add_media(GRAPHIC, "55_PERCENT_v01")
    state["media_refs"] = {"55_PERCENT": graphic_ref}
    save()
    added = step("place 55% paper accent", "add_clips", {
        "projectId": PROJECT_ID, "timelineId": TIMELINE_ID,
        "entries": [{"mediaRef": graphic_ref, "startFrame": START, "endFrame": END, "includeAudio": False}],
    })
    clips = added.get("clips", [])
    if len(clips) != 1:
        raise RuntimeError(f"Expected one 55% clip; found {len(clips)}")
    accent_clip_id = clips[0].get("id")
    if not accent_clip_id:
        raise RuntimeError("Palmier omitted 55% clip ID")
    state["accent"] = {"clip_id": accent_clip_id, "frames": [START, END]}
    save()

    duration = END - START
    step("size 55% accent for phone readability", "set_keyframes", {
        "projectId": PROJECT_ID, "timelineId": TIMELINE_ID, "clipId": accent_clip_id,
        "property": "scale", "keyframes": [[0, 0.32, 0.0868, "linear"], [duration - 1, 0.32, 0.0868, "linear"]],
    })
    pos = [[0, 0.42, 0.30, "linear"], [8, 0.42, 0.21, "linear"],
           [duration - 19, 0.42, 0.21, "linear"], [duration - 1, 0.42, 0.30, "linear"]]
    step("animate 55% accent behind and above laptop edge", "set_keyframes", {
        "projectId": PROJECT_ID, "timelineId": TIMELINE_ID, "clipId": accent_clip_id,
        "property": "position", "keyframes": pos,
    })
    state["accent"].update({"position_keyframes": pos, "scale": [0.32, 0.0868],
                             "layer_order": "Accents track below Middle and above Background"})
    save()

    foley_ref = add_media(FOLEY, "book-page-02.wav")
    state["media_refs"]["book-page-02.wav"] = foley_ref
    save()
    sound = step("place one page gesture with 55% entrance", "add_clips", {
        "projectId": PROJECT_ID, "timelineId": TIMELINE_ID,
        "entries": [{"mediaRef": foley_ref, "startFrame": START, "source": [0.0, 0.733]}],
    })
    sound_clips = sound.get("clips", [])
    if len(sound_clips) != 1 or not sound_clips[0].get("id"):
        raise RuntimeError("Palmier did not return exactly one paper SFX clip")
    sfx_clip_id = sound_clips[0]["id"]
    step("gain and fade paper gesture", "set_keyframes", {
        "projectId": PROJECT_ID, "timelineId": TIMELINE_ID, "clipId": sfx_clip_id,
        "property": "volumeDb", "keyframes": [[0, -24, "hold"], [18, -24, "linear"], [21, -60, "linear"]],
    })
    state["foley"] = {"clip_id": sfx_clip_id, "start_frame": START, "source_seconds": [0.0, 0.733],
                      "volume_db": [[0, -24, "hold"], [18, -24, "linear"], [21, -60, "linear"]],
                      "tail_fade_frame": 21}
    save()

    timeline = guard()
    video_tracks = [t for t in timeline.get("tracks", []) if t.get("type") == "video"]
    audio_tracks = [t for t in timeline.get("tracks", []) if t.get("type") == "audio"]
    accent_track = next(t for t in video_tracks if any(c.get("id") == accent_clip_id for c in t.get("clips", [])))
    sfx_track = next(t for t in audio_tracks if any(c.get("id") == sfx_clip_id for c in t.get("clips", [])))
    if (sfx_track.get("name") or sfx_track.get("label")) != "SFX":
        step("name paper gesture track SFX", "manage_tracks", {
            "projectId": PROJECT_ID, "timelineId": TIMELINE_ID,
            "set": [{"trackId": sfx_track["trackId"], "name": "SFX"}],
        })
    state["accent"]["track_id"] = accent_track.get("trackId")
    state["foley"]["track_id"] = sfx_track.get("trackId")
    state["status"] = "accent_and_foley_added_pending_visual_and_audio_review"

    FRAMES.mkdir(parents=True, exist_ok=True)
    review_frames = [1028, 1032, 1036, 1050, 1090, 1144, 1154, 1163]
    for frame in review_frames:
        guard()
        result = palmier.request("tools/call", {"name": "inspect_timeline",
                                    "arguments": {"projectId": PROJECT_ID, "timelineId": TIMELINE_ID,
                                                  "startFrame": frame}})
        if result.get("isError"):
            raise RuntimeError(f"Palmier inspect_timeline failed at frame {frame}")
        images = [item for item in result.get("content", []) if item.get("type") == "image"]
        if len(images) != 1:
            raise RuntimeError(f"Expected one inspection image at frame {frame}; got {len(images)}")
        (FRAMES / f"frame_{frame:04d}.png").write_bytes(base64.b64decode(images[0]["data"]))
    state["review_frames"] = review_frames
    final_timeline = guard()
    state["after"] = {
        "video_track_order": [t.get("name") or t.get("label") for t in final_timeline.get("tracks", []) if t.get("type") == "video"],
        "audio_track_order": [t.get("name") or t.get("label") for t in final_timeline.get("tracks", []) if t.get("type") == "audio"],
        "total_frames": final_timeline.get("totalFrames"),
    }
    state["status"] = "trial_added_pending_review"
    save()
    print(json.dumps({"status": state["status"], "project_id": PROJECT_ID, "timeline_id": TIMELINE_ID,
                      "accent": state["accent"], "foley": state["foley"],
                      "frames": str(FRAMES), "receipt": str(RECEIPT)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    state: dict = {}
    palmier = None
    try:
        main()
    except Exception as exc:
        if state:
            state["status"] = "interrupted_pending_inspection"
            state["error"] = repr(exc)
            save()
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
