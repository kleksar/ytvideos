# Minnie v02 character MG assets — QA status

These are generated working candidates for Paper Detour 027, not approved montage assets. None passed edge QA. Do not mark them ready or assume BG/FG registration from matching canvas dimensions alone.

## Provenance and workflow

- Prepared in this folder under the `paper_artist.toml` role contract.
- Read the project `AGENTS.md`, Paper Detour channel guidance, and the `imagegen` skill before generation.
- The final clean-style attempts used written character/clothing/palette direction and the approved Paper Detour parallax reference. The old Minnie/pupil character cutouts were not passed as style references for those attempts because they contain a similar halo.
- PNG source candidates were created with image generation. Files named `*_registered.png` were canvas-normalized to 941×1672 RGBA by fitting/padding without stretching; this normalization does not remove edge artifacts, repair clipped silhouettes, or prove scene alignment.
- No Palmier project, storyboard, or file outside this `characters/` folder was edited.

## Candidates and visual count

| Candidate | Intended use | Visible figure count | Canvas / alpha bounds | QA result |
|---|---|---:|---|---|
| `MG_classroom_waiting_thirteen_v03_registered.png` | S06 classroom | Minnie + exactly 13 pupils | 941×1672 RGBA; alpha bbox `(6,0)–(934,1659)` | **DRAFT / FAIL** — only 6 px lateral margin, no top margin; red fringe remains (751 red-edge pixels among 17,403 sampled edge pixels, 4.32%). |
| `MG_storm_line_twelve_plus_carried_v03_registered.png` | S01/S08/S09/S10 storm crossing | Minnie + 12 walking pupils + youngest carried | 941×1672 RGBA; alpha bbox `(0,126)–(939,1559)` | **DRAFT / FAIL** — touches both horizontal canvas edges; red fringe remains (448/13,927 sampled edge pixels, 3.22%). |
| `MG_teacher_boy_memory_v01_registered.png` | S05 memory beat | Minnie + 1 generic boy | 941×1672 RGBA; alpha bbox `(0,49)–(935,1671)` | **DRAFT / FAIL** — touches left and bottom edges; red fringe remains (655/18,377 sampled edge pixels, 3.56%). |
| `MG_thread_overlay_v01_registered.png` | Independent behind-MG thread layer | Not applicable | 941×1672 RGBA; alpha bbox `(0,95)–(940,1252)` | **DRAFT / FAIL** — strand is too thick and has a strong red fringe (2,374/3,556 sampled edge pixels, 66.76%). Exact placement/occlusion against walking figures is untested. |

The edge-pixel values are a visual QA heuristic for detecting the bright red/orange fringe; they are not a perceptual quality score. All four registered PNGs have transparent RGBA canvases. Transparency alone does not make their visible edges clean.

## Coordinator follow-up, 1 November 2026

Two more image-generation attempts were reviewed after the candidates above: an edit of the classroom group and a paper-craft restyle guided by the approved parallax reference. The edit still showed a bright orange/red fringe and did not create safe margins. The restyle moved closer to the channel's tactile-paper look, but still showed a bright edge and clipped the group at the canvas boundary. Both were rejected and excluded from this pack; no character MG is approved for import.

## Compatibility limits

- The classroom count was visually recounted as 13 pupils plus Minnie. The crossing was visually recounted as 12 walking pupils plus the youngest carried by Minnie. The memory beat contains one generic boy with Minnie.
- The generated walking group has no rope baked into the people. The thread is a separate PNG and must remain independently layered.
- No asset has been composited over the assigned scene BG/FG plates. Boot-to-ground contact, overlap order, exact scale/perspective, hidden-background coverage, safe margins for rightward parallax, and thread visibility only through gaps therefore remain unverified.
- Do not use the original source variants or the registered candidates as finished assets. The latest reviewed generation attempts still showed the halo or unsafe crop. The candidates may be retained as count/pose references while a clean cutout approach is chosen.

## Earlier generated candidates

These earlier iterations are retained for provenance and are also not approved:

- `MG_classroom_waiting_thirteen_v01.png`
- `MG_classroom_waiting_thirteen_v02_source.png`
- `MG_classroom_waiting_thirteen_v03_style_ref.png`
- `MG_storm_line_twelve_plus_carried_v01.png`
- `MG_storm_line_twelve_plus_carried_v02_source.png`
- `MG_storm_line_twelve_plus_carried_v03_style_ref.png`
- `MG_teacher_boy_memory_v01_source.png`
- `MG_thread_overlay_v01_source.png`
