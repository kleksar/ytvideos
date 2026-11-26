EDITORIAL_CANDIDATE_UNREGISTERED — not an official run, script gate or owner approval.

# Pepsi 349 — local selection and runtime handoff

Original PR baseline commit `683b0f7a5bbae99ea6fdb0f21481e91adc44d9cf`, preserved original root masters `script.en.txt` and `script.ru.txt`. Three fully written bilingual editorial alternatives live under [02m](variants/02m/script.en.txt), [05m](variants/05m/script.en.txt), [10m](variants/10m/script.en.txt); complete owner-facing translations at matching `script.ru.txt`. Hashes, distinct story maps, source boundaries and eight-criterion evaluations are in [story-review.md](story-review.md). **Editorial preference 05m is not user approval.**

- Story/timing: current 05m uses 27 EN/RU blocks (supersedes historical 29-block copy); 02m and 10m use their own paragraphs. Historical 25-shot `storyboard.md` is invalid for all. Do not inherit spans, timings, footage, packaging timecodes, reviews or approval. Rebuild only from the exact chosen script after real review/approval.
- Channel: `paper_detour`, EN narration with full semantic RU companion; all proposed variants **Long 16:9**, including the 02m brief edition, because no tested Shorts loop is claimed. The current `channel.json` supports Long and demands a 10-second themed end-screen after approval. Word-count estimates are not measured audio durations. Keep actual pinned production requirements and rates.
- Independent first-listener: **UNVERIFIED**. Actual independent host `sessions.independent` and live local `ytv` runtime were not available in this run. Reviewer must see exact EN/RU without author scoring, report concrete rough lines and first drop-off, then receive sources and earlier version. No synthetic receipt or run ID.
- Migration: coordinator reads existing run/status before starting anything; do not replace an existing run's pins with this PR checkout. For newly authorised use, take one exact selected script as `--source-script` through documented workflow, register true source and correct hashes, perform real independent review and request exact owner approval. This Git Draft is not `awaiting_script_approval`.
- Do not merge, move Draft, generate external/AI media or TTS, or alter scheduled videos, publication or channel policy.

## 2026-11-19 exact short-version change

02m EN/RU now describe Victoria Angelo's documented hopes for five children and distinguish her personal story from the **other claimants** in the 2006 court case. 02m EN SHA-256 `c027b99f1348e38d58f864118fc67b1d09138a3187348eb20e9d9762e73b9451`, RU `022202228807b2f66fc9662a12c6bd2650988607b73af84a14e8887cc52b82f9` (305 EN words). Prior 02m review/scene evidence is stale. At that historical revision 05m and 10m were untouched; preserve historical storyboard and master files; recommend 05m editorially, without authorization of any production. See story-review for eight checks and research for sources.

## 2026-11-24 — current 10m revision

Baseline `6e515fef07007a7b4c4b4cbf579af53333715b46`; canonical main `a6023668001421b689a8142cebc0bd436545be6b` (#124 merged). Original 02m/05m and root master unchanged. Old 10m EN/RU blob SHA `158f6fa39c55e9b88ac856cdc4517eae761f705e` / `9dd72b520ece975d2ae194ea93c9a4dd5dcb05fd`; old text SHA-256 `b04e3fa200216ac508728caed29912caf2667739593933ca34cbcc0e33b1e7c0` / `a02a5ae11d68bb4078cb636203a9b1e35104e9bc853d038151b58c75b0a3e967`. New 10m: 1617 → 1283 EN words; 1367 → 1072 RU words; 23 aligned paragraphs; SHA-256 EN `a48e9163079240b79cd5b3cf1c9fb37af82f4cea3f87cad75775219a22267eee`, RU `e631bd784c8ea8277d302714f8d0f1e4a1ecc8af99da09cff669738d9ed76bec`. Estimate at hypothetical 125–155 wpm: 8.28–10.26 min, excluding pauses and 10s end screen; exact 10m remains UNVERIFIED. No prior 10m evidence applies. Recommendation 05m remains provisional; independent reviewer, runtime, rights, actual timings and owner approval UNVERIFIED.

10m authorial spans are in story-review, not production shots. Paper plane: candidate in bank-counter diorama at P06, no historical assertion. Actual reference, rights, final location and QA not available. Linked ending after P23: dependent on a verified related released/approved video and actual intro clip; do not invent a target or authorize media. Existing 05m packaging is unchanged.

## 2026-11-24 — exact 02m/05m factual and causal correction

EDITORIAL_CANDIDATE_UNREGISTERED. Baseline `e48087cc525fd022c22917e7dc98268ddbb0b49b`; canonical main `a6023668001421b689a8142cebc0bd436545be6b` (#124 merged). 10m and original root master/storyboard preserved; the root master contains superseded claims and must not be selected as current 05m. This is a bounded correction of unapproved alternatives, not a production instruction.

| Target | Full EN | Full RU | Words EN/RU | SHA-256 EN | SHA-256 RU | Decision |
|---|---|---|---|---|---|---|
| 02m Long | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 297 / 281 | `98b3e1dab86b68cdbe53295b1219ae25ab8e876082b71177200f5c2143238315` | `d4e0b65579b22bb5628972b779c81a90fc78cd4c82966bcf318209b95b8a6ab7` | Factual repair |
| 05m Long | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 730 / 633 | `ef436c78d48535a9a4d74b71e4ce73e10f9a6d7dc8207a98807c9f075bf385ee` | `87dd2366ee033b0b61393c2cc5e1779485b237a7f298909ae3272b3af568141f` | Factual and payoff repair; recommended |
| 10m Long | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1283 / 1072 | `a48e9163079240b79cd5b3cf1c9fb37af82f4cea3f87cad75775219a22267eee` | `e631bd784c8ea8277d302714f8d0f1e4a1ecc8af99da09cff669738d9ed76bec` | Preserved |

Old 02m/05m SHA-256 (EN/RU respectively): `c027b99f1348e38d58f864118fc67b1d09138a3187348eb20e9d9762e73b9451`, `022202228807b2f66fc9662a12c6bd2650988607b73af84a14e8887cc52b82f9`, `cc8459a28a341ae5e8112194583b7f306c8f6a283d1e12ddb3c0e43f6a544b90`, `cea3c6c3827eed80475337450c8edb541f64f6bea577814e916556781a507ef3`. Previous 02m/05m exact-script evidence is stale; 10m hashes and evidence remain unchanged. EN estimated at illustrative 125–155 wpm, excluding pauses and end screen: 02m 1.92–2.38 min; 05m 4.71–5.84 min; 10m 8.28–10.26 min. Actual timing UNVERIFIED.

Before → after: 02m no longer claims a majority of protests were peaceful without a denominator; specifies offer deadline, claimant argument and unknown individual legal outcome. 05m removes the invented cap-table action and unsupported audience quantifier; opening asks what distinguished valid caps, not the unestablished root cause of mass printing; the concrete seven-cap claim and actual published prize range replace repeated code exposition. The final court decision now resolves the two men's claims and expired goodwill offer before returning briefly to Victoria. The separate damages track, two-key vault and full award ladder still belong to 10m. Source-backed and bilingual author check only. No owner approval, no independent reviewer, no runtime receipt.
Current 02m/05m spans and independent-review blockers are in story-review. Do not use historical root as 05m or inherit storyboard. Register only selected exact bytes with canonical context; no production authorized.
