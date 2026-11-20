EDITORIAL_CANDIDATE_UNREGISTERED — not an official run, script gate or owner approval.

# Pepsi 349 — local selection and runtime handoff

Original PR baseline commit `683b0f7a5bbae99ea6fdb0f21481e91adc44d9cf`, preserved original root masters `script.en.txt` and `script.ru.txt`. Three fully written bilingual editorial alternatives live under [02m](variants/02m/script.en.txt), [05m](variants/05m/script.en.txt), [10m](variants/10m/script.en.txt); complete owner-facing translations at matching `script.ru.txt`. Hashes, distinct story maps, source boundaries and eight-criterion evaluations are in [story-review.md](story-review.md). **Editorial preference 05m is not user approval.**

- Story/timing: source 05m retains 29 EN/RU blocks; 02m and 10m use their own paragraphs. Historical 25-shot `storyboard.md` is invalid for all. Do not inherit spans, timings, footage, packaging timecodes, reviews or approval. Rebuild only from the exact chosen script after real review/approval.
- Channel: `paper_detour`, EN narration with full semantic RU companion; all proposed variants **Long 16:9**, including the 02m brief edition, because no tested Shorts loop is claimed. The current `channel.json` supports Long and demands a 10-second themed end-screen after approval. Word-count estimates are not measured audio durations. Keep actual pinned production requirements and rates.
- Independent first-listener: **UNVERIFIED**. Actual independent host `sessions.independent` and live local `ytv` runtime were not available in this run. Reviewer must see exact EN/RU without author scoring, report concrete rough lines and first drop-off, then receive sources and earlier version. No synthetic receipt or run ID.
- Migration: coordinator reads existing run/status before starting anything; do not replace an existing run's pins with this PR checkout. For newly authorised use, take one exact selected script as `--source-script` through documented workflow, register true source and correct hashes, perform real independent review and request exact owner approval. This Git Draft is not `awaiting_script_approval`.
- Do not merge, move Draft, generate external/AI media or TTS, or alter scheduled videos, publication or channel policy.

## 2026-11-19 exact short-version change

02m EN/RU now describe Victoria Angelo's documented hopes for five children and distinguish her personal story from the **other claimants** in the 2006 court case. 02m EN SHA-256 `c027b99f1348e38d58f864118fc67b1d09138a3187348eb20e9d9762e73b9451`, RU `022202228807b2f66fc9662a12c6bd2650988607b73af84a14e8887cc52b82f9` (305 EN words). Prior 02m review/scene evidence is stale. Preserve untouched 05m and 10m, historical storyboard and master files; recommend 05m editorially, without authorization of any production. See story-review for eight checks and research for sources.
