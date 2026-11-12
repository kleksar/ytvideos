# Paper Detour 036 — screen accents v03

Date: 2026-11-02

## Scope and assets

Ten static English accent PNGs for the 45.2-second Short, including the former nine-cue plan plus a separate “ALREADY OCCUPIED” beat as the amphibian enters the occupied burrow. The assets replace neither the narration nor the voice recording. C02 (`250 MILLION YEARS`), C05 (`SEVEN BROKEN RIBS`) and C06 (`ALREADY OCCUPIED`) reuse the exact v02 title PNGs. The remaining seven exact-text assets were generated with the built-in image generation tool, using the existing Paper Detour `250 MILLION YEARS` accent as a style reference. C01 was refined to a one-line phrase after the first two-line candidate failed the shared optical-size check.

Exact ready-to-import files are in `import_ready_v03/`. Each is a transparent 1080×1920 RGBA PNG with its title composited at the same canvas position, so Palmier can use an identical full-frame transform for every cue. `IMPORT_MANIFEST.json` records hashes. Source titles, exact mask line boxes and provenance are under `source_pngs_v03/`; helper measurements and authoritative assigned scene-pair previews are under `rendered_v03_preflight/`.

The helper preflight covers all ten assigned scene/title pairs. Shared face height is 85 px; per-line measurements are 84–85 px; optical center is X≈0.50, Y≈0.16. The 360×640 phone contact sheet and every full-frame scene/title composite were visually inspected. The text is legible, stays within the picture, and leaves the animals, skulls, fracture inset, and flood action visible. This is static candidate preflight, not final Palmier composite QA. Actual Shorts UI safe-area and motion envelope remain unverified.

## Timing and limits

Proposed ranges were recalculated from `voice_en.alignment.json` at 30 fps and are recorded in `CUE_SHEET_v03.md`. Durations range from 1.2 to 2.63 seconds, within the cue-sheet working limits. They remain preliminary until the current voice is auditioned and the Palmier composite is checked. No audio was generated, edited or replaced.

## Palmier handoff

The new crop and ten full-canvas title PNGs are ready to import. Palmier Timeline 2 is preserved; these changes have not yet been applied to a new timeline because the Mac was locked when the editor handoff was attempted. Do not claim v03 has been assembled in Palmier until a new timeline, media links, clip ranges, and transforms are verified in the application.
