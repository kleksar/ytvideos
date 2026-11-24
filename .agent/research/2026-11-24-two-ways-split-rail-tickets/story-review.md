# Author review — revised 10m, exact 02m/05m retained

Author: current writing assistant (not independent reviewer). Confidence high on stated model and arithmetic, medium on text and EN/RU equivalence, low on audience and measured duration. No reviewer session available in direct/deferred tools. No official script gate. Fresh independent reviewer must receive only exact text first, sources after first reading, and preserve actual result. This is one author review, not viewer testing.

| File | Words (whitespace) | SHA-256 |
|---|---:|---|
| [variants/02m/script.en.txt](variants/02m/script.en.txt) | 284 | `ec17729d5cb0cf19825625dd40d5bd6dfe4d3868e7beabc14d7a813defbe3549` |
| [variants/02m/script.ru.txt](variants/02m/script.ru.txt) | 234 | `6f5bd2f37cbd339a8d4329e3d567d16e0eb4332eae1b70a637d49deefc1fbf34` |
| [variants/05m/script.en.txt](variants/05m/script.en.txt) | 680 | `ce99e64e1e21a0633cc8b5ea997e0aa7b05e17057098a71ce9733a906ceeb50d` |
| [variants/05m/script.ru.txt](variants/05m/script.ru.txt) | 590 | `20fe6eab98e688b7acca82cc198f9a94d315f6a57a76e1fca401e50c0ba9ff1f` |
| [variants/10m/script.en.txt](variants/10m/script.en.txt) | 1492 | `001274fd9ed534dc7d960ac46a6cb51fbcc00a7231c806b76f5da74f02da4ac0` |
| [variants/10m/script.ru.txt](variants/10m/script.ru.txt) | 1316 | `2c6a0efae234495487a19592c258adc6167e65288d2f798fa6fce2eecf9b4040` |

Timing assumption EN 125–145 written words/min, RU 110–140; most numeric values written as speech. Actual TTS not performed. 02m outside routine 35–50s target; 05m/10m Long canvas/fps/end screen undefined. Estimates and format acceptance remain UNVERIFIED, no voice speed changes.

| Criterion | 02m | 05m | 10m |
|---|---|---|---|
| Interest / significance | 8: same ride, £80 vs £55; practical question | 8: price plus express eligibility | 8: avoid paying for invalid or needlessly expensive combinations |
| Opening | 9: first line one train, £80 vs two | 8: three concrete questions after £80 fare | 8: £80 and shorter fares, two extra questions; setup slower |
| Development | 8: cheap pair → skipped stop → different valid pair → changed quote | 8: why fare differences exist, express fallback, fee boundary | 8: compare three splits, express validity, checkout rank reversal and fare eligibility; dense |
| Payoff | 9: £25 and £15 savings, A wins at £49 | 9: £25, £15, £6 reversal, fee threshold | 9: cheapest £53 triple costs £62 at checkout, £61 pair wins; final £65 fallback after repricing |
| Freshness | 7: familiar British split-ticket tip, clear express caveat | 8: fee boundary and actual stop rule | 8: fee basis changes optimal split; displayed cheaper fare may be invalid |
| Visual expression | 9: identical train and two ticket groups, one stop disappears | 8: same map and totals; fee break-even | 8: distinct per-ticket versus per-order fee rows and crossed restricted fare; same map still repeats |
| Naturalness / clarity | 8: “I don't need to get off just because one ticket ends there”; one dense price line | 8: “I didn't have to abandon the idea of splitting”; fee arithmetic | 7: later repeated resets around £49 and £56 still demand concentration |
| Audience evidence | UNVERIFIED: no matched baseline | UNVERIFIED | UNVERIFIED |
| Classification | STRONG_CANDIDATE | STRONG_CANDIDATE | REWORK |

Individual text maps and weakest passage:
- 02m: immediate same-ride choice → model and score → A80 → B55 → no exit, seat caveat → express eliminates invalid pair, B65 → A49 beats B55 → practical conclusion and seam. First frame establishes exact question. “The two valid tickets cost forty-six and nineteen pounds” is the densest price line; keep it paired with visual totals. All questions resolved before closing. Interest, development and payoff each ≥8 by author judgement.
- 05m: £80 prompt and validity question → model and choose → both prices → mechanism, stop/seat conditions → express fallback → £49 reversal → fee sensitivity → actionable conclusion. Added value versus 02m is the explanation of why price sums differ and the exact £25 fee crossover, not repeated opening. Main weakness: “At twenty-five pounds extra, both methods cost eighty” after earlier fare reversals may feel like a second ending. Strong candidate, but 2m delivers core quicker.
- 10m revised: price screen → all four combinations → cheap pair → stop and seat restrictions → express eliminates two splits → cheaper middle leg makes triple cheapest → checkout reverses rank → fee basis reverses it again → cheaper through offer wins only if valid → changed first-leg price changes best split → practical decision. Payoff: “The fare that looked cheapest a moment ago is now a pound more expensive than the pair.” Weakest point: “I reset again, with no fees and all original products valid.” The listener must retain several conditions. REWORK for pace. 

Baseline 7462b52ffd4f2588812dc250f7df1cad1789ff56; initial EN 4a6ba69f66a31185eec183e80f69ff892a6febacb6d9cb7d6bd64a89f4a769da, RU 27a95e53e86ecd434273e04a0062ffa64feb6ff34b96b6c0fe72aec1a8c0b806. Preserve 02m/05m byte-identically because the short resolves the central question, the five-minute text adds the fare mechanism and flat-fee boundary. 10m replaces the repeated flat fee exercise with a genuine new comparison, not additional length for its own sake. Prior 10m timings and author assessment superseded; no independent review transferred.

02m loop author textual read of both complete cycles EN/RU (no audio). Tested simple object repeat vs direct final question, chose question with answered core outcome. EN last “Before I change trains just to save money, what choice do I have at the ticket screen?” → first “I can take the same train with one ticket for eighty pounds, or with two tickets that might cost less.” RU last “Прежде чем менять поезд ради экономии, какой выбор у меня есть при покупке?” → first “Я могу проехать на одном и том же поезде с билетом за восемьдесят фунтов или с двумя билетами, которые могут стоить дешевле.” Direct answer before next A/B comparison. Cold first line understandable; final already gives method and all results. No fake cliffhanger; text seam author PASS, independent and actual AV seam UNVERIFIED. Long loops N_A. No invented native next video or promotional tail.

| Check | 02m | 05m | 10m |
|---|---|---|---|
| Model calculation and ordinary-ticket rule | PASS author | PASS author | PASS author |
| EN/RU equivalence | PASS author | PASS author | PASS author |
| Format | UNVERIFIED: length outside routine profile | FAIL production: no Long definition | FAIL production: no Long definition |
| Rights | UNVERIFIED: future media/brand inputs; original scripts, no clips | same | same |
| Loop | PASS author text; independent & AV UNVERIFIED | N_A | N_A |
| Independent review | UNVERIFIED | UNVERIFIED | UNVERIFIED |

Recommendation 02m. One immediately visible decision, valid stop constraint and reversal fit the core promise. 05m adds meaningful price explanation and fee sensitivity, but extra arithmetic diminishes pace. 10m adds checkout fee basis, ranking reversal and ticket eligibility; multiple resets and arithmetic density still weaken pace. Do not manufacture a 10m production route. Scores are editorial judgements, not probabilities, retention or CTR. No production approval.


### Revised 10m textual spans (EN/RU paragraph order, no timed storyboard)

- 1: I want to catch a train from West to Harbour — route/choice.
- 2: Could I buy those shorter trips and ride all the way to Harbour for less — route/choice.
- 3: I'm going to build a small model of a British railway and make two ways of buying the same journey c — route/choice.
- 4: Here's the route — route/choice.
- 5: Which would you choose — route/choice.
- 6: I'll buy nothing until I've compared the available prices — fare cards and totals.
- 7: Now I check B — fare cards and totals.
- 8: But I have another possible split — fare cards and totals.
- 9: What about dividing the journey into three pieces — fare cards and totals.
- 10: I've now covered every way to divide this simple route at its two intermediate stops — fare cards and totals.
- 11: I can show all four results together and choose the cheapest valid option — fare cards and totals.
- 12: Why might the prices behave like this — stop eligibility.
- 13: There's also a practical rule that keeps the comparison honest — stop eligibility.
- 14: When the train stops at Junction, I don't have to get off and board again simply because the first t — stop eligibility.
- 15: Now I change exactly one feature of my itinerary — stop eligibility.
- 16: Look at my three split choices again — stop eligibility.
- 17: Imagine that I only searched for the cheapest split on the slower service and copied it onto my expr — basket and separate fee rows.
- 18: Back on my stopping train, I find a different offer — basket and separate fee rows.
- 19: I put that combination in the basket — basket and separate fee rows.
- 20: The fare that looked cheapest a moment ago is now a pound more expensive than the pair — basket and separate fee rows.
- 21: The three tickets saved two pounds in fares, but the third ticket added three pounds at checkout — basket and separate fee rows.
- 22: Suppose the seller instead charges five pounds once for an entire order, regardless of the number of — restricted fare / updated comparison.
- 23: What happens when the fares themselves move — restricted fare / updated comparison.
- 24: I reset again, with no fees and all original products valid — restricted fare / updated comparison.
- 25: That would be a mistake — restricted fare / updated comparison.
- 26: There's one last boundary to my comparison — decision and payoff.
- 27: When I reach Harbour in this model, I haven't bought a different journey — decision and payoff.
- 28: I can take this method to a real booking screen, but not these invented fares — decision and payoff.

Estimated EN 1492 words / 125–145 wpm = 10.29–11.94 min; RU 1316 / 110–140 wpm = 9.40–11.96 min. No pauses or end screen; measured duration UNVERIFIED. Author model arithmetic 28 equalities PASS; revised text pair compared for amounts, eligibility and payoff; independent review UNVERIFIED, Long loop N_A and Long production FAIL. No detailed storyboard, no approval. 02m remains recommended editorial candidate.
