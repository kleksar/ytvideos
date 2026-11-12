# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/nuviko_history/videos/037_voyager_1_repair`
UTC: 2026-11-05T01:52:42.902946+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 654 | 0.350 |
| UNKNOWN | 9439 | 2.887 |

Logical bytes: 3476208684.
Filesystem-reported allocated sum: 3515826176.
Project packages read: 6; skipped symlinks: 55.
Unresolved import entries: 1379.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
