# Paper Detour 042 — YouTube release receipt v01

- Completed: 2026-11-03.
- Channel: Paper Detour, `UCMVfdfaNxV3ZkI3_J3Eejzw`.
- Video: `UqWIwpbTMik` — https://youtube.com/shorts/UqWIwpbTMik
- Uploaded asset: `Work/render-042-v09/previews/042_bird_migration_en_review_v04.mp4` (review preview), 130,333,052 bytes, SHA-256 `bbf951340478cab5cab914564f3c9b4f8cca36de219c3c0c0b683f390dddebba`.
- Upload receipt/state: `/Users/diplomat/.local/share/story-youtube/paper-detour/releases/042/upload-state-v01.json` (outside the project; no credentials stored in this receipt).

## Saved video fields

Fresh YouTube Data API read-back on 2026-11-03 returned:

The field-level result is saved in `YOUTUBE_API_READBACK_v01.json`.

- Title: `Did People Really Think Birds Flew to the Moon?`
- Description: exact approved paragraph followed by `#Shorts #BirdMigration #WhiteStork #Pfeilstorch #History #PaperDetour`.
- Separate Tags: empty array; no search tags were supplied or approved.
- Category `27`; default language/audio language `en`; made-for-kids `false`.
- Access `unlisted`; `uploadStatus=processed`; `processingStatus=succeeded`; no failure/rejection reason returned.
- `containsSyntheticMedia` was submitted as `false` with the upload. YouTube omitted that field from the post-release API read-back, so the saved value is `not_returned`, not independently verified.
- Privacy-update receipt: `/Users/diplomat/.local/share/story-youtube/paper-detour/releases/042/privacy-state-v01.json`.

## Cover and playlist

- User-selected cover A: `Thumbnails/Upload/PD042_A_arrow_v01.png`, SHA-256 `158f21c24253cb41ae2c14ed28185dc560c3d60e78f4a9e2c149efb5dadc0207`.
- Set in YouTube Studio on a computer, then saved and reloaded. Studio showed the uploaded cover in the Short's details form, the exact title/description, and `По ссылке`; all changes were saved. This is the UI-only Shorts cover route. No API thumbnail response was treated as proof.
- Playlist: intentionally unassigned while link-only. The matching `Real Stories & Discoveries` playlist is Public; membership there would make the Unlisted Short discoverable beyond the requested link-only release. No playlist or playlist access was changed.

## Scope and limits

- Native A/B experiment: not launched; YouTube's current Shorts eligibility excludes native title/thumbnail experiments. The user selected one cover/title pair.
- Independent post-render video/audio QA was not performed; the accepted input remains a review preview. This is not reported as QA-passed or final-master status.
- Studio read-back was performed on the channel's video details page after reloading. No claim is made about independent mobile-device display or a public search surface.

## Related project adjustment

The privacy-transition helper previously overwrote `containsSyntheticMedia` with `true` regardless of the video. It now preserves the currently returned value and changes only visibility. The project's current-process route check completed with no obsolete montage routes.

## Current local storage

- Following the user's Public-release and cleanup instruction, this accepted review-preview MP4 and episode-owned images, thumbnails, audio, caches and completed Work packages were retired under `Edit/MediaLifecycle/TEXT_ONLY_ARCHIVE_RECEIPT_v01.json`. The remote Public video remains available at the URL above. The original downloaded source in `Downloads` remains outside the episode archive.
