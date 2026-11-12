# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/nuviko_history/videos/002_pompeii`
UTC: 2026-11-03T14:45:39.377116+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 1482 | 2.156 |
| UNKNOWN | 9 | 0.002 |

Logical bytes: 2317567346.
Filesystem-reported allocated sum: 2322481152.
Project packages read: 41; skipped symlinks: 0.
Unresolved import entries: 2614.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
