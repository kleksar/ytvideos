EDITORIAL_CANDIDATE_UNREGISTERED

# Oceanos — editorial handoff / exact revisions

**Repo** `kleksar/ytvideos` — channel `nuviko_history`, English illustrated Long; observation 2026-11-17.

- **Source remote main:** `247ebe9245091972c5a93ecb84ce55ad8c15a211`. New story branch created only from this SHA, not from another open PR. Parent tree `ba3c89e835e4687b90b21f9ca199bf1add71f487`.
- **Editorial policy:** PR **#124 has merged**, so 2/5/10 requirement is read from current `main` `docs/standards/editorial.md` and `.agents/skills/ytv-write-script/SKILL.md`, not from the prior proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72`. This document does not import any unrelated PR changes.
- **No runtime start:** GitHub-only connector access permits text blobs/tree/PR; this session has **no local cloned workspace/runtime/database** from which to execute `uv run ytv start`, so no plan_summary, read_next, task_guide, pinned reference documents, run ID, lease, receipt or script gate exists. This is explicitly permitted *editorial Git queue*, not an official production run.
- **Independent review capability:** no available independent runtime reviewer/session with the required `ytv-script-review-v1` storage. Status **UNVERIFIED**. Author's `story-review.md` is not such a response.
- **Owner approval:** NONE. Five minutes is the *editorial recommendation only*; there is no approved TTS master, storyboard, image-generation or video authorization.

## Six exact outputs

| Edition | EN source / SHA-256 | RU complete meaning-preserving / SHA-256 | Author's decision |
|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) `a000bcefaa2419be0656468593df625ac65eefb50c6f0abbd5dd17134ea16964` | [RU](variants/02m/script.ru.txt) `bb69e35db88ae1eed3bf263757f023154881e5fba45b33e31df24dd12e598eae` | STRONG_CANDIDATE |
| 05m | [EN](variants/05m/script.en.txt) `ae540db53a7fb922b49d5878ce0180c03348b8aff1e3b371a0f133aa3b881b65` | [RU](variants/05m/script.ru.txt) `f01314b2da87de5f644637f503623ba925cea490ab8068d8eba39effc5b25094` | STRONG_CANDIDATE; recommended |
| 10m | [EN](variants/10m/script.en.txt) `9fb6046c916bc23a00c881c6cd7b002be0e5926ac0d4b8c65a38d55bab61e614` | [RU](variants/10m/script.ru.txt) `7e0c7c621162a77473a9662d7299d5325efe0263ccacb75885a19b2b38cf473c` | REWORK; full draft present |

Git blob SHA-1 from creation API, in the same order:

- 02m EN `e226b32f3808d841e11a63c9ef0ab0efeb7c4125`, RU `ce8e08613114356e692b2e530335b5a71f0e1666`.
- 05m EN `97a6bc133605ae76f34c4d82ef0a8d9e7d92003a`, RU `48697c45ddaddc2183af179fc8a9e3becf87970e`.
- 10m EN `3d50801bbe2a7f448eb2fadc057968c320152eb0`, RU `ee8ea0bb2791b2feb0639c1b7bbcffc10c8ff849`.

Shared supporting research `research.md`, individual version checks `story-review.md`, proposed title/cover `packaging-brief.md`. No storyboard/prompts produced because recommended script is not independently reviewed. No source/reference media bytes invented.

## Local continuation — do not import this queue as a finished script gate

1. Read **current** remote main, PR head, exact text hashes and runtime status; locate any existing run for the same idea before creating a new one. Compare current runtime pins rather than substituting checkout docs. Preserve all other story PRs and approved texts.
2. With an actual local checkout and user intent to develop the new script, use the current [ytv-start](../../../.agents/skills/ytv-start/SKILL.md) and current task contract. For instance, a new run is only appropriate if no existing run exists: `uv run ytv start --channel nuviko_history --format long --intent 'Oceanos 1991; evaluate editorial Git candidate and prepare one exact script'`. Read returned `plan_summary`, `read_next`, `task_guide`, `reference_documents` **before** execution. This command was **not** run here and may require an updated intent/route after an owner decision.
3. Submit **exact full 05m EN text** to a genuinely separate reader without the author's evaluation/beat map; first read opening, then the full text, then let them access research; capture its native unchanged review record using the canonical helper/schema. Repeat for another chosen version as needed. No fabricated PASS. New SHA-256 means a new review.
4. Verify the specialist diver details in full original March 1992 source before approving a 10m edition, and reconcile any contrary claims with the primary investigation; no inaccurate 571 vs 581 number should appear in public narration.
5. Register variants as `script_variant` and `story_review` artifacts with the real returned IDs and hash if runtime requires; obtain one exact master and owner script approval via normal two-gate workflow. Do **not** treat Git PR as a production-ready receipt.
6. For **approved** master only, obtain and inspect actual Nuviko traveler image PNGs, image/rights evidence and music; then tie visual scene spans and prompts to exact variant + SHA-256, verify voice timing, next-video intro asset and creative checks. Do not transfer spans from other versions or claim source media exist.
7. No merge, paid tools, vidIQ credits, audio, TTS, image/video providers, MP4, upload, publication or scheduling was performed by this editorial task.

**Remaining blockers:** independent review absent, registered runtime absent, final exact owner script approval absent, measured voice duration absent, 10m specialist-source full access missing, historical media rights/character bytes not inspected, next published Nuviko related video/real intro unverified. CI/read-back of this proposed PR tracked separately from artistic review.
