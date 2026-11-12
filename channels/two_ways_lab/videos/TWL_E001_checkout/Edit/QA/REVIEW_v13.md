# TWL_E001 v13 — review evidence

MP4 SHA-256 `18e98b1e780d357d7edfc7e3c4268c73f671b56a92ebee45489c831393d3c060`. User acceptance pending.

- The intermediate image at 0:07 was 20 frames / 0.667 s in v12; it is now 50 frames / 1.667 s, starting at frame 210 (7.0 s). The next scene starts at frame 260 (8.667 s). Sampled rendered frames around both cuts are in `v13_seven_seconds.jpg`; cuts are still cuts between independently generated scene images.
- The same v12 source sound mix is used, without a new recording. The SRT file is byte-identical to v12. Prior voice alignment and text checks are recorded in `REVIEW_v12.md`; they do not establish naturalness or subjective sound quality.
- The render plan enforces a minimum of 45 frames per scene. The shared renderer validates that optional threshold; its test suite passed 20 tests in the active checkout and 20 on the clean upstream checkout. Upstream media checks passed 12 tests.
- Complete FFmpeg decoding succeeded. `ffprobe_v13.json`: 1080×1920, 30 fps, 802 frames, 26.733 s, H.264/AAC.
- Subjective audio and loop listening, physical phone playback, and independent review are unverified. Sampling the cuts is not a review of every frame.
- v12 was rejected and moved to Trash; its exact receipt is `REJECTED_v12.json`.
