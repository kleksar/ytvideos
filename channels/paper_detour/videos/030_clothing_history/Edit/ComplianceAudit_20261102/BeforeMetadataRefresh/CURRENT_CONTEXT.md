# CURRENT_CONTEXT — Paper Detour030 Clothing History

## Current local delivery — v13

[MP4](Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v13.mp4) · [separate EN SRT](Deliverables/PAPER_DETOUR_030_CLOTHING_HISTORY_EN_v13.srt).190s,16:9,1920×1080,30fps.39scenes,4.1667–6s;33paper accents. All39scenes have depth parallax and whole-image camera motion. Grain/Ripple overlays absent.

Accepted story: [RUv04](Source/Script/NARRATION_RU_v04_20261102.md); actual voiced text: [ENv05](Source/Script/NARRATION_EN_v05_20261102.txt). Existing Lawrence voice/music/SFX mix preserved bit-for-bit as AAC; no new audio generated.83SRTcues unchanged.

Current [shotlist and actual camera keys](Storyboard/SHOTLIST_v13.json), [accent cues](Storyboard/CUE_SHEET_v13.json), [provenance](Source/Production/MEDIA_PROVENANCE_v13.md), [QA](Edit/v13/QA/REVIEW.md), [measurements/hashes](Edit/v13/QA/REPORT.json).

## Exact editable version

Palmier project **B1BA2D18**, final isolated timeline **82684371**, `Clothing History v13 — full parallax and camera animation`; final snapshot **948BCAAD**. Baseline **A7C273C5** and archive versions retained. Only API edits; no manual `.palmier` edits.

Common [motion config](Edit/ImageMotion/motion.json) and [PNG bindings](Edit/ImageMotion/sources_v13.json); common pipeline [run](Edit/ImageMotion/f2eb90506b76cbdabfa3/run.json). Selected gentle-aligned preset: same visible horizontal direction, motion25%less than strong/reference, alternating depth direction for zoom/vertical moves. Scene-specific depth framing retained.

After the common apply, addressed native-verified fixes: D06 omitted to expose main stone blade; D10 uses approved alternate anchor; V27/V29/V31 camera keys widened to keep hats/feet inside frame. [Final edit state](Edit/v13/POST_EDIT.json) is authoritative; helper run fingerprint predates these fixes. Do not reapply over this edited target. [Actual timeline](Edit/v13/timeline_final.json).

## Authorizations and visual decisions

User accepted RUv04 and authorized voice/music/SFX/fullmix and final video, then explicitly requested motion, more paper text, depth parallax, grain removal and unused-render cleanup. **Extra High waived for030.** No delegation. One complete paper diorama per scene, whole-image motion, direct cuts. D23 ends at a clip cut; final C06 holds to film end.

River/crossing is the recurring motif; future museum is an artistic metaphor. V25 uses the accepted wide V23 image. V30 is an intentional torso detail in the accepted source. Original PNGs preserved. Accepted A/B/C covers and [thumbnail grammar](../../brand/CLOTHING_HISTORY_THUMBNAIL_GRAMMAR.md) retained.

## Verification and cleanup

Final video/audio decode PASS; video payload matched native export and AAC matched accepted mix. Author reviewed277actual exported frames covering all39scenes and33accents, plus preflight/depth samples. In final samples: motion visible, hats/feet fit after correction, no empty edges or face occlusions observed.

**Full190s1×playback with sound/listening and subjective sync/balance/pronunciation remain UNVERIFIED. Independent AV review NOT_PERFORMED.** Machine checks and frame samples do not establish those checks.

[Unused-render cleanup](Edit/v13/RENDER_CLEANUP.json), [final derivative cleanup](Edit/v13/FINAL_RENDER_CLEANUP.json). Removed unused library entries, unreferenced previews/helper/probe renders, rejected/native duplicate exports and old duplicate delivery SRT. Imported motion MP4s required by existing timelines, original PNG/audio/mix, depth cache, project files, logs and QA images retained. Current delivery has one EN MP4/SRT pair.

Grain removal was completed by the concurrent user-authorized global cleanup and [verified here](Edit/v13/grain_removal_verified.json); [global receipt](../../../.agent/OVERLAY_CLEANUP_20261102.json). No upload/publication in this task. Historical private tests remain external and are recorded in the archived context.

Previous context: [beforev13](Source/Production/CONTEXT_BEFORE_V13_DELIVERY_20261102.md). Earlier version records are historical; this document is the current entry.

## Separate user-authorized grain review — Test03

The current chat explicitly authorizes isolated15-second grain previews on the accepted earlier parallax excerpt; v13 production delivery and its grain-free edit stay unchanged. Test01 (`8PwziOHGxag`) was deleted locally/fromYouTube as requested. [Test02](https://www.youtube.com/watch?v=4ZkHRuUEaYE) used amplitude×4 (RMS4.8), sigma1.0UHDpx. The user now requests **amplitude×3 (RMS3.6), grain15%larger (sigma1.15)** and another private upload. [Test03 preset/journal](Edit/Grain_Test_20261102_v03/REVIEW.md); source remains the same clean71.533s reference MP4, frames811–1260/V07–V09,450frames/15s,UHD30p,AACcopy. [Test03 private preview](https://www.youtube.com/watch?v=NcJAyqebXC4), ID `NcJAyqebXC4`, is uploaded and processed: API private/processed/succeeded and metadata readback PASS; player3840x2160@30/VP9/BT.709 verified. Local technical QA PASS; user acceptance pending. No general production preset change. The exact source/Test02/Test03 are pinned in storage policy; bounded preflight audit/plan are linked in the Test03 journal, no deletion performed.

Test03 storage follow-up: [bounded post-upload audit](Edit/MediaLifecycle/grain03-postupload-audit/audit.json) / [plan](Edit/MediaLifecycle/grain03-postupload-plan/plan.json). No deletion authorized by these audit-only reports; source/Test02/Test03 remain pinned. No changes to the v13 production timeline/delivery.


## Хранение и миграция 030 — 2026-11-02

Пользователь прямо разрешил перемещение/удаление существующих медиа для улучшения архитектуры. [Текущий storage report](Edit/MediaLifecycle/migration-20261102/REVIEW.md), [layout](Edit/MediaLifecycle/layout.json), [карта зависимостей](Edit/MediaLifecycle/dependencies.json), [current MP4/SRT pointers](Deliverables/current.json). Восемь pinned сравнений v07–v10 перенесены в Work/legacy-storage-20261102/previews с compatibility aliases; семь подтверждённых QA scratch файлов удалены (1,031GiB logical). Все239учтённых imported/source/shared файлов, финальная пара и live timeline82684371 проверены неизменными. Imported legacy paths сохранены; активные grain/compliance scopes не затронуты. Свежие QA-проходы складывают кадры в Work, отчёты/evidence — в Edit. Предыдущий запрет удаления относился к прежней задаче и историческому audit, не является текущим scope этого поручения.
