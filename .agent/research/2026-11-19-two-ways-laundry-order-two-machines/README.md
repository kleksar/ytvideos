EDITORIAL_CANDIDATE_UNREGISTERED

# Two Ways Lab — The Dryer Decides Which Laundry Load Goes First

**RU логлайн:** я сравниваю две честные стратегии для одной стиральной машины и одной сушилки: A начинает с самой короткой стирки, B — с самой долгой сушки. В условной двухзагрузочной модели A заканчивает за **140 минут**, B — за **165**. Но если рубашки сушатся десять минут вместо сорока пяти, B побеждает **130 против 140**. Это проверенный математический расчёт, **не измерение настоящей техники**.

## Одна история — три полных редакции

| Target | Полный English (production candidate) | Полный русский | Editorial / actual production limitation |
|---|---|---|---|
| **2 minutes** | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | **STRONG_CANDIDATE — recommended**; illustrated Short available as a format, but 111s target exceeds channel's 35–50s normal Short |
| 5 minutes | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | STRONG_CANDIDATE editorial; **Long recipe missing / BLOCKED** |
| 10 minutes | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | REWORK editorial: added value falls with numeric density; **Long recipe missing / BLOCKED** |

All six are independent, continuous narrations with complete payoff. RU carries the same material story and model qualifications as EN, not three outlines. EN counts / estimated duration at 150wpm: **278 / 1:51**, **795 / 5:18**, **1570 / 10:28**. Actual TTS timing and final AV seam are UNVERIFIED; no live test.

**Why recommend two minutes?** The initial surprise and the controlled flip are both completely explained without forcing a viewer through multiple basket inventories. The 5m adds a third basket and shows that even the flipped two-basket winner can reverse again (A185 vs B190 in the fast-shirt three-load scenario). The 10m explores a different objective and all 24 permutations of four loads (A215/B235, best other order205), but the numbers make it less accessible. More runtime is not a reason to choose it.

## Evidence, review and production handoff

- [research.md](research.md) — eleven actual candidates, three competing finalist pitches including a stronger-visualized suitcase alternative, genuine public questions/YouTube-indexed examples, algorithm source and every reproducible model input/result, audience limitations.
- [story-review.md](story-review.md) — all six exact SHA-256 hashes and Git blobs, **separate 8-criterion authorial reviews** per length, principal weaknesses, statuses, model/translation/format/rights/loop/independent review separated.
- [packaging-brief.md](packaging-brief.md) — exact first words, two-method choice, headline/cover promise, full delivered payoff, proposed Short semantic seam and unverified next-video dependency.
- [handoff.md](handoff.md) — source main SHA, merged policy, runtime/reviewer format blockers, local integration path and required real confirmation.

**Current state:** Git editorial-only queue. No `uv run ytv start`, pinned task packet, run ID, independent reviewer, script approval, brand image bytes, TTS, video, MP4, CI claim, upload or schedule. A two-minute editorial recommendation is not the creator's script approval. Do not merge or manufacture media under this task.

Strongest alternative: roll vs fold clothing in one suitcase, potentially higher visual and broad YouTube appeal, but no controlled real measurements for an honest numerical winner; it was not dismissed as boring or forgotten.
