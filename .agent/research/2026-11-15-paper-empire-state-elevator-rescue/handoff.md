EDITORIAL_CANDIDATE_UNREGISTERED — Git-only; no verified runtime, pinned context, independent reviewer or script approval.

# Handoff / source of truth

- Repository: `kleksar/ytvideos`, source base `main` `b1be73fbcd2a87dafe34ad65c479d337a26ebd80` (recheck immediately before any merge).
- Owner-requested proposed policy: [Draft PR #124](https://github.com/kleksar/ytvideos/pull/124), exact source revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72`; **not merged** at creation. Only its 2/5/10 editorial requirement incorporated, not branch files or runtime changes.
- Channel: `paper_detour` active, illustrated EN, short+long in `channels/paper_detour/channel.json`. 02m editorial Short; 05m/10m editorial Long; no unsupported production formats.
- Files: common `research.md`, `story-review.md`, `packaging-brief.md`, full `variants/{02m,05m,10m}/script.{en,ru}.txt`. Exact file SHA-256 in story-review. Recommended **05m** subject to independent review/owner selection. **No storyboards or timed scene spans**; original text never repinned.
- Runtime/blocker: available environment in this attempt had GitHub connector, but not the actual local `uv` repository/run database/executor needed for `uv run ytv start` and subsequent `plan_summary`, `read_next`, `task_guide`, and pinned `reference_documents`. Accordingly NO official run IDs, leases, receipts, approvals, independent model `ytv-script-review-v1`, or validated script gate exist. Git commit + CI don't change this.
- Independent reviewer/blocker: no separate independent reviewer session returning the required schema; self-reading and editorial scores below are **author-only**, not a pass. For Short pass two cycles as canonical text input; first-lister/causal fact-checker must see exact texts without author beat map or scores.
- Demand: indexed YouTube pages, not video playback or creator metrics; current audience demand UNVERIFIED. Sources/limitations documented in `research.md`.
- No provider calls, imagegen, TTS, MP4, upload or publication. All media assets and AV seam UNVERIFIED.

## Authorized path to production after owner chooses an exact variant

1. Locate current main policy, PR state, selected language file, Git commit SHA and SHA-256. Do **not** assume proposed PR #124 was merged or replace historical pins.
2. On a local authorised runtime, `uv run ytv start --channel paper_detour --format long --intent 'owner-selected Empire State Building/B-25 05m production script'` **only when a genuine new run is appropriate**. Use documented source-script import pathway when owner's instruction accepts exact completed text; don't repeat editorial review of an explicitly accepted source and don't manufacture acceptance from this Git PR.
3. Read actual `plan_summary`, `read_next`, `task_guide`, and pinned `reference_documents` before any work. Use `uv run ytv instructions` for narrow preflight when appropriate.
4. If still an editorial candidate, obtain independent `ytv-script-review-v1` on exact selected texts; block on material gaps and record actual review. Only owner selection/approval can promote one exact EN master. Supporting 02m and 10m don't spawn other runs.
5. With approved exact narration, build storyboard/prompts **only for selected script/hash**, then audio/imagegen/render under applicable gates. Existing production pins can change only by explicit migration; never force an older approved run to adopt this proposal.

Scope: **new editorial Draft PR only**, common docs/skills, releases and channels unchanged.
