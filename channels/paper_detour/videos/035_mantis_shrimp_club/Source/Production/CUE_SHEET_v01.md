# Paper cue sheet v01 — Short 035

**Status:** narration v06 and Lawrence voice v01 were accepted by the user (“озвучка ок”, 2026-11-02). Static cue placements were accepted by coordinator. Scene-frame mapping, interface safe-zone overlay, motion, cue-to-voice playback and final MP4 remain `UNVERIFIED`.

**Narration:** accepted `NARRATION_EN_v06.txt`; English. Voice file `Source/Voice/en_v01_lawrence/voice_en.mp3`; script input omits only the service loop note. Character timing source: `Source/Voice/en_v01_lawrence/voice_en.alignment.json`. Alignment is automated; exact seconds below are not frame placement or playback-verified sync.

**Editorial decisions:** `CAPTION_DECISIONS_v01.md` (verbatim / complementary / no-text options recorded for every beat before PNG generation).

**Typography / scene mapping:** actual transparent imagegen PNGs are retained in `Source/Graphics/accent_pngs_v01/`; normalized cue layers used in the accepted static preflight are under `Source/Graphics/render_v03/cues/`. Reference: `channels/paper_detour/videos/001_radio_game/Source/Images/accent_typography_v2/A_MESSAGE.png`. `CAPTION_RENDER_MANIFEST_v03.json` and `Source/Graphics/render_v03/manifest.json` record inputs, hashes, bounds, scale, and coordinates. Canvas is 941 × 1672. Target common face-height is 76 px; actual measured maximum face-height is C01 76 px and C02 73 px (4% difference, within the one alternate zone's ±10% allowance). Both phrases use two authored lines.

| Cue | Text / PNG | Scene, cut and anchor | Spoken trigger → end | Time / source | Function and preselect review | Static geometry / visual check | Entrance / hold / exit |
|---|---|---|---|---|---|---|---|
| C01 | `THE` / `EXCEPTION`; `Source/Graphics/render_v03/cues/C01/cue.png` (source: `accent_pngs_v01/C01_THE_EXCEPTION_v01.png`) | S03; primary center `[0.50, 0.145]`; follows S02, cuts to S04. | “began to stand apart” → “the others.” | 13.28–15.60 s; character alignment, input-indexed. Seconds are preliminary; frame mapping and playback are `UNVERIFIED`. | Adds contrast after “broadly alike” without restating “front pair.” | 76 px max face-height, 2 lines; alpha bounds on 941 × 1672 canvas `[317,115,626,350]`. Full frame and 360 × 640 preview reviewed; clear of mantis shrimp, eyes, and action. Selected primary. | No movement specified. Preliminary static hold begins at semantic trigger and ends after spoken end; exact reveal/hold/exit, frame mapping, and scene cut remain `UNVERIFIED` pending timeline assembly and playback. |
| C02 | `PIERCE` / `≠ STRIKE`; `Source/Graphics/render_v03/cues/C02/cue.png` (source: `accent_pngs_v01/C02_PIERCE_NOT_EQUAL_STRIKE_v01.png`) | S06; alternate center `[0.68, 0.15]`; follows S05 spearer close-up, cuts to S07. Primary `[0.50,0.145]` rejected because it covers the eyes. | “its striking end” → “a powerful blow.” Do not reveal before the trigger. | 26.56–32.08 s; character alignment, input-indexed. Seconds are preliminary; frame mapping and playback are `UNVERIFIED`. | Links the preceding piercing close-up to the smasher's distinct function. | 73 px max face-height, 2 lines; alpha bounds `[469,174,812,331]`. Full frame and 360 × 640 preview reviewed; alternate avoids the eyes, club, and body. Right margin is preserved in the static mock. | No movement specified. Preliminary static hold begins at semantic trigger and ends after spoken end; exact reveal/hold/exit, frame mapping, and scene cut remain `UNVERIFIED` pending timeline assembly and playback. |

## No-text scenes

S01, S02, S04, S05, S07, S08 and S09 remain clear as recorded in `CAPTION_DECISIONS_v01.md`. S09's open sentence and hard cut back to S01 must stay unlettered.

## Preflight evidence and limits

- Contact sheet: `Source/Graphics/render_v03/CAPTION_CONTACT_SHEET_v01.png`; each selected full composite and its phone preview was inspected, as were the exact cue PNGs and face masks.
- Helper technical geometry: `PASS` for S03+C01 primary and S06+C02 alternate. The unselected S06 primary comparison overlaps the eye area and is not used.
- Visual text/scene collision: coordinator `PASS` for the two selected static placements; no animal, face, limb action or club detail is obscured. Text is readable in the supplied phone reduction.
- Platform Shorts UI safe-zone overlay was not supplied or tested. The phone mock has clear right-edge margin, but this does not prove platform safe-zone compliance; keep that check `UNVERIFIED` until checked against the actual release preview/interface.
- Automated character alignment now supplies provisional seconds; these values are not yet mapped to scene frames. Automated alignment is present; exact vocal emphasis/pronunciation and actual 1× playback are not independently reviewed. Cue-to-frame mapping, cue motion, playback sync, safe-zone UI, and actual MP4 review are `UNVERIFIED`. No import/edit or publication is authorized by this cue sheet.
