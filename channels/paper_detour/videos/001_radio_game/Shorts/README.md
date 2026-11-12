# Rarovista 001 — Shorts production

# Review batch — updated Shorts, 2 November 2026

| Short | Review file / delivery | Status |
|---|---|---|
| 01 — Software You Could Tape Off the Radio | [v04 subtitle review MP4](01_radio_signal/Work/short01_subtitles_20261102_v02/previews/short01_subtitles_full_v04_group_v02_review.mp4) | Visual QA PASS on 279 frames; targeted motion-framing PASS on 81 unique frames across all six scenes. Overall UNVERIFIED pending audible subtitle sync. Original narration/AAC unchanged. [Receipt](01_radio_signal/Edit/QA/short01_motion_review_20261102_v01/reviewer_receipt_v02_motion.json). |
| 02 — The Radio Recording That Played Too Fast | [v04 accent motion review MP4](02_decoder/Work/short02_accent_motion_fix_20261102_v01/previews/PAPER_DETOUR_001_SHORT02_ACCENT_MOTION_REVIEW_20261102_v04.mp4) | Technical metadata/full decode PASS; accent entry/hold/exit visually PASS on samples from all nine cues. Overall UNVERIFIED pending audible subtitle sync. Voice/A1 unchanged; AAC packets stream-copied from v03. [QA report](02_decoder/Edit/QA/short02_accent_motion_fix_20261102_v01/technical/report.json); [motion frame review](02_decoder/Edit/QA/short02_accent_motion_fix_20261102_v01/technical/c01_entry_exit_frames.jpg). |
| 03 — The Radio Broadcast You Could Read | [current v01 delivery](03_stereo_text/Deliverables/PAPER_DETOUR_001_SHORT03_STEREO_EN_REWORK_20261102_v01.mp4) | QA PASS; user confirmed subtitle highlight sync on the full review. Release record says the replacement is public and processed. [QA](03_stereo_text/Edit/rework_20261102/FINAL_QA_v01.json), [release readback](03_stereo_text/Packaging/Metadata/RELEASE_STATE_20261102.json). |
| 04 — Can a radio show be followed without hearing it? | [text draft](04_computer_text/Script.md) | Text only; no approved voice/video exists, so it is outside the existing-video reupload batch. |

Shorts 01 and 02 remain local review candidates; no new upload, promotion, deletion, or cleanup was done in this subtitle pass. Their automatic alignments are timing evidence, not proof of spoken sync. Short 02's animated accent entrance, hold and exit now pass the targeted visual check; its spoken subtitle sync remains unverified. Short 03 is already complete.


## Supporting Short candidate — computer text for a radio programme

A separate text-only supporting Short draft is at [04_computer_text/Script.md](04_computer_text/Script.md). It is about the late-1980s computer-text accessibility initiative and remains distinct from the Japanese-community FM-stereo broadcast and MSX Avenger stories. Extra High fact-check and editorial review are recorded in the script file. Status: awaiting user acceptance; no audio or video has been created.

The three scripts were reviewed and revised with [ChatGPT Pro](https://chatgpt.com/c/6ae3aef8-7cb8-83eb-9c3e-dbd499983f05) on 30 October 2026. The complete Pro response contains separate creative direction and its source links; public descriptions below intentionally omit source links. The longer film is still in production; do not invent a link to it.

## 01 — Software You Could Tape Off the Radio

Narration: `01_radio_signal/narration_pro_v2.txt`. A record button and cassette illustrate how audio could carry a program; the archive dates its own MSX-related copy to 1987. Visual treatment is schematic, not a demonstrated launch at a listener's home.

Description: A record button could capture more than music. Follow an illustrated explanation of software delivery by radio, with Brazil's Clip Informática as the historical example. #ComputerHistory #RadioHistory #MSX

Source: [Datassette](https://datassette.org/pt-br/softwares/diversos/audios/br-brasil/clip-informatica-especial-numero-102).

## 02 — The Radio Recording That Played Too Fast

Narration: `02_decoder/narration_pro_v2.txt`. A quiet, accelerated online recording leads to Weber Kai's decoder instructions and his reported match to Avenger. His instructions describe six output files, not six individually established matches. We have not reproduced the comparison or observed the game running. The identity of his recording and Datassette's copy has not been established.

Description: What program did this radio recording carry? Explore Weber Kai's decoding procedure and the match he reported. #DigitalPreservation #MSX #ComputerHistory

Source: [Weber Kai's decoder README](https://github.com/weberkai/msx-tape-read#the-big-challenge-r%C3%A1dio-usp---clip-inform%C3%A1tica---episode-102).

## 03 — The Radio Broadcast You Could Read

Narration: `03_stereo_text/narration_pro_v2.txt`. A separate 1988 FM stereo broadcast carried Portuguese speech and encoded Japanese text on separate channels; a connected computer could decode and display the text. This is not the same broadcast as the MSX story and is not evidence of real-time machine translation.

Description: One radio message, two ways to receive it: listen in Portuguese or read in Japanese. #RadioHistory #ComputerHistory #TechnologyHistory

Source: [Superinteressante, 31 August 1988](https://super.abril.com.br/comportamento/computador-fm/).

## Shorts cover API readback — 1 November 2026

On Paper Detour channel `UCMVfdfaNxV3ZkI3_J3Eejzw`, the following local PNG
covers were set with YouTube Data API and read back as `matched`:

- `01_radio_signal`: video `85dwIXy_lZs`,
  [`program-on-tape-concept.png`](01_radio_signal/Packaging/Thumbnails/program-on-tape-concept.png).
- `02_decoder`: video `7DygREwtxfY`,
  [`short_cover_game_in_static_20261031.png`](02_decoder/Edit/publication_20261031/thumbnail/short_cover_game_in_static_20261031.png).

## Production safeguards

Use 9:16, English original, separate captions, the paper character and independently made schematic visuals. If illustrative audio signal is used, label it as a reconstruction during the sound. Do not present created art as documentary photographs or a historical game screen. Preserve recordings and word alignment per version; assess the final mix and captions on playback. Only a verified completed export belongs in each `Deliverables/`; clean obsolete duplicate export sets after verifying a replacement. Each video is intended initially for **private / ограниченный доступ**; verify channel and processing before reporting upload success.


## Short 01 — timing diagnostic 2026-11-03

After user skipped 028 Taj Mahal and requested the next existing Short, resumed Short 01. Current v04 review candidate remains unchanged and contains 31 subtitle groups with no double quotation marks. Reconciled retained exact voice and WhisperX forced timings against a format-only adapter of the separate older Whisper-small word timings and detected silence. Result: `01_radio_signal/Edit/subtitles_20261102/pause_reconciliation_20261103_v01.json`, 80 words and 16 flags, `REVIEW_REQUIRED`; disagreements include `developer` 0.405 s, `decode` 0.445 s, and ASR spans crossing detected silence. Adaptation files are in `01_radio_signal/Work/short01_subtitles_20261102_v02/` with source notes; no word times or audio changed. These discrepancies alone do not identify which boundary is correct. Subjective sync is still unverified; do not claim a final timing PASS or replace the public Short on this evidence.


## Short 02 — resumed review 2026-11-03

User reacted positively to the Short 01 review and asked to continue; this is not a specific confirmation of word-level sync. Short 02 current v04 review is `02_decoder/Work/short02_accent_motion_fix_20261102_v01/previews/PAPER_DETOUR_001_SHORT02_ACCENT_MOTION_REVIEW_20261102_v04.mp4`, SHA-256 `5045b616adb23bb7d0fd0a08f4a2c79583f4c682ebed3514c6e7c54cca1f284f`. Verified current file identity, 1080×1920 30fps and 41 subtitle-group texts with no double quote marks; viewed existing accent contact sheet. AAC stream SHA-256 `b79ae037166a556920a11f642b6aeeeb5b57e3156e04dc1569f5f999995e4ab8` is identical to v03. Existing comparison found provider and WhisperX timing close on average but audible sync is UNVERIFIED; no new audio or YouTube action. Earlier v04 technical decode PASS and targeted accent review are documented in `02_decoder/Edit/renewal_20261102/README.md`.
