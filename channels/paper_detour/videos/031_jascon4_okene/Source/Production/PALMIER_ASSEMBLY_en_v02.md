# Palmier assembly receipt — 031 Jascon-4 / Harrison Okene — v02

**Status:** current rough cut v02 assembled 2026-11-01; pending full 1× audiovisual review.

## Target

- Channel and language: Paper Detour, English.
- Palmier project: `Paper Detour 031 Jascon-4 Montage Draft 20261101`, project ID `8BE390BC`, path `/Users/diplomat/Paper Detour 031 Jascon-4 Montage Draft 20261101.palmier`.
- Timeline: `031 Rough Cut v02 EN 4-6s`, ID `7F5AA451`, copied from v01 `D101EEBD` so the previous assembly remains intact.
- Settings: 1080×1920, 30 fps, Rec.709; total 2139 frames (71.3 s).
- Snapshot before the v02 duration adjustment: `031_v02_before_duration_adjustment`, ID `214AEF1C`.
- Saved v02 snapshot: `031_rough_cut_v02_20261101`, ID `B27119E9`.
- Previous rough cut v01 remains as timeline `D101EEBD`, snapshot `031_rough_cut_v01_20261101` (`11C21216`).

## Assembly

- Main video track `9332C084` contains all 16 accepted still dioramas in storyboard order, on one continuous track with direct cuts and no gaps.
- Voice track `DCD6FEA6` contains `voice_en.mp3` from frame 0 through frame 2139. Palmier's media catalog reports 71.314 s; the 30 fps timeline resolves the clip to 2139 frames (71.3 s). The source timing worksheet records 71.28 s, so the final frame boundary should be checked during playback.
- Frame ranges are half-open `[start, end)`. The first ten scene cut points follow the source alignment grid; the boundary after scene 11 and the closing block were adjusted to keep every still within the requested 4–6 s range:

| # | Still | Frames | Approx. duration |
|---:|---|---:|---:|
| 01 | `01_search_wreck_v01` | 0–173 | 5.77 s |
| 02 | `02_hand_contact_v01` | 173–298 | 4.17 s |
| 03 | `03_survivor_found_v01` | 298–449 | 5.03 s |
| 04 | `04_tug_at_sea_v01` | 449–602 | 5.10 s |
| 05 | `05_depth_section_v01` | 602–722 | 4.00 s |
| 06 | `06_divers_arrive_v01` | 722–846 | 4.13 s |
| 07 | `07_search_continues_v01` | 846–972 | 4.20 s |
| 08 | `08_same_ship_missed_pass_v01` | 972–1116 | 4.80 s |
| 09 | `09_attempt_find_v01` | 1116–1238 | 4.07 s |
| 10 | `10_air_pocket_v01` | 1238–1361 | 4.10 s |
| 11 | `11_depth_time_v01` | 1361–1500 | 4.63 s |
| 12 | `12_preparation_v01` | 1500–1620 | 4.00 s |
| 13 | `13_diving_bell_v01` | 1620–1740 | 4.00 s |
| 14 | `14_decompression_chamber_v01` | 1740–1860 | 4.00 s |
| 15 | `15_surface_survivor_v01` | 1860–1980 | 4.00 s |
| 16 | `16_surface_to_wreck_v01` | 1980–2139 | 5.30 s |

This retiming moves the start of scene 12 0.24 s earlier than the source timing grid and the start of scene 16 0.19 s later; the intervening scenes are evenly held at 4.0 s. Confirm these small shifts feel natural against the spoken phrases during playback. No narration speed changes, motion, transitions, captions, music, or SFX were added.

## Verification and limits

- `get_timeline` readback confirmed 16 contiguous still clips on Main and one narration clip on Voice, all ending at frame 2139.
- Composited frames were inspected at 0, 1560, 1680, 1800, 1920, and 2070. The expected opening, preparation, diving-bell, decompression-chamber, survivor, and closing images appeared on the corresponding clip IDs. This was a sampled visual check; it does not verify every frame or audio sync.
- No full timeline playback, human listening review, export, upload, or publication was performed.
