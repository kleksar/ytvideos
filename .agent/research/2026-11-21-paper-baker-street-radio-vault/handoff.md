EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Paper Detour Baker Street 1971, 2/5/10-minute story

## Immutable source and policy

- Repository: `kleksar/ytvideos`. Before drafting: actual remote `main` `09fa62d02a85f5fdcbfcc73c5acb2dcbe99aa035`, tree `115379cf521ee2fb7ea9fc10c21061e90e6d4a43`. Review PR head later on the actual open Draft PR, not guessed as a local commit.
- Branch: `work/story-drafts/paper-baker-street-20261121` (new branch only, created from *this* verified main; do not use older runtime pins). Story folder: `.agent/research/2026-11-21-paper-baker-street-radio-vault`.
- #124 has merged (2026-11-16); no proposed-policy overlay is applied and no unrelated changes imported. Channel `paper_detour` / English / `illustrated`; 2m proposed Short, 5m and 10m proposed Long, both supported in ChannelSpec. Latest preceding story Draft PR at research time #320 Two Ways Lab, so Paper is due.
- No protected accepted source, old run, existing PR or active work is modified. #20 S-5 and #25 Lawnchair Larry were read as natural narration examples, NOT reused as scripts.
- Recommendation: **05m Long**, `variants/05m/script.en.txt`, SHA-256 `c2e8aa2a470fc5f79b6c970047ed753cecc081965fdd95c7beb07c2304c3c48b`. English words 663, plausible ~4:15–5:00, audio timing **UNVERIFIED**.
- 02m EN SHA-256 `af8cd67f1a7e830aa65026f255e80cce21f4633d431c66e7889b931e042a3f0c`; RU SHA-256 `a553dfb203a4eca281cd3dd829adb92a5673898cae519f6781eea060f1980aae`.
- 05m EN SHA-256 above; RU SHA-256 `232ffdb31b6d6db77549d0f788cadd8c894772d33d92ba693664e4c34a682ec8`.
- 10m EN SHA-256 `beb0c7446127cfd4a2b1a8ab70c7aab6946a6cf46102af768ed15633fbb29b6a`; RU SHA-256 `754e33a84d91414e5189d376964394d7dd5877642d5503ee2cd835e838a6af7d`.

## Why this is Git-only, not official script gate

Local actual attempted command (run outside a repository checkout):
```bash
uv run ytv start --channel paper_detour --format long --intent 'Paper Detour Baker Street 1971 bank burglary: prepare full 2m 5m 10m EN RU editorial scripts'
```
Actual result: `error: Failed to spawn: ytv / Caused by: No such file or directory (os error 2)`. `uv` exists; `ytv` does not. No `run_id`, `plan_summary`, `read_next`, `task_guide`, `reference_documents` pins, lease, approval, independent reviewer receipt or TTS output exists. Deferred tool registry was searched for `spawn_agent` / `sessions.independent`; no callable session launcher was surfaced. This does not prove the user's own host lacks the capability. Keep review **UNVERIFIED**.

## Authorized continuation in the actual local runtime

1. Fetch actual PR commit/tree and materialize its six files. Check all six SHA-256s above against bytes including final LF; verify PR base is remote main and that no accepted source was overwritten. Resolve any conflict with existing pinned sessions through documented migration; **do not replace pins silently**.
2. Read current on-host skills and exact runtime snapshot. Decide the exact production format with owner: recommended `long` 05m. From the repository checkout, run `uv run ytv start --channel paper_detour --format long --intent 'Paper Detour 1971 Baker Street bank burglary, proposed 05m Long; 02m/10m editorial variants'` **before** any new production research/script tasks. Inspect and read `plan_summary`, `read_next`, `task_guide`, and pinned `reference_documents`. This Git package does not authorise treating past remote research as a completed runtime task. If exact full text is explicitly selected and accepted for production by owner, use documented `--source-script` and provenance/approval route rather than fake editorial receipts.
3. Attach the exact EN/RU variant files with `attach-artifact --kind script_variant` and `story-review.md` with `--kind story_review` where the actual task context permits, using real sources and recording returned artifact IDs/hash. One exact master only, not three parallel productions. Do not invent API flags; read `docs/operations/task-contract.md` or CLI help in the pinned workspace.
4. Spawn a genuinely independent first reader if actual `sessions.independent` exists. Give bare exact 05m EN (and 02m twice consecutively for Short if considered) **without** this review, rating table or beats. Then give research for fact check; store their genuine schema response unchanged, bound to exact SHA. A reviewer can reject the story. After any script change, new hash → new review.
5. If owner selects 05m, confirm exact script approval through actual runtime, then storyboard. After that obtain real Paper profile reference assets and a licensed rights path, measure Lawrence 1.10× TTS, sync EN/RU and any spans, verify paper-plane Easter egg with its actual approved PNG reference. 10s Long end screen requires a verified Public target + real intro clip; this is presently `BLOCKED_NO_TARGET`. External video clips require separate owner permission even after script approval. No steps above were executed here.
6. Later stages retain their separate approved MP4 gate, upload/publication authority, native clickable target checks and calendar read-back. None is implied by CI or this editor recommendation.

## Evidence and editorial issues carried forward

- Core event/wording: [research.md](research.md), including 1971 TIME report and 2008 Rowlands account, cited secondary synthesis and dated YouTube cards.
- Audience demand for 2026 comparable Paper Detour EN Shorts/Longs, CTR, retention **UNVERIFIED**. Do not interpret large creator views as expected outcome.
- 02m text loop is semantic author-only; actual second-cycle cold-read and AV seam **UNVERIFIED**. 05m recommended story content reviewed by author, not independent reviewer. 10m complete but REWORK.
- 05m contains cautious uncertainty that burglar occupancy at Sunday inspection is unknown. Do not “upgrade” it to “police stood above the thieves” in packaging.
- Primary-source attribution of granular umbrella/old-well details still relies on published cited secondary accounts; do not claim direct court transcript access. Film-specific royal-photo motives excluded.
- No generated footage, TTS, licensed photographs, music, user credential or media bytes in Git.

Only this new story folder is within scope. Shared docs, other PRs, profiles, scheduling and existing releases remain unchanged.

