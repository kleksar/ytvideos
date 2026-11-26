EDITORIAL_CANDIDATE_UNREGISTERED

# Git-only handoff — Two Ways Lab / Three Gifts, Two Discounts

**Base confirmed remote main:** `7c94f825056b98cb65d8de94dd3eec709cc78188`. **Branch:** `work/story-drafts/two-ways-three-gifts-two-discounts-20261118`. **Main policy:** #124 merged; canonical `AGENTS.md`, `.agent/documentation-index.md`, `.agents/skills/ytv-write-script/SKILL.md`, `docs/standards/editorial.md` and `narration.md` read from current main. No proposed revision substituted. Active Two Ways Lab ChannelSpec explicitly supports illustrated Short only; alternate unmerged proposals did not change the active profile.

## One history; six full texts and source hashes

| Duration | Full English narration / SHA-256 | Full Russian narration / SHA-256 | Verdict |
|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) — `e8296509cc67c9131a709bb8bda81ed075819bcc2f0866a1afaea84bac4fbe52` | [RU](variants/02m/script.ru.txt) — `ee29f6be87a65eaf74427e9a897fce5e509951a8f11067393636808fb136d490` | STRONG_CANDIDATE, Short-length blocker |
| **05m** | [EN](variants/05m/script.en.txt) — `f8b22c48206cbda4dcc6b0d09dc7399a94fbb50d4934efd68ab801d67b024961` | [RU](variants/05m/script.ru.txt) — `1c33f52a8f20812fe226b7b3d104b5b9d3c81929ace5036ecdb6da7965f49bfc` | **STRONG_CANDIDATE, editor recommended, Long blocker** |
| 10m | [EN](variants/10m/script.en.txt) — `4155a782b2e0ca2e9648faf084e469b2cff96c3114bbc24d28179f2a204017b9` | [RU](variants/10m/script.ru.txt) — `f8064461260f900385767a6a09d2c2b7ab12c3d72c857062139c1b06a582fc17` | REWORK, Long blocker |

Full [research](research.md) holds actual selection of 12 competing tasks, three finalist submissions, source strength, YouTube metadata, calculations and boundaries. [Story-review](story-review.md) holds exact SHA-256/word counts, eight criteria per finished edition, major flaws and separately marked check states. [Packaging](packaging-brief.md) ties promise to precise first visible events, arithmetic change, reveal and full payoff. All files editorial only; no AV/scene assets created.

## Precise missing capabilities and blockers

1. **No live executable repository checkout or shared production workspace in current GitHub-connector editorial environment.** There is GitHub read/write capability, but not a runnable checkout with `uv run ytv start`. Thus no run ID, task claim, actual `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, `input_hash`, artifact receipt, lease, script gate or approval. **Git-only editorial queue is explicitly allowed by owner for this task; it is not official production.**
2. **No independent first-listener reviewer using the actual current reviewer schema.** Author scored, checked maths and compared EN/RU, but did not create an independent review response, fake a reader, or claim one. Exact text without author's verdict/beat map must be given to independent reviewer *before* sources; require their unchanged schema response. Any new text bytes require new review.
3. **No compatible production format.** Two Ways Lab active `short` targets 35–50s; full 282-word 02m is outside that target. There is no configured `long` recipe and `05m`/`10m` are editorial proposals only. Neither CI nor editorial score grants the missing format. Do **not** alter channel configuration or statuses in this story PR.
4. **No real TTS/video, media references, licensed images, exact PNG reference bytes, sound, thumbnails, external provider credits, live uploaded video or platform analytics.** Actual timing, model-to-physical validation, rights, AV seam and audience response all UNVERIFIED. No paid calls, purchases, publication or schedule edits.

## Local continuation when authorized

First resolve/approve a genuinely supported format **without modifying old pins implicitly**. Local worker then checks out the exact PR head and SHA, reads **then-current** `AGENTS.md`, writer, workflow, task contract, editorial and channel profile, and starts a real workflow as described by canonical `.agents/skills/ytv-start/SKILL.md`: `uv run ytv start --channel two_ways_lab --format SUPPORTED_FORMAT --intent 'owner-selected exact script and source commit'`. Read the actual `plan_summary`, `read_next`, `task_guide`, pinned reference docs and input sources from the response, and follow state/next action, not this handoff as a replacement for runtime. For explicitly accepted finished source, use the canonical `--source-script` / accepted-source import and owner decision mapping; don't fabricate a second approval or make an early source approval just because this PR is a Draft.

Read selected exact script to independent reviewer without this document, scores or beat map before any source/fact followup. Store the *reviewer's own response* according to existing schema and revisit only defects. Before a master is approved, three variants remain separate supporting artifacts, never stitched together for TTS. If owner selects shorter native 35–50s Short, create a new short text/hash and new independent double reading; do not silently trim 02m or graft a fake loop. If owner selects a genuine Long, activate a valid Long recipe only by separately approved maintenance/migration first.

Only after exact selected and supported script passes applicable review and real approval should a storyboard/preproduction/prompts be generated **for that exact variant/hash**, using real references and spans. A placeholder script/estimated word timing cannot stand in for recorded timings or actual media. Older story PRs, owner-approved texts, status and common docs must remain unchanged. No merge from this editorial task.
