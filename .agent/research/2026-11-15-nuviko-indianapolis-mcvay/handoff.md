# Current handoff — 2026-11-25

Baseline: `6e4124400ac9acd50e8f6fb66061f4bfe44560d4`; canonical main read at `a6023668001421b689a8142cebc0bd436545be6b` (#124 merged). Existing Draft PR #111 only. Root master EN/RU and original storyboard unchanged. The current 05m is **no longer byte-identical to root**. All six changed hashes invalidate prior variant review/timing/span evidence; old evidence below is historical, not current. Long 16:9 for all three; no Short loop required. `EDITORIAL_CANDIDATE_UNREGISTERED`; no owner approval, independent reviewer or runtime registration. Estimates at 130–160 EN words/minute before pauses and separate end screen, not measured. Existing voice settings unchanged.

| Target | Full EN/RU | Words EN/RU | Estimated EN duration | SHA-256 EN / RU |
|---|---|---:|---|---|
| 02m | [EN](variants/02m/script.en.txt) · [RU](variants/02m/script.ru.txt) | 278 / 251 | 1:44–2:08 | `6ed3425fde3b0bf6201597530eedbb716469e26f2e28a9b4183b02983fefaaeb` / `0b2356cd7d142b6854e9f5635cbf8e554b0002557636b55d85fb27881426553d` |
| 05m | [EN](variants/05m/script.en.txt) · [RU](variants/05m/script.ru.txt) | 755 / 664 | 4:43–5:48 | `896c30fc2105b150b794180e89b86eabad65f0286ec0d09fd5c95e76d8510879` / `6fdbc2f9f802b9c125a12c2e27ec849abb17597d2bd2f2682ee5c31b7d483c7f` |
| 10m | [EN](variants/10m/script.en.txt) · [RU](variants/10m/script.ru.txt) | 1519 / 1339 | 9:30–11:41 | `c40d4cf112564e229f95afa99aa5e3c597f2ed7262a5e381a275ff9d29926676` / `892a2d5dfb9f209dac498a5f71755c65acd8b7de9bdc3d1a99ac1523b7005503` |

Provisional selection: 05m. Before production, transfer the selected exact text to a verified canonical ytv checkout using current task contract, inspect actual run/context/pins and use explicit migration if necessary. No local checkout/runtime or independent review session available here. Give independent reviewer blind exact EN/RU texts before source ledger; preserve actual reviewer response. New storyboard must bind selected exact hash; root storyboard is valid only for unchanged root evidence. No run ID, receipt, media, approval or timing invented. See [review](story-review.md) and [research](research.md).

---

## Historical material — superseded where inconsistent with the current revision above

# 2026-11-18 three-length editorial handoff — USS Indianapolis / McVay

**Current status: `EDITORIAL_CANDIDATE_UNREGISTERED`.** One historical story, three complete EN+RU Long scripts; provisional recommendation **05m** only, with no independent reviewer, approval or verified local runtime. This section supersedes earlier source-only instructions but preserves them below for historical accountability.

- **Baseline branch HEAD:** `54fbb08ae6f234b67392d1bd3dc7837d2851f7fa`. Original [EN](script.en.txt) Git blob `347528bce1ad269fa3e5adf1aee1129aa408ece0` and [RU](script.ru.txt) blob `b3884363ebc46f3f2b692b8ba3431e4a409ec7e7` are **unchanged**.
- **02m Long 16:9:** [EN](variants/02m/script.en.txt) SHA-256 `1442226bf3d27b1c82e85583c286d743be9dbf2fe16b41a90fd20fee7cf226d0`; [RU](variants/02m/script.ru.txt) `c9fc7beb4fd3c563dc997f25674d9a087a8ef5cf3986df01d74f15a31fe5d3cd`. Fresh storyboard required if selected.
- **05m Long 16:9 — recommended:** [EN](variants/05m/script.en.txt) `f7c6c8180e8a4dbb8698710e918dcde3f74d6888bfe1f24cc81a2bec272e3f9e`; [RU](variants/05m/script.ru.txt) `df6416de61e408a3c298cc5db0c54e2277574d9744f67c3a3b4b7aa4201cf858`. Byte-identical to original root pair; source 26 semantic spans remain source-matched **but timing is not measured**.
- **10m Long 16:9:** [EN](variants/10m/script.en.txt) `dc31d3085b2602f0d45ebddda18d7f3f85ebfa0e7dc8a0bafb99c33ab441d01f`; [RU](variants/10m/script.ru.txt) `222f98239c7e398820a795d21eda85b1b1efb607030b17d83381e7caf2e4bfd8`. Fresh storyboard required if selected; old 26 spans do **not** cover 36 paragraphs.
- Full three-way story maps, separate editorial criteria and evidence limits: [story-review.md](story-review.md); new factual source ledger: [research.md](research.md); all descriptions and links: [README](README.md). No caption/TTS/frame/AV media evidence created.

**Next legitimate step only after owner chooses one exact EN master:** obtain actual `ytv start --channel nuviko_history --format long` / `status` in a verified checkout and preserve returned run/context/pins (no guessing). Register exact chosen script and version-support artifacts through the documented task contract. Give an actually independent fresh reviewer the exact text **without** this author's verdict first, then source ledger, solicit genuine English first-listener and bilingual fact assessment; reviewer records their own unmodified `ytv-script-review-v1`. A new hash needs a fresh response. Subject to exact owner script approval, hand off only the selected version for original meaning-aligned storyboard/timing. Do not auto-create three runs, reinterpret a PR recommendation as approval, start providers or affect saved runs.

**Main unresolved historical question:** precise scope/timing of Hashimoto's anti-zigzag statements during the original trial vs pretrial and later appeals; root 05m keeps original phrase. Independently fact-check before owner script approval, and if corrected rehash/review and rebind scene spans. Recorded public audience samples are not measured current demand. Expected runtime/audio/independent session access is absent in this GitHub editing environment: **UNVERIFIED**, not a fictitious run or receipt.

---

## Preserved previous handoff

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Handoff — USS Indianapolis / Captain McVay

Target: `channels/nuviko_history`, actual ChannelSpec `active`, English Long 16:9 illustrated. No Nuviko Videos music recipe. Base main SHA checked at authoring: `5d3222c8888c775d2195c8b2949949f2d992e98d`. Branch intended: `work/story-drafts/nuviko-indianapolis-mcvay-20261115`.

Exact source text: `script.en.txt` (future TTS/SRT master, only after approvals); full semantic Russian `script.ru.txt`. Claims/evidence/search counterdata in `research.md`. Scores and checks in `story-review.md`; per-scene exact paragraph spans and conceptual AI prompts in `storyboard.md`; honest packaging in `packaging-brief.md`.

**Capability missing:** Local git checkout and the project `uv run ytv start` runtime/store aren't mounted in this GitHub-connector host, so no real run, pinned read_next, plan_summary, task_guide, leases, source_script receipt, or official script gate exists here. No available independent session spawn tool from host registry was found, so original `ytv-script-review-v1` was not produced. This is a Draft editorial queue item and **must not be marked production-ready**.

**Exact local transfer:** On the proper ytvideos machine, sync the reviewed branch without merging it into main; inspect `AGENTS.md`, ChannelSpec and skill pins; execute `uv run ytv start --channel nuviko_history --format long --intent 'Review and register the editorial USS Indianapolis / McVay draft from .agent/research/2026-11-15-nuviko-indianapolis-mcvay'` prior to running the official new episode research/script. Read actual `plan_summary`, `read_next` task files, `task_guide` and pinned `reference_documents`. Revalidate sources, audience evidence, EN/RU; feed exact candidate narration to the official script task via its actual claim/inputs and receipt, not guessed fields. Run canonical `python -m ytvideos.script_review --script script.en.txt --output reader-input.json` (Long, no seam), deliver to a genuine independent fresh `sessions.independent` reviewer and preserve unmodified `ytv-script-review-v1` with exact SHA-256. Show full EN and RU for actual owner approval. Do not produce media or upload under this task.

Known open issues: viewer baselines n=2 only for one comparable source; own channel search terms, CTR, retention UNVERIFIED. 1945 visual archival reference images, rights and actual PNG assets not supplied. Current storyboard timing estimates are not voice alignment. Historic totals 315–317 / 1195–1196 vary slightly. User refusals #13 telegraph and #88 canal bridge remain untouched. No production permissions, merges or channel status changes.


## 2026-11-15 revision supersedes earlier handoff metadata

Parent SHA: `d79ec5a189a3c423d3c54efbc77488e3110ce3c8`. The revised EN/RU text has 26 semantic paragraphs and corresponding storyboard spans. The earlier wording suggesting a cleared/removed court-martial verdict is **invalid**; Congress's text was added to the personnel record in 2001 and the underlying conviction remained. Read `research.md` new revision section, `story-review.md` new ratings and `storyboard.md` instead of relying on the old scene count. Prior text hashes, lengths, approvals, author confidence, estimated timings and independent-review outcomes are STALE or UNVERIFIED. Obtain exact post-push HEAD and source hashes before official runtime registration. No official `ytv start` was invoked.
