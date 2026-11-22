EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate

# Handoff to local agent (not a registered episode)

- **Repo:** `kleksar/ytvideos`; **branch:** `work/story-drafts/nuviko-great-diamond-hoax-1872-20261113`; **main source SHA:** `9218c2c12fad948a90960b6a22cc79ec67261ec0`; **channel:** `nuviko_history` (main ChannelSpec says `active`), English illustrated narrative **Short**.
- **Candidate revisions:** `editorial-en-v1` and `editorial-ru-v1`; no accepted production-script SHA-256, no frozen task pins, no run ID. Git blob SHAs are available in GitHub tree after commit; check exact bytes and hash on local host. Source evidence is `research.md` with source access date 2026-11-13.
- **Exact files:** `.agent/research/2026-11-13-nuviko-great-diamond-hoax/script.en.txt` (EN future narration master), `.agent/research/2026-11-13-nuviko-great-diamond-hoax/script.ru.txt` (owner review only), `.agent/research/2026-11-13-nuviko-great-diamond-hoax/research.md`, `story-review.md`, `storyboard.md`, `packaging-brief.md`.
- **Actual capability gap:** this agent environment has `uv` but no executable `ytvideos` checkout under /mnt/data; no host tool for a fresh `sessions.independent` reviewer was found. Thus `uv run ytv start`, `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, research/script task receipts, original reviewer `ytv-script-review-v1` and state `awaiting_script_approval` have NOT happened. User never approved exact text. This PR is NOT ready for media.
- **Scope:** research and editorial text packet ONLY. Do not merge automatically, render, TTS, imagegen, upload or publish from this branch. Real character/reference image bytes, audio timings, seam, audience performance and independent EN/RU review: UNVERIFIED.

## Portable next steps in an actual local checkout

1. Fetch this PR and read all eight text files, current remote main standards, channel config and current story queue. Review copy and claims, check live current branch/base and own changes.
2. **Before treating the text as a new production artifact**, start a genuinely new official run under current workflow (do not invent prior run):
   ```bash
   uv run ytv start --channel nuviko_history --format short --intent 'Review and develop editorial hypothesis Great Diamond Hoax 1872 in .agent/research/2026-11-13-nuviko-great-diamond-hoax; no production without owner approval'
   ```
   Record the actual returned `run_id`, `plan_summary`, `read_next`, `task_guide` and pinned `reference_documents`, and follow real `research`/`script` task contracts. The candidate `script.en.txt` is NOT a user-approved `--source-script`.
3. Reverify sources, choose or reject this story against latest queue, perform live independent full EN double-read and exact-hash `ytv-script-review-v1`; a new reviewer must be able to reject. Complete bilingual comparison and capture real task receipts. After substantive edits, synchronize RU, all storyboard spans and exact text seam; preserve previous revisions.
4. Show full EN and RU to owner at actual script gate; only real owner approval of exact revision permits further workflow. This automation explicitly forbids media and merge, irrespective of GitHub checks or reviewer outcome.

**Checks performed in this editorial-only host:** GitHub remote head/tree and existing PR/Issue/branches read; 16 exact EN/RU scene spans matched to script source, text loop logically reviewed, external sources inspected. **Not performed:** checkout `uv run ytv`, repository-local unit/eval tests, real host reviewer, bilingual independent review, voice, video, AV check; GitHub CI checked on new exact commit separately after push.

---

## 2026-11-17 addendum — updated variant selection and exact refs

The preceding instructions described the original Short and remain historical context, **not** automatic authorization. Latest complete story alternatives now live at:
- 02m: `variants/02m/script.en.txt` SHA-256 `bf7c7b8970faf1a2e7e14c14cd1761de35c5542a9f2409da16853fa7cabf5958` and `variants/02m/script.ru.txt` SHA-256 `8b3b9c042856f97acee9b7338e299bc06ad12269636293ab4ced044aaacd6bc5` (byte-exact originals).
- 05m: `variants/05m/script.en.txt` SHA-256 `baf1e32252edd54e2ff6730cdf223351d6f302229aae3c3fb902e0accbbd2be6` and `variants/05m/script.ru.txt` SHA-256 `fcc64829b2f4928f4408de784f5422ef104535f85a3b4de066bb432859876e09`; **authorial preferred Long**.
- 10m: `variants/10m/script.en.txt` SHA-256 `fa3bb5444e8baac8ade307b593cf0f6acdd61e5d645b8e1d121f012253b81db1` and `variants/10m/script.ru.txt` SHA-256 `8a7cf1a8fdddd61dcb63c1975d1d262380b46e2e2688ad9f935fe9ec8a09217f`.

No approved master: do **not** use the old Short-only example command to implicitly choose production for the preferred Long. In a genuine local checkout with current `main`, inspect current runs/pins first; register a new `nuviko_history --format long` run **only if no relevant existing run** and after mapping to the actual runtime requirements. Attach supporting variants/review through existing artifact API; then complete genuine independent blind review and actual owner choice/approval for **one exact script hash**. A Git-only status remains `EDITORIAL_CANDIDATE_UNREGISTERED`; all TTS, media, source reference bytes, timing and measured viewer signals remain `UNVERIFIED`.

The old S001–S016 preliminary storyboard and all its scene spans belong **only** to the unchanged 02m original SHA-256 `bf7c7b8970faf1a2e7e14c14cd1761de35c5542a9f2409da16853fa7cabf5958`. Any 05m/10m production needs new scene count, full semantic spans, and visual intent after master selection. No storyboard reuse, automatic pins migration, budget spending or production has been performed.


### 2026-11-22 · exact 10m re-edit, superseding previous 10m only

Full [10m EN](variants/10m/script.en.txt) SHA-256 `fefce974e5930fedc17fe62692e449d3c442b2c013a84f15c6fca7ea894cd5dc` and [10m RU](variants/10m/script.ru.txt) SHA-256 `0ac9f83ce226b6a19875670c580d3ed15b1604b503e3e89b334d84551524625f` (1293 EN words) replace the earlier **unapproved 10m candidate**, not original root or 02m/05m. Full research claims and limits are in [research](research.md#2026-11-22-10m-claim-check); story map, eight criteria and changed hashes in [story-review](story-review.md#2026-11-22--substantive-10m-second-edition-new-exact-hashes). Recommended 05m remains unchanged; independent exact-hash comparison, runtime registration, owner approval, audio and Long scene spans not performed. For future local agent, fetch current branch, verify these exact hashes and canonical context/pins, use real `ytv start` only if appropriate and never mistake editorial Git text for official task result. Status `EDITORIAL_CANDIDATE_UNREGISTERED`.
