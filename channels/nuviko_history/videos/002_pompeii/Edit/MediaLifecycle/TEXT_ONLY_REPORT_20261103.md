# Pompeii — TEXT_ONLY lifecycle record

Updated: 2026-11-03 (Europe/Belgrade)

## Release proof and retained YouTube state

- Channel: Nuviko History (`UCbyLx6Rf3iWww4bPZJ2oo2A`)
- Video: [3mhzbbbWA0g](https://youtu.be/3mhzbbbWA0g)
- Accepted render SHA-256: `5212f7f04dcb607a642dd24e9e3895290c05ab1a30fc6b702efd209bf9c672ff`
- Processing: `succeeded`; prior fresh YouTube API read-back confirmed Public.
- Captions: manual English SRT was `serving` on the prior fresh API read-back.
- Playlist: public History Documentaries (`PLCtiNAU_98r0`), containing this release and two already-public long films.
- YouTube Studio screenshot check on 2026-11-03 shows the thumbnail experiment UI as “Тестирование…” and the History Documentaries playlist on the video details page. Experiment state: active/checking; variants B, A, C; B description fixed; result pending. Local variant art is deleted after its upload to YouTube.
- The release used the explicit one-release exception at `USER_DIRECTED_RELEASE_EXCEPTION_v04.md`: the strict renderer receipt gate did not pass for the 18 px subtitle override against the 29 px channel profile. No false receipt was created; this does not amend the standard.

## Cleanup plan

- Exact plan: `Packaging/AB_20261103_v03/Release/TEXT_ONLY_PLAN_20261103.json`
- Exact candidates: 7,770 regular files; 7,211,107,815 logical bytes; 7,227,187,200 summed allocated bytes.
- Inventory SHA-256: `e05b457068028b5aaad102bef01b2cfb6b3e7dacbb9d6deed0885e7b4930738b`
- Scope: episode-owned image/cover, audio, video/render, cache/frame and `.DS_Store` files listed in the exact plan. Shared brand assets outside this episode are excluded. Textual scripts, story/research/provenance, metadata, SRT/CSV/JSON/Markdown, configs, plans and receipts are retained.
- Every planned file was rechecked by exact path, regular-file identity, device/inode, size, timestamps, hard-link count and SHA-256 immediately before unlink. No directory-wide recursive delete was used.

## Final result

- `TEXT_ONLY` verified on 2026-11-03.
- Deleted: 7,770/7,770 planned files; 7,211,107,815 logical bytes; summed file allocation before deletion 7,227,187,200 bytes.
- Mismatches, already absent files, or unlink errors: 0.
- Post-delete check: all planned paths absent; 0 remaining episode files with image, audio, video, render/cache, or cover extensions; 0 remaining media bytes by that inventory.
- Pruned 198 empty episode-owned directories. Retained text/config/scripts: 372 files, 37,381,417 logical bytes; summed allocated blocks now 38,289,408 bytes. `du -sk` reports approximately 37,392 KiB for the retained episode tree.
- One existing `.agents/skills` tooling symlink remains; it is outside the media plan and was not followed or removed.
- Physical APFS space reclaimed is unknown because snapshots/clones may share blocks. The files are unlinked from the episode tree; byte-for-byte recovery of generated media is not guaranteed.
- Current local project/timeline pins and active-work entries are empty in `Edit/MediaLifecycle/policy.json`. The remote YouTube experiment continues independently; its variants have been uploaded to Studio, while their local image files are retired. No A/B result is available yet.
- Exact execution receipt: `Edit/MediaLifecycle/DELETE_EXECUTION_RESULT_20261103.json`.
