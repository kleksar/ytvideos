# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/043_pompeii_choice`
UTC: 2026-11-03T17:54:42.743507+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| BLOCKED | 6 | 0.045 |
| PROTECTED | 102 | 0.030 |
| UNKNOWN | 497 | 0.029 |

Logical bytes: 110956006.
Filesystem-reported allocated sum: 112234496.
Project packages read: 6; skipped symlinks: 7.
Unresolved import entries: 1052.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|
| `Work/paper043-prod-v02/scratch/render_v01/scene_00004.mp4` | 0.0 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Work/paper043-prod-v02/scratch/render_v01/scene_00005.mp4` | 0.0 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Work/paper043-prod-v02/scratch/render_v01/scene_00001.mp4` | 14.3 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Work/paper043-prod-v02/scratch/render_v01/scene_00000.mp4` | 12.9 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Work/paper043-prod-v02/scratch/render_v01/scene_00002.mp4` | 10.5 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Work/paper043-prod-v02/scratch/render_v01/scene_00003.mp4` | 8.5 | BLOCKED | TEXT_REFERENCE_REVIEW |

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.

Read/coverage errors:
- Text dependency scan skipped large file: /Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-03-published-media-cleanup/all_radio_deletions.jsonl
- Text dependency scan skipped large file: /Users/diplomat/ytvideos/channels/paper_detour/research/2026-11-03-published-media-cleanup/all_published_media_deletions.jsonl
