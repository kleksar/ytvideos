EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Tunnel 57 — exact local handoff

**Channel:** `nuviko_history` (active according to main ChannelSpec, NOT music channel `nuviko_videos`). **Format:** English illustrated Long 16:9, 2560×1440/30 fps, Nuviko photoreal historical reconstruction; RU is reading translation, not voice. **Current status:** text-only authorial editorial candidate; no official run, no production-ready state, no actual approval.

**Verified base main (2026-11-15):** `5d3222c8888c775d2195c8b2949949f2d992e98d`, root Git tree `e92a9c5b9ee656aa1448f34264b217ca1d0cbe98`. A new branch from this base must be rechecked before push and PR publication. Source research uses recorded URLs and limitations in `research.md`.

## Content, identity and provisional outputs

- `script.en.txt` EN Git blob SHA: `537ab0539c1e6048fa28486d32f1f8c8f8e588ef` (552 words, 42 paragraphs). English is future TTS/SRT candidate only.
- `script.ru.txt` RU Git blob SHA: `50471b35bf32a42df2469d1bc931c0414c32bb24` (42 equivalent paragraphs).
- `story-review.md` Git blob SHA: `9385bc3a1a0ad95687011e5cf07b46088dc339b8`. Eight authorial criteria; no independent reviewer.
- `storyboard.md` Git blob SHA: `d268727748c4c85d7cfe4fa9e27b930f0376cb1c`. Forty-two provisional exact EN/RU spans. 4–6-sec holds are creative estimates, not measured TTS timecodes. End screen concept needs actual generation and QA later.
- `research.md` Git blob SHA: `521eb3f4af3858684b749c2faa6de1251de9bce1`. Historical claim ledger + selection + cautious YouTube sampling, no confirmed same-author baseline.
- `packaging-brief.md` has three different title/thumbnail hypotheses, none generated.

## Runtime blocker observed

Real terminal attempt in this host: `uv run ytv start --channel nuviko_history --format short --intent 'Исследовать сильный исторический сюжет для Nuviko History; сценарий без производства'` ended `Failed to spawn: ytv (No such file or directory)` (exit 2). That was only a capability check; it did **not** create a run, and no Long start was attempted. No pinned `plan_summary`, `read_next`, `task_guide`, `reference_documents` or task/claim/lease receipt exists. Project checkout or executable ytv CLI is missing in this host. Tool discovery also found no actual `sessions.independent` / fresh spawn_agent reviewer capability; changing author role is not independent review.

## Transfer in an authorized local checkout

1. Do not treat this PR as a production run. First inspect existing runs, current branch, canonical docs and ChannelSpec; do not register a duplicate if this exact story was imported elsewhere.
2. In the **authorized local checkout containing the real runtime and persistent store**, use `uv run ytv start --channel nuviko_history --format long --intent 'Проверить редакционную заготовку Tunnel 57, 1964, по сохранённым research и exact EN/RU script; довести только до script gate'`. Capture actual run ID, `plan_summary`, `read_next`, `task_guide`, pinned skills and all referenced documents. If CLI/provider missing, stop dependent step, not silently replace it.
3. Treat the two scripts and research as **unapproved imported candidate inputs**. Check facts and EN↔RU against exact bytes and historical sources, calculate actual SHA-256 in local runtime, record current provisional storyboard as a non-production coverage suggestion. Do not claim the above Git SHA-1 equals SHA-256.
4. Obtain a genuinely fresh independent first-listener and bilingual reviewer via available host. Show cold open, then exact full EN text without author score, then the full narration again (Long loop not mandatory). Provide sources and strongest Thai cave alternative **after** blind first reading. Require original `ytv-script-review-v1`, exact EN SHA-256 and observed findings. If the story is rejected/revised, update both scripts, dependent spans, hashes and review.
5. Only then present **entire** exact EN+RU for the owner's **explicit script approval**; await real `awaiting_script_approval` state, do not create fake approval IDs. This recurring Draft PR task grants **no** permission to make images, TTS, media, render, upload, schedule, publish or merge.
6. After actual separate production authorization, use channel pinned references and verify real identity PNG files and source rights; no claimed actual source bytes in this editorial packet.

**Measured results / external operations:** no live TTS/audio, no images, no MP4, no imported model reviews, no upload, no publication. vidIQ current available balance 0, no paid queries. Known blockers are runtime and independent review access; source and evidence search can continue free of charge.
