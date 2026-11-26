# Current editorial package — 2026-11-26

EDITORIAL_CANDIDATE_UNREGISTERED — prepared, author desk-checked, 05m recommended. No owner approval, independent reviewer, registered run, measured duration or production. Baseline e2bf1e2f295f24fc9a9ad4244d2c33acbf2a3db1. Root/master and historical storyboard unchanged. Only revised 02m/10m are new text; 05m preserved.

| Duration | Complete scripts | EN/RU words | EN SHA-256 | RU SHA-256 | Status |
|---|---|---:|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) / [RU](variants/02m/script.ru.txt) | 256/206 | `5538ff7e00e1b6b7ae54caa5ae34207121f36d7b5ad3ed187f2f39918878ee8b` | `2684e3b884e119164858090c40c845ce4d8f32eda098a7f4b1e5f8d8cc545781` | revised |
| 05m | [EN](variants/05m/script.en.txt) / [RU](variants/05m/script.ru.txt) | 571/436 | `4677c37aa4611a4568a1a875cc18d437c1e6018dd3fa38128c9fd2206bd13e69` | `0b1518f4a6654516405d1aa6ed006c7a6ea2512d8e803a643035e26819b1d5fa` | preserved; recommended |
| 10m | [EN](variants/10m/script.en.txt) / [RU](variants/10m/script.ru.txt) | 1270/1020 | `53cc4ae965585cd9765252c53e8ad9c04b725e75643f737b077a5f0f53692fb8` | `da92c93dbb48b19d5301675fc1127bea0c8f1a47e9f426d9e38fe8c19a47930b` | revised |

[Current comparison, hard checks and paragraph-level story maps](story-review.md). [Shared research](research.md). Old scene/timing mapping is not valid for any alternative; root storyboard stays archival. New 02m has explicit action callback, new 10m adds the 2024 recognition after the named prisoner outcome. Transfer only after canonical runtime review and owner selection, without replacing pins.

---

## Historical notes (baseline, superseded where inconsistent)

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate

# Handoff — Great Locomotive Chase r1

- Channel: `nuviko_history` (current `channel.json` at fresh remote main: `active`); English narrative illustrated **Short**, RU complete natural reader translation only. This task authorizes **research/editorial text**, not production.
- Source base remote main at decision: `9b2f92c36b6c889f6628958a2b8192583e759ecf` (git tree `3aa3dceac8f988da6ebfd16cf0cb236c59b15b7e`); actual main and PR base are verified again at write. Revision `nuviko-general-locomotive-chase-r1`; sources G1–G5, P1–P2, D1–D2 in `research.md`. No production/run/reviewer IDs.
- **Exact portable transfer path:** `.agent/research/2026-11-13-nuviko-general-locomotive-chase/script.en.txt` master future TTS/SRT only after official gate and owner approval; `.agent/research/2026-11-13-nuviko-general-locomotive-chase/script.ru.txt` full owner translation (not Russian voice), plus `.agent/research/2026-11-13-nuviko-general-locomotive-chase/research.md`, `.agent/research/2026-11-13-nuviko-general-locomotive-chase/story-review.md`, `.agent/research/2026-11-13-nuviko-general-locomotive-chase/storyboard.md`, `.agent/research/2026-11-13-nuviko-general-locomotive-chase/packaging-brief.md`, and `.agent/research/2026-11-13-nuviko-general-locomotive-chase/README.md`.
- Missing runtime capability: no executable checked-out repository in current host for `uv run ytv start`. GitHub connector read/write is **not** ytv runtime. Thus no `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, registered run, leases, research/script receipts or `awaiting_script_approval` were created.
- Missing reviewer capability: fresh `sessions.independent`/host agent session not exposed by available tools. Original `ytv-script-review-v1` on exact EN SHA-256, twice-full-Short read, and independent EN/RU equivalent review are **UNVERIFIED**, not simulated. Author-only speech/loop desk check is not a gate. Actual voice/music/subtitle/AV seam **UNVERIFIED**.
- Image reference bytes: the `channels/nuviko_history/brand/VISUAL_PROFILE.md` was read, but original two PNG reference assets were not opened or hash verified; no 2D host is proposed in current scenes. Sources are only historical writing, not copied footage or image assets.
- Local transfer, **only upon separate owner's decision to progress this hypothesis**: in an actual local checkout, inspect remote main and existing run for duplicates; run `uv run ytv start --channel nuviko_history --format short --intent 'Review editorial candidate at .agent/research/2026-11-13-nuviko-general-locomotive-chase/script.en.txt with .agent/research/2026-11-13-nuviko-general-locomotive-chase/research.md, no media production'`. Read returned **real** `plan_summary`, `read_next`, `task_guide`, pinned documents and `next_action`, then import exact EN text and research into research/script tasks by their contract. No fabricated task receipts. The path is relative to repository root; use `--source-script` only when appropriate per actual CLI and authorization, preserving exact bytes.
- Obtain independent blinded reviewer once on exact EN plus its repeated text and literal seam through genuine host; retain verbatim `ytv-script-review-v1` tied to exact EN hash. Reviewer may reject story, scene or closing seam; synchronize EN/RU/storyboard/packaging on revision and repeat review for new hash. Show owner full script at real `awaiting_script_approval` only if actual runtime reaches it. A PR/merge provides no production authority.
- No TTS, image generation, render, upload, schedule, publish or merge permitted by this handoff. No source reference bytes or timings claimed.
- Repository-only checks performed: exact scene spans constructed from EN/RU masters, 14 scenes on both sides, full two-copy EN/RU text prepared for author loop desk read; actual remote ref/diff/PR and CI checked after commit separately. No executable local `python scripts/check_repository.py`, `uv` unit tests, production footage or media reviewer in this host. **UNVERIFIED** until observed.


## Editorial version transfer — 2026-11-17

Baseline branch head `7b0ba94a789120b0c4eb375f50f6a30de884ebae`; root originals remain at their exact Git blobs `f83dc170fb23e9c1b870aaab0d71aca391e25cfd` (EN) and `dd99bf0955ec417a0d7205de1a00411ddbbb3b5b` (RU). This append-only editorial package does **not** replace the original Short, create a ytv run, or alter production pins. Read the six full `variants/{02m,05m,10m}/script.{en,ru}.txt` and [exact hashes and review](story-review.md). 05m recommended editorial Long, **not accepted**. Short 02m retains the old 14-scene provisional storyboard; no original asset was re-bound to Long.

For official transfer select only one owner-approved exact EN text after independent first-listener review. In a runnable pinned checkout, invoke the supported `uv run ytv start --channel nuviko_history --format long --intent 'Review selected Great Locomotive Chase editorial Long candidate; do not produce media'` (use short if 02m selected), read actual context and attach the **real** selected bytes/supporting artifact IDs through task contract. Observe exact source hash and required approvals. This command is future guidance only; **not executed here**. Never switch an existing run's pins to PR checkout without explicit migration.

Remaining gates: independent session reviewer with real `ytv-script-review-v1` response tied to hash, bilingual first-listener judgement, runtime registration, exact owner master approval, selected Long storyboard and independent shot coverage review, actual image/voice/MP4 and release permissions. There is no TTS or AV evidence; media creation and publication are unauthorized.

## Editorial follow-up 2026-11-21 — 10m, no production

Revised full 10m narrative EN `variants/10m/script.en.txt` (SHA-256 `820d16a232b49b2903fa58044b39245180304590025efe42c9996afe6f8b2a0d`) and RU `variants/10m/script.ru.txt` (SHA-256 `3e91ea3cb46492096aafdd6c1b853965407c79fa4337a799e2e3208b2202810c`); baseline `3935d5c76a48ae51dec48bdffb40877aa63de46f` and old 10m hashes retained in story-review. Added government- and participant-supported October prison break, March prisoner exchange and Parrott's first decoration; stopped repeating abstract raid explanation after the train stalled. Independent reviewer, bilingual listening, production-run canonical pins, exact master approval, voice timing, new 10m storyboard and all media are UNVERIFIED. The old 14-scene storyboard belongs exclusively to untouched root/02m; do not reuse it or move runtime pins. Preserve approved or scheduled external artifacts; none altered here. Five-minute Long is still the provisional editorial recommendation; transfer via the existing canonical runtime and `attach-artifact` only after a genuine selection/verification.
