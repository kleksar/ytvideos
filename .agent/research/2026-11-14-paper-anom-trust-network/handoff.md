EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# ANOM handoff — text-only

- Channel `paper_detour`, active at fresh remote main `5d3222c8888c775d2195c8b2949949f2d992e98d`, illustrated EN Long 16:9. Russian reading translation; no Russian voice. Reference main tree `e92a9c5b9ee656aa1448f34264b217ca1d0cbe98`. 51? The exact scene count is 51, not a measured duration.
- Exact `script.en.txt` SHA-256 `524035d2a5c9c47a8805e661bd94845e5c8579b3923b82a46cb68ec38c714fb6` and whole RU master `script.ru.txt`. This editorial correction supersedes baseline `fabf7d4c3e01c0ad047e10249ed0c7e1830267df`; no prior official run, accepted script hash or approval exists. Read `research.md` for source-by-claim and historical uncertainty.
- **Observed blocker:** this execution container has `uv` but no checked-out private project with executable `ytv`. `uv run ytv start --channel paper_detour --format long --intent 'Исследовать и создать редакционный сценарий сильной истории для Paper Detour, без производства медиа'` exited 2 `Failed to spawn: ytv (No such file or directory)`. No `plan_summary/read_next/task_guide/pinned reference_documents` were produced. Session tool discovery had no `sessions.independent` or fresh `spawn_agent` host. Therefore official script gate and independent reviewer are NOT_DONE / UNVERIFIED.
- **Exact local transfer:** In an authorized local project checkout with the actual shared runtime Store, first check whether a matching run already exists; only if absent execute `uv run ytv start --channel paper_detour --format long --intent 'Review text-only ANOM editorial candidate; no media'`. Read actual `plan_summary`, `doctor`, and all `read_next.task_file`, `skill_file`, `requirement_files` and pinned reference documents; import these scripts/research as *unapproved inputs* using documented tasks. Obtain fresh independent `ytv-script-review-v1` on exact EN hash `524035d2a5c9c47a8805e661bd94845e5c8579b3923b82a46cb68ec38c714fb6`, preserve response verbatim; after that request genuine owner approval of exact text. Do not invent a run ID or change canonical rules to bypass limitations.
- Further open tasks: independent audience and bilingual review; exact references pixels/rights (paper plane S024 only planned); actual final voice timing, source images, subtitles, mix, end-screen, MP4 and real view QA; independent approvals. No work was done on any of these.
- Only Draft PR text-only scope. No merge, production media, TTS, imagegen, render, upload, publication, scheduling, channel changes or other branch updates. No credits spent.

## Revised draft identity

Prior EN hash `fc6186455c47d7aff433bc7dcf5dc42b55272f7fd176a213756e55ae28209021` at HEAD `fabf7d4c3e01c0ad047e10249ed0c7e1830267df` is superseded by `524035d2a5c9c47a8805e661bd94845e5c8579b3923b82a46cb68ec38c714fb6`. S042–S043 narration/visual coverage changed in both languages. Do not reuse former review results, estimates, or pretend the new script was approved; full independent review and runtime remain UNVERIFIED.


## Editorial queue amendment — 2026-11-16

The existing source is protected as-is: head baseline `a9dc6312be379c159c501609becb160b274f87b4`; old `script.en.txt` and `script.ru.txt` blobs `c11d85e2e460261c9fc7cd2d15d8d14906e6a374` / `29c4a34b91dbdfc84442dbd147dbb65914f3acac`. New complete 02m and 10m EN/RU files, plus verbatim 05m duplicates, live in `variants/`. See current `story-review.md` for every full link, SHA-256 and reason to prefer 05m. No master switch, no approval/migration, no media.

Preserved source `storyboard.md` has 51 EN/RU spans for **unchanged original / 05m ONLY**. 02m and 10m require their own freshly selected scene counts, exact spans/visual intent and subsequent audio-based timings. `packaging-brief.md` concepts still target the original/05m EN hash, not all variants. No prior timing or review applies to a new text hash.

**If transferred locally:** find a genuinely existing pinned run before considering `ytv start`; attach the selected exact text/research through canonical runtime inputs, obtain an independent unbiased `ytv-script-review-v1` response and then an actual owner decision. This branch has no official runtime gate or independent session. Do not treat Git CI as viewer evidence. Long is supported in the currently read Paper Detour ChannelSpec, but script selection is not production permission.
