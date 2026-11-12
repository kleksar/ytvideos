# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/new_channel/videos/002_margorie_mccall`
UTC: 2026-11-03T00:32:25.669840+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 174 | 0.103 |
| UNKNOWN | 28 | 0.082 |

Logical bytes: 197761868.
Filesystem-reported allocated sum: 198205440.
Project packages read: 34; skipped symlinks: 9.
Unresolved import entries: 903.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
