# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/nuviko_history/videos/009_black_death`
UTC: 2026-11-03T06:35:47.688509+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 3174 | 2.414 |
| UNKNOWN | 2841 | 8.062 |

Logical bytes: 11248047098.
Filesystem-reported allocated sum: 11277971456.
Project packages read: 37; skipped symlinks: 3.
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
