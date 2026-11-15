EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Handoff — USS Indianapolis / Captain McVay

Target: `channels/nuviko_history`, actual ChannelSpec `active`, English Long 16:9 illustrated. No Nuviko Videos music recipe. Base main SHA checked at authoring: `5d3222c8888c775d2195c8b2949949f2d992e98d`. Branch intended: `work/story-drafts/nuviko-indianapolis-mcvay-20261115`.

Exact source text: `script.en.txt` (future TTS/SRT master, only after approvals); full semantic Russian `script.ru.txt`. Claims/evidence/search counterdata in `research.md`. Scores and checks in `story-review.md`; per-scene exact paragraph spans and conceptual AI prompts in `storyboard.md`; honest packaging in `packaging-brief.md`.

**Capability missing:** Local git checkout and the project `uv run ytv start` runtime/store aren't mounted in this GitHub-connector host, so no real run, pinned read_next, plan_summary, task_guide, leases, source_script receipt, or official script gate exists here. No available independent session spawn tool from host registry was found, so original `ytv-script-review-v1` was not produced. This is a Draft editorial queue item and **must not be marked production-ready**.

**Exact local transfer:** On the proper ytvideos machine, sync the reviewed branch without merging it into main; inspect `AGENTS.md`, ChannelSpec and skill pins; execute `uv run ytv start --channel nuviko_history --format long --intent 'Review and register the editorial USS Indianapolis / McVay draft from .agent/research/2026-11-15-nuviko-indianapolis-mcvay'` prior to running the official new episode research/script. Read actual `plan_summary`, `read_next` task files, `task_guide` and pinned `reference_documents`. Revalidate sources, audience evidence, EN/RU; feed exact candidate narration to the official script task via its actual claim/inputs and receipt, not guessed fields. Run canonical `python -m ytvideos.script_review --script script.en.txt --output reader-input.json` (Long, no seam), deliver to a genuine independent fresh `sessions.independent` reviewer and preserve unmodified `ytv-script-review-v1` with exact SHA-256. Show full EN and RU for actual owner approval. Do not produce media or upload under this task.

Known open issues: viewer baselines n=2 only for one comparable source; own channel search terms, CTR, retention UNVERIFIED. 1945 visual archival reference images, rights and actual PNG assets not supplied. Current storyboard timing estimates are not voice alignment. Historic totals 315–317 / 1195–1196 vary slightly. User refusals #13 telegraph and #88 canal bridge remain untouched. No production permissions, merges or channel status changes.


## 2026-11-15 revision supersedes earlier handoff metadata

Parent SHA: `d79ec5a189a3c423d3c54efbc77488e3110ce3c8`. The revised EN/RU text has 26 semantic paragraphs and corresponding storyboard spans. The earlier wording suggesting a cleared/removed court-martial verdict is **invalid**; Congress's text was added to the personnel record in 2001 and the underlying conviction remained. Read `research.md` new revision section, `story-review.md` new ratings and `storyboard.md` instead of relying on the old scene count. Prior text hashes, lengths, approvals, author confidence, estimated timings and independent-review outcomes are STALE or UNVERIFIED. Obtain exact post-push HEAD and source hashes before official runtime registration. No official `ytv start` was invoked.
