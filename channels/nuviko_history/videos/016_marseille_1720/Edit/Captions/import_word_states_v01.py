#!/usr/bin/env python3
"""Import precise one-line word-highlight overlays into the motion target timeline."""
from pathlib import Path
import json, os, sys, time
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from stories.automation.palmier.inspect_connection import PalmierConnection

EP = Path(__file__).resolve().parents[2]
PROJECT = "3C0B4689"
MOTION_RUN = EP / "Edit/ImageMotion/96e776dad46d8e170e1d/run.json"
WORDS = EP / "Edit/Captions/word_states_manifest_source_v01.json"
OUT = EP / "Edit/Captions/word_state_import_v01.json"
PENDING = EP / "Edit/Captions/word_state_import_v01.pending.json"
BATCH = 100


def parse(response, name):
    if response.get("isError"):
        raise RuntimeError(f"{name} returned an error; pending receipt is preserved")
    texts = [x.get("text", "") for x in response.get("content", []) if x.get("type") == "text"]
    if len(texts) != 1:
        raise RuntimeError(f"{name} returned an ambiguous response")
    return json.loads(texts[0])


if PENDING.exists():
    raise SystemExit("Unreconciled pending operation exists; inspect live Palmier before retrying")
motion = json.loads(MOTION_RUN.read_text())
if motion.get("status") != "complete" or not motion.get("target_timeline_id"):
    raise SystemExit("Image-motion apply is not complete; refusing to write subtitles")
wordmap = json.loads(WORDS.read_text())
if wordmap.get("audibleSync") != "UNVERIFIED" or wordmap.get("fps") != 30 or wordmap.get("canvas") != [1920, 1080]:
    raise SystemExit("Unexpected subtitle source/status/geometry")
target_id = motion["target_timeline_id"]
conn = PalmierConnection(); conn.connect()


def read(name, args):
    return parse(conn.request("tools/call", {"name": name, "arguments": args}), name)


state = json.loads(OUT.read_text()) if OUT.exists() else {
    "status": "started", "projectId": PROJECT, "targetTimelineId": target_id,
    "sourceWordMapSha256": wordmap.get("cueMapSha256"), "mediaImport": None, "batches": []}
if state.get("projectId") != PROJECT or state.get("targetTimelineId") != target_id:
    raise SystemExit("Existing subtitle receipt belongs to a different Palmier target")


def save():
    temp = OUT.with_suffix(".tmp")
    temp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    temp.replace(OUT)


def mutate(name, args, operation):
    if PENDING.exists():
        raise RuntimeError("Unreconciled pending operation exists")
    PENDING.write_text(json.dumps({"tool": name, "operation": operation, "arguments": args,
                                   "time": time.time()}, ensure_ascii=False, indent=2) + "\n")
    result = parse(conn.request("tools/call", {"name": name, "arguments": args}), name)
    state.setdefault("operations", []).append({"tool": name, "operation": operation,
                                               "arguments": args, "result": result,
                                               "time": time.time()})
    save(); PENDING.unlink()
    return result


timeline_args = {"projectId": PROJECT, "timelineId": target_id}
timeline = read("get_timeline", timeline_args)
if (timeline.get("fps"), timeline.get("width"), timeline.get("height"), timeline.get("totalFrames")) != (30, 1920, 1080, 16125):
    raise SystemExit("Motion target no longer matches the subtitle frame contract")
scenes = [t for t in timeline.get("tracks", []) if t.get("name", t.get("label")) == "Scenes"]
voice = [t for t in timeline.get("tracks", []) if t.get("name", t.get("label")) == "Narration"]
if len(scenes) != 1 or len(scenes[0].get("clips", [])) != 127 or len(voice) != 1 or len(voice[0].get("clips", [])) != 1:
    raise SystemExit("Unexpected motion target tracks; preserve and reconcile before writing")

# Reconcile the media library by deterministic filenames; directory import is one write.
assets = read("get_media", {"projectId": PROJECT}).get("assets", [])
by_name = {a.get("name"): a for a in assets if a.get("type") == "image" and not a.get("generationStatus")}
expected_files = wordmap["stateFiles"]
missing = [a for a in expected_files if Path(a["path"]).stem not in by_name]
if missing:
    if len(missing) != len(expected_files):
        raise SystemExit("Partially imported subtitle library; reconcile imported files before retry")
    args = {"projectId": PROJECT, "source": {"path": str(Path(expected_files[0]["path"]).parent)},
            "folder": "NuvikoSubtitlesV01"}
    state["mediaImportPending"] = {"source": args["source"]["path"], "count": len(expected_files)}
    save()
    result = mutate("import_media", args, "import all word-state PNGs")
    state["mediaImport"] = result
    assets = read("get_media", {"projectId": PROJECT}).get("assets", [])
    by_name = {a.get("name"): a for a in assets if a.get("type") == "image" and not a.get("generationStatus")}
    missing = [a for a in expected_files if Path(a["path"]).stem not in by_name]
if missing:
    raise SystemExit(f"Subtitle image import is incomplete: {len(missing)} missing; inspect media library")
for item in expected_files:
    asset = by_name[Path(item["path"]).stem]
    if asset.get("type") != "image":
        raise SystemExit(f"Subtitle media type mismatch: {item['id']}")

expected = []
for item in wordmap["timeline"]:
    media_ref = by_name[Path(item["image"]).stem]["id"]
    expected.append({"mediaRef": media_ref, "startFrame": item["startFrame"],
                     "endFrame": item["endFrame"], "imageId": item["image_id"],
                     "cue": item["cue"], "wordIndex": item["word_index"], "word": item["word"]})

# If a previous batch succeeded before interruption, resume only absent exact intervals.
timeline = read("get_timeline", timeline_args)
caption_tracks = [t for t in timeline.get("tracks", []) if t.get("name", t.get("label")) == "Subtitles"]
image_tracks = [t for t in timeline.get("tracks", []) if t.get("type") == "video" and
                any(c.get("mediaType") == "image" for c in t.get("clips", []))]
existing = []
if caption_tracks:
    if len(caption_tracks) != 1:
        raise SystemExit("Multiple subtitle tracks found; reconcile before writing")
    existing = caption_tracks[0].get("clips", [])
elif image_tracks:
    if len(image_tracks) != 1:
        raise SystemExit("Unlabeled image overlay track exists; inspect before writing")
    candidate = image_tracks[0]
    expected_by_span = {(e["startFrame"], e["endFrame"]): e for e in expected}
    for clip in candidate.get("clips", []):
        e = expected_by_span.get(tuple(clip.get("frames", [])))
        if not e or clip.get("mediaRef") != e["mediaRef"]:
            raise SystemExit("Unlabeled overlay track does not match this subtitle manifest")
    if not candidate.get("clips"):
        raise SystemExit("Empty unlabeled overlay track found; inspect before writing")
    mutate("manage_tracks", {**timeline_args, "set": [
        {"trackId": candidate["trackId"], "name": "Subtitles"}]}, "reconcile and name existing subtitle track")
    timeline = read("get_timeline", timeline_args)
    caption_tracks = [t for t in timeline.get("tracks", []) if t.get("name", t.get("label")) == "Subtitles"]
    if len(caption_tracks) != 1:
        raise RuntimeError("Could not reconcile the existing subtitle track name")
    existing = caption_tracks[0].get("clips", [])
existing_by_span = {tuple(c["frames"]): c for c in existing}
for c in existing:
    expected_at_span = next((e for e in expected if (e["startFrame"], e["endFrame"]) == tuple(c["frames"])), None)
    if not expected_at_span or c.get("mediaRef") != expected_at_span["mediaRef"]:
        raise SystemExit("Unexpected subtitle clip on target")
missing_entries = [e for e in expected if (e["startFrame"], e["endFrame"]) not in existing_by_span]
track_index = caption_tracks[0]["index"] if caption_tracks else None
for start in range(0, len(missing_entries), BATCH):
    batch = missing_entries[start:start+BATCH]
    entries = [{"mediaRef": e["mediaRef"], "startFrame": e["startFrame"],
                "endFrame": e["endFrame"]} for e in batch]
    if track_index is not None:
        for entry in entries: entry["trackIndex"] = track_index
    result = mutate("add_clips", {**timeline_args, "entries": entries},
                    f"add subtitle word states {start+1}-{start+len(batch)}")
    timeline = read("get_timeline", timeline_args)
    if track_index is None:
        new_tracks = [t for t in timeline.get("tracks", []) if t.get("type") == "video" and
                      t.get("name", t.get("label")) != "Scenes" and
                      any(c.get("mediaType") == "image" for c in t.get("clips", []))]
        if len(new_tracks) != 1:
            raise RuntimeError("Could not identify the new subtitle track")
        track_index = new_tracks[0]["index"]
        rename = mutate("manage_tracks", {**timeline_args, "set": [
            {"trackId": new_tracks[0]["trackId"], "name": "Subtitles"}]}, "name word-state track Subtitles")
        timeline = read("get_timeline", timeline_args)
    subtitle_track = next(t for t in timeline["tracks"]
                          if t.get("name", t.get("label")) == ("Subtitles" if track_index is not None else "Subtitles"))
    actual_by_span = {tuple(c["frames"]): c for c in subtitle_track.get("clips", [])}
    for e in batch:
        clip = actual_by_span.get((e["startFrame"], e["endFrame"]))
        if clip is None or clip.get("mediaRef") != e["mediaRef"]:
            raise RuntimeError(f"Subtitle batch readback mismatch at frame {e['startFrame']}; reconcile before retry")
    state["batches"].append({"firstEntry": start, "count": len(batch), "trackIndex": track_index})
    save()

# Exact final interval/reference verification and preserved source tracks.
timeline = read("get_timeline", timeline_args)
caption_tracks = [t for t in timeline.get("tracks", []) if t.get("name", t.get("label")) == "Subtitles"]
if len(caption_tracks) != 1 or len(caption_tracks[0].get("clips", [])) != len(expected):
    raise RuntimeError("Subtitle track coverage/count mismatch")
actual_by_span = {tuple(c["frames"]): c for c in caption_tracks[0]["clips"]}
if len(actual_by_span) != len(expected): raise RuntimeError("Duplicate subtitle interval")
cursor = expected[0]["startFrame"]
for e in expected:
    c = actual_by_span.get((e["startFrame"], e["endFrame"]))
    if c is None or c.get("mediaRef") != e["mediaRef"] or c.get("mediaType") != "image":
        raise RuntimeError(f"Subtitle clip readback mismatch at cue {e['cue']} word {e['wordIndex']+1}")
    if e["startFrame"] != cursor: raise RuntimeError("Gap/overlap in word-highlight subtitle coverage")
    cursor = e["endFrame"]
if cursor != 16125: raise RuntimeError("Subtitle track does not reach the end of the scene timeline")
scene_after = next(t for t in timeline["tracks"] if t.get("name", t.get("label")) == "Scenes")
voice_after = next(t for t in timeline["tracks"] if t.get("name", t.get("label")) == "Narration")
if len(scene_after["clips"]) != 127 or len(voice_after["clips"]) != 1:
    raise RuntimeError("Motion or narration track changed while adding subtitles")
snapshot = mutate("manage_snapshots", {**timeline_args, "action": "save",
                                       "name": "Word-highlight subtitles v01"}, "snapshot subtitles target")
state.update({"status": "subtitle_timeline_ready", "targetTimeline": timeline,
              "wordStateCount": len(expected), "uniqueImages": len(expected_files),
              "snapshot": snapshot, "coverageFrames": [expected[0]["startFrame"], cursor],
              "timingStatus": "SOURCE_TIME_DRAFT_REVIEW_REQUIRED", "audibleSync": "UNVERIFIED"})
save()
print(json.dumps({"status": state["status"], "projectId": PROJECT, "timelineId": target_id,
                  "wordStates": len(expected), "uniqueImages": len(expected_files),
                  "snapshot": snapshot, "receipt": str(OUT)}, ensure_ascii=False))
