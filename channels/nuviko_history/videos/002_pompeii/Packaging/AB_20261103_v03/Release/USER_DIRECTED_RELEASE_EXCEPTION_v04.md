# User-directed release of accepted v04

Date: 2026-11-03

- Exact accepted media: `Work/subtitles-20261103-v04/previews/NuvikoHistory_002_Pompeii_Final_Hours_review_v04.mp4`
- SHA-256: `5212f7f04dcb607a642dd24e9e3895290c05ab1a30fc6b702efd209bf9c672ff`
- User acceptance: recorded in `MP4_ACCEPTANCE_v04.md`; full playback and spoken-word highlight sync confirmed by the user in `USER_AV_REVIEW_v04.md`.
- Project delivery preflight remains **not passed**: the rendered Nuviko subtitle padding is 18 px while the current profile is 29 px, and the standard Paper/Nuviko uploader refuses the plan's per-render style override. No delivery receipt is fabricated and this exception does not mark that check as passed.
- Direct user instruction on 2026-11-03: make the completed video public and delete the episode's images, video sources, and other media because they are no longer needed.
- Authorized scope: upload this exact accepted MP4 to Nuviko History, apply selected package B, upload its accepted English SRT, create the authorized public `History Documentaries` playlist and include only already-public long history films plus this release, verify the final Public state, then run the episode's TEXT_ONLY archive.
- Exception: execute the YouTube upload with the existing resumable YouTube Data API transport while retaining all mechanical identity/read-back checks. Do not present the release preflight or `delivery.json` as passed. This records the user's explicit release instruction; it does not change the global renderer or uploader policy.

## External operation record

- Upload: YouTube Data API resumable upload completed to channel `UCbyLx6Rf3iWww4bPZJ2oo2A`; video `3mhzbbbWA0g`; exact accepted MP4 SHA-256 above; upload initially Private.
- Metadata: selected B title, description with the reviewed 18 hashtags, tags, English video/audio language, not-for-kids setting, and synthetic-media disclosure sent. API read-back confirmed title, description hash, tags, language, audience and final access. API did not return the synthetic-media field; Studio showed “Да, ИИ использовался”.
- Thumbnail: `B_thumbnail_v04.png` SHA-256 `444c90fd29f99598e36173ed7112fb815af6dcaf9cf9ae8db3cf02865b11354a`; `thumbnails.set` accepted and thumbnail URL read-back matched.
- Captions: English manual SRT SHA-256 `321983ffa384b4a2d3c6942b2709e831c9498f25b4aa3c8f5d1fb5d679b69fe0`; caption ID `AUieDaY-2ydAyp_fWZBPWwf3vYlOQwngY-15xMxJ2cogfdHCH_10EYJn`; read-back `serving`, not draft.
- Playlist: public `History Documentaries`, ID `PLCtiNAU_98r0`; contains Black Death, Marseille 1720 and Pompeii. No Shorts or other unlisted videos were added.
- Public transition: `publish_public.py` confirmed Public and processing `succeeded`; final read-back at `2026-11-03T21:31:41Z` confirmed video ownership, title, metadata hash, Public access, processing, caption and playlist membership.
- A/B: YouTube Studio saved and displayed an active title-and-thumbnail test with B, A, C. Studio report showed “checking” and estimated 13 days 23 hours remaining. B is first/default; the description stays fixed to B. Results are pending. See `AB_EXPERIMENT_20261103.md`.
- Complete current API/Studio read-back: `RELEASE_READBACK_20261103.json`.
