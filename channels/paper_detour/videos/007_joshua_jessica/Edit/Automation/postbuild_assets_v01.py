#!/usr/bin/env python3
"""Add the episode-specific support, paper accent, foley, and grain transform to the fresh 007 timeline."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
from pathlib import Path

EPISODE = Path(__file__).resolve().parents[2]
AUTOMATION = EPISODE / "Edit" / "Automation"
QUICK = EPISODE / "Source" / "Images" / "QUICK_IMPORT_CURRENT"
BUILD_RECEIPT = AUTOMATION / "build_paper_project_receipt.json"
RECEIPT_PATH = AUTOMATION / "postbuild_assets_v01_receipt.json"
FPS = 30

SHOTS = [
    ("01_14_hook_loop", 0, 90),
    ("02_absence", 90, 183),
    ("03_jessica_name", 183, 273),
    ("04_old_messages", 273, 366),
    ("05_reply_card", 366, 456),
    ("06_all_night", 456, 546),
    ("01_14_hook_loop", 546, 636),
    ("08_tears", 636, 726),
    ("09_promise_daylight", 726, 816),
    ("10_waiting_quote", 816, 906),
    ("11_resource_used", 906, 996),
    ("12_resource_meter", 996, 1164),
    ("13_saved_conversations", 1164, 1254),
    ("01_14_hook_loop", 1254, 1344),
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def save_receipt(receipt: dict) -> None:
    temp = RECEIPT_PATH.with_suffix(".json.tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    temp.replace(RECEIPT_PATH)


class Palmier:
    def __init__(self) -> None:
        sys.path.insert(0, str(EPISODE.parents[2] / "stories" / "automation" / "palmier"))
        from inspect_connection import PalmierConnection

        self.client = PalmierConnection()
        self.client.connect()

    def call(self, name: str, args: dict) -> dict:
        response = self.client.request("tools/call", {"name": name, "arguments": args})
        if response.get("isError"):
            raise RuntimeError(f"Palmier {name} failed: {response.get('content')}")
        texts = [x["text"] for x in response.get("content", []) if x.get("type") == "text"]
        if len(texts) != 1:
            raise RuntimeError(f"Palmier {name} returned an unexpected response")
        return json.loads(texts[0])


def journal_call(p: Palmier, receipt: dict, label: str, tool: str, args: dict) -> dict:
    receipt["pending"] = {"label": label, "tool": tool, "args": args}
    save_receipt(receipt)
    result = p.call(tool, args)
    receipt["steps"].append({"label": label, "tool": tool, "actionId": result.get("actionId"), "result": result})
    receipt.pop("pending", None)
    save_receipt(receipt)
    return result


def main() -> int:
    if RECEIPT_PATH.exists():
        raise RuntimeError(f"Receipt already exists; inspect Palmier before any retry: {RECEIPT_PATH}")
    build = json.loads(BUILD_RECEIPT.read_text(encoding="utf-8"))
    if build.get("status") != "ready_for_review" or build.get("exported") or build.get("published"):
        raise RuntimeError("Expected a ready, unexported, unpublished 007 timeline")
    project_id, timeline_id = build.get("project_id"), build.get("timeline_id")
    if not project_id or not timeline_id:
        raise RuntimeError("Build receipt omitted exact Palmier IDs")

    p = Palmier()
    projects = p.call("manage_project", {"action": "list"}).get("projects", [])
    project = next((x for x in projects if x.get("id") == project_id), None)
    if not project or not project.get("isAccessible"):
        raise RuntimeError("The exact 007 project is not accessible")
    visible_before = [x.get("id") for x in projects if x.get("isVisible")]
    timeline = p.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
    if (timeline.get("width"), timeline.get("height"), timeline.get("fps"), timeline.get("totalFrames")) != (1080, 1920, FPS, 1344):
        raise RuntimeError("The 007 timeline metadata changed; stop before editing")

    receipt = {
        "version": 1,
        "status": "preparing",
        "project_id": project_id,
        "timeline_id": timeline_id,
        "project_name": build.get("project_name"),
        "visible_project_ids_before": visible_before,
        "asset_sha256": {},
        "steps": [],
    }
    save_receipt(receipt)

    # Add the matching static edge-support plate under every moving background.
    media_refs = {}
    for folder, _, _ in SHOTS:
        if folder in media_refs:
            continue
        path = QUICK / folder / "BG_EDGE_SUPPORT.png"
        if not path.is_file():
            raise RuntimeError(f"Missing required edge-support plate: {path}")
        receipt["asset_sha256"][str(path)] = digest(path)
        imported = journal_call(p, receipt, f"import support {folder}", "import_media", {
            "projectId": project_id, "source": {"path": str(path)},
            "folder": "PaperLayers/007_joshua_jessica_short_20261101/PostBuild",
        })
        ref = imported.get("mediaRef") or imported.get("assetId") or imported.get("id")
        if not isinstance(ref, str) or not ref:
            raise RuntimeError(f"Import omitted media ID for {path}")
        media_refs[folder] = ref
        receipt.setdefault("media_refs", {})[str(path)] = ref
        save_receipt(receipt)

    support_entries = [
        {"mediaRef": media_refs[folder], "startFrame": start, "endFrame": end, "includeAudio": False}
        for folder, start, end in SHOTS
    ]
    added = journal_call(p, receipt, "place all 14 edge-support plates", "add_clips", {
        "projectId": project_id, "timelineId": timeline_id, "entries": support_entries,
    })
    if len(added.get("clips", [])) != len(SHOTS) or len(added.get("createdTracks", [])) != 1:
        raise RuntimeError("Unexpected support clip/track count")
    support_track_id = added["createdTracks"][0].get("trackId")
    if not support_track_id:
        raise RuntimeError("Palmier omitted support track ID")
    journal_call(p, receipt, "name support track", "manage_tracks", {
        "projectId": project_id, "timelineId": timeline_id,
        "set": [{"trackId": support_track_id, "name": "Support"}],
    })
    receipt["support"] = {"track_id": support_track_id, "clip_ids": [c.get("id") for c in added["clips"]]}
    save_receipt(receipt)

    # Place the one approved word between the background and the frame plane.
    jessica = EPISODE / "Source" / "Graphics" / "Final_v01" / "JESSICA_v01.png"
    if not jessica.is_file():
        raise RuntimeError("The approved JESSICA_v01 graphic is missing")
    receipt["asset_sha256"][str(jessica)] = digest(jessica)
    imported = journal_call(p, receipt, "import JESSICA_v01", "import_media", {
        "projectId": project_id, "source": {"path": str(jessica)},
        "folder": "PaperLayers/007_joshua_jessica_short_20261101/PostBuild",
    })
    jessica_ref = imported.get("mediaRef") or imported.get("assetId") or imported.get("id")
    if not isinstance(jessica_ref, str) or not jessica_ref:
        raise RuntimeError("Import omitted JESSICA_v01 media ID")
    receipt.setdefault("media_refs", {})[str(jessica)] = jessica_ref
    save_receipt(receipt)
    accent = journal_call(p, receipt, "place JESSICA paper accent", "add_clips", {
        "projectId": project_id, "timelineId": timeline_id,
        "entries": [{"mediaRef": jessica_ref, "startFrame": 204, "endFrame": 246, "includeAudio": False}],
    })
    if len(accent.get("clips", [])) != 1 or len(accent.get("createdTracks", [])) != 1:
        raise RuntimeError("Unexpected JESSICA accent clip/track count")
    accent_track_id = accent["createdTracks"][0].get("trackId")
    accent_clip_id = accent["clips"][0].get("id")
    if not accent_track_id or not accent_clip_id:
        raise RuntimeError("Palmier omitted JESSICA clip/track ID")
    journal_call(p, receipt, "name accent track", "manage_tracks", {
        "projectId": project_id, "timelineId": timeline_id,
        "set": [{"trackId": accent_track_id, "name": "Accents"}],
    })
    word_width = 320 / 941
    word_height = 109 / 1672
    x0 = 395 / 941
    y_hidden = 374 / 1672
    y_visible = 265 / 1672
    position_keys = [
        [0, x0, y_hidden, "linear"],
        [7, x0 + (4 / 4) * (7 / FPS) / 941, y_visible, "linear"],
        [32, x0 + (4 / 4) * (32 / FPS) / 941, y_visible, "linear"],
        [41, x0 + (4 / 4) * (41 / FPS) / 941, y_hidden, "linear"],
    ]
    for prop, keyframes in (
        ("scale", [[0, word_width, word_height, "linear"], [41, word_width, word_height, "linear"]]),
        ("position", position_keys),
    ):
        journal_call(p, receipt, f"animate JESSICA {prop}", "set_keyframes", {
            "projectId": project_id, "timelineId": timeline_id,
            "clipId": accent_clip_id, "property": prop, "keyframes": keyframes,
        })
    receipt["accent"] = {"track_id": accent_track_id, "clip_id": accent_clip_id,
                         "start_frame": 204, "end_frame": 246,
                         "layer_order": "below MG frame, above BG",
                         "position_keyframes": position_keys,
                         "scale": [word_width, word_height]}
    save_receipt(receipt)

    # One small CC0 paper movement on the paper resource-scale reveal.
    sfx = EPISODE / "Source" / "Audio" / "book-page-02.wav"
    if not sfx.is_file():
        raise RuntimeError("The documented CC0 paper movement is missing")
    receipt["asset_sha256"][str(sfx)] = digest(sfx)
    imported = journal_call(p, receipt, "import CC0 book-page-02", "import_media", {
        "projectId": project_id, "source": {"path": str(sfx)},
        "folder": "PaperLayers/007_joshua_jessica_short_20261101/PostBuild",
    })
    sfx_ref = imported.get("mediaRef") or imported.get("assetId") or imported.get("id")
    if not isinstance(sfx_ref, str) or not sfx_ref:
        raise RuntimeError("Import omitted the SFX media ID")
    receipt.setdefault("media_refs", {})[str(sfx)] = sfx_ref
    save_receipt(receipt)
    sfx_result = journal_call(p, receipt, "place single paper foley gesture", "add_clips", {
        "projectId": project_id, "timelineId": timeline_id,
        "entries": [{"mediaRef": sfx_ref, "startFrame": 1025, "source": [0.0, 0.733]}],
    })
    if len(sfx_result.get("clips", [])) != 1 or len(sfx_result.get("createdTracks", [])) != 1:
        raise RuntimeError("Unexpected SFX clip/track count")
    sfx_track_id = sfx_result["createdTracks"][0].get("trackId")
    sfx_clip_id = sfx_result["clips"][0].get("id")
    if not sfx_track_id or not sfx_clip_id:
        raise RuntimeError("Palmier omitted SFX clip/track ID")
    journal_call(p, receipt, "name SFX track", "manage_tracks", {
        "projectId": project_id, "timelineId": timeline_id,
        "set": [{"trackId": sfx_track_id, "name": "SFX"}],
    })
    journal_call(p, receipt, "set paper foley gain and natural tail", "set_keyframes", {
        "projectId": project_id, "timelineId": timeline_id, "clipId": sfx_clip_id,
        "property": "volumeDb", "keyframes": [[0, -24, "hold"], [18, -24, "linear"], [21, -60, "linear"]],
    })
    receipt["sfx"] = {"track_id": sfx_track_id, "clip_id": sfx_clip_id,
                      "start_frame": 1025, "source_seconds": [0, 0.733],
                      "gain_db": -24, "tail_fade_frames": 3}
    save_receipt(receipt)

    # Rotate the 16:9 alpha-grain plate so it retains its fine texture on the 9:16 canvas.
    timeline = p.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
    grain_track = next((t for t in timeline.get("tracks", []) if (t.get("name") or t.get("label")) == "Grain"), None)
    if not grain_track:
        raise RuntimeError("Grain track is missing")
    grain_clips = grain_track.get("clips", [])
    if len(grain_clips) != 6:
        raise RuntimeError(f"Expected six grain segments, found {len(grain_clips)}")
    for clip in grain_clips:
        clip_id = clip.get("id")
        frame_range = clip.get("frames")
        duration = frame_range[1] - frame_range[0] if isinstance(frame_range, list) and len(frame_range) == 2 else 0
        if not clip_id or duration <= 1:
            raise RuntimeError("Grain clip metadata is incomplete")
        last = duration - 1
        for prop, keys in (
            ("scale", [[0, 16/9, 9/16, "linear"], [last, 16/9, 9/16, "linear"]]),
            ("position", [[0, (1-16/9)/2, (1-9/16)/2, "linear"],
                          [last, (1-16/9)/2, (1-9/16)/2, "linear"]]),
            ("rotation", [[0, 90, "linear"], [last, 90, "linear"]]),
            ("opacity", [[0, 0.575, "linear"], [last, 0.575, "linear"]]),
        ):
            journal_call(p, receipt, f"fit grain {prop} / {clip_id}", "set_keyframes", {
                "projectId": project_id, "timelineId": timeline_id,
                "clipId": clip_id, "property": prop, "keyframes": keys,
            })

    # Enforce the true stack: grain / FG / frame / word / BG / edge support.
    target_video_order = [grain_track["trackId"], accent_track_id]
    now = p.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
    by_name = {(t.get("name") or t.get("label")): t["trackId"] for t in now.get("tracks", []) if t.get("type") == "video"}
    for required in ("Foreground", "Middle", "Background", "Support"):
        if required not in by_name:
            raise RuntimeError(f"Missing expected image plane track: {required}")
    target_video_order = [grain_track["trackId"], by_name["Foreground"], by_name["Middle"],
                          accent_track_id, by_name["Background"], support_track_id]
    for index, track_id in enumerate(target_video_order):
        now = p.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
        videos = [t for t in now.get("tracks", []) if t.get("type") == "video"]
        current = next((i for i, t in enumerate(videos) if t.get("trackId") == track_id), None)
        if current is None:
            raise RuntimeError(f"Video track vanished before reorder: {track_id}")
        if current != index:
            journal_call(p, receipt, f"stack video track at {index}", "manage_tracks", {
                "projectId": project_id, "timelineId": timeline_id,
                "reorder": [{"trackId": track_id, "to": index}],
            })

    final = p.call("get_timeline", {"projectId": project_id, "timelineId": timeline_id})
    video_tracks = [t for t in final.get("tracks", []) if t.get("type") == "video"]
    audio_tracks = [t for t in final.get("tracks", []) if t.get("type") == "audio"]
    if [t.get("name") or t.get("label") for t in video_tracks] != ["Grain", "Foreground", "Middle", "Accents", "Background", "Support"]:
        raise RuntimeError("Final video track stacking differs from the planned BG/accent/MG/FG order")
    if [t.get("name") or t.get("label") for t in audio_tracks] != ["Narration", "SFX"]:
        raise RuntimeError("Final audio tracks are not ordered Narration then SFX")
    snapshot = journal_call(p, receipt, "save pre-export 007 snapshot", "manage_snapshots", {
        "projectId": project_id, "timelineId": timeline_id, "action": "save",
        "name": "007 final edit ready for render 20261101",
    })
    projects_after = p.call("manage_project", {"action": "list"}).get("projects", [])
    visible_after = [x.get("id") for x in projects_after if x.get("isVisible")]
    if visible_before != visible_after:
        raise RuntimeError(f"Visible project changed unexpectedly: {visible_before} -> {visible_after}")
    receipt.update({"status": "ready_for_export", "final_video_track_order": [t.get("name") for t in video_tracks],
                    "final_audio_track_order": [t.get("name") for t in audio_tracks],
                    "snapshot": snapshot, "visible_project_ids_after": visible_after})
    save_receipt(receipt)
    print(json.dumps({"status": receipt["status"], "project_id": project_id, "timeline_id": timeline_id,
                      "video_tracks": receipt["final_video_track_order"],
                      "audio_tracks": receipt["final_audio_track_order"],
                      "accent": receipt["accent"], "sfx": receipt["sfx"],
                      "grain_segments": len(grain_clips), "receipt": str(RECEIPT_PATH)},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        if RECEIPT_PATH.exists():
            try:
                receipt = json.loads(RECEIPT_PATH.read_text(encoding="utf-8"))
                receipt["status"] = "interrupted_pending_inspection"
                receipt["error"] = str(exc)
                save_receipt(receipt)
            except Exception:
                pass
        raise
