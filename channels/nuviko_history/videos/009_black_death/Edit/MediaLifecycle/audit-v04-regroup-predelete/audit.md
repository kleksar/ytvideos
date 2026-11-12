# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/nuviko_history/videos/009_black_death`
UTC: 2026-11-03T12:03:45.137603+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| BLOCKED | 1 | 0.878 |
| PROTECTED | 10399 | 10.810 |
| UNKNOWN | 2884 | 10.763 |

Logical bytes: 24105994379.
Filesystem-reported allocated sum: 24170610688.
Project packages read: 39; skipped symlinks: 3.
Unresolved import entries: 2614.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|
| `Deliverables/en/long/black_death_nuviko_en_v03.mp4` | 899.0 | BLOCKED | TEXT_REFERENCE_REVIEW |

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.

Read/coverage errors:
- Text dependency scan skipped large file: /Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-03-published-media-cleanup/all_radio_deletions.jsonl
- Text dependency scan skipped large file: /Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-03-published-media-cleanup/all_published_media_deletions.jsonl
