EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Chilean 33 miners / Nuviko History, 2026-11-17

## Source, scope, concurrency

- Source remote `main` **`247ebe9245091972c5a93ecb84ce55ad8c15a211`** at entry; channel `nuviko_history`. No main documents or runtime pins altered.
- The story-policy PR [#124](https://github.com/kleksar/ytvideos/pull/124) **merged 2026-11-16** (commit `3bd47ae64c6eee627e2822f5986e64d386c855ce`); use **current main** canonical editorial, not a proposed branch revision.
- Story draft branch `story/nuviko-chile-miners-20261117`, based on exactly that main commit (unless a commit race is detected and remediated before branch creation). **New Draft PR into main only; no merge**. Owner's accepted work Apollo 13 #46 and Lawnchair Larry #25 excluded; existing #107 Andes note and #113 cave rescue kept intact.
- No changes to other story PRs, issue queue, channel configuration or scheduled episodes.
- Do not create or claim registered runs, leases, receipts, approved master, verified media reference bytes, TTS, images, rendered videos or uploads.

## Exact existing editorial package

All six full scripts in `variants/{02m,05m,10m}/script.{en,ru}.txt` (see [story-review](story-review.md) for exact SHA-256 **and Git blob SHA**). English is production narration; Russian is complete semantic editorial counterpart. Long 16:9 for all three. Single shared [research](research.md), review, [packaging brief](packaging-brief.md), this handoff, [README](README.md). Two minutes strong, five minutes recommended, ten complete but REWORK for excess technical exposition.

## Runtime and reviewer capability (observed blocker)

GitHub connector is available and was used to read all canonical docs and write only editorial Git artifacts. The automation's execution context does **not** expose a checked-out `ytvideos` filesystem with its `uv` environment and its local coordinator database. Consequently **`uv run ytv start` could not be executed**, and there are no `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, valid `task_id` or run-scoped receipts to claim. A separately authenticated fresh independent narrative reviewer under `ytv-script-review-v1` was not available in this context; authorial read-through cannot replace it. These are concrete capability blockers **for an official runtime issuance**, not a reason to forge outputs.

## Local continuation (never already performed)

1. Local operator checks out the actual remote branch/commit, confirms six UTF-8 script hashes in [story-review](story-review.md), and reviews current main rules plus task-specific channel profiles.
2. Decide one candidate variant (05m recommended but not approved). In local `ytvideos` checkout, use actual documented `uv run ytv start --channel nuviko_history --format long --intent 'Chilean San José miners 2010: 33 alive, note, rescue shaft'` **before any new production/research** and follow the returned `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`; follow documented source-import/attach-artifact route appropriate to the task and status. Do not invent old pins or automatically import all three as production masters.
3. Supply exact scripts to a fresh independent reviewer **without** the author's scores, verdicts or beat map on first reading; sources only after first pass; retain genuine schema result and tie it to exact SHA-256. Material changes invalidate that review. If the reviewer rejects the topic, stop.
4. Attach selected exact text, variants and story-review through actual `attach-artifact` receipts and run's script gate; keep real run IDs/hashes/approval events, not invented ones. Owner approval is still required before media work.
5. Only **after** approved/reviewed master 05m (or owner-selected 02m/10m), prepare detailed storyboard/prompts linked explicitly to that variant and hash using *actual* Nuviko traveler reference PNG bytes under `channels/nuviko_history/brand/References`; do not pretend this Git editorial packet viewed/generated them. No other variant's old timings apply.
6. Measure real spoken timing and AV QA only after permitted TTS/MP4; until then timing, audience demand, release readiness, actual visual assets, sound and end-screen are UNVERIFIED.

## Evidence / limitations

12-screened → three competing cases → Chile selected on *changing problems*; United 232 strongest alternative. NatGeo premiered documentary Sept 25/26 2026: recent publisher attention, not independent YouTube CTR/retention evidence. Video titles/views from publicly indexed metadata only; no footage, transcripts or viewer comments watched. Same-author ordinary baseline and own channel analytics absent. No vidIQ credits spent. Rights: only original text; media/reference bytes have not been copied.

One editorial author self-check and a small factual wording correction ("search hole" instead of "first hole") made before hashes were finalized; **not** a separate independent review or full production PASS. Substantive edits require fresh review and hash updates. Exact Git commit/PR/CI state to be recorded only after real remote write/read-back; do not treat queued/in-progress as success.
