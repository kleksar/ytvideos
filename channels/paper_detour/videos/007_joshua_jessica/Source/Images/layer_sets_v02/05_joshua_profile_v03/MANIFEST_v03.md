# Plan 06 “All night” — v03 new-composition attempt

**Status: NOT READY. No importable set.** This is a layer-first new-composition candidate guided by `Source/Images/05_joshua_profile_master_v03.png`. The original profile master, prior v01/v02 drafts, and the separate single-tear beat are preserved untouched. This candidate contains no tear or crying; it is the pensive “All night” beat only. Files here are still PNGs/QA notes; no video, audio or Palmier work was done.

## Layers and endpoint stills

Z-order is **BG → MG → FG**. All files are full-canvas 941×1672 PNGs. BG is opaque RGB; MG and FG are RGBA with alpha 0–255. The t0 composite defines a candidate new master from these generated layers; it is not a pixel-registered copy of `05_joshua_profile_master_v03.png`.

| Plane | File | Strong alpha bounds (alpha ≥128) | Contents |
|---|---|---:|---|
| BG | `05_joshua_profile_BG_v03_clean_room_table_NOT_READY.png` | opaque | Night room, shelf/photo, lamp, window, distant plants, chair and continuous tabletop clean plate. |
| MG | `05_joshua_profile_MG_v03_Joshua_laptop_table_support_NOT_READY.png` | x=6…936, y=538…1269 | Joshua's profile, sweater/arms, chin-supporting hand, laptop and a broad connected tabletop support patch under the elbow/laptop. |
| FG | `05_joshua_profile_FG_v03_mug_saucer_NOT_READY.png` | x=79…587, y=961…1387 | Mug and saucer/contact shadow. The cutout is technically contained but was generated at a much larger scale than the mug in the candidate master. |

| Still | BG position | MG position | FG position | File |
|---|---:|---:|---:|---|
| t0 | 0 px | −8 px | 0 px | `05_joshua_profile_t0_BG0_MG-8_FG0_v03b_NOT_READY.png` |
| t4 static reference | +4 px | 0 px | +11 px | `05_joshua_profile_t4_BG+4_MG0_FG11_v03b_NOT_READY.png` |

The positive plane deltas are +4/+8/+11 px. BG+4 uses four-column left-edge extension. The candidate new t0 master, [`05_joshua_profile_master_v03b_layerfirst_NOT_READY.png`](05_joshua_profile_master_v03b_layerfirst_NOT_READY.png), is byte-identical to t0. Earlier v03 endpoint files with MG 0→+8 are preserved as diagnostics; v03b changes MG placement to −8→0 to avoid pushing the laptop/support cutout beyond the right edge.

## QA and blockers

- **Framing/margins: FAIL.** The reframe improves the medium profile, but the full MG strong-alpha bounds are x=6…936. At t4 only about 4 px remain at the right edge; at t0 the MG left edge is clipped by about 2 px. This misses the requested side margin for the whole Joshua+hand+laptop+support group.
- **FG composition/contact: FAIL.** The ImageGen mug cutout is about three times the source mug's apparent width/height. In t0/t4 it dominates the lower frame and overlaps Joshua's torso and the laptop keyboard/base, competing with the pensive face and breaking the intended foreground hierarchy. It is not an acceptable contained foreground object despite its alpha bounds staying inside the canvas.
- **MG matte: FAIL.** Cyan/light contrast previews show conspicuous warm orange fringe around hair, sweater, and hand.
- **Support:** MG includes a connected tabletop support patch under the laptop and elbow, and the laptop reads grounded in the stills. The patch is a local tabletop region moving +8 px against BG +4 px, so motion/playback contact remains unverified.
- **Anatomy/story:** Face and pensive chin-support pose are visible; no tear is added, preserving the tear scene as a separate beat. No obvious extra digits, but the curled hand does not allow a conclusive finger count at this resolution. No jewelry or readable text/UI appears; the laptop is closed from the viewer's side/has no visible UI.

These failures are sufficient to keep the candidate NOT READY. No further generation was attempted in this folder. The new scene remains provisional and should not be imported.

## Provenance and hashes

- Candidate reframe: `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-2871f40d-8c0c-4f26-8956-1495cde6da28.png`.
- BG clean plate: `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-8e766a3f-0513-4ab9-9374-237c0b5850ca.png`.
- MG extraction: `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-0c1a066b-a114-40ef-be67-5c0f98f3ab18.png`.
- FG mug extraction: `/Users/diplomat/.codex/generated_images/01a194dc-840f-74e0-9335-6fea5634e223/exec-d4b173e2-2895-4100-af56-18561fab2636.png`.

| File | SHA-256 |
|---|---|
| BG | `ba13468cd314fb64b0b18a5f7201061a4ce8c8677cc83519e85ebcf4f9e82c1e` |
| MG | `de1ff5dfd4eafae84365116a84caf8e11eea87ca5068e2121ff5d371616e08cc` |
| FG | `7e2f8b53de8ead378540553df9a1b8ff1b32398968f8f24ab8de3185713c893d` |
| t0 master/composite | `4391c074c22ddeb12e50f48976368a46f5597c51f3625c42db5d31de8b1e0b9d` |
| t4 still | `a263b7bb6ae6bd67c34986544566c4c3fe66fc32390376939897164d28770bf6` |

## Independent review outcome

Independent static review of v03b confirms t0/master/t4 recomposition and that the v03b offset avoids the previous 4 px right crop. The MG still has only a 4 px strong-alpha right margin, with soft alpha reaching x=940. The mug is substantially oversized versus the candidate and covers a large portion of the laptop keyboard/base and lower torso. MG/table support shifts 4 px relative to BG; cup/coaster shift 7 px relative to tabletop. Contacts read grounded in the stills, but these differential movements may slide. Warm QA contours remain, the hand digits cannot be counted, and playback was not reviewed. **NOT READY remains.**
