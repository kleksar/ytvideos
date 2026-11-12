# Review export contract — Short 02 accent motion v04

Status: `READY_TO_RENDER` for a local review candidate. This is not a final delivery or publication authorization.

## Bound edit

- Palmier project `31F93804`; canonical timeline `7537BAE9`, `Timeline 1`.
- Canvas 1080×1920 (9:16), 30/1 fps, Rec.709 SDR; 1098 frames / 36.6 s.
- Pre-edit snapshot `AEBCE842` (`Before Short02 accent motion repair 20261102`).
- Nine existing V2 cream/orange PNG accents receive only position and opacity keyframes. Existing 3-frame fades are cleared to avoid multiplying them with the approved four-frame opacity ramps. Current PNG mediaRefs, scene intervals, exact cue intervals, static transforms/hold positions, V3 subtitle overlay and A1 edit are preserved.
- Motion: rise from 0.02 canvas fraction below the current hold point; reach full opacity and stop at local frame 4; hold to frame D−5; continue 0.02 canvas fraction above the hold point and fade to zero at D−1. X and scale remain fixed. Palmier position serialization rounds to 0.001 normalized coordinates; the largest verified static-position difference is 0.0005, under 0.6 px on the 1080 px axis.
- Fresh live timeline after edit verified 9/9 cue keyframe tracks, all clip timing/media and transforms unchanged, and V3/V1/A1 tracks unchanged. Evidence: `Work/short02_accent_motion_fix_20261102_v01/timeline_mutation_report.json`.

## Render and audio handling

- Purpose: verify the missing accent movement in the final composition, with screen-space subtitles and baked scene motion unchanged.
- Palmier engine export: H.264, Match Timeline, new temporary path `Work/short02_accent_motion_fix_20261102_v01/scratch/SHORT02_ACCENT_MOTION_NATIVE_EXPORT_v04.mp4`; no overwrite. Engine-managed profile/level/bitrate, AAC encoding and metadata are to be measured, not asserted from settings.
- Final local review candidate: `Work/short02_accent_motion_fix_20261102_v01/previews/PAPER_DETOUR_001_SHORT02_ACCENT_MOTION_REVIEW_20261102_v04.mp4`.
- To honor the unchanged-voice scope, the final preview will take its AAC packets from the exact v03 review candidate `Work/short02-provider-alignment-review-20261102/previews/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v03.mp4` (SHA-256 `bd5d071beb1465db056f6c2746da778b74602814675d3f04b2de425ec4685d6f`) by stream copy. Verify packet/data hashes and duration after mux. Do not create or edit audio.
- Pre-render lifecycle audit: `Edit/MediaLifecycle/pre-render_short02_accent_motion_fix_20261102_v02/`; ownership lock: `channels/paper_detour/.rarovista-timeline-lock/`.

## Acceptance gate

This output is a local review candidate. The previously established overall QA remains `UNVERIFIED` until listening-based subtitle sync and other outstanding checks are completed. No promotion, upload, deletion or release action is included.
