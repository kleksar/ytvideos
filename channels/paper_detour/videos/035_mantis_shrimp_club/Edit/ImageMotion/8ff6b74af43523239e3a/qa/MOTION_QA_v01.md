# Motion and cue sample QA — Paper Detour Short 035

**Run:** `8ff6b74af43523239e3a`  
**Source still timeline:** `D4A45BE0` — `Timeline 1 — Paper Detour 035 visual rework v03`  
**Motion target:** `2436013F` — `Timeline 1 — Paper Detour 035 visual rework v03 — image motion`  
**Snapshot:** `B4AF2610` — `Batch image motion verified`  
**Preset:** `framing-safe`; **grain:** `none`; canvas `1080×1920`, `30 fps`, `1325` frames.  
**Structural check:** `PASS` in `run.json`.

All ten cached motion clips were also checked with `ffprobe`: one 1080×1920, 30 fps video stream, no audio stream, and exactly `N+2` stored frames for a timeline length of `N` (the helper trims the two safety frames in Palmier). All ten checks passed.

## Scene movement and framing

Rendered camera/depth-cache clips were inspected at five local frames per scene (start, quarter, midpoint, three-quarter and final visible frame). The exact frame list is `motion_samples_v01/samples.json`; the five-point strips are `S01_motion_5point.jpg` through `S10_motion_5point.jpg`.

| Scene | Frames | Camera path | Key movement | Visual sample result |
|---|---:|---|---|---|
| S01 | `[0,122)` | push-in | scale `1.0595 → 1.0805`, center fixed | Both complete animals, spear, club and center gap remain visible. |
| S02A | `[122,242)` | pull-out | scale `1.0805 → 1.0595`, center fixed | Full animal, antennae, tail and repeated limbs remain visible. |
| S02B | `[242,362)` | pull-out | scale `1.0805 → 1.0595`, center fixed | Full animal and limb tips remain visible. |
| S03 | `[362,482)` | pan-right | scale `1.1`; visible center X `.4895 → .5105` | Whole animal and silhouette remain inside frame. |
| S04 | `[482,612)` | push-in | scale `1.0595 → 1.0805`, center fixed | Both complete animals and weapon tips remain separated and visible. |
| S05 | `[612,782)` | pan-right | scale `1.1`; visible center X `.4895 → .5105` | Full spearer, attached spear limb and terminal tip remain visible. |
| S06 | `[782,962)` | pan-left | scale `1.1`; visible center X `.5105 → .4895` | Full smasher, connected limb and complete club remain visible. |
| S07 | `[962,1082)` | pan-left | scale `1.1`; visible center X `.5105 → .4895` | Complete early form, antennae, tail and repeated limbs remain visible. |
| S08 | `[1082,1202)` | pan-right | scale `1.1`; visible center X `.4895 → .5105` | Both complete forms, spear, club and separation remain in frame. |
| S09 | `[1202,1325)` | push-in | scale `1.0595 → 1.0805`, center fixed | Both forms and weapon tips remain visible for the return to S01. |

No tested sample showed a clipped protected animal or weapon tip, exposed canvas, or distortion. This is five-point sampling, not frame-by-frame playback review.

## Accent cue composites

Nine cue states per phrase were recomposited over the exact rendered motion-cache frames, using the existing imported cue PNG, source-image canvas coordinates, and target keyframes: preceding frame, entry start, entry midpoint, full-opacity entry, hold midpoint, fade start, fade midpoint, final visible frame, and next-frame boundary. Contact sheets are `cue_composites_v01/C03_contact_v01.jpg`, `C01_contact_v01.jpg`, `C04_contact_v01.jpg`, `C02_contact_v01.jpg`, and `C05_contact_v01.jpg`. Each sampled source frame is preserved beside its corresponding composite.

| Cue | Global frames | Scene | Sampled global frames |
|---|---:|---|---|
| C03 | `[0,101)` | S01 | `1324, 0, 2, 4, 50, 96, 98, 100, 101` |
| C01 | `[398,468)` | S03 | `397, 398, 400, 402, 433, 463, 465, 467, 468` |
| C04 | `[482,610)` | S04 | `481, 482, 484, 486, 546, 605, 607, 609, 610` |
| C02 | `[797,962)` | S06/S07 cut | `796, 797, 799, 801, 879, 957, 959, 961, 962` |
| C05 | `[965,1082)` | S07/S08 cut | `964, 965, 967, 969, 1023, 1077, 1079, 1081, 1082` |

At full opacity, all five phrases remain legible and separated from the animals and their striking limbs. Cue entry and exit samples stay within the canvas; adjacent boundary samples show the cue absent on the neighboring frame. C04 on the still source timeline has opacity/position keys at local frames `0, 4, 123, 127`, with its exit inside `[482,610)`.

## Scope and remaining checks

The helper reports timeline structure `PASS`; it created a separate target and retained the voice/cue tracks. No audio was changed and no grain was applied. Full playback, spoken-word synchronization/listening, the 0.08-second alignment tail, loop playback, Shorts UI-safe zones and final-export QA remain `UNVERIFIED`. No export was made.

Cue sheets use an offline recomposite of actual motion-cache frames and exact timeline cue PNG/keyframe inputs; they are not screenshots captured from Palmier. Camera/depth samples are real rendered-cache frames, not the earlier camera-only motion envelope mock.
