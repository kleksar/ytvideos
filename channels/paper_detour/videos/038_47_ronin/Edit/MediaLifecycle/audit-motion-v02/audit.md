# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/038_47_ronin`
UTC: 2026-11-03T12:04:54.118517+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 634 | 0.464 |
| UNKNOWN | 620 | 0.547 |

Logical bytes: 1085271805.
Filesystem-reported allocated sum: 1087991808.
Project packages read: 39; skipped symlinks: 3.
Unresolved import entries: 2614.

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
