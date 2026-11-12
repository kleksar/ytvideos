#!/usr/bin/env python3
"""Add the 118 accepted-score stills and the original audio to Palmier v07.

This episode-specific assembly preserves the recovered M4A at native speed.
It mutates only the explicit v07 timeline and journals every batch.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
SERIES = ROOT / "channels/nuviko_history/videos/009_black_death"
RUN = SERIES / "Edit/Long/v07_original_audio"
MANIFEST = RUN / "manifest_v01.json"
RECEIPT = RUN / "palmier_assembly_receipt_v01.json"
PROJECT_ID = "C7F9F043"
SOURCE_TIMELINE_ID = "05828824"
TARGET_TIMELINE_ID = "F382ACF5"
MEDIA_FOLDER = "Black Death v07"
MIN_FREE_BYTES = 8 * 1024**3


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_tool_response(result):
    if result.get("isError"):
        raise RuntimeError(result)
    contents = [x.get("text", "") for x in result.get("content", []) if x.get("type") == "text"]
    if len(contents) != 1:
        raise RuntimeError(f"Unexpected Palmier response: {result}")
    return json.loads(contents[0])


def call(connection, name, args):
    return load_tool_response(connection.request("tools/call", {"name": name, "arguments": args}))


def timeline(connection, timeline_id):
    return connection.read_tool("get_timeline", {"projectId": PROJECT_ID, "timelineId": timeline_id})


def clip_index(tl):
    return {clip["id"]: clip for track in tl.get("tracks", []) for clip in track.get("clips", [])}


def baseline(tl):
    return {
        "timelineId": tl["timelineId"], "name": tl["name"], "totalFrames": tl["totalFrames"],
        "fps": tl["fps"], "width": tl["width"], "height": tl["height"],
        "tracks": [{"trackId": t["trackId"], "type": t["type"],
                    "clipIds": sorted(c["id"] for c in t.get("clips", [])),
                    "captionGroups": [[g["captionGroupId"], g["clipCount"], g["frameRange"]]
                                      for g in t.get("captionGroups", [])]}
                   for t in tl.get("tracks", [])],
    }


def main():
    import shutil
    if not RECEIPT.exists():
        raise SystemExit(f"Missing mutation receipt: {RECEIPT}")
    receipt = json.loads(RECEIPT.read_text())
    if receipt.get("targetTimelineId") != TARGET_TIMELINE_ID or receipt.get("status") not in ("started", "tracks_cleared"):
        raise SystemExit(f"Receipt is not in a resumable clear state: {receipt.get('status')}")
    m = json.loads(MANIFEST.read_text())
    if m.get("voice_speed_applied") != 1.0 or m.get("frames") != 21224 or len(m.get("scenes", [])) != 118:
        raise SystemExit("Manifest does not describe the locked original-audio 118-scene cut")
    if shutil.disk_usage(SERIES).free < MIN_FREE_BYTES:
        raise SystemExit("Less than 8 GiB free; assembly blocked")
    for scene in m["scenes"]:
        p = Path(scene["path"])
        if not p.is_file() or sha(p) != scene["sha256"]:
            raise SystemExit(f"Missing or changed image: {p}")
    voice = Path(m["voice"])
    if not voice.is_file() or sha(voice) != m["voice_sha256"]:
        raise SystemExit("Original audio missing or changed")

    sys.path.insert(0, str(ROOT / "automation/palmier"))
    from inspect_connection import PalmierConnection
    c = PalmierConnection(); c.connect()
    source = timeline(c, SOURCE_TIMELINE_ID)
    source_baseline = baseline(source)
    target = timeline(c, TARGET_TIMELINE_ID)
    if (target["width"], target["height"], target["fps"]) != (1920, 1080, 30):
        raise SystemExit("v07 must be 1920x1080/30")
    if target.get("tracks"):
        raise SystemExit("v07 already has tracks; inspect receipt and live state before proceeding")
    if receipt.get("sourceV06Baseline") and receipt["sourceV06Baseline"] != source_baseline:
        raise SystemExit("Source v06 changed since the recorded baseline")
    receipt["sourceV06Baseline"] = source_baseline
    receipt["status"] = "tracks_cleared"

    media = call(c, "get_media", {"projectId": PROJECT_ID, "folder": MEDIA_FOLDER}).get("assets", [])
    by_name = {a["name"]: a for a in media}
    refs = {}
    for s in m["scenes"]:
        name = Path(s["path"]).stem
        asset = by_name.get(name)
        if not asset or asset.get("type") != "image":
            raise SystemExit(f"Palmier image not found by exact imported name: {name}")
        refs[s["shot_id"]] = asset["id"]
    voice_name = Path(m["voice"]).stem
    voice_asset = by_name.get(voice_name)
    if not voice_asset or voice_asset.get("type") != "audio":
        raise SystemExit("Palmier import of original audio not found")
    if len(set(refs.values())) != 118:
        raise SystemExit("Palmier image refs are not unique")

    added = []
    for offset in range(0, 118, 8):
        subset = m["scenes"][offset:offset + 8]
        before = timeline(c, TARGET_TIMELINE_ID)
        before_ids = set(clip_index(before))
        # On the empty clone, omit trackIndex so Palmier creates the video
        # track; an explicit index is only valid after a track exists.
        entries = [{"mediaRef": refs[s["shot_id"]], "startFrame": s["start"],
                    "endFrame": s["end"]} for s in subset]
        receipt["pending"] = {"action": "add_image_batch", "sceneIndexes": [offset, offset + len(subset)]}
        RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
        result = call(c, "add_clips", {"projectId": PROJECT_ID, "timelineId": TARGET_TIMELINE_ID,
                                         "entries": entries})
        new_clips = result.get("clips", [])
        after = timeline(c, TARGET_TIMELINE_ID)
        after_map = clip_index(after)
        if len(new_clips) != len(subset):
            raise RuntimeError("Palmier returned an unexpected image clip count")
        verified = []
        for scene, clip in zip(subset, new_clips):
            actual = after_map.get(clip["id"])
            if not actual or actual.get("frames") != [scene["start"], scene["end"]] or actual.get("mediaRef") != refs[scene["shot_id"]]:
                raise RuntimeError(f"Image clip failed verification: {scene['shot_id']}")
            verified.append({"shot_id": scene["shot_id"], "clipId": clip["id"],
                             "frames": actual["frames"], "mediaRef": actual["mediaRef"]})
        if set(after_map) - before_ids != {x["clipId"] for x in verified}:
            raise RuntimeError("Unexpected clips appeared during image batch")
        added.extend(verified)
        receipt.setdefault("imageBatches", []).append({"sceneIndexes": [offset, offset + len(subset)],
                                                        "clips": verified,
                                                        "actionId": result.get("actionId")})
        receipt.pop("pending", None); receipt["imageClips"] = added
        receipt["status"] = "images_added"
        RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")

    before = timeline(c, TARGET_TIMELINE_ID)
    receipt["pending"] = {"action": "add_original_audio", "path": str(voice)}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    audio_result = call(c, "add_clips", {"projectId": PROJECT_ID, "timelineId": TARGET_TIMELINE_ID,
                                          "entries": [{"mediaRef": voice_asset["id"], "startFrame": 0}]})
    after = timeline(c, TARGET_TIMELINE_ID)
    audio_clips = [clip for track in after["tracks"] for clip in track.get("clips", [])
                   if clip.get("mediaRef") == voice_asset["id"]]
    if len(audio_clips) != 1 or audio_clips[0]["frames"][0] != 0:
        raise RuntimeError("Original audio clip did not land once at frame 0")
    if abs(audio_clips[0]["frames"][1] - 21224) > 2 or after["totalFrames"] != 21224:
        raise RuntimeError(f"Timeline duration differs from original audio contract: {audio_clips[0]['frames']} / {after['totalFrames']}")
    if baseline(timeline(c, SOURCE_TIMELINE_ID)) != source_baseline:
        raise RuntimeError("Source v06 changed during assembly")
    receipt.pop("pending", None)
    receipt.update({"audioClip": {"clipId": audio_clips[0]["id"], "frames": audio_clips[0]["frames"],
                                  "mediaRef": voice_asset["id"], "assetSha256": m["voice_sha256"]},
                    "timelineFrames": after["totalFrames"], "durationSeconds": after["durationSeconds"],
                    "status": "assembled_stills_and_original_audio",
                    "sourceV06Unchanged": True,
                    "tracks": [{"trackId": t["trackId"], "type": t["type"],
                                "clipCount": len(t.get("clips", []))}
                               for t in after.get("tracks", [])],
                    "audioActionId": audio_result.get("actionId")})
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"timelineId": TARGET_TIMELINE_ID, "frameCount": after["totalFrames"],
                      "imageClips": len(added), "audioClip": audio_clips[0]["frames"],
                      "tracks": receipt["tracks"], "sourceV06Unchanged": True}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
