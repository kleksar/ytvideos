# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900`
UTC: 2026-11-02T05:31:07.421896+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 2521 | 1.706 |
| UNKNOWN | 1 | 0.000 |

Logical bytes: 1832531534.
Filesystem-reported allocated sum: 1839017984.
Project packages read: 31; skipped symlinks: 11.
Unresolved import entries: 224.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
