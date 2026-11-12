# Plan 12 resource-meter layer set — v02 canonical composition

**Status: PASS for the accepted canonical still layers and t0/t4 static endpoint composites only. Motion playback is not verified.** Parent accepted the v02 layer-first composition as the new canonical master. `Source/Images/07_resource_meter_master_v01.png` remains unchanged and is retained as a visual reference; this v02 master is a declared new composition, not a pixel-registered extraction of v01. The original failed drafts with `NOT_READY` suffixes remain preserved.

## Import-named layer files

Z-order: **BG → MG → FG**. All planes and stills are 941×1672. The clean import-named copies have the same bytes as the reviewed v02 layer candidates.

| Plane | Import path | Format / alpha | Strong alpha bounds | Contents |
|---|---|---|---|---|
| BG | `07_resource_meter_BG_v02_layered.png` | RGB, opaque | — | Whole room and continuous tabletop clean plate. |
| MG | `07_resource_meter_MG_v02_layered.png` | RGBA, alpha 0–255 | x=0…898, y=551…1216 | Blank-screen laptop, resting hand/cuff and laptop base/contact shadow. The left crop is beyond the canvas at both listed positions. |
| FG | `07_resource_meter_FG_v02_layered.png` | RGBA, alpha 0–255 | x=498…915, y=1225…1331 | Physical paper resource strip. This candidate is positioned +90 px vertically versus the source strip so it rests on clear tabletop below the laptop base; the existing contact shadow is retained. |

## Canonical master and static endpoints

- New canonical master: [`07_resource_meter_master_v02_layered.png`](07_resource_meter_master_v02_layered.png). It is a byte-identical copy of the reviewed t0 composite.
- t0 composite: [`07_resource_meter_t0_canonical_v02_layered.png`](07_resource_meter_t0_canonical_v02_layered.png).
- t4 static endpoint: [`07_resource_meter_t4_static_endpoint_v02_layered.png`](07_resource_meter_t4_static_endpoint_v02_layered.png).

| Endpoint | BG position | MG position | FG position |
|---|---:|---:|---:|
| t0 | 0 px | −8 px | 0 px (+90 px canonical Y placement) |
| t4 | +4 px | 0 px | +11 px (+90 px canonical Y placement) |

All three planes have positive horizontal deltas of +4/+8/+11 px. The t0 and t4 static compositions were reviewed; no timeline or motion playback has been tested. BG+4 edge-fill candidate is retained as `07_resource_meter_BGplus4_edgefill_v02.png`.

## Independent evidence and story clarity

Independent review passed internal t0/t4 BG/MG/FG recomposition, all three endpoint deltas, the table contact, and edge positions. The reviewer also found the laptop, blank screen and paper strip physically grounded. Parent selected this layer-first v02 image as the new canonical composition, resolving the earlier mismatch against v01 by keeping v01 only as a reference. The prior reviewer measured MAE 16.50 and more than 865,000 pixels differing by over 10 levels against the old v01 master; that historical comparison does not establish or invalidate registration to the newly accepted v02 canonical master.

The strip has no numerals or UI. Its long-axis centerline measures about **45.4% teal used / 54.6% beige remaining**. Reviewer noted the colors alone could be ambiguous. The planned separate paper “55%” accent during narration clarifies remaining capacity without adding UI text to the asset.

**Scope limit:** PASS applies to the still canonical composition, layer inputs and checked static endpoints. Do not claim that continuous motion, timing or playback has been reviewed.

## Provenance and hashes

The import-named copies were created from the existing v02 candidates; source candidates and master v01 were not modified.

| File | SHA-256 |
|---|---|
| `07_resource_meter_master_v02_layered.png` | `9d16dac39e11fdf4e354cf4bc4d22818c688132b7f1d277d4cdf3c2d1322a31b` |
| `07_resource_meter_t0_canonical_v02_layered.png` | `9d16dac39e11fdf4e354cf4bc4d22818c688132b7f1d277d4cdf3c2d1322a31b` |
| `07_resource_meter_t4_static_endpoint_v02_layered.png` | `fe8dff9676190c611e09f1d6255527a351da892bd797698202476a2d2cfe7f3e` |
| `07_resource_meter_BG_v02_layered.png` | `1ba64371d7aabeaff2d5362d95076e7d9b45b9ada5da9aed3b585fe4c1f8b68c` |
| `07_resource_meter_MG_v02_layered.png` | `c4ac1ba98c882a9572357300d2b0eaafa917688cffcd4279a99cf4d94215ca0c` |
| `07_resource_meter_FG_v02_layered.png` | `7ac58a965d78ea59bfda963cd3ff28ea0f40c7b8f1f77c8825b1bb900a49ec93` |
| t0 composite | `9d16dac39e11fdf4e354cf4bc4d22818c688132b7f1d277d4cdf3c2d1322a31b` |
| t4 composite | `fe8dff9676190c611e09f1d6255527a351da892bd797698202476a2d2cfe7f3e` |
