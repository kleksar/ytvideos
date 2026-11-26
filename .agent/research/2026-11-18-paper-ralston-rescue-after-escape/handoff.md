EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Paper Detour / Aron Ralston after escape

- **Base remote main at drafting:** `7c94f825056b98cb65d8de94dd3eec709cc78188`.
- **Policy:** PR #124 merged before this work. Use canonical `AGENTS.md`, `.agent/documentation-index.md`, `.agents/skills/ytv-write-script/SKILL.md`, `docs/standards/editorial.md`, `narration.md`, `docs/workflow.md`, `docs/operations/task-contract.md`, `docs/development.md`, `channels/paper_detour/{channel.json,PROFILE.md,AGENTS.md}` and `brand/PAPER_PLANE.md` from remote main. No proposed unmerged policy imported.
- **Exact story folder:** `.agent/research/2026-11-18-paper-ralston-rescue-after-escape`. `research.md` is common to all three editorial variants. `variants/{02m,05m,10m}/script.{en,ru}.txt` are all distinct complete versions. EN is intended production master.
- **Chosen by author only:** 05m Long, SHA-256 of EN exact bytes `9c8d84286a90a59c607cb89e16e10a2f6e09f9f0dce19dd159dc06d04859e4d7`, RU `d5d90cd5d6ed3f7f6f57c8dc6197276f629a6f49bdcf1128942a702176cceba1`. This is **not an owner-selected/approved master**.
- **Other hashes** (exact UTF-8 with trailing LF): 02m EN `54075a04531f68146ead8176be4411b581720ac814800d681189e344c51db3bb`; 02m RU `3227de9c2d29dc94534cf75211064ddef6744c19b01d8d354b26de3f58c55cc3`; 10m EN `efce422a75c906117ee85d90255f56c970fb4af723d4e1a83f9477d8f852a154`; 10m RU `631ee565cdd685a694717affcdeba6c30d48d82fe540e5dec255136886f0b65e`.
- **Revision baseline:** all new text, original draft for this PR, no received owner edit. No old runtime pins copied/updated; existing acceptance #20 S-5, #25 Lawnchair Larry, active #46 Apollo 13 untouched. 2m / 5m are authorial STRONG_CANDIDATE, 10m REWORK; not measured. Zero additional author revision loops spent.
- **What stopped official registration:** Current host lacks a local checkout/workspace for `uv run ytv start` and required `plan_summary/read_next/task_guide/pinned reference_documents`; it also lacks observed `sessions.independent`/fresh reviewer tool. Separate Git editorial exception allowed by owner. `uv run ytv start`, lease, receipts, reviewer JSON, approval and `awaiting_script_approval` have **not** occurred. No fake IDs.
- **Another blocker:** real Paper reference PNG (paper plane/scene style) bytes not accessible in this worker, so no detailed committed production `preproduction.json` or image-review claim. Exact 05m spoken-word duration and scene spans require future measured audio and an actual selected text hash. End-screen target and true next-film intro media `BLOCKED_NO_TARGET` until Public Paper video selected and asset rights verified. This does not block editorial texts.

## Local continuation (only after actual owner selection)

1. In the real repository checkout at exact accepted PR commit, check source bytes/hash and active run status; do not start duplicate run. If truly new, `uv run ytv start --channel paper_detour --format long --intent 'Aron Ralston story selected by owner' --source-script .agent/research/2026-11-18-paper-ralston-rescue-after-escape/variants/05m/script.en.txt`. Read **actual** returned plan_summary/read_next/task_guide and pinned requirements; no guessed identifiers.
2. For an actual owner-approved identical source, follow `docs/workflow.md#принятый-источник-без-повторной-редакции` and `uv run python -m ytvideos.source_script` using real run/revision/SHA/source-message ID/origin from the environment. For a not-yet-approved script, obtain the true independent `ytv-script-review-v1` result for exact text first and then one owner approval. Do not invent either.
3. Register supporting `script_variant` and `story_review` using `ytv attach-artifact` with real paths/ids from the runtime response. Supply selected master and precise hashes to coordinator. Do not automatically produce three videos.
4. After the 05m text passes actual independent read, build **only that variant's** detailed preproduction plan/scene prompts, real reference sheets and test `uv run python -m ytvideos.preproduction --file EXACT_PATH --script EXACT_MASTER --channel paper_detour --format long`. Any post-edit changes to master invalidate planned Unicode spans, review hash and estimated timing. Never fabricate images, scene refs or screenshots.
5. Any TTS/music/media/Flow/render/upload/publication require their own recorded permissions and provider capability. **No such operation in this PR.**

## Boundary

All 11 new Git files should be the only diff in this PR. No other branch changed, no merge, no shared editorial standards changed, no existing PR closed, no schedules altered. Recheck exact final branch SHA, public PR draft state and available CI statuses after push. `queued` or `in_progress` CI is not a pass.
