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
