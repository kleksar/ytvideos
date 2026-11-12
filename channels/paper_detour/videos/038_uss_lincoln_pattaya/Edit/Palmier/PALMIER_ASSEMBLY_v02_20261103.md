# Palmier assembly v02 — 2026-11-03

**Purpose:** static replacement-image review timeline; the user will add animation and inspect the result.

## Target and preservation

- Created separate Palmier project `Paper 038 USS Lincoln Pattaya Visual Assembly v02.palmier` through Palmier's Save As command. Source project v01 remains untouched.
- In the v02 copy, preserved the copied `Timeline 1`, saved a history snapshot before editing, and created a separate blank timeline. Renamed that timeline `Paper 038 Visual Assembly v02`.
- Palmier UI did not expose projectId or timelineId; target was verified by visible project path, project title and active timeline title.
- Project settings visibly remained 1080×1920, 30 fps, 9:16, Rec.709. Saved the project with Command-S and saved a history snapshot after assembly.

## Assembly

- Imported the 16 selected still images from `Source/Images/paper_v02/`; no sources were moved.
- Built 17 still clips in the following order, hard cuts with no gaps. S17 reuses the exact S01 source.

| Scene | Source | Duration |
|---|---|---:|
| S01 | `S01_v03.png` | 5.5 s |
| S02 | `S02_v03.png` | 5.0 s |
| S03 | `S03_v02.png` | 4.7 s |
| S04 | `S04_v02.png` | 4.1 s |
| S05 | `S05_v02.png` | 4.1 s |
| S06 | `S06_v02.png` | 4.3 s |
| S07 | `S07_v03.png` | 5.1 s |
| S08 | `S08_v02.png` | 5.9 s |
| S09 | `S09_v02.png` | 4.0 s |
| S10 | `S10_v03.png` | 5.0 s |
| S11 | `S11_v03.png` | 4.0 s |
| S12 | `S12_v02.png` | 5.4 s |
| S13 | `S13_v02.png` | 4.6 s |
| S14 | `S14_v03.png` | 5.2 s |
| S15 | `S15_v02.png` | 5.7 s |
| S16 | `S16_v02.png` | 4.0 s |
| S17 | `S01_v03.png` reused | 4.8 s |

**Total:** 81.4 seconds, 2,442 frames at 30 fps (`00:01:21:12`).

## Verification and limits

- Palmier's assembly agent reported exact placement and durations, and inspection of a composited sample from every still. The visible timeline showed the active v02 name, 81.4-second duration and the first three clip labels (`S01_v03`, `S02_v03`, `S03_v02`). The preview showed the selected S01 composition.
- Hard cuts only. No camera motion, animation, audio, captions, subtitles, transitions, export or publication were added.
- The image set remains pending user review; no independent image review has been completed. The active project is left open on the v02 review timeline for the user.
