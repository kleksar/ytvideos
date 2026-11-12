# Endurance EN v04 — release in progress

2026-11-06: user requested publication to open access in the source thread. The request accepts the shown recommended B title, cover and description and the previously accepted v04 MP4 under root §7.

- Channel Nuviko History `UCbyLx6Rf3iWww4bPZJ2oo2A`; verified via API.
- MP4 `Deliverables/Endurance_en_review_v04.mp4`, SHA-256 `5cb856cda02053b40f0309a95617253a41aae457cf8d607b01eb8fbd724dc059`; current hash verified. Acceptance: `Edit/QA/ENDURANCE_USER_ACCEPTANCE_EN_v04.md`.
- Package: `ENDURANCE_RELEASE_PACKAGE_EN_v05.json`, B title/description/cover; upload metadata `ENDURANCE_UPLOAD_METADATA_EN_v01.json`. Education 27, EN audio and metadata, not made for kids, synthetic media declared. No separate tags supplied.
- API upload returned video ID `4-LLLu-LWfY`, https://www.youtube.com/watch?v=4-LLLu-LWfY. Read-back: `private`, processing `processing`. Transfer success does not establish completed processing.
- Thumbnail B API accepted and matched read-back; destination pixel preview not yet checked.
- Playlist `PLCtiNAU_98r0` History Documentaries: item `UExDdGlOQVVfOThyMC5DQUNERDQ2NkIzRUQxNTY1`, confirmed after insertion.
- English SRT upload preflight reported processing not yet succeeded; no caption POST performed. Retry only after processing succeeds. Private upload state is `~/.local/share/story-youtube/nuviko-history/endurance049-v04-upload.json` (contains sensitive upload state, do not publish).
- Still required: processing, manual English captions and read-back, checks, dynamic calendar, public publication, native A/B and status, then lifecycle cleanup. Studio showed both SD and HD processing. No publication or A/B start claimed.

## Verified public release and A/B

- YouTube API publication receipt: `confirmed`, `public`, `processing=succeeded`; Studio independently showed «Для всех», SD and HD processed. Video URL: https://www.youtube.com/watch?v=4-LLLu-LWfY.
- English manual caption `AUieDabkA4kM4H5tLLSBeLlmWAbiJ03ssNxXG7fgCr__4V3CHmDTnJMW`, `serving`, SRT SHA-256 `ea5413fa6e5e91f036943b7eb1f4c37dc6557fa9f7a42bbd4131f22385d18c34`. Playback/content of remote track not independently verified.
- Studio read-back confirmed synthetic/altered content «Да». API publish receipt did not return the field.
- Native paired title and thumbnail experiment saved and video page saved. Studio report shows three matching B, A, C pairs and status «Идёт проверка…», estimated 13 days 23 hours; no winner or impressions yet. Current test state is review pending, not a measured result.
- Calendar read covered the channel uploads and playlists; posts were not checked. Last other upload was 2026-11-06 10:14 UTC. The user directly requested public access, without a future time.
- Storage: `PARTIAL_TEXT_ARCHIVE`, no media removed in this pass. Episode directory measured 5.4 GiB (`Work` 2.7 GiB, `Deliverables` 2.6 GiB, `Edit` 54 MiB, `Packaging` 22 MiB, `Source` 9.5 MiB). Process inspection with `ps` was denied by environment, and no exact per-file consumer/writer inventory was completed; do not interpret empty `lsof` output as proof. Archive remains to be performed per lifecycle after fresh scope checks. Unverified playback and any active consumer hold only necessary files; do not blindly delete.
