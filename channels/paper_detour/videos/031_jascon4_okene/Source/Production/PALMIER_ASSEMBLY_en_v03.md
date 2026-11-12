# Palmier assembly receipt — 031 Jascon-4 / Harrison Okene — v03

**Status:** seven selected English paper accents applied to v03; full 1× audiovisual review and export are pending.

## Target and preservation

- Channel and language: Paper Detour, English.
- Palmier project: `Paper Detour 031 Jascon-4 Montage Draft 20261101`, project ID `8BE390BC`, file `/Users/diplomat/Paper Detour 031 Jascon-4 Montage Draft 20261101.palmier`.
- Current timeline: `031 Rough Cut v03 EN Paper Accents`, ID `9BB70406`, duplicated from v02 `7F5AA451`.
- Canvas and output: 1080×1920, 30 fps, Rec.709, 2139 frames (71.3 s).
- v02 and its snapshot `031_rough_cut_v02_20261101` (`B27119E9`) remain unchanged. v01 remains a separate timeline.
- Final v03 snapshot: `031_v03_after_cue_alignment_and_geometry_20261101` (`88B9F612`). Pre-correction snapshot: `031_v03_before_cue_alignment_corrections_20261101` (`716000D7`). Earlier safe points: pre-accent duplicate `B8EC1FAE` and post-initial-retime/pre-accent snapshot `37C9188F`.

## Scene edit

The selected cue `TWELVE PEOPLE ON BOARD` ends on “board” at 24.32 s. The cut after scene 05 was moved to frame 735 so its fade completes on that composition. The adjacent cuts were adjusted to retain 4–6 seconds per still; all remaining boundaries match v02.

| # | Still | Frames | Duration |
|---:|---|---:|---:|
| 01 | `01_search_wreck_v01` | 0–173 | 5.77 s |
| 02 | `02_hand_contact_v01` | 173–298 | 4.17 s |
| 03 | `03_survivor_found_v01` | 298–449 | 5.03 s |
| 04 | `04_tug_at_sea_v01` | 449–602 | 5.10 s |
| 05 | `05_depth_section_v01` | 602–735 | 4.43 s |
| 06 | `06_divers_arrive_v01` | 735–855 | 4.00 s |
| 07 | `07_search_continues_v01` | 855–975 | 4.00 s |
| 08 | `08_same_ship_missed_pass_v01` | 975–1116 | 4.70 s |
| 09 | `09_attempt_find_v01` | 1116–1238 | 4.07 s |
| 10 | `10_air_pocket_v01` | 1238–1361 | 4.10 s |
| 11 | `11_depth_time_v01` | 1361–1500 | 4.63 s |
| 12 | `12_preparation_v01` | 1500–1620 | 4.00 s |
| 13 | `13_diving_bell_v01` | 1620–1740 | 4.00 s |
| 14 | `14_decompression_chamber_v01` | 1740–1860 | 4.00 s |
| 15 | `15_surface_survivor_v01` | 1860–1980 | 4.00 s |
| 16 | `16_surface_to_wreck_v01` | 1980–2139 | 5.30 s |

## Accents and tracks

- `Accents`, video track ID `F5BC07D8`, index 0, composites above `Main`, track ID `A2502C4B`, index 1. The `Voice` audio track remains track ID `AECB4FC4`, index 2.
- Seven separate transparent PNGs from `Source/Images/accent_v01/` are present on `Accents`; exact cue text, alignment intervals, frame ranges, and animation keys are in [`PAPER_CUE_SHEET_en_v01.md`](PAPER_CUE_SHEET_en_v01.md).
- Only the cue PNGs animate. Each uses a 4-frame fade in, stable hold, and 4-frame fade out with a small vertical path. The image plates remain static and cuts remain direct.
- The cue `ONLY SURVIVOR` starts at frame 1852, eight frames before the scene 14→15 cut, because its spoken trigger `only` begins at 61.76 s. It enters on the decompression-chamber image, holds over the cut, and exits on the survivor image.
- No full subtitles, SRT/WebVTT, new sound, music, SFX, narration edit, or voice-speed change was added.

## Verification and limits

- `get_timeline` readback confirmed 16 contiguous stills, one unchanged English voice clip ending at frame 2139, and seven accent clips on the upper `Accents` track. Full structural readback is [`PALMIER_STATE_en_v03.json`](../../Edit/PALMIER_STATE_en_v03.json).
- Geometry was normalized with the explicit 1/2-line manifest: 90 px common face-height, 820.8 px safe line width, widest measured rendered cue 778.7 px; max cap-height readback error 0.4122 px; max optical-anchor error 0.0006593; all 7 IDs and preserved opacity curves passed the helper post-readback.
- Actual Palmier frame samples were visually checked at all seven cue holds and around the scene-05 cut and the scene-14→15 cue crossing. Contact sheets are in `Edit/accent_preflight_v01/timeline_reads_v03/`. The native inspection frames include Palmier’s coordinate-grid diagnostic overlay.
- Speech timing comes from `voice_en.alignment.json`; no on-ear cue-by-cue review or full 1× playback was performed. Phrase sync, uninterrupted visual comprehension, and final playback remain **UNVERIFIED**. No MP4 export, upload, or publication was performed.
