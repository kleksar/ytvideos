# PD027 Minnie full-stills timeline receipt v01 (ARCHIVE)

> **Superseded by [`PD027_Minnie_PaperDiorama_v02_receipt.md`](PD027_Minnie_PaperDiorama_v02_receipt.md).** This historical receipt records the v04 images, which read too realistically for the approved Paper Detour style. Palmier timeline `B332DEEF` was updated in place with the v05 paper-diorama stills and renamed to v02; use the newer receipt for current media references and preview.

**Date:** 1 November 2026  
**Project:** `Paper Detour 027 Minnie Freeman 20261101` — `7CDA44DD`  
**Timeline:** `PD027 Minnie Freeman full stills v01 20261101` — `B332DEEF`  
**Canvas:** 1080×1920, 30 fps, 1050 frames / 35 seconds.

## Assembly

The timeline uses the English candidate v03 and existing Lawrence voice file `Source/Voice/lawrence_minnie_v03_20261101/voice_en.mp3` (`CF78F82E`, 34.96 seconds). No new voice, music, or effects were generated.

| Track | Track ID | Content |
|---|---|---|
| V2 `Grain` | `5E2038DF` | Five contiguous clips from the existing 8-second ProRes grain source, 50% opacity, full vertical cover crop (0.342 from each horizontal edge); total [0,1050). |
| V1 `Main` | `E1B86BE0` | Ten complete full-frame stills plus the exact S01 media reused at the end. Direct cuts only. |
| A1 `Dialogue` | `182A6627` | Existing Minnie v03 VO at frame 0 through frame 1050. |

| Beat | Clip ID | MediaRef | Timeline frames |
|---|---|---|---:|
| S01 Hook | `190C935F` | `F2928ABB` | 0–173 |
| S02 Door | `95C9BE56` | `1B7F0393` | 173–300 |
| S03 Windows | `11582729` | `4B7D1282` | 300–420 |
| S04 Farmhouse distance | `874D1B00` | `F1A8D026` | 420–516 |
| S05 Twine memory | `D0557891` | `15E88638` | 516–626 |
| S06 Wait | `D9129DC6` | `9A8EA410` | 626–716 |
| S07 Roof gone | `A23E5359` | `995B3943` | 716–780 |
| S08 Crossing | `CC4606F4` | `B80627BE` | 780–870 |
| S09 Near loss v02 | `A308BC78` | `0C8354A1` | 870–960 |
| S10 Arrival | `9E5D7D12` | `1DBC8C4C` | 960–1020 |
| S01 repeat | `61544078` | `F2928ABB` | 1020–1050 |

S07 is 64 frames (2.13 seconds) and S10 is 60 frames (2 seconds). These short holds preserve the spoken roof-loss and farmhouse-arrival turns; they are deliberate beats in this assembly rather than accidental gaps. The final second reuses the exact S01 media as the VO trails off on “connected by—”.

## Verification

- `get_timeline` confirmed 11 continuous, non-overlapping main clips, grain and dialogue coverage from frame 0 to 1050, and V2 Grain above V1 Main.
- Independent reviewer verified the scene order, exact S01 media reuse, S09 v02, voice placement, grain crop/opacity, full coverage, and absence of doomscrolling assets from this timeline.
- Independent still review passed S09 v02: twelve walking children are individually countable in two rows of six, plus the youngest carried by Minnie.
- Sampled Palmier inspector frames at 0, 236, 360, 468, 570, 671, 748, 825, 915, 990 and 1035 are in [`QA/PALMIER_INSPECTION_v02.jpg`](QA/PALMIER_INSPECTION_v02.jpg). Inspector frames include a diagnostic grid/burn-in; they are not clean master frames.
- S04's view of the farmhouse from inside the school is an illustrative spatial reconstruction. The script confirms the nearest farmhouse was three-quarters of a mile away; a sightline from the classroom is not documented.

Full playback at normal 1× speed, audio listening, and grain seam continuity remain unverified. The timeline is open in Palmier for review. No MP4 export or publication was made in this assembly pass.
