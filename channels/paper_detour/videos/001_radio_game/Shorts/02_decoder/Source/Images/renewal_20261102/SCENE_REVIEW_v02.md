# Scene 07 replacement candidate — 2026-11-02

Status: **DRAFT CANDIDATE — not imported or accepted for the timeline**.

## Purpose and decision

The current `06_reported_comparison.png` places two comparison cards in the fixed on-screen subtitle zone during the last two groups (`an MSX game`, `called Avenger.`). The cards are story-relevant props, so this is a text-composition collision. The retained narration, words, cue timing, subtitle baseline, and upper `AVENGER` accent stay unchanged.

The coordinator consulted ChatGPT.com with the visible mode **5.6 Extra High** (the project selector showed **5.6 Extra High**). Recommendation: raise the two cards and magnifying glass together as one composition block, preserve their relative scale and placement, leave the upper accent and subtitle baseline fixed.

## Candidate file and provenance

- Candidate: `06_reported_comparison_v02_caption-safe.png`
- Native dimensions: 941 × 1672 px; portrait ratio 0.5628. Requested target in prompt: 2160 × 3840 px. The tool returned the measured size above; this is not 4K native resolution.
- SHA-256: `9c43429641f19f4c119b709b2e5c09c9437fed468f1b955e0a2383aa4456e403`
- Edited source: `../director_trial_20261031/06_reported_comparison.png`, SHA-256 `11c6918e8bceb4b283cb76172976f7a393f42797ecf9c9e77082401773e5d6e8`
- Style reference: `channels/paper_detour/Shared/References/Paper/paper004_user_38.png`, SHA-256 `238bb11958c8e59224edcd006db060df0bddd0c9e100f795e44eeb537ebdc166`
- Generation service output: `/Users/diplomat/.codex/generated_images/01a19ab6-e212-7370-8b9b-fce4d2514654/exec-3d8ae1a5-12ff-4d1d-9026-e3f184c4d7d4.png`; immutable project copy is the candidate above.
- Applied controls: built-in image editing; source and style reference supplied. No resolution control was exposed; actual native dimensions are recorded above.

## Exact edit prompt

> EDIT reference image 1, using reference image 2 only to match the handmade paper/card material, layered edges, fibers, warm physical light, and dimensional shadows. Create a complete opaque full-frame portrait 9:16 Paper Detour diorama, maximum available image quality and fine detail, target 4K UHD 2160×3840. Preserve the exact cozy tabletop setting and overall palette from image 1: warm red desk lamp on the upper left, leafy plants/bookshelves, deep midnight blue wall, paper stack at left, blank textured paper box at center-right, and wooden tabletop. The only composition change: move the two face-up paper comparison cards and the magnifying glass upward together as one compact group, maintaining their relative scale, angle, order, and contact shadows. Position the entire group clearly in the central portion of the frame, with the lowest edge of either card well above the lower subtitle-safe area (leave the lower 22 percent of the frame free of foreground objects, with only the textured tabletop/background visible there). Do not move the lamp, paper stack, box, plants, wall art, or camera perspective. Keep generous dark-blue negative space in the upper central region for a separate title accent; do not add any lettering, numbers, title text, captions, logos, frames, or watermarks. Maintain physically plausible spacing and avoid overlap between the lifted card/magnifier group and the paper stack or box. The cards may retain their existing sunset-and-mountain illustrations but must remain visible and unobstructed. This is one static scene, no animation.

## Checks

- Opened the exact candidate full-frame and compared its paper material, warm lighting, cards, magnifier, tabletop, and protected upper accent area with the source and Paper reference.
- Static composition: lower subtitle zone is clear of foreground props; the cards and magnifier are grouped higher and remain visible. The upper central field remains open for the separate accent.
- Native source is below the requested 2160 × 3840 target and below the 1080 × 1920 delivery canvas; it must be judged at the actual delivery crop before acceptance.
- Not yet checked in the motion-rendered scene, through the full camera/parallax path, or in a scene-plus-caption composite. No Palmier import, timeline change, or export has occurred.
- Therefore this file is a candidate only. It does not invalidate the current exported MP4 or its QA record; importing it will require a targeted motion/caption check and a new export/QA.
