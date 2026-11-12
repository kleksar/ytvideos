# Plan 09 — Daylight pause, v04

**Status: NOT READY.** Static endpoints exist for review, but the MG alpha bounds touch both horizontal canvas edges. At the required `MG 0 → +8 px` move, the cropped left edge of the table moves into the frame and exposes a vertical BG gap; the right side also remains crop-sensitive. Do not import this set as a motion-safe three-plane shot.

## Composition and provenance

- Storyboard beat: “Before leaving, he promised to come back.” Joshua is fully in frame, slightly right of center, paused beside the chair and still looking toward the laptop. This is a pause, not a doorway exit.
- Generated source candidate: `06_daylight_v04_master_candidate_source_NOT_READY.png`. It is a full-scene visual reference for this new composition, not the final canonical composite.
- Canonical t0: `06_daylight_v04_master_layerfirst_NOT_READY.png`, assembled from the layers below. It is byte-identical to the t0 endpoint.
- Layer-first generation: BG clean room/window plate; MG Joshua, chair, laptop and continuous table/support in one group; FG near-left side table/plant. ImageGen generated the candidate and layer cutouts; static compositing and the bottom transparent-row correction to MG were done locally. No imported master was overwritten.
- Canvas: all usable layer files and endpoint stills are 941×1672. No text or UI was added.

## Layer order and endpoints

| Z order | File | Canvas / mode | Alpha bounds at alpha ≥128 | Position t0 → t4 |
|---|---|---|---|---|
| BG | `06_daylight_BG_v04_clean_room_window_NOT_READY.png` | 941×1672 RGB, opaque | — | `0 → +4 px` |
| MG | `06_daylight_MG_v04_Joshua_chair_laptop_table_NOT_READY.png` | 941×1672 RGBA | `(0, 95)–(940, 1613)` inclusive | `0 → +8 px` |
| FG | `06_daylight_FG_v04_left_furniture_plant_NOT_READY.png` | 941×1672 RGBA | `(0, 984)–(279, 1671)` inclusive | `−11 → 0 px` |

The endpoint files are `06_daylight_t0_BG0_MG0_FG-11_v04_NOT_READY.png` and `06_daylight_t4_BG+4_MG8_FG0_v04_NOT_READY.png` (both 941×1672 RGB). BG+4 uses a mirrored 4-pixel edge continuation. The requested layer deltas are present in the still construction: BG +4, MG +8, FG +11. These are static endpoint images only; playback, motion quality and timing have not been verified.

## Visual/technical checks

- **Contact grouping:** Joshua, both hands, laptop, chair and the tabletop/support travel together in MG. In the stills, the left hand rests beside the laptop on the tabletop; the right hand holds the chair back; shoes remain on the rug. No detached prop is visible. The grouped supports protect internal hand/laptop/table/chair contacts, but the whole group shifts relative to the BG floor by 4 px over the endpoint.
- **Face and hands:** face reads as downcast and directed toward the laptop. The left hand is visible on the table; the right hand is visible on the chair. Fine finger count is not confidently verifiable at this frame size. No jewelry is prominent enough to verify.
- **Alpha/edge:** MG and FG were viewed over cyan and light QA backgrounds. MG has a visible warm/orange fringe and opaque alpha reaches both x=0 and x=940; these are unresolved defects. FG also reaches x=0 and y=1671; its `−11 → 0` move keeps its cropped left/bottom edge at or beyond the frame but is not a substitute for independent edge review.
- **Endpoint inspection:** t0 and t4 are both 941×1672. At t4, the MG shift exposes a straight vertical BG strip at the left edge of the previously cropped table, so the contact/edge test fails. No independent review has been recorded; the set remains NOT READY regardless.
- The raw MG from ImageGen was 941×1671 and is retained only as a diagnostic (`..._raw.png`). The import-shaped MG above is 941×1672 after adding one transparent bottom row without changing existing pixel coordinates.

## Files and SHA-256

| File | SHA-256 |
|---|---|
| `06_daylight_BG_v04_clean_room_window_NOT_READY.png` | `105163d75ab3c04d0981114441ae45792bb8e7cccad5c92fb2973f60349bf237` |
| `06_daylight_MG_v04_Joshua_chair_laptop_table_NOT_READY.png` | `f4c6232c8d8f37b7ca0a89b98c0dc7f38c6906c7ef9da1976040bb5e87ab8b5c` |
| `06_daylight_FG_v04_left_furniture_plant_NOT_READY.png` | `e214afa86352f0b3b6385ebc0f7d959aeacec7cdfe6382c24e21874f91771c75` |
| `06_daylight_v04_master_candidate_source_NOT_READY.png` | `affd2eaaf92c5458bbe5346c6ffe3fd829dda4b4acc4fe6240b4c06fd8bd46e8` |
| `06_daylight_v04_master_layerfirst_NOT_READY.png` | `a2aa9ed56e61efee8c7f73e9dd71f2b00a24ff872e90f3f4a2e9223348406a49` |
| `06_daylight_t0_BG0_MG0_FG-11_v04_NOT_READY.png` | `a2aa9ed56e61efee8c7f73e9dd71f2b00a24ff872e90f3f4a2e9223348406a49` |
| `06_daylight_t4_BG+4_MG8_FG0_v04_NOT_READY.png` | `64dea47eb7a778e8701b91c7531b81f7fdbb369b67c9a101d5638681f5f73b3b` |

QA composites over cyan/light backgrounds and the raw MG are retained in this folder with `_QA` / `_raw` filenames; they are diagnostic files, not import layers.
