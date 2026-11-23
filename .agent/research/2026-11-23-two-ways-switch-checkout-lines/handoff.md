EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Two Ways Lab: switching staffed checkout queues

## Identity and branch source

Source remote main observed 2026-11-23: a6023668001421b689a8142cebc0bd436545be6b. New story branch must descend from exactly this SHA after a final race check. #124 merged 2026-11-16 11:21 UTC; historical proposed revision 7d6bdf7702a2a241a33a21677fce29f26ada9b72 is not separately pinned. Use current main canonical editorial/writer skill; no common docs/skills/ChannelSpec changes here. Last created story Draft #373 was Nuviko, so this round is Two Ways Lab.

Relevant current documents read: root AGENTS; documentation index; writer skill; full editorial and narration; workflow, development, task contract; Two Ways channel.json, AGENTS, README, BACKLOG, SCENE_PLANNING, VISUAL_PROFILE. Same queue topology not the subject: #136 is pooled vs split lines, #368 is self-service vs staffed. This story instead compares my decision to change from one existing staffed checkout line to another at t=60. Audience overlap is nevertheless a counter-signal.

## Six full texts / exact proposed master

| Edition | Full EN | Full RU | SHA-256 EN / RU |
|---|---|---|---|
| 02m, Short editorial recommendation | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 8fe085cd58076f8116792424f4b5c265147997d68c3c807c1d0c6b3afd460983 / 6dd8341adc99cbb44d424e60f2cd58bcfffd7ed84ad16d833a3b7fa0fc427ed0 |
| 05m, revised Long proposal only | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 2ba66aca993083494205acd59916cdb53390ab86cbaf0c2d19c03ebd725ec84b / b0f9f2807e9d231b5db90f8769fa81ece4236672635fd0b9332c5e9f08445ad7 |
| 10m, REWORK, Long proposal only | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | e1316d220049c7d6c8b11bd191f91ee684e3b0b2fd0c9e7b0473448e0a5eee74 / e03c4f8f766c599b1b4a525c9ac54806938004eccb9f926ab34f8378b6f03f2e |

Research, formulas, competitor caveats: [research.md](research.md). Eight-criterion authored review, SHA-256 and QA: [story-review.md](story-review.md). Title, thumbnail, early proof, payoff, next-video obstacle: [packaging-brief.md](packaging-brief.md).

## Actual blockers, no invented work

Current environment has uv but no installed ytv app; actual invocation
`uv run ytv start --channel two_ways_lab --format short --intent 'Prepare three complete editorial script variants for switching checkout lines'`
returned `Failed to spawn: ytv — No such file or directory (os error 2)`.
No repo/runtime project checkout is mounted. Therefore no genuine start, plan_summary, read_next, task_guide, pinned reference_documents, run, lease, receipt, approval or script gate was created. Independent reviewer session / ytv-script-review-v1 is unavailable. No self-review will impersonate an independent reviewer. The Git-only queue is explicitly allowed but remains UNREGISTERED.

Short production recipe exists at 1080×1920 and 30 fps; however 02m script (~2m estimated) exceeds channel's standard 35–50-second Short target. Do not speed the voice to force fit. For 05m/10m, ChannelSpec long fps/canvas are null; **NO supported Long recipe**. They are editorial-only with production blocker, not existing or fictitious Long runs. All voice timings, SRT, AV seam, hero/style reference bytes and visual rights are UNVERIFIED. No image/video/TTS provider, media, uploads or publication changes were made.

## Route to resume without fake authority

1. On the host with repo + ytv installed verify current PR exact commit, each script byte hash, existing run/approvals and pinned documents. Check for source imports/active runs first and do not override.
2. Once owner selects exact EN master and intended supported format, use actual ytv start or canonical accepted-source import only with genuine owner decision and message ref. Read plan_summary, read_next, task_guide and pinned reference_documents. One selected master, not three automatic productions.
3. For a normal script gate, send exact text (no author verdict or beat map) to a **separate independent reader** before supplying research. Preserve authentic response in existing ytv-script-review-v1 schema. For Short, require literal full-text double cycle and seam judgment. Changed hash means new review.
4. After exact text passes applicable checks, fetch real hero/style reference image files, validate actual SHA-256, prepare detailed scene cards, prompts and Unicode narration spans for that EN hash only. Do not transfer spans from another edition or assume file bytes.
5. Resolve mismatch of recommended 2m with 35–50s channel preference, verify media rights, measured TTS and MP4 AV seam before any release authorization. A GitHub CI green mark is not script approval.

This PR remains Draft. No merge, force-push, editing other PRs, changing common docs/skills/channel status, TTS, imagegen, MP4, upload or publication is authorized.

## Existing PR #376: substantive editorial revision (2026-11-23)

Baseline head `ba4c1f897d6274f63222380e1678020f055cea2b`. Old 05m SHA-256 EN `f047392e2b90cf1a4f6393a381983610d425e5c22858bc232e1ae04946dd4341`, RU `8c88ea54eebb95f39c44a090bd6d8427dd4b38925759fce47d995f5d9379b18c`. New 05m exact EN `2ba66aca993083494205acd59916cdb53390ab86cbaf0c2d19c03ebd725ec84b` (838 words), RU `b0f9f2807e9d231b5db90f8769fa81ece4236672635fd0b9332c5e9f08445ad7` (697 words). The previous conclusion largely explained uncertainty and sunk cost after the two conditional results. The revision replaces that explanatory tail with an explicit third trial: reset original no-price-check schedule, B5 joins at second 63 while the protagonist walks from t60 to t65, so B ends at t245 (4:05) versus unchanged A195 (3:15). If B5 enters at second 67 *after* protagonist arrives, B ends at t205 (3:25). The original A+25s price check occurs **only** in trial two, never in trial three. This new scene adds an independent causal risk of crossing and keeps full first-person EN/RU. Existing 02m/10m exact text unchanged. 02m packaging/scene assumptions are not applied to 05m.

Self-check of calculations/EN-RU mapping performed on text; no independent reviewer, measured speech length, storyboard, live evidence, actual ytv run or owner approval. This remains EDITORIAL_CANDIDATE_UNREGISTERED. Two Ways Long ChannelSpec has no canvas/fps. The intended 05m requires its own new independent reader on exact hash and production-format resolution. No protected masters, channel docs, provider assets or production states altered.
