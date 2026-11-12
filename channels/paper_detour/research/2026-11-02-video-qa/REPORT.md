# Paper Detour: video QA refactor — 2026-11-02

## Current result

The user's early framing rule is installed in scene-images (canonical early composition procedure), storyboard (camera envelope handoff) and image-motion (consume/recheck). The Paper image profile's obsolete blanket ban on authorized camera/parallax was reconciled with current channel instructions. No media, timelines, sound or YouTube data were changed here.

**Portable final QA skill: completed.** [ytv-video-qa](../../../.agents/skills/ytv-video-qa/SKILL.md) owns the reusable procedure, [Paper offline profile](../../../.agents/skills/ytv-video-qa/references/paper-detour.md), motion checks, coverage and defect/recheck records. Its stdlib/FFmpeg helper performs technical inspection and exact frame extraction. Ten focused tests pass, plus a real pilot run. Production, audio delivery, captions, image-motion, edit/release and discovery/documentation route to it. The former audio QA profile is a compatibility link, not a duplicate procedure.

The required [personal Extra High consultation](../../../.agent/consultations/paper_video_qa_skill_20261102.md) returned only completion summaries twice. The user then explicitly granted the one-time exception «Да, закончить QA-навык здесь». Development was completed locally under that scope; no invisible recommendation is attributed to ChatGPT.

## Linked parallax session

Read two pages of recent turns from [Автоматизировать 2.5D параллакс](codex://threads/01a199c3-17b7-73a2-b08c-2d2d4dcff94f). [Focused evidence](parallax_thread_evidence.json) excludes reasoning items and is not an exhaustive thread export.

- Actual motion direction was measured using normalized image-patch correlation with scipy FFT convolution, filtering low-confidence or negligible displacement and comparing median horizontal displacement. The configured sign had not always matched the visible direction; measurements were used to correct it.
- Framecounts, duration, aspect and two reserve tail frames outside the visible range were checked. Other tracks and clip properties were compared while accounting for regenerated clone IDs. These are structural preservation checks.
- Samples from all 15 scenes were inspected. The session explicitly distinguished this from full playback/listening. Neither direction measurement nor three sample positions establishes that a face, important object or text stays in frame throughout motion.
- Latest accepted direction is aligned; the intervening inverse experiment was reverted. Current presets and renderer remain owned by image-motion. No historical effect experiment becomes a current requirement.

The user's additional rule is explicit: debug crop risks before image creation. Storyboard specifies movement limits and protected content; images are composed and checked against those limits before import. The final composite still needs a separate check, including intermediate extrema and moving text overlays. There is no universal safe-margin percentage.

## Pilot 033: existing delivery audit

Target: `new_channel/videos/033_time_stop`. Existing delivery SHA-256 remains `6d3ce02af25a3a655961d25c84448f6d697f7ed4a74865a840cf7df179653dd9`.

- Full FFmpeg decode of selected video and audio streams: exit 0, no error output. Fresh counted decode through ffprobe returned 1502 video frames.
- [Stream metadata](ffprobe.json): H.264 High, 1080×1920, 30 fps, BT.709, 1502 frames / 50.066667 s; AAC LC mono 44100 Hz, 181298 bit/s measured. Historical encoder target was 192 kbit/s; measured VBR does not itself fail that target.
- [Native audio levels](audio_native_levels.log): mean −25.3 dBFS, sample peak −4.1 dBFS. These are measurements, not a universal loudness target or a true-peak test.
- [Read-only audio comparison](audio_measurements.json): ten one-second RMS-envelope windows against existing voice; best lag +10 ms in each, correlations 0.95661–0.98929. No observed accumulated shift in those windows. This does not prove sample identity, every spoken word, natural pronunciation or complete listening. PCM was decoded in memory; no new audio file was generated. Silence candidates are observations to compare with narration, not automatically defects.
- [Read-only live timeline](get_timeline.json), identity verified through [project discovery](projects.json) and [media](get_media.json): project `887E5C83`, recorded work timeline `FB491927`, 14 background stills, 8 accent clips, 1 dialogue clip. No timeline mutation.
- [Scene intervals](scene_durations.json): 11 of 14 fall outside the current Paper 4–6 second standard; S05, S11, S14 comply. Range 1.533333–7.566667 s. This checks current policy conformity and does not erase historical user acceptance or authorize re-editing.
- **Freshness: STALE.** Current context and the cleanup receipt record a timeline change after this delivery. Matching its historical SHA does not make the old MP4 an export of the updated edit. Live discovery also lists a later motion timeline `C5A62B3F`; this audit does not select or modify it, and its active writer's handoff must establish the next export target.
- Separate SRT: NOT_REQUESTED under the existing Short contract. It is not a missing deliverable.

New [offline helper report](../../videos/033_time_stop/Edit/QA/20261102_offline_v01/report.json) confirms technical PASS and overall FAIL for the stale/policy-nonconforming target. Extracted and inspected 84 frames in three contact sheets at 270×480 per sample; additionally inspected native frames 113, 1379, 1380 and 1471 at 1080×1920. All 14 scenes, 13 cuts and eight accents are represented. No new blocking crop/face/text defect was found in that sample. See [review receipt](../../videos/033_time_stop/Edit/QA/20261102_offline_v01/review_receipt.json) for exact indices and limits.

[Cue alignment observations](cue_alignment_observations.json): six onset anchors agree within one frame; C13 follows the end of “Nothing” and C14 follows the final sentence, rather than those phrases' onsets. This is a timing-handoff ambiguity, not permission to shift the accepted edit. Full intentional cue-sync acceptance remains UNVERIFIED. The initial helper plan sampled a candidate C14 exit that is actually a final hold; the [corrected review plan](pilot_qa_plan_corrected.json) records no C14 fade and retains that frame as an extra sample. Raw evidence is preserved.

No subjective listening or independent review is claimed. Player playback is NOT_REQUIRED by the current Paper offline profile. Historical acceptance retains its original scope. Current-release readiness is **not PASS**: an export matching the accepted current edit and its required offline QA remain open. Existing private YouTube video was not changed.

## Remaining work

[Scoped validation](validation.json): seven affected skills pass schema checks, 393 local links resolve, the new skill resolves to the same canonical file from all 50 managed entry points, role TOML parses and ten helper tests pass. Native skills/list and independent behavioral review were not performed. The earlier global governance validator still reports broader migration/probe/documentation discrepancies; no project-wide green status is claimed.

Obtain the active editor's handoff of the accepted current timeline, resolve current scene-policy conformity and cue-anchor metadata, then check its actual new export. This task created no new delivery, sound or timeline edit. Further portable storyboard/caption work follows the implementation plan; QA infrastructure itself is now available from the production entry point.
