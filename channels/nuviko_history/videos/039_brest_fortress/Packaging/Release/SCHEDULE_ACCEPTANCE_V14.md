# Release instruction and schedule plan, V14

User instruction: «откладывай на завтра на 7 утра по белграду в открытый». Received 2026-11-07. This authorizes publication on 2026-11-08 at 07:00 Europe/Belgrade (06:00 UTC), and constitutes acceptance of the current exact MP4 and selected packaging under project root §7. This records the instruction; it is not an independent observation of the user's playback.

MP4 SHA256 e0b791d0baf22f8b927a630b9121ba8fe266ae06ebc3a3f8d1f13933fdc4304d. Video 1H2-Pj7thHY, channel UCbyLx6Rf3iWww4bPZJ2oo2A. Selected title: The German Report That Revealed Brest Fortress’s Defiance; thumbnail A. Manual English SRT SHA256 2071c7daa59815e871a7721e8833a7e4967464ff3f8bfb9d8802e302cac1589c.

Channel uploads API checked 2026-11-07: 15 videos including the private new video and recent public releases; no scheduled publishAt returned. The previous Brest edition 1Zxdf06ckhA remains public. Community posts and independent local queues were not fully checked; no claim the slot is clear. Exact time is directly requested by user.

SRT structural parsing, literal text order and word-map boundary matching are documented in Edit/QA/audio-sync-v13/srt_map_check.json and Edit/QA/audio-sync-v14/REVIEW.md: 192 cues, 1555 words, 0 mismatches, boundary tolerance 2ms. Audio stream timing is unchanged. Listening and independent subjective synchronization remain unverified.

## Saved schedule read-back

The schedule adapter returned an inconclusive response and recorded `outcome_unknown`. A separate fresh read-only YouTube API request subsequently confirmed channel `UCbyLx6Rf3iWww4bPZJ2oo2A`, video `1H2-Pj7thHY`, `privacy=private`, `publishAt=2026-11-08T06:00:00Z` (07:00 Europe/Belgrade), and `processing=succeeded`. Private is the normal pre-publication state for a scheduled video. No repeat mutation was performed. The protected adapter receipt retains its original uncertain-write record; this later independent read resolves the saved scheduling state.

A/B is not started for a scheduled release. Three candidate titles and thumbnail paths are retained in `Packaging/Metadata/REBUILD_v13_PACKAGING.md` and `Packaging/Thumbnails/rebuild_v13/` for later use. The historical public video was not changed.

## Archive status

`PARTIAL_TEXT_ARCHIVE`: no media removed or moved in this pass (0 files, 0 bytes). Work (~34 GiB logical as reported by du), Source (~996 MiB), Edit (~65 MiB) and Packaging (~12 MiB) remain. A per-file ownership/consumer inventory and safe recoverable removal were not completed; the local material is retained rather than treating unknown dependencies as safe to remove. Three A/B thumbnails must remain available for the later test. Free space at check: approximately 16 GiB. No space reclamation claimed.
