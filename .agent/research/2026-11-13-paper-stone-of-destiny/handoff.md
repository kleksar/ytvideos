## Revision: three narration lengths (2026-11-17)

**Status remains EDITORIAL_CANDIDATE_UNREGISTERED**: neither 05m nor 10m is an approved source. Baseline `904407730fdb82d703d0b19a16e81542a465b411`. Original Short and its old storyboard have not been altered. Complete text options: [02m EN](variants/02m/script.en.txt) / [RU](variants/02m/script.ru.txt), [05m EN](variants/05m/script.en.txt) / [RU](variants/05m/script.ru.txt), [10m EN](variants/10m/script.en.txt) / [RU](variants/10m/script.ru.txt). Exact SHA-256 and review coverage: [story-review](story-review.md).

**Editorial recommendation = 05m Long**, not permission to start a Long render. The channel's `long` format is described in current `channel.json`; runtime execution still requires actual pinned task context and a single owner-selected exact master. Do not import the previous root Short when producing the recommended Long; select the exact variant path after reviewing current state. Explicitly preserve existing run pins and approved media if any other worker has registered them since this Git-only candidate was written. Before any start, check saved run/active production and resume rather than duplicate.

No independent review host or executable ytv checkout is available **to this GitHub connector session**. The PR gives no proof of a session elsewhere; check locally. The CLI example below was written for the original Short and is retained as historical guidance only. For a chosen **new Long** with no existing run, use canonical `ytv start --channel paper_detour --format long --intent 'evaluate Stone of Destiny variant and present for approval'` from the current pinned workflow. Then attach exact six scripts/this review with real IDs, do independent blind-first listening on each candidate, register only a single chosen script, request actual owner's approval, and build new storyboard from that hash. No TTS/MP4/images may be started under this task.

---

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate

# Handoff to local agent
- Channel: `paper_detour` (Paper Detour), active in `channels/paper_detour/channel.json` on checked remote main 182d251810e9a23d61960b15ba86acb4053094a0.
- Format: English narrative Short 9:16, handwritten/physical layered full-frame paper dioramas only after formal user approval.
- Current branch: `work/story-drafts/paper-stone-of-destiny-20261113`; textual source directory: `.agent/research/2026-11-13-paper-stone-of-destiny/`; source revision: Git commit of this PR (read actual SHA from PR, **not a fabricated value**).
- Exact EN script: `.agent/research/2026-11-13-paper-stone-of-destiny/script.en.txt`; RU owner text: `.agent/research/2026-11-13-paper-stone-of-destiny/script.ru.txt`; research `research.md`; tentative art guidance `storyboard.md`.
- Background references read: root AGENTS, main workflow/editorial/visual/thumbnails/development, ytv-start and ytv-write-script, channel.json/profile, PAPER_PLANE and thumbnail playbook. Actual media image reference bytes not available; listed art assets are not inspected images.
- Missing capabilities: this automation host has remote GitHub read/write and public web, but no checked-out repository for `uv run ytv start`, no `sessions.independent`/independent script reviewer. No run, task IDs, output receipts, `ytv-script-review-v1`, script hash approval, or user approval is claimed. Independent interest and bilingual checks UNVERIFIED.

## Exact resumable local procedure (do not treat editorial PR as official stage)
1. Use fresh clean checkout and remote `main`, check git status and other workers' branches; open this PR and inspect eight text files before importing.
2. BEFORE any production: `uv run ytv start --channel paper_detour --format short --intent 'Исследовать и представить сценарий Stone of Destiny 1950; использовать редакционный кандидат и проверить факты/интерес, без медиа до явного согласования'`. Persist actual run ID/plan_summary. Then open exactly the paths in `read_next`: saved task packet, `task_guide`, skill, pinned `reference_documents`; use actual task `context`, not this unregistered README as an authoritative runtime task.
3. On legitimate research/script tasks, submit exact content by the CLI's `next_action` and save returned real research/script task receipts, `source/revision` IDs and hashes; recheck selection against changed queue and owner feedback. If another live run already owns this story, resume it instead of creating a duplicate.
4. Independent fresh reviewer receives first lines, original full EN twice and literal EN seam with exact file hash, without author beat map; they can reject interest. Preserve original `ytv-script-review-v1` and independent bilingual review or mark UNVERIFIED. Make applicable legitimate `narrative_loop` evidence. Do not forge a receipt or invent `awaiting_script_approval` before actual runtime gate.
5. Only after completed script gate show full EN+RU and seek real owner's approval. Only after explicit approval from owner under current workflow, run actual image/audio/video tasks; today's automation permission does not authorize media or publishing.
6. Art references must be obtained as real bytes and exact hashes before generation; check Paper plane cameo S010 against `channels/paper_detour/brand/PAPER_PLANE.md`, thumbnails/crop and paper-full-frame QA. The storyboard is not timed by TTS.
7. Before merge, recheck main/PR diff/CI/other branches and ask owner to review; **no automated merge**.

## Planned editorial check, not independent acceptance
AUTHOR PASS for interest as hypothesis, factual caution and EN/RU parity, literal textual EN+RU loop; INDEPENDENT UNVERIFIED; AV UNVERIFIED; runtime script gate **NOT REACHED**. 2026-11-13 source references: https://www.policemuseum.org.uk/crime-casebook/interesting-cases/the-stone-of-destiny-1950/, https://www.historicenvironment.scot/about-us/news/20-facts-revealed-about-the-stone-of-destiny/, https://www.theguardian.com/news/1950/dec/27/mainsection.fromthearchive, https://perthmuseum.co.uk/the-stone-of-destiny/.
