# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/028_taj_mahal`
UTC: 2026-11-02T23:34:41.330296+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 471 | 0.398 |
| UNKNOWN | 2580 | 0.408 |

Logical bytes: 865726542.
Filesystem-reported allocated sum: 873218048.
Project packages read: 35; skipped symlinks: 9.
Unresolved import entries: 903.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.

Read/coverage errors:
- Package metadata: [Errno 2] No such file or directory: '/Users/diplomat/ytvideos/25A8FF9A/media.json'
