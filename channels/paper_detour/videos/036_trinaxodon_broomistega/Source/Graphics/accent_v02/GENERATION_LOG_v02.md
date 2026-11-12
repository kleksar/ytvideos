# Paper Detour — screen accents v02 generation log

Date: 2026-11-02

## Scope

Nine static paper-text accents for the 45.2-second English Short. They replace the four-cue working set for the next edit. This is an editor-authored working version under the user's instruction to proceed without consultation. Narration, voice, and audio mix were not changed.

## Visual source and method

- Six cue PNGs were newly generated as transparent paper-lettering assets with the image generation tool, using the already established Paper Detour accent language: cream cut-paper letterforms, warm orange paper outline/accent, soft dimensional shadow, compact centered composition, transparent canvas. Generated exact wording was checked visually before use.
- Three cues reuse the project’s existing v01 assets rather than generating replacements: `HOSTILE SURFACE`, `SEVEN BROKEN RIBS`, and `REFUGE → TRAP`.
- All nine were normalized by the project helper to a shared measured 80 px cap/face height for a 1080×1920 canvas. Selected anchor: upper center, `[0.50, 0.12]`.
- Source cue files: `source_pngs_v01/cues/C01.png` through `C09.png`.
- Prepared timeline-ready files: `import_ready_v02/`.
- Full-frame and phone-size candidate composites, bounds, and technical manifest: `rendered_candidate_v02/`.

## Asset mapping

| Cue | Text | Provenance |
|---|---|---|
| C01 | TWO SKELETONS / ONE BURROW | New transparent paper accent |
| C02 | 250 MILLION YEARS | New transparent paper accent |
| C03 | HOSTILE SURFACE | Reused v01 cue asset |
| C04 | ASLEEP THROUGH / THE HEAT | New transparent paper accent |
| C05 | SEVEN BROKEN RIBS | Reused v01 cue asset |
| C06 | ALREADY OCCUPIED | New transparent paper accent |
| C07 | REFUGE → TRAP | Reused v01 cue asset |
| C08 | SEALED IN STONE | New transparent paper accent |
| C09 | FOUND TOGETHER | New transparent paper accent |

## Review status

The author visually inspected all nine rendered cue PNGs and all nine full-frame/phone mockups at the candidate's shared 80 px face-height. Wording is legible; accents do not cover the animals, injury, or skeletons in those candidate pairs. The helper’s static candidate size/position checks pass. In Palmier, the cue clips use 972 px-wide transform rectangles. A read-only calculation from the matching local PNGs and actual transforms estimates per-line face-height at 116–154 px; the cues do not share the intended 80 px optical size, and C04's optical center is notably higher. Alpha bounds remain inside the frame with about a 39 px minimum horizontal margin, but exact bounds on a full-size Palmier composite and Shorts interface safe area are UNVERIFIED. Rebuild the geometry and repeat all assigned pair preflights before acceptance. Timeline 2 ranges are present; playback sync, actual audio listening, and export QA have not been done. No motion was applied.
