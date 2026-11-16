EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Local handoff — Paper Detour Poyais
Main at initial source reading: `5d3222c8888c775d2195c8b2949949f2d992e98d`, tree `e92a9c5b9ee656aa1448f34264b217ca1d0cbe98`. Channel: paper_detour active, English illustrated Long 16:9. Scope: text-only research/scripts/review/preliminary scenes/packaging. No merge, media creation, TTS, imagegen, render, upload, publication or status change.

Actual official CLI attempted before topic selection/web research in current host:
`cd /mnt/data && uv run ytv start --channel paper_detour --format long --intent 'Самостоятельный отбор сильного сюжета для Paper Detour; только редакционная очередь, без производства'`
Observed error: `Failed to spawn: ytv; No such file or directory (os error 2)`.
No official repo checkout, run ID, plan_summary, read_next, pinned task_guide/reference_documents, leases or receipts. Independent sessions.independent reviewer capability absent in current host; cannot produce original `ytv-script-review-v1`. User audience and YouTube Studio unavailable. Reference PNG bytes (Paper P02/P04 and approved paper plane image) unavailable/NOT inspected; no image creation was ordered.

**Exact local transfer:** in authorised checkout fetch current main and this PR, `uv sync --locked --extra dev --extra media --extra postgres --extra youtube`, run `uv run ytv start --channel paper_detour --format long --intent 'Review existing unregistered Poyais editorial story'`. Open actual returned `plan_summary`, `read_next`, task_guide, pinned skill, reference_documents, profile, production_requirements and real next actions. Import `research.md`, `script.en.txt`, `script.ru.txt` as unapproved editorial references, NOT as approved exact production script via `--source-script`. Capture actual refs and receipts only through local runtime, get genuine independent reviewer to first read intro then complete EN and full twice without author scoring, original result `ytv-script-review-v1` tied to exact EN SHA-256; correct defects and redo reviewer on any changed hash. Obtain actual user acceptance of resulting script before images/audio and later exact MP4; separate external video approval when applicable. Approved paper plane/photo references must be opened and hashes checked before any production. No script gate was passed by this PR.

Files: README.md, research.md, script.en.txt (Git blob `a1f81096b7d05c15283607f303baeb9f2c954745`), script.ru.txt (`e8b0594a621f58d806a5310052c618f9f70bc5af`), story-review.md, storyboard.json (39 exact bilingual spans, no measured time), packaging-brief.md, handoff.md. This handoff doesn't claim to be official task packet or approval.


---
## Варианты для будущего легального переноса (2026-11-16)
| Цель | EN (полный текст) | RU (полный текст) | EN words | Примерная речь при 125–150 слов/мин (без музыкального хвоста) | Редакционный результат |
|---|---|---|---:|---|---|
| 2m Long | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 243 | 97–117 сек. + паузы | Самостоятельная краткая версия, акцент на человеческих потерях |
| **5m Long** | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | **671** | 268–322 сек. + паузы | **Рекомендована к first-listener review** |
| 10m Long | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1360 | 548–658 сек. + паузы | Более глубокая финансово-колониальная версия, риск перегруза |

All variants are Git-only `EDITORIAL_CANDIDATE_UNREGISTERED`; exact SHA-256 and Git blobs in `story-review.md`. Baseline master and `storyboard.json` still refer to original `1e4fe7d9435c8693d53d88e49e6570ed15a77797`. A selected script is ONE new master and needs owner decision, fresh independent first-listener reading tied to exact hash, new storyboard only for that master, actual runtime context with pins, and real script approval before any production. Never treat PR update as `ytv start` or existing runtime migration. Reference `#124` was proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` at this review, not main. No TTS, image generation, AV, upload or publication done.
