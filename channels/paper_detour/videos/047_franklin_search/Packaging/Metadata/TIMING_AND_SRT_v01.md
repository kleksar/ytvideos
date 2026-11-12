# Timing and SRT checks

Exact accepted video: 047_franklin_search_review_v05.mp4 SHA-256 edc32753ad91003b5958b6bb9e5e0ba05c558583c9f84746d470c436440d12d5, duration 576.566667 s.

Chapters v01: formal validation PASS against exact MP4; estimated boundaries from accepted final-audio WhisperX word map (e.g. 49.942, 82.463, 119.524, 285.890, 329.752, 395.514, 436.595, 467.256, 518.958 s), rounded down to whole seconds. Status MACHINE_CHECKED; chapter boundary playback and precise audible sync remain UNVERIFIED. YouTube guidance https://support.google.com/youtube/answer/9884579?hl=en.

English SRT: structure and exact text coverage PASS; byte-identical to reconstruction from 159 retained cues. All 1,458 cue words match the timed word map, each cue first/last time within 2 ms of word map. Source mix and text bound by hashes in word map; unchanged full-mix timeline. Machine alignment remains an estimate and separate-track audible playback remains UNVERIFIED. Readability has four cues over 23 characters/second heuristic (43, 72, 120, 124); not a platform threshold. See SRT_VALIDATION_v01.json.
