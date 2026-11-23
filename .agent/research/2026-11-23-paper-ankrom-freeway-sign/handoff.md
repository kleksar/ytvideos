EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Ankrom freeway sign · 2026-11-23

**Status:** one complete three-duration, six-full-script **editorial Git candidate**; NOT an official `ytv` run or approved source, no reviewer receipt. The next chosen master is only a recommendation.

## Exact lineage

- Source **remote main SHA** read at authoring: `131ef24068d75967b1e43aa88e5f1370f6775054`. New PR branch created separately from this commit, never from another story.
- Main policy includes merged [PR #124](https://github.com/kleksar/ytvideos/pull/124), merged 2026-11-16; **not** the old proposal revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72`. Canonical files read from main: root `AGENTS.md`, `.agent/documentation-index.md`, `.agents/skills/ytv-write-script/SKILL.md`, editorial/narration/workflow/development/task contract, Paper channel.json/AGENTS/PROFILE/PAPER_PLANE/thumbnail playbook.
- Last actual drafted story before attempt: [#368](https://github.com/kleksar/ytvideos/pull/368), Two Ways Lab. Therefore Paper Detour chosen. Existing rejected #13/#88 and protected #20/#25/#46 unchanged.
- New story files only under `.agent/research/2026-11-23-paper-ankrom-freeway-sign/`; shared docs, channel status, scheduled releases, production media, other PRs untouched.
- Source research: [research.md](research.md). Author ratings and exact SHA-256: [story-review.md](story-review.md). Provisional packaging: [packaging-brief.md](packaging-brief.md).

## Variants/next chosen input

| Variant | Production EN | Complete RU | Editorial status |
|---|---|---|---|
| 2m / Short | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | REVISED — author-checked contrast seam; independent/AV UNVERIFIED |
| **5m / Long** | **[EN](variants/05m/script.en.txt)** | **[RU](variants/05m/script.ru.txt)** | **STRONG_CANDIDATE, recommended** |
| 10m / Long | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | REWORK — diminishing new viewer value in second half |

Recommended script exact SHA-256: `7a1b87cbe472784d24867ddfa0b091cd7349f835976ed0845f10c79890f6d562` (includes terminal LF). Not owner selection, approval, or independent review. All EN/RU versions are complete. No production master has been chosen. Revised 02m SHA-256: EN `d099b88483fd23a5e566b883e284067092f3ab2cfdd1577d4b5f5898613b4739`, RU `d1a98ba955a1031cfe8e1d26638d38633fef3ec7f7f15f291a6ae05c136976d5`; the exact old hashes remain in [story-review.md](story-review.md). Independent reviewer must compare both exact 02m texts blind-first.

## Observed blocker / migration path

Attempt to run canonical `uv run ytv start --channel paper_detour --format short --intent '...'` failed in this execution environment: `Failed to spawn: ytv; No such file or directory (os error 2)`. No plan_summary, read_next, task_guide, pinned reference_documents or run/lease could be produced; **do not fabricate them**. The separate Git-only editorial queue is explicitly permitted. Independent external first-reader/reviewer capable of saving the strict existing receipt is also **unavailable**, hence review = UNVERIFIED. First-reader input must contain the exact master without the author's verdict/ratings/beat maps; give sources **after first reading** and keep its original result, not a paraphrase. New text hash requires new review.

**Local transfer after choosing a text:** on actual equipped host, check branch/PR and verify SHA-256, invoke actual `uv run ytv start` with the chosen Paper format and the owner's specific intent; read returned plan_summary/read_next/task_guide/reference pins and follow `docs/operations/task-contract.md` for `attach-artifact --kind script_variant` and `--kind story_review`. Import **one exact recommended selected script** into the normal script gate, obtain independent review/approval; do not backdate receipts, change active pins or bypass ownership decisions. If a run already exists, use `status`→`resume`, not a duplicate `start`. Then write storyboard/prompts tied to the chosen variant+hash with full Paper style and real assets. Only authorised later production may do TTS/media/MP4. Visual-rights provenance, timing, AV seam (2m) and final owner master selection remain pending.

PR checks: never treat queued/in_progress as PASS; inspect exact remote HEAD and checks after write. No automatically scheduled publication.
