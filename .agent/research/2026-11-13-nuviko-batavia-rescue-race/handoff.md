EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate

# Handoff — editorial candidate Batavia rescue race

- **Candidate:** `nuviko-batavia-rescue-race-editorial-v01` / `.agent/research/2026-11-13-nuviko-batavia-rescue-race/`.
- **Channel/status at observation:** `nuviko_history` / `active` from main `channels/nuviko_history/channel.json`. Not musical `nuviko_videos`.
- **Format:** English 9:16 Short; RU is reading translation only; no Russian audio.
- **Verified remote main HEAD at preparation:** `96c8fa1573c02e8e7987e272a569bf34f037691e` (tree `a2d08903183e88f5c8b9870cd01ea39bc56f98cb`). **Git branch's source/base is this commit** unless explicitly rebased in a later separately authorized change.
- **Sources inspected:** National Museum of Australia May 15 2026 revision (https://www.nma.gov.au/defining-moments/resources/wreck-of-the-batavia), WA Museum including published excerpt of historical Pelsaert journal (https://museum.wa.gov.au/research/research-areas/maritime-archaeology/batavia-cape-inscription/batavia/index.html), ANMM 2024-09-12 (https://www.sea.museum/en/article/the-batavia-shipwreck-disaster). Access 2026-11-13. Claim/evidence/uncertainty in `research.md`.
- **Revision IDs:** `research:editorial-v01`, `script:en-v01`, `translation:ru-v01`, `storyboard:visual-provisional-v01`, `packaging:brief-v01`. These are **local editorial labels, not canonical ytv task IDs or hashes**.
- **Exact complete draft narrations:** `script.en.txt` (188 words, editorial estimate only) and `script.ru.txt`. No production voice timings.
- **Scripts and storyboard:** scene S001 covers exact EN/RU first two lines; S002–S015 cover each remaining line in order; do not overwrite scripts with prompts. No media assets.
- **Own checks:** EN/RU meaning and written loop text inspected; see `story-review.md`. Independent interest, independent bilingual review, independent 2× Short read, `ytv-script-review-v1`, exact script hash, AV loop and consumer QA = **UNVERIFIED**.
- **Missing capabilities:** no local checked-out `ytvideos` project or executable `ytv` entrypoint/run store in this host; no `sessions.independent` or separate independent reviewer. This task cannot execute the official `uv run ytv start`, inspect the actual `plan_summary`/`read_next`/`task_guide` and pinned reference_documents, or produce actual task receipts or `awaiting_script_approval`. GitHub connector is only a source/PR transport.
- **Live workflow:** none entered. PR / merge neither registers the episode nor proves readiness; the narrative remains a proposal.

## Local agent path — requires a new explicit owner instruction

1. In a clean local `ytvideos` checkout, fetch latest `main` and this PR branch; evaluate whether the candidate should be developed at all, considering existing releases, reviews and rejected topics. If proceeding under the owner's express order, run **before new official research**: `uv run ytv start --channel nuviko_history --format short --intent 'Подготовить исторический Short о Batavia 1629 и гонке лодок за спасательным кораблём; редакционный кандидат лежит в .agent/research/2026-11-13-nuviko-batavia-rescue-race/'`.
2. Read the command's actual `plan_summary`, `read_next`, task packet, `task_guide`, pinned channel/reference docs and runtime capabilities; use the real run ID and real research/script input hashes and task receipts. Our draft is evidence/hypothesis, not an accepted official script or an approved `--source-script`.
3. Perform the prescribed research/selection and script tasks. For the exact EN output, summon a fresh independent reviewer with the full Short repeated *literally twice*, exact text/hash and the EN end→start seam, plus initial cold reading uninfluenced by author assessment; obtain actual `ytv-script-review-v1` output. Reviewer may reject topic. Separately validate RU meaning (or mark independent bilingual review UNVERIFIED).
4. Only after verified receipts may the run reach `awaiting_script_approval`. Show the entire exact EN/RU script to the owner for explicit approval. **No production or media tasks** may start from this automation, PR or merge; local agent needs a new specific owner instruction and current workflow approvals.
5. Do not modify channel status, common docs/skills, any other contributor's active PR, or try to infer missing TTS/imagegen/timing assets.

No force-push, merge, TTS, image generation, render, upload, release or extra Issue was undertaken for this editorial candidate.
