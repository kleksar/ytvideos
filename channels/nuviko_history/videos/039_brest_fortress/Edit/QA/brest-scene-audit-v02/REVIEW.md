# Brest Fortress 039 · v02 review

Exact MP4 SHA-256: `a4ab38fe9c77eb5206482ac287b2c1d95162405570d1ac195e608a362b908789`.

- Original review MP4 v01: all 116 scene midpoints and all 69 distinct active sources visually audited. The original file was completely decoded by the QA helper. Baseline findings and revision decisions are in [preflight](PRE_RENDER_REVIEW.md).
- Revised montage: 117 scenes / 18,370 frames. All intervals are 120–180 frames at 30 fps. Zero adjacent duplicate source paths; 72 distinct PNGs verified against their manifest. The 11 generated replacements have native dimensions 1672×941; the montage renders to 2560×1440.
- Encoded v02: FFprobe reports H.264 2560×1440 at 30 fps, 18,370 frames and 612.333 seconds of picture. Visually reviewed all 18 extracted sample pictures on [sheet 1](export-samples-1.jpg) and [sheet 2](export-samples-2.jpg). Confirmed readable gate turrets, host/room style separation, East Fort earthworks and ditch, distinct memorial views, casualty-figure overlay, and quote insertion/removal at the sampled cut boundaries. The graphic and English caption band are visually separate in the samples.
- AAC elementary stream packet payload hash matches v01 exactly. The audio speed of 1.10× is already evidenced at synthesis, and the complete mix, groups and frame intervals match v01. This is machine comparison, not a listening review.
- The file was encoded successfully. The workspace renderer source changed during encoding, which prevented automatic writing of the receipt. The v02 receipt was written after validating the saved FFmpeg command, frozen engine, exact inputs and stream metadata. See [provenance recovery](render_provenance_recovery.json).
- Coverage is creator-side and sampled for v02. Continuous v02 playback/full decode, independent AV QA, listening, user acceptance and any applicable reference-image release clearances remain unverified.
