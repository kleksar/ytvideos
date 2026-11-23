# Story review — three exact editorial scripts

**EDITORIAL_CANDIDATE_UNREGISTERED.** Author assessment only. No independent `ytv-script-review-v1` reading input/result, no runtime script gate, owner approval, media or measured voice timing. Dates: 2026-11-23. Reference editorial: current merged main (PR #124 merged), not unmerged proposed revision.

## Exact scripts and byte identities
| Variant | EN script Git blob | EN SHA-256 (exact UTF-8 + trailing LF) | EN words | RU Git blob | RU SHA-256 | RU words | Proposed format |
|---|---|---|---:|---|---|---:|---|
| 02m | `40c6343b23d40c3a11787ad4cfe311a85a8315b3` | `9c9199fdd669a3be407596f4206ac37c4282653287f108c8dbd2fd2e4e5657ee` | 292 | `9d7fa0c65e2e7fcc0593466f30125bf02ed1911e` | `a58f8b23de419a5af078b238a137618edd8abbd9cccd3c455eb72d532ce5b1fe` | 264 | Short editorial proposal; ~35–50s preferred channel target exceeded |
| 05m | `bf5da0f51a4254f0de8fe777a13ac21073bc941e` | `319a42061f65b2b2ba045cccd2ce6adeb97792ef8e33f247ef02b96ad2e7bf17` | 821 | `89f19adc890a4d5662fb0595dc6af389d263cb59` | `12cae654ec1b5aef6377ed2d7bba6fd02895c4dceb7a55b99b3c4dd3db4a991d` | 670 | Long editorial proposal, Long ChannelSpec unresolved |
| 10m | `f4e78e8e8a7f145c14a03e5462ac354d0dbc1d9e` | `1d6bed0ca4edbb9f6517e84baca4e23b4f22c112b2fbe92a30a0ba168d5fadb5` | 1523 | `ceee8fdef0cfdbf1e8c41f6627235f176d3c3f66` | `b4f574203739ccde6584fbad0ef0410d7688730e2efda8720d5d8f524a270f76` | 1219 | Long editorial proposal, Long ChannelSpec unresolved |

Speech duration **estimate only**, not measured: 02m 292w / 140–165wpm ~1:46–2:05 before pauses; allow ~1:55–2:15. 05m 821w ~4:59–5:52 before pauses; allow ~5:05–6:05. 10m 1523w ~9:14–10:53 before pauses; allow ~9:30–11:15. Pauses/illustrated result may extend. Actual production voice may differ. **Do not alter voice speed** to meet the name of a variant.

## Script-specific maps and classifications

### 02m — STRONG_CANDIDATE; **recommended**
- Opening: “I can fold these eight T-shirts faster than I can roll them. So why would I roll them for a trip?”
- Setup: one case, eight shirts, A folded stack vs B visible rolls; vote before answer; disclose assumed timed model.
- Development: 40 vs 72 seconds packing → three expected retrievals 23,20,17 vs 2,2,2 → 100 vs 78 total.
- Payoff: “The slower packing method wins by twenty-two seconds.” Then one-request reversal 63 vs 74 and conditional practical choice.
- Literal EN seam: “And that sounds backward, because” → “I can fold these eight T-shirts faster than I can roll them.” This is a causal spoken completion not a repeated noun. RU seam: “И это звучит странно, потому что” → “Я могу сложить эти восемь футболок быстрее, чем свернуть их в рулоны.” Both author-read twice; **independent reader UNVERIFIED**, actual audio/visual seam UNVERIFIED.
- Defect: 292 English words near upper edge of 2m and much longer than channel's nominal 35–50s Short; model visualization and real listening not validated.
- Author, confidence: ChatGPT, moderate for mechanics/scene logic, low for attention and acoustic seam.

### 05m — STRONG_CANDIDATE (editorial only)
- Opening: “Would I save time by rolling my clothes, or is folding still faster when I actually use the suitcase?”
- Setup/advance: disclose unknown future shirt selection and equal access rules; define why preplanned outfits differ.
- Development: full cumulative expected-search explanation; 1/2/3 accesses; exact second-access crossover; distinguish expectation from actual realized outcome; suggest stopwatch validation.
- Payoff: no one method is always best; look at frequency of retrieval, not packing appearance.
- Long ending has no required spoken loop; Long format **production BLOCKED**.
- Defect: extra exposition at midsection may exceed intended 5m and require major scene variation. Main math repeats the shorter version, albeit with causal depth.
- Author, confidence: ChatGPT, moderate for maths and translation, lower for interest/performance.

### 10m — REWORK (complete text, not a production recommendation)
- Opening asks whether packing and later retrieval are same task.
- Development: first-order model; expectation vs one actual draw; two requests threshold; speed sensitivity `A=46+18t`; n=4/3 crossover; test protocol.
- Payoff: a method wins *for a fixed task*, not as a universal travel hack.
- Long ending has no required loop; Long production BLOCKED.
- Main defect: long arithmetical sensitivity analysis and repeated cautions may exhaust general audience before payoff; would require actual measurements or a different angle to merit 10 min. **Not** padded with invented historical action.
- Author, confidence: ChatGPT, high for arithmetic, modest for voice, low for viewer attention.

## Eight editorial criteria — independent per exact English+Russian version
Author scores 1–10 are qualitative **not retention/CTR**; unknown audience demand = UNVERIFIED, never fabricated 8.

| Criterion and cited evidence | 02m | 05m | 10m |
|---|---|---|---|
| 1. Interest / significance: unexpected slower-packing winner vs familiar suitcase choice | **8**: change after three mornings | **8**: explains when to choose | **7**: threshold could feel niche |
| 2. Opening: first listener needs an immediate dilemma | **8**: “why would I roll them” | **8**: question before explanation | **7**: two related abstract questions |
| 3. Development / reason to stay: new consequences not same fact repeated | **8**: prep lead → three searches → reversal | **8**: 1/2/3 request threshold adds understanding | **7**: sensitivity tables slow causal action |
| 4. Payoff: full answer before end | **9**: 100/78, then opposite 63/74 | **8**: visible second retrieval crossover | **8**: precise threshold but no new emotional beat |
| 5. Angle freshness: packing footage generally old, repeated access model new hypothesis | **8**: repeated access vs packing only | **8**: switch at second reach | **7**: much of expansion is formulas |
| 6. Visual expressiveness: A stack, B rolls, item removal, no fake physical result | **8**: clear dual-color object state | **8**: cumulative progress and two rounds | **7**: too many static numeric overlays |
| 7. Natural/clear voice: first-person, spoken complete sentences, same EN/RU facts | **8**: everyday "On a one-night stay, I fold" | **8**: concrete stack-to-suitcase reasoning | **7**: wordy quantitative passages |
| 8. Verified viewer demand: no controlled same-author baseline or actual comments / own metrics | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** |

Scores are authored assessment with confidence **medium** except viewer interest confidence **low**. No independent reviewer is credited. Classification only if interest/development/payoff >=8: 02m/05m meet this editorial threshold; 10m fails interest/development. Biggest shared drawback: the scenario is a mathematical toy with unmeasured motion timings, and packing-vs-rolling is an old crowded theme.

## QA and limitations per variant
| Test | 02m | 05m | 10m |
|---|---|---|---|
| Model arithmetic / internal rules | PASS authored verification (see research) | PASS authored verification | PASS authored verification |
| First person and parallel EN/RU meaning | PASS author comparison | PASS author comparison | PASS author comparison |
| Rights of future visual materials | UNVERIFIED; no actual assets | UNVERIFIED | UNVERIFIED |
| Exact script source identity | Git blob+SHA-256 recorded | Git blob+SHA-256 recorded | Git blob+SHA-256 recorded |
| Supported production format | Short known, nominal duration mismatch requires decision | Long recipe BLOCKED | Long recipe BLOCKED |
| Short verbal loop | Author check PASS; independent UNVERIFIED | N_A Long | N_A Long |
| Actual AV seam and acoustic timings | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Independent first listener/result schema | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Script approval / registered run | NOT DONE | NOT DONE | NOT DONE |

## Incremental comparison and decision
- **2 → 5:** add equally likely target-position proof, explain actual versus expected outcomes, second-request crossover and advance-outfit caveat. Useful but pacing slower and no applicable channel Long recipe.
- **5 → 10:** add operating-time sensitivity `t=32/18`, fewer-shirts scenarios and physical test protocol. Valuable only to analytical niche; ordinary audience may not want eight more calculations.
- **Recommend 2m** for strong simple A/B surprise + full useful reversal, without claiming it meets final format gate. If channel's usual 35–50s Short is strict, the 2m variant is **not** silently compressed and a separate owner-authorized production choice is needed.

Two authored editorial passes at most; the only substantive second pass was removal of external research-meta language from 10m EN/RU. No independent reading took place. A future rewrite to improve 10m would invalidate this exact verdict/hash and need fresh review.

## Production restriction
No `ytv start`, pinned reference packet, actual independent review, source approval, media bytes, provider usage, MP4 or release recorded here. Convert the chosen exact EN script into local runtime using real CLI when available, inspect pinned plan, obtain independent review of its literal text, and seek owner approval. Do not mark an official script gate PASS.
