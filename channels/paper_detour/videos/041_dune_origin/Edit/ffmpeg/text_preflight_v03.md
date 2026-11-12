# 041 Paper text-layer preflight v03

- Scope: static scene/cue placement before video render, using generated transparent cue PNGs and the selected 1440×2560 still frames.
- Assigned scene/cue pairs reviewed from `Work/ffmpeg-captions-v03b/previews/contact_sheet.jpg`: S02/GRASS, S08/ARRAKIS, S09/ARRAKIS, S11/DUNE, S12/DUNE.
- Visual review: all three cues read as paper cut letters, distinct from subtitle typography, one horizontal line, optically centered at the top; none appears side-aligned or rotated. The text is legible at phone-size previews and does not cover the main subject in the shown still compositions.
- Geometry: 110 px common face-height target on 1440×2560; same X/Y anchor. Exact PNG positions and source art are in the helper manifest. Cues spanning cuts are checked on both compositions.
- Subtitle implementation: FFmpeg montage uses the accepted Chalkboard SE Paper profile and a validated 54-group plan, exact 133-word alignment, continuous group state over all frames, and one active word state at a time. Exact audio-to-word synchronization has not been listened to in this preflight.
- Limits: static previews do not verify animated pan/zoom extrema, actual encoded frames, or audio sync. Those remain unclaimed. The project rule is to deliver the rendered MP4 immediately without additional post-render checks.
