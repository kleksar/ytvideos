EDITORIAL_CANDIDATE_UNREGISTERED: no production/runtime state.

# Handoff — PR #121 family-photo same-story variants

**Source/baseline:** `584c8fffb6cdfc143111aa7109e754e9c6012ead` (root scripts, storyboard, prior review); read latest PR head before any continuation. Original root EN SHA-256 `08fc974695c8765092ddba48fb5567b826f809836fb2522fee946f260a8b267e`; root RU `a74944c0b722fc0bab80155e1378bf8876004e5157c47877327c6871eb7b50c9`. Neither original bytes nor old storyboard were overwritten.

**Current policy reference read:** remote main `bd5ae9b34749337e305a20345d163b7c2fa30827`, with #124's three-duration rule merged. Channel `two_ways_lab` supports English 1080×1920 illustrated Short, loop required, first-person participant narration. **Long has null video.canvas / fps**; 05m/10m remain editorial only. 02m is substantially longer than the normal 35–50 second Short target. `docs/standards/editorial.md` and `docs/standards/narration.md` read; exact run pins cannot be replaced by checkout.

| Duration | Complete EN/RU | SHA-256 EN | SHA-256 RU | Status |
|---|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) / [RU](variants/02m/script.ru.txt) | `3d9eac9b1068c8173535edb200c5e91a9b1c99f969ace490c6c271b78e076942` | `40a54ee2e7001db077732a302625ea45680d49ef402c152adfdb2f0bbd325ccc` | complete, author checked; independent UNVERIFIED |
| 05m | [EN](variants/05m/script.en.txt) / [RU](variants/05m/script.ru.txt) | `87ad4110fd1e417babfc45646f8b6d17455169343970812d47fbf0e86d3d3d96` | `dfecee73c1b3f3a983f7bd2b79a6d877021970b9e17010730198317551becdcc` | complete, author checked; independent UNVERIFIED |
| 10m | [EN](variants/10m/script.en.txt) / [RU](variants/10m/script.ru.txt) | `a1fffe73a6b996abc5292342c511f37f639b68ec59ef3f397999a4d71c37c728` | `00215ee60c26f9b0d54cead8d891c79ab11d81256793c01e8771856e20eabb5e` | complete, author checked; independent UNVERIFIED |

**Editorial recommendation:** 05m (C14 with grandmother G2 gives genuine second payoff). This is **not owner approval or production permission**. All six text hashes, 8-criterion reviews, individual story maps, evidence and comparative weaknesses live in [story-review.md](story-review.md). [model_check.py](model_check.py) verifies exact totals. Existing research/video comparisons are retained and unchanged in substance.

## Recovery path in capable host

This GitHub-only run can write versioned text but has no local persistent `ytv` runtime/store, pinned task packets or genuine independent first-listener available here. No `ytv start`, official script gate, artifact IDs or review receipts were created. On a capable host, fetch **remote main**, inspect ChannelSpec and this PR's exact SHA-256, register a **single selected supported exact** text via the canonical `ytv` start / attach-artifact / reading-packet flow. In a genuine new run, respect its pinned context and do not silently migrate active runs. Supply independent reviewer the exact unscored EN before research and preserve the actual `ytv-script-review-v1` reply; read RU separately. Any revision to its English bytes requires a new independent review and invalidates old timing/spans.

**Blockers:** Long configuration for recommended variant (not authorized to alter), independent first-listener, bilingual review, owner choice/approval, runtime registration, actual character/image reference bytes, revised storyboard, real TTS timing and MP4 loop. Do **not** use baseline S001–S011 with variants. No production, TTS, imagegen, upload, publication, auto-merge or merge authorized.
