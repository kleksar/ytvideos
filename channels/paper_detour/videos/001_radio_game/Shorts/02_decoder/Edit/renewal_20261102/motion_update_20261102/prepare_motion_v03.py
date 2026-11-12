import hashlib
import json
import sys
from pathlib import Path

ROOT = Path("/Users/diplomat/ytvideos")
RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "automation/image_motion"))
from run import prepare_finished

old_plan = ROOT / "channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Edit/renewal_20261102/motion_prepared.json"
image = ROOT / "channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Source/Images/renewal_20261102/06_reported_comparison_v03_caption-safe_1080x1920_offset100.png"
motion = json.loads((RUN / "motion.json").read_text())
scenes = json.loads(old_plan.read_text())
assert len(scenes) == 7
last = scenes[-1]
assert last["source"]["mediaRef"] == "3BADC5E9"
assert last["source"]["frames"] == [924, 1098]
last["image"] = str(image)
last["image_hash"] = hashlib.sha256(image.read_bytes()).hexdigest()
last["depth_input"] = None
last["depth_hash"] = None
last.pop("clean_video", None)
last.pop("video", None)

run_dir = RUN / "motion"
run_dir.mkdir(exist_ok=True)
scratch = ROOT / "channels/paper_detour/videos/001_radio_game/Work/image-motion-short02-caption-integrate-20261102/scratch"
scratch.mkdir(parents=True, exist_ok=True)
for i, scene in enumerate(scenes, 1):
    scene["video"] = prepare_finished(scene, motion, run_dir, scratch_dir=scratch)
    (RUN / "motion_prepared_v03.json").write_text(json.dumps(scenes, indent=2, ensure_ascii=False) + "\n")
    print(f"prepared {i}/7: {scene['video']}", flush=True)
