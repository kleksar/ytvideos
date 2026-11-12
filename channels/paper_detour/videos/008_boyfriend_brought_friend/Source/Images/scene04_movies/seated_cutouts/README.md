# Scene 04 — isolated seated character layers

**Status: DRAFT.** This set is a candidate cutout pass for scene 04. It is not approved, a registered final composite, or tested in Palmier.

## Current candidate files

| File | Character / pose | Canvas | Visible alpha bbox* | Format and alpha |
|---|---|---:|---:|---|
| `scene04_seated_N_v03.png` | N, narrator, left position; rust-orange overshirt, cream shirt, dark trousers; seated facing screen, rear / slight three-quarter view | 941×1672 | 538×800 at (0, 550) | RGBA; non-opaque, four corners transparent |
| `scene04_seated_B_v03.png` | B, boyfriend, center position; deep teal overshirt, cream shirt, dark trousers; seated facing screen, rear / slight three-quarter view | 941×1672 | 420×713 at (308, 513) | RGBA; non-opaque, four corners transparent |
| `scene04_seated_M_v03.png` | Matt, right position; coral overshirt, cream shirt, light trousers; seated facing screen, rear / slight three-quarter view | 941×1671 | 317×644 at (624, 565) | RGBA; non-opaque, four corners transparent |

All three are standalone full-canvas layers with one whole seated figure; no chairs, cinema background, screen, text, or props are baked into them. M's ImageGen output is one pixel shorter than the requested 1672 px canvas; this is retained as generated and must not be assumed to have exact vertical registration.

\*Visible alpha bbox is measured on pixels with alpha above 1%; it records the rough content bounds, not a hard cutout boundary.

N's visible alpha reaches the left canvas edge, and M's reaches the right canvas edge. Both may be clipped by the frame; do not treat their outer silhouettes as complete cutout contours.

## References inspected

- `../../character_continuity/character_lineup_v01.png` — DRAFT identity and outfit reference. N is the leftmost woman with short dark wavy hair and rust-orange overshirt; B is the dark-haired man in teal; Matt is the copper-haired man in coral. It is an opaque horizontal lineup, not a seated pose master.
- `../scene04_movies_background_v01.png` — 941×1672 opaque cinema plate, blank screen, empty room; used only for scene light and perspective.
- `../scene04_cinema_seat_fg_v01.png` — 941×1672 transparent foreground seat layer; used for seat-back height and occlusion context. It contains **two** close chair backs, so it does not establish three separate foreground seat positions for the trio.
- `../scene04_seated_trio_mg_v01.png` — 941×1672 transparent grouped pose; DRAFT, used for relative seated pose, scale, eye-line and left/center/right positions. It is not itself registered against the cinema BG/FG.

## Generation history and rejected drafts

All figures were made with the built-in imagegen tool and requested on a transparent full 9:16 canvas. The v03 candidates were generated one person at a time from the grouped trio layer, with instructions to retain only the selected person and preserve that person's source position and scale. The generator returned the requested 941×1672 size for N and B and 941×1671 for M. This is model-guided extraction/redrawing, not a pixel-preserving alpha mask from the group master; small differences in silhouette, relative scale, and position remain possible.

The earlier attempts remain in `iterations_not_for_use/`:

- `scene04_seated_N_v01.png`, `scene04_seated_B_v01.png`, `scene04_seated_M_v01.png` — first isolated generations. Each was centered and too large for its group slot; rejected for registration.
- `scene04_seated_N_v02.png`, `scene04_seated_B_v02.png`, `scene04_seated_M_v02.png` — second pass from all four references. The person selection improved, but size/body extent still drifted from the grouped pose; rejected as registered scene layers.

The v03 files are the best current individual candidates, not a claim of final registration.

The v03 imagegen prompts used Image 1 as the grouped source and asked to keep one selected person at the existing position/scale while making the other two transparent. The exact calls were:

- N: “Use case: background-extraction of a registered paper-diorama layer. Edit Image 1 as a transparent-layer extraction, not as a new portrait. Keep only the leftmost narrator, the rust-orange seated woman, exactly at her current pixel coordinates and current scale on the 941×1672 canvas. Preserve her original seated pose and visible extent from head through torso/upper lap; do not add legs or extend her below the original source silhouette. Set the two other people completely transparent. Preserve the exact camera, layout, body scale, lighting, paper texture, and all transparent empty canvas. Do not crop, resize, recenter, enlarge, shift, or redraw the retained person. No chairs or background; keep actual transparency. No added body parts, props, text, or marks.”
- B and Matt: same instruction with “the central deep-teal boyfriend” or “the rightmost coral-shirted Matt” selected; retain source pose/extent, clear the other two people, keep the full canvas and transparent background, and add no chairs, background, props or text.

## Checks and remaining limits

- **Format / transparency: PASS.** ImageMagick reports sRGBA with non-opaque alpha on all candidates; all four canvas corners sample alpha 0.
- **One character / no extras: PASS by visual inspection.** Each v03 has one person only; no chair, background, screen, text, or prop is visible.
- **Identity / wardrobe: PASS at the visual-reference level.** Hair and outfit colors match the lineup. The rear-facing view limits facial-identity comparison.
- **Pose: PARTIAL.** All three read as seated and face the screen. N shows more of the lap/lower silhouette than B or Matt. N and Matt reach the frame edges; exact pelvis-to-seat contact and equal eyeline/scale across seat positions remain unverified.
- **Hands / fingers: N_A.** Hands are not visible as distinct fingers in these rear views; there is no finger-count evidence to inspect.
- **Edge / lighting: UNVERIFIED in production.** A warm orange rim/fringe is visible around hair and clothing. It may agree with the cinema sconces, but final edge quality and spill against the background need review.
- **Layer registration: UNVERIFIED.** A temporary visual preview of BG → N/B/M v03 → seat FG was inspected. The three figures read across the row and foreground chairs obscure their lower bodies, but the two-chair FG cannot validate three seat contacts; some side-by-side overlap and N's lower silhouette need a proper scene master review. The preview was not saved as an approved composite.
- No source reference, BG, FG seat, grouped pose, Palmier project, or other folder was edited.
