# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/new_channel/videos/002_margorie_mccall`
UTC: 2026-11-03T00:41:11.653276+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| PROTECTED | 194 | 0.104 |
| UNKNOWN | 65 | 0.172 |

Logical bytes: 296376146.
Filesystem-reported allocated sum: 302768128.
Project packages read: 34; skipped symlinks: 9.
Unresolved import entries: 907.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
