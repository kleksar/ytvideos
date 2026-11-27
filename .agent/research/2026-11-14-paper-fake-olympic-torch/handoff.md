## 2026-11-27 editorial revision

Baseline `a14e4950807e9bd8394565426e0e88a78f92a0bd`; canonical main `7c779c4b2fd379c85166ae1b164fa53d1ea08843` (#124 merged). EDITORIAL_CANDIDATE_UNREGISTERED. Original root scripts, old storyboard and 05m pair preserved. Only 02m and 10m variants changed; older pointers and assessments of those variants are historical. No approval, media, runtime lease or independent reviewer receipt inferred.

| Duration | EN | RU | Words EN/RU | Decision |
|---|---|---|---:|---|
| 2 min | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 249/194 | Revised; author seam checked |
| 5 min | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 602/495 | Recommended; preserved |
| 10 min | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1210/950 | Revised; target timing unverified |

05m remains preferred: its failed first attempt, replacement, police escort, official welcome and correction provide consecutive developments. 02m now answers the event before restarting and adds the exam payoff. 10m adds the authentic relay handover, the preparations of real runners, mayor's return indoors, Larkin's reported link to Marsden, and later documentary return; removes repetitive conclusion/2000 detour. At 140–160 spoken words/minute, actual 10m timing remains UNVERIFIED (and may fall short); no padding. No production started.

Current handoff: selected exact 05m Long only after owner choice; root storyboard.json remains bound to original 02m hash, NOT revised 02m or either Long. Old estimated timings/reviews for changed pairs invalidated. New version-specific visual map in story-review.md is editorial only. Transfer via canonical ytv start, context/pins, independent reviewer and exact owner approval; external active leases/runtime state are unavailable in Git-only host. Do not overwrite approved source or migrate pins implicitly. No publication.

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Transfer handoff — Paper Detour, fake Olympic torch (1956)

- Channel/format: `paper_detour`, `short`, English illustrated narration; RU is full semantic translation only, not a planned second voice.
- Verified prewrite `main` SHA: `636386783a13b7b11d2173c233b68654f43d9848`; source files were read on that SHA. See `research.md` for selection and URL/claim/evidence/uncertainty.
- This PR changes only its story package. No change to `docs/`, `.agents/skills/`, channel status, production or published materials.
- Script version: first candidate for this event; exact source text is `script.en.txt`, exact RU translation `script.ru.txt`. S001–S014 are mapped verbatim in `storyboard.json`. Duration not measured. No audio, images, video, external paid tool, upload or publication.
- Source dates/limitations: Barry Larkin interviewed in 2004 by The Independent; Irish Times 2000-06-10; historian's 2018-01-10 account; ABC description 2023-08-20 (audio NOT played); official 1956 torch collection; competing 2026-09-23 Short. Historical quotes NOT invented.
- Author checks: interest/clarity/fact/reach/loop discussed separately in `story-review.md`; text seam author PASS only. Independent, text-to-voice, subtitles and AV checks UNVERIFIED.
- Missing capability **in this execution host**: accessible repository checkout/runtime for `uv run ytv start` and live `sessions.independent` reviewer. GitHub connector can read/write Git objects but does not create a local run or produce a reviewer receipt.
- **Local transfer** (NOT executed): in an authorized clone at the exact remote revision, invoke `uv run ytv start --channel paper_detour --format short --intent 'Оценить сюжет о поддельном олимпийском факеле Сиднея 1956 года'`; read actual `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`; import `research.md`, `script.en.txt` and `script.ru.txt` as **candidate inputs** following the actual task contract (do not invent run ID/lease/receipt). Give the unprimed reviewer the opening, then the exact entire EN narration twice with seam, without author verdict/beat map. Only afterwards provide source ledger and strongest alternative. Record their original `ytv-script-review-v1` on the exact EN hash and rerun if changed.
- `awaiting_script_approval` is NOT achieved; no script approval, MP4 approval, production permission, provider reservation or upload permission is implied.
- Prior version handling: if script edited, preserve exact old EN/RU bytes as distinct versions, update every scene span and narrative statement, invalidate review/word timings and obtain a new independent response.

## 2026-11-16 superseding scope note: three-version editorial package

The bullets above describe the **original 2026-11-14 Short only**, not a claim that all scripts are Shorts. All unchanged original EN/RU and S001–S014 remain tied to source blobs `58a8b726d89142e9b136d54f1d21ec52ad8ba1a4` / `0ce453fd2f0e9971247a9ec578fa313add4f75d0`. `variants/02m/` copies those exact bytes. New standalone Long `variants/05m/`, `variants/10m/` need different storyboard, approximate timings and 10-second Paper Detour Long end-screen design after owner picks one. Do not re-use old 14 scenes or claim they span Long.

Recommendation: **05m Long**. See `story-review.md` for exact six SHA-256 and independent UNVERIFIED, `research.md` for E01–E05 source ledger / conflicting old accounts. Use correct `--format long` ONLY for the selected Long, inspect actual channel pin/spec, do not change the channel spec. The earlier `--format short` example above is still for the original 02m candidate, **not** the new recommended master.

No runtime checkout, `ytv start`, independent session or host TTS/MP4 observed here. After explicit owner choice, in an authorized checkout register the chosen exact script and supporting variants/review via the canonical artifact/helper interfaces, then obtain fresh independent first-listener and actual script gate per pins. Review not approved by writing this PR.