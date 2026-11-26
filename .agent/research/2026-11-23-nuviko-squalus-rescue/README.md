EDITORIAL_CANDIDATE_UNREGISTERED

# Nuviko History — Eight Men Inside the Rescue Chamber That Got Stuck (1939)

**RU логлайн:** в 1939 году после затопления подлодки «Сквалус» из носовых отсеков спасли 25 человек. В стальной камере застряли последние восемь. Когда водолаз перерезал один заклинивший трос, второй едва не оборвался. Спасатели изменили плавучесть камеры так, чтобы повреждённый трос больше не поднимал её вес. Все 33 человека, пережившие затопление, оказались на поверхности; 26 погибли при первоначальной аварии.

**One real event, three complete standalone English narrations and three full Russian translations.** Independent review, measured duration, actual AV loop, runtime and user approval are NOT complete.

| Target / proposed format | Full RU | Full EN | Author result |
|---|---|---|---|
| 02m / Short 9:16 | [Русский](variants/02m/script.ru.txt) | [English](variants/02m/script.en.txt) | REVISED: unsupported assumed belief removed; independent loop + AV UNVERIFIED |
| **05m / Long 16:9** | **[Полный русский](variants/05m/script.ru.txt)** | **[Complete English](variants/05m/script.en.txt)** | **STRONG_CANDIDATE — recommended, NOT approved** |
| 10m / Long 16:9 | [Русский](variants/10m/script.ru.txt) | [English](variants/10m/script.en.txt) | REVISED: real extra rescue setbacks; 1303 EN words, possible UNDERLENGTH and independent pacing UNVERIFIED |

**Why 05m:** after the early 7+9+9 rescues the fourth ascent introduces a genuine new trap, followed by a checkable solution and complete human outcome. The revised Short removes unfounded mental-state narration. The revised 10m adds verified buoy-telephone/anchor/hatch problems, the failed reel brake, two failed replacement-wire dives, precise ballast stages and salvage setback, but its 1303 EN words risk undershooting ten minutes at faster speech; names and the late salvage detour require a blind reader. No invented drama or guaranteed views. Recommendation is not owner approval.

- [Evidence, 12-story screen and three real finalists, contemporary Navy reports, competing YouTube metadata and demand limits](research.md)
- [Exact six script SHA-256, all 8 editorial criteria for each variant and separate QA statuses](story-review.md)
- [Packaging concepts and promise → first evidence → payoff for selected 05m SHA only](packaging-brief.md)
- [Precise Git-only status, runtime/import route and remaining blockers](handoff.md)

**Critical blocker:** `uv run ytv start` could not spawn `ytv`; no official run/plan/pins/reviewer/approval. The full official 1939 Navy operations report could not be fetched directly (indexed excerpts corroborated); `7+9+9+8=33` versus some contradictory secondary `26+7` summaries must be resolved against the original named log before production. An archival clip listed for licensing is **not** licensed for reuse. No production, no merge, no channel scheduling edits. Source remote `main`: `33bc7ddda96320be96c41c6b0aa385b4ea8e0131`, current policy #124 merged.


## Revision progress — 2026-11-23

**Before:** PR #373 HEAD `a000ad1f14ca7a2d65c571ed2c58af8431d35106`: three full EN/RU versions, 10m with procedural padding and a questionable 02m assertion about passenger beliefs. **After:** 02m and 10m EN/RU substantively revised; 05m production/presentation hashes and its packaging brief explicitly unchanged. New script SHA-256: 02m EN `8713b07fede498ee96dae2c76d026d09aa7477a1b8c1070e15cf9903d0e0cff5`, RU `c389d9ea8f195eb8ca36e6bea50f49fc1cec600174d008ed7b27f3fff0e3129a`; 10m EN `e9a37f4173fd8833f5d75561fd0912499c2236f15ed10e3bc042e738478f89a2`, RU `ae774c7413eae993a7e7a87486f263d3d846a020173658c3de4516ab2a9b1fcc`. See [story-review](story-review.md#2026-11-23-follow-up--preserved-baseline-and-actual-editorial-change), [new primary evidence](research.md#2026-11-23-revision-specific-primary-source-evidence-new-10m-facts), [handoff](handoff.md). The actual new remote commit and CI must be confirmed after Git write; unverified results must not be promoted to PASS.
