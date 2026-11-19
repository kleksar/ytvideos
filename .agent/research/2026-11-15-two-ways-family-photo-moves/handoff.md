EDITORIAL_CANDIDATE_UNREGISTERED: no production/runtime state.

# Handoff — PR #121 family-photo same-story variants

**Source/baseline:** `584c8fffb6cdfc143111aa7109e754e9c6012ead` (root scripts, storyboard, prior review); read latest PR head before any continuation. Original root EN SHA-256 `08fc974695c8765092ddba48fb5567b826f809836fb2522fee946f260a8b267e`; root RU `a74944c0b722fc0bab80155e1378bf8876004e5157c47877327c6871eb7b50c9`. Neither original bytes nor old storyboard were overwritten.

**Current policy reference read:** remote main `bd5ae9b34749337e305a20345d163b7c2fa30827`, with #124's three-duration rule merged. Channel `two_ways_lab` supports English 1080×1920 illustrated Short, loop required, first-person participant narration. **Long has null video.canvas / fps**; 05m/10m remain editorial only. 02m is substantially longer than the normal 35–50 second Short target. `docs/standards/editorial.md` and `docs/standards/narration.md` read; exact run pins cannot be replaced by checkout.

| Duration | Complete EN/RU | SHA-256 EN | SHA-256 RU | Status |
|---|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) / [RU](variants/02m/script.ru.txt) | `96b153a284578ae6b205b59b1a78940da2956fee488d9700c505e122a1a88168` | `ac32a22447b5d659a7ea1617e1e23571e1696a4e1a777f3b6f66f168ad4a55e7` | complete, author checked; independent UNVERIFIED |
| 05m | [EN](variants/05m/script.en.txt) / [RU](variants/05m/script.ru.txt) | `8e2b50fe1c50a1a21df8613b49c99cd549581885fba3d7bd4532d661c3a6a4c0` | `1d63f079f88621337653af4cb96029ce17c9d51f6e8be8601ec39e6938762308` | complete, author checked; independent UNVERIFIED |
| 10m | [EN](variants/10m/script.en.txt) / [RU](variants/10m/script.ru.txt) | `5afc73df229b9d0dfefeeabfa59903c9d157e95274acc05a607fc1659d2c2356` | `03b4f33970c02e5c9498e9fd91f701d4b0c4e69a67c3bcaae85dd550e8044800` | complete, author checked; independent UNVERIFIED |

**Editorial recommendation:** 05m (C14 with grandmother G2 gives genuine second payoff). This is **not owner approval or production permission**. All six text hashes, 8-criterion reviews, individual story maps, evidence and comparative weaknesses live in [story-review.md](story-review.md). [model_check.py](model_check.py) verifies exact totals. Existing research/video comparisons are retained and unchanged in substance.

## Recovery path in capable host

This GitHub-only run can write versioned text but has no local persistent `ytv` runtime/store, pinned task packets or genuine independent first-listener available here. No `ytv start`, official script gate, artifact IDs or review receipts were created. On a capable host, fetch **remote main**, inspect ChannelSpec and this PR's exact SHA-256, register a **single selected supported exact** text via the canonical `ytv` start / attach-artifact / reading-packet flow. In a genuine new run, respect its pinned context and do not silently migrate active runs. Supply independent reviewer the exact unscored EN before research and preserve the actual `ytv-script-review-v1` reply; read RU separately. Any revision to its English bytes requires a new independent review and invalidates old timing/spans.

**Blockers:** Long configuration for recommended variant (not authorized to alter), independent first-listener, bilingual review, owner choice/approval, runtime registration, actual character/image reference bytes, revised storyboard, real TTS timing and MP4 loop. Do **not** use baseline S001–S011 with variants. No production, TTS, imagegen, upload, publication, auto-merge or merge authorized.
