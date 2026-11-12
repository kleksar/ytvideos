# Plan 08 — v13-derived layer-first set

**Status: PASS for static t0/t4 still review; continuous motion unverified.** This is a new layer-first canonical master derived from the approved v13 composition reference. It does not claim pixel equality with the flat v13 source. No video or audio was created.

## Exact import map and placements

| Role | File | Canvas / mode | t0 x/y | t4 x/y |
|---|---|---|---|---|
| Canonical master | `masters/08_tears_master_v01_layered.png` | 941×1672 RGB | Actual t0 composite | — |
| BG | `layers/08_tears_BG_v01.png` | 941×1672 RGB opaque | 0/0 | +4/0 |
| MG | `layers/08_tears_MG_v01.png` | 941×1672 RGBA | −20/0 | −12/0 |
| FG | `layers/08_tears_FG_v01.png` | 941×1672 RGBA | 0/0 | +11/0 |

Order: **BG → MG → FG**. Net motion is BG +4, MG +8, FG +11 px right over the tested interval. BG t4 uses a mirrored 4 px left-edge fill. No layer has a Y offset.

Previews: `previews/08_tears_v01_t0_BG0_MGminus20_FG0.png` and `previews/08_tears_v01_t4_BGplus4_MGminus12_FGplus11.png`.

## QA record

- All selected masters/layers/previews are 941×1672. BG is opaque RGB; MG/FG are RGBA.
- The canonical master equals the t0 preview byte-for-byte. Both t0 and t4 previews recompose exactly from the listed layers/positions; RGB difference bounding boxes are empty.
- MG carries Joshua’s face, single tear, hair, full shoulders and sweater as one group. MG alpha ≥2 bounds are x=26…940/y=480…1527; at t0 they are x=6…920 and at t4 x=14…928. Full-frame strong alpha (≥128) at t0 is x=14…918 and at t4 x=22…926. In the shoulder band y=950…1249, alpha ≥2 is x=41…905 at t0 and x=49…913 at t4; strong alpha is narrower at x=44…902 and x=52…910 respectively. Independent review confirms the t4 right shoulder ends at x≈913, leaving a 27 px blue-wall margin with the full silhouette inside the frame; the left shoulder has about 49 px. This passes the adjusted no-crop/≥20 px endpoint criterion. The face and single tear remain readable; hands are outside the crop, so finger count is not applicable.
- FG is the existing small blurred desk corner. Its alpha ≥2 bounds are x=0…94/y=1516…1671 at t0 and x=11…105/y=1516…1671 at t4. It remains in the lower-left foreground, but touches the left and bottom frame edges at t0 and the bottom edge at t4, as in the source framing. This is explicitly flagged for the reviewer to judge; do not import unless the edge crop is accepted.
- Cyan matte QA shows warm orange/red edge pixels around the cutout; independent review found they read as motivated amber/cool rim light over the actual simple blue wall. Reviewer accepted the FG lower-left edge touching left/bottom at t0 and bottom at t4 as a natural soft foreground corner with no hard matte.
- Independent still review passed exact t0 master equality, t4 recomposition, 941×1672 dimensions, face/tear, background, matte read, FG edge treatment and shoulder safety under the adjusted ≥20 px margin criterion. No playback; continuous motion remains unverified.
- The BG is a generated clean night wall. The MG+FG are generated alpha cutouts from v13. There is no hand movement, no added props, no text or UI. Endpoint stills only; continuous motion has not been played.

## Provenance

- Flat composition reference: `../plan08_tears_v13_v01/masters/08_tears_master_v13_composition.png`.
- BG ImageGen source: `/Users/diplomat/.codex/generated_images/01a194de-e95f-7233-95be-7f11b3636ee3/exec-ae044df1-3262-4890-8ed2-b2881a07e6b1.png`.
- MG ImageGen source: `/Users/diplomat/.codex/generated_images/01a194de-e95f-7233-95be-7f11b3636ee3/exec-d776ec7f-aec3-4336-9553-240dac203748.png`.
- FG ImageGen source: `/Users/diplomat/.codex/generated_images/01a194de-e95f-7233-95be-7f11b3636ee3/exec-77011e41-3daa-4929-8f93-8ded2a201a2a.png`.
- This set is a new v01 sibling; v13/v14/v15 source masters and prior drafts remain untouched.
