# Media lifecycle audit

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history`
UTC: 2026-11-02T04:55:40.903707+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

| Classification | Files | Logical GiB |
|---|---:|---:|
| BLOCKED | 7 | 1.031 |
| PROTECTED | 1681 | 3.739 |
| UNKNOWN | 579 | 0.325 |

Logical bytes: 5470786167.
Filesystem-reported allocated sum: 5476126720.
Project packages read: 6; skipped symlinks: 3.
Unresolved import entries: 187.

| Declared path | MiB | Status | Blockers |
|---|---:|---|---|
| `Edit/v09/QA/v09_audio_s16le.pcm` | 34.8 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Edit/v09/QA/native_video.h264` | 237.9 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Edit/v09/QA/v08_audio_s16le.pcm` | 34.8 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Edit/v09/QA/final_video.h264` | 237.9 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Edit/v09/QA/accepted_audio_s16le.pcm` | 34.8 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Edit/v10/QA/native_video.h264` | 238.0 | BLOCKED | TEXT_REFERENCE_REVIEW |
| `Edit/v10/QA/final_video.h264` | 238.0 | BLOCKED | TEXT_REFERENCE_REVIEW |

Physical reclaim: **unknown**. Logical groups are not guaranteed disk savings.

- No deletion implementation or permission. No writer absence proof.
- All found imports protected, including retained timelines; unlisted/inaccessible projects and external consumers remain unknown.
- Text scan is heuristic and cannot prove absence of dependencies. Source hashes/QA are evidence, not user acceptance.
- APFS CoW and snapshots prevent inferring physical reclaim from logical or allocated sums.
