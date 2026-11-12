# Storm and farmhouse layer kit — v01

**State:** source-layer draft for the current v06/v07 scene direction; not yet assembled with the character MG, registered in Palmier, or checked in motion. All files are 941×1672 portrait PNGs (approximately 9:16) on a shared full-frame canvas. BG files are opaque; the three new FG files have alpha transparency. At 1080×1920, scale all plates together and preserve their registration.

## Shot setup map

| Shot | Background (BG) | Whole-character middle layer (MG) | Foreground layer(s) (FG) | Composition intent |
|---|---|---|---|---|
| **S01 — blizzard hook** | `01_hook_school_edge_BG_from_v01.png` — unchanged copy of `minnie_v01/09_school_escape_storm_background_v01.png` | Use the character worker's whole line: twelve pupils walking and the youngest carried by Minnie. Keep the twine legible in the first second, in clear gaps between silhouettes. | `FG_low_snow_ridge_v01.png`; the low ridge should leave the line and boots readable. | School remains at left, roof outside frame; open storm to the right, destination hidden. The people and twine layer must remain separate from the school BG.
| **S04 — distance to shelter** | `02_farmhouse_distant_BG_v01.png` | The whole pupil group staged small near the lower-left edge, still at the school-side of the scene; no route is drawn. | `FG_snowbank_edge_v01.png` | Distant house is small but readable in the upper-right area. Keep the lower-center field available for the MG.
| **S08 — crossing** | `03_farmhouse_crossing_BG_v02.png` | Same group and order, larger than S04 and traveling through the lower middle toward the house. | `FG_snowbank_edge_v01.png`, translated minimally so the group remains readable. | The house stays on the right; retain an open corridor around heads and the visible twine.
| **S09 — tightening storm / near-loss** | `04_farmhouse_near_loss_BG_v02.png` | Same group in the same travel direction. Keep all pupils countable by the cut to S10. | `FG_low_snow_ridge_v01.png`; keep the ridge under their boots. | Narrow visibility at the far edges while the house remains visible. Do not imply a child is lost or that the path disappears.
| **S10 — exterior arrival** | `05_farmhouse_threshold_BG_from_v01.png` — unchanged copy of `minnie_v01/07_farmhouse_exterior_threshold_v01.png` | All thirteen pupils remain outside at the threshold; do not show anyone crossing inside. | `FG_threshold_snow_lip_v01.png` | The center of the low snow lip stays below the characters' feet; keep the full group countable and preserve ground contact.

The MG is owned by the separate character-layer task and is intentionally not duplicated in this folder. The background and FG PNGs leave the center open for it. These are not five full master composites yet.

## Registered assets

| File | Role | Alpha | Shot use / notes |
|---|---|---:|---|
| `01_hook_school_edge_BG_from_v01.png` | Full-frame BG | No | Existing cold-open school edge, copied unchanged for kit convenience; school at left, roof cropped out. |
| `02_farmhouse_distant_BG_v01.png` | Full-frame BG | No | Quiet distance plate; one generic front-facing farmhouse, small amber window left and door right. |
| `03_farmhouse_crossing_BG_v02.png` | Full-frame BG | No | Denser crossing shot edited from the distant master so the same farmhouse is maintained. |
| `04_farmhouse_near_loss_BG_v02.png` | Full-frame BG | No | Stronger storm and narrower visibility; house remains legible. Edited from the same distant master. |
| `05_farmhouse_threshold_BG_from_v01.png` | Full-frame BG | No | Existing exterior threshold plate, copied unchanged; arrival remains outdoors. |
| `FG_snowbank_edge_v01.png` | Full-frame registered FG overlay | Yes | Low near-camera snow edge, mainly in bottom fifth. Keep it below faces and avoid hiding the group. |
| `FG_low_snow_ridge_v01.png` | Full-frame registered FG overlay | Yes | Narrow snow ridge for shots where all walking figures and boot contacts need to remain readable. |
| `FG_threshold_snow_lip_v01.png` | Full-frame registered FG overlay | Yes | Narrow foreground snow lip, mainly in bottom eighth, with a restrained amber reflection on the right. |

## Visual checks and limits

- Read and visually inspected the user-approved parallax reference `channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png`, plus the existing winter plates 05, 07 and 09 in `minnie_v01`. The reference uses a close, layered physical set: full background, whole-character layer and a near-camera prop plane, with tactile matte paper and contact shadows.
- Visually compared the active BGs: 02 is the distant master; 03 v02 and 04 v02 were edited from it to keep the same farmhouse. They share the 941×1672 canvas, cold indigo/blue layered-paper snow, diffuse upper-left light, and the same approximate house silhouette/orientation (front-facing, window left, door right). Exact pixel identity across the house is not verified. The background house is an illustrative reconstruction, not a verified portrait of a specific farmhouse.
- Checked PNG dimensions and alpha metadata with `sips`: all eight active BG/FG files have identical 941×1672 canvases; the five BGs are opaque and the three new FG overlays retain alpha. No text, people, route or footprint was added to the new plates.
- **Static FG-to-BG overlay edge check: PASS** for the current pairings below. The preview images are in `QA/`; they are review composites, not import layers or full master compositions.

  | Shot | BG + FG pair | Static edge result | Preview |
  |---|---|---|---|
  | S01 | hook-school BG + low snow ridge | PASS — edge is clean against the dark snowfield; group/twine clearance not yet assessed. | `QA/S01_hook_BG_FG_preview.png` |
  | S04 | distant-house BG + snowbank | PASS — no visible halo at the paper edge; overlaps lower snow detail as a natural foreground drift. | `QA/S04_distance_BG_FG_preview.png` |
  | S08 | crossing BG v02 + snowbank | PASS — edge color and surface sit within the cold snow palette. | `QA/S08_crossing_BG_FG_preview.png` |
  | S09 | near-loss BG v02 + low snow ridge | PASS — edge remains clean and low; central storm space stays open. | `QA/S09_near_loss_BG_FG_preview.png` |
  | S10 | threshold BG + threshold lip | PASS — narrow lip aligns along the bottom and picks up the warm doorway edge. | `QA/S10_threshold_BG_FG_preview.png` |

- **Still UNVERIFIED:** composite alignment with the separate MG, character contact with snow/threshold, any FG overlap of shoes or twine, alpha fringe at final 1080×1920 scale, edge bleed after movement, parallax playback, moving grain, or Palmier import. Do not treat static BG+FG preview passes as final shot approval.
- A separate upper snow-gust cutout was excluded from this pack because it showed a visible cyan fringe against transparency. The lower snowbank and threshold cutouts are retained; inspect their alpha edges again over the final plates before import.
- User's intended direction is BG, MG and FG all moving subtly left-to-right, with the displacement increasing by depth. Match storyboard v07: BG/MG/FG +2/+8/+16 px per second at 1080×1920. Scale all three rates together for the 941×1672 plates (about 0.87×); check edge coverage and contacts after the character layer is assembled. These are proposed values, not motion-tested values.

## Provenance

The three new BGs and three new FG cutouts were created with the built-in image-generation tool from written prompts and copied into this folder; the original generated files remain in the Codex generated-image cache. The hook and threshold BGs are copies of the earlier v01 PNGs, not new generations. No existing source asset was overwritten or moved; two first-pass BGs created in this task were moved into this kit's `Archive/` after continuity review. Nothing was imported into Palmier.

The first text-generated S08/S09 backgrounds had visibly different farmhouse proportions; they are retained in `Archive/` as superseded drafts and are not part of the active kit. Active S08/S09 plates are v02 edits from the S04 distant background.
