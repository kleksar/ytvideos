# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/002_margorie_mccall`
UTC: 2026-11-03T02:33:18.564752+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 204 | 0.104 |
| UNKNOWN | 5407 | 0.395 |

Logical bytes: 535696714.
Filesystem-reported allocated sum: 548249600.
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
