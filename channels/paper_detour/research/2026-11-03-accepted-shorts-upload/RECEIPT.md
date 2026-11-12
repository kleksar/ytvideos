# Paper Detour — accepted review uploads, 2026-11-03

User accepted the shown IQ preview and requested upload of ready videos. These exact versions were previously shown and accepted; they remain review exports with incomplete final QA. Channel `UCMVfdfaNxV3ZkI3_J3Eejzw` verified through OAuth. API read-back: `api_readback.json`.

| Video | Local SHA-256 | New YouTube ID | Privacy/processing | Playlist | Thumbnail |
|---|---|---|---|---|---|
| IQ label animation | `4ce1497fce0180182697a6718e39b6bc9c8b892ca41f05b4be90cf94627ee8b5` | `ecfl1WVuyeo` | private / succeeded | `PLOSBLM3rTTl0`; item `UExPU0JMTTNyVFRsMC4yODlGNEE0NkRGMEEzMEQy` | v06 API accepted/readback matched; live pixels unverified |
| Boyfriend / parallax | `5aa46bd09217a348df713f8eadd87f6de335245d6a091b03b5a8928903516a10` | `Yz1Fn3GRsrw` | private / succeeded | `PLa2eDoWjSKkA`; item `UExhMmVEb1dqU0trQS4xMkVGQjNCMUM1N0RFNEUx` | accepted v02 JPEG conversion, API accepted/readback matched; live pixels unverified |
| Radio Short 02 v04 | `5045b616adb23bb7d0fd0a08f4a2c79583f4c682ebed3514c6e7c54cca1f284f` | `gc19EQoi-L0` | private / succeeded | `PLEIDCTZ8y2k8`; item `UExFSURDVFo4eTJrOC4yMDhBMkNBNjRDMjQxQTg1` | existing accepted cover, API accepted/readback matched; live pixels unverified |

Current title and description copied from fresh old-public-video readback. Three new uploads and playlist assignments verified. All are private: complete final QA / visible cover verification and applicable calendar review still outstanding; subtitle sync for Short 02 remains unverified on hearing. Existing public and private uploads remain unchanged. No audio changed, no cleanup or deletion. Exact upload state lives under `~/.local/share/story-youtube/paper-detour/` by individual video.

Already published Short 03 `pLU8w7hcGvE` and Minnie `L553TNYK6C4` were not duplicated. Existing earlier private copies `HdacCAb3ir0`, `1PdhvePinFg`, `Ox_77_Y7gUw`, `g95tLmrQ2VM` predate the newly accepted edits and must not be mistaken for these new versions. The old IQ, radio, and boyfriend public IDs remain `xYS2XBeR_Jc`, `7DygREwtxfY`, `sA-PYrDl5H8`.

## Public release — 2026-11-03

The user explicitly instructed publication of these three previously accepted previews after being told their review limitations. Authorized YouTube Data API `videos.update` was applied to each existing video, with before/intended/after saved in `public_<video ID>.json`. Channel ownership, exact IDs, privacy and processing were rechecked; all three returned Public and processing succeeded. Public YouTube oEmbed independently returned HTTP 200, expected title and Paper Detour author for each. Existing public originals and other private copies were not changed.

Studio content listing displayed no notices for these three and showed their uploaded cover images at small size, but an identity-verification prompt prevented detailed Studio inspection and inspection of scheduled community posts. Video calendar API inventory saved as `calendar_before_public.json`; no future video publication time was returned. Do not treat unavailable post calendar or image pixels as verified. Accepted videos retain their earlier explicit QA scope and UNVERIFIED statuses: no new claim of complete scene/cue review, independently heard speech/subtitle sync or independent QA. In particular Short 02 audible sync remains unverified. User approved release with these disclosed limitations. Audio unchanged. No deletion or cleanup.

## Old versions deleted; storage audit — 2026-11-03

Following the user's explicit request, deleted public old versions `xYS2XBeR_Jc`, `sA-PYrDl5H8`, `7DygREwtxfY` and superseded private uploads `HdacCAb3ir0`, `1PdhvePinFg`. All five deletions verified absent with a later API read; new `ecfl1WVuyeo`, `Yz1Fn3GRsrw`, `gc19EQoi-L0` remain Public. Individual pre-delete state and deletion receipts are in this directory. Previous public views before deletion: IQ 9, date story 13, radio 101; private IQ 1. Counts are a point-in-time read, not transferred to the new videos.

Read-only media-lifecycle audit/plan written under each of `003_iq_gallery`, `008_boyfriend_brought_friend`, and `001_radio_game` in `Edit/MediaLifecycle/{audit,plan}-release-cleanup-20261103`. Live Palmier discovery failed (connection reset/refused), reports identify 873 unresolved imports and five accessible packages; coverage is incomplete. Scoped workspace clean dry-run for 35 old radio QA scratch images refused due to the same discovery failure. Palmier UI currently shows a New Project save panel for an unrelated 038 task; it was not disturbed. No local media was deleted and no reclaim is claimed. Retry live dependency audit and authorized exact cleanup after Palmier connection is restored, keeping current exports and active other-session work safe.
