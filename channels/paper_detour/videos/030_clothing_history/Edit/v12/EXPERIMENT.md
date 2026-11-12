# Clothing history — local native Full HD grain test v12

**Scope:** only compare grain strength. Local-only test at 15% opacity, against v11 at 33% using the same native 1920×1080 grain cycle.

## Timeline

- Project `B1BA2D18`; source timeline v11 `E6076D37`; isolated v12 `2D8D9202`.
- Snapshot before edit: `1085A090`.
- Only change: opacity on all 24 `Grain` clips set to `0.15`. The same mediaRef `43710BAA` remains; one continuous track covers frames `[0,5700)` without gaps. Scenes, accents, timing, transforms and Mix track remain from v11.
- Source cycle: `../../../../Shared/Overlays/Film_Grain/paper_fine_grain_8s_1920x1080_30fps_v01.mov`; 1920×1080, 30 fps, 240 frames, ProRes 4444 alpha; SHA-256 `9459ca3890454b4ec9dbf9728d37aab83b59b0a0abf21b2ef85bd18a78b172fe`.

## Local MP4

- [`PAPER_DETOUR_030_NATIVE_FULLHD_GRAIN_15_LOCAL_v12.mp4`](PAPER_DETOUR_030_NATIVE_FULLHD_GRAIN_15_LOCAL_v12.mp4): 1920×1080, 30 fps, 190 seconds, H.264, 616,478,776 bytes.
- Video encode: libx264, preset medium, CRF 16, tune grain, yuv420p, BT.709.
- Accepted audio from `Source/Audio/v06/accepted_v05_mix.m4a` copied without re-encoding. Extracted AAC payload SHA-256 matches source: `3ba2d8175d566eff1addd0b5278b82fd36616a5e41da0e68cba1531939321e6e`.
- Final MP4 SHA-256: `a50ef10b9b4545c1f1af7eee99aaa7ff2735d697f4f186e126963eb4a242573a`.
- Full decode passed. Actual MP4 frames 239→240 and frame367 inspected; no visible break at the sampled cycle boundary, title remains readable and grain is visible at reduced strength. Full-length 1× playback and independent review were not performed.
- Uploaded as a private review copy after the local render, at the user’s request: [v12](https://www.youtube.com/watch?v=OR0E1mrQKak). API readback confirms `private`, `processed`, and `processing succeeded`. It was not made public or scheduled.
