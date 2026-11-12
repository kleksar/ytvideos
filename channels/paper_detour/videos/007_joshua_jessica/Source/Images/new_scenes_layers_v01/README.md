# 007 Joshua/Jessica — new scene image sets (v01)

## Status

**Active storyboard import mapping:** use [`../QUICK_IMPORT_CURRENT/`](../QUICK_IMPORT_CURRENT/README.md). It contains 12 unique approved BG/MG/FG triples covering all plan appearances. Plan 06 reuses the independently approved 05B v04 profile set; Plan 07 returns to hook v05; Plan 14 matches the hook start. The dedicated all-night v02/v03 variants described below remain archived and excluded after edge review.

**Candidate review status:** 01B v04, 05B v04, 06B v04, 07A v06 and 08 v03 have independent PASS for static registration and their tested t0/t4 stills; continuous animation remains unverified. 01_hook_loop v05 independently PASSED static registration, the t0 and motion endpoint stills, and exact loop-match identity; continuous motion remains unverified. v04 is excluded because its shifted mug nearly touched the frame; v05 moves it inward while keeping net +4/+8/+11 drift. The five-finger count is still unclear. 03_jessica_name v04 independently PASSED static/t0/t4 still review: the frame/easel and book/pencil contacts hold, strong content stays inside, and the warm contour reads as lamp-side rim light; continuous motion remains unverified. Paired night plans 04/05 v02 independently PASSED static/t0/t4 still review; continuous motion remains unverified. 05C v11 is **NOT READY** after independent review: at t4 its MG moves the right shoulder crop from source x=935 to x=943, crossing the 941 px canvas and visibly slicing more sweater; the folded hand's five-finger count is also uncertain. v12 is **NOT READY** after review: endpoint recomposition and layer contacts pass, and the suspected support boundary near y≈1305 matches the natural table front edge in the real scene. The blocker is composition: its side-profile/chin-rest pose and busy shelf/lamp/vine/book do not match the approved 08 beat (front 3/4, both shoulders, hands below face, simple wall and soft foreground edge). The dedicated Plan06 all-night candidate remains **NOT READY**: independent review found an 8px BG/MG table strip at x≈0–7 in t4; bounded BG v03 retained corrupted red/green/dark fragments at that edge; reverse registration exposed a new orange stripe on the opposite edge at t0; and the final t0 BG0/MG−4/FG0 → t4 BG+4/MG+4/FG+11 test still has a distinct vertical tonal BG/MG strip at the far-left wall/table edge in t4. That final pair’s t0 laptop/hand/table and book contacts look connected, but the registration fails visual edge QA. No further repairs are planned for this archived candidate. Active storyboard Plan06 uses approved 05B v04; Plan07 returns to hook v05. 08 tears v13 has about 50–60px side margins vs. ≥70; v14 fails the left ≥40px t0 bound; v15 moved the subject right, but the right shoulder reaches x≈935–940 and crosses the x=893 safety line. Those master-only variants remain **NOT READY**. A separate v13-derived layer-first set independently PASSED exact t0/t4 still review, face/tear, BG, shoulder visibility and FG corner treatment under the adjusted ≥20 px right-margin criterion; t4 right-shoulder clearance is 27 px. Continuous motion is unverified. The folder's 07A v01 master is the wrong blank quote-card image and is excluded; the accepted 07A set derives from the actual resource-meter reference. Keep candidates out of production until their manifest row says PASS.

Canvas target: 941×1672 px. Layer order when evaluating: **BG → MG → FG**.

## Per-scene manifest

| Scene | Master | Layers | Actual check | Status |
|---|---|---|---|---|
| 01_hook_loop | `masters/01_hook_loop_master_v05_layered.png` | `layers/01_hook_loop_BG_v05.png`, `_MG_v05.png`, `_FG_v05.png` | 941×1672; BG RGB opaque; MG/FG RGBA. Canonical master equals BG0 + MG−20 + FG−25 composite. Exact loop-match still duplicates t0 byte-for-byte. Motion diagnostic: BG+4, MG−12, FG−14 (net +4/+8/+11). MG left crop stays off-canvas; mug is inset farther from the right frame edge. Independent v05 review passed recomposition, loop identity, edge margin and visible contacts; hand finger count remains unclear. | **PASS — continuous motion unverified; hand digits unclear** |
| 03_jessica_name | `masters/03_jessica_name_master_v04_layered.png` | `layers/03_jessica_name_BG_v04.png`, `_MG_v04.png`, `_FG_v04.png` | 941×1672; BG RGB opaque; MG/FG RGBA. Canonical master is BG0 + MG−8 + FG0; t4 is BG+4/MG0/FG+11 (net +4/+8/+11). BG left edge uses mirrored 4px preview fill at t4. Frame/easel/support patch in MG; contained book+pencil and shadow in FG. Independent reviewer passed t0/t4 recomposition, safe extents, matte read, and frame/book contacts; continuous motion unverified. | **PASS — continuous motion unverified** |
| 04_old_messages | `paired_night_04_05_v01/masters/04_old_messages_master_v02_layered.png` | `paired_night_04_05_v01/layers/04_old_messages_BG_v02.png`, `_MG_v02.png`, `_FG_v02.png` | 941×1672; BG RGB opaque, MG/FG RGBA. Canonical layer composite; t0 BG0/MG−8/FG−20 and t4 BG+4/MG0/FG−9 (net +4/+8/+11). Three blank physical message cards; no text/UI. Independent review passed t0/t4 recomposition, physical-card read, mirrored BG fill and contacts; continuous motion unverified. | **PASS — continuous motion unverified** |
| 05_reply_card | `paired_night_04_05_v01/masters/05_reply_card_master_v02_layered.png` | `paired_night_04_05_v01/layers/05_reply_card_BG_v02.png`, `_MG_v02.png`, `_FG_v02.png` | 941×1672; BG RGB opaque, MG/FG RGBA. Canonical layer composite; t0 BG0/MG−11/FG0 and t4 BG+4/MG−3/FG+11 (net +4/+8/+11). One blank physical card on the screen plane; no UI/text. Card FG registered from an ImageGen cutout by recorded crop/resize/paste. Independent review passed t0/t4 recomposition, screen-perspective/contact read and no-UI treatment; continuous motion unverified. | **PASS — continuous motion unverified** |
| 01B_absence | `masters/01B_absence_master_v04_layered.png` | `layers/01B_absence_BG_v04.png`, `_MG_v04.png`, `_FG_v04.png` | All 941×1672; BG RGB opaque, MG/FG RGBA. Canonical master equals t0 composite. Tested t4 positions BG+4/MG+8/FG+11 with mirrored 4 px BG left bleed. Independent review passed static registration, t0/t4 endpoints and contacts; continuous motion unverified. | **PASS — continuous motion unverified** |
| 05B_not_really_jessica | `masters/05B_not_really_jessica_master_v04_layered.png` | `layers/05B_not_really_jessica_BG_v04.png`, `_MG_v04.png`, `_FG_v04.png` | All 941×1672; BG RGB opaque, MG/FG RGBA. Canonical master equals t0 composite with FG−11; tested t4 positions BG+4/MG+8/FG0 with mirrored 4 px BG left bleed. Independent review passed static registration, both endpoints and visible contacts; continuous motion unverified. | **PASS — continuous motion unverified** |
| 05C_tears | `masters/05C_tears_master_v12_layered.png` | `layers/05C_tears_BG_v12.png`, `_MG_v12.png`, `_FG_v12_registered.png` | All 941×1672; BG opaque, MG/FG RGBA. Selected registered FG already includes +40 px vertical registration; use at y=0, do not add +40 again. t0: BG x0/MG x+3/FG x0. t4: BG x+4/MG x+11/FG x+11; all y0. t0 byte-identical to master; t4 recomposes exactly. `FG_v12.png` is a 940×1672 raw diagnostic, not selected; it would require y=+40. Independent review passed endpoint recomposition, layer contacts and the support boundary's match to the natural table edge; composition does not match the approved plan 08 framing. | **NOT READY — composition mismatch** |
| Dedicated 06_all_night candidate (archived) | `plan06_all_night_v01/masters/06_all_night_master_v02_layered.png` | `plan06_all_night_v01/layers/06_all_night_BG_v02_table.png`, `.../06_all_night_MG_v01.png`, `.../06_all_night_FG_v01.png` | 941×1672; BG RGB opaque, MG/FG RGBA. Initial t0 0/0/0→t4 BG+4/MG+8/FG+11 recomposes exactly; independent reviewer found t4 left x≈0–7 corrupted after BG v03 patch. Reverse test: t0 BG−4/MG−8/FG−11, t4 0/0/0; t0 showed an orange far-right mirrored-BG strip. Final registration-only preview pair uses t0 BG0/MG−4/FG0→t4 BG+4/MG+4/FG+11, Y=0; both previews recompose exactly from these placements (mirrored 4 px BG fill at t4). Full-frame and enlarged QA found a distinct far-left vertical tonal strip at the wall/table BG/MG boundary in t4; t0 hand/laptop/table and book contacts remain connected, with the left sweater advanced 4px into the existing frame crop. Exact filenames and QA record are in the scene README. | **NOT READY — t4 edge artifact; no further attempts on this candidate** |
| 08_tears_v13 | `plan08_tears_v13_v01/masters/08_tears_master_v13_composition.png` | No layers generated | 941×1672 RGB. Front 3/4, one tear, hands outside the frame, clean wall and small soft FG lip. Guide preview marks x=70/871; the sweater crosses both guides and leaves only ~50–60px side margin. | **NOT READY — shoulder margins below 70px; no layers** |
| 08_tears_v14 | `plan08_tears_v14_v01/masters/08_tears_master_v14_composition.png` | No layers generated | 941×1672 RGB. Single bounded edit after v13. Guide preview marks x=40/893; the right shoulder has room for +8, but left shoulder reaches x≈18–25 at y≈1200–1300 and fails the t0 ≥40px margin. No layer extraction/review. | **NOT READY — left shoulder below 40px; no layers** |
| 08_tears_v15 | `plan08_tears_v15_v01/masters/08_tears_master_v15_composition.png` | No layers generated | 941×1672 RGB. Guide preview marks x=40/893. Left shoulder now passes x=40, but right shoulder reaches x≈935–940 at y≈1200–1300, crossing x=893 and leaving no safe room for MG+8. Master-only; no layer extraction/review. | **NOT READY — right shoulder crops at t4; no layers** |
| 08_tears_v13_layers | `plan08_tears_v13_layers_v01/masters/08_tears_master_v01_layered.png` | `plan08_tears_v13_layers_v01/layers/08_tears_BG_v01.png`, `_MG_v01.png`, `_FG_v01.png` | 941×1672; t0 BG0/MG−20/FG0; t4 BG+4/MG−12/FG+11, Y=0. Master=t0 byte-equal; both endpoints recompose exactly. Independent still review passed shoulders inside frame, t4 right clearance 27 px, face/tear, BG matte and FG corner treatment under the adjusted ≥20 px endpoint criterion. Continuous motion unverified. | **PASS — static t0/t4 only** |
| 06B_waiting_quote | `masters/06B_waiting_quote_master_v04_layered.png` | `layers/06B_waiting_quote_BG_v04.png`, `_MG_v04.png`, `_FG_v04.png` | All 941×1672; BG opaque, MG/FG RGBA. MG v04 adds a transparent bottom row to correct v03's 941×1671 canvas. Master is byte-identical to the t0 composite. Independent review passed static registration and t0/t4 still endpoints. | **PASS — continuous motion unverified** |
| 07A_resource_used | `masters/07A_resource_used_master_v06_layered.png` | `layers/07A_resource_used_BG_v06.png`, `_MG_v06.png`, `_FG_v06.png` | All 941×1672; BG opaque, MG/FG RGBA. Four isolated alpha=1 pixels on the far-left border were cleared in the copied MG/FG cutouts. Master is byte-identical to the t0 composite. Independent review passed static/t0/t4, no visible ghosts/gaps, and tested contacts. | **PASS — continuous motion unverified** |
| 08_saved_conversations | `masters/08_saved_conversations_master_v03_layered.png` | `layers/08_saved_conversations_BG_v03.png`, `_MG_v03.png`, `_FG_v03.png` | All 941×1672; BG RGB opaque, MG/FG RGBA. Canonical master equals t0 composite with FG−11; tested t4 positions BG+4/MG+8/FG0 with mirrored 4 px BG left bleed. Independent review passed registration, static/t0/t4 stills and contacts; continuous motion unverified. | **PASS — continuous motion unverified** |

## Provenance

Masters were generated with ImageGen as new compositions/edits using the inspected release masters as visual/continuity references:

- 01B_absence ← `Source/Images/02_photo_master_v03.png`
- 03_jessica_name ← `Source/Images/02_photo_master_v03.png`
- 05B_not_really_jessica ← `Source/Images/05_joshua_profile_master_v03.png`
- 05C_tears ← `05B_not_really_jessica_master_v01.png`
- 06B_waiting_quote ← `Source/Images/06_daylight_master_v2.png`
- 07A_resource_used ← correct source `Source/Images/07_resource_meter_master_v01.png`; the owned `07A_resource_used_master_v01.png` was later found to be an incorrect blank-card composition and is excluded.
- 08_saved_conversations ← `Source/Images/03_message_laptop_master_v03.png`

The BG/MG/FG diagnostics for 01B and 08 were produced with ImageGen edits from their new masters. Composite previews were assembled for visual QA with ImageMagick; they are diagnostics, not delivery frames. ImageGen output files were copied without resizing. Dimensions and alpha presence were checked with `sips`/`file`; dimensions/transparency alone were not treated as proof of readiness.

## Limits of this handoff

- 01B v01–v03, 05B v01–v03, 08 v01/v02, and 01_hook_loop v01–v03 files are diagnostic only. 01B v04, 05B v04, 06B v04, 07A v06, and 08 v03 have independent PASS for their static/t0/t4 still checks. 01_hook_loop v04 is an excluded diagnostic; v05 has independent PASS for static/t0/t4 stills and loop identity, with continuous motion unverified. 03_jessica_name v01–v03 are diagnostics; v04 has independent PASS for static/t0/t4 stills, with continuous motion unverified. 05C v04, v08, and v11 are NOT READY diagnostics.
- No maximum-parallax motion was rendered. The tested endpoint images are stills and do not prove edge/contact continuity through animation.
- No voice, video, edit timeline, or Palmier project was created or changed.

## 08 layer-first v02 diagnostic trial (NOT READY)

Per parent direction, the static BG→MG→FG diagnostic composite was promoted only as a **new canonical v02 layered master**. The original `08_saved_conversations_master_v01.png` remains untouched as a visual reference; the original v01 layers also remain untouched and are not relabeled ready.

- Canonical trial master: `masters/08_saved_conversations_master_v02_layered.png`
- Canonical trial layer files: `layers/08_saved_conversations_BG_v02.png`, `..._MG_v02.png`, `..._FG_v02.png`
- Endpoint still: `previews/08_saved_conversations_v02_max_shift_BGplus2_MGplus3_FGplus5.png`
- Exact preview offsets: BG +2 px horizontal, MG +3 px horizontal, FG +5 px horizontal. The BG preview uses a 2 px left-edge extension copied from its leftmost edge to avoid an exposed blank border. The preview is one still, not an animation.
- Actual equality check: the v02 master is byte-for-byte identical to `previews/08_saved_conversations_static_composite_check.png`; it therefore exactly equals the static composite of the v01 diagnostic layers. All v02 images are 941×1672. v02 MG/FG preserve alpha.
- Independent review found material redraw/registration differences and warm alpha fringes on this version. It is superseded by v03 below; retain v02 only as a diagnostic and do not import it.

Additional planned 4-second endpoint QA requested by parent:

- `previews/08_saved_conversations_v02_4s_BGplus4_MGplus8_FGplus11.png`
- Exact offsets: BG +4 px, MG +8 px, FG +11 px. The BG needed a 4 px left-edge extension made from its leftmost column; MG/FG needed no edge fill.
- Visual spot check: laptop, blank card stack, mug, pencil holder and nearest foreground book all remain visible at this endpoint; no contact point appears detached in this still. This is not a motion render and does not by itself establish approval.
- The independent reviewer was asked to include both endpoint previews in the pending review.

Alternative 4-second endpoint with mirrored BG bleed (created after a seam concern):

- `previews/08_saved_conversations_v02_4s_BGplus4_MGplus8_FGplus11_mirror_fill.png`
- Same +4/+8/+11 offsets; BG outer 4 px were filled by mirroring its first 4 columns, rather than repeating its first column. This remains a preview-only transform. Independent review was asked to identify whether the lower-left warm strip comes from BG edge fill, an expected frame-edge object contour, or a matte seam, and to compare both fill variants.

## 08 v03 overscan candidate — independent PASS for tested stills

This is the current import-map candidate for 08 only. Independent review passed static registration and both t0/t4 still endpoints. Continuous motion is unverified. All earlier v01/v02 files and previews are retained as diagnostics/reference and are excluded from import.

| Role | Exact file | Dimensions / alpha | t0 position |
|---|---|---|---|
| Master | `masters/08_saved_conversations_master_v03_layered.png` | 941×1672 RGB, opaque | Canonical v03 composition |
| BG | `layers/08_saved_conversations_BG_v03.png` | 941×1672 RGB, opaque | x=0 px |
| MG | `layers/08_saved_conversations_MG_v03.png` | 941×1672 RGBA | x=0 px |
| FG | `layers/08_saved_conversations_FG_v03.png` | 941×1672 RGBA | x=−11 px |

Compositing order is **BG → MG → FG**. FG v03 was ImageGen edited from FG v02 to move the cutout content +11 px within its full frame and add a plausible continuation of the blurred foreground book/plant into source x=0–10. BG/MG v03 are unchanged copies of v02. The t0 composite was saved at `previews/08_saved_conversations_v03_t0_BG0_MG0_FGminus11.png`; the master is byte-for-byte identical to that composite. It was visually checked against v02. `magick compare -metric MAE` between v02 and v03 masters returned 451.981 (normalized 0.00689679); this aggregate value records the redraw delta and is not a registration pass by itself.

Planned 4-second endpoint: `previews/08_saved_conversations_v03_t4_BGplus4_MGplus8_FG0.png`; positions are BG x=+4, MG x=+8, FG x=0. For the preview only, BG leftmost 4 px use a mirrored extension of the first 4 columns to avoid exposed blank canvas. Reviewer confirmed the former x≈11 line was the FG hard crop, not BG fill, and passed the fixed v03 still endpoints. No continuous motion render was reviewed.

### Excluded diagnostic files

Do not import 01B v01–v03, 05B v01–v03 or 08 v01/v02 as approved sets. 05C is in progress; 06B and 07A still need matching BG/MG/FG sets and review. No Palmier or video files were created or edited.

Independent review updates: **PASS** for 01B v04, 05B v04, and 08 v03 on static registration and the tested t0/t4 still endpoints. These passes do not establish continuous motion safety.

## Current import-map updates

### 01B_absence — v03 overscan draft (review failed)

| Role | Exact file | Dimensions / alpha | Placement |
|---|---|---|---|
| Master | `masters/01B_absence_master_v03_layered.png` | 941×1672 RGB opaque | t0 composite |
| BG | `layers/01B_absence_BG_v03.png` | 941×1672 RGB opaque | t0 0 px; t4 +4 px |
| MG | `layers/01B_absence_MG_v03.png` | 941×1672 RGBA | t0 0 px; t4 +8 px |
| FG | `layers/01B_absence_FG_v03.png` | 941×1672 RGBA | t0 −11 px; t4 0 px |

Order: BG → MG → FG. The t0 composite is `previews/01B_absence_v03_t0_BG0_MG0_FGminus11.png`; t4 still is `previews/01B_absence_v03_t4_BGplus4_MGplus8_FG0.png`, using mirrored 4 px BG left bleed. Parent's independent review failed v03: the right-edge cropped laptop/tablet contour enters the visible frame near x≈930 in t0. Preserve this set as a draft; a right-edge continuation or safer contained FG redesign is still needed before another review.

### 01B_absence — v04 contained-FG set (independent PASS for tested stills)

| Role | Exact file | Dimensions / alpha | Placement |
|---|---|---|---|
| Master | `masters/01B_absence_master_v04_layered.png` | 941×1672 RGB opaque | t0 composite |
| BG | `layers/01B_absence_BG_v04.png` | 941×1672 RGB opaque | t0 0 px; t4 +4 px |
| MG | `layers/01B_absence_MG_v04.png` | 941×1672 RGBA | t0 0 px; t4 +8 px |
| FG | `layers/01B_absence_FG_v04.png` | 941×1672 RGBA | t0 0 px; t4 +11 px |

Order: BG → MG → FG. BG retains the edge-cropped lamp/cup/laptop/near leaves; MG is the contained potted plant; FG is the contained couple photo frame/easel. t0 composite is `previews/01B_absence_v04_t0_BG0_MG0_FG0.png`; t4 is `previews/01B_absence_v04_t4_BGplus4_MGplus8_FGplus11.png` and uses mirrored 4 px BG left bleed. `sips` confirms canvas and alpha presence; parent reports independent PASS for t0/t4 stills and static registration. Continuous motion remains unverified. v01–v03 stay excluded.

### 05B_not_really_jessica — v04 overscan set (independent PASS for tested stills)

| Role | Exact file | Dimensions / alpha | Placement |
|---|---|---|---|
| Master | `masters/05B_not_really_jessica_master_v04_layered.png` | 941×1672 RGB opaque | t0 composite |
| BG | `layers/05B_not_really_jessica_BG_v04.png` | 941×1672 RGB opaque | t0 0 px; t4 +4 px |
| MG | `layers/05B_not_really_jessica_MG_v04.png` | 941×1672 RGBA | t0 0 px; t4 +8 px |
| FG | `layers/05B_not_really_jessica_FG_v04.png` | 941×1672 RGBA | t0 −11 px; t4 0 px |

Order: BG → MG → FG. FG contains the near tabletop plane, laptop, cup/coaster and plant so the desk occludes Joshua's lower torso as in the scene. The t0 composite is `previews/05B_not_really_jessica_v04_t0_BG0_MG0_FGminus11.png`; t4 still is `previews/05B_not_really_jessica_v04_t4_BGplus4_MGplus8_FG0.png`, with mirrored 4 px BG left bleed. Dimensions/alpha were checked with `sips`; the t0/t4 stills were visually inspected. Parent reports independent review PASS for static registration and both tested still endpoints. Continuous motion remains unverified.

Older 05B v02/v03 assets and previews remain diagnostic. 05C v02/v03, 06B v02/v03, 07A v01/v02/v03 and 07A v04/v05 layers are historical drafts/diagnostics and are excluded from import unless a later section explicitly identifies them as current. Current 05C/06B/07A details follow.

### 05C_tears — v12 inset composition candidate (NOT READY)

| Role | Exact file | Dimensions / alpha | t0 position | t4 position |
|---|---|---|---|---|
| Master | `masters/05C_tears_master_v12_layered.png` | 941×1672 RGB | Canonical v12 composite | — |
| BG | `layers/05C_tears_BG_v12.png` | 941×1672 RGB opaque | x=0, y=0 | x=+4, y=0 |
| MG | `layers/05C_tears_MG_v12.png` | 941×1672 RGBA | x=+3, y=0 | x=+11, y=0 |
| FG | `layers/05C_tears_FG_v12_registered.png` | 941×1672 RGBA | x=0, y=0 | x=+11, y=0 |

Order is **BG → MG → FG**. The selected `FG_v12_registered.png` already includes the cutout's +40 px vertical registration; use y=0 at both endpoints and do **not** apply +40 again. `layers/05C_tears_FG_v12.png` is the unregistered 940×1672 ImageGen source diagnostic and is excluded; if used for reconstruction it requires x=0/y=+40. The t0 master is byte-identical to `previews/05C_tears_v12_t0_BG0_MGplus3_FGregistered0.png`; t4 is `previews/05C_tears_v12_t4_BGplus4_MGplus11_FGregisteredPlus11.png` with mirrored 4 px BG left bleed. Both stills recompose exactly from these selected layers and listed placements; independent reviewer passed those static checks, contacts and the support boundary where it meets the natural table edge. The t0 keeps a restrained tear, hand-to-chin pose, side profile and prominent book/shelf/lamp/vine. Those choices do not match the approved plan 08: front 3/4 medium close-up, both shoulders in frame, hands below face, simple wall and soft foreground edge. Preserve v12 as a diagnostic only; do not import. Continuous motion remains unverified.

### 05C_tears — v11 contained-FG candidate (NOT READY)

| Role | Exact file | Dimensions / alpha | t0 position | t4 position |
|---|---|---|---|---|
| Master | `masters/05C_tears_master_v11_layered.png` | 941×1672 RGB | Canonical v11 composite | — |
| BG | `layers/05C_tears_BG_v11.png` | 941×1672 RGB opaque | 0 px | +4 px |
| MG | `layers/05C_tears_MG_v11.png` | 941×1672 RGBA | 0 px | +8 px |
| FG | `layers/05C_tears_FG_v11.png` | 941×1672 RGBA | 0 px | +11 px |

Order is **BG → MG → FG**. Source framing is `masters/05C_tears_master_v10.png`; this is the wider close-up with one restrained tear and a small contained notebook. MG carries Joshua, his chin-resting hand, the complete laptop and its immediate desk-support/contact patch together. FG is a separate closed notebook with its soft desk shadow. The t0 master is byte-identical to `previews/05C_tears_v11_t0_BG0_MG0_FG0.png`; t4 is `previews/05C_tears_v11_t4_BGplus4_MGplus8_FGplus11.png` with mirrored 4 px BG left bleed. All dimensions/alpha checked; MG alpha bounds are x=10…940, y=278…1648, and FG bounds x=132…432, y=1330…1465. At t4 the MG right shoulder crop moves from source x=935 to x=943, crossing the 941 px canvas and visibly slicing more sweater; this is the blocking defect. The notebook stays fully inside, and the hand/laptop and notebook/desk contacts hold in inspected stills. Independent review also found the folded hand's five-finger count uncertain. Continuous motion remains unverified. Preserve v11 as a diagnostic; do not import.

### 05C_tears — prior diagnostics (NOT READY)

| Role | Exact file | Dimensions / alpha | t0 position | t4 position |
|---|---|---|---|---|
| Master | `masters/05C_tears_master_v04_layered.png` | 941×1672 RGB | Canonical v04 composite | — |
| BG | `layers/05C_tears_BG_v04.png` | 941×1672 RGB opaque | 0 px | +4 px |
| MG | `layers/05C_tears_MG_v04.png` | 941×1672 RGBA | 0 px | +8 px |
| FG | `layers/05C_tears_FG_v04.png` | 941×1672 RGBA | 0 px | 0 px |

v04 preserved v03 pixels and added exactly two transparent rows to FG, but anchored FG at both endpoints; it does not meet fastest-plane movement. The next v08 attempt added a notebook but shifted the cropped MG left by 8 px; this created an internal right-edge cutoff near x≈932 and is excluded. v11 remains excluded because of its reviewed shoulder cut; v12 is the only current candidate and remains a draft until independent review. All v01–v10 remain drafts/diagnostics and are excluded.

### 06B_waiting_quote — v04 corrected canvas (PASS for tested stills)

| Role | Exact file | Dimensions / alpha | t0 position | t4 position |
|---|---|---|---|---|
| Master | `masters/06B_waiting_quote_master_v04_layered.png` | 941×1672 RGB | Canonical v04 composite | — |
| BG | `layers/06B_waiting_quote_BG_v04.png` | 941×1672 RGB opaque | 0 px | +4 px |
| MG | `layers/06B_waiting_quote_MG_v04.png` | 941×1672 RGBA | 0 px | +8 px |
| FG | `layers/06B_waiting_quote_FG_v04.png` | 941×1672 RGBA | −11 px | 0 px |

Order is **BG → MG → FG**. The t0 master is byte-identical to `previews/06B_waiting_quote_v04_t0_BG0_MG0_FGminus11.png`; the t4 still is `previews/06B_waiting_quote_v04_t4_BGplus4_MGplus8_FG0.png`. BG leftmost 4 px use mirrored edge fill at t4. v04 copies v03 BG/FG and pads one fully transparent bottom row on MG without changing any visible pixel coordinates. The composition keeps the blank quote card, laptop, cup/coaster and foreground notebook; no generated writing or interface. Independent reviewer passed static registration and tested t0/t4 stills. Continuous movement remains unverified.

### 07A_resource_used — v06 layer-first object insert (PASS for tested stills)

| Role | Exact file | Dimensions / alpha | t0 position | t4 position |
|---|---|---|---|---|
| Master | `masters/07A_resource_used_master_v06_layered.png` | 941×1672 RGB | Canonical v06 composite | — |
| BG | `layers/07A_resource_used_BG_v06.png` | 941×1672 RGB opaque | 0 px | +4 px |
| MG | `layers/07A_resource_used_MG_v06.png` | 941×1672 RGBA | 0 px | +8 px |
| FG | `layers/07A_resource_used_FG_v06.png` | 941×1672 RGBA | 0 px | +11 px |

Order is **BG → MG → FG**. Correct story reference is `Source/Images/07_resource_meter_master_v01.png`. The folder's v01 image was accidentally a blank quote-card composition; it is kept untouched as an excluded diagnostic. v03 is an ImageGen-edited object insert from the correct reference: blank-screen laptop, no person, and a separate unmarked physical cardstock strip filled teal for approximately 45%, fully inside frame. BG/MG/FG v06 were made with ImageGen from that master; BG retains the mug/coaster, pencil cup, and foreground books while clearing only the laptop and scale. The t0 composite is the new canonical master and is byte-identical to `previews/07A_resource_used_v06_t0_BG0_MG0_FG0.png`. The t4 still is `previews/07A_resource_used_v06_t4_BGplus4_MGplus8_FGplus11.png`; BG uses mirrored 4 px left bleed. Four isolated alpha=1 specks at x=0 were cleared from the MG/FG cutouts; the actual laptop/strip are inset by >150 px, so object edges were not touched. RGB MAE between the canonical v06 composite and the v03 input master is 20.63; this records ImageGen redraw differences and is not a registration pass. Independent review passed static registration, t0/t4 recomposition, the real-background edges and endpoint contacts with no visible ghost/edge gap. Continuous movement is unverified; no video was made.


## 01 hook/loop v05 candidate — PASS for tested stills

Source continuity reference: `Source/Images/01_room_laptop_master_v03.png`. ImageGen created the new master reference `masters/01_hook_loop_master_v03.png`; it remains untouched. The v05 layer set reuses ImageGen edits from that v03 reference: a clean night-room/desk BG, a transparent Joshua + chair + laptop MG, and a transparent mug/coaster FG. The canonical master is the actual v05 BG→MG→FG composite, not the earlier v03 reference, so it is a new canonical composition for both plan 01 and plan 14. v04 is retained as a diagnostic only.

| Role | Exact file | Canvas / alpha | Placement |
|---|---|---|---|
| Master | `masters/01_hook_loop_master_v05_layered.png` | 941×1672 RGB | Canonical composite |
| BG | `layers/01_hook_loop_BG_v05.png` | 941×1672 RGB opaque | t0 x=0; motion diagnostic t4 x=+4 |
| MG | `layers/01_hook_loop_MG_v05.png` | 941×1672 RGBA | t0 x=−20; motion diagnostic t4 x=−12 (net +8) |
| FG | `layers/01_hook_loop_FG_v05.png` | 941×1672 RGBA | t0 x=−25; motion diagnostic t4 x=−14 (net +11) |

Compositing order is BG→MG→FG. The t0 still is `previews/01_hook_loop_v05_t0_BG0_MGminus20_FGminus25.png`; the master is byte-identical to it. `previews/01_hook_loop_v05_t4_loopmatch_BG0_MGminus20_FGminus25.png` is an exact copy of the same canonical composite for the plan 14 loop return. Separate motion endpoint `previews/01_hook_loop_v05_t4_motion_BGplus4_MGminus12_FGminus14.png` uses a mirrored 4px BG left-edge extension for that preview only. MG’s strong-alpha left edge is at source x=0 and remains off-canvas at both tested placements. FG is placed −25 px at t0 and −14 px at the motion endpoint; the mug/coaster therefore shifts inward from v04 while keeping net +11 px movement. Reviewer found v04 had only ~4 px strong-alpha margin at the right endpoint; v05 now keeps a visibly larger inset and no overlap with the laptop in the inspected still. The t0 master and shifted still were visually inspected; the hand detail crop is `previews/01_hook_loop_v04_hand_detail.png`, and a cyan matte diagnostic from v04 is `previews/01_hook_loop_v04_matte_cyan.png`. Independent reviewer passed v05 static registration/recomposition, exact loop-frame identity, safe mug inset, laptop/desk and chair/floor contacts. Warm contours read as rim light in the actual room. Individual fingers remain visually unclear at this framing. No animation was rendered; motion safety is based on still endpoints only.

Older 01 hook layer attempts v01–v04 are preserved as excluded diagnostics. The first MG attempt v01 changed scale/registration and had a visible desk-support mismatch; the book-stack FG trial v01 enlarged/shifted the book into the laptop/hand area. v04 was rejected because mug edge safety failed at the planned +11 shift. They are not importable.


## 03 “Her name was Jessica” close-up v04 — PASS for tested stills

The new composition originates from `Source/Images/02_photo_master_v03.png`. ImageGen created a tighter shot in `masters/03_jessica_name_master_v02.png`: the same two faceless paper silhouettes are the story focal point; the notebook/pencil is moved fully onto the foreground tabletop. This is a distinct close insert from the source medium shot. The v04 layer set uses an ImageGen clean room/table plate, a frame/easel and base-contact group, and a book+pencil cutout with its contact shadow. The canonical master is the t0 layer composite, so it follows the actual registered layers rather than claiming pixel equality to the earlier v02 composition. The clean plate includes only the existing lamp, window, plant, mug/coaster and table; a generated background-chair detail was removed before creating v03/v04 layers.

| Role | Exact file | Canvas / alpha | Placement |
|---|---|---|---|
| Master | `masters/03_jessica_name_master_v04_layered.png` | 941×1672 RGB | Canonical composite |
| BG | `layers/03_jessica_name_BG_v04.png` | 941×1672 RGB opaque | t0 x=0; t4 +4 |
| MG | `layers/03_jessica_name_MG_v04.png` | 941×1672 RGBA | t0 −8; t4 0 (net +8) |
| FG | `layers/03_jessica_name_FG_v04.png` | 941×1672 RGBA | t0 0; t4 +11 |

Compositing order: BG→MG→FG. t0 preview `previews/03_jessica_name_v04_t0_BG0_MGminus8_FG0.png` is byte-identical to the master. t4 diagnostic is `previews/03_jessica_name_v04_t4_BGplus4_MG0_FGplus11.png`; BG’s first 4 columns are mirrored into the exposed left edge for this preview only. All layers are 941×1672; the MG strong-alpha bounds are x=121…925/y=434…1296 and the FG strong-alpha bounds are x=28…715/y=1219…1508. At t4 the frame’s rightmost strong-alpha x is 933 and the book’s rightmost strong-alpha x is 726; both stay within the frame. The book and pencil remain a separate complete foreground group, and its shadow stays under it. The MG contains the frame/easel and narrow support/contact patch. Actual t0/t4 composites and a cyan matte diagnostic `previews/03_jessica_name_v04_matte_cyan.png` were inspected; the cyan test exposes warm rim light around the frame/book cutouts. Independent review passed the real-background edge read, frame/easel table support, book contact shadow, safe endpoints and distinct keepsake-close-up read. No animation was rendered; endpoint stills do not prove continuous motion.
