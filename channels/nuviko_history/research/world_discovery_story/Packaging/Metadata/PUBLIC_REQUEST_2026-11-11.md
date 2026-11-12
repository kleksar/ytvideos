# Public release request — 2026-11-11

User requested immediate public release (“давай в открытый”) after approving the video and choosing package C. The permission applies to Nuviko History channel `UCbyLx6Rf3iWww4bPZJ2oo2A` and the approved 1080p file `Edit/Previews/world_discovery_PREVIEW_1080p_v01.mp4`, SHA-256 `6043a4049d6abfdda67e30e0ca32b2a3feb56302abe041f6fc0e93c6e7af621c`, with title “The Map of the World Was Never Finished” and `Packaging/Thumbnails/C_upload_candidate_v01.jpg`, SHA-256 `d5e7daa6d583ec18ff74101dc60e732be14f5f3ad75711f9fb288504644ba58a`. It also authorizes release-related upload and application of the selected package.

State when recorded: no upload or public release has been verified; the configured channel OAuth refresh failed with `invalid_grant`. A request to check alternate token files was rejected by automatic approval review as credential probing; no alternate credential was accessed. The current file has a known two-frame timestamp gap near 05:47, lacks a bound delivery receipt and has outstanding audiovisual and subtitle timing checks; see `Work/compact_preview_v01/RECEIPT.md` and `Work/preview_v01/QA_RECEIPT.md`. A/B, captions, playlist membership and end screen have not been verified on YouTube. Metadata JSON is a draft with attribution and chapter checks outstanding.

## Reauthorization follow-up

Google OAuth upload/read consent completed; `channels.list(mine=true)` returned channel `UCbyLx6Rf3iWww4bPZJ2oo2A` / Nuviko History on 2026-11-11 (Belgrade). New intended upload/read credential is in a separate protected file; no old credential was overwritten. Read-only playlist inventory returned private History Shorts (6) and public History Documentaries `PLCtiNAU_98r0` (13).

Separate request to start Google consent for `youtube.force-ssl` was rejected by automatic approval review because it grants broad management, including deletion, beyond explicit approval of that scope. No management token was created. Subtitles, playlist writes and Public transition remain blocked pending explicit user approval of this scope and Google consent. No video was uploaded or published.

## Management consent and calendar read — 2026-11-11

User explicitly approved requesting the wide YouTube management scope, including its ability to change/delete video; Google consent completed. `channels.list(mine=true)` with the new separately protected `youtube.force-ssl` credential returned exactly `UCbyLx6Rf3iWww4bPZJ2oo2A`, Nuviko History. No other video has been changed.

Read uploads playlist and all 22 returned video resources. Most recent public video `-8Ufspka8W4` has `snippet.publishedAt` 2026-11-10 17:17:38 UTC; no `publishAt` was observed on the 22 returned resources. As of the read on 2026-11-10 around 23:30 UTC, the project 8-hour minimum had not elapsed. If that timestamp is the actual public release time, earliest interval-compliant time is 2026-11-11 01:17:38 UTC / 02:17:38 Europe/Belgrade. `snippet.publishedAt` alone may not establish the exact time of a prior private-to-public change; verify actual publication time before relying on the estimate. Posts, queue outside this account and any future changes were not verified. Re-read calendar at actual release.

2026-11-11 check: approved 1080p derivative has no delivery receipt; uploader requires a receipt bound to this exact file and technical QA. Source 2K receipt cannot prove derivative provenance and must not be substituted. The sidecar timing review remains UNVERIFIED, and 2 frame timestamps are missing at ~05:47. No upload or publication performed.

## Published after user decision

User explicitly requested public release, was told of open technical and SRT checks, then instructed us to proceed regardless. The exact approved 1080p file was uploaded directly through the YouTube API as private without claiming a successful delivery receipt; actual upload receipt: `UPLOAD_RECEIPT_OVERRIDE_v01.json`. Channel ID `UCbyLx6Rf3iWww4bPZJ2oo2A`, video ID `HizfLrGkzNk`. Thumbnail C API accepted and read-back matched; playlist `PLCtiNAU_98r0` membership verified. Manual English SRT SHA-256 `f74792d72669cfd1747e092ce6851253e18df5808c681a07a42b7329908b1382` is serving, but audible alignment remains unverified. API verified processing succeeded and privacy Public: `PUBLIC_RECEIPT_OVERRIDE_v01.json`.

A/B and native end screen not configured: Chrome reported another extension UI blocking automation on the newly opened Studio edit page. The task-owned tab was closed; no attempt to bypass the block. Accepted media and thumbnail alternatives remain retained: lifecycle final cleanup requires verified A/B state. Storage state NOT_TEXT_ONLY; no media removed in this pass.

## A/B, end screen and cleanup follow-up

Studio confirmed title/thumbnail pair test running for C, B and A; its report showed review in progress and an estimate of 13 days 23 hours. Native end screen saved and reopened: Nuviko History subscribe and public related video `Gm_E_yZlxfU`, both 8:03:23–8:13:23. Public playback not separately tested. See `AB_ENDSCREEN_RECEIPT_20261111.json`. On user request 8526 episode-owned media files (3,460,685,037 logical bytes) moved to the macOS Trash as one staged object; no permanent deletion or disk-space reclamation is claimed. External references/music and text retained. See `CLEANUP_PLAN_20261111.json` and `CLEANUP_RECEIPT_20261111.json`.
