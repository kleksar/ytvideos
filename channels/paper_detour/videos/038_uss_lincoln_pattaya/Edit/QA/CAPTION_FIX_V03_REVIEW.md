# Paper 038 caption fix — v03 review

- Export: `Deliverables/Paper038_EN_v07_review_v03.mp4`
- SHA-256: `aedfa79d015287c1807c7ac7af4ce5790691338b1d4e05b1b14c8f2575f5d1bd`
- Edit: Palmier project `020961F2`, isolated timeline `058B37CE`, snapshot `6C231D9F`.
- Caption implementation: transparent word-state overlay on V2, above the original 15 scene clips. The overlay schedule is derived from the retained word map; first active frame is `ceil(start_seconds × 30)`. For each word onset, the current word becomes yellow and the other words stay cream.
- Visual word-state review: all 158 mapped word-start frames checked in contact sheets `Edit/QA/paper038-en-v07-caption-fix-v03/word_start_sheet_01.jpg` through `_09.jpg`. Expected single-word state is visible at every sampled onset.
- Technical QA: `Edit/QA/paper038-en-v07-caption-fix-v03/report.json`; stream metadata, full decode and frame extraction PASS; 1,786 video frames decoded.
- Resolution/FPS/color/audio measured: 1440×2560, H.264 High, yuv420p, 30/1 CFR, BT.709 limited; AAC LC stereo 44.1 kHz.
- Word highlighting: PASS for visual color-state behavior on the 158 sampled starts. Frame/cue timing against the spoken voice: UNVERIFIED because the automatic word map remains REVIEW_REQUIRED and has not been listened through.
- Full-frame, full-motion, subjective audio and independent review: UNVERIFIED. User MP4 review: PENDING.
