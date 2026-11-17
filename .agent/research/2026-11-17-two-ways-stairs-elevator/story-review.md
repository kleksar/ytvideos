# Six exact scripts — author's editorial review

**Author:** GPT-6 writing agent, 2026-11-17. **Confidence:** medium on structural/artistic judgments, high on pure arithmetic as rechecked below, low on actual audience demand. All scores are subjective editorial estimates, never CTR, retention or likelihood of success. Independent reviewer: **UNVERIFIED**; a self-review is not independent.

## Exact script inventory

| Version | EN file / SHA-256 | RU file / SHA-256 | Words (EN / RU) | Target / expected reading range (not measured) | Editorial class |
|---|---|---|---:|---|---|
| 02m | [script.en.txt](variants/02m/script.en.txt) `0fcb1363d56996c44938098e17ef7dcc1d7865da930da2117fc7f1859625e342` | [script.ru.txt](variants/02m/script.ru.txt) `f55cb440d0b2b2f2a30e224035ac97a16533d7cb82d032a941a3cf0599c32123` | 296 / 261 | EN ~1:51–2:09; RU ~1:52–2:11 at 138–160/120–140 wpm; pauses unspecified | STRONG_CANDIDATE (editorial only) |
| 05m | [script.en.txt](variants/05m/script.en.txt) `d49893cab27936132be9351cfba68becde44048627dce1dd99a920283e25550b` | [script.ru.txt](variants/05m/script.ru.txt) `697340e0ae2e745815a43e50e1f351ab852d864078b094759926d3fb0bf1713f` | 792 / 677 | EN ~4:48–5:40; RU ~4:40–5:33 at 140–165/122–145 wpm; pauses unspecified | STRONG_CANDIDATE (editorial only) |
| 10m | [script.en.txt](variants/10m/script.en.txt) `6beeedee73102a1dfcfca2010fe21bbf50454aea7587e45b248617422899661b` | [script.ru.txt](variants/10m/script.ru.txt) `903fa4cb27dcb63054bab37acca48fb79d2b38bd7b385f01136336946c92f67a` | 1661 / 1364 | EN ~9:46–11:27; RU ~9:24–11:22 at 145–170/120–145 wpm; pauses unspecified | REWORK |

**Target-format note:** 2m is drafted as an independently complete Short with narrative_loop required, but the current active ChannelSpec's ordinary target is 35–50 seconds; compatibility **UNVERIFIED / production blocker**. 5m and 10m are proposed editorial Long scripts only; ChannelSpec has no operational Long canvas/fps/recipe (**production blocker**). No variant is approved for production.

## Eight criteria / every exact language text

Scale 1–10; demand evidence is **UNVERIFIED**, never set to zero or arbitrarily eight. Columns: interest/significance; opening; development; payoff; freshness of angle; visual expressiveness; clarity/natural voice; **evidence of audience demand**.

| Exact revision | Interest | Opening | Development | Payoff | Angle | Visual | Voice | Demand | Grounded observation and strongest flaw |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| 02m EN | 8 | 8 | 8 | 9 | 7 | 9 | 8 | UNVERIFIED | A switches from 64s to 73s, then the wait alone flips B to 37s; opening question and final same question after answer; main drawback: nearly two minutes is longer than this channel's normal 35–50s Short. |
| 02m RU | 8 | 8 | 8 | 9 | 7 | 9 | 8 | UNVERIFIED | «Кабина движется быстрее меня. Но по лестнице…» is the reversal; wait-only second calculation completes promise; main drawback: closing/question seam is conversational rather than a demonstrated AV loop. |
| 05m EN | 8 | 8 | 8 | 9 | 8 | 9 | 8 | UNVERIFIED | The 39s break-even, extra 18s stop, and fifth-floor reversal offer successive independent discoveries; drawback: 792 EN words may run longer than five minutes. |
| 05m RU | 8 | 8 | 8 | 9 | 8 | 9 | 8 | UNVERIFIED | «А для пяти лестница требует восемьдесят, лифт — семьдесят шесть с половиной» changes winner; hospital comparison gives real-world limit; drawback: floor calculations risk becoming too numerical when heard. |
| 10m EN | 8 | 8 | 7 | 8 | 8 | 8 | 7 | UNVERIFIED | Adds uncertainty/expected value, guaranteed deadline vs mean, fairness of restarting clock, and published fourteen-trip research; drawback: several calculations delay closing payoff and can cause numerical fatigue; REWORK. |
| 10m RU | 8 | 8 | 7 | 8 | 8 | 8 | 7 | UNVERIFIED | Explicit split between average time and sixty-five-second guarantee gives a new decision, not repetition; drawback: too many conditional examples without measured visual pace; REWORK. |

No score for audience demand; competitor pages do not establish retention or CTR. Interest, development and payoff each meet >=8 only for 02m and 05m. **10m REWORK** because development=7 despite substantial evidence and an additional decision criterion. Editorial score does not grant a production pass.

## Story maps and language parity

**02m:** promise/question «Would I reach the fourth floor faster by taking the stairs?» → two paths at one lobby → stairs 64s → lift 73s → unexpected 9s stair win → only wait changes 48→12 → lift 37s, 27s ahead → 39s tie / accessibility caveat → open question returns as narrator's next genuine decision. Exact EN/RU numbers and causality match. Short textual last→first: “...the old question has a more precise meaning. Would I reach the fourth floor faster by taking the stairs?” → first “Would I reach the fourth floor faster by taking the stairs?” This is an author-proposed narrative reset with completed result, **not independent seam PASS**. Actual AV seam **UNVERIFIED**.

**05m:** same setting and metric; start 64 vs 73 → threshold 39s → first flip at 12s wait → hypothetical intermediate stop of +18s shifts threshold to 21s → floor sensitivity at 1/4/5/8 → real Canadian study distinguished from model → conditional answer. All statements in EN/RU preserve illustrative assumptions, real study limits and no claim of self-performed race. Long narrative loop N_A.

**10m:** model definition and full journey → wait flip → stop flip → floor count flips winner → separately labelled uncertainty thought experiment (12/48 equally likely, expected B55 versus A64, risk threshold deadline 65) → published hospital study → fairness warning about switching strategies after 30s already elapsed → exact conditional verdict and limitations. Contains separate substantive inference not in 05m. The two translations carry same caveats. Long loop N_A.

## Verification matrix

| Check | 02m | 05m | 10m | Basis |
|---|---|---|---|---|
| Arithmetic/model | PASS author calculation | PASS author calculation | PASS author calculation | Independent formulas shown in [research](research.md); all totals recomputed |
| Source substantiation of actual study | PASS for attributed 2011 study | PASS | PASS | Primary open full-text paper; fictional model assumptions explicitly labelled |
| English/Russian semantic parity | PASS author reading, independent UNVERIFIED | PASS author reading, independent UNVERIFIED | PASS author reading, independent UNVERIFIED | Same actors, values, caveats, ending |
| Rights | PASS for newly written narration | PASS | PASS | Original text; third-party work paraphrased without borrowing dialogue/footage |
| Channel production compatibility | UNVERIFIED / blocked | FAIL: no Long recipe | FAIL: no Long recipe | Current channel.json and AGENTS |
| Narrative seam | UNVERIFIED | N_A (Long) | N_A (Long) | No independent double reading / no MP4 |
| Independent reviewer result/receipt | UNVERIFIED | UNVERIFIED | UNVERIFIED | Separate reviewer session not available |
| TTS durations / AV acceptance | UNVERIFIED | UNVERIFIED | UNVERIFIED | No TTS/media produced |

**Arithmetic audit:** A=16f; B=w+11+3.5f with no stop. At f4,w48: A64/B73; w12: B37. Equality w39. Add 18 stop => B55 at w12 or B91 at w48 and tie wait w21. At f1,w48: A16/B62.5. At f5,w48: A80/B76.5. At f8,w48: A128/B87. Independent two-point assumption (p=0.5 for 12/48): mean B(37+73)/2=55; A=64; deadline65 means A guaranteed and B wins only in short-wait outcome. **These are model calculations, not empirical measurements.**

## Added value versus duration and final recommendation

**2→5:** genuinely new causal tests: a halfway wait threshold, a passenger stop, and floor count changing the winner; inclusion of limited real hospital evidence. The script can fill 5m but is more technical than an ordinary 35–50 second Two Ways short.

**5→10:** adds a separate, explicit decision under uncertain waiting and a risk-sensitive deadline, followed by real-study qualification and the error of switching routes after sunk waiting. This is conceptually relevant but dramatically less compact; the expected audience drop point is the second numerical floor comparison / pre-expected-value transition. **Do not choose it merely for length.**

**Recommendation: 02m editorial master candidate**, because the entire promise and two genuine opposing outcomes are legible with the lowest computation load. It still needs Short length/production compatibility resolution and independent review. 05m is a worthwhile alternative editorial Long only, unsupported for production. 10m should be shortened or refocused before any further decision. This is a recommendation, **not approval**.

## Review scope

One author review of each of six exact texts, no simulated reviewer or review receipt. No complete formal reviewer round occurred; revision count after author full texts: 0. New hash requires new independent review. If the owner chooses 02m, import that exact EN/RU pair only after approved migration into a real ytv run, attach all versions and this comparison, then independent reading and script approval. No storyboard prompts or scene timings are claimed for other versions.

