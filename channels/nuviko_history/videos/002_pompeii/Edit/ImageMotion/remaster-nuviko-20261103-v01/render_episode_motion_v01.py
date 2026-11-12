#!/usr/bin/env python3
"""Render the Pompeii motion package from exact current timeline clip spans."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
EPISODE = ROOT.parents[2]
REPO = ROOT.parents[5]
WORK = EPISODE / "Work/remaster-nuviko-20261103-v01"
ASSETS = EPISODE / "Assets/Generated/Pompeii_Remake_v01"
MOTION_ASSETS = EPISODE / "Assets/Generated/Pompeii_Motion_v01"
LAYER_ROOT = ASSETS / "layered_v01"
TIMING = json.loads((ROOT / "timeline_clip_map_v02.json").read_text())
INPUTS = json.loads((WORK / "motion_input_manifest_v01.json").read_text())
VISION = json.loads((ROOT / "layer_prep_receipt_v01.json").read_text())
SAM = json.loads((ROOT / "sam2_layer_prep_receipt_v01.json").read_text())
LAYER_BY_SCENE = {int(row["scene"]): row for row in VISION + SAM}
INPUT_BY_SCENE = {int(row["scene_id"][1:]): row for row in INPUTS["images"]}
TIMING_BY_SCENE = {int(row["scene"]): row for row in TIMING["clips"]}
CLEAN_DIR = WORK / "scratch/clean_motion_v01"
RECEIPTS = ROOT / "motion_receipts_v01"
RENDERER = ROOT / "render_pompeii_motion_v01.py"
GRAIN = REPO / "automation/image_motion/apply_g08_layered.py"
PYTHON = REPO / "Shared/Image_Motion/Tools/sam2-local/.venv/bin/python"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe(path: Path) -> dict:
    result = subprocess.run([
        "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)
    ], check=True, capture_output=True, text=True)
    data = json.loads(result.stdout)
    video = next(x for x in data["streams"] if x["codec_type"] == "video")
    return {
        "width": int(video["width"]), "height": int(video["height"]),
        "fps": video["r_frame_rate"], "frames": int(video.get("nb_frames", 0)),
        "duration_seconds": float(data["format"]["duration"]),
        "codec": video["codec_name"], "pix_fmt": video.get("pix_fmt"),
    }


def render_one(scene: int) -> dict:
    started = time.monotonic()
    input_row = INPUT_BY_SCENE[scene]
    layer = LAYER_BY_SCENE[scene]
    timing = TIMING_BY_SCENE[scene]
    frames = int(timing["frames"])
    source = EPISODE / input_row["file"]
    if digest(source) != input_row["sha256"]:
        raise RuntimeError(f"K{scene:03d}: source hash changed")
    if int(timing["endFrame"]) - int(timing["startFrame"]) != frames:
        raise RuntimeError(f"K{scene:03d}: malformed timeline span")
    for candidate in (MOTION_ASSETS / f"K{scene:03d}.mp4",):
        if candidate.exists() and not candidate.with_suffix(".mp4.g08.json").exists():
            raise FileExistsError(f"K{scene:03d}: final asset exists without grain receipt")

    clean = CLEAN_DIR / f"K{scene:03d}.mp4"
    final = MOTION_ASSETS / f"K{scene:03d}.mp4"
    source_hash = input_row["sha256"]
    if not final.exists():
        if not clean.exists():
            subprocess.run([
                str(PYTHON), str(RENDERER),
                "--foreground", layer["foreground"],
                "--background", layer["background"],
                "--mask", layer["mask"],
                "--output", str(clean), "--scene", str(scene), "--frames", str(frames),
            ], check=True, capture_output=True, text=True)
        else:
            print(json.dumps({"scene": scene, "event": "clean_exists_resume_from_g08"}), flush=True)
        subprocess.run([
            str(PYTHON), str(GRAIN), "--input", str(clean), "--output", str(final),
            "--image-sha256", source_hash, "--frames", str(frames), "--fps", "30", "--preset", "g08",
        ], check=True, capture_output=True, text=True)

    receipt = {
        "scene": scene,
        "timeline_clip_id": timing["clipId"],
        "timeline_media_ref": timing["mediaRef"],
        "timeline_frames": [timing["startFrame"], timing["endFrame"]],
        "timeline_frame_count": frames,
        "source": str(source),
        "source_sha256": source_hash,
        "foreground": layer["foreground"],
        "background": layer["background"],
        "mask": layer["mask"],
        "clean_motion": str(clean),
        "final_motion": str(final),
        "final_motion_sha256": digest(final),
        "final_probe": probe(final),
        "g08_receipt": str(final.with_suffix(".mp4.g08.json")),
        "order": ["contain-fit layers", "clean layered parallax", "opposed camera", "G08"],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }
    receipt_path = RECEIPTS / f"K{scene:03d}.json"
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = receipt_path.with_suffix(".json.partial")
    tmp.write_text(json.dumps(receipt, indent=2) + "\n")
    tmp.replace(receipt_path)
    return receipt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenes", help="Comma-separated scene numbers; omit to render all")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    scenes = [int(x) for x in args.scenes.split(",")] if args.scenes else list(range(1, 180))
    if not scenes or any(s not in INPUT_BY_SCENE for s in scenes):
        raise SystemExit("Unknown scene in request")
    if args.workers < 1 or args.workers > 3:
        raise SystemExit("workers must be 1–3")
    motion_manifest = {
        "version": 1,
        "episode": "002_pompeii",
        "run": WORK.name,
        "project_id": TIMING["projectId"],
        "timeline_id": TIMING["timelineId"],
        "fps": 30,
        "timeline_canvas": [TIMING["width"], TIMING["height"]],
        "motion_render_canvas": [1920, 1080],
        "contain_fit": "Preserve the complete still inside a 16:9 frame; no crop; black matte outside original aspect.",
        "foreground_travel_reference_px": 12,
        "camera": {"scale": 1.10, "travel_width_fraction": 0.045, "trajectory": "linear"},
        "grain": "g08, after parallax and camera",
        "order": ["still", "separate foreground+restored background", "clean parallax", "opposed camera", "G08", "Palmier subtitles"],
        "inherited_clip_transforms_to_reset": [
            row["scene"] for row in TIMING["clips"] if row["transform"]
        ],
        "inherited_source_trims_to_clear": [
            row["scene"] for row in TIMING["clips"] if row["trimStartFrame"] or row["trimEndFrame"]
        ],
        "clips": [
            {
                "scene": scene,
                "clip_id": TIMING_BY_SCENE[scene]["clipId"],
                "timeline_frames": [TIMING_BY_SCENE[scene]["startFrame"], TIMING_BY_SCENE[scene]["endFrame"]],
                "frames": TIMING_BY_SCENE[scene]["frames"],
                "source": INPUT_BY_SCENE[scene]["file"],
                "source_sha256": INPUT_BY_SCENE[scene]["sha256"],
                "foreground": LAYER_BY_SCENE[scene]["foreground"],
                "background": LAYER_BY_SCENE[scene]["background"],
                "mask": LAYER_BY_SCENE[scene]["mask"],
                "clean_output": str(CLEAN_DIR / f"K{scene:03d}.mp4"),
                "final_output": str(MOTION_ASSETS / f"K{scene:03d}.mp4"),
            }
            for scene in range(1, 180)
        ],
    }
    manifest_path = ROOT / "motion_manifest_v01.json"
    if manifest_path.exists():
        existing = json.loads(manifest_path.read_text())
        if existing != motion_manifest:
            raise SystemExit("Existing motion manifest differs; create a new version")
    else:
        manifest_path.write_text(json.dumps(motion_manifest, indent=2) + "\n")
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    MOTION_ASSETS.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    errors = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(render_one, scene): scene for scene in scenes}
        for future in as_completed(futures):
            scene = futures[future]
            try:
                row = future.result()
                print(json.dumps({"scene": scene, "status": "complete", "frames": row["timeline_frame_count"],
                                  "seconds": row["elapsed_seconds"], "sha256": row["final_motion_sha256"]}), flush=True)
            except BaseException as exc:
                errors.append({"scene": scene, "error": repr(exc)})
                print(json.dumps({"scene": scene, "status": "failed", "error": repr(exc)}), flush=True)
    report = {"run": WORK.name, "scenes_requested": scenes, "completed": len(scenes) - len(errors),
              "failed": errors, "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    path = ROOT / "motion_batch_status_v01.json"
    path.write_text(json.dumps(report, indent=2) + "\n")
    if errors:
        raise SystemExit(f"{len(errors)} scene render(s) failed; see {path}")


if __name__ == "__main__":
    main()
