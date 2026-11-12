# Paper cue sheet v03 — Short 035

**Status:** existing five accepted phrase PNGs re-mapped to the new scene set and frame plan v02. Captions are static geometry during scene camera motion and do not receive scene parallax. Existing accepted voice and words are unchanged. Alignment remains automatic; heard sync/playback is still unverified.

| Cue | Text | Scene / frame interval | Timing source | Static composition check |
|---|---|---|---|---|
| C03 | `ONE LIMB.` / `TWO WEAPONS?` | S01 / `[0,101)` | Voice alignment, 30 fps quantization | Primary, face-height 76 px; full composite and phone reduction inspected. |
| C01 | `THE` / `EXCEPTION` | S03 / `[398,468)` | Voice alignment, 30 fps quantization | Primary, 76 px; full composite and phone reduction inspected. |
| C04 | `SEPARATE PATHS` | S04 / `[482,610)` | Voice alignment, 30 fps quantization | Primary, 76 px; full composite and phone reduction inspected. |
| C02 | `PIERCE` / `≠ STRIKE` | S06 / `[797,962)` | Voice alignment, 30 fps quantization | Existing alternate, 73 px; full composite and phone reduction inspected. |
| C05 | `A NEW ROLE` | S07 / `[965,1082)` | Voice alignment, 30 fps quantization | Primary, 76 px; full composite and phone reduction inspected. |

Exact PNG provenance and previous words/trigger-end notes remain in `CUE_SHEET_v02.md`, `CAPTION_DECISIONS_v02.md` and `Source/Graphics/render_v04/manifest.json`. New static scene/cue composites are in `Source/Graphics/render_v05/pairs.json` and `Source/Graphics/render_v05/pairs/`; every assigned pair was viewed full-frame individually and together at phone size. Their anchors, scale, and pixel positions were inherited from the accepted geometry: C03 `(182,109)`, C01 `(312,66)`, C04 `(165,143)`, C02 alternate `(459,142)`, C05 `(232,166)` on the 941×1672 scene canvas.

**Checks:** static geometry `PASS`; motion/intermediate extrema `UNVERIFIED`; sync/listening `UNVERIFIED`; final exported caption visibility `UNVERIFIED`. New scene imagery invalidates the previous motion composites. Re-check all five cue states over the actual camera/depth path and extracted export frames before calling them final.
