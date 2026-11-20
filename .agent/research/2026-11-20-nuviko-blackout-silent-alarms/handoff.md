EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Nuviko History: August 2003 blackout

**Canonical source main:** `450f005793e94ad6ca889e0090befe7fcf4d75b1`, the main HEAD fetched and confirmed immediately before creating story branch `work/story-drafts/nuviko-2003-blackout-alarms-20261120`. Earlier in this same run, `main` was `17e14e451a06704c880f9b8fe606b3411ac06dee`, then advanced one commit in unrelated Easy English Routine research docs. The first attempt to write any branch was **aborted before write**. The later story branch was created from the new main, not old. No force push, user files deleted or rewritten.

**Policy:** #124 merged November 16, 2026; writer skill/editorial from current main are canonical. Earlier proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` now historical and **not falsely treated as main or an active runtime pin**. Current `AGENTS.md`, index, writer skill, editorial, narration, workflow, task-contract and Nuviko profile/AGENTS/channel.json/brand were read. Accepted comparison versions #20 S-5 revision `78b375bf0004fdeb45722e6106f2919f09e82fe1` and #25 Lawnchair Larry revision `28862598989045cd02990e654b086afae28fea59` were read without modifications.

**Observed capability blocker:** attempted `cd /mnt/data && uv run ytv start --channel nuviko_history --format long --intent 'new editorial story packet 2 5 10 min'`; exit 2 with `Failed to spawn: ytv / No such file or directory (os error 2)`. The repository project runtime and executable `ytv` were not installed in the host. No real `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, run ID, lease, receipt, reviewer result or approved script gate. No independent reviewer capability invoked: **UNVERIFIED**, not author PASS.

**Files:** `variants/02m/script.en.txt`, `script.ru.txt`; same for `05m`, `10m`: **six full texts**, all complete, SHA-256 recorded in `story-review.md`. Shared `research.md` covers verified factual statements and competitor/baseline URL/observation, `story-review.md` scores each variant on eight criteria, `packaging-brief.md` ties honest hook/title/cover/payoff. **05m Long** recommended, not approved. 10m is REWORK despite being complete; 02m is a Long proposal, not Short.

**Local continuation:** fetch remote, check exact branch SHA, actual text bytes/hashes, main rules/pins; in authorised working repo run:
```
uv run ytv start --channel nuviko_history --format long --intent '2003 blackout alarms and cascade' --source-script .agent/research/2026-11-20-nuviko-blackout-silent-alarms/variants/05m/script.en.txt
```
Then read actual plan_summary/read_next/task_guide and all pinned reference_documents, attach variants with `--kind script_variant` and story review with `--kind story_review` using current runtime task contract. Supply exact six texts **without author ratings/map** to a separate independent reviewer, then give sources for subsequent fact-check, preserve genuine schema response and redo review for any modified hash. Only present **one exact selected** master for owner script approval. If current policy differs from existing runtime pins, use explicit migration, never checkout substitution.

**Production blockers:** independent reviewer UNVERIFIED; official script gate and user approval not done; real VO time, AV seam, accepted external narrator PNG bytes/media usage rights, storyboard/scene prompts, voice and final QA UNVERIFIED. Scope strictly editorial; no external TTS/imagegen/video, MP4, YouTube upload, publication, schedule or merge. Do not infer success from CI alone.
