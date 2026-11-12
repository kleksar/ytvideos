# Review export contract — Short 02 renewal v02

Status: `REVIEW_ONLY`; not a final deliverable and not authorized for upload.

## Source revision

- Palmier project: `31F93804` (`Paper Detour 001 Short 02 Director Trial 20261031.palmier`).
- Timeline: `7537BAE9`, `Timeline 1`.
- Saved Palmier snapshot: `Short02 scene07 v03 and ASR subtitle review draft 20261102`, saved 2026-11-02 16:58 local. The project UI still indicates live edits; this saved snapshot preserves the review state.
- Timeline: 1098 frames, 36.6 seconds, 1080×1920, 30/1 fps, Rec.709 SDR.
- Tracks: V3 review subtitles (ASR-estimated timings), V2 nine paper accent stills, V1 seven scene clips including scene 07 v03 parallax, A1 existing premix. Narration and audio clip are unchanged.

## Review output

- Unique output: `../../Deliverables/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v02.mp4`.
- Purpose: let the owner inspect the actual assembled image, motion and subtitle timing before any final export decision.
- Container: MPEG-4; video codec: H.264; resolution: Match Timeline (1080×1920); frame rate: 30 fps; color: Rec.709. Palmier Export Queue exposes these native choices; bitrate/quality and AAC controls are engine-managed unless the export UI exposes them.
- Audio source: unchanged A1 premix `preview_mix_36p6_no_sfx_stereo.wav`, SHA-256 `d8e942f34436dc41c3d3a2eed91e99bcefcaa19371d1cecc01d599b9327495a2`. No new audio, normalization or level changes are authorized.
- Review input subtitle MOV: `Assets/Generated/renewal_20261102/short02_subtitles_asr_timing_review_20261102.mov`, SHA-256 `6d67a23acb47dd67a3d038d4410797682ab6aea779abff841bdbf189f1e11ca2`, no audio.
- Scene 07 motion input: `Assets/Generated/renewal_20261102/scene07_v03_parallax_1080x1920.mp4`, SHA-256 `cfdae565695923b56cc4c339168ec352f5205e9b332bbcc4ceadd3d66c6f455e`, no audio.

## Gate and limitations

The V3 timings are derived from local Whisper word timestamps on the exact earlier MP4. Whisper token `102` was apportioned across “one hundred and two” using earlier alignment proportions. Hearing-based synchronization is `UNVERIFIED`; this blocks final acceptance and publication. The output must remain visibly named and stored as a review candidate until the owner checks speech-to-caption timing and the standard final QA is complete.

Pre-render lifecycle audit: `pre_render_review_audit_20261102/audit.json` and `.md`; no audit errors or missing declared candidates. Coverage is bounded, not exhaustive; unrelated unresolved imports and inaccessible external dependencies remain outside this render’s verified coverage.

## Export result

Completed in Palmier Export Queue at 2026-11-02 17:02 local. Queue showed `Completed` for the exact path below.

- Actual file: `../../Deliverables/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v02.mp4`.
- SHA-256: `629644be7a4f6c0ca6accd567cd0409c00556f948062846609c00cc52f6da01b`.
- Measured: 36.6 s; 1098 H.264 frames, High profile, 1080×1920, yuv420p, 30 fps, BT.709; AAC-LC stereo 44.1 kHz at 116107 bit/s. Palmier exposes no audio rate/bitrate controls in this export path; those values are engine-managed, not manually selected.
- Managed technical check: `PASS` for stream metadata, full decode and frame extraction. Visual samples were self-reviewed: all 7 scene start/mid/end points and all 41 cue midpoints. Scene 07 framing and sampled subtitle geometry passed.
- Full QA verdict: `UNVERIFIED`. Whole-program A1-to-output numerical signal correspondence passed (zero estimated offset; correlation `0.99958`; residual RMS `-53.72 dBFS`), but subjective audio listening and audible subtitle sync remain unverified. Visual cue samples and scene 07 motion framing passed as self-review samples; intervening frames and independent review remain unverified. AAC sample rate/bitrate remain engine-managed. This file is a review copy only.
- QA records: `../../../../Edit/QA/short02-review-v02-qa-20261102/report.json` and `reviewer_receipt.json`; review plan: `review_qa_plan_v02.json`.
