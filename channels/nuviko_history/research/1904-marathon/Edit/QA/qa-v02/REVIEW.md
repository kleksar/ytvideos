# Review v02 — Codex self-review

Media: `Deliverables/nuviko_lorz_short_v02.mp4`; SHA-256 `d78a659edb3cccb95af2fe7ea7c79997fb8a221b33a21f81aa77931b98f4de34`. Edit `Edit/plan-v02.json`, passport `Edit/Export/EXPORT_CONTRACT_v03.json`, renderer receipt adjacent to MP4. Export uses exact accepted voice and music mix, no upload. The engine snapshot and delivery receipt were produced on completed render. Image reconstructions are scaled up from approximately 941×1672, not native 2K.

- `stream_metadata`: PASS — 1440×2560, H.264 High yuv420p, progressive, SAR 1:1, BT.709 tv; AAC LC, 48 kHz stereo; 993 frames, 33.1 s, 30/1; see `report.json` and ffprobe.
- `full_decode`: PASS — all streams decoded by helper with no errors; `report.json`.
- `scene_duration`: PASS — seven scenes 4–5.1 s as per plan.
- `frame_sampling`: Reviewed 86 sampled extracted frames at cut boundaries, scene begins/midpoints/ends, subtitle group boundaries and holds; phone-size contact-1 through contact-5. These are samples, not continuous playback. No major crop or unreadable subtitle observed on samples.
- `motion_framing`: UNVERIFIED in continuous playback. Compared sampled scene beginnings/midpoints/ends and saw slow zoom/pan with principal subjects retained; actual screen direction at every intermediate instant not established. S004 runner passes close to right edge without sampled truncation.
- `semantic_grouping`: self-reviewed group sequence; word group splits include “got / into” and “back / to”, legible in context but not ideal syntactically. No text missing from narration based on machine comparison.
- `cue_timing`, `word_highlighting`: sampled word highlights and group changes appear in prescribed colours and locations; automated provider alignment used, but speech sync was not independently heard and not every word change individually viewed. UNVERIFIED for auditory timing.
- Editorial note: image of Hicks begins at frame 753 while “Lorz was disqualified” remains through frame 761; “The next year, Lorz” starts over Hicks at frame 834 and Boston image begins at frame 873. Narrative supplies the subject, but these transitions merit attention in user playback.
- `audio_signal`: decoded AAC vs mix PCM: correlation 0.9999789, normalized RMS difference 0.0003852, 48 kHz stereo; sample peak -5.6 dBFS. AAC decoded padding adds 448 samples per channel outside source length. This is signal correspondence, not judgment of audible quality.
- `subjective_audio_listening`: UNVERIFIED; available tools do not provide auditory perception. Pronunciation, music balance and heard sync require listening.
- `srt`: structure and transcript coverage PASS via `Edit/srt_v01_report.json`; timing mapping and playback UNVERIFIED, based on provider alignment for the same source and conform speed.
- `independent_review`: UNVERIFIED; this is author self-review. No user acceptance, release, or upload.

Overall review: UNVERIFIED; suitable for user review with explicit limits, not a claim of full audiovisual QA. Five contact sheets preserve actual sampled indices; source frame map and automated evidence are in `report.json`. The first render lacked a delivery receipt because semantic_grouping.py changed during its run; v02 used newly prepared subtitles and a stable engine snapshot. Hardware encoder failed -12908; libx264 used.
