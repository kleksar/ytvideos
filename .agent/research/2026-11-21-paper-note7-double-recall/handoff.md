EDITORIAL_CANDIDATE_UNREGISTERED

# Git-only editorial handoff — Paper Detour / Galaxy Note7 double recall

**Scope:** ONE new story, six complete texts (EN/RU at 2/5/10 minutes), shared research, authorial eight-criteria review and candidate packaging. **Not an official release or independent script gate.** No merge, production, TTS, media, MP4, upload, publication, schedule or new Issue.

## Canonical versions

- Remote `main` as first checked: `131ef24068d75967b1e43aa88e5f1370f6775054`, main Git tree `c92263f9171a6a4500dcfcdb3afa37b180bb1c79`. Branch was created against the then-current remote main; see verified PR metadata for head after write.
- PR #124 *already merged* on 2026-11-16, merge commit `3bd47ae64c6eee627e2822f5986e64d386c855ce`. Read rules from current main `docs/standards/editorial.md` and `.agents/skills/ytv-write-script/SKILL.md`. The older proposed head `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is historical provenance only and was not treated as a main revision or imported.
- Producer profile is `channels/paper_detour/channel.json` with `status=active`, `language=en`, `illustrated`, allowed Long; `channels/paper_detour/PROFILE.md`, `AGENTS.md`, `brand/PAPER_PLANE.md` apply.
- Recommendation: [05m English](variants/05m/script.en.txt) SHA-256 `b959955a448a564d8fc53ca097c3746e5df92de90f5fe050f6f42f77c0841042`, [RU](variants/05m/script.ru.txt) `c9d4f1676bf7c3f36a02a25d9201b36381a6149865babb2cb1e17a957805c6e1`. **Owner has not selected/approved** master; this recommendation is NOT approval.
- Other full pairs/hashes, word counts and individual weaknesses: [story-review](story-review.md). All source-claims and limited YouTube comparisons: [research](research.md). Honest packaging and 05m-only provisional scene outline: [packaging](packaging-brief.md) · [outline](scene-outline.05m.md).
- Current scripts are Long proposals, including the compact 02m version. Do not relabel 02m as Short without a new script/loop review.

## Subsequent editorial revision — existing PR #341

Baseline head `735697b2a882ed9b9615cdf0b1f65d59f1189cd7`; 10m EN/RU replaced in place (full texts, not summaries) after inspecting complete 02m/05m/10m texts and shared research. The old 10m ended in general explanation and a long materials/recycling coda. The revised 10m follows two physical defects into the announced checks and owner return actions, then pays off the green battery icon. New 10m EN SHA-256 `36fed409c03cbbd30ac7e7d2785f6545e42f82f7913b95a8e0627b6b155a275c`, RU SHA-256 `9a68a33bbb93b0fa65d9d58859e72b3cc084eea520b071f7c8fbadea2ff2bd15`; baseline 10m EN `6d7112de8704676cda1cab70855ed8bbf0751d0ba9966029c5466289562bb142`, RU `875bb201f18d775ec7c1e61233e0ba7cac3e6c7c2aee245a648f360c3f44aabb`. Exact paths [10m EN](variants/10m/script.en.txt) / [10m RU](variants/10m/script.ru.txt). No new source claim beyond the same [research](research.md) ledger. The 02m and selected 05m pairs and hash-bound 05m scene outline remain unchanged.

**Independent cold review, measured TTS, chosen-hash storyboard, runtime registration and owner approval UNVERIFIED.** 05m remains author recommendation, not authorization. Invalidate any checks tied to former 10m hash; new 10m is EDITORIAL_CANDIDATE_UNREGISTERED. Next unresolved action: independent blind comparison, allowing rejection of either/both; real coordinator must attach selected exact variant and obtain required approvals.

## Observed capability blockers

1. **Runtime unavailable here:** attempted real `uv run ytv start --channel paper_detour --format long --intent 'Paper Detour: Note7 recall and replacement battery failure — unregistered editorial candidate'` in active container; result `error: Failed to spawn: ytv; Caused by: No such file or directory (os error 2)`. There is no mounted ytvideos project or trusted runtime DB here. **No run ID, plan_summary, read_next, task_guide, pins, claim, lease, receipt, or script gate exists** for this proposal.
2. **Independent reader unavailable:** tool discovery exposed no authorized `sessions.independent`/reviewer capability. No `ytv-script-review-v1`, independent bilingual review, two-pass cold reading or comparison verdict. Do not convert self-review to PASS. A fresh reading of the **selected exact hash** remains required.
3. **Media inputs not accessible/checked:** approved Paper-plane image SHA is documented but actual PNG bytes are not here. Historical photo/video rights, release metadata, exact audio/speech duration, thumbnail preview, endscreen target and actual intro are not established. All applicable media QA and AV seams are UNVERIFIED. `BLOCKED_NO_TARGET` applies only if future Long end screen still has no eligible actual public target.
4. **YouTube demand and rights:** actual video/comment/transcript playback unavailable; public metadata has non-comparable creators and stale index possibility. CTR, retention, creator baseline, current 30–90d demand UNVERIFIED. No paid vidIQ calls: discovered `vidiq_youtube_search` and `vidiq_comment_insights` each cost 5 credits; Paper `max_paid_units=0`.

## Transfer to a trusted local coordinator (DO NOT run this here as a fake workflow)

1. Fetch **exact PR commit** and check that the recommended EN/RU hashes match the immutable files; read `research.md`, `story-review.md`, and all current pinned canonical documents. Preserve old runs and previously approved texts; do not substitute current main for stored runtime pins.
2. In the real project/runtime, before executing new research/script production, register a new intended **Long** run per current `ytv-start` entrypoint, e.g. `uv run ytv start --channel paper_detour --format long --intent 'Editorial review of unregistered Note7 draft PR <actual-number>'`. This is an instruction for the **future local worker**, not evidence the run exists.
3. Read actual `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, `inputs`, `artifact_root` and production requirements; inspect the actual runtime's independent-review capability. Attach both languages of each 2/5/10 script and common review via documented `attach-artifact --kind script_variant` and `--kind story_review` with exact observed source paths, save real returned IDs and hashes.
4. Give a **fresh independent reader** an exact script **without** this author's scores, beat map or recommended title; ask first for cold-open interpretation, then entire text/attention drop points, then alternate-source check and two full readings if applicable. Reader should preserve its genuine existing schema answer without coordinator rewrites. If reviewer objects to the entire concept, record REJECT. On script text change, new hash and renewed review required.
5. Propose **one** exact compatible Long master on actual `awaiting_script_approval` only when genuine required checks pass; get an actual owner decision. Recommendation in PR is not permission.
6. Only after authorization use the actual approved Paper references and source rights, generate media, record Lawrence English TTS at pinned 1.1x, align word captions/scenes, produce and review MP4; any further upload/publication needs explicit separate instruction. Existing production pins are not automatically migrated.

## Git concurrency/scope

Create one new branch off newly rechecked remote main using non-force expected SHA. Source content consists exclusively of a new directory `.agent/research/2026-11-21-paper-note7-double-recall/`. Do not change existing PR/Issues, common docs/skills, channel status or public assets. After write perform direct remote read-back on *actual new PR head*, diff scope verification and commit-check/workflow-run status; `queued` and `in_progress` are not success. Record true final commit and state in PR (not this pre-commit text).

**Production blockers** are not instruction to modify shared policies or conjure missing files. This remains an editorial candidate until genuine runtime review and owner approval.
