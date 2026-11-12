# Paper Detour 042 — YouTube release plan v01

- Target: Paper Detour (`UCMVfdfaNxV3ZkI3_J3Eejzw`), English Shorts.
- User's packaging selection: cover A + title B. Selected title: `Did People Really Think Birds Flew to the Moon?`. Selected cover: `Thumbnails/Upload/PD042_A_arrow_v01.png`, SHA-256 `158f21c24253cb41ae2c14ed28185dc560c3d60e78f4a9e2c149efb5dadc0207` (941×1672 PNG).
- Requested visibility: **Public**, explicitly instructed by the user on 2026-11-03; current status is confirmed in `YOUTUBE_PUBLICATION_RECEIPT_v01.md`.
- Exact accepted upload was the user-approved review MP4 `Work/render-042-v09/previews/042_bird_migration_en_review_v04.mp4`; SHA-256 `bbf951340478cab5cab914564f3c9b4f8cca36de219c3c0c0b683f390dddebba`; 130,333,052 bytes. Its local copy is retired under `Edit/MediaLifecycle/TEXT_ONLY_ARCHIVE_RECEIPT_v01.json` after Public confirmation. The render manifest classified it as `preview`; independent post-render QA was not performed.
- Original upload metadata: `UPLOAD_METADATA_v01.json`. Current description metadata: `UPLOAD_METADATA_v02.json`; full hashtag decision/evidence: `HASHTAG_REVIEW_v02.md`.
- Native YouTube title/thumbnail A/B experiment: not launched. YouTube Help currently excludes Shorts from native A/B testing: https://support.google.com/youtube/answer/16391400?hl=en .
- Shorts cover write route: YouTube Help directs custom Shorts cover selection to Studio on a computer: https://support.google.com/youtube/answer/72431?hl=en . The Data API thumbnail endpoint does not prove the Shorts poster selection. Save in Studio and verify the refreshed Shorts surface.
- Playlist membership remains unassigned; the current Public access request did not include a playlist change.
- Separate YouTube Tags: empty (`[]`); no search tags were supplied or approved. Description hashtags are preserved separately.
- Audience: not made for kids. Category 27 / Education; English metadata and audio. `contains_synthetic_media:false` based on the visibly stylized paper-diorama presentation; no realistic synthetic scene is presented as authentic footage.
- Upload: completed 2026-11-03. Video ID `UqWIwpbTMik`; URL https://youtube.com/shorts/UqWIwpbTMik .
- Current API read-back: `privacyStatus=public`, `uploadStatus=processed`, `processingStatus=succeeded`, and `selfDeclaredMadeForKids=false`; exact read-back: `YOUTUBE_PUBLICATION_READBACK_v01.json`.
- Thumbnail: Studio accepted `PD042_A_arrow_v01.png`; after save and reload, the selected thumbnail was visible in the form and the form had no pending changes. Visual evidence is the Studio thumbnail preview, not an API `thumbnails.set` response.
- Current metadata read-back: title, exact narrative and all 24 hashtags, empty Tags, category 27, default text language `en`, and made-for-kids setting matched the approved bundle. The API did not return `containsSyntheticMedia`; `false` was submitted on upload, but the final value is unverified. `defaultAudioLanguage` now reads `en-US` after the description update; it was `en` before and the difference's origin is unknown. Details: `YOUTUBE_METADATA_UPDATE_RECEIPT_v02.md`.
- Native A/B: not launched; Shorts are ineligible under the current official YouTube Help guidance.
- Independent post-render video/audio QA: not performed. The uploaded file is the user-approved review preview.
