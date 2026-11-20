EDITORIAL_CANDIDATE_UNREGISTERED

# Handoff — Paper Detour, Pendleton 1952

**Task type:** Git-only editorial candidate, never an official production script completion. **Repository:** `kleksar/ytvideos`; **source main** `58c22b4e9d53330bd072457c10bddb40854db224` (fresh 2026-11-17 read). **Policy:** PR #124 merged: exact canonical documents on main; prior proposed revision `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is **not** current main nor a pinned reference revision. Existing active runs continue with their own original pins; migrate only on explicit request. Branch proposed: `story/paper-pendleton-second-rescue-20261117`, based *only* on current main above.

## Exact contents and selection

- 02m: [EN](variants/02m/script.en.txt) `5bfc160bbb54c59e8d3e2c3b3497b5979e73f86d444b3d9710816d37b5769968`; [RU](variants/02m/script.ru.txt) `5c0e5ee19fa56b4f8161891de3efc25921d1f5deeaef7086b85795b57e619960`. `STRONG_CANDIDATE`.
- **Recommended editorial** 05m: [EN](variants/05m/script.en.txt) `db96dc473fb7c468552479a3e2cfa425c7475fdcd1612e6d61c04853a5c65a06`; [RU](variants/05m/script.ru.txt) `cfefb1d783f4b26eb67406a38376ffd135e55abe9737e99ee3104b37739d60b1`. `STRONG_CANDIDATE`.
- 10m: [EN](variants/10m/script.en.txt) `1a59a3c2b4a87baecfc978a59e6d8abe07d9002251d988062e2c0d1ae4d49d2b`; [RU](variants/10m/script.ru.txt) `1950ea979015c95010e8c460b7b5a9c27ff1af4133ade9a4aa20ecb634efe0b3`. `REWORK`.
- [Full shared research](research.md), [six per-text ratings, full story maps and comparison](story-review.md), [packaging](packaging-brief.md), README. No media/reference files or fake agent responses.

## Exact capability blockers (current execution host)

1. **Runtime:** the execution host provides a GitHub connector and a global `uv` binary, but **no mounted `ytvideos` project checkout with configured local `ytv` command, task database, secrets and artifact store**. It is not possible to execute a valid `uv run ytv start` here, nor to read actual `plan_summary`, `read_next`, `task_guide`, `pinned reference_documents`, lease or receipt. **Zero actual run IDs.** Git-only candidate is explicitly allowed for this editorial queue, but must not be renamed a production run.
2. **Independent review:** no available independent session/reviewer capability was invoked, no fresh `ytv-script-review-v1`, no first-listener response. All grades in story-review are the *author's*, not independent evidence. An author reread is not a reviewer.
3. **YouTube evidence:** one very recent long maritime episode found in third-party indexes but differing reported views (86.7K versus 499K) and publish dates (October 11 versus 13, 2026). Direct watch URLs returned throttling/errors. No full accessible transcripts, real comments, Paper channel comparable baseline, actual CTR or retention. Demand for this exact 05m paper format = **UNVERIFIED**.
4. **Production:** Paper Long recipe does exist; **actual runtime and voice timing still unavailable**. No licensing review of specific assets, no actual reference image bytes, no planned frame timestamps, no accepted storyboard, no TTS, no footage, no Flow, no MP4, no publishing credentials or approval. Editorial score/CI do not authorize any of them.

## Transfer to an authorized local capable checkout (separate owner-controlled action)

1. Read latest `AGENTS.md`, `.agent/documentation-index.md`, `ytv-write-script` and pinned task instructions, current Paper `channel.json`/`PROFILE.md`; verify exact selected Git blob/SHA-256 and any concurrent PR, duplicate or owner decision.
2. **Before new production research/write actions**, start a **single actual** `uv run ytv start --channel paper_detour --format long --intent 'prepare reviewed Pendleton rescue script from editorial candidate'` *only when the owner requests a run*. Read real `ytv plan` (`plan_summary`), `read_next`, task guide and pinned reference documents. If an existing run is found, continue it rather than duplicating.
3. As supporting evidence attach the three exact EN/RU pairs with `attach-artifact --kind script_variant`, shared `research.md` as source evidence and `story-review.md` as `--kind story_review` using contract-defined real `--source`. Save returned artifact IDs / bytes / hashes, no invented IDs.
4. For proposed 05m English exact hash, generate the canonical independent reading input using `uv run python -m ytvideos.script_review` with the actual contract flags; give a fresh reviewer exact full EN **without author grades/map**, then full RU and historical evidence only after first reading. Reviewer can reject premise or format; preserve their genuine response in existing schema. Any text revision invalidates previous hashes and spans/reviews.
5. If and only if ready, present *all three complete versions* and recommend one exact master for actual `awaiting_script_approval`. Only owner's real selection/approval can register one master. If 10m selected, it is REWORK and requires justified editorial recheck. Do not create three production runs.
6. **After exact script approval**, check real Paper reference bytes and rights, draft detailed scene plan / prompts only for approved text/hash, select real images/audio and use normal production workflow/approvals. No video provider run or upload was authorized by this Draft PR.

**Unperformed by this PR:** no merge, force-push, deletion or update of another PR, shared docs/skills, channel status, schedule, paid credits, SFX, TTS, image generation, Google Flow, MP4, upload or publication.

**Next rotation:** if remote after this PR still has its story as latest, next channel Nuviko History; always recheck remote first.
