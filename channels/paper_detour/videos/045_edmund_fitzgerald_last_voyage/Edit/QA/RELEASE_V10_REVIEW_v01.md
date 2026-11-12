# v10 final release verification

MP4 SHA-256: 59d029fc15ca93238f6c08a96c174102687b638088ba2673ab20efb11878bed5. Technical full decode PASS; see qa-release-v10-technical/report.json.

Codex visually inspected v10 contact sheets containing all 152 subtitle-group midpoints, the entrances and exits of 45 scenes, and a sample of caption transitions (every eighth group), plus full-size frames for the corrected S02 and S24. No severe subtitle/label collisions observed in that sampled coverage. This is not continuous playback or an independent review.

User reported watching v07 with audio and highlighted captions throughout with no sync faults, and separately watching its SRT with matching speech; see release_v07_midpoints/USER_AUDIBLE_REVIEW_v01.md and ../../Packaging/Metadata/Release_v04/Subtitles/USER_SRT_REVIEW_v01.md. Decoded PCM of v07, v08 and v10 has the identical SHA-256 28e0a73ca76e95d4c7975924bbe607af321220a308f13d04712797fad210b35d. v07 and v10 subtitle contracts have identical audio binding, transcript, word map, groups and frame count. Their scene plans differ only in image paths for scenes 2 and 24, with scene boundaries unchanged. The assistant did not listen and no distinct full v10 playback with SRT is claimed.

SRT structure and text mapping: 66 cues, all 581 words, zero boundary delta against the common word map, in Subtitles/TIMING_MAP_COMPARISON_v01.json. The manual EN track is separately verified on YouTube.

Chapters: the v07 ten-marker content check and 0.8-second-after-boundary frame samples are recorded in CHAPTERS_REVIEW_v04.md. The v10 timeline and narration timing match v07; only scene image files 2 and 24 differ. Chapter timing carries forward on that basis; not independently replayed end-to-end in v10.
