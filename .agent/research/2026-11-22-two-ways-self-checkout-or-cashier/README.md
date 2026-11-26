EDITORIAL_CANDIDATE_UNREGISTERED
# Two Ways Lab — I Chose the Shorter Line and Finished Later

**RU логлайн:** у кассы самообслуживания почти нет очереди, но с восемнадцатью одинаковыми товарами при объявленных условиях быстрее кассир: 149 против 161 секунды. С шестью товарами победитель меняется; на пятнадцати — ничья. Это *модель*, не снятый эксперимент и не реальные скорости магазина.

| Version | Full EN | Полный RU | EN words | Proposed format | Author status |
|---|---|---|---:|---|---|
| 2m | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 256 | Short, duration exceeds 35–50s channel orientation | **STRONG_CANDIDATE; recommended editorial** |
| 5m | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 762 | Long not configured | STRONG_CANDIDATE editorial; production BLOCKED |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1533 | Long not configured | **REWORKED editorial**: decision robustness under uncertain wait; independent review UNVERIFIED; production BLOCKED |

**Recommendation:** the **2m EN master**, because the basket-size reversal and complete answer land before the longer uncertainty analysis. It is a complete ~2-minute **editorial** Short proposal, **not** a production-ready 35–50s Short. Do not truncate or silently speed up accepted narration; register and review exact master, resolve the channel-length mismatch with owner before production. 5m/10m remain alternate editorial manuscripts, not authorized Long production.

**Exact context:** source main `131ef24068d75967b1e43aa88e5f1370f6775054`; #124 merged, so editorial policy read from main. New story branch from this main only. Last verified story PR #367 Nuviko; chosen next channel Two Ways. Closest related PR #136 compares queue arrangements, #272 checkout package value: not this **staff-assisted service rate versus self-scan service rate with the same items** question. Remote dupes need recheck before PR.

**Evidence files:** [research](research.md) (funnel, source accuracy, audience limits, formulas, alternative), [story-review](story-review.md) (eight criterion per variant, hashes and independent-review blocker), [packaging-brief](packaging-brief.md), [handoff](handoff.md).

**Unavailable capability:** `uv run ytv start --channel two_ways_lab --format short ...` cannot start: `Failed to spawn: ytv — No such file or directory (os error 2)`. No saved run, plan_summary/read_next/task_guide/pins, script gate, lease, receipt, or approval. Independent reviewer not available. To transfer: check out exact reviewed commit on a real project runtime, execute `uv run ytv start --channel two_ways_lab --format short --intent 'staff vs self checkout modeled comparison'`, read returned plan/inputs/pins, attach exact scripts/review by existing artifact contract and submit **one** selected exact EN master for independent review and owner approval. Do not auto-produce alternatives.

**Other blockers:** NO authorized Long recipe in current ChannelSpec, no measured voice duration, no independently observed exact loop or AV seam, no clearance of any future images or trademarks. 5/10 are editorial proposals only. Do not request TTS, media, MP4, or publishing via this PR.

**2026-11-23 editorial progress (10m only):** `102ed6a39153bfe62cee0f3b299b5cd8aa244e58` → verified remote commit is recorded in the PR progress comment. New EN/RU 10m exact SHA-256: `764a131675b25e9570fb0e342633b1a9372f5759cea7e7caff75350518b4f868` / `8878ad934f6032dbb4dd9a23e584e9e62ca00e218c56e7c491d65af95028b188` (1533/1306 words), previous `02b5d68577c6b0e775f3692b10c19200baecf516c0482734b87e64693a35d844` / `2c4b11c04d0633552305b5576e6ef97c610a2302d7a89cc775e99973fe32f217`. Difference: adds the consequential A queue uncertainty range 70–100 seconds, demonstrates unstable eighteen-item choice versus more robust six-item choice, then tests a 45-second help delay and q=89 crossing. This is a hypothetical model only; independent review remains UNVERIFIED. 02m and 05m exact scripts unchanged; recommendation remains **02m editorial**, not owner approval.
