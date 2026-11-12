# Harrison Short v02 — internal review

Exact file: ../harrison-review-v02.mp4
SHA-256: eda2cd33730e1e1c11ea0bf4b68890da9bf3c8f6a24dd91e05e95641ff6b6d4f
Edit: ../harrison-edit-v02.json; export: ../harrison-export-contract-v03.json; renderer receipt: ../harrison-review-v02.mp4.delivery.json.

- stream_metadata PASS: ffprobe counted 1420 video frames, 1440x2560, 30/1 fps, 47.333333 sec, H.264 High yuv420p limited Rec.709; AAC LC mono 48 kHz. Raw probe: ../harrison-probe-v02.json.
- full_decode PASS: FFmpeg decoded both complete streams with `-v error -map 0:v:0 -map 0:a:0 -f null -`, no errors reported.
- frame_sampling / motion_framing PARTIAL: beginning, middle and end of all nine scenes sampled in motion-extrema.jpg (27 frames); content stays framed and subtitle bands do not cover focal items at these samples. Direction and zoom were compared at sampled endpoints. Full continuous playback was not performed.
- semantic_grouping: all 139 words read in caption_groups; protected John Harrison, east or west and kept time remain together. Two forced/ambiguous boundaries remain: “sailors where they / were in the ocean?” and “to prove that the method / could work at sea.” Both preserve exact words and remain readable in context.
- subtitle continuity PASS mechanically: groups cover frame 0 through exclusive frame 1420 with no gaps. All 139 word-event frames correspond to ceil(alignment seconds * 30). Visual sample of 6 word boundaries (before/on/after) in word-transitions.jpg; not all 139 boundaries visually reviewed. Alignment is machine-estimated and unverified by listening.
- audio_signal: source mix measured -21.1 LUFS integrated and -1.2 dBTP by FFmpeg ebur128; this is not a judgment of intelligibility or music balance. Independent ASR base.en reproduced all 139 normalized words in order; ../harrison-audio/asr-base-en-v01.json. Subjective listening UNVERIFIED.
- independent_review UNVERIFIED; SRT and user acceptance not performed.
- reference rights: ../harrison-visual-pilot/h4-provenance-v02.md. Wikimedia Commons photo is CC BY-SA 4.0, used as visual reference for generated reconstructions; packaging draft contains attribution and flags assessment of applicable share-alike requirements before publication.

This is internal technical and sampled visual review, not user acceptance or authorization to publish.
