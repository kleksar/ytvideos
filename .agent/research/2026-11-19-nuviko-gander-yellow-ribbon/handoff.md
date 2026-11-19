EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Nuviko History / Gander / Operation Yellow Ribbon

- **Base remote main observed before editorial work:** `d7dbf4d8de0a0719e062e72b7e21b7d3748de100` (2026-11-19). Recheck before publish. New branch from exact remote main; update branch only with expected SHA and no force.
- **Policy:** current `main` `docs/standards/editorial.md` SHA blob `cd8ed20c697af001df887853772971a81176b7e1`, writer skill SHA `fb45362fbc2ac5d0ae9d5178c2c98536637061df`. Previous proposed #124 is merged; original proposed policy rev `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is historical reference only, NOT imported.
- **Channel:** `nuviko_history`, English narration master, illustrated 16:9 Long is supported. No existing accepted run/pins rewritten. Source `channel.json` blob `f8dd73dfcfe38080a201cb871fbd01f8f2c06140`.
- **Contents:** README, research, six full UTF-8 scripts under `variants/{02m,05m,10m}/script.{en,ru}.txt`, story-review (SHA-256 exact scripts and eight criteria), packaging brief, handoff. 5m recommended, owner not yet approved it; 10m REWORK but fully written.
- **Unregistered capability:** attempted `uv run ytv start --channel nuviko_history --format long` before writing; failed `Failed to spawn: ytv Caused by: No such file or directory` in this Git-only environment. No `plan_summary`, `read_next`, `task_guide`, pinned task packet or registered run was available. No false run IDs/leases/receipts/approvals.
- **Reviewer unavailable:** no actual independent exact-text reader result under task contract, no separate bilingual review, no cold-read attention verdict. Author scoring is not independent review. Every new exact script SHA requires its own reviewer and any revision invalidates stale assessment.
- **Narration timing:** EN 266/607/1309 words, rate assumptions only (125–140wpm and pauses). No TTS, SRT, AV seam or MP4 observation. Long loop = N_A, not an omitted Short QA. Underlying producer voice/speed must be taken from pinned local runtime, not re-guessed.
- **No storyboard/prompts yet:** author independent text gate required first; no actual reference images/rights/read-back, no fake video timestamps. No new image files, voice, providers, sound, upload, schedule or edit of other PRs.
- **External materials:** research URLs and limitations in `research.md`; no copied video lines, no borrowed musical scenes or unauthorized media. Upcoming 10s endscreen needs verified genuinely related published episode, real playable next intro and native UI QA; no fake target.

## Local continuation (not executed)

1. On authorized checkout, `uv sync --locked --extra dev --extra media --extra postgres --extra youtube`; confirm the CLI before attempting a new run. Check no existing run by topic/version, then `uv run ytv start --channel nuviko_history --format long --intent "Produce approved Gander version from editorial candidate"`. Honor returned plan_summary/read_next/task_guide and **actual pinned** reference_documents; do not treat this Git draft as approval.
2. Supply research and exact chosen `script.en.txt`, `script.ru.txt`, and story-review as supporting source artifacts using the repo's actual CLI `attach-artifact --kind script_variant` and `--kind story_review`, not guessed IDs. If the user adopts 2m/10m instead of 5m, choose that exact SHA and redo dependent checks.
3. Independent reviewer reads exact text cold without ratings/beat map; afterward source-backed check, EN/RU equivalence and native format. Preserve actual schema result, no fabricated approval.
4. On explicit owner approval of one exact version, produce one storyboard, prompts and output media bound to that exact EN SHA. Get actual references, use pinned Nuviko visual profile. Finish mandated script gate and separate MP4 approval, then release only on explicit instruction.

**Next decision required:** one exact master text selection/approval after independent review; none inferred from Draft PR status. No merge requested.