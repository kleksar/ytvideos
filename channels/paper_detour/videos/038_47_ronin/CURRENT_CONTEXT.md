# Paper Detour — 47 Ronin

Updated 2026-11-04. English long film, registry entry Paper 038. Current scope: complete the approved YouTube release and start its approved native title/thumbnail experiment.

## Accepted media

- Accepted MP4 (retired locally after release; path absent): `Deliverables/47_ronin_en_v05.mp4`, SHA-256 `a1e897b48b87d000a7dcccff9d376b147ec559c87e633cfcc1d2132b7199512c`, 2560×1440, 30 fps, 568.355 s. User reviewed and accepted this exact file.
- Current delivery receipt: `Deliverables/47_ronin_en_v05.mp4.delivery.json`; release preflight passes. Subtitle review records 418/418 semantic groups, five sampled frames, user acceptance of caption fit, and a fresh 1,668/1,668 forced-alignment timing match. No coordinator continuous listening or independent review is claimed.

## YouTube state — verified 2026-11-04

- Paper Detour `UCMVfdfaNxV3ZkI3_J3Eejzw`; video `muokDIO62dg`; Public: https://www.youtube.com/watch?v=muokDIO62dg.
- Title A and description A are saved; category 27, English audio/language, not made for kids. Processing is `processed`; custom thumbnail A API write/read-back matched. The API returned no Tags field and no `containsSyntheticMedia` value.
- English manual SRT track is `serving`. The Public `Real Stories & Discoveries` playlist contains this video exactly once.
- Native end screen saved and reopened in Studio: Subscribe plus `lRkxm3mij5o` (“Galveston: The City That Raised Its Ground”) and `rsU6CkCwWjA` (“The Machine Gun Jammed. The Emus Kept Coming.”), all from 9:18:11 to 9:28:11. Targets were live-checked as Public, long-form, owned Paper videos before configuration.
- API read-back: `Packaging/Metadata/YOUTUBE_RELEASE_READBACK_20261104.json`. End-screen plan/read-back: `Packaging/EndScreen/END_SCREEN_PLAN_v04.md`.

## Remaining action

The approved three title/thumbnail pairs are in `Packaging/Metadata/AB_PACKAGE_EN_v02.md`; A/A remains the initial version and description A stays fixed. The native A/B dialog accepted the three titles, but the browser computer-use interface did not open a file chooser for thumbnail B/C after activation, so no experiment was saved or started. Continue from the Studio A/B dialog after enabling a file-picker path in the browser tool; upload the exact B and C derivatives from `Packaging/Thumbnails/AB_20261103/Upload/`, save, and read back that all three pairs are active. Do not claim that an A/B test is running until Studio confirms it.

## Storage — 2026-11-04

User requested removal of the source media of published videos while retaining audio and text. Fresh API status for `muokDIO62dg`: public, processed, processing succeeded. The accepted local MP4 and episode-owned scene images, previews, and generated visual media were retired; audio and text remain. A later explicit instruction removed all local images, including the selected A/B thumbnails. The approved test had not yet been started; the thumbnail files would have to be recovered or remade before starting it. The old local delivery receipt records the accepted file historically, not a present file. Storage is PARTIAL_TEXT_ARCHIVE due to retained audio and A/B assets. Exact per-file hashes and results: [primary plan](../../../../.agent/audits/cleanup-20261104/episodes-plan.json), [additional media](../../../../.agent/audits/cleanup-20261104/episodes-extra-plan.json). YouTube was not modified.

Later cleanup 2026-11-04: all remaining local pictures and videos were deleted at the user’s explicit direction; audio and text remain. See [cleanup record](../../../../.agent/audits/cleanup-all-visual-20261104/REPORT.md).
