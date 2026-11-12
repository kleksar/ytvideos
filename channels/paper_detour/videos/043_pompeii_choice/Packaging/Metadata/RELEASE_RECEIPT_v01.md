# Paper Detour 043 — YouTube release receipt v01

- Initial upload result: **uploaded and verified Unlisted** on 2026-11-03; current access is Public (see “Current release state” below).
- Channel: Paper Detour `UCMVfdfaNxV3ZkI3_J3Eejzw` (`@rarovista`).
- Video: [https://www.youtube.com/shorts/LQRdFHkgEPg](https://www.youtube.com/shorts/LQRdFHkgEPg), video ID `LQRdFHkgEPg`.
- Uploaded MP4: `Work/paper043-prod-v05/previews/043_pompeii_choice_EN_review_v04.mp4`; SHA-256 `5c48abfcd91eee6612fecfeb3d19d5b9d77f95b65b617bbc163edced4dc54316`; 92,978,104 bytes; H.264 1440×2560, 30 fps, 36.100 s; AAC mono 44.1 kHz. Exact user-approved MP4; no re-export.
- Upload processing: succeeded; SD and HD complete.
- Initial access read-back: API `unlisted`; Studio after reload displayed **По ссылке**. This was the upload-time state; the current state is Public, with no schedule.
- Title: `Pompeii: Run Through Falling Stones or Stay Inside?`.
- Description and distinct YouTube tags: exact read-back matches `release_metadata_v01.json` (language/audio language EN; category 27; made for kids false).
- Shorts thumbnail: selected A, `NO EASY CHOICE`. `thumbnails.set` accepted the 2160×3840 PNG (SHA-256 `d327b92e8a8fb88edf4efba8b919c1b5f6d8578f0353c711fcf8cca6d346a5b9`) and API read-back matched. After Studio reload the thumbnail image is visible in the icon and video previews; exact title and text are legible. A JPEG upload derivative was prepared and visually inspected locally, but the API submission used the PNG.
- Playlist: `Real Stories & Discoveries` (`PLEIDCTZ8y2k8`), Public playlist. Membership read-back confirmed one item, playlist item ID `UExFSURDVFo4eTJrOC5DNzE1RjZEMUZCMjA0RDBB`, position 18 of 18 at upload time. It now occupies position 18 of 19; existing order was preserved.
- Separate SRT track: **not requested**. Captions are burned into the MP4.
- Shorts native A/B test: unavailable; package A is the single selected title/thumbnail release. No experiment was started.
- Synthetic-content field: upload metadata sent `contains_synthetic_media: false` because the story is a clearly stylized paper-diorama animation. The current Data API read-back omitted this field (`not_returned`); Studio rendering was checked, but the declaration itself was not independently confirmed in Studio.
- Independent audio synchronization QA remains **UNVERIFIED** (25 local forced-alignment disagreements; no audible-sync claim). User acceptance of MP4 is recorded in `CURRENT_CONTEXT.md`.


## Current release state

On 2026-11-03, after the user's direct instruction to publish publicly, YouTube API `videos.update` changed this video to **Public**. A fresh read-back confirmed Public, processed, processing succeeded, and exact title/description/Tags and channel/video identity; no schedule or `publishAt` is set. The public page displayed the accepted title. See [Public release receipt](PUBLIC_RELEASE_RECEIPT_v01.md) and [TEXT_ONLY receipt](../../Edit/MediaLifecycle/TEXT_ONLY_RECEIPT_v01.md). The local approved MP4 and thumbnail files were retired after this verified release; their file paths below record historical upload provenance only.

## Initial upload read-back (Unlisted)

The initial upload `videos.list` read-back matched the exact video ID, channel, title, complete description, tags, category/languages, `unlisted`, processing `succeeded`, and `selfDeclaredMadeForKids: false`. The playlist read-back returned the new membership once at position 18 of 18 at that time. The custom thumbnail API write/read-back and refreshed Studio preview showed the chosen image. No external subtitle track was added. Current Public status and final processing state are recorded above and in the linked Public receipt.
