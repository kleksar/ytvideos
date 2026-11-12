# Short 01 subtitle overlay export contract v04 review candidate

Status: READY_TO_RENDER. This is a review candidate, not the promoted current delivery. The user explicitly authorized reworking the video. Narration and every existing audio clip must remain as currently placed and mixed.

## Binding

- Palmier project `58F68144`, canonical timeline `7178D5B6`, snapshot after subtitle overlay `67870081` (pre-edit snapshot `025E8E00`).
- Current image/motion/semantic accent arrangement retained from accepted Short 01 v03; one top transparent subtitle overlay clip on the new `Dialogue` track, frames `[0,885)`.
- Exact transcript: `channels/paper_detour/videos/001_radio_game/Shorts/01_radio_signal/Source/Voice/strategy_v1/narration_en.txt`. Alignment source: same episode's `strategy_v1` A1 voice recording; 80 exact words. Timing map is an independently forced-aligned draft; audible subtitle synchronization is **UNVERIFIED**. Semantic group plan has 32 groups, max 3 words, one line.
- Subtitle appearance: Chalkboard SE Bold, 72 px, cream with dark outline; active word warm yellow; fixed centered baseline and continuous visibility. Positions and width were checked on 100 frame samples across scene cuts and word changes; full contact evidence is under `Work/short01_subtitles_20261102_v01/previews/subtitle_composite/`.
- Overlay dependency: `channels/paper_detour/videos/001_radio_game/Shorts/01_radio_signal/Assets/Generated/short01-subtitles-20261102-v01/short01_narration_subtitles_overlay_v01.mov`; ProRes 4444 with alpha, 1080×1920, 30/1 fps, 885 frames, no audio.
- Previous v03 file SHA-256: `7bfbb706e14ebb66bfef5d25e99ca80eebc454ae2d2711e9f79f8ef989f281b3`.

## Output contract

- Candidate path: `channels/paper_detour/videos/001_radio_game/Shorts/01_radio_signal/Work/short01_subtitles_20261102_v01/previews/short01_subtitles_full_v04_review.mp4`; new path, overwrite refused.
- MP4 H.264, Match Timeline, 1080×1920, 30/1 FPS, Rec.709 SDR, progressive, 885 frames / 29.5 s.
- Required encoded video: yuv420p, BT.709 primaries/transfer/matrix, limited/video range; measure from resulting file.
- Existing audio only: original A1 voice, A2 music and A3 SFX. Preserve their clip positions, trims, volume and route. Native AAC stereo 48 kHz, at least 256 kb/s per Paper delivery profile; measure the actual file. No new audio, no voice change, no normalization or speed change.
- No separate SRT requested for this Paper Short; the narration subtitles are burned in. Current title, description, hashtags and thumbnail for v03 are not revised by this visual subtitle operation.
- Before export: exact project/timeline and dependencies confirmed; snapshot saved; scoped lifecycle audit completed at `Edit/MediaLifecycle/audits/short01_subtitles_preexport_20261102_v02/audit.json` with zero coverage errors.

## Open checks after export

Bind export job and SHA. Probe streams, exact frame count, full decode, and all audio track/sample properties. Inspect final MP4 frames around every scene/cue boundary, phone size, karaoke word persistence, protected details, accent/subtitle spacing, and start/end visibility. Compare retained speech and subtitle triggers on the exported file; because no audible playback has occurred, leave voice-to-caption sync **UNVERIFIED** until reviewed. Do not promote or update the YouTube replacement while this blocking sync status remains unresolved.
