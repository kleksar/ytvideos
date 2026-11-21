EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Nuviko 442nd / Lost Battalion

**Nature:** only a Git editorial queue candidate, not a canonical registered `ytv start` run, not a lease, accepted script, receipt, reviewer PASS or owner approval. Scope approved: one story, three complete standalone versions and EN/RU pairs. Do not trigger TTS, image generation, video, Resolve render, upload, publication, calendar changes or merge.

## Actual base and policy

- Repository: `kleksar/ytvideos`, default branch `main`; source main checked at authoring and pre-write: `131ef24068d75967b1e43aa88e5f1370f6775054`; base tree `c92263f9171a6a4500dcfcdb3afa37b180bb1c79`. If main changed before branch creation, branch must use newly checked main and this note updated; not force-push.
- PR #124 rule on three durations **already merged** into main (merge commit `3bd47ae64c6eee627e2822f5986e64d386c855ce`). No open proposed-policy override was applied, no unrelated PR changes imported.
- Canonical owner: `AGENTS.md`, `.agent/documentation-index.md`, `.agents/skills/ytv-write-script/SKILL.md` #Сюжетные PR и переработка, full `docs/standards/editorial.md`, `docs/standards/narration.md`, `docs/workflow.md`, `docs/development.md`, `docs/operations/task-contract.md`, `channels/nuviko_history/{AGENTS.md,README.md,channel.json,PROFILE.md,brand/VISUAL_PROFILE.md}`.
- Actual closest story PR sequence at authoring: #326 Nuviko → #329 Two Ways → #330 Paper. Consequently next **Nuviko**. Duplicate search for 442nd, Lost Battalion, Nisei and Vosges found no corresponding story PR. Existing protected #20/#25/#46, rejected #13/#88 unchanged.

## Actual unavailable capabilities and evidence

**Runtime attempt in this working container** (`/mnt/data`, `uv` exists; no local repo checkout):
```bash
uv run ytv start --channel nuviko_history --format long --intent 'Редакционная версия 2/5/10 одной истории; только официальная регистрация, без медиа'
```
Result: exit code **2**; `error: Failed to spawn: ytv; Caused by: No such file or directory (os error 2)`. No run was registered; no task packet, plan_summary, read_next, task_guide, pinned reference_documents, claim or receipt exists in this environment. Direct tools and deferred registry were surveyed; **no independent new agent-session spawn tool observed**, so `sessions.independent` cannot be reported available. An independent `ytv-script-review-v1` result does not exist. No fake IDs.

## Contents and recommendation

- Common fact research, 12-story selection, strongest alternative and public YouTube demand caveats: [research.md](research.md).
- All six exact production EN and full semantic RU scripts: `variants/{02m,05m,10m}/script.{en,ru}.txt`; word counts/sha256, individual 8-criterion reviews and gate statuses in [story-review.md](story-review.md).
- Recommended **`05m` EN** master, SHA-256 `a964d1dba62fa58ca6158f3c279c7a2ffb29d37b98a294fad36736bbcf5a1e3f`. Selected as *editorial* comparison only. `02m` Short has author-confirmed weak verbal seam (REWORK); `10m` is an alternative with pacing risk, not silently rejected.
- Title/first visual/hook/payoff and honest click promise in [packaging-brief.md](packaging-brief.md).
- No detailed storyboard, scene prompts, reference bytes, media or timings generated. The future storyboard belongs to exact selected text/hash after independent review; no old spans are transferable.

## Authorized continuation in full local runtime

1. Fetch current remote main; preserve source branch/commit and do not overwrite accepted source or unrelated changes. In a **working checkout with `ytv` installed**, create real new `nuviko_history` long run via canonical `uv run ytv start` with an accurate intent and exact candidate pointer; do not treat PR recommendation as approval.
2. Read exact `plan_summary`, `read_next`, all materialized `task_file`, `skill_file`, `requirement_files`, `task_guide` and pinned `reference_documents`; respect run/version pins. A historical active run must be explicitly migrated if applicable.
3. Import/select the six existing alternatives through permitted supporting `attach-artifact --kind script_variant` and the reviewed comparison `--kind story_review` with real sources. Preserve returned IDs/hashes, never fabricate a script gate.
4. Prepare the canonical first-reader input for the precise 05m EN file via `uv run python -m ytvideos.script_review`. Send the complete text to a genuinely independent fresh session **without** this author's scores, verdict, narrative map or suggested fixes. After first reading, provide source map. Reviewer independently emits its original schema-bound response. If the text changes, compute new hash and require a fresh review. Preserve any rejection rather than changing the review.
5. Check factual support, translation, first-listener attention, known unknowns, any applicable loop, and actual TTS length; ask the owner to approve exactly one chosen hash through current runtime gate before media. Owner approval is **not** implied by this Draft PR.
6. For confirmed 05m selected master only, draft channel-specific storyboard tied to exact EN hash with actual source/reference image bytes and rights. For Long end-screen, verify a real next-video target and actual intro input; otherwise retain blocker. No fabrication of the 2D traveler PNG references.
7. Verify PR exact remote head/diff/CI before any future merge; queued or in_progress checks are not success. Merge and all production require separate human authorization.

## Remaining explicit blockers

- `ytv` executable/working local checkout absent; official run and pinned task packet missing.
- Independent reader sessions not exposed in this host; no legitimate `ytv-script-review-v1` result.
- 02m script changed after initial author FAIL: conceptual text transition AUTHOR CHECKED, independent repeated cycle and AV seam UNVERIFIED.
- 05m/10m durations estimated only; correct voice speed 1.10 must be measured later, never altered to hit length.
- Owned Studio audience statistics, matched YouTube baselines and recent viewer demand UNVERIFIED.
- Original archival media/license, exact traveler PNG/reference bytes, actual next-video intro, and native end-screen implementation not available; do not pretend they were.

## 2026-11-21 — exact 02m r2 handoff (initial fail superseded)

Existing PR #331 baseline HEAD `5b8981ffc8c1fe5a7b394e1b003a944f1a8d561a`; old EN/RU 02m SHA-256 `416fa42bd426bbc49d1dd1ecd0f2f2b9c00b5ea8ea20bba5578e4f4678596d59` / `dc44cac53f12099f1a997f984c870b9ed2a34541638127e1e4832c3520217dd3`. New EN `89557319f52b40ff91601946e7d95ac16721c08a8fdf05a0a43a0149e089d89b` (276 words), RU `127a2e6b32a5a9b6e3cb3595b372fe203d3d02144e8cbbf3de17c514d198a6d2` (246 words). Current end 31 Oct new orders → start 26 Oct first recall is an author-checked *candidate*, NOT an independent or AV loop PASS. Select only one exact master in a genuine pinned runtime after fresh independent review and owner's approval; unchanged 05m EN `a964d1dba62fa58ca6158f3c279c7a2ffb29d37b98a294fad36736bbcf5a1e3f` remains a preliminary editorial recommendation. All media, script receipts, scene spans and actual timing for changed 02m require fresh evidence. No current host independent-session capability or executable project runtime was confirmed.
