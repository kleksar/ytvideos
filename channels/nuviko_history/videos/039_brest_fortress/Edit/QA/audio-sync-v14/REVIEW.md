# V14 technical QA for private upload

Exact MP4 `Work/rebuild-early-20261106/previews/full_review_v14.mp4`, SHA-256 `e0b791d0baf22f8b927a630b9121ba8fe266ae06ebc3a3f8d1f13933fdc4304d`. Formal provenance and encoder settings: `Work/rebuild-early-20261106/render_v14/` and corresponding `full_review_v14.mp4.delivery.json`. Official renderer re-created V13's edit with exact scene replacements and unchanged V13 full mix. A separate pre-render settings check passed at `check_v14/settings_check.json`.

MP4 metadata: H.264 2560×1440, 30 fps, 18,671 frames, 622.366667 seconds; AAC stereo 44.1 kHz. Compressed AAC audio SHA-256 `73459b9a189bbb26b83c319d6a88e0860d302c240021ca2ce8b25d008c6236d9` is identical for V13 and V14. At each of 622 one-second windows decoded audio correlates >=0.999900 with the intended mix (`signal_correlations.json`). Same 433 caption groups and 1,555 word-event frames as V13; last caption has same effective end 612.1 s as V13's filter. Sidecar 192 cues and 1,555 words match map in `Edit/QA/audio-sync-v13/srt_map_check.json`; soundtrack has unchanged sample timing.

Twelve exact V13 and V14 frames scaled to 640×360 at 0.6, 55.0, 131.2, 165.9, 220.8, 274.85, 371.8, 550, 564, 605.53, 611.7 and 617.0 seconds have zero pixel difference (`visual_comparison.json`, `v13_v14_contact.jpg`). This is sampling, not comparison of every frame. Video compressed stream hashes differ; no claim of video-byte identity. The same scene source paths, camera settings, and exact subtitle groups were reconstructed from previous versioned edit plans.

Audio listening and subjective balance remain UNVERIFIED. SRT map agreement is not independent proof that a machine-aligned word matches the actual speech. Private staging is requested; no release or public visibility is inferred.

Full video and audio decode: PASS, `ffmpeg -v error -xerror -i full_review_v14.mp4 -map 0:v:0 -map 0:a:0 -f null -` returned exit code 0 with no reported errors. Technical status PASS for private staging; subjective/independent checks remain as recorded above.
