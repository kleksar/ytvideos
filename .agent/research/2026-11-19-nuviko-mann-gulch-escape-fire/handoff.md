EDITORIAL_CANDIDATE_UNREGISTERED

# Local transfer / blockers

- **Repository:** `kleksar/ytvideos`; source remote `main` SHA `5f6579f00bd03e42b74d5868a860234d19602d7b`, read 2026-11-19 and checked again before write.
- **Policy:** #124 already **merged 2026-11-16**; apply canonical `main` `docs/standards/editorial.md` and `.agents/skills/ytv-write-script/SKILL.md`; older proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is historical and must **not** be mislabeled as main or injected.
- **Six scripts:** `variants/{02m,05m,10m}/script.{en,ru}.txt`; exact SHA-256 and word counts in `story-review.md`.
- **Recommended sole candidate master:** `variants/05m/script.en.txt`, SHA-256 `3c345f2c02fdbf37aabc4acbfc64438002671692af4338f2fa06e655770e2555`, **recommendation only**.
- **Current state:** author-checked Git-only editorial draft, no approved run. `research.md` is research evidence, `scene-plan-05m.md` preliminary for matching variant only. Other variants must not inherit its scene timings.
- **Actual blocker:** the attempted `uv run --offline ytv start --channel nuviko_history --format long --intent ...` returned `Failed to spawn: ytv (os error 2)`: no installed runner/checkout. Therefore `start.plan_summary`, `read_next`, `task_guide`, pinned reference_documents, `claim`, `receipt`, `script_gate` and any run ID **do not exist** here. No fake fallback or direct DB record.
- **Independent first listener:** not available as a separate session with unchanged JSON schema; no `ytv-script-review-v1` response. Every script `independent_review=UNVERIFIED`; author scores never substitute. New text hash requires independent review again.
- **Channel reference limitation:** Nuviko profile read; actual two accepted traveler PNGs/hashes not opened. No image creation, final media scene approval or shot timings claimed.
- **External data limits:** YouTube public metadata indexed and third-party counts only, no video watch/audio or readable viewer comments; public demand, CTR, retention UNVERIFIED.
- **Other remaining checks:** choose exact version with owner; natural voice duration and required narration speed; full independent script review and source verification; complete exact scene prompts after approved variant; licensed imagery and host refs; endscreen target/intro and UI; final MP4/QA only on separate authorized task. Do not start any media, upload or schedule in this editorial task.

## Transfer procedure on authenticated local environment

1. Read new `main` and compare current PR head against recorded source and any concurrent work. Do **not** overwrite branch or pins.
2. In a real project checkout with dependencies, execute `uv run ytv start --channel nuviko_history --format long --intent 'Mann Gulch 1949 — choose and produce an owner-approved exact narration'` **before a new production research session**. Inspect actual `plan_summary`, `read_next`, `task_guide` and pinned docs from this run; use documented accepted-source import flow if owner already expressly approves one exact narration.
3. Register six exact script variants and shared story-review using the CLI `attach-artifact` forms returned by current contract, preserving bytes and hashes. Do not pretend this Git-only authored research predates the missing official `start`.
4. Have an actually independent reviewer first read exact scripts without author scores/research/beat map; then provide source evidence separately; obtain genuine reviewer output in its native schema. Do not forge reviewer. Repeat only for hash revisions.
5. Propose the **05m** script for explicit owner selection; preserve one real script approval gate. Do not automatically create three runs or use a Draft PR as permission.
6. Rebuild a production shot list from approved exact master and actual pinned requirements; load the two Nuviko PNG references, verify bytes/hashes and continuity. Then proceed only when separately authorized.

