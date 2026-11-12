# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/nuviko_history/videos/016_marseille_1720`
UTC: 2026-11-03T08:41:39.529825+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 5277 | 10.497 |
| UNKNOWN | 8 | 0.671 |

Logical bytes: 11991413433.
Filesystem-reported allocated sum: 12012113920.
Project packages read: 38; skipped symlinks: 3.
Unresolved import entries: 2619.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.

Read/coverage errors:
- Text dependency scan skipped large file: /Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-03-published-media-cleanup/all_radio_deletions.jsonl
- Text dependency scan skipped large file: /Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-03-published-media-cleanup/all_published_media_deletions.jsonl
