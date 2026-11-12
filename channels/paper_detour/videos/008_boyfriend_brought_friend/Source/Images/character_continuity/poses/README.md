# Short 008 — neutral standing character cutouts

**Status:** `DRAFT`. These are provisional continuity and layout references, not approved production finals or registered Palmier assets.

## Files

| Character | Original candidate | Preferred neutral DRAFT | Canvas |
|---|---|---|---|
| N — narrator | `CHAR_N_STAND34.png` | `CHAR_N_STAND34_v02.png` | 941×1672, 8-bit RGBA |
| B — boyfriend | `CHAR_B_STAND34.png` | `CHAR_B_STAND34_v02.png` | 941×1672, 8-bit RGBA |
| M — Matt | `CHAR_M_STAND34.png` | `CHAR_M_STAND34_v02.png` | 941×1672, 8-bit RGBA |
| F — invited friend | `CHAR_F_STAND34.png` | `CHAR_F_STAND34_v02.png` | 941×1672, 8-bit RGBA |

All four files have an alpha channel with transparent pixels outside most of the figure. Each file contains one whole person on the same tall canvas; none is divided into body parts. The complete figure and both shoes are within the frame. Their apparent heights are close, though Matt's stance fills slightly more vertical space and F is narrower because of her silhouette.

## Design and provenance

- The direct visual reference for all four was [`character_lineup_v01.png`](../character_lineup_v01.png). The lineup README records its scene 01 identity references and differences among earlier source versions.
- The designs carry forward the lineup's clothing and hair: N has a short dark wavy bob and rust-orange overshirt; B has dark wavy hair and a deep navy/teal overshirt; Matt has tousled auburn/copper hair and a coral overshirt; F has shoulder-length dark chestnut waves and a muted sage-blue overshirt. Each wears a cream shirt and casual trousers/shoes matching the lineup.
- F is the narrator's invited single friend, not Matt's fiancée. Her image is a neutral stand-in because no earlier F source image existed. No ring, flowers, phone, bag, text, or relationship gesture was added.
- Each cutout was generated separately with the built-in ImageGen tool using the lineup as its reference. The generated PNGs were copied to these filenames without pixel edits. Original ImageGen outputs are recorded under `/Users/diplomat/.codex/generated_images/01a194ca-6f84-7360-b821-dda96d304209/`:
  - N: `exec-a81be330-9b58-45ac-83fc-6e28b5ea398c.png`
  - B: `exec-1e652681-f7ac-45b4-859d-6ef4572ebc5a.png`
  - Matt: `exec-f7171af6-8489-4149-b704-636985624d3d.png`
  - F: `exec-eda30e3e-4d40-4739-a6f4-173eba7f3326.png`

## Visual check and limits

- Checked each PNG's dimensions and alpha channel, then viewed each cutout both over transparency and against a light-gray preview. All four show a calm near-front three-quarter stance, full silhouettes, visible hands, and both shoes. No obvious missing limb or severe hand defect was seen at this review size; this is not a finger-by-finger anatomy approval.
- There are small detached alpha specks in the transparent field, and some contours show a colored fringe/edge glow. These are visible on a light background at full canvas size. The files remain DRAFT and need review on the intended scene backgrounds; they are not described as clean or composite-ready.
- Figure margins are tight, especially around Matt's hair and shoes. Do not crop the canvas or infer a safe camera crop from these files.
- ImageGen's canvas placement does not establish a reliable anchor, pivot, foot baseline, or scene registration. Confirm those coordinates in a test composite before using these cutouts in a moving shot. Move each complete PNG as a layer; these files are not rigged characters.

## Preferred neutral retries v02 — independent static QA

| Character | File | Canvas / format | Status |
|---|---|---|---|
| N | `CHAR_N_STAND34_v02.png` | 941×1672 RGBA | DRAFT; no obvious detached points at preview size; warm edge fringe needs scene check |
| B | `CHAR_B_STAND34_v02.png` | 941×1672 RGBA | DRAFT; no obvious detached points at preview size; warm edge fringe needs scene check |
| M | `CHAR_M_STAND34_v02.png` | 941×1672 RGBA | DRAFT; two isolated 1 px alpha components within hair by threshold review; warm edge fringe needs scene check |
| F | `CHAR_F_STAND34_v02.png` | 941×1672 RGBA | DRAFT; no obvious detached points at preview size; warm edge fringe needs scene check |

These four are ImageGen retries from the character lineup plus the corresponding original cutout. Independent static QA found N/B/F have no obvious detached points at preview size; M retains two 1 px alpha components within the hair by threshold inspection. Warm orange-red fringe is still visible on several edges. No programmatic pixel cleanup was done. Prefer v02 as the neutral visual candidate, then confirm the fringe on actual scene backgrounds. Neither version establishes scale, anchor, pivot, baseline or compatibility with a scene master.
