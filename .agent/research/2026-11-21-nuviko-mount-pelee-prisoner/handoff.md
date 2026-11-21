EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Nuviko History / Mount Pelée prison survivor, 2026-11-21

## Provenance
- Expected remote base `main`: `131ef24068d75967b1e43aa88e5f1370f6775054`, to be checked again before commit.
- Editorial policy #124 **merged** as observed 2026-11-21; canonical `docs/standards/editorial.md` and `.agents/skills/ytv-write-script/SKILL.md` read from current main, **not** unmerged proposed policy. #124 proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is historical merged head, not current main SHA.
- Read canonical AGENTS.md, documentation-index, writer skill, editorial, narration, workflow/development/task-contract/task-execution, hook patterns and Nuviko channel.json/AGENTS/README/PROFILE/brand VISUAL_PROFILE. No common docs/skills/ChannelSpec edits.
- Latest checked topic Draft PR was #339 Paper Detour; this one is Nuviko by actual remote rotation. No Pelée/Cyparis duplicate found among GitHub PRs searched; PRIVATE/SCHEDULED uploads not accessible, thus exhaustive YouTube queue duplicate check UNVERIFIED.
- The independent example texts were read from accepted B revisions: #20 S-5 `78b375bf0004fdeb45722e6106f2919f09e82fe1`, #25 Lawnchair Larry `28862598989045cd02990e654b086afae28fea59`. They were NOT modified.

## Runtime capability blocker
Attempted `uv run ytv start --channel nuviko_history --format long --intent 'Сюжетная редакционная заготовка Mount Pelée 1902: three complete 2/5/10m scripts'` in this host. Error: `Failed to spawn: ytv; No such file or directory`; no local repository environment / working `ytv` entrypoint. Official plan_summary, read_next, task_guide, pinned reference_documents, run ID, lease, receipt, script gate and approval are **NOT** present. Do not claim successful `ytv start`, independent review or approved master.
- Independent `ytv-script-review-v1` reviewer/sessions.independent not available in this run; all versions independent_review=UNVERIFIED. A later reviewer must read the **exact immutable text** without author ratings/beat map, from canonical reading input, then inspect sources after first pass. Don't backfill a result.
- This is only an explicitly permitted Git editorial queue item, not production. No TTS, images, video providers, MP4, upload, publish or schedule actions.
- The two Nuviko actual reference PNG images weren't fetched; any future storyboard/thumbnail work must inspect both actual bytes/hash before use. No fake media.

## Exact artifacts
All files are new under `.agent/research/2026-11-21-nuviko-mount-pelee-prisoner/`. Scripts are **six complete independent EN/RU narrations**, not outline expansions or concatenated master:
- 02m: `variants/02m/script.en.txt` / `script.ru.txt` (strong premise but Short seam REWORK).
- 05m: `variants/05m/script.en.txt` / `script.ru.txt` (editorial recommendation: narrative density, documents all central turns).
- 10m: `variants/10m/script.en.txt` / `script.ru.txt` (complete broader Long, Roddam witness and hazard-science context; weaker focus).
- SHA256 and Git blob SHA per text: see story-review.md. Any future text update invalidates hash-bound review/timing.

Supporting docs: `research.md` sources/funnel/YouTube limitations, `story-review.md` ratings/blocks, `packaging-brief.md`, and `README.md`. No storyboard/prompts generated yet because recommended exact script still lacks independent review (editorial says detailed storyboard **after** review).

## Transfer after owner/editorial decision
1. In working repository with installed `ytv`, read current **runtime pins**, verify channel active and supported long, start a **single** official run (`uv run ytv start --channel nuviko_history --format long ...`) before any *new* production research. Read returned `plan_summary`, `read_next`, `task_guide`, all pinned `reference_documents`; do not silently replace existing pins. A Git-only candidate is not a proof of a run.
2. Import shared research and six scripts with existing `attach-artifact --kind script_variant` and the review comparison `--kind story_review`, only following actual CLI instructions, capturing returned IDs/hashes. Choose ONE exact master for production and obtain canonical independent text review then owner script approval at real gate; do not silently treat recommendation as owner's selection.
3. Resolve remaining claims about scope of survivor counts from S1/S2. If editorial changes any exact narration, recalculate hashes and obtain fresh independent review. Estimate actual speech timing with approved voice at prescribed speed 1.1x only once.
4. Only after exact version is reviewed, develop detailed Nuviko storyboard bound to its hash. Obtain actual traveler references and rights before any scene generation. Save receipts; do not invoke media automatically based on PR.
5. CI for future PR head checks is not approval. Leave this PR Draft, do not merge or mutate scheduling.
