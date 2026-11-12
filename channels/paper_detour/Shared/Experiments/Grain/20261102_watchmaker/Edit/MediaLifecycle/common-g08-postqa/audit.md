# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/Shared/Experiments/Grain/20261102_watchmaker`
UTC: 2026-11-02T06:10:16.834633+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 74 | 0.577 |
| UNKNOWN | 82 | 0.116 |

Logical bytes: 744940655.
Filesystem-reported allocated sum: 746020864.
Project packages read: 5; skipped symlinks: 8.
Unresolved import entries: 187.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
