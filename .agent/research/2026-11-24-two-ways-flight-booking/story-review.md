# Author review — exact variants

Author: ChatGPT editorial agent, 2026-11-24. Confidence moderate for narrative judgments; high for explicit arithmetic; low/unverified for real audience demand. Not independent review or script approval. Reviewed clean EN/RU texts in this package; no audio. Word count below counts whitespace-separated words. Estimated spoken target assumes approximately 125–155 English words/min and 105–140 Russian words/min (working estimates, not voice calibration), pauses included only as rough allowance, no measured timing. Exact speaker duration, final AV and channel readiness UNVERIFIED.

| File | Words | SHA-256 |
|---|---:|---|
| [variants/02m/script.en.txt](variants/02m/script.en.txt) | 286 | `d9a972c32b40bec7f1f8e361f84d60d5d50cf2c63a5b18bed61a70a16e85eddf` |
| [variants/02m/script.ru.txt](variants/02m/script.ru.txt) | 227 | `f76ec2c74c520e908388ae6e20525bfc69fa533bc5ce1b48a8bb16c299382b10` |
| [variants/05m/script.en.txt](variants/05m/script.en.txt) | 735 | `ef82cf137d755e4f81ebc7f03769cd958763ab63516635f7163beddd39c315ba` |
| [variants/05m/script.ru.txt](variants/05m/script.ru.txt) | 584 | `2a3e853aab75b9d5f16fc15588492b9e1f54c552b372f001a88117e03d9801f9` |
| [variants/10m/script.en.txt](variants/10m/script.en.txt) | 1628 | `b4506bea1f105d827adc1cf32a43a01aa34147efc38c5e68f67eee17dab72fe9` |
| [variants/10m/script.ru.txt](variants/10m/script.ru.txt) | 1315 | `8fd985f93c99366b3df8470da8147c9b8f489bf2d2d2a61be79cb8f94b1f164e` |

## 02m — STRONG_CANDIDATE
Map: four adults/same flight → pick A/B → one price level cannot fill cheap request → reset, two receipts → second-price change reverses outcome → compare before paying. 
| Criterion | Score | Basis |
|---|---:|---|
| Interest | 8 | Same flight, different total; $160 saving matters before checkout. |
| Opening | 8 | “Should I book all four at once, or split them into two bookings?” concrete choice. |
| Development | 8 | First price group fails capacity; reset and reveal two receipts; second purchase exposed to new price. |
| Payoff | 9 | $700 vs $860; then $890 vs $860 with conditional caveat. Action: compare prices and conditions. |
| Freshness | 7 | Well-known travel advice, not novel; two controlled scenarios focus on mechanism. |
| Visual | 8 | Two clearly distinct price-tag piles, exactly four final tickets, split receipts, no invented live website. |
| Speech | 8 | Ordinary first-person action; numbers are tied to payment; “one price level” still abstract. |
| Demand | UNVERIFIED | Indexed neighboring videos and real questions, no measured TWL response. |
Main weakness: arithmetic and conditions require time beyond normal 35–50s TWL slot; some listeners may disengage at “one price level per booking.” Literal ending “And it starts before I enter any payment details.” → opening “I'm buying four tickets for the same flight...” and RU equivalent: natural return to the purchase decision after payoff, but also could read as a fresh restart rather than seamless continuation. Author checked cold opening and two textual cycles EN/RU; AV and independent loop UNVERIFIED. Pair options considered: question-first / before-payment reminder (selected); result-first / explanation reminder (reveals winner early); quote-screen first / same quote screen (not enough verbal connection). No claim of perfect seam.
Checks: model facts PASS (arithmetic and conditional rule only); EN/RU sense PASS author; format UNVERIFIED (duration exceeds channel normal target; verify exact format locally); rights UNVERIFIED; loop UNVERIFIED; independent review UNVERIFIED.

## 05m — STRONG_CANDIDATE
Map: choice + why second payment → price tags not seats → A/B identical start → calculation of $80 per cheap seat → quote ladder → changed price and $295 threshold → real booking conditions. 
| Criterion | Score | Basis |
|---|---:|---|
| Interest | 8 | “what would have to happen to make it cost more?” introduces actual second question. |
| Opening | 8 | Four friends, one flight; two bookings vs one. |
| Development | 9 | Quote ladder gives actionable next step before second payment exposure. |
| Payoff | 9 | Break-even $295 each and a clear decision rule, not merely winning amount. |
| Freshness | 7 | Price bucket advice widely known; clear controlled reversal is useful. |
| Visual | 8 | Reset two boxes, four passenger quote ladder, price-change card and two receipts. |
| Speech | 8 | “I put both confirmations on the table” makes the calculation concrete; terms remain a little dense. |
| Demand | UNVERIFIED | Broad adjacent evidence only. |
Main weakness: quote ladder and arithmetic can slow the middle; likely loss point “The two methods are back to even...” if visual arithmetic is unclear. Long treatment does not have a production recipe. 
Checks: model facts PASS; EN/RU sense PASS author; format FAIL (Long unavailable); rights UNVERIFIED; loop N_A for proposed Long; independent review UNVERIFIED.

## 10m — REWORK (revised)
Map: four-adult task and identical inventory → A/B stable reveal → group size quotes and one-ticket exception → second fare rises → $295 boundary → two mild changes independently save $70 but together lose $20 → boundary shifts to $250 → one remaining ticket makes B incomplete → check actual conditions before payment.
| Criterion | Score | Basis |
|---|---:|---|
| Interest | 8 | Familiar four-friend decision; now a partial reservation introduces a concrete non-price stake. |
| Opening | 8 | “If a method only gets two of us on board, it has not completed the job” establishes a testable completion condition, though explanation before A still takes time. |
| Development | 8 | Combined price/benefit changes make a new outcome; missing last seat tests a qualitatively different failure. Group-size subsection still slows transition to the main counterexample. |
| Payoff | 8 | “B has failed the task” correctly distinguishes completion from cheap receipts; practical decision retains both fare and risk. |
| Freshness | 7 | Combined-cost and completion cases add nuance to familiar split-fare advice, not evidence of novelty across YouTube. |
| Visual | 8 | Two receipts + separate service charge; later two confirmed travelers and two unconfirmed, one remaining ticket; no live website fabricated. |
| Speech | 7 | Arithmetic is tied to actions, but the group-size examples and two break-even prices remain dense. |
| Demand | UNVERIFIED | No measured demand for this exact treatment. |
Confidence: moderate author judgment; high arithmetic conditional on inputs. Weak point: “What if my search for two shows the higher price” may feel like a detour after the first reveal; later two thresholds require sustained attention. EN estimate 10.5–13.0 min before separate pause allowance, RU 9.4–12.5 min; exact timing UNVERIFIED. Checks: model arithmetic and completion logic PASS author; EN/RU semantic alignment PASS author; Long format FAIL (canvas/fps missing); rights and independent reviewer UNVERIFIED; loop N_A for Long. No storyboard/timing or approval for this new hash.

## Compare
| Target | Added viewer value | Cost to attention | Recommendation |
|---|---|---|---|
| 02m | Stable price and reversal; clear actionable check | “one price level” abstract; textual seam still UNVERIFIED | **Preferred editorial candidate** |
| 05m | Quote ladder and $295 threshold | Arithmetic near “The two methods are back to even” | Useful deeper option |
| 10m | Joint cost reversal, $250 threshold, explicit incomplete-group failure | Group-size sensitivity and repeated thresholds; more difficult to absorb aloud | Revised but REWORK for pace |

Six complete editorial texts; no approved master or independent receipt. The exact 02m/05m files, author findings and packaging are preserved. The 10m old timing/score is historical, not evidence for new hash. Selected 02m still needs independent review, duration and format compatibility, textual/AV seam and actual visual rights before production.

## Revision progress — 2026-11-24
Baseline commit `d57a85eca7a344021081c1bfef14d4d381b4aaa4`, old 10m EN SHA-256 `a57d88e7e45049a070578ff6676beca7fbeb0c768452d685d492c09c237ed8b8`, RU `fe13a2662716a6e49ed869351e45ff04fb4c9608c7ffc1dfd19ac97ce3b4e809`; exact paths unchanged. Prior package already had six texts; all six read → 10m substantively revised → all six author-checked at baseline/new hashes → 02m remains recommended, not approved. New scenario assertions tested against model, not observations. 10m visual intent: generic checkout, same original inventory reset; add separate service receipt only in combined test; show one unsold ticket and exactly two confirmed travelers in incomplete test. No approved storyboard exists; no spans/timings transferred. Runtime/independent review UNVERIFIED; next: independent review and compatible format for the selected script; remaining open PR backlog is not completed.
