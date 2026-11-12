# Scene image generation and review — v01

## Shared generation spec

Built-in `image_gen` was used (no CLI/API fallback). Every final still is a full-bleed opaque vertical 9:16 paper/card diorama; prompts asked for maximum available quality and a 4K UHD target (2160×3840), layered cut-paper edges/fibers, physical contact shadows, no writing/UI/labels, and the accepted Paper004 reference for material and light. Actual returned files are **941×1672 px** (roughly 9:16), below the requested target and below the 1440×2560 delivery canvas. The final render will upscale them; this is a quality limitation, not native 4K/2K artwork.

Primary reference: `/Users/diplomat/ytvideos/channels/paper_detour/Shared/References/Paper/paper004_user_38.png` (SHA-256 `238bb11958c8e59224edcd006db060df0bddd0c9e100f795e44eeb537ebdc166`). For stork-bearing frames, `S01_v02.png` was also used only to keep the white stork, red bill and feather/arrow material consistent.

## Final selected images

| Scene | Final prompt-specific composition | File | SHA-256 | Review |
|---|---|---|---|---|
| S01 | Close hook: white stork neck, red bill, dark shaft; cool North European meadow; repositioned upward to keep lower-center subtitle clear. | `S01_v02.png` | `1b027d39585889f9fbcb6d93d23b4e65f6b4befce29aa1604dc440ddeb81014b` | PASS composition/material; no graphic injury. |
| S02 | Returning swallows and storks over a spring village; nest moved left, calm central lower roof area. | `S02_v02.png` | `262f141b91dc775b754a82908bbfcd8e88aa7ace72f3ce07c770b6cb136441a6` | PASS; scene text-fit still awaits actual overlay. |
| S03 | Generic 17th-century English scholar in a candlelit study with blank book and moonlit window; not a Morton likeness. | `S03_v01.png` | `3d05b67b3e4c8c185f029de97795c846c4bff55ebd1d2beb96fa7e938493d78d` | PASS as generic reconstruction. |
| S04 | Large textured paper Moon with a few small swallows and stork, visibly an imagined hypothesis. | `S04_v01.png` | `a1c8925af27f797f43bfe018cd42c992828086052f9181581e2a139ed301eaf3` | PASS as visual metaphor. |
| S05 | Upright stork in northern German meadow with arrow already in feathered neck; no hunter or shooting act; bird raised clear of subtitle line. | `S05_v02.png` | `47329929a5155a564909859dd39e322b6682b0b6fd1e93c3cffcc130ae2b188f` | PASS; no blood or weapon. |
| S06 | Neck/shaft close-up with African paper silhouette behind, no route or pinpoint. | `S06_v01.png` | `a357818c6de7ebee441af05a9790119be1e83c20524d26986008d01bb2f62bbe` | PASS; arrow and bill read separately. |
| S07 | Stork carrying arrow across a broad sea between distant Europe and Africa; lower-center subtitle on open water. | `S07_v02.png` | `5ff4e297c9741f8fd6c7933e99f9312677967388aa82aeb1f63969e8c4ca4eb7` | PASS; symbolic distance, no route. |
| S08 | Complete stork on plain plinth, arrow clear in neck, restrained exhibit study. | `S08_v01.png` | `a44f7f1795232185f7f5585268f5954bd488f568fae425088fb0276719d05afa` | PASS; interpretive diorama, not an archival image. |
| S09 | Generic natural-history collection interior with the stork behind a case; no labels/logos. | `S09_v01.png` | `f530db8340ce1f41b61f8e9e863402d202b85f05b7dc5c94a751a31487d9ae2a` | PASS as generic reconstructed room. |
| S10 | Wide migration tableau: a few birds between stylized continents, empty Moon distant. | `S10_v01.png` | `1c9f50916fd507af0ce60574f6e83d0e6fdc516c630d880c3dd6339b7956c7d7` | PASS; no exact route or universal claim. |
| S11 | Byte-identical reuse of the S01 master for the loop. | `S11_v01.png` | `1b027d39585889f9fbcb6d93d23b4e65f6b4befce29aa1604dc440ddeb81014b` | PASS; identical hash to S01. |

The full final-set contact sheet is `CONTACT_SHEET_v01.jpg`; all final scene PNGs were inspected at full displayed resolution and together. Material, composition and gross object continuity pass coordinator preflight. This does **not** validate final subtitle/accent composites, motion/crop endpoints, full MP4, sound or independent review.

## Rejected / superseded generations

- Initial S01 was replaced because the stork/arrow sat too low for the fixed subtitle center; S01 v02 is selected.
- S02 v01 was replaced because the nest occupied the centered subtitle line; S02 v02 moves the nest left.
- S05 v01 was replaced to keep the standing bird and feet above the fixed subtitle line; S05 v02 uses a clear field behind the subtitle.
- Initial S07 placed the shaft at the beak and is rejected. A first correction moved it to the neck; S07 v02 further moves the continents away from the subtitle line. Only S07 v02 is selected.
- The first S08 batch result was visible but returned without a usable saved workspace-path hint. A single-path S08 generation was created and saved as `S08_v01.png`.
