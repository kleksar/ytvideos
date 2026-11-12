# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/003_iq_gallery`
UTC: 2026-11-03T02:00:46.710804+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 699 | 0.581 |
| UNKNOWN | 1608 | 1.712 |

Logical bytes: 2461611921.
Filesystem-reported allocated sum: 2466418688.
Project packages read: 5; skipped symlinks: 9.
Unresolved import entries: 873.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.

Read/coverage errors:
- Live Palmier discovery: [Errno 54] Connection reset by peer
