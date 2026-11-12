# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/new_channel/videos/003_iq_gallery`
UTC: 2026-11-03T01:39:35.122181+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 689 | 0.539 |
| UNKNOWN | 1526 | 1.462 |

Logical bytes: 2147994671.
Filesystem-reported allocated sum: 2152628224.
Project packages read: 6; skipped symlinks: 9.
Unresolved import entries: 865.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
