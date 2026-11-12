# Current context — Paper Detour 028

**Очистка 2 ноября 2026:** устаревшие локальные материалы удалены по поручению пользователя; актуальные пути и ограничения восстановления — в [CLEANUP_RENDER_20261102.md](CLEANUP_RENDER_20261102.md). Прежние упоминания наличия удалённых файлов ниже исторические.


## Current release

- Video **fvRm9Vxwagk**, https://www.youtube.com/shorts/fvRm9Vxwagk — **Public**, Paper Detour `UCMVfdfaNxV3ZkI3_J3Eejzw`. User reported publishing; read-only API check at 2026-11-02T01:13:06.282099+00:00 confirmed Public. Agent performed no publication/scheduling mutation. [Current publication receipt](Packaging/Metadata/PUBLICATION_CURRENT_20261102.md). Original Private upload authorization and receipts are retained.
- Current title: **The Taj Mahal Cost Him His Hands**, 32 characters. Original title clipped on the actual responsive Shorts surface; shortened after a separate Extra High check, applied via API while preserving other fields. Exact current metadata: `Packaging/Metadata/YOUTUBE_METADATA_CURRENT_20261102.json`. Original upload metadata snapshot retained unchanged for resumable-state fingerprints.
- Current external evidence: [publication read-back](Packaging/Metadata/YOUTUBE_PUBLICATION_READBACK_20261102.json); original [Private upload receipt](Packaging/Metadata/YOUTUBE_UPLOAD_20261102.md) and [Private read-back](Packaging/Metadata/YOUTUBE_READBACK_FINAL_20261102.json) are historical. Public/no future schedule, processing succeeded; accepted English audio/metadata preserved. HD was verified during Private QA. Description has #TajMahal #PaperDiorama #HistoryShorts #Shorts; separate Tags empty.
- Playlist `PLa2eDoWjSKkA`, Legends & Personal Stories, position 3; item `UExhMmVEb1dqU0trQS4wOTA3OTZBNzVEMTUzOTMy`. Previous three members/order and playlist Public access preserved. Manual sorting verified before insert; final membership reread after all writes.
- Cover PRAISED. THEN PUNISHED. API stored the correct standard image but did not select the separate Shorts poster. A documented Studio-only fallback applied the same JPEG; save/reload and fresh actual desktop plus responsive 390×844 Shorts surfaces showed the correct image and full title. Receipt: `Packaging/Metadata/YOUTUBE_SHORTS_THUMBNAIL_UI_RECEIPT_20261102.json`.

## Accepted local film

- Language English; conversation Russian. Accepted narration `Source/Script/NARRATION_EN_v01.md`, existing voice `Source/Voice/lawrence_v01/voice_en.mp3`. User-provided dramatic anecdote; no independent historical verification. Do not add unwanted “allegedly/legend” disclaimers to the accepted narration.
- Final delivery the previous delivery recorded in the export receipt: 1066 frames, 35.533333 s, 1080×1920, 30 fps, H.264 High, AAC-LC mono 192 kbps. SHA-256 `add9aa0f2a9add86b662b550e0d8b91fb7d22db2c45ed2670f3ad3839fac2bf8`. Export evidence `Storyboard/QA_Export_v10.md`.
- Palmier project `25A8FF9A`, timeline `8565580B`, snapshot `33A6FC2A`; original v01 preserved. Shared media `2200F995`, clips `486DD2CD`/`4341B274`/`0D80E013`/`E7CAAE18`, film range [0,1066), above Main and below phrase PNGs.
- Eight scenes S01/S02/S03/S05/S06/S07/S10/S11; cuts 0/126/261/396/531/657/795/945/1066. Existing scene/cue/dialogue timing and keyframes preserved. Gentle whole-frame camera motion explicitly authorized for this episode. Seven phrase accents: `Storyboard/CUE_SHEET_EN_v03.md`. Final question joins opening answer.
- Audio authorization remains existing accepted source plus AAC 192 re-encode; no new voice/music/SFX. No separate SRT: selective accents only.

## Verification limits

- Technical file checks, full decode, frame count and source-to-AAC signal/timing comparison passed. Actual YouTube 1080p playback reached duration 35.561 s, ended=true, unmuted, rate 1. [Player evidence](Packaging/Metadata/YOUTUBE_HD_PLAYBACK_20261102.json).
- Player execution is not continuous subjective viewing/listening. Tool does not transmit system audio; pronunciation, perceived mix and subjective AV sync remain unverified. No independent reviewer used. Public channel grid and native phone app remain unchecked; earlier responsive Chrome cover/title checks were performed while Private. Publication read-back adds no subjective AV review.
- Earlier pre-upload records are historical. Current release state is the verified receipt above. No further external action is implied by preparation or the existing private upload.

Текущая техническая очистка2026-11-02: основной монтаж, титры и звук сохранены; для обновлённого edit требуется новый export/QA. Общая квитанция — `.agent/OVERLAY_CLEANUP_20261102.json` от корня проекта.

## Saved expanded metadata — 2026-11-02

User authorized catalog metadata updates and explicitly allowed coordinator fallback after Extra High returned no result twice. Saved/API-verified title **The Taj Mahal Cost Him His Hands #TajMahal #Shorts**;description has11hashtags. [Current fields](Packaging/Metadata/METADATA_CURRENT_fvRm9Vxwagk_20261102.json),[receipt](Packaging/Metadata/EXPANDED_METADATA_RECEIPT_20261102.json). Actual privacy **public** unchanged;old cover/playlists/languages/Tags preserved. Earlier metadata strings above are historical;media/layout cleanup changes remain intact.


<!-- storage-rollout-20261102 -->
Storage layout and current local availability were audited on 2026-11-02: [migration record](Edit/MediaLifecycle/rollout-20261102/REVIEW.md). Imported paths and active work are preserved; use `Deliverables/current.json` together with the episode’s QA and current edit.


## Caption update in progress — 2026-11-03

- Subtitles v01 draft uses the existing EN v01 narration and `voice_en.alignment_clipped.json`, grouped into 40 exact-text cues (95 words). No voice file or alignment was changed.
- Review-only MP4: `Work/tajmahal_subtitles_20261103_v01/previews/captions_review_v04/shorts_subtitles_review.mp4`, SHA-256 `7f50463d1b194d0c84436851951c9cd02e0988fcf0f8a74153a5cc3bdeec3f9b`. It is based on a YouTube download because the accepted local v10 MP4 was deleted in the 2026-11-02 cleanup. Use for caption/composition review only; do not promote or upload. Its AAC stream is an exact copy of the YouTube-derived input, not proven byte-identical to the deleted v10 audio.
- Automated pause/ASR reconciliation is `REVIEW_REQUIRED`: 38 flags, no word times changed. Keep heard-sync and cue timing `UNVERIFIED` until reviewed against the retained recording.
- Offline inspection report: `Edit/QA/tajmahal_caption_review_20261103_v01/report.json` (technical PASS; overall verdict UNVERIFIED). Visual sample receipt: `Edit/QA/tajmahal_caption_review_20261103_v01/reviewer_receipt.json`; 84 representative frames across scenes, cuts, subtitle and accent cue regions inspected. Text placement looked clear in sampled frames; full motion-path review remains UNVERIFIED.
- Local parallax review preview is now available at `Work/tajmahal_subtitles_20261103_v01/previews/captions_review_v06/shorts_subtitles_review.mp4`. It uses the 35.533 s, 1080×1920, 30 fps Palmier image-motion timeline `A40393B6`; eight still scenes were rendered as depth-parallax clips with their existing camera keyframes preserved. The native export is `Work/tajmahal_subtitles_20261103_v01/previews/parallax_review_v01/palmier_parallax_no_subtitles.mp4`. Audio is the original Dialogue mediaRef `87DB1704`; the subtitle pass copies the AAC stream exactly (matching stream hash). The quote-free subtitle rule is in the canonical subtitle skill; this render has 40 groups / 95 words and no straight or curly double quote marks.


## Parallax and subtitle review — 2026-11-03

- Motion run and binding: `Edit/ImageMotion/a00b2d187da8ef459182/run.json`; pre-render contract: `Edit/ImageMotion/a00b2d187da8ef459182/export_contract_v01.json`; export receipt: `Edit/ImageMotion/a00b2d187da8ef459182/export_receipt_v01.json`. Target is timeline `A40393B6`; source timeline `8565580B` remains unchanged.
- The whole-image depth parallax is rendered for all 8 scene clips using prepared maps and the existing four-key camera paths. The 40-frame scene/keyframe sample showed no visible black borders or subject deformation. Full-motion review remains incomplete.
- Quote-free screen subtitles are implemented by the canonical subtitle skill and helper. They remove straight/curly double quote glyphs from subtitle tokens only; the accepted narration/script and voice are unchanged. The actual render has no visible quotation marks.
- QA run `Edit/QA/tajmahal_parallax_subtitles_20261103_v03/`: stream metadata and full decode PASS; technical status PASS; overall verdict UNVERIFIED. Of 228 extracted samples, 79 inspected (40 subtitle-group midpoints plus 40 scene/keyframe samples, with one overlap). Visual samples showed no subtitle/accent collision. Cue sync remains unverified because the alignment is still REVIEW_REQUIRED and listening did not occur. Audio AAC stream matches exactly between native export and captioned review file.
- Accepted v10 grain source `2200F995` is absent from the live Palmier media library; API insertion was rejected as unavailable. This preview has no grain layer, and the earlier clean-parallax branch remains separate. No YouTube mutation was performed.
- Next: user reviews the complete preview; before any release, resolve grain/source choice if needed, complete remaining required frame/motion and cue/audio checks, and follow the release skill.

## Gentler parallax review — 2026-11-03

- User requested weaker depth movement and easing. New baseline-derived run `Edit/ImageMotion/563fd317bd283338cf20/run.json`, timeline `239B6743`, preset `framing-safe`: offset 0.12 vs 0.165 and height 0.20 vs 0.26. Depth trajectory uses the existing cosine ease; source camera keyframes were kept unchanged (`smooth` between held ends). `camera: existing` does not apply the preset camera factor.
- Review MP4: `Work/tajmahal_subtitles_20261103_v01/previews/captions_gentler_v07/shorts_subtitles_review.mp4`, SHA-256 `43c9d49d367195f516a031dddef0ba1566395e29e063d1c1fda01e8ec94e3691`. Existing Dialogue track and quote-free caption grouping retained; AAC stream is byte-identical to the native Palmier export. Accepted v10 grain source remains unavailable, so this preview has no grain.
- `Edit/QA/tajmahal_gentler_parallax_20261103_v01/`: technical PASS; overall UNVERIFIED. Twenty-four scene start/mid/end samples visually reviewed with no obvious border or text overlap; full motion, detailed cue edges and audible sync remain unverified. No YouTube changes.


## Motion from scene cuts — 2026-11-03

- User requested removal of entry pause and smooth motion immediately from each cut. Isolated timeline `8996BA59` copied from `239B6743`; per-scene position/scale keys start at frame 0 with smooth interpolation instead of a six-frame hold. Original 8 depth-parallax clips and their cosine trajectories remain unchanged, so their very slow initial acceleration can still look subtle. Other tracks, clip ranges, media refs and voice were preserved. Evidence: `Edit/ImageMotion/no_initial_hold_20261103/`.
- Review MP4: `Work/tajmahal_subtitles_20261103_v01/previews/captions_no_hold_v08/shorts_subtitles_review.mp4`, SHA-256 `156f5793e69a41c98dfec1b440ac1d39c0af904d70972ad32e19edc4a5020868`. Its AAC bitstream matches the preceding candidate exactly (SHA-256 `10ee65ef372483e7250a5092ecc6a56186313e28829e06723e75f9347edbd568`). Subtitles remain quote-free. Grain asset remains unavailable as before.
- Technical QA PASS, final verdict UNVERIFIED: `Edit/QA/tajmahal_no_hold_20261103_v01/`. Reviewed 40 entry frames across all eight scenes; continuous motion and heard subtitle sync remain unverified. No publication changes.


## No depth parallax — 2026-11-03

- User requested removal of added depth parallax. Isolated timeline `C1634F50` is cloned from original still-image baseline `8565580B`: all eight Main clips use original image media, no rendered depth videos. Existing camera paths retain smooth animation from frame zero with the previous six-frame holds removed. Other tracks and timing preserved. Evidence: `Edit/ImageMotion/no_depth_20261103/`.
- Review MP4: `Work/tajmahal_subtitles_20261103_v01/previews/captions_no_depth_v09/shorts_subtitles_review.mp4`, SHA-256 `b6276c13dc6c7226a8e76cd7933ff53213628346a834e69f3ba7ef68dbcc601e`. AAC bitstream matches preceding preview exactly (`10ee65ef372483e7250a5092ecc6a56186313e28829e06723e75f9347edbd568`); subtitle groups retained. Accepted v10 grain source is still unavailable, so this preview has no grain.
- Technical QA PASS; overall UNVERIFIED. Visually reviewed 24 scene start/mid/end frames; full motion and heard sync remain unverified. QA `Edit/QA/tajmahal_no_depth_20261103_v01/`. No YouTube mutation.


## Batch decision — 2026-11-03

User explicitly said to skip this video and move on. Leave its public video and all local sources/preview versions as they are; do not continue this Taj Mahal rework or upload/delete it as part of the current batch unless the user returns to it.
