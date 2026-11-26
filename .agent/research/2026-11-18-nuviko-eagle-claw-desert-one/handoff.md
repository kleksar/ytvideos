EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Eagle Claw / Nuviko History

**Source main at research:** `7c94f825056b98cb65d8de94dd3eec709cc78188`. **Canonical policy:** PR #124 already merged 2026-11-16; read from main, not its former proposed revision. **Branch commit:** recorded in the actual Git PR (do not substitute a made-up SHA). **Chosen candidate:** 05m EN `c1e129e3472ea39e6c643ab37b15223de1cce6baeceeb992e6bf66c329ab9717`; recommendation, not approval.

### Exact files
- `variants/02m/script.en.txt` + `script.ru.txt`, EN 259 words, author STRONG_CANDIDATE; intended Long, not Short.
- `variants/05m/script.en.txt` + `script.ru.txt`, EN 608 words, author STRONG_CANDIDATE, recommendation.
- `variants/10m/script.en.txt` + `script.ru.txt`, EN 1280 words, author REWORK.
- `research.md`: claim evidence and audience caveats; `story-review.md`: per-variant review, hashes, blockers; `packaging-brief.md`: grounded promise. `README.md`: overview.

### Explicit capability blocker
This tool host has GitHub API read/write and web research, **but no executable working checkout with functioning `uv run ytv start`, and no authorized independent script reviewer/session**. Therefore no actual `ytv start`, `plan_summary`, `read_next`, `task_guide`, pinned run reference documents, lease, review receipt or script gate was created. The main docs were read through GitHub at the documented SHA; they are not a runtime snapshot. This is the owner's explicitly permitted **Git-only editorial queue exception**, not a production bypass.

### Required local transfer after owner picks one exact text
1. Re-fetch PR and selected exact commit; check `sha256sum` of both EN and RU scripts and the current channel policy. Use the immutable selected EN file.
2. Locally run (in a real checkout with existing workspace/store) `uv run ytv start --channel nuviko_history --format long --intent 'Eagle Claw editorial candidate: research/review one exact story'`; inspect and preserve returned `run`, `plan_summary`, `read_next`, `task_guide` and pinned `reference_documents`. **Do not invent command outputs.**
3. Attach script variants and story review as artifacts using actual command/API returned by pinned task contract. Have a **separate independent reviewer** read the opening/full exact text **without these author ratings or beat map**, then give sources and strongest alternative; reviewer must itself save existing `ytv-script-review-v1` schema. Any changed hash needs re-review. Treat 10m editor rating as REWORK, not a passed independent gate.
4. After that only, request owner approval of **one** exact master. For production import of already *accepted* source, follow the distinct `source_script` trust route in `docs/workflow.md`; do not forge owner evidence. Keep existing runs pinned; migration only.
5. Build a detailed storyboard / independent prompts for **only the selected 05m exact hash** after content checks, with actual references; verify Nuviko 2D presenter PNGs, archived images/licenses, spans, sound planning, native 10-second end screen and real related published video. Never apply other variant's indices/timing. No preview of #191 while it remains an unpublished Draft.
6. No TTS, imagegen, Flow, MP4, external video, scheduling, upload or publication is authorized by this PR. Do not merge it merely because CI passes.

### Checks remaining
- Source fact/meaning comparison by author: done; source accessibility mixed (contemporary FRUS fully read; DoD 2025 excerpt only, site 403).
- YouTube demand (same-format baseline for Nuviko), comments and private Studio: UNVERIFIED.
- Independent reviewer, EN/RU first-listener, exact read-twice Short seam (N_A Long), TTS voice duration, reference rights, AV QA: UNVERIFIED.
- GitHub CI: check exact PR HEAD; queued/in_progress means pending, not success.
- Production master approval, next video actual intro, native end-screen target: not done.
- Main may have advanced while this candidate was prepared; before transfer use real commit SHA and reject concurrent duplicates.

**Zero provider credits and zero media work** in this editorial PR.
