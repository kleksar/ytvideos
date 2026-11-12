# Paper cue sheet — 031 Jascon-4 / Harrison Okene — EN v01

**Status:** seven selective paper accents applied to Palmier v03. Full 1× audiovisual review remains **UNVERIFIED**; no export was made.

## Accepted scope and inputs

- Channel: Paper Detour; English narration.
- User selected **only paper accents in frame**. Full visible subtitles and an SRT/WebVTT sidecar are outside this pass.
- Recording: [`voice_en.mp3`](../Voice/voice_en.mp3); text source: [`voice_en_tts_v01.txt`](../Voice/voice_en_tts_v01.txt), translated from the accepted script in [`ENGLISH_TRANSLATION_EXTRA_HIGH_v01.md`](../Voice/ENGLISH_TRANSLATION_EXTRA_HIGH_v01.md); timing source: [`voice_en.alignment.json`](../Voice/voice_en.alignment.json). Audio speed and content were not changed.
- Selection consultation: coordinator checked the visible `Extra High` label in Chrome immediately before the request. The complete prompt and response are preserved in [PAPER_CUE_SELECTION_EXTRA_HIGH_20261101.md](PAPER_CUE_SELECTION_EXTRA_HIGH_20261101.md); [project chat](https://chatgpt.com/g/g-p-6ae147d3975481919b5bfda6935777d0-yt-video/c/6ae7adff-4824-83ed-9e5b-cf5570ed3700). The first table response was truncated; a focused follow-up returned the complete seven-cue review. It confirmed the suspense order and made three corrections: display the four-word crew count without a slash, end `AIR POCKET` on `pocket`, and time `ONLY SURVIVOR` from `only` through `survivor`.
- Exact assets are in [`Source/Images/accent_v01/`](../Images/accent_v01). `A02_TWELVE_PEOPLE_ON_BOARD.png` is a two-line layout (`TWELVE PEOPLE` / `ON BOARD`); the slash in earlier notes was only a line-break marker, not printed artwork.

## Cue map

Alignment times are word boundaries in seconds. Clip ranges are half-open `[startFrame, endFrame)` at 30 fps. The clip starts on the floor-rounded trigger frame with opacity 0; its first visible frame follows the trigger. The final word ends before the four-frame fade-out begins. The clip end is five frames after the fade-out start so the last keyframe reaches zero on `endFrame − 1`.

| ID / PNG | Scene and exact displayed words | Spoken trigger → end | Alignment seconds | Palmier clip frames | Narrative function and pair preflight |
|---|---|---|---:|---:|---|
| A01 — `A01_GRAB_HIM.png` | `02_hand_contact` — **GRAB HIM** | `grab` → `him` | 7.920–8.480 | `[237,260)` | Sudden physical contact. Scene + PNG full-frame entry/hold/exit composites and phone reduction: PASS. |
| A02 — `A02_TWELVE_PEOPLE_ON_BOARD.png` | `05_depth_section` — **TWELVE PEOPLE**<br>**ON BOARD** | `twelve` → `board` | 23.160–24.320 | `[694,735)` | Establishes the scale of the disaster. Two lines preserve the four consecutive spoken words. Cue and its fade finish before the revised cut at frame 735. Pair preflight: PASS. |
| A03 — `A03_BROUGHT_UP_FOUR.png` | `07_search_continues` — **BROUGHT UP FOUR** | `brought` → `four` | 28.960–30.320 | `[868,915)` | Makes the recovery count a suspense beat. Pair preflight: PASS. |
| A04 — `A04_STILL_INSIDE.png` | `08_same_ship_missed_pass` — **STILL INSIDE** | `still` → `inside` | 32.800–33.440 | `[984,1009)` | Holds the unresolved fact that Okene remains inside the hull. Pair preflight: PASS. |
| A05 — `A05_AIR_POCKET.png` | `10_air_pocket` — **AIR POCKET** | second `air` in “There was still an air pocket inside the hull” → `pocket` | 43.520–44.000 | `[1305,1325)` | Highlights the survival condition without extending the phrase into the rest of the sentence. Pair preflight: PASS. |
| A06 — `A06_SIXTY_HOURS.png` | `11_depth_time` — **SIXTY HOURS** | `sixty` → `hours` | 46.640–47.360 | `[1399,1426)` | Gives the survival duration one clear emphasis. Pair preflight: PASS. |
| A07 — `A07_ONLY_SURVIVOR.png` | `15_surface_survivor` — **ONLY SURVIVOR** | `only` → `survivor` | 61.760–63.080 | `[1852,1898)` | Final reveal and contrast with the rest of the crew. The clip begins in the last 8 frames of `14_decompression_chamber` and holds across the cut into `15_surface_survivor`; neither word is shown before its spoken trigger. Both scene/PNG pairs pass. |

## Geometry and animation

- Canvas: 1080×1920, 30 fps. Primary optical face-center on hold: `(0.50, 0.18)`; common cap height: 90 px. Entry centerY: `0.20`; hold: `0.18`; exit: `0.16`. No alternate anchor was needed.
- Safe width ratio: `0.76` (820.8 px). Widest line: `BROUGHT UP FOUR`, 778.7 px after Palmier normalization. All phrases preserve the same optical cap height within raster/transform rounding.
- Motion on the separate `Accents` track: keyframes relative to each clip at `0`, `4`, `D−5`, `D−1`; opacity `[0, 0] → [4, 1, hold] → [D−5, 1] → [D−1, 0]`; position moves entry → hold → exit using the same x and scale. The paper dioramas remain static.
- Helper application report: [`placement_plan_v02.json`](../../Edit/accent_preflight_v01/placement_plan_v02.json). Palmier readback error: max cap-height difference 0.4122 px; max optical-anchor error 0.0006593; all 7 clip IDs present; opacity curves preserved.

## Visual evidence

- Each of the seven original scene/PNG pairs was reviewed as a full-frame and phone-size composition at entry, hold, and exit. Contact sheets and full-resolution composites are in [`Edit/accent_preflight_v01/`](../../Edit/accent_preflight_v01).
- Cue A07 crosses into scene 14 before the cut because its spoken trigger `only` begins before scene 15. Final-size pair composites over the decompression-chamber still are [`entry`](../../Edit/accent_preflight_v01/A07_ONLY_SURVIVOR_scene14_entry_final.png) and [`hold`](../../Edit/accent_preflight_v01/A07_ONLY_SURVIVOR_scene14_hold_final.png); phone-size checks are [`entry`](../../Edit/accent_preflight_v01/A07_ONLY_SURVIVOR_scene14_entry_final_phone.jpg) and [`hold`](../../Edit/accent_preflight_v01/A07_ONLY_SURVIVOR_scene14_hold_final_phone.jpg). Its exit occurs only on scene 15.
- Palmier `inspect_timeline` sample sheets: [`cue holds`](../../Edit/accent_preflight_v01/timeline_reads_v03/contact_cue_holds.jpg) and [`entry, fades, and cuts`](../../Edit/accent_preflight_v01/timeline_reads_v03/contact_entry_exit_cuts.jpg). Palmier adds a diagnostic coordinate grid to these inspection renders; it is not part of the source images or accent PNGs.
- Timeline structure and keyframes are saved in [`PALMIER_STATE_en_v03.json`](../../Edit/PALMIER_STATE_en_v03.json). These visual checks cover selected static frames and cut boundaries; they do not replace playback.

## Verification limits

- Timing is alignment-derived and frame-rounded. No one has listened to each cue at 1× or watched the complete assembled video with sound; phrase sync and full playback remain **UNVERIFIED**.
- No MP4 was rendered, and no upload or publication occurred.
