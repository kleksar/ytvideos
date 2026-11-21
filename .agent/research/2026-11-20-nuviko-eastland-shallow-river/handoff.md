EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Eastland, 2026-11-20

**Source remote main at selection:** `c4624e2ae4035f5ec744354633c6a3b1cf54aa22`, branch will be created strictly from contemporaneous main after race recheck. PR #124 was **merged**; canonical editorial and writer skill from main used, NOT pre-merge proposed revision. **Do not change old runtime pins** without explicit migration. Other docs/skills/channel status are untouched.

**Official start attempt:** `uv run ytv start --channel nuviko_history --format long --intent 'Новый сильный сюжетный редакционный пакет 2/5/10 минут EN/RU для Nuviko History'` from the session workspace failed: `Failed to spawn: ytv — No such file or directory (os error 2)`. Thus no official run ID, lease, task_guide/pinned snapshot, artifact IDs, script gate or approval. The Git-only queue is the explicit owner-allowed exception, not production.

**Independent reviewer capability:** not available as a distinct session that can read exact texts twice, self-produce `ytv-script-review-v1` and independently respond. **UNVERIFIED; no fabricated schema/receipt.** Exact texts live at `variants/02m/script.en.txt`, `variants/02m/script.ru.txt`, `variants/05m/script.en.txt`, `variants/05m/script.ru.txt`, `variants/10m/script.en.txt`, `variants/10m/script.ru.txt`. SHA-256 and word counts in `story-review.md`; candidate content read-back required after remote commit.

**Editorial recommendation:** 05m EN / Long, SHA-256 `6c3426efc8953bafab522a47b915965146019a3935ea5678197a8fd4d4995537`. Strong central contrast of upper-hull dry escape vs lower-deck traps and newly explained lifeboat failure. 02m marked REWORK because Short loop is not a semantic continuation; 10m REWORK after slow late third. No automatic production of alternatives.

**Promotion path (local machine with actual repo/runtime):**
1. Sync the real checked-out repository and run `uv run ytv start --channel nuviko_history --format long --intent 'Подготовить утверждённый Eastland master из редакционного Draft PR'` **only after owner chooses and authorizes exact variant**. A story research workflow for an unapproved proposal instead follows `AGENTS.md` and `docs/workflow.md`; do not infer approval from this PR.
2. Read the returned `plan_summary`, `read_next`, `task_guide`, and `pinned reference_documents`, honoring old run pins or documented migration rather than fresh rules substitution. Use existing editorial helper for reviewer input and demand an authentic separate independent reviewer result; independent reviewer must initially receive exact texts WITHOUT this authored verdict/review map; then the fact sources and strongest alternative.
3. Record the source PR + immutable commit + exact EN script SHA-256 and full paired RU; attach supporting `script_variant` and `story_review` artifacts by the documented task contract and capture returned IDs.
4. Only after review and explicit script approval prepare **05m-specific** storyboard/preproduction material tied to the same SHA. Actual source reference PNGs for Nuviko protagonist, historical imagery rights, voice duration, music/captions and semantic transition to actual selected next video require local inspection. Never use guessed source bytes or earlier storyboard spans.
5. No TTS, images, videos, MP4, upload, publish, channel configuration or schedule changes are authorized here. Merge is also not authorized.

**Outstanding checks:** independent first listener `UNVERIFIED`; real runtime `BLOCKED`; historical images/protagonist reference bytes `UNVERIFIED`; AV seam/duration `UNVERIFIED`; same-channel next-story intro/link `UNVERIFIED`; public audience CTR/retention `UNVERIFIED`; 02m narrative seam `FAIL` (author); actual PR CI status must be recorded against exact remote HEAD. No synthetic PASS.
