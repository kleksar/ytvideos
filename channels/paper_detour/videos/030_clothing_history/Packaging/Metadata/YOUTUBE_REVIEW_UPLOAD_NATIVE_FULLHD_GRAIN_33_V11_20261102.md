# YouTube private review upload — native Full HD grain 33% v11

**Verified:** 2026-11-02. **Purpose:** visual test of the finer full-resolution grain against private v10; not a public master.

- Video ID `TWAObKXZVJ8`; [open on YouTube](https://www.youtube.com/watch?v=TWAObKXZVJ8).
- Paper Detour channel ID `UCMVfdfaNxV3ZkI3_J3Eejzw`; title `Clothing Through the Ages — Native Full HD Grain 33% (Private Review v11)`.
- YouTube API readback: `private`, upload `processed`, processing `succeeded`; category `27`; metadata/audio language `en`; made-for-kids `false`; duration `PT3M11S`; no processing failure. Title and description matched submitted values.
- Compared with v10, only grain source resolution/scale changes: native 1920×1080 8-second ProRes 4444 alpha cycle, 33% opacity. Scenes, accents, timing and accepted audio are unchanged.
- Final MP4 is 1920×1080, 30 fps, 190 seconds, H.264, 1,193,901,605 bytes; SHA-256 `eec8e2515b886dc10060e08a0979cdd0fb7a619a472a7db9564e01d74f699862`.
- Decode passed. Selected frame 367 and the actual MP4 loop-boundary pair 239→240 were inspected. The accepted AAC payload matches `Source/Audio/v06/accepted_v05_mix.m4a` bit-for-bit. Full 190-second 1× playback and independent review were not performed.
- No public release, schedule, thumbnail, playlist, or manual subtitle was set.

Direct comparison: [v10 fine grain, 33%](https://www.youtube.com/watch?v=HwniKlV8S9Q). The project retains earlier private comparison versions v08 and v09.

Local files: [final MP4](../../Edit/v11/PAPER_DETOUR_030_NATIVE_FULLHD_GRAIN_33_EN_v11.mp4), [experiment](../../Edit/v11/EXPERIMENT.md), [QA report](../../Edit/v11/QA/QA_REPORT.json), [metadata](../../Edit/v11/QA/YOUTUBE_REVIEW_METADATA.json).
