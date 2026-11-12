# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/Shared/Experiments/Grain/20261102_watchmaker`
UTC: 2026-11-02T05:22:19.611030+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 26 | 0.253 |
| UNKNOWN | 25 | 0.009 |

Logical bytes: 281089719.
Filesystem-reported allocated sum: 281194496.
Project packages read: 5; skipped symlinks: 11.
Unresolved import entries: 187.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
