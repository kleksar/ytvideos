# Paper Short 038 — caption asset generation log v01

**Date:** 2026-11-03  
**Decision owner:** Paper captions  
**Caption choices:** [decision record v01](DECISION_RECORD_v01.md)  
**Cue sheet:** [v01](CUE_SHEET_v01.md)

## Source PNGs

Both phrases were generated with the built-in `image_gen` tool as transparent PNG candidates. The selected source outputs were copied into this versioned episode directory; generator originals remain in the Codex generated-images directory.

1. `IRAN-BORN_v01.png` — [selected source PNG](IRAN-BORN_v01.png), 2172×724, RGBA, real alpha; SHA-256 `4705f8e03189c0ee44d1382084dd141dcdb07703181bf195e72a5edbfafae531`.
2. `WE_ARE_ALL_BROTHERS_v01.png` — [selected source PNG](WE_ARE_ALL_BROTHERS_v01.png), 2172×724, RGBA, real alpha; SHA-256 `94562033be64459b0e140f4eebcc31d44a3d27069041ba61c1090ac8c9f4e06d`.

Positive references used for both: `A_MESSAGE.png`, `MATCH.png`, `REPORTED.png`, and `FORMAT_MATTERS.png` in `channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/`. The actual accepted PNG files were visually inspected before generation and both resulting source PNGs were checked for exact wording, line break, cream paper face, orange-red edge, shadow and alpha. No confirmed production font or full glyph atlas was available; these remain visual candidates compared directly against the accepted channel PNGs.

## Exact generation prompts

### C01 — IRAN-BORN

> Create one isolated semantic caption asset with the exact uppercase text IRAN-BORN: I R A N, hyphen, B O R N. One line only. Large wide rounded slightly irregular sans-serif forms physically cut from thick cream paper, subtle warm orange-red paper edge and soft dimensional shadow, visible matte paper fibers. Match the supplied accepted Paper Detour typography references in letter shape, thickness, cream face, orange rim, spacing, bevel and shadow. Keep the complete phrase centered and fully inside the canvas with generous transparent margins. Use true transparent background with alpha; no black, white, colored, textured, or checkerboard background. No icons, no other words or extra letters, no frame. Clean editorial caption PNG.

Selected generator original: `/Users/diplomat/.codex/generated_images/01a19e92-58c1-7d10-9da8-7626efa8e45c/exec-817a8e2c-ac58-45eb-8678-4d6806cb83c0.png`.

### C16 — WE ARE ALL / BROTHERS

> Create one isolated semantic caption asset with exactly this uppercase wording and exact two-line break: line 1 `WE ARE ALL`; line 2 `BROTHERS`. Do not add quotation marks, punctuation, or any other text. Large wide rounded slightly irregular sans-serif letters physically cut from thick cream paper, subtle warm orange-red paper edge and soft dimensional shadow, visible matte paper fibers. Closely match the supplied accepted Paper Detour typography references in letter shape, thickness, cream face, orange rim, spacing, bevel and shadow. Keep both lines centered, line widths balanced, line spacing clear, and the complete phrase fully inside the canvas with generous transparent margins. True transparent background with alpha; no black, white, colored, textured, or checkerboard background. No icons, no frame. Clean editorial caption PNG.

Selected generator original: `/Users/diplomat/.codex/generated_images/01a19e92-58c1-7d10-9da8-7626efa8e45c/exec-2cfe3e1e-1882-45ef-843f-42e053f13ac6.png`.

## Preparation and inspection

- The scene PNGs remain unchanged at 941×1672. Work-only preview derivatives were resized with Pillow LANCZOS to 1080×1920 for the helper's exact canvas contract. The aspect ratio adjustment is approximately −0.053%, arising from the rounded native source dimensions.
- Helper: `render_paper_captions.py` v1.1.0, SHA-256 `86fcde095d01b3300ac1497f9f38c5f38494a740f5dcd987af9a8595d42a8150`; Pillow 11.3.0.
- The first input attempt used automatically separated cream-face rows and stopped because the hyphen/texture fragmented row bands. No caption PNG was imported from that attempt. Explicit measured face-line boxes were added and the helper completed.
- A selected-anchor trial placed C01 on the primary and visibly crossed the S01 fold. One Extra High consultation accepted the channel's single alternate anchor for S01 while keeping the primary for S16. The final alternate was refined horizontally to retain the x=100 safe boundary and a visible gap before the fold; no independent resize or scene modification was introduced.
- Current managed preparation: `Assets/Generated/captions-v01-current/`; current preview/composite evidence: `Work/captions-v01-current/`. The helper's global static geometry result is technical PASS; tool states for visual, synchronization and motion are UNVERIFIED.
- Final current C01 cue: 436×146 px, face line 68 px, alpha bbox `[10,2,426,137]`, SHA-256 `c5ed0a3c513c40bdffdaef2ab5df8ec758d837ec36476de88015fc0e239bc3dd`.
- Final current C16 cue: 501×167 px, face lines 65/67 px, alpha bbox `[34,11,495,167]`, SHA-256 `2adb802bdd84a4bf0cd4d8fcab21d49ee7213ab4db0d199d08d81766b9e04dd8`.
- Coordinator visually inspected actual source PNGs, cue/mask PNGs, both assigned full-resolution composites, both phone previews, and the contact sheet. C01/S01 uses the upper-left alternate; C16/S16 uses the upper-right primary. S17 remains text-free with the clean reused S01 image. Independent image review, recording audition, final synchronization, caption-motion path and final MP4 QA have not occurred.

## Superseded comparisons retained

- `Work/captions-v01-preflight/` — failed first helper attempt; its diagnostic directory remains.
- `Assets/Generated/captions-v01-preflight-2/` + matching `Work/` — early common-primary placement; retained for comparison, not current.
- `Assets/Generated/captions-v01-preflight-3/` + matching `Work/` — first alternate-position trial at x=0.30; retained for comparison, superseded by the slightly left-shifted final safe placement.
- `Assets/Generated/captions-v01-preflight-4/` + matching `Work/` and `Assets/Generated/captions-v01-selected/` + matching `Work/` — duplicate successful selected-geometry previews before final backend status was recorded. They are not current; `captions-v01-current` is the canonical helper output.

All retained trials are provenance/working data. Do not import their cues in place of the current version.
