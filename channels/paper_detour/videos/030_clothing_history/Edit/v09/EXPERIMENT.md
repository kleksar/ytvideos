# Paper Detour 030 — grain restored to the 25% baseline, v09

## Request

User asked to return the full-frame grain to its original strength and upload another copy for review.

## Timeline

- Duplicated v08 timeline `479ECE26` in project `B1BA2D18` as isolated timeline `B10FBA68`; snapshot `ABCA6C4B` saved before the edit.
- Changed only Grain clip `65FB718C` opacity `0.50` → `0.25`, matching accepted v06.
- Source remains mediaRef `9543F1E4`; clip spans frames `[0,5700)`. No scene, text, timing or audio edit.
- Live comparison confirms v09 matches v06 except generated IDs/timeline name; against v08 the sole edit difference is Grain opacity.

## Export and audio preservation

- Palmier native export job `F1489722-E5CC-482A-A5D8-157A9DA6A763` at 1920×1080, 30 fps, 190 s.
- Palmier re-encoded its AAC output differently from the accepted mix. That native MP4 was retained for diagnostics and not uploaded.
- Final `PAPER_DETOUR_030_GRAIN_25_BASELINE_EN_v09.mp4` copies the native H.264 video stream and muxes the preserved accepted AAC mix from `Source/Audio/v06/accepted_v05_mix.m4a` without re-encoding. QA confirms the H.264 payload equals the native picture and the AAC payload equals the accepted mix bit-for-bit; full decode passed.
- Actual frames 367, 1380, 2983, and 4990 were compared against v08. At 25% the grain is visibly lower; sampled text remains readable. Full-length 1× playback and independent AV review were not performed.

## Private YouTube review

- Paper Detour video ID `EUwJ5ES4UmY`, https://www.youtube.com/watch?v=EUwJ5ES4UmY.
- API readback confirmed `private`, `processed`, processing `succeeded`; this v09 baseline is for comparison with private v08 at 50%, ID `2Ks3XDf4JwM`.
- Neither version is a public master or public release. Await user's visual judgment.
- Detailed status and metadata: [`../../Packaging/Metadata/YOUTUBE_REVIEW_UPLOAD_GRAIN_25_V09_20261102.md`](../../Packaging/Metadata/YOUTUBE_REVIEW_UPLOAD_GRAIN_25_V09_20261102.md).
