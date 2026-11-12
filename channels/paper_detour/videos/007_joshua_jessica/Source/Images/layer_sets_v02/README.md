# Layer-first canonical prototypes v02 — scene QA and status

This folder contains still-only layer candidates and QA records. **Static still-set PASS rows in this overview:** plan 04, plan 05, plan 12 v02, and plan 13. Continuous motion remains unverified for those sets. Plan 04/05 assets remain in the sibling `new_scenes_layers_v01` folder and are referenced here without copying or moving. Plans 06, 08, and 09 are NOT READY. Only still PNGs and diagnostics were made; no video or audio.

## Status across selected plans

| Storyboard plan / scene | Status | Concrete check / per-set evidence |
|---|---|---|
| 01 — `01_room_laptop_master_v03.png` diagnostic | **NOT READY — independent review failed** | Horizontal matte cutoff at y≈1637–1639 crosses floor/chair/desk; warm fringe remains on MG/FG. Full shot-01 record remains below. |
| 02 — `02_photo_master_v03.png` | **NOT READY — independent edge review failed** | FG shift −11 exposes a right-edge seam; containment leaves a rectangular tabletop matte. See `02_photo/` drafts and central [`MANIFEST.md`](MANIFEST.md). |
| 04 — old messages | **PASS — static/t0/t4 still review only** | Paired v02 set in `../new_scenes_layers_v01/paired_night_04_05_v01/`: blank physical cards; t0 BG0/MG−8/FG−20, t4 BG+4/MG0/FG−9. Independent review passed recomposition, card/contact read and edge fill. The local `03_message_laptop` v04 set remains a failed diagnostic. [Paired night set report](../new_scenes_layers_v01/paired_night_04_05_v01/README.md). |
| 05 — reply card | **PASS — static/t0/t4 still review only** | Paired v02 set in `../new_scenes_layers_v01/paired_night_04_05_v01/`: one blank physical card; t0 BG0/MG−11/FG0, t4 BG+4/MG−3/FG+11. Independent review passed card/screen perspective and contacts. The local `04_reply_card` v03 set remains a failed diagnostic. [Paired night set report](../new_scenes_layers_v01/paired_night_04_05_v01/README.md). |
| 06 — Joshua profile, “All night” | **NOT READY — independent review failed** | v03b leaves 4 px at MG's right edge; the oversized mug covers the laptop keyboard/base and lower torso. MG support shifts 4 px versus BG and the mug/coaster 7 px versus tabletop; warm matte remains and hand digits are uncountable. [Plan 06 v03 report](05_joshua_profile_v03/MANIFEST_v03.md). |
| 08 — tears (`05C_tears` v12; v11 superseded) | **NOT READY — independent review failed** | v12 t0/t4 layer recomposition is exact, but the side-profile/hand-to-chin/prominent-book composition conflicts with the approved front 3/4 shot plan. Warm rim is strong and an MG support boundary near y≈1305 is unresolved. v11 separately cuts the shoulder at t4. [Scene-set review record](../new_scenes_layers_v01/README.md). |
| 09 — daylight (`06_daylight` v04; v03 superseded) | **NOT READY — author endpoint check failed** | v04 groups Joshua, chair, laptop and table in MG, but its table crop touches both horizontal edges; MG+8 exposes a vertical BG strip on the left. Warm matte fringe remains. v03 also had a left crop and support drift. [Plan 09 v04 report](06_daylight_v04/MANIFEST_v04.md). |
| 12 — resource meter v02 | **PASS — static layer set and t0/t4 stills only** | Parent accepted v02 as the new canonical master; independent review passed recomposition, layer deltas, table contact and endpoint edge positions. Motion playback is unverified. A separate paper “55%” accent is needed to clarify remaining capacity. [Plan 12 manifest](07_resource_meter_v02/MANIFEST_v02.md). |
| 13 — saved conversations (`08_saved_conversations` v03) | **PASS — static/t0/t4 still review only** | Independent review passed registration, static endpoints and contacts; t0 BG0/MG0/FG−11, t4 BG+4/MG+8/FG0. Continuous motion is unverified. [Scene-set review record](../new_scenes_layers_v01/README.md). |

The parent-owned storyboard import map is not changed here. See [`MANIFEST.md`](MANIFEST.md) for referenced paths and offsets. Keep NOT READY candidates out of import; plan 04/05 references point to the paired v02 files in the sibling folder and do not duplicate those assets.

**Status: FAILED INDEPENDENT REVIEW / NOT READY / NOT APPROVED.** All shot-01 files remain drafts. The current set is a new layer-first composition guided by `Source/Images/01_room_laptop_master_v03.png`; it is not a pixel extraction or a claim that the new master matches the original. No original or imported asset was changed. The independent reviewer found a straight horizontal alpha cutoff through the scene and visible warm fringe.

## Current test set — candidate v05

Composite order: **BG → MG → FG**. Every plane and both still endpoints are 941×1672.

| Plane | File | Dimensions | Format / alpha | Contents |
|---|---|---:|---|---|
| BG | `01_opening/01_layerfirst_BG_v02.png` | 941×1672 | RGB, opaque | Night room, wall, window, bookcase and floor. The BG has no desk. |
| MG | `01_opening/01_layerfirst_MG_v14_from_v13_shiftminus8.png` | 941×1672 | RGBA, transparent exterior | Joshua, chair, sweater, laptop/keyboard/hand, desk, lamp, cup and books as one connected group. |
| FG | `01_opening/01_layerfirst_FG_v03.png` | 941×1672 | RGBA, transparent exterior | Small lower-left near plant. |

The proposed canonical t0 is `01_opening/01_layerfirst_static_canonical_v07.png`, byte-identical to `01_opening/01_layerfirst_t0_BG0_MGplus8_FGminus11_v05.png`.

| Still endpoint | BG position | MG position | FG position | Output |
|---|---:|---:|---:|---|
| t0 | 0 px | +8 px | −11 px | `01_opening/01_layerfirst_t0_BG0_MGplus8_FGminus11_v05.png` |
| t4 (4-second position reference) | +4 px | +16 px | 0 px | `01_opening/01_layerfirst_t4_BGplus4_MGplus16_FG0_v05.png` |

MG v14 is v13 shifted exactly 8 px left on the same transparent 941×1672 canvas using ImageMagick, without scaling or resampling. The positions compensate that source offset: t0 reproduces the v13 composition, and t4 moves the visible MG group a further +8 px. BG moves +4 px and uses the mirrored four-column left-edge fill in `01_opening/01_layerfirst_BGplus4_edgefill_v02.png`; FG moves +11 px from −11 to 0. All three planes move left-to-right. These are static endpoint stills only; no animation/video was rendered or reviewed.

## QA and unresolved issues

- **Canvas and registration: PASS for the current PNGs.** The three layers and both endpoint stills are 941×1672. BG is opaque; MG and FG contain alpha. The t0 endpoint and canonical master are byte-identical.
- **t0 equivalence: PASS with a minor low-alpha exception.** Compared with direct compositing of v13 at MG x=0, the new compensated t0 differs only in x=0…7, y=1095…1287: max 1 level in the red channel and zero in green/blue (mean absolute RGB difference `[0.000392, 0, 0]` on a 0–255 scale). This is the faint low-alpha edge clipped by the leftward source shift; the strong silhouette begins at x=11 in the compensated t0 and is intact.
- **Right edge: reviewer PASS for seam only.** The reviewer confirmed that the v14 strong-alpha boundary at t4 is 8 px beyond the frame, so no internal vertical matte seam appears. At t0 the strong silhouette reaches the right frame edge; the image frame still crops the lamp/cup there.
- **Left silhouette/contact: reviewer PASS.** The reviewer saw about 11 px of room at left, an open hand remaining on the keyboard, and intact cuff/laptop contacts. The v14 shift clips only low-alpha pixels at the extreme left; the t0 visual comparison shows no structural loss to Joshua, chair or desk.
- **Horizontal matte cutoff: FAIL.** The independent reviewer found a straight horizontal band at approximately y=1637–1639 in both stills. MG alpha spans almost the full width above the line, then drops to zero; the line crosses the floor, chair and desk and does not read as a natural room boundary. This is a blocking defect.
- **Alpha edges: FAIL.** Warm red/yellow fringe is plainly visible around hair, sweater, hand, lamp, cup, chair and desk on both gray and cyan diagnostics: `01_opening/01_layerfirst_MG_v14_t0_BFBFBF_NOT_SCENE_PREVIEW.png` and `01_opening/01_layerfirst_MG_v14_t0_00C8E8_NOT_SCENE_PREVIEW.png`. FG v03 also has a warm fringe. These are matte checks, not scene previews. This defect remains open even if the offset endpoints pass review.
- **Framing/anatomy/text: partial.** The latest close recompose keeps the head, upper back, keyboard and open hand prominent and does not reveal full legs/feet. The face is not visible from this rear angle. The hand reads open with separated digits; exact finger count is not conclusive at the diagnostic crop scale. No jewelry or legible text appears, and the laptop screen is blank. Lamp/cup remain near the right frame edge. The desk and lamp were kept with the MG to preserve object/support contacts rather than splitting them into the desk-free BG.
- **Independent review: FAIL — `/root/review_story_assets`, shot 01 v14/v05.** The reviewer checked the still endpoints only. Along with the horizontal cutoff and warm fringe, continuous motion remains unverified.
- **No video/audio.** Only still PNGs, contrast diagnostics, and static composites/endpoints were made. No MP4/MOV/MKV is present in this folder.

## Provenance and superseded attempts

- Visual guidance: `Source/Images/01_room_laptop_master_v03.png`. BG v02 and FG v03 come from the earlier layer-first set. MG v07 was reviewed as the closest intimate attempt, but its right edge was clipped when used at t0. The built-in ImageGen recompose v13 is saved at `01_opening/01_layerfirst_MG_v13_recompose_attempt_NOT_READY.png`; it kept the close framing but still touched the right frame edge. MG v14 is a deterministic translation of that v13 layer, not a new generation.
- v14 provenance: ImageMagick shifted v13 left exactly 8 px inside a transparent 941×1672 canvas. FFmpeg composited BG/MG/FG at the t0 and t4 integer offsets and produced still endpoints only. ImageMagick produced the contrast diagnostics. The t0 comparison was made against a temporary direct v13 composite; no original master or imported image was modified.
- Earlier complete candidate v04 (MG v11) had clear horizontal margins but widened the shot enough to show the full chair, feet and desk supports; it is superseded. MG v12 failed to produce right-side continuation and touched both frame edges. MG v13 still touched the right edge (`alpha > 127` bounds x=11…940), so it was not used directly as a production layer. Failed drafts remain in this folder with `NOT_READY` or `INVALID` in their filenames.
- The parent later authorized independent 02–07 work despite shot 01 remaining failed; consult [`MANIFEST.md`](MANIFEST.md) for current per-scene status. This does not change shot 01's failed review or approve its assets.

## SHA-256 — candidate v05

| File | SHA-256 |
|---|---|
| `01_opening/01_layerfirst_BG_v02.png` | `230af8d406f29146c03d3f82261b0f0c2a9f370bb6fe173dd8987638df6e8c4a` |
| `01_opening/01_layerfirst_MG_v14_from_v13_shiftminus8.png` | `0257dbd873df4128abb04658aebab44a544a9dab77c39361b002390f4c833e5a` |
| `01_opening/01_layerfirst_FG_v03.png` | `50d226c6a20c81df812aec185ea96a673d0a2f8938c117299e4b31913615c251` |
| `01_opening/01_layerfirst_BGplus4_edgefill_v02.png` | `6c94d38cd82904ff3b161076a2f12000ca8e1b04ae41568f8fa3e6dab61aa9b1` |
| `01_opening/01_layerfirst_static_canonical_v07.png` | `d51a381b2fd66b2462770bca443a462c96b784484ef7c210ad0fc84c5348f535` |
| `01_opening/01_layerfirst_t4_BGplus4_MGplus16_FG0_v05.png` | `535a473dde3bd76fe12db4b40136fa6e43472650108a3f36ebe453682a1f8daa` |

## SHA-256 — superseded failed MG attempts

| File | SHA-256 |
|---|---|
| `01_opening/01_layerfirst_MG_v11.png` | `26375995d7e827e245cdaa5fd1d2e240ba50d286f6e87b392776694273411541` |
| `01_opening/01_layerfirst_MG_v12_overscan_attempt_NOT_READY.png` | `7cc6f96366c2269731e350b857f98222f394532e83d58a1dc12e1a5d044d727e` |
| `01_opening/01_layerfirst_MG_v13_recompose_attempt_NOT_READY.png` | `7b17e56bcfa15caf6003e64e10f9986a44213d3c0dbb2f3d366461ae241aa8e1` |
