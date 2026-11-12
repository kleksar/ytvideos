# Review export contract — Short 02 renewal v03

Status: `READY_TO_RENDER` as a review-only synchronization candidate. It is not a final deliverable and is not authorized for upload.

## Bound edit

- Palmier project `31F93804`; canonical timeline `7537BAE9`, `Timeline 1`.
- Canvas 1080×1920 (9:16), 30/1 fps, Rec.709 SDR; timeline end 1098 exclusive frames / 36.6 s.
- Snapshot before this pass: `24814FA4` (`Before Short02 provider timing review overlay 20261102`). Snapshot after update: `4C4EE863` (`Short02 provider timing review candidate 20261102`).
- V3 clip `DC4C604C` now references the 1098-frame, silent ProRes 4444 overlay `short02_subtitles_provider_timing_review_20261102.mov`, SHA-256 `2b201b2ed905abea882d9e71ebe8fd619db820d7402467a280d6f14789afd9f3`.
- V2 accents, V1 seven motion scenes (including scene 07 v03), A1 clip identity/range and all other tracks are preserved. A1 remains `preview_mix_36p6_no_sfx_stereo.wav`, SHA-256 `d8e942f34436dc41c3d3a2eed91e99bcefcaa19371d1cecc01d599b9327495a2`; no audio has been generated or edited.
- Subtitle design/grouping remains the accepted 41 groups, 87 words, single line, Chalkboard SE Bold 72 px, 750 px safe width, fixed baseline at y=1479, continuous display/highlight policy. Timing now follows the original conformed provider map, checked against the independent forced-alignment estimate; exact word maps and comparison are linked from `subtitle_forced_alignment_20261102/COMPARISON.md`.

## Render request

- Purpose: owner review of the subtitle timing on the current motion edit. Audible synchronization remains `UNVERIFIED`.
- Output: `/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game/Shorts/02_decoder/Work/short02-provider-alignment-review-20261102/previews/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v03.mp4` (new path; do not overwrite v02 or current delivery).
- MPEG-4 / H.264 / Match Timeline; 30 fps and Rec.709 follow the actual timeline. Palmier exposes no bitrate, H.264 profile/level, AAC rate/bitrate/channel-map, range, or fast-start controls in this route; these remain engine-managed and must be measured in QA.
- Audio: retain the exact existing A1 edit and source. The review export may re-encode through Palmier's engine; no normalization, replacement, or sound design is part of this pass.
- Pre-render storage audit: `pre_render_provider_review_audit_20261102/audit.json`; bounded scope, no coverage errors. Target occupancy was checked by exact project/timeline read; there is no other writer under the shared radio lock.

## Acceptance gate

This review export is a timing comparison, not a publishable file. It must remain outside `Deliverables/current.json`. The final release still requires the owner's listening-based word-sync check against this exact candidate, the Paper final-video QA contract, and a new release check. Preserve the existing A1 and original published video until a fully verified replacement exists.
