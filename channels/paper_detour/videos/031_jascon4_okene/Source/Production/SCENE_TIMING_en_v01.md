# Scene timing draft — 031 Jascon-4 / Harrison Okene

**Status: SOURCE ALIGNMENT DRAFT — applied to v01; v02 timing changes are documented in [PALMIER_ASSEMBLY_en_v02.md](PALMIER_ASSEMBLY_en_v02.md). Current v03 scene-05 adjustment for the accepted paper cue is documented in [PALMIER_ASSEMBLY_en_v03.md](PALMIER_ASSEMBLY_en_v03.md).**

## Inputs and limits

- Channel: Paper Detour; English narration.
- Voice: `Source/Voice/voice_en.mp3`; measured duration 71.28 s.
- Alignment: `Source/Voice/voice_en.alignment.json`; 1,106 aligned characters match the English TTS text. The final alignment end is 71.36 s, 0.08 s beyond the MP3 duration.
- Image order and meaning: accepted 16-frame storyboard and the phrase mapping in `SCENE_MAPPING_EXTRA_HIGH_20261101.md`.
- Timing method: proposed direct cuts follow the measured character alignment and word boundaries. The timings below are coordinator-derived. A separate Extra High timing answer did not render in the ChatGPT interface; this grid is not presented as consultant-endorsed.
- On 2026-11-01, this grid was applied to Palmier timeline `D101EEBD` in project `8BE390BC` as rough cut v01. It was copied to timeline `7F5AA451`; several closing cut points were shifted slightly so every still lasts 4–6 seconds. See [PALMIER_ASSEMBLY_en_v01.md](PALMIER_ASSEMBLY_en_v01.md) and [PALMIER_ASSEMBLY_en_v02.md](PALMIER_ASSEMBLY_en_v02.md) for both frame maps and snapshots.
- No image, narration, storyboard, or voice file was changed. Neither timeline has received full 1× playback or human listening/synchronization review.

## Proposed 16-frame timing

| # | Accepted image | In → out | Duration | Spoken cue at/around the cut |
|---:|---|---:|---:|---|
| 01 | `01_search_wreck` | 00:00.00 → 00:05.76 | 5.76 s | Full opening line, ending on “sunken tugboat.” |
| 02 | `02_hand_contact` | 00:05.76 → 00:09.92 | 4.16 s | “He reached for a hand—and felt it grab him.” The cut out follows “still”; frame 03 begins on “alive.” |
| 03 | `03_survivor_found` | 00:09.92 → 00:14.96 | 5.04 s | “Alive in there. Could they bring him up?” then “To understand how he ended up inside…”; cut on “let’s go back.” |
| 04 | `04_tug_at_sea` | 00:14.96 → 00:20.08 | 5.12 s | Starts on “let’s go back,” continues through the date and “2013”; frame 05 begins just before “the tugboat sank.” |
| 05 | `05_depth_section` | 00:20.08 → 00:24.08 | 4.00 s | “The tugboat sank off the coast of Nigeria. There were twelve people on…”; cut at the start of “board.” |
| 06 | `06_divers_arrive` | 00:24.08 → 00:28.19 | 4.11 s | Starts on “board,” then “The divers had come to recover the bodies. By then…”; cut just after “then.” |
| 07 | `07_search_continues` | 00:28.19 → 00:32.40 | 4.21 s | “They had already brought up four. Harrison Okene, the ship’s cook…”; cut after “cook.” |
| 08 | `08_same_ship_missed_pass` | 00:32.40 → 00:37.20 | 4.80 s | “Was still inside the hull. The diver had not seen him on his first pass.” |
| 09 | `09_attempt_find` | 00:37.20 → 00:41.28 | 4.08 s | Starts after “first pass”; “According to Okene…” through “but returned”; cut after “returned.” |
| 10 | `10_air_pocket` | 00:41.28 → 00:45.36 | 4.08 s | Starts on “to the air pocket”; continues through “There was still an air pocket inside the hull.” |
| 11 | `11_depth_time` | 00:45.36 → 00:50.24 | 4.88 s | Full sentence: “Okene spent more than sixty hours in it, at a depth of about 30 metres.” |
| 12 | `12_preparation` | 00:50.24 → 00:54.08 | 3.84 s | “Now they had to get him out of the hull. They guided him to the diving…”; cut on the start of “bell.” |
| 13 | `13_diving_bell` | 00:54.08 → 00:57.92 | 3.84 s | Starts on “bell”; continues through “along a backup umbilical line. After he was brought up”; cut after “up.” |
| 14 | `14_decompression_chamber` | 00:57.92 → 00:61.68 | 3.76 s | “Okene was placed in a decompression chamber. Okene was the…”; cut just before “only.” |
| 15 | `15_surface_survivor` | 00:61.68 → 00:65.79 | 4.11 s | Starts on “only survivor”; continues through “The other eleven crew members died.” |
| 16 | `16_surface_to_wreck` | 00:65.79 → 00:71.28 | 5.49 s | Final line begins at 00:65.81: “The divers went down to search for bodies—and saved a man they never expected to find alive.” |

**Total:** 71.28 s. All 16 accepted stills are used in storyboard order. This original v01 map has three closing scenes at 3.76–3.84 s; v02 shifts the final cuts to keep every still within the requested 4–6 s range. The revised cut points are frame-rounded and require 1× review against the spoken words.

## Review notes before timing is treated as final

1. Listen to the English voice at 1×, especially the pronunciation of “Jascon-4” and “Okene”; technical ASR was inconclusive for both names.
2. Check the last 0.08 s of the alignment/file-duration discrepancy while listening; the proposed final image holds to the MP3 boundary at 71.28 s.
3. Review the current v03 sequence at 1× with audio before treating the timing as final. This document and sampled composited frames do not establish visual-audio sync QA.
