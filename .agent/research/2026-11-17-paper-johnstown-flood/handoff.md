EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Johnstown Flood 1889 (Paper Detour)

- **Origin:** `kleksar/ytvideos` remote main commit `247ebe9245091972c5a93ecb84ce55ad8c15a211`; new editorial-only branch `work/story-drafts/paper-johnstown-flood-20261117` (created from exact main, no borrowed PR content); 2026-11-17.
- **Policy:** PR #124 was confirmed **merged**, so docs/standards/editorial.md from remote main (not a proposed revision) governs the three versions. No shared docs/skills/ChannelSpec changes.
- **Story identity:** Johnstown Flood, South Fork Dam, Pennsylvania, 1889-05-31. Existing PR search checked Johnstown and competing duplicates; do not attach this script to a separate story without fresh checks.
- **Language/channel:** Paper Detour EN production, RU editor translation, illustrated Long 16:9. The 02m/05m/10m files are complete narrative scripts; there are no invented runtime IDs.
- **Exact recommended script:** `.agent/research/2026-11-17-paper-johnstown-flood/variants/05m/script.en.txt`, SHA256 `783570e5f1deca6a39f8e33fffb8e8b69446c42288483b93c702620322b50106`. RU corresponding SHA256 `ca3b3cb9d6ae8afabcf2e31312188401ee04a647fc9fb6564e19469cda68b5cf`. All six exact hashes in `story-review.md`. Long 10m is now REVISED_CANDIDATE (author-only), not accepted. 05m recommendation is author opinion only.

## Actual blockers and implications
1. **Local production runtime was not available in this connector-only environment:** no checked-out project/DB with a working `uv run ytv start`; cannot truthfully read this new run's `plan_summary`, `read_next`, `task_guide` or pinned `reference_documents`. Therefore no official research/script gate, run ID, lease, receipt, or user approval exists. The owner's Git-only editorial exception authorizes this candidate but **not** a production task.
2. **Independent first-listener/reviewer inaccessible:** no separate reviewer with authenticated exact-text response per `ytv-script-review-v1` could be executed. Author table is *not* an independent verdict. On local handoff, present opening separately; then full exact text **without** `story-review.md` author diagnosis or beat map, ask for recall, interest, precise loss-of-interest point, payoff. Give sources only after first reading. Preserve actual schema response verbatim and repeat for modified hashes.
3. No TTS/MP4, real audio end-screen, reference PNG/media permissions, or YouTube Studio measurements: timing, artwork, licence checks and narrative audience demand remain UNVERIFIED. These do not convert this into a 'ready to produce' release.
4. Current main/version pins for preexisting runs must never be overridden; use documented `docs/migration.md` route if reconciling a previously pinned run.

## Local import procedure after authorized continuation
From the authorized project checkout and production DB/store, verify **current** main and PR exact script hashes, and inspect actual channel spec first. Then:
```bash
uv run ytv start --channel paper_detour --format long --intent 'Review Johnstown 1889 exact 05m draft from editorial PR and propose script approval'
```
Read the returned `plan_summary`, `read_next`, `task_guide` and pinned `reference_documents` BEFORE any new research or script task; execute only issued `next_action`. Attach the exact six variants and review with the documented `attach-artifact --kind script_variant` and `--kind story_review` forms once actual run IDs/paths exist (see task contract). Never fabricate `--source` or receipt IDs. Run the independent reviewer on the exact chosen script; if it rejects theme/phrases, apply at most two meaningful author revisions and recompute hashes. Present the chosen exact script to owner at the usual script gate. **Do not start TTS, image generation, montage, upload, schedule or publish as a result of this Draft PR.**

For a later accepted master, make detailed storyboard/prompts only for that exact variant+hash, not all three. Preserve per-scene timing bindings to the actual audio and actual references; verify paper plane PNG SHA and source license, no imaginary bytes. The 10s end-screen follows Paper's profile when a legitimate Public long/playlist next target is known.

## Concurrency and traceability
Before writing this PR, remote main and concurrently created/closed Drafts must be rechecked; if new conflict appears, stop or rebase new work without force-push. After create, read back branch SHA and diff and check actual CI statuses at that SHA. `queued` / `in_progress` are not success. No other story PR closed, merged, rebased or rewritten.

## Revision 2026-11-28
Baseline `7ee1936257c661ed50efbb5534d1b68080811d79`; current canonical main `7c779c4b2fd379c85166ae1b164fa53d1ea08843`. Exact revised 10m EN `402d109814acbf2db992f9e95fcd7fa25af5939c41c643810cd6995b3d11096a` / RU `c0c7da0cd52a8aae4a702abdc3c9d7867958a709f84fe851aa0dcbb6d59b5708`. 02m/05m unchanged; recommended 05m hash unchanged. Git-only text revision; no runtime capability or external lease registry observed, no known owner acceptance/production in PR body, conversation or review threads at preflight. Old 10m timing/review evidence invalidated; new paragraph map is editorial only. Follow existing local import procedure; no migration of preexisting pins.
