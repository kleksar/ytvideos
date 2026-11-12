# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/050_great_stink_london`
UTC: 2026-11-05T19:10:51.846664+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 7116 | 1.334 |
| UNKNOWN | 640 | 3.742 |

Logical bytes: 5450965685.
Filesystem-reported allocated sum: 5484834816.
Project packages read: 6; skipped symlinks: 55.
Unresolved import entries: 1379.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
