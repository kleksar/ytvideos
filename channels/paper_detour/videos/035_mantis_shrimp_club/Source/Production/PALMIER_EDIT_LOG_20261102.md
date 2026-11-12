# Palmier edit log — 2026-11-02

## Target

- Project: `Edit/Paper Detour 035 Mantis Shrimp Evolution v01.palmier/`
- Timeline: `Timeline 1`
- Settings read in Palmier: 1080×1920, 9:16, 30 fps, Rec.709.
- Separate project instance was used for 035. The existing 036 project was left untouched.
- Snapshot: `035 — assembled with cues, pre-export` (a second snapshot with this same label is also present).

## Assembly readback

- Main scene track, frame ranges: S01 `[0,122)`, S02 `[122,352)`, S03 `[352,474)`, S04 `[474,612)`, S05 `[612,763)`, S06 `[763,965)`, S07 `[965,1090)`, S08 `[1090,1241)`, S09 `[1241,1325)`.
- Track order: Accents above Grain above Main; Voice on its own track.
- Timeline: 1325 frames = 44.1667 s at 30 fps. Direct cuts, no transitions.
- Grain: six consecutive copies `[0,240)`, `[240,480)`, `[480,720)`, `[720,960)`, `[960,1200)`, `[1200,1325)`; last source segment begins at frame 0; opacity 25%.
- Voice clip: `[0,1325)`. No audio edits were made.

## Accent placement entered in Palmier

Palmier readback rounds position values to three decimal places and does not expose the original source paths. Exact decimal values below are the values submitted; clip and media IDs were read back.

| Cue | Media ID | Clip ID | Timeline frames | Normalized size W×H | Position keys (clip-relative frame, x, y) | Opacity keys |
|---|---|---|---|---|---|---|
| C01 | `96CFFBBF` | `6F62FA9A` | `[398,468)` | `0.33475 × 0.20574` | `(0,.332,.09447)`, `(4,.332,.03947)`, `(65,.332,.03947)`, `(69,.332,.01947)` | `(0,0)`, `(4,1 hold)`, `(65,1)`, `(69,0)` |
| C02 | `AC75C5A6` | `6C30AA00` | `[797,962)` | `0.38257 × 0.12141` | `(0,.48778,.10493)`, `(4,.48778,.08493)`, `(160,.48778,.08493)`, `(164,.48778,.06493)` | `(0,0)`, `(4,1 hold)`, `(160,1)`, `(164,0)` |

Both cues were matched by artwork and crop dimensions against `Source/Graphics/render_v03/cues/C01/cue.png` and `.../C02/cue.png`. Timeline captures were inspected at frames 400/402/465 for C01 and 799/801/959 for C02. Each cue stayed inside frame and clear of the eye, animal and action in those samples. This is sampled composite inspection, not full playback review.

## Export status

- A first attempt was interrupted by Save-panel focus loss. The project was reopened by its exact path before continuing.
- A static review preview was then exported to `Edit/Previews/Paper Detour 035 Mantis Shrimp Evolution Static Review v01.mp4` using Video / H.264 / MPEG-4, match timeline (1080×1920), 30 fps, Rec.709.
- `ffprobe`: 44.166667 s, H.264 1080×1920 at 30 fps; AAC mono, 44.1 kHz, measured 64,389 bit/s. Full-file FFmpeg decode completed without error. The AAC bitrate is below the delivery target; this is only a review preview, not final delivery.
- No full playback, loop seam, final audio-tail check, or AV review has been completed. User review is pending.
- No upload or publication is authorized by this log.

## User-directed cleanup — 2026-11-02

- Before cleanup, Palmier saved snapshot `2F23A38D`, “035 — before removing grain and QA renders”.
- Through Palmier-managed project operations, removed Grain track `A280E97A` with clips `87A9853C`, `A159FA09`, `18DBB824`, `CD823C2D`, `5EF41611`, `8C6599A3`, plus media entry `8B31B7A0`.
- Removed the six temporary QA still entries from the active project media inventory: `9206E03E`, `1F66117B`, `7AF1BB8D`, `ED818418`, `454FBF29`, `CBEA8A32`.
- Re-read Timeline 1 `5DFC7333`: Main, Accents, Voice remain; scene/cue/audio timing and project settings are unchanged; duration remains 1325 frames. Current media inventory contains the nine scene PNGs, accepted voice, and two cue PNGs.
- Palmier removed the QA media entries but left their six generated project-local files under `media/frame-*.png`. They are no longer in the active media inventory; one rendered QA image is also embedded in Palmier chat history. No manual `.palmier` changes or filesystem deletions were performed. The shared grain source file and source PNGs remain intact.
- Per the user’s current direction, grain is intentionally absent from this episode timeline. This is a release-specific override of the usual Paper grain requirement. The forthcoming scene-motion step is deferred until the user has reviewed the static preview; use a separate motion target from this baseline and do not restore Grain.

## Expanded accent set and motion branch — 2026-11-02

- **Editorial source:** coordinator-created `CAPTION_DECISIONS_v02.md`, at the user's explicit direction to continue without Extra High. The failed Extra High consultation remains recorded in `CONSULTATIONS_20261102.md`; no recommendation is attributed to it.
- **New glyph assets:** C03 `ONE LIMB. / TWO WEAPONS?`, C04 `SEPARATE PATHS`, C05 `A NEW ROLE`; transparent imagegen PNGs retained under `Source/Graphics/accent_pngs_v01/`. Normalized assets and all five assigned pair mockups are in `Source/Graphics/render_v04/`; each full and phone composite was visually checked.
- **Snapshot before edits:** `FE1510AF`, “035 — before expanded cue set”.
- **Timeline edits:** added C03 media `4CC5E96E` / clip `1A3655A2` frames `[0,101)`; C04 media `AE45994D` / clip `08A650FD` frames `[474,610)`; C05 media `37A7A598` / clip `E6B6B615` frames `[965,1082)`. Track `Accents` (`86F0655B`). The app reported exact geometry accepted and position/opacity keys applied; readback rounded geometry to three decimals. C01/C02, Main, Voice, settings, and source Timeline 1 were read back unchanged. Grain stayed absent. See the Palmier conversation and `CUE_SHEET_v02.md` for submitted geometry/keyframes.
- **Motion branch:** baseline source project `ACFE2102`, Timeline 1 `5DFC7333`; target timeline `B2535318` (`Timeline 1 — image motion`). Pre-edit snapshot `43356E9D`, “Batch image motion verified”. Nine scene clips were replaced by validated whole-image motion videos; Accents and Voice were preserved. Preset `gentle-aligned`; camera `auto`; `depth_zoom=1.03` per scene. No part of a paper creature was animated.
- **Automation receipts:** `Edit/ImageMotion/0bf2c9d6888bcf57bcb7/` includes plan, before/after target, receipts, schemas, renderer logs, scene hashes and `run.json`. Status `complete`; `timeline_structure=PASS`; full playback remains `UNVERIFIED`. Depth maps and motion videos are cached in `Shared/Image_Motion/Cache/`.
- **Review export:** `Edit/Previews/Paper Detour 035 Mantis Shrimp Evolution Motion Review v01.mp4`, Video/H.264/MP4, match timeline, 30 fps, Rec.709. `ffprobe` reports 1080×1920, 44.166667 s, AAC mono 44.1 kHz at 64,389 bit/s; full FFmpeg decode passed. This is a review preview, not final delivery.
- **Initial visual QA (superseded):** `Edit/ImageMotion/0bf2c9d6888bcf57bcb7/qa/motion_scene_contact_sheet.png` sampled start/middle/end. It was too sparse and did not identify important subject parts crowding or leaving frame edges in S01/S04/S08 and close-up S05/S06. The user's report exposed this gap; see the motion-safe image revision section below. Full audio playback, loop seam, spoken cue sync, platform safe-zone and independent review remained unverified; no publication/upload.

## Motion-safe image revision v02 — 2026-11-02

- **Reason:** user reported that subjects were leaving the screen under zoom, horizontal/vertical movement and parallax. Current documentation already has an explicit motion-safe composition gate; this pass found the previous images had been checked as stills, while motion review only sampled start/middle/end. S01/S04/S08 and close-ups S05/S06 were too tight under the actual camera/depth path.
- **Protected baseline:** saved snapshot `192DF47A` (“035 — before motion-safe image revision v02”) on original Timeline 1 `5DFC7333`; the original timeline was not modified. Cloned still source `Timeline 1 — motion-safe stills v02` `684CA938`; snapshot before swapping source stills `6B4222B2`. Readback preserved Accents (5 clips), Main (9) and Voice (1), 1080×1920/30 fps.
- **Image selection:** imported S01_v02, S02_v02, S03_v02, S04_v03, S05_v02–S09_v02 from `Source/Images/paper_v02/`. Replaced only the nine scene stills on the isolated still-source copy; retained all cue clips, cue media, voice clip, interval boundaries, and no-Grain state. S04_v02 was rejected after pre-import motion render still showed side-edge crowding; S04_v03 passed the repeated five-point check. Exact image hashes, prompts, generation IDs and inspected details are in `Source/Images/paper_v02/GENERATION_LOG_v02.md`.
- **Motion plan:** rendered from the still-source copy into a new target `Timeline 1 — motion-safe image revision v02` `CE143DE4`. Snapshot after structural verification `6E2B3F1D`. Profile `framing-safe`; per-scene camera modes: push-in, push-in, pan-right, push-in, pull-out, pull-out, pan-left, pan-right, push-in; all scene `depth_zoom=1.0`. Tracks Accents/Main/Voice and timing/settings read back intact; Grain absent. Run `Edit/ImageMotion/79fc35ac5f5e9a97be5e/run.json`: `status=complete`, `timeline_structure=PASS`, `full_playback=UNVERIFIED`. Source mapping and receipts: `sources_v02.json`, `motion_v02.json`, `timeline_static_revision_receipt_v02.json` in `Edit/ImageMotion/`.
- **Export:** `Edit/Previews/Paper Detour 035 Motion Safe Review v02.mp4`, H.264, 1080×1920, 30 fps, 44.166667 s; AAC mono 44.1 kHz at 64,389 bit/s. `ffprobe` stream/format inspection passed; complete FFmpeg decode passed. This is a review preview, not the final local deliverable. The existing voice was preserved; no audio was generated or changed intentionally.
- **Framing evidence:** rendered before import and inspected five points (first, quarter, middle, three-quarter, last) for each scene. Re-rendered S04_v03 and inspected the same five points. In the export, inspected five scene positions per scene and five entrance/hold/exit positions per cue using `Edit/ImageMotion/79fc35ac5f5e9a97be5e/qa/export/`. At inspected frames the animals' narrative focal parts remain inside frame, no empty image edges appear, and captions remain legible and separated from action. This is sampled visual QA; no claim of frame-by-frame inspection or independent review.
- **Not completed:** full 1× listening/playback, audible cue sync, last spoken endpoint and loop seam, Shorts UI safe-zone, independent review and final delivery QA. No upload/publication.

## Motion-safe preview final QA — 2026-11-02

- User replied “гуд” after the motion-safe review preview and proposed QA/export next step; treated as direction to proceed. No new image or timeline edit was made after snapshot `6E2B3F1D`.
- Exact export target re-read in Palmier: project `ACFE2102`, timeline `CE143DE4` (`Timeline 1 — motion-safe image revision v02`), H.264/MP4, Match Timeline 1080×1920, 30 fps, Rec.709, 1325 frames / 44.166667 s. No new render was submitted because the native Save dialog stopped responding before path submission; no file was written to `Deliverables`.
- Existing review preview SHA-256 `cdb99ded49513d86e4b2ed1bce26dd175cabc5ce7042497943921a15489c131e`; bound to the above timeline and motion snapshot. Contract: `Edit/Export/EXPORT_CONTRACT_v01.json`.
- QA helper: stream metadata and full decode `PASS`; 1325 video frames, H.264 High / yuv420p / bt709 limited progressive, AAC-LC mono 44.1 kHz; measured video bitrate ≈10.24 Mbps, audio sample peak −2.9 dBFS and mean −24.7 dBFS. Source/export decoded audio correlation peaked at 0.946 at an estimated 13 ms lag; no listening was performed.
- All 75 frames requested by the QA plan were viewed in contact sheets at about 20% width across scene motion samples, cue entry/hold/exit/last states, all eight cut edges and cue boundaries. In those samples, focal objects and accent PNGs remain in frame and separated. Full-resolution individual inspection of consequential anatomy/glyph detail remains outstanding. S09’s designed close-up crops the rear body at the right edge; forebody and weapon remain visible. Motion between sampled frames, speech sync/listening, loop seam and independent review remain unverified.
- Channel pacing policy failed: S02 230 frames / 7.667 s, S06 202 / 6.733 s, S09 84 / 2.800 s; Paper range is 4–6 s per scene. Current receipt: `Edit/QA/final-qa-v01/reviewer_receipt_v02.json`; helper output: `Edit/QA/final-qa-v01/helper/report.json`. Overall `FAIL`; do not promote the preview as the final delivery. Timing/storyboard must be revised, then dependent motion/cue and final export QA repeated. User’s “гуд” does not waive this channel requirement.
