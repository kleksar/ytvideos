# v04 — accent motion and opening reframe

**Date:** 1 November 2026  
**Palmier project:** `845D33BD`  
**Current timeline:** `008_en_boyfriend_friend_voice_v04_animated_accents_20261101` (`5D067D47`)  
**Pre-render snapshot:** `F4EA9357` — “Before v04 render — animated accents + S01b side reframe 20261101”  
**Previous version:** v03 timeline `B6614DFE`, restored to its pre-edit state from snapshot `B9120C75`; its original still and static accents are intact.

Apply the current general rules for enumeration, exact human quotations, and grounded character emotion from [Paper Editorial Cue Standard](../../../docs/PAPER_EDITORIAL_CUE_STANDARD.md).

## Accent animation

All 45 phrase PNGs on `Accents` keep their existing image size and horizontal center. At 30 fps, each cue enters from center Y `0.20` with opacity `0`, reaches the fixed center Y `0.18` with opacity `1`, holds, then moves upward to center Y `0.16` with opacity `0`. The movement spans `0.02` of frame height per leg (38.4 px on a 1920 px canvas); X remains centered at `0.50`.

For a cue of `D` frames, clip-relative keys are at `0`, `4`, `D−5`, `D−1`. Smooth interpolation is used by default; the key at frame 4 holds both position and opacity. Durations in this timeline range from 18 to 36 frames, so every cue retains at least a 10-frame full-opacity hold. The minimum-length cue `A44` uses frames `0 / 4 / 13 / 17`.

The Palmier `position` values are top-left normalized coordinates computed from the target center and each PNG's existing width/height. The accent center stays in one safe upper zone; no PNG is resized or moved sideways during the cue. No scene plate or character was animated. Lawrence's original `VO` media and timing are unchanged.

## Opening image

The close two-shot `S01a` at frames `[0,29)` remains. The second opening shot `S01b` at `[29,116)` replaces the former flatter, front-facing trio angle with [`S01b_room_trio_side_v02.png`](../Source/Images/full_frame_redo_v02/S01b_room_trio_side_v02.png), a diagonal three-quarter view of N, B and Matt around the table. This keeps the reveal beat while giving the composition clearer depth and a blank dark-blue wall for the title.

The replacement is a complete `941 × 1672` paper/card diorama. It was reviewed in Chrome ChatGPT.com with the visible GPT-6 **“Очень высокий” (4/5 / Extra High)** setting, against the approved Paper 004 image [`user_reference_parallax_20261101.png`](../../004_last_video/Storyboard/user_reference_parallax_20261101.png). Extra High selected `S01b` for replacement and passed the final diagonal candidate: the first cue “EVERY SINGLE DATE” has clean space at all three vertical positions, away from foliage, characters and the title's readable area. The blush and paper texture were accepted as integrated in the diorama. The first opening still is unchanged.

## Palmier and preview checks

- v04 contains 37 full-frame scene stills, 45 animated accent clips, and one original VO clip on `[0,3855)`; the timeline is `[0,3858)` at 30 fps, `1080 × 1920`, 128.600 seconds.
- All 45 clips report four position and four opacity keys. `inspect_timeline` was checked across the opening cue, the 18-frame `A44`, and the last cue. The 18-frame sample showed four-frame entry, held center and four-frame exit; the opening title stays within the dark wall.
- Before-copy timeline v03 was restored from snapshot `B9120C75`; v04 is the separate working version. Do not edit the Palmier project package directly.
- Export job `5FA2C219-9685-4197-AA87-B6E7F33FCF5C` completed to [`../Deliverables/008_boyfriend_friend_en_1080x1920_30fps_voice_v04_animated_accents_20261101.mp4`](../Deliverables/008_boyfriend_friend_en_1080x1920_30fps_voice_v04_animated_accents_20261101.mp4). `ffprobe`: H.264 High, 1080×1920, 30 fps, 128.600 s; AAC-LC mono, 44.1 kHz, 64.466 kb/s. Full video decode passed. Decoded audio is byte-identical to v03 PCM (`c9792851e27ba5f5d5825731c3268ad3f25dbd0d8ed768caf6fc3157fddb2fb4`). Exported frames at the opening cue and 18-frame A44 confirmed the keyframe movement; this was a frame-sample check, not a full-length real-time playback review.

