# Paper cue sheet v02 — Short 035

**Status:** coordinator-designed expanded accent set, assembled in Palmier and placed on the motion review timeline. User replied “гуд” after receiving Motion Safe Review v02 and directed work to continue to QA/export. The subsequent QA found that scene pacing still violates the Paper 4–6 s rule in S02, S06 and S09; this preview is not a final delivery. These are paper phrase accents, not continuous subtitles. The accepted voice is reused unchanged.

**Editorial basis:** `CAPTION_DECISIONS_v02.md`. Three new cue PNGs were added alongside the two existing cues. The selected scenes keep S02, S05, S08 and S09 text-free; S09 stays clear for the open sentence and direct loop.

**Timing source:** accepted narration EN v06 plus `voice_en.alignment.json`, an automatic character alignment of the accepted recording. Seconds below are alignment-derived, quantized to the 30 fps timeline frames shown. The coordinator did not independently listen to the recording in this pass; audible emphasis, exact playback sync and the last spoken endpoint remain `UNVERIFIED`.

| Cue | Exact text | Scene / anchor | Trigger → end | Alignment time → timeline frames | Purpose | Optical size / source alpha bounds | Motion of phrase |
|---|---|---|---|---|---|---|---|
| C03 | `ONE LIMB.` / `TWO WEAPONS?` | S01 / primary | “A spear in one mantis shrimp” → “A hammer in another.” | 0.00–3.36 s → `[0,101)` | Reframes the spoken contrast as the question that drives the story. Opening accent is a deliberate short hook repetition. | 76 px target face-height on 941×1672 working canvas; alpha bbox `[191,160,749,326]`. | 4-frame fade and 0.055 upward travel into hold; 4-frame upward exit. |
| C01 | `THE` / `EXCEPTION` | S03 / primary | “began to stand apart” → “the others.” | 13.28–15.60 s → `[398,468)` | Punctuates the shift from S02's repeated pattern. | 76 px target; alpha bbox `[317,115,626,350]`. | Existing 4-frame entrance/hold/exit keys preserved. |
| C04 | `SEPARATE PATHS` | S04 / primary | “Across different lineages” → “two very different shapes.” | 15.80–20.32 s → `[474,610)` | Helps read the side-by-side outcomes as distinct lineage paths, not one modern form transforming into the other. | 76 px target; alpha bbox `[175,149,767,345]`. | 4-frame fade and 0.055 upward travel into hold; 4-frame upward exit. |
| C02 | `PIERCE` / `≠ STRIKE` | S06 / alternate | “its striking end” → “a powerful blow.” | 26.56–32.08 s → `[797,962)` | Bridges the spearer close-up and smasher close-up with a functional contrast. | 73 px existing face-height; alpha bbox `[469,174,812,331]`. | Existing 4-frame entrance/hold/exit keys preserved. |
| C05 | `A NEW ROLE` | S07 / primary | “As the front pair changed” → “another pair of limbs.” | 32.16–36.08 s → `[965,1082)` | Marks the turn from anatomy to significance without copying “defining weapon.” | 76 px target; alpha bbox `[239,181,703,325]`. | 4-frame fade and 0.055 upward travel into hold; 4-frame upward exit. |

The C03/C04/C05 values refer to each normalized cue's alpha bounds in its 941×1672 scene composite. C01/C02 use the previously checked v03 composites. The asset render and five actual assigned pairs are recorded in `CAPTION_RENDER_MANIFEST_v04.json` and `Source/Graphics/render_v04/manifest.json`; all five full-frame and phone-size pairs were visually inspected. New source glyph PNG provenance is under `Source/Graphics/accent_pngs_v01/`.

## Palmier placement

- **Baseline:** project `ACFE2102`, still Timeline 1 `5DFC7333`; the user-directed no-Grain state was preserved.
- **Current motion review target:** `Timeline 1 — motion-safe image revision v02`, timeline ID `CE143DE4`; still-source copy `684CA938`. Original baseline `5DFC7333` remains unchanged.
- **Accents track in current motion target:** `A67F8B4A`.
- Cue media remain unchanged. Current target clip IDs are C03 `70B20B80` `[0,101)`, C01 `0BB45473` `[398,468)`, C04 `E000C761` `[474,610)`, C02 `83345E97` `[797,962)`, and C05 `3CE40581` `[965,1082)`. Their phrase artwork and keyframes were copied with the scene revision. Palmier API readback rounds normalized values to three decimals. See `PALMIER_EDIT_LOG_20261102.md` and `Edit/ImageMotion/timeline_static_revision_receipt_v02.json`.
- Animation is applied to the paper phrase layers. Scene characters and individual paper parts remain static.

## Preflight and review evidence

- Static pair geometry: five actual scene/cue pairs rendered from accepted scene PNGs and actual authored cue PNGs; shared target face height 76 px. All five full composites and phone reductions were visually inspected. Primary anchor selected on S01, S03, S04, S07; the already accepted alternate remains on S06. No text crosses an animal, eye, weapon/limb detail or frame edge in those mockups.
- Current motion review export: `Edit/Previews/Paper Detour 035 Motion Safe Review v02.mp4`. H.264 1080×1920 / 30 fps, 44.166667 s; AAC mono 44.1 kHz at 64.4 kb/s. Full-file FFmpeg decode passed; the source soundtrack was retained unchanged.
- Current motion visual sampling: `Edit/ImageMotion/79fc35ac5f5e9a97be5e/qa/export/` contains five positions per scene and five positions per cue (entrance, hold, end and neighboring states). Every inspected frame keeps the story focal forms inside frame and cue text clear of the animals. This is sampled inspection, not frame-by-frame continuous proof.
- Pipeline receipt: `Edit/ImageMotion/79fc35ac5f5e9a97be5e/run.json` status `complete`; structure check `PASS`; source baseline and v01 motion branch preserved; target is a separate copy. Preset `framing-safe`, `depth_zoom=1.0`. Grain remains absent.
- **Still unverified:** full 1× playback/listening, audible cue sync and pronunciation, S09→S01 loop seam, last 0.08 s alignment overhang, device/platform Shorts UI safe zone, final delivery QA, and independent review. This is a motion review preview, not a final delivery export. No music/SFX were added; no upload/publication was made.
