# Nuviko History — Pompeii Public release preflight

Date: 2026-11-03. User directly requested a Public upload. Target resolved by live API: Nuviko History, channel `UCbyLx6Rf3iWww4bPZJ2oo2A`. Selected release package: variant B, title/description in `upload_metadata_B_v01.json`, thumbnail `../Thumbnails/B_thumbnail_v04.png` (SHA-256 `444c90fd29f99598e36173ed7112fb815af6dcaf9cf9ae8db3cf02865b11354a`; 1672×941). Hashtags: [review v01](../Hashtags/hashtag_review_en_v01.md).

## Final state

The exact accepted v04 is Public as `https://youtu.be/3mhzbbbWA0g`; processing is `succeeded`. The approved B title/description/tags and thumbnail are saved, the manual English SRT is `serving`, and the public `History Documentaries` playlist (`PLCtiNAU_98r0`) contains only the two previously public long films plus Pompeii. YouTube Studio shows the native title-and-thumbnail A/B/C test as active/checking; B is first/default and the B description stays fixed. Exact read-back: [RELEASE_READBACK_20261103.json](RELEASE_READBACK_20261103.json); experiment contract/status: [AB_EXPERIMENT_20261103.md](AB_EXPERIMENT_20261103.md).

The delivery receipt gate did not pass because v04 has a 18 px subtitle padding override while the active profile says 29 px. Per the user's direct instruction to release this exact accepted file, a one-release API exception was used and recorded in [USER_DIRECTED_RELEASE_EXCEPTION_v04.md](USER_DIRECTED_RELEASE_EXCEPTION_v04.md). No false delivery receipt was created, and the global gate remains unchanged. Public/A-B/API read-back is complete; TEXT_ONLY cleanup is now in progress under the user's direct request.

## Fresh channel state

- `channels.list(mine=true)` resolved the exact target channel.
- `playlistItems.list` for its uploads playlist returned 5 entries, one page. Current reads showed 3 public videos and 2 unlisted; none has a future `publishAt`. The recent public upload cadence is dense on 2026-11-03; the user's direct immediate Public instruction governs this release.
- YouTube Studio `Content → Posts` showed “Publish your first post”; no community posts were present.
- YouTube Studio `Content → Playlists` showed no playlist rows/content. The API `playlists.list(mine=true)` response was inconsistent (`totalResults=5`, zero returned item rows), so no stable playlist ID is verified. The user has now authorized a public `History Documentaries` playlist containing the already-public long history films and this release; exclude unlisted videos and Shorts.
- The user confirmed full playback of this exact v04 and that spoken-word highlighting matched. This resolves audible-sync evidence by user attestation, not independent review.
- No release, upload, thumbnail, metadata, caption or playlist mutation was executed in this task.

## Release blockers

1. Historical preflight blocker: the current adapter would not produce a delivery receipt for the v04 style override; this was handled only through the recorded one-release user-directed API exception.
2. The exact MP4 user acceptance, full-playback sync attestation, uploaded captions and all available read-backs are retained in the release records. Independent AV review was not performed.
3. Public upload, caption, thumbnail, playlist, processing and active A/B state are complete; see the linked read-back above.

The official YouTube upload adapter is private-only and requires the delivery receipt; the public transition script checks the playlist, caption, processing and original upload receipts. The user has since directly instructed that this exact accepted video be made Public and the episode media deleted. That explicit instruction authorizes a one-release API exception recorded in [USER_DIRECTED_RELEASE_EXCEPTION_v04.md](USER_DIRECTED_RELEASE_EXCEPTION_v04.md); it does not turn the missing delivery receipt into PASS or alter the global uploader policy. Continue to retain exact media identity, channel ownership, upload state, thumbnail/SRT/playlist read-backs, and final Public verification before lifecycle cleanup.
