"""Prepare the exact Endurance v02 edit from manually selected and reviewed sources."""
from datetime import datetime
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EPISODE = HERE.parent.parent
ROOT = EPISODE.parents[3]
EDIT = EPISODE / "Edit"
OUT = EPISODE / "Deliverables" / "Endurance_en_review_v02.mp4"
spec = importlib.util.spec_from_file_location("episode_montage", ROOT / "automation/ffmpeg_montage/montage.py")
montage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(montage)


def read(path):
    return json.loads(path.read_text())


def create(path, data):
    with path.open("x") as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
        out.write("\n")


def camera(mode, focus, subject, reason):
    if mode in ("I", "O"):
        zoom = "in" if mode == "I" else "out"
        scale = [1.0, 1.018] if mode == "I" else [1.018, 1.0]
        centers = [[.5, .5], [.5, .5]]
        direction = "none"
    else:
        zoom = "none"
        scale = [1.022, 1.022]
        left, right = [.495, .5], [.505, .5]
        centers = [left, right] if mode == "L" else [right, left]
        direction = "right_to_left" if mode == "L" else "left_to_right"
    return {
        "direction": direction, "zoom": zoom,
        "camera": {
            "subject": subject, "focus": focus, "reason": reason,
            "start": {"center": centers[0], "scale": scale[0]},
            "end": {"center": centers[1], "scale": scale[1]},
        },
    }


def main():
    board = read(HERE / "SHOT_MAP_v02.json")
    selected = read(HERE / "SELECTION_v02.json")
    slots = board["slots"]
    assert set(selected) == {slot["id"] for slot in slots} and len(selected) == 122
    motions = {}
    for row in (HERE / "MOTION_REVIEW.tsv").read_text().splitlines():
        ident, mode, x, y, subject, reason = row.split("|")
        motions[ident] = camera(mode, [float(x), float(y)], subject, reason)
    assert len(motions) == 112
    tested_opening = read(HERE / "hook_probe_v03/input_manifest.json")["scenes"]
    plan = read(EDIT / "ENDURANCE_EN_EDIT_v01.json")
    plan["subtitles"].pop("review", None)
    plan["purpose"] = "Endurance complete visual rebuild v02 for review"
    plan["status"] = "READY_TO_RENDER"
    plan["scenes"] = []
    image_records = []
    for idx, slot in enumerate(slots):
        record = selected[slot["id"]]
        assert record["status"] == "SELECTED", slot["id"]
        assert montage.delivery.file_record(record["file"]["path"]) == record["file"], slot["id"]
        image_records.append(record["file"])
        if idx < len(tested_opening):
            s = dict(tested_opening[idx])
        else:
            s = motions[slot["id"]]
        a, b = slot["frames"]
        s.update(image=record["file"]["path"], start_frame=a, end_frame=b)
        plan["scenes"].append(s)
    assert len({f["sha256"] for f in image_records}) == 122
    prepared = montage.validate(plan, EPISODE)
    assert prepared["frames"] == 16796
    montage.delivery.validate_words(plan, EPISODE, prepared["frames"])
    revision = EDIT / "ENDURANCE_EN_EDIT_v02.json"
    assert not OUT.exists()
    create(revision, plan)

    passport = read(EDIT / "ENDURANCE_EXPORT_CONTRACT_v01.json")
    record = montage.delivery.file_record(revision)
    inputs = montage.delivery.render_inputs(revision, plan, EPISODE)
    assert all(rec in inputs for rec in image_records)
    passport["purpose"] = "New full visual edition of Endurance v02 for user review"
    profile = ROOT / ".agents/skills/ytv-video-export/references/delivery.md"
    passport["settings_profile"] = montage.delivery.file_record(profile)
    passport["edit"].update(
        timeline_id=str(revision),
        timeline_read_path=str(revision),
        timeline_read_sha256=record["sha256"],
        saved_revision_evidence=str(HERE / "SELECTION_v02.json"),
        dependencies=inputs,
    )
    existing = HERE / "opening_probe_v02/subtitle_contract.json"
    passport["subtitle_handoff"] = {
        "contract": str(existing),
        "sha256": sha256(existing.read_bytes()).hexdigest(),
        "review": str(HERE / "hook_probe_v03/REVIEW.md"),
        "status": "UNCHANGED_TIMING_REBIND_AT_RENDER__PLACEMENT_CHECK_ON_FULL_EXPORT",
    }
    passport["preflight"].update(
        time=datetime.now().astimezone().isoformat(),
        authorization_references=["User requested complete rebuild of Endurance images and edit using linked discussions"],
        fresh_settings_evidence=str(HERE / "SELECTION_v02.json"),
        output_path=str(OUT),
        writer_and_export_state="New exclusive FFmpeg output and work path",
    )
    passport["source_resolution_note"] = "ImageGen native sizes measured separately per file. FFmpeg scales to the delivery canvas."
    create(EDIT / "ENDURANCE_EXPORT_CONTRACT_v02.json", passport)
    print(f"Prepared {len(image_records)} verified source bindings for {OUT}")


if __name__ == "__main__":
    main()
