# CURRENT_CONTEXT — 031 Jascon-4 / Harrison Okene

## Active assembly — 2026-11-02

- Channel: **Paper Detour**, English Short, 16 accepted paper dioramas, 1080×1920, 30 fps, 2139 frames / 71.3 s. Selective paper accents only; no full subtitles/SRT/VTT requested.
- Current source/working state: project `8BE390BC`, source timeline v11 `1BD3395C`. During motion preparation v11 changed; readback showed Grain removed and the Accents track relabelled. The first apply safely stopped on its source fingerprint. I preserved the current state, then generated v12 from this updated baseline.
- **Current motion version: v12 `F34C8B11`, “031 Rough Cut v12 Gentle Parallax No Grain”**, snapshot `F8F1B358`. The v12 timeline contains only `Accents`, `Main`, and `Voice`; 16 scene clips carry DepthFlow 1.0.1 `gentle-aligned` parallax and reduced existing camera keys. Scenes without camera keys retain no independent camera movement; parallax animates each full scene as one image. No grain track, character animation, part animation, new artwork, audio change, or cue timing change.
- Motion provenance and depth/cache: `Edit/ImageMotion/936f1549d77ebfe1ff84/run.json`, `motion_v12.json`, `sources_v12.json`. Structural timeline verification PASS; 16 clips. Scene motion sample sheets are `MOTION_QA_S01-08.jpg` and `MOTION_QA_S09-16.jpg` in that run directory.
- New MP4: `Deliverables/031_jascon4_okene_en_short_1080x1920_30fps_v12_gentle_parallax_no_grain.mp4`. H.264/yuv420p, 1080×1920, 30 fps, 71.300 s, 2139 frames; AAC-LC mono 44.1 kHz, target 192 kbit/s, measured average ~172 kbit/s; full decode PASS; video bitstream preserved during audio mux. Receipt: `Edit/MP4_DELIVERY_RECEIPT_v12.json`; delivery note: `Source/Production/MP4_DELIVERY_v12.md`.
- 27 actual MP4 frame samples reviewed (16 scene midpoints + 11 cue holds). Sampled frames show legible cues and no obvious deformation/collision. Full 1× playback, subjective listening, seam review and independent review remain **UNVERIFIED**; classify as REVIEW MP4 until those checks occur. No upload/publication.
- The prior v11 local MP4 was deleted after v12 decode, stream, duration and sampled-frame validation; v11 timeline/project and all source artwork remain preserved.

## Authorities and accepted inputs

- Extra High consultation for the motion choice is saved in `Source/Production/PARALLAX_CONSULTATION_20261102.md`; exact visible model label and chat URL are recorded there. It supported restrained whole-scene movement, with no independent parts animation.
- User timestamps are seconds:frames at30fps. Date useranchor00:17:26=f536; location20:05=f605 was shifted to spoken “off”00:21:03=f633. Existingdate/locationcue ranges[536,609)/[633,687).
- Accepted story/script and original storyboard retained: `Source/Script/narration_ru_v01.md`,Englishworking`narration_en_v01.md`,`Source/Voice/voice_en_tts_v01.txt`,`Storyboard/storyboard_v01.md`. Detailed history and translation/review statuses are preserved in context history. English product language required explicitly by user.
- Actual images: seven complete above-water replacements in `Source/Images/paper_abovewater_v05/` plus nine v03 images. Uniformly opaque water hides both body and submerged background; do not reintroduce rejected tiny-underwater-body edits. Scene/reference/provenance records remain in v07 assembly log and image generation journals. No source file discarded.
- Exact positive channel reference: Paper004userframe38:08,local`channels/paper_detour/videos/004_last_video/Storyboard/user_reference_parallax_20261101.png`; use current channel reference catalog for new work.
- No authorization to publish/upload. No new sound was made. Current local MP4 is v12; full 1× visual playback and subjective listening remain UNVERIFIED.

## History

Previous current-context text,permissions,IDs,statuses and all chronological source links retained verbatim in `Edit/CONTEXT_HISTORY_before_v11_20261102.md`. Historical assembly/cue/image/audio records are not deleted or rewritten as new acceptance. Read relevant record when that dependency changes.

Состояние после обновления 2026-11-02: в активном таймлайне нет Grain; применён мягкий параллакс целых сцен, новый MP4 прошёл decode и выборочную визуальную проверку. Предыдущий локальный v11 MP4 удалён после проверки v12; timeline/project, grain source asset и исходные изображения сохранены. Полный 1× просмотр и прослушивание остаются непроведёнными.
