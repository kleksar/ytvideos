EDITORIAL_CANDIDATE_UNREGISTERED

# Nuviko History · USS Squalus — Git-only story handoff

**Source remote main at drafting:** `33bc7ddda96320be96c41c6b0aa385b4ea8e0131` (real main observed 2026-11-23; recheck before writing PR). **Policy:** PR #124 merged on 2026-11-16; its original proposed head `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is historical context, NOT current main/pinned runtime. Canonical docs read from that current main. **Branch:** `editorial/nuviko-squalus-rescue-20261123`; final PR HEAD is the authoritative committed revision, to be checked from remote.

**Execution boundary:** the current host does not provide a working checkout/binary `ytv`. Attempt: `uv run --offline ytv start --channel nuviko_history --format short --intent 'подготовка истории о спасении USS Squalus'` → `Failed to spawn: ytv; No such file or directory (os error 2)`. No `plan_summary`, `read_next`, `task_guide` or pinned `reference_documents`; **NO** official run, lease, receipt, independent script gate or approval has been created. This README/PR is expressly permitted Git-only editorial queue, not an executable episode.

### Exact six variants

| Proposed format | Full English master | Full Russian meaning | SHA-256 EN / RU | Author status |
|---|---|---|---|---|
| 02m Short | [script.en.txt](variants/02m/script.en.txt) | [script.ru.txt](variants/02m/script.ru.txt) | `010d4e8ae5c8d5d488bc669cc7821912ece50711541abf9a58b6e414f6dd7f30` / `6ba9cec015281808406fff53f4c8bc50bdde77e56fa4455064e759ffe975f283` | STRONG_CANDIDATE, independent loop/AV UNVERIFIED |
| **05m Long** | [script.en.txt](variants/05m/script.en.txt) | [script.ru.txt](variants/05m/script.ru.txt) | `8da96f2f246b9795e09fe336c2cd6dbf797b787c2643366acc0dedd36556eefe` / `1039347ec8908a783737f31ed5709bf4ea0875b82ba9d18d466e0ba76b7b0a89` | **STRONG_CANDIDATE · recommended; not approved** |
| 10m Long | [script.en.txt](variants/10m/script.en.txt) | [script.ru.txt](variants/10m/script.ru.txt) | `b7edcf56283406707bab782f4fa19bd6a663988ffac025d2b118bd67ffb11d7d` / `e837136df6902e5df1309b6d565056c3f6481f13264156e92ea5915ac6380e9a` | REWORK_PACING, complete story |

Full selection, URL/source observations, contradictory passenger counts, archival rights and limitations: [research.md](research.md). Author-only eight criteria per variant, exact hashes and honest QA matrix: [story-review.md](story-review.md). [packaging brief](packaging-brief.md) applies **only to the 05m SHA**.

### What to do when the actual local runtime is available

1. Fetch this Draft branch in a configured checkout, get the actual HEAD and validate **exact bytes/SHA-256** of all six UTF-8 scripts. Reopen the original 1939 Navy rescue operations report and diving log, reconcile `7+9+9+8` versus inconsistent secondary `26+7` / `25+7`, and confirm every claim. Do not overwrite pinned old runs.
2. Only under a genuine new-script/production owner decision, use official `uv run ytv start --channel nuviko_history --format long --intent 'actual owner instruction'` or the documented `--source-script` accepted-source route where applicable. This Git candidate does NOT retroactively supply a run before research; do not invent a run or approval. Read returned `plan_summary`, `read_next`, `task_guide` and all actual pinned references.
3. Provide an independent reviewer **exact text** without author scores/beat map. For Short, give two full continuous cycles and seek literal cold-start / seam observations. Save real `ytv-script-review-v1` output unmodified. A different SHA requires a new reviewer. Gate can fail and reject even this topic; author QA is not independent QA.
4. Present the three verified variants and results; ask owner to select **one** exact EN master. Proposed 05m is not authorization. Register supporting alternatives/review via existing `attach-artifact` interface, not new states or fictitious receipt. Obtain the required explicit script approval for selected master.
5. **Only then**, if production is expressly authorized, make a storyboard/preproduction packet bound to the selected exact hash, read Nuviko character source PNGs and verify actual bytes/hashes, secure asset usage rights, and check audio, 10s long endscreen with an actual related-video intro, word/SRT sync and final AV. No spans or timing may be reused from another variant.

### Outstanding checks

- **Historical source limitation:** direct full HTML fetch of official Navy `rescue_ops_report.html` and original 1939 lecture timed out (indexed excerpts read); reconcile named-count table before formal script gate. Demand/retention/CTR, video length and actual competitor watch **UNVERIFIED**.
- **Independent reviewer capability:** no fresh independent `sessions.independent` result available; do not simulate `PASS`.
- **Format/timing:** 02m Short loop author-provisional, AV seam unverified; 05/10 Long ChannelSpec supported, but TTS length and both end-screen native parts unverified. No corresponding approved next-video intro; do not fake one.
- **Visuals/rights:** the Nuviko actual turnaround/emotions PNGs, chamber/ship historical references and image rights have NOT been inspected or acquired by this Git-only script run; these are future storyboard/production blockers.
- **No side effects:** no docs/skills/runtime pins/channel status edits, no forced push or merge, no TTS, imagegen, external AI-video, MP4, upload, publication or schedule changes. CI for the final exact PR head must be checked and not treated as a script-quality/approval gate.
