# Short02 targeted motion/framing QA — 2 November 2026

**Candidate:** `PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v03.mp4`  
**SHA-256:** `bd5d071beb1465db056f6c2746da778b74602814675d3f04b2de425ec4685d6f`  
**Verdict:** motion/framing targeted PASS; overall QA UNVERIFIED.

## Coverage

Extracted and viewed 35 full-resolution frames from the exact candidate, five in each scene: starts, 25%, 50%, 75%, and last visible frame. The 35 IDs are in `sampling.json`; seven contact sheets are saved in the run preview folder. The 35 samples supplement the earlier 403-frame composition/caption review. This pass was targeted, not frame-by-frame.

## Motion match to final MP4

Patch matching used 240×240 grayscale texture windows at 25 fixed grid positions per sampled pair, Hann-windowed FFT phase correlation, subpixel peak interpolation, and a confidence cutoff. Accepted matches (typically 8–22 per pair; 5 at the very end of S07) show coherent progression across the quarter points. Scene-level measurements and confidence counts are in `patch_matching.json`.

| Scene | Visible result from first to last sampled frame |
|---|---|
| S01 | visible texture displacement at last sample (+60, +0) px from scene start |
| S02 | visible texture displacement at last sample (-56, +0) px from scene start |
| S03 | zoom-in: estimated final affine scale 1.0500x / 1.0416y; interpolated center drift approximately (-26, -0) px |
| S04 | visible texture displacement at last sample (+75, -0) px from scene start |
| S05 | visible texture displacement at last sample (-81, +0) px from scene start |
| S06 | zoom-in: estimated final affine scale 1.0483x / 1.0401y; interpolated center drift approximately (25, -0) px |
| S07 | visible texture displacement at last sample (+80, +0) px from scene start |

The visible pan direction matches the seven linear finish receipts. S03 and S06 increase in estimated scale from start through end, consistent with their zoom-in receipts. The endpoints are the camera-path extrema; patch estimates across quarter points were monotonic, so no extra extrema frame was indicated. Matching is an estimate of image motion, not an exact camera solve.

## Visual findings

On all seven sheets, the scene image filled the canvas without blank borders or exposed corners. Key objects stayed within the intended compositions; no unintended crop, visible depth tear, double edge, face/hand warp, or motion reversal appeared at the checked positions. Screen-space subtitles remained inside the frame and separated from the higher accent text. The five-point review does not certify every intervening frame.

No audio work or listening was performed. Narration is unchanged. Spoken subtitle synchronization remains UNVERIFIED, so the overall QA verdict remains UNVERIFIED; this motion result does not authorize delivery promotion or publication.
