# Motion and text visual QA — v01

- Episode: Paper Detour 028 — Taj Mahal.
- Project: `Paper Detour 028 Taj Mahal Montage Draft 20261101` (`25A8FF9A`).
- Timeline: `028 Rough Cut EN v01` (`5F604C92`), 1080×1920, 30 fps, 1066 frames.
- Before-edit snapshot: `DC304F26` (`028 before motion and EN cues`).
- Completed edit snapshot: `520475F5` (`028 EN Motion and Text v01`).
- Motion prescription: `.agents/consultations/20261101-paper-taj-mahal-camera-motion-prescription.md` (ChatGPT composer visibly showed `Extra High`).
- Cue review: `.agents/consultations/20261101-paper-taj-mahal-cue-table-review.md` (ChatGPT composer visibly showed `Extra High`).
- Cue schedule: `CUE_SHEET_EN_v03.md`; production assets: `../Source/Images/Text_Cues_EN_v03/production/`.

## Structural checks

- Main still track remains contiguous, direct-cut, and unchanged in timing: eight scene clips cover `[0,1066)`.
- Whole-frame keyframes are on all eight complete still-diorama clips. Scale endpoints stay between 1.020 and 1.044; adjacent shot endpoints match, and S11 settles at the exact S01 opening pose (1.020 at center).
- All seven English cue PNGs are on the new V2 overlay track above V1. Timeline clip intervals are exactly those in the cue sheet; cue clips do not alter the Dialogue track.
- All cue PNGs are the v03 normalized preflight renders and preserve alpha. The cue layer size/position maps the inspected 941×1672 placement to the 1080×1920 timeline canvas.
- C01–C10 use four-frame fade-ins, a hold, and five-frame fade-outs. C11 enters over four frames and holds through frame 1065 with no exit, clearing on the S11→S01 cut.

## Visual inspection

Palmier `inspect_timeline` rendered 54 distinct frames across every shot’s movement, every cue’s entrance/hold/exit, and the S01→S02 and S07→S10 cue crossings. The generated inspection frames are 288×512 and include the diagnostic coordinate grid; they were collated in:

- `QA_Motion_Text_v01/motion_cues_review_01.jpg`
- `QA_Motion_Text_v01/motion_cues_review_02.jpg`

The samples show the complete dioramas remain filled during the zooms, captions stay in their assigned top zones, text remains above the scene layer, and the two cue/cut crossings remain legible. The static v03 pair preflight was separately inspected full-size and at phone-preview size; see `TEXT_CUE_PREFLIGHT_EN_v03.md` and the helper contact sheets.

## Limits

This is a timeline edit and visual sample review. No narration was generated or changed, and no music or effects were added. No continuous playback, subjective audio listening, MP4 export, full-resolution playback QA, or publication was performed. Story facts remain unverified, as in the earlier rough cut.
