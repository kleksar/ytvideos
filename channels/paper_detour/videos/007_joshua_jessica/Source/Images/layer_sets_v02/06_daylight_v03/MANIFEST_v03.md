# Plan 09 daylight — v03 fresh layer-first attempt

**Status: NOT READY. No importable set.** This is a fresh canonical candidate derived from `Source/Images/06_daylight_master_v2.png`; it is not a pixel-registered replacement or approved master. All previous v01/v02 drafts and the original v02 master remain untouched. Only still PNGs and QA stills were created; no video, audio or Palmier work was done.

## Layer stack and static endpoints

Composite order is **BG → MG → FG**. Every layer and endpoint is full-canvas 941×1672. BG is opaque RGB; MG and FG are RGBA with transparent surroundings.

| Plane | File | Strong alpha bounds (alpha ≥128) | Contents |
|---|---|---:|---|
| BG | `06_daylight_BG_v03_generated_clean_plate_NOT_READY.png` | opaque | Generated clean room/window and continuous wooden tabletop plate, cleared of Joshua, laptop and near plant. |
| MG | `06_daylight_MG_v03_Joshua_laptop_table_support_NOT_READY.png` | x=0…921, y=481…1466 | Joshua, hand, full laptop, contact shadow, and connected tabletop support directly beneath the laptop footprint. The figure is naturally cropped at the left edge. |
| FG | `06_daylight_FG_v03_contained_plant_source_NOT_READY.png` | x=713…940, y=1254…1560 before endpoint shift | Lower-right potted plant, pot and its table contact shadow. The endpoints move it left to keep a clear frame margin. |

| Still | BG position | MG position | FG position | File |
|---|---:|---:|---:|---|
| t0 | 0 px | −8 px | −45 px | `06_daylight_t0_BG0_MG-8_FG-45_v03_NOT_READY.png` |
| t4 static reference | +4 px | 0 px | −34 px | `06_daylight_t4_BG+4_MG0_FG-34_v03_NOT_READY.png` |

All three layers move right by +4/+8/+11 px between these still endpoints. BG+4 uses four-column edge extension at the newly exposed left edge. The canonical t0 master is [`06_daylight_master_v03_layerfirst_NOT_READY.png`](06_daylight_master_v03_layerfirst_NOT_READY.png), byte-identical to the t0 still.

## Visual QA and blockers

The reframed scene removes the oversized foreground chair. Joshua, his hand and the complete laptop read clearly in an intimate over-shoulder composition. The laptop remains visually supported by the table patch carried in MG at both static endpoints; no obvious detached duplicate is visible in these stills. The FG plant is contained after its leftward placement: its strong-alpha bounds are x=668…895 at t0 and x=679…906 at t4, leaving at least 35 px at the right edge.

The set is **NOT READY** because contrasting-matte inspection shows strong warm red/orange contours around Joshua's hair, shoulder, sweater and hand. The MG also touches the left frame edge due the intentional torso crop; the crop stays at the frame boundary at both endpoints, but has no extra horizontal safety margin. Although the laptop stays on its attached support patch, that patch is a local section over the continuous BG tabletop and moves 4 px relative to that surface; motion may read as a sliding table patch. Only t0/t4 stills were inspected, not animation playback. Do not promote this candidate or call the contact-safe motion verified.

Anatomy/text check: head is seen from behind, so facial details are not assessable. The hand is visible on the keyboard/trackpad; there are no obvious extra digits, but exact finger count is not conclusive at this angle. No jewelry or legible text/UI is present; the laptop screen is blank. Original source masters were not edited.

## Provenance

- Reframed canonical source candidate: `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-8acc3615-403b-40bf-8050-61649a47cbef.png` (ImageGen edit guided by the v02 daylight master).
- BG clean plate: `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-04c83779-94de-41ab-925a-092d18b66557.png`.
- MG extraction with tabletop support: `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-0dc82b69-615d-4875-a476-bd9510b88121.png`.
- FG plant extraction: `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-c78843c5-1f7c-4a8f-bc8d-488649d20c6d.png`.

## SHA-256

| File | SHA-256 |
|---|---|
| `06_daylight_layerfirst_master_candidate_source_NOT_READY.png` | `1055383e5694feae196b1fb681fbc85849b356630c7301500fb969f102da70c7` |
| `06_daylight_BG_v03_generated_clean_plate_NOT_READY.png` | `bbf8284f03748dfe96fecfa0cc2319e7566bed804b504a46869d9c962faa29cb` |
| `06_daylight_MG_v03_Joshua_laptop_table_support_NOT_READY.png` | `c729e65f01c8b54bbdac545521640a6151a010606d6525ecd74eabaa93f0c222` |
| `06_daylight_FG_v03_contained_plant_source_NOT_READY.png` | `39e5dd3cbffbf724b9bcff48c8e03feea22b3d461e50327a470c1474047bc26a` |
| `06_daylight_master_v03_layerfirst_NOT_READY.png` | `1dec90fb7d236bef53af6650d943fae76f999b1c2b0e1c4f34bfeaec0e7ea57c` |
| `06_daylight_t4_BG+4_MG0_FG-34_v03_NOT_READY.png` | `bf57a2e9d83f9ce7d027e0203b24d9ece40b7cbcb893e3c406126f87bd8e6ac1` |

## Independent review outcome

Independent static review confirms endpoint recomposition and the +4/+8/+11 px layer deltas, but keeps v03 **NOT READY**: the MG retains a left-frame crop, and the local MG tabletop support shifts 4 px relative to the BG tabletop. Warm red/orange matte contours remain. Playback was not reviewed. Do not promote this candidate.
