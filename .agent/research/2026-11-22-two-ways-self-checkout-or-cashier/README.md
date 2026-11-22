EDITORIAL_CANDIDATE_UNREGISTERED
# Two Ways Lab — I Chose the Shorter Line and Finished Later

**RU логлайн:** у кассы самообслуживания почти нет очереди, но с восемнадцатью одинаковыми товарами при объявленных условиях быстрее кассир: 149 против 161 секунды. С шестью товарами победитель меняется; на пятнадцати — ничья. Это *модель*, не снятый эксперимент и не реальные скорости магазина.

| Version | Full EN | Полный RU | EN words | Proposed format | Author status |
|---|---|---|---:|---|---|
| 2m | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 256 | Short, duration exceeds 35–50s channel orientation | **STRONG_CANDIDATE; recommended editorial** |
| 5m | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 762 | Long not configured | STRONG_CANDIDATE editorial; production BLOCKED |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1657 | Long not configured | REWORK, padded sensitivity discussion; production BLOCKED |

**Recommendation:** the **2m EN master**, because the basket-size reversal and the full answer land without the long digression. It is a complete ~2-minute **editorial** Short proposal, **not** a production-ready 35–50s Short. Do not truncate or silently speed up accepted narration; register and review exact master, resolve the channel-length mismatch with owner before production. 5m/10m remain alternate editorial manuscripts, not authorized Long production.

**Exact context:** source main `131ef24068d75967b1e43aa88e5f1370f6775054`; #124 merged, so editorial policy read from main. New story branch from this main only. Last verified story PR #367 Nuviko; chosen next channel Two Ways. Closest related PR #136 compares queue arrangements, #272 checkout package value: not this **staff-assisted service rate versus self-scan service rate with the same items** question. Remote dupes need recheck before PR.

**Evidence files:** [research](research.md) (funnel, source accuracy, audience limits, formulas, alternative), [story-review](story-review.md) (eight criterion per variant, hashes and independent-review blocker), [packaging-brief](packaging-brief.md), [handoff](handoff.md).

**Unavailable capability:** `uv run ytv start --channel two_ways_lab --format short ...` cannot start: `Failed to spawn: ytv — No such file or directory (os error 2)`. No saved run, plan_summary/read_next/task_guide/pins, script gate, lease, receipt, or approval. Independent reviewer not available. To transfer: check out exact reviewed commit on a real project runtime, execute `uv run ytv start --channel two_ways_lab --format short --intent 'staff vs self checkout modeled comparison'`, read returned plan/inputs/pins, attach exact scripts/review by existing artifact contract and submit **one** selected exact EN master for independent review and owner approval. Do not auto-produce alternatives.

**Other blockers:** NO authorized Long recipe in current ChannelSpec, no measured voice duration, no independently observed exact loop or AV seam, no clearance of any future images or trademarks. 5/10 are editorial proposals only. Do not request TTS, media, MP4, or publishing via this PR.
