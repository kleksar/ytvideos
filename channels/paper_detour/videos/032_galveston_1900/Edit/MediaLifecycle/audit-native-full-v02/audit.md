# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900`
UTC: 2026-11-02T08:43:22.402857+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 4872 | 7.784 |
| UNKNOWN | 217 | 0.522 |

Logical bytes: 8918299216.
Filesystem-reported allocated sum: 8930267136.
Project packages read: 32; skipped symlinks: 8.
Unresolved import entries: 224.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
