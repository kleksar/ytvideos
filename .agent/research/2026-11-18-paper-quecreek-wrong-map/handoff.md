EDITORIAL_CANDIDATE_UNREGISTERED

# Quecreek — handoff to an authorized local coordinator

## Identity and provenance

- Repo: `kleksar/ytvideos`; PR #232, branch `editorial/paper-quecreek-two-holes-20261118`.
- Source **remote main** (verified before new branch): `833e2cc2cb9c8d92bcdf9388cd2eb42755ca317f`; policy PR #124 was **merged on 2026-11-16**. Do not cite `7d6bdf7702a2a241a33a21677fce29f26ada9b72` as current main; that is historical proposed policy commit.
- Six narrations are from exact Git commit `e9259037c5254a2d571b3953cd11b13b63daacfc`; each `script.en.txt` and `script.ru.txt` and their SHA-256 are in [story-review](story-review.md). Recommended `variants/05m/script.en.txt` SHA-256 `25f2df5c320b0472a6de7b3612f82ba86c84cf1fe4b11631c4bf25ac5031c45d`. Its semantic RU SHA-256 `15c9cf2e64d157cb7c62d65e3cbbb8f4a09155e2dc6e24c40139f6c28212b0f2`.
- No changed common docs, skills, runtime policies or channel status. No media bytes, run IDs or reference screenshots included.
- No implicit migration of active runs or pins. Do not alter accepted source such as #20 S-5 and #25 Larry.

## Unavailable capabilities / verification

- This GitHub-connector editorial host has not executed a local repository runtime or `uv run ytv start`, therefore has **no real `plan_summary`, `read_next`, `task_guide`, pinned `reference_documents`, run/lease/approval**. The exception is editorial Git queue only, not official script completion.
- An independent `sessions.independent` reviewer with separate exact-text cold read has **not been observed/executed**. The author scores are self-review only. `ytv-script-review-v1` response: absent. Audio listening, AV loop, TTS duration and media rights UNVERIFIED.
- Actual user choice of one master, exact script gate and owner approval are **not given**.
- Detailed `preproduction.json`, storyboard scene prompts, spans and timing are intentionally not fabricated before independent selection/review. Scope only applies to `05m` after confirmation.
- A public next-video target has not been checked; Paper Long endscreen link remains `BLOCKED_NO_TARGET`, not a selected unverified URL.
- No vidIQ credits, images, TTS, Flow, MP4, YouTube uploads or schedule actions executed.

## Local continuation (only when authorized)

1. `git fetch origin`; check out the exact PR revision/commit, read [research](research.md) and [story-review](story-review.md); compare any updated GitHub HEAD and user decisions. Do not silently import an older current checkout or mutate existing run pins.
2. For a **new** work request, run one `uv run ytv start --channel paper_detour --format long --intent 'Quecreek mine rescue: draft 2/5/10m proposal and select one exact script'` **before local production work**; read its actual `plan_summary` / `read_next` / `task_guide` / pinned docs. If the owner expressly accepts this precise 05m script for production, use the actual accepted-source `--source-script /absolute/path/to/variants/05m/script.en.txt` route and real owner source event as documented in current workflow, **not** an automatic approval. Avoid two duplicate starts.
3. Attach/refer to the two alternative variant files and `story-review.md` through actual task-contract outputs/artifacts with real hashes/IDs. Get a truly independent first-listener result over exact EN and RU 05m texts, initially **without this author's assessment**, then show research and strongest Beaconsfield alternative. If rejected, preserve rejection; if edited, recalculate hashes and repeat review.
4. Ask the owner to choose and approve one exact master under the existing script gate. Only then prepare detailed illustrated scene prompts and a `preproduction.json` tied to the selected exact script SHA; resolve genuine physical image and paper-plane references by reading bytes/hashes, then validate with `uv run python -m ytvideos.preproduction` before production. A structural check isn't artistic review or owner approval.
5. Actual TTS and AV-based duration/loop, channel recipe, scene references and next-video target must each be verified independently; no media or publication is authorized by this PR.

Story review table status is editorial only; pending checks and absence of a local run are material blockers before official pipeline.
