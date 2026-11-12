#!/usr/bin/env python3
"""Build an exact-frame QA sample plan for Short 02 review export v02."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path("/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Shorts/02_decoder")
MEDIA = ROOT / "Deliverables/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v02.mp4"
CUES = ROOT / "Edit/renewal_20261102/subtitle_asr_retime_20261102/cue_map.json"
OUT = ROOT / "Edit/renewal_20261102/review_qa_plan_v02.json"
FPS = 30

digest = hashlib.sha256(MEDIA.read_bytes()).hexdigest()
cues = json.loads(CUES.read_text())["groups"]
cue_plan = []
for i, cue in enumerate(cues, 1):
    start = round(cue["start"] * FPS)
    end = round(cue["end"] * FPS)
    cue_plan.append({
        "id": f"C{i:02d}",
        "start": start,
        "end": end,
        "entry_end": min(end, start + 3),
        "exit_start": max(start, end - 3),
    })

plan = {
    "sha256": digest,
    "frame_count": 1098,
    "fps": "30/1",
    "required_review_checks": [
        "stream_metadata", "full_decode", "frame_sampling", "motion_framing",
        "cue_timing", "audio_signal", "subjective_audio_listening", "independent_review"
    ],
    "freshness": {
        "status": "CURRENT",
        "evidence": "Palmier project 31F93804 / timeline 7537BAE9; saved snapshot named Short02 scene07 v03 and ASR subtitle review draft 20261102 at 16:58 local; review MP4 rendered from that live timeline at 17:02 local."
    },
    "expected": {
        "video": {"width": 1080, "height": 1920, "codec_name": "h264", "pix_fmt": "yuv420p", "color_space": "bt709"},
        "audio": {"required": True, "codec_name": "aac", "channels": 2, "sample_rate": 44100}
    },
    "scenes": [
        {"id": "S01", "start": 0, "end": 177},
        {"id": "S02", "start": 177, "end": 330},
        {"id": "S03", "start": 330, "end": 468},
        {"id": "S04", "start": 468, "end": 606},
        {"id": "S05", "start": 606, "end": 774},
        {"id": "S06", "start": 774, "end": 924},
        {"id": "S07", "start": 924, "end": 1098}
    ],
    "cues": cue_plan,
    "extra_frames": [924, 925, 1009, 1095, 1097]
}
OUT.write_text(json.dumps(plan, indent=2) + "\n")
print(f"{OUT}\nsha256={digest}\ncues={len(cue_plan)}")
