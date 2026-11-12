# Render preflight v02 — Anandibai Joshee

- Scope: one local user-review MP4; no upload or publication.
- Saved edit: `Edit/Storyboard/montage_v01.json`; compiled plan and input manifest are in `Work/plan_check_v03/`.
- Timeline: 2560×1440, 30/1 CFR target, 4,784 frames / 159.466667 s. Thirty speech scenes occupy frames 0–4,484; two silent end screens occupy 4,484–4,784. Every scene is within 120–180 frames.
- Final audio: `Source/Audio/narration_en_v26_110_endcard_silence.wav`, mono PCM 44.1 kHz, 159.466667 s. Its 149.459206 s speech prefix is sample-for-sample identical to the accepted mix; 10.007461 s of zero-valued PCM follows for the silent end cards. Speed 1.10× was applied exactly once before the original accepted mix. No new speech, music, SFX, gain or fade.
- Alignment: exact accepted transcript forced-aligned by WhisperX to the final speech mix. The map is re-bound to the derived padded mix because its entire speech prefix is unchanged. It remains a machine estimate; audible sync is unverified. The independent Whisper small model disagrees on 123 flagged word onsets/tokenizations; these are retained as an open machine comparison, not “fixed” by shifting the map.
- Subtitles: renderer-generated Paper word captions use the exact 431-word map and end at frame 4,484. Separate English SRT passed structure and literal text coverage; its timing/playback stay UNVERIFIED. Ten syntax-boundary warnings in the automatic one-line grouping were reviewed and retained; they preserve all spoken words and measured width.
- Visual preflight: selected 30-scene sequence and two end screens are in the image manifest/contact sheet. A 2560×1440 composite of scene 01, the first active word state and the real Paper Frame was inspected: caption is legible and the overlay remains transparent in the central story area. Full motion throughout every scene is not verified here.
- Paper Frame: WebM source was decoded with explicit `libvpx-vp9` to retain alpha; the prepared ProRes 4444 overlay matches 4,784 frames, 2560×1440, 30/1, 159.466667 s. Alpha is represented as yuva444p12le.
- Output: `/Users/diplomat/ytvideos/channels/paper_detour/videos/049_anandibai_joshee/Deliverables/Anandibai_Joshee_EN_review_v01.mp4`; absent, no overwrite; no writer targets it.
- Encoder: FFmpeg 8.1.2, `h264_videotoolbox` available; H.264, 20M target, yuv420p, bt709 limited, AAC-LC mono 44.1 kHz / 192k, fast-start. Actual output profile/GOP/bitrate remain unmeasured.
- Cleanup/dependency scan: `Edit/MediaLifecycle/audit-pre-render-v02/audit.json`, zero coverage errors; no deletions.
- Required next step: exact renderer settings check. After it passes, render. Project root says hand over the successful MP4 immediately without additional post-render checks; no such checks will be claimed.
