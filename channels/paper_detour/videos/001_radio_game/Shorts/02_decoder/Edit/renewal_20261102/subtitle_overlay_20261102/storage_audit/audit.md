# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/001_radio_game`
UTC: 2026-11-02T15:43:23.133163+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 759 | 0.635 |
| UNKNOWN | 2153 | 0.993 |

Logical bytes: 1748251064.
Filesystem-reported allocated sum: 1755979776.
Project packages read: 33; skipped symlinks: 8.
Unresolved import entries: 903.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.

Read/coverage errors:
- Package metadata: [Errno 2] No such file or directory: '/Users/diplomat/ytvideos/31F93804/media.json'
