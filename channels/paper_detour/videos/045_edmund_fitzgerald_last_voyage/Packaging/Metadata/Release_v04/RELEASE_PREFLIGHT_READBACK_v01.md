# Release preflight read-back — Paper 045 v07

## Authorization and current account

The user instructed on 2026-11-05: publish the current approved film Public and apply a native A/B experiment. Approval is recorded against v07 hash `e2a2ae29688a5737ed85f2323985fe895a12315362007fd2da9212a02364641d`.

A read-only `channels.list(mine=true)` check using the configured Paper Detour credential returned Paper Detour channel ID `UCMVfdfaNxV3ZkI3_J3Eejzw`. One other candidate credential resolved to a different channel and was discarded before any operation. No writes were made.

## Dynamic publishing state

Read-only YouTube API snapshot on 2026-11-05:

- Five existing playlists; `Real Stories & Discoveries` (`PLEIDCTZ8y2k8`) is Public and contains 25 entries.
- 26 recent upload items were checked for nonpublic/scheduled status. None were returned; the most recent upload activity was 2026-11-04 03:38 UTC. The explicit immediate-Public instruction supplies no schedule time.
- The recent activity feed was read; returned events were uploads and playlist-item changes. No future slot or release schedule appeared in the checked upload items.

## Delivery preflight

User acceptance is bound in the delivery receipt to this exact MP4. Receipt identity, input dependencies, renderer, source audio and subtitle contract are present. The local receipt's evidence references were normalized to current path/hash records without changing their review statuses. `delivery.validate_release()` now stops at `ValueError: Required delivery changes remain open`. Those open entries document `audible_sync` and full-film `visual_placement`; the review statuses are still `UNVERIFIED`.

The candidate SRT passes structure/text/wrapping checks, but it does not resolve the receipt's audible timing review. The prior review records 53 onset differences above 0.15 seconds versus a WhisperX estimate and says no full-track listening was performed. The global uploader's required preflight therefore blocks video upload before any API call. The native A/B pair test and Public transition were not attempted.

## Prepared upload defaults

`UPLOAD_METADATA_EN_v01.json` selects variant A as the default title/thumbnail pair and description A as the single fixed description during the pair experiment. Variants B/C are in `TITLE_CARDS_v04.md`. The native experiment supports three title-thumbnail pairs, but can start only after the target video exists and Studio state/eligibility are verified.

## Changes in this pass

- Recorded exact MP4 approval in the delivery receipt.
- Read channel, playlist, recent uploads and target playlist through the matching Paper channel credential.
- Prepared exact upload metadata and refreshed the playlist assignment proposal.
- No video, thumbnail, subtitle, playlist, metadata or experiment write was made to YouTube.
