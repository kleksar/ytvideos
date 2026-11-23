EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff: Two Ways Lab — voice vs typing

Source verified remote main: `131ef24068d75967b1e43aa88e5f1370f6775054`; branch must be created from **this** commit for this proposal, not from another story PR. The #124 policy is **merged**, so current canonical `docs/standards/editorial.md` and writer skill on main apply; proposal revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is historical evidence, **not** the branch base.

Attempted actual command at task entry:
```sh
uv run ytv start --channel two_ways_lab --format short --intent 'Editorial queue: one new A/B story 2,5,10 min'
# error: Failed to spawn: ytv
# Caused by: No such file or directory (os error 2)
```
This isolated environment has no working ytv executable/project runtime, no pinned `plan_summary`, `read_next`, `task_guide`, `reference_documents`, no run ID, no lease and no independent reviewer session. The current work is explicitly allowed **Git-only editorial queue**, **not** the official script gate.

Package: [full 2m EN/RU](variants/02m/script.en.txt), [full 5m EN/RU](variants/05m/script.en.txt), [full 10m EN/RU](variants/10m/script.en.txt) with companion `script.ru.txt` in each folder, common [research](research.md), [story-review](story-review.md), [packaging brief](packaging-brief.md), and [README](README.md). Exact SHA-256, word counts and author checks are in story-review. No storyboard/prompts because a genuinely independent first read of the chosen exact variant has **not** occurred; existing media spans/timings do not apply to these texts.

Recommended exact editorial candidate: `variants/02m/script.en.txt`, SHA-256 `64798a4de3046935b8d50234c4261ab25730608f3d4306df288a8e6cc6c35dfb`; RU companion SHA-256 `7ed09960e59de7b9b92e6400822e542892718602adac624f4bfd465cdad9e8d3`. `STRONG_CANDIDATE` is author's editorial classification, **not** approval. 05m has Long production blocker; 10m additionally REWORK for duration and payoff density.

To continue in an authorized working checkout with actual dependencies:
1. Confirm this PR still Draft and correct canonical channel state, then start **one real `uv run ytv start`** for the owner-selected Short source. Read the actual `plan_summary`, `read_next`, `task_guide` and pinned `reference_documents`; if already registered, use `status`/`resume` not a duplicate run.
2. Attach all six exact scripts as `script_variant`, research and review as supported artifacts using official `attach-artifact` commands with actual source paths. Persist returned IDs/hash. No fictitious receipts.
3. Send exact full English candidate and full Russian companion *without scores or beat map* to a separate independent reviewer; first read then source fact check and repeat the literal Short twice. Save reviewer's own schema response unchanged. On substantive rewrite, re-hash and re-review.
4. If accepted by the reviewer, plan storyboard **only for selected exact hash**, read actual hero visual reference files + hash, prepare each frame logically in native Two Ways Lab style. No Paper/Nuviko visual import.
5. Confirm actual voice/TTS duration, applicable Short delivery and seam, applicable media rights. Submit one selected script through existing approval gate; do not create 05m/10m Long runs until a real compatible recipe is commissioned and configured.
6. Verify exact CI/remote head and receive explicit owner's master choice before production. `CI success` alone is not artistic acceptance.

Blocked: absent local ytv runtime; independent review access; actual TTS timing and AV seam; channel Long recipe; media/brand reference bytes; audience retention/demand evidence. No paid provider, TTS, images, MP4, upload, publication or schedule changes made.

## 2026-11-23 · existing PR #353 content revision

Original preserved HEAD: `6f3b974c3e57a6bab0b6ea497219fd10ea0d8197`. 02m/05m master texts, package and original historical author observations stay intact. **New 10m script SHA-256** EN `983bdaee9c0251594acea79a2909235731546cc589c18dd056e731211ba9e56a` / RU `f695d55d2e08d27c9da67f9debac0cee709c17875fe5f3bd967fa9e1cc38fdea`, 1239 EN words. Full paths [EN](variants/10m/script.en.txt), [RU](variants/10m/script.ru.txt). New causal beats and conditional E110=158-second countercase: [review](story-review.md#2026-11-23-substantive-review--10m-exact-revision-supersedes-earlier-10m-author-judgement), [research](research.md#2026-11-23-revision-specific-sensitivity-case-10m-only). The prior 10m script/evaluation SHA remains historical only. 10m likely under 10 minutes at normal speech, and production Long is separately BLOCKED by null canvas/fps. **02m still provisional preferred; it has not been approved**. Original [packaging brief](packaging-brief.md) remains associated only with unchanged 02m exact hash.

Pending real local `ytv` and genuine independent first-listener, import the exact preferred draft using canonical runtime context/pins, register variants and review as supporting artifacts and obtain **one** owner-approved script. For 02m reviewer, read full EN/RU twice with literal seam, not merely the last and first lines. New 10m hash invalidates any earlier 10m review (none independently observed). Recompute from remote bytes before importing. No agent/Codex session telemetry is available from this connector; the expected-HEAD branch CAS is the write-race protection. No media calls or production effects were authorized.
