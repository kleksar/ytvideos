# Paper Detour 043 — public access receipt v01

- User instructed immediate public release on 2026-11-03.
- Channel: Paper Detour `UCMVfdfaNxV3ZkI3_J3Eejzw` (`@rarovista`).
- Video: `LQRdFHkgEPg` — https://www.youtube.com/shorts/LQRdFHkgEPg.
- Calendar preflight (2026-11-03 20:39 UTC): API returned 22 recent uploads, zero future video schedules, and visibility counts of 18 Public / 4 Unlisted / 0 Private. The four newest uploads were published to the channel as Unlisted; their IDs are recorded in `PUBLIC_RELEASE_RECEIPT_v01.json`. Studio Posts showed three entries, each labeled Published, dated 2026-11-02 (two) and 2026-10-31; no scheduled entry appeared in the list. The user specifically instructed immediate Public for this Short.
- API method: YouTube Data API `videos.update`, `part=status`, existing `youtube.force-ssl` scope, exact owned video ID and ETag precondition. The request changed `privacyStatus` from `unlisted` to `public`, preserving license, embed setting, public-stat visibility and self-declared audience. No `publishAt` was present or set.
- Write response: HTTP 200. The first immediate API read still showed stale `unlisted`; after three bounded read-only checks, YouTube returned `public` consistently. A final fresh read verified exact title, description, separate Tags, channel ownership, Public access, no schedule, processed upload and `processing=succeeded`. Other status fields matched their before-state. Synthetic-content status remains `not_returned` by the API.
- The public Shorts URL opened in YouTube with the accepted title visible. The API read-back is the authority for Public visibility; the browser session was signed in.
- Before TEXT_ONLY cleanup, the local MP4 was verified against the accepted upload SHA-256 `5c48abfcd91eee6612fecfeb3d19d5b9d77f95b65b617bbc163edced4dc54316`. Existing independent audio-sync QA remains **UNVERIFIED**; this visibility change does not change that result.
- Detailed before/after status and calendar data: [PUBLIC_RELEASE_RECEIPT_v01.json](PUBLIC_RELEASE_RECEIPT_v01.json). Current description metadata: [release_metadata_v02.json](release_metadata_v02.json).
