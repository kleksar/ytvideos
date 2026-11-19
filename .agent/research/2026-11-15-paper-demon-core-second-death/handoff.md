EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Paper Detour Long — Demon Core, handoff

Repo main observed `5d3222c8888c775d2195c8b2949949f2d992e98d`; tree `e92a9c5b9ee656aa1448f34264b217ca1d0cbe98`. English narration Git blob `262f8c73a5cb21ea2cda536260e0e7cc4462d86c`, RU complete meaning translation `1c5ad76c84f1cbfb2d2ab80f1646fb7e393a65c4`; story-review refers exactly to these text bytes. Channel from live `channels/paper_detour/channel.json` active; English illustrated Long, physical full-frame paper 16:9. This PR only adds 8 text files under one episode folder.

## Actual blocker
GitHub connector works but runtime host has no authorized ytvideos checkout (`/mnt/data/ytvideos` absent) and `command -v ytv` produced nothing (although `uv` exists). Thus **no actual `uv run ytv start` was run**, no pinned plan_summary/read_next/task_guide/receipts/run ID, no original independent session reviewer. Cannot claim `awaiting_script_approval`. Do not forge IDs or accept author scoring as review.

## Local entry
1. Authorized coordinator checks existing actual runs with current CLI status/resume to avoid duplication; otherwise from correct checkout executes `uv run ytv start --channel paper_detour --format long --intent 'Review and consider editorial Demon Core two accidents; no media generation'`.
2. Read actual `plan_summary`, `doctor`, `read_next`, pinned task guide, skill, full reference documents and assets; import research + exact unapproved scripts as inputs, not as a completed official run.
3. Run original `ytv-script-review-v1` on genuine exact EN SHA-256, fresh independent session with blind opening, then complete text and repeated full read; separately assess full Russian meaning. No use of this author scoring in blind review input.
4. If review requests change, update both texts and all dependent scene spans/briefs, invalidate old hashes/timing/review. Present full exact EN/RU for real owner script approval. The owner must actually decide.
5. This automation **does not permit** merge, paid providers, imagegen, TTS, video clips, renders, audio, YouTube upload or publication, regardless of PR merge/CI.

## Verification
EN/RU story has 34 paragraph pairs and provisional S IDs; full independence/MP4/TTS/image and actual runtime unknown. CI status must be read back on exact final PR HEAD. Paper-plane reference pixels are not available here; no pretend brand asset creation.

## 2026-11-16 editorial backfill (main SHA 3bd47ae64c6eee627e2822f5986e64d386c855ce)

**Three full EN + RU editorial candidates** now in `variants/{02m,05m,10m}/script.{en,ru}.txt` (see [README](README.md), [story-review](story-review.md) exact SHA-256). Proposed **05m**; no owner approval. Original `script.en.txt`/`script.ru.txt` and 34-scene `storyboard.md` stay pinned to baseline, not silently reassigned. Do not assume those 34 spans cover any variant; storyboard follows the chosen script only.

New sources for 10m claims appended to the single `research.md`. Some rules tightened after Daghlian; 10m makes that fact explicit rather than claiming no response until Slotin. Real independent reader is still unavailable in Git-only connector; this author-only review is **UNVERIFIED** for independent gate. Runtime remained unregistered; no ytv CLI/claim/receipt or provider calls. The original older SHA reference remains historical evidence, not a live runtime pin. Next steps: establish authorized local coordinator, inspect canonical run context/pins first, present exact variants blind to reviewer, select one approved master and create a new tied storyboard only then. Never auto-produce all three.

## 2026-11-19 — second 05m editorial pass (not production)

The current preferred, **unapproved** Long is [05m EN](variants/05m/script.en.txt) SHA-256 `7f53e0278f02ab5d2a62d3e36c1b122f64df3c145235539bfc50c73f4fe8f3e7`, paired with [full 05m RU](variants/05m/script.ru.txt) `20501ef20f2a18169411216f4ff66ffe93eceadedba578896c622761ac956516` (715 English words, estimated timing only). 02m, 10m, the original master and 34-scene storyboard stay unchanged. This is a substantial rewrite of the first/later safety-response sequence and the Slotin demonstration; see [fact evidence](research.md#2026-11-19-05m-causal-repair--first-safety-response-vs-later-remote-control) and [story-review](story-review.md#2026-11-19-exact-05m-revision-and-hard-check-delta).

At local transfer, check actual current run and immutable pins, attach exact six scripts as editorial candidates, give blind reader exact 05m without author assessment, obtain genuine bilingual/factual review and owner selection before constructing **new 05m-specific scenes**. Root storyboard and original production references remain historical only. No TTS, media, upload, approval, runtime migration or pin edit in this PR.
