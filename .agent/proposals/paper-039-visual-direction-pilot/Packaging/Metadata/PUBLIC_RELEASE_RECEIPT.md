# Public release — 2026-11-07

- Paper Detour / The Great Emu War, channel `UCMVfdfaNxV3ZkI3_J3Eejzw`, video `aS3TxDoPjjU`: https://youtu.be/aS3TxDoPjjU
- User directly requested public release; exact upload SHA-256 `660587120d7588961c4c8eea2130795b5a5632cf920b205211b7ac1443dd1fca`. API readback: public; processing succeeded; manual English captions serving; playlist membership verified (see Private upload receipt for exact ID).
- Studio 2026-11-07: three title and thumbnail variants saved, then main Save; status for title and thumbnail test reads `Тестирование…`. Variants: Australia Sent Soldiers to Fight Emus; The Birds the Machine Guns Couldn’t Stop; Why Farmers Asked the Army to Fight Emus. Thumbnail A/B/C uploaded. No winner yet.
- Prior public version `rsU6CkCwWjA` remains unchanged. Native end screen not configured; final ten seconds contain narration. Independent listening/playback not established by publication.

## Cleanup plan

After confirmed public and active A/B, retiring accepted MP4: `Deliverables/review_v02.mp4`, 768365981 bytes, SHA-256 above, inode 129569105, link count 1. No open file found by bounded lsof at inspection. Move to macOS Trash with `trash`, verify exact destination and hash; no irreversible removal authorized under environment. Other episode media remain pending bounded consumer/ownership inventory, with unknown consumers treated as hold. Trash on the same volume does not itself reclaim space. Storage state PARTIAL_TEXT_ARCHIVE until remaining media and Trash are resolved.

## Cleanup result

- One file, 768365981 logical bytes, moved to `/Users/diplomat/.Trash/review_v02.mp4`; inode and SHA-256 verified at destination; original path absent. No permanent deletions. Available space 37,999,368 KiB before and 37,732,688 KiB after; concurrent writes/APFS prevent attributing difference to this move.
- Remaining episode directory approximately 2.6 GiB including source and generated media: PARTIAL_TEXT_ARCHIVE, pending exact ownership/consumer inventory and permitted permanent removal. Trash object also remains and still occupies space. No claim of reclaimed space or complete archival.

## Follow-up cleanup, 2026-11-07

Fresh API readback using the matching Paper account: `aS3TxDoPjjU` public, processed, processing succeeded. The original accepted hash and publication receipt establish upload identity; previous Studio readback established the A/B test. Bounded external-consumer search found no other episode referring to this pilot path, and `lsof +D` found no open files before staging. 9,563 episode-owned media files, 2,775,798,705 logical bytes, moved preserving relative paths to `/Users/diplomat/.Trash/paper039-retired-media-20261107`; each destination inode, byte count and SHA-256 verified. Exact former paths and hashes: `CLEANUP_PLAN_20261107.json`; result: `CLEANUP_VERIFICATION_20261107.json`. The earlier accepted MP4 remains separately at `/Users/diplomat/.Trash/review_v02.mp4` (768,365,981 bytes, SHA-256 above). Neither object permanently deleted; no space-reclaimed claim. Free-space snapshots: 48,305,984 KiB before and 48,074,172 KiB after; unrelated concurrent activity and APFS prevent attribution. External music and reference image retained under `music/Constance_Kevin_MacLeod.mp3` and `references/AWM_REL_10285_Lewis_Mk1.jpg`; shared/external materials excluded. Text archive retained. Storage remains PARTIAL_TEXT_ARCHIVE until exact Trash objects can be removed with explicit confirmation.

## Final deletion, 2026-11-07

At the user's direct request to finish this episode cleanup, 9,563 exact staged files plus the separately verified accepted MP4 were permanently deleted from the two specified Trash locations: 9,564 files, 3,544,164,686 logical bytes, no errors, no remaining staged directory. `CLEANUP_DELETION_20261107.json` records execution. Free space was 48,305,984 KiB before staging and 51,140,280 KiB after deletion; concurrent system activity and APFS mean the difference cannot be attributed solely to cleanup. The earlier partial-status text above is historical; the user subsequently authorized completing cleanup. Two external source files remain under music and references as required by root §9, so directory state is PARTIAL_TEXT_ARCHIVE despite removing all inventoried episode-owned generated media.
