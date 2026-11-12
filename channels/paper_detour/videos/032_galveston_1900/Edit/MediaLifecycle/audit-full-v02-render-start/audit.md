# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/032_galveston_1900`
UTC: 2026-11-02T07:32:16.403946+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 4095 | 7.774 |
| UNKNOWN | 197 | 0.447 |

Logical bytes: 8827375761.
Filesystem-reported allocated sum: 8837627904.
Project packages read: 32; skipped symlinks: 8.
Unresolved import entries: 224.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
