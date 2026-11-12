# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/003_iq_gallery`
UTC: 2026-11-03T02:33:18.475229+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 711 | 0.540 |
| UNKNOWN | 1531 | 1.613 |

Logical bytes: 2312008013.
Filesystem-reported allocated sum: 2316689408.
Project packages read: 36; skipped symlinks: 9.
Unresolved import entries: 1390.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.

Read/coverage errors:
- Text dependency scan skipped large file: /Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-03-published-media-cleanup/all_radio_deletions.jsonl
