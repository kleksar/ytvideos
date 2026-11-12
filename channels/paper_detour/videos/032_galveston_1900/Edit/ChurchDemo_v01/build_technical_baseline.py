"""Build an isolated G08 technical comparison from already accepted church art."""
import json
import pathlib
from palmier_client import call, ROOT

episode = ROOT.parent.parent
pid = "25533909"
before = json.loads((ROOT / "get_timeline_before.json").read_text())
before = json.loads(before["result"]["content"][0]["text"])
plan = json.loads((episode / "Edit/ImageMotion/77fd09462902d1474398/plan.json").read_text())
state_path = ROOT / "technical_baseline.json"
if state_path.exists():
    state=json.loads(state_path.read_text());tid=state["timeline_id"]
    live=call("get_timeline",{"projectId":pid,"timelineId":tid},"resume_empty_baseline")
    if state["status"]!="building" or live["tracks"]:
        raise SystemExit("Existing nonempty target: inspect before another mutation")
else:
    snapshot = call("manage_snapshots", {"projectId": pid, "timelineId": "6C26D0C3", "action": "save", "name": "Before isolated church G08 demo"}, "full_before_snapshot")
    created = call("create_timeline", {"projectId": pid, "name": "Galveston church G08 technical baseline v01"}, "create_technical_baseline")
    tid = created.get("timelineId")
    if not tid:
        raise RuntimeError(str(created))
    state = {"project_id": pid, "timeline_id": tid, "status": "building", "scope": "EXISTING_ART_G08_TECHNICAL_COMPARISON", "full_film_source": "6C26D0C3", "audio_source_in_frame": 14173, "frame_count": 668, "fps": 30, "new_creative_storyboard": "PENDING_EXTRA_HIGH_OR_USER_EXCEPTION"}
    state_path.write_text(json.dumps(state, indent=2))
call("set_project_settings", {"projectId": pid, "timelineId": tid, "width": 2560, "height": 1440, "outputColorSpace": "rec709"}, "technical_canvas")
entries = [{"mediaRef": plan[106+i]["source"]["mediaRef"], "startFrame": i*167, "endFrame": (i+1)*167} for i in range(4)]
call("add_clips", {"projectId": pid, "timelineId": tid, "entries": entries}, "add_accepted_church_stills")
now = call("get_timeline", {"projectId": pid, "timelineId": tid}, "technical_stills")
scene_track = now["tracks"][0]
call("manage_tracks", {"projectId": pid, "timelineId": tid, "set": [{"trackId": scene_track["trackId"], "name": "Scenes"}]}, "name_scene_track")
for i, clip in enumerate(scene_track["clips"]):
    old = before["tracks"][1]["clips"][106+i]
    for prop in ("position", "scale"):
        keys = old.get("keyframes", {}).get(prop)
        if keys:
            old_end = keys[-1][0]
            keys = [[round(k[0]*166/old_end), *k[1:]] for k in keys]
            call("set_keyframes", {"projectId": pid, "timelineId": tid, "clipId": clip["id"], "property": prop, "keyframes": keys}, f"technical_scene_{i+1}_{prop}")
call("add_clips", {"projectId": pid, "timelineId": tid, "entries": [{"mediaRef": "666A8A59", "startFrame": 0, "source": [14173/30, 14841/30]}]}, "add_existing_odom_excerpt")
now = call("get_timeline", {"projectId": pid, "timelineId": tid}, "technical_audio")
at = next(t for t in now["tracks"] if t["type"] == "audio")
call("manage_tracks", {"projectId": pid, "timelineId": tid, "set": [{"trackId": at["trackId"], "name": "Dialogue"}]}, "name_dialogue")
# Existing approved PNGs and geometry; only enough hold is restored, no new wording.
old_cues = before["tracks"][0]["clips"][-3:-1]
cue_specs = [(325, 379), (615, 660)]
call("add_clips", {"projectId": pid, "timelineId": tid, "entries": [{"mediaRef": old["mediaRef"], "startFrame": a, "endFrame": b} for old, (a,b) in zip(old_cues, cue_specs)]}, "add_existing_accents")
now = call("get_timeline", {"projectId": pid, "timelineId": tid}, "technical_with_cues")
ct = next(t for t in now["tracks"] if t["type"] == "video" and t["trackId"] != scene_track["trackId"])
call("manage_tracks", {"projectId": pid, "timelineId": tid, "set": [{"trackId": ct["trackId"], "name": "Accents"}]}, "name_accents")
for clip, old, (a,b) in zip(ct["clips"], old_cues, cue_specs):
    call("set_clip_properties", {"projectId": pid, "timelineId": tid, "clipIds": [clip["id"]], "transform": old["transform"]}, "cue_transform_"+clip["id"])
    d=b-a
    pk=old["keyframes"]["position"]
    positions=[[0,*pk[0][1:3]],[4,*pk[1][1:3],"hold"],[d-5,*pk[-2][1:3]],[d-1,*pk[-1][1:3]]]
    for prop,keys in [("position",positions),("opacity",[[0,0],[4,1,"hold"],[d-5,1],[d-1,0]])]:
        call("set_keyframes", {"projectId":pid,"timelineId":tid,"clipId":clip["id"],"property":prop,"keyframes":keys},"cue_"+clip["id"]+"_"+prop)
call("manage_tracks", {"projectId": pid, "timelineId": tid, "reorder": [{"trackId": ct["trackId"], "to": 0}]}, "accents_above_scenes")
final = call("get_timeline", {"projectId": pid, "timelineId": tid}, "technical_baseline_final")
assert final["totalFrames"] == 668, final["totalFrames"]
source_manifest=[]
for i in range(4):
    source_manifest.append({"mediaRef":plan[106+i]["source"]["mediaRef"],"image":plan[106+i]["image"],"depth_zoom":plan[106+i]["depth_zoom"],"camera":"existing"})
(ROOT/"technical_sources.json").write_text(json.dumps(source_manifest,indent=2))
config={"episode_dir":str(episode),"project_id":pid,"timeline_id":tid,"source_manifest":"technical_sources.json","scene_track":"Scenes","preset":"gentle-aligned","grain":"g08","camera":"existing","depth_zoom":1.0}
(ROOT/"technical_motion.json").write_text(json.dumps(config,indent=2))
state["status"]="still_baseline_ready"
state["scene_intervals"]=[[i*167,(i+1)*167] for i in range(4)]
state["cue_intervals"]=cue_specs
state_path.write_text(json.dumps(state,indent=2))
print(json.dumps(state))
