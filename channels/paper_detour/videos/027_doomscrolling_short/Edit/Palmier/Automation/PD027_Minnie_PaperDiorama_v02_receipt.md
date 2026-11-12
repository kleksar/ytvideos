# PD027 Minnie paper-diorama timeline receipt v02

**Date:** 1 November 2026  
**Project:** `Paper Detour 027 Minnie Freeman 20261101` — `7CDA44DD`  
**Timeline:** `PD027 Minnie Freeman paper diorama v02 20261101` — `B332DEEF`  
**Canvas:** 1080×1920, 30 fps, 1050 frames / 35 seconds.

## Assembly

The timeline follows script candidate v03 and uses the existing Lawrence voice file `Source/Voice/lawrence_minnie_v03_20261101/voice_en.mp3` (`CF78F82E`). No new voice, music, or SFX were generated. User approval for the existing VO was recorded earlier in this task.

| Track | Track ID | Content |
|---|---|---|
| V2 `Grain` | `5E2038DF` | Five contiguous clips from the existing 8-second ProRes grain source (`6B3E19C2`), 50% opacity, 0.342 left/right crop, full coverage `[0,1050)`. |
| V1 `Main` | `E1B86BE0` | Ten complete paper-diorama images and the exact S01 media reused at the end. Direct cuts only. |
| A1 `Dialogue` | `182A6627` | Existing VO media `CF78F82E`, `[0,1050)`. |

| Beat | Clip ID | MediaRef | Timeline frames |
|---|---|---|---:|
| S01 hook | `190C935F` | `63D117B3` | 0–173 |
| S02 door | `95C9BE56` | `1E8B4A98` | 173–300 |
| S03 windows | `11582729` | `38E41522` | 300–420 |
| S04 farmhouse distance | `874D1B00` | `3F9F580D` | 420–516 |
| S05 twine memory | `D0557891` | `1F865F62` | 516–626 |
| S06 wait | `D9129DC6` | `2A984944` | 626–716 |
| S07 roof gone | `A23E5359` | `6EEF61DB` | 716–780 |
| S08 crossing | `CC4606F4` | `3B2BD464` | 780–870 |
| S09 near loss | `A308BC78` | `C487425B` | 870–960 |
| S10 arrival | `9E5D7D12` | `5A7DC30D` | 960–1020 |
| S01 repeat | `61544078` | `63D117B3` | 1020–1050 |

## Verification and preview

- `get_timeline` confirmed eleven continuous, non-overlapping main clips, the exact S01 media reuse, a 35-second VO, and full grain coverage above the main track. Timeline is open in Palmier at frame 0.
- All ten source images have matching 941×1672 dimensions and show complete scenes. The contact sheet is `Source/Images/minnie_v05_paper_diorama/QA/CONTACT_SHEET_v01.jpg`.
- S09 was inspected at full size: twelve walkers in two six-child rows plus the youngest carried by Minnie. This was a coordinator check, not independent review.
- Palmier export: `Edit/Previews/PD027_Minnie_PaperDiorama_v02_20261101_render.mp4`.
- Review copy with audio encoded to AAC-LC: [`PD027_Minnie_PaperDiorama_v02_20261101_review.mp4`](../../Previews/PD027_Minnie_PaperDiorama_v02_20261101_review.mp4). `ffprobe`: H.264 1080×1920, 30 fps; AAC-LC mono 44.1 kHz (configured 192 kbit/s; measured average 157 kbit/s); 35.014 seconds. Full FFmpeg decode with `-xerror` passed. SHA-256: `ea4c7cdc0d7cd5c1e87ec5d5f7855821522d2dd7a3e8d8a3fd6675b6261fde43`.
- Representative frames from the rendered file are in `QA/PD027_Minnie_PaperDiorama_v02_render_contact.jpg`. A full 1× playback and human audio listening were not performed. No independent review, publication, or final `Deliverables` export is recorded.

The earlier `PD027_Minnie_FullStills_v01` render uses the superseded v04 images and must not be treated as the current visual version.
