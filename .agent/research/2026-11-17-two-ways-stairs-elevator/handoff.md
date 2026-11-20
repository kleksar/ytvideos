EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff: Two Ways Lab Elevator vs Stairs

- **Source main**: `81ed6aeb36fa004a00c4561f67dac5f23848d8af`, verified remote before branch.
- **Working branch**: `work/story-drafts/two-ways-stairs-elevator-20261117`; content created from main via GitHub Git objects and expected-ref updates without force.
- **Canonical policy**: `docs/standards/editorial.md`, `.agents/skills/ytv-write-script/SKILL.md`, `docs/standards/narration.md` from this main. Former proposed #124 has **merged**, so no unmerged policy import.
- **Potential future conflict**: [#138](https://github.com/kleksar/ytvideos/pull/138) remains Draft unmerged at selection; it proposes removing A/B identity. Re-evaluate if merged before any production migration; do not silently rewrite this editorial package.
- **Variant texts/hash and author review**: [story-review.md](story-review.md), exact versions (02m/05m/10m EN/RU), one source research and independent checks still pending.
- **Runtime blocker**: no actual `uv run ytv start` invocation or persisted run: connector context only, no checkout/project store available; consequently no `plan_summary`, `read_next`, `task_guide`, `reference_documents`, no lease, reviewer receipt or approval. Do NOT treat this as official `script` task completion.
- **Independent reviewer blocker**: fresh separate reviewer execution/context absent. Author review only; `independent_review=UNVERIFIED` for exact hashes. Passing CI is irrelevant to this.
- **Production compatibility**: channel Short target 35–50s; proposed complete 2m variant may not fit. 5/10m Long format is missing operational recipe and canvas/fps; do not enable it here.
- **Provider/analytics**: vidIQ account balance observed zero; no credits spent and no purchase. Youtube titles/news listings observed, videos/transcripts/comments not watched/read; demand UNVERIFIED.
- **What to do locally after acceptance**: inspect current main/PR#138 and own run collisions; use actual `uv run ytv start --channel two_ways_lab --format short --intent 'review/import editorial elevator-vs-stairs variants'` only if an authorized active channel configuration allows it; read the returned pinned packet fully; attach six exact script artifacts and story-review with IDs using documented `attach-artifact --kind script_variant` and `--kind story_review`; independent new reviewer first reads exact text without author notes, then receives sources; verify 02m loop/duration; choose exactly one master with explicit owner script approval. If 02m exceeds Short production limits, record blocker and request an authorized format decision instead of mislabeling as compatible. Any new hash invalidates old review.
- **Only after script review/approval**: detailed storyboard and prompts for exact recommended variant/hash, with channel reference assets fetched/verified. Existing source files are narrative text only. No artificial media/reference bytes created.
- **Prohibited**: no docs/skills/channel status changes, no merge, no TTS/images/Flow/MP4/upload/scheduling.

