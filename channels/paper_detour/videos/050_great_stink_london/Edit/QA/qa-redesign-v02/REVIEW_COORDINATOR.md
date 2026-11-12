# Paper 050 redesign — exact-file review v02

Media `Deliverables/review_redesign_en_v02.mp4`; SHA-256 `2f2c74c675dd27437c5290ca9abb2b32122a884cf27363f4cd538ca3a8491b3b`. Edit `Edit/LongForm_v01/plan_visual_redesign_review_v03.json`; export passport `Edit/LongForm_v01/EXPORT_CONTRACT_redesign_review_v02.json`. User review pending; no publication authorization for this revision.

- `stream_metadata` and `full_decode`: PASS by managed helper `report.json`; 7584 decoded video frames, 2560×1440, H.264, 30 fps, Rec.709 tags; AAC stereo 44.1 kHz; 252.8 s; no helper failures.
- `frame_sampling`: coordinator inspected all 153 extracted scene start/mid/end samples on `scene_frames_1.jpg` through `scene_frames_6.jpg` at 320×180 per image, including both sides of cuts. No obvious missing scenes, text collisions, empty/black frames, or incomplete ending in these samples. Boy scene 16 shows one cloth-holding hand. This is not inspection of every frame or full-size anatomy for every source.
- `cut_recheck`: PASS at sampled frames 4924/4925 and 6299/6300: Barking label/subtitle now changes to southern label with its next subtitle. S35→S36 at 5044/5045 checked in sheet. Other transitions are covered by the sampled neighboring scene endpoints only.
- `motion_framing`: start/mid/end samples cover every scene; intermediate motion, direction and smoothness have not been fully viewed; UNVERIFIED.
- `cue_timing` and `word_highlighting`: visually sampled states at 153 frames; caption map copied from exact unchanged voice and rebound to selected music mix; sample highlights shown. Full cue-by-cue audit and audible synchronization of this new mix UNVERIFIED. User had approved sync of three previous voice-only samples, not this entire mix.
- `audio_signal`: mix converted to mono 8 kHz in both source WAV and rendered AAC, aligned without offset. Over common samples Pearson correlation 0.999953 and RMS error 0.000752; source 2,022,400 samples versus decoded AAC 2,022,551 samples (151 samples trailing difference at 8 kHz). Helper sample peak -2.9 dBFS. This supports approximate signal preservation, not perceived balance.
- `subjective_audio_listening`: UNVERIFIED. Coordinator cannot hear audio in current environment; no claim of intelligibility, music audibility, tonal fit or audible subtitle sync. Music is Scott Buckley `Signal to Noise — No Piano Melody` as documented in audio handoff, including CC BY credit for future description.
- `srt`: source-time draft exists; separate final upload SRT is not verified. It is not needed for user MP4 review, but remains required before any release.
- `independent_review`: UNVERIFIED; all image and exact-file checks above are coordinator self-review.

The helper's overall verdict remains UNVERIFIED because required coverage has limitations; its technical result is PASS. This receipt does not assert full audiovisual QA or user acceptance.
