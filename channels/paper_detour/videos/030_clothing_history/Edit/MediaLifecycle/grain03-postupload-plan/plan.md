# Media lifecycle plan

Episode: `/Users/diplomat/ytvideos/channels/paper_detour/videos/030_clothing_history`
UTC: 2026-11-02T04:55:44.029325+00:00

**Read-only. Nothing deleted. This is not an executable deletion plan.**

Review candidates: 0.000 GiB logical.
Blocked declarations: 1.031 GiB logical.
Stale dependency inputs: 0.

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
