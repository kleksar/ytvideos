# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/new_channel/videos/007_joshua_jessica`
UTC: 2026-11-03T00:17:12.920532+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 943 | 0.983 |
| UNKNOWN | 354 | 0.146 |

Logical bytes: 1212125219.
Filesystem-reported allocated sum: 1214869504.
Project packages read: 34; skipped symlinks: 9.
Unresolved import entries: 903.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
