# Accent cue sheet v02 — higher position and upward motion

Supersedes v01 geometry/motion only. User selected the previous TEXT AS SOUND position as the model for all scenes, requested more space above subtitles, and specified rise → hold → rise while fading out. Words, frames and two-line layout remain those in v01; audio is unchanged.

All five cues: primary hold-center (0.50,0.16) at 1080×1920; common face-height 80 px. Entry starts at Y=0.18, reaches hold Y=0.16 over four frames with opacity 0→100%. Hold is stationary. Exit starts at D−5 and reaches Y=0.14 and opacity 0% at D−1. X and scale do not change. No letter sounds. Exact overlay layer bounds are in `Assets/Generated/accents-v05/manifest.json`, input `accent_input_v04.json`.

Current full review: `Work/rework_20261102/full_review_accents_v03/short03_accents_REVIEW.mp4`. Renderer `add_accents_review_v03.py` copies the continuous base's audio stream, with no audio re-encoding. Original voice source unchanged. Review-only automatic cue timings remain unverified by listening. Artwork is dense in the upper zone of S01/S03/S07: accents approach the ear motif, radio handle/buttons and monitor casing respectively; the rendered top placement needs user visual review before delivery acceptance. Do not describe a static geometry PASS as proof of protected-object clearance.
