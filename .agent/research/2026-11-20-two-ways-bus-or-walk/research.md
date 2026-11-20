# Research — Wait or Walk? Two Ways Lab

Access observed: **2026-11-20**. Channel: `two_ways_lab`, English narration with full Russian editorial equivalents. **EDITORIAL MODEL, not a real field experiment.**

## Selection and why someone might watch

Audience: English-speaking everyday commuters; no familiarity with a named city or transit jargon needed. Main question: **Can a faster bus get me to the same door later than walking?** Concrete action: I reach an illustrated bus stop, choose A (wait, then ride) or B (start walking), both clocks start simultaneously and end at the same destination. The wait changes from 5 to 15 minutes; the apparent winner reverses. The added reveal for 05m is that people prefer different actions even at an equal-time finish. The 10m investigates *unknown* arrivals, not just a known countdown.

Twelve genuinely distinct directions screened, not twelve rewordings of this prompt:

| # | Different everyday problem | Fast decision and factual/queue check |
|---|---|---|
| 1 | Wait at a bus stop vs walk directly to the destination | **FINALIST / SELECTED**: personal choice, clear reversal, published stated-preference survey, real YouTube comparisons |
| 2 | Air-dry damp laundry vs use an electric tumble dryer | **FINALIST / STRONGEST ALTERNATIVE**: clear need for ready clothes, energy/time tradeoff; actual dryer type, conditions, fabric and total drying time missing, so no universal single-metric winner |
| 3 | Bike vs walk for a short trip including bike retrieval/locking | **FINALIST**: same door and travel time, potentially vivid 2-stage crossover; no measured overhead for the hypothetical rider and audience video matches weaker than for #1 |
| 4 | Charge a phone to 80% twice vs 100% once | Battery cycle-health specs and comparable device use hard to establish; 'twice vs once' does not ensure same energy/service |
| 5 | Cold wash vs warm wash for one stained item | Physical cleaning outcome depends on actual stain, detergent, material; no observed test |
| 6 | Cook four portions in batches vs finish each separately | Needs appliance/workload model; only a schedule does not establish taste, safety or quality |
| 7 | A bus route with a transfer vs later direct route | Existing #285 directly covers this strong angle; protected duplicate |
| 8 | Nearby gas station vs cheaper station farther away | Existing #307 directly covers the equal-end-state detour |
| 9 | Elevator vs stairs to the fourth floor | Existing #175, another valid model already claimed |
| 10 | Shower vs bath by total water used | Existing #275 covers conditional water threshold |
| 11 | One shared checkout queue vs independent lines | Existing #136; E001 already uses queues |
| 12 | Weighing a bag with one missing object vs checking individually | Existing #262 and #207 cover substantially similar puzzle |

The three finalists are not fake weak competitors. Laundry has a stronger tactile image and instantly relatable urgency; biking has stronger movement and greater practical flexibility. The winner **#1** is better supported by (1) a published survey asking the exact choice, (2) distinct documented outcomes in real bus-vs-pedestrian video reporting, and (3) one measurable variable with a genuine change of winner. **Counterargument:** its arithmetic is elementary, the 10m variant risks becoming a classroom explanation, and the comparable YouTube videos are older or news reports, not a recent controlled illustrated A/B trend. This remains a *demand hypothesis*, not verified channel demand.

## Exact reproducible model — two methods, one starting state

- Physical setup: a fictitious stop **S** and a single destination door **D**. One initial instant `t=0`. Two independently reset copies of the same state; no physical experiment took place.
- **A:** wait `W` minutes for the next bus at S, then ride `R=10` minutes to D. **B:** walk directly from S to D in `P=20` minutes.
- Objective announced before reveal: elapsed minutes at D. Both alternatives use the *same departure instant* and the *same end door*. Fare, comfort, weather, intermediate stops, boarding, walking after alighting, varying bus speed, and delays other than `W` are excluded from the deterministic base scenario. They are limits, **not evidence of a winner**.
- `A(W) = W + 10`; `B = 20`; `A-B = W-10`. Thus:
  - `W=5`: A=15, B=20, A wins by 5
  - `W=15`: A=25, B=20, B wins by 5
  - `W=10`: tie at 20
  - `W=9`: A=19, 1 minute faster
  - `W=11`: A=21, 1 minute slower
  - If actual ride is `R=12`, crossover becomes `W=8`.
- 10m additional **separate, clearly labeled hypothetical uncertainty model**, same physical start/finish and **the same two methods**: bus arrival `W ~ Uniform(0,H)`, chosen without claimed real observations; `E[A]=H/2+10`, `B=20`. At H=10, A average15; H=20, equal20; H=30, A average25. For H=20 A has range10..30 while B=20 fixed. Means do not establish a risk preference. Waiting a little then walking / catching at another stop are *outside* the defined A/B methods; 10m explicitly does not announce a third winner.
- Model arithmetic is an exact mathematical calculation under assumptions, **not observation of a city**. Real route times, waiting distributions and traffic can reverse a choice.

## Primary evidence and claim ledger

| Evidence (opened/read on 2026-11-20) | Supports exactly | Boundaries |
|---|---|---|
| Kathrin Viergutz, *Walking, Waiting, Interchanging: A Scenario-Based Analysis of User Requirements in Local Public Transport*, International Transportation (2018), [publisher text](https://elibrary.narr.digital/xibrary/10.24053-IV-2018-0106), [DLR hosted paper](https://elib.dlr.de/124333/1/Viergutz_Walking_Waiting_Interchange_International_Transportation_1-2018.pdf) | Figure 1, pp. 42–43: **n=391 online questionnaire** with walk20 / ride10 and waits5,10,15. Prefer bus 78.01% at 5 wait; prefer walk 62.92% at 10 wait; prefer walk 85.93% at 15 wait. | Stated preference, *not measured racing times, not representative population demand*. Grey category present; percentages for two main choices don't sum to 100. PDF visual screenshot endpoint failed cache; accessible full text/parsed figure cross-read, no claim of successful PDF screenshot. |
| Anthony B. Morton, [*A Note on Walking Versus Waiting*](https://arxiv.org/abs/0802.3653) (2008-02-25) | Research distinguishes knowing exact arrival, probability distributions of arrival and intermediate stops; simplified optimal decision can change with arrival assumptions. | Research mathematics has assumptions; **our** numerical values and `Uniform(0,H)` are illustrative independent calculations, not a quote of findings from this paper. |
| [ENERGY STAR — Clothes Dryers](https://www.energystar.gov/products/clothes_dryers), [Australian Government energy rating guidance](https://www.energyrating.gov.au/consumer-information/products/clothes-dryers) | Laundry finalist: dryer energy usage differs by type/load; line drying saves appliance energy, but readiness depends on environment. | Not evidence that a specific garment dries in a fixed number of minutes. |
| [Urban Mobility Mode Shift to Active Transport (SAGE)](https://journals.sagepub.com/doi/abs/10.1177/21582440241228644) | Bike/walk finalist: study uses different empirical model assumptions for travel speeds (1.2 vs 2.3 m/s) and short trip classification. | Not actual bike retrieval/lock overhead or outcome for this model. |
| [Viewing NYC 2019 report](https://viewing.nyc/watch-these-frustrated-pedestrians-race-a-crosstown-manhattan-bus-on-foot/) and [2025 Streetsblog challenge report](https://nyc.streetsblog.org/2025/08/08/team-pedestrian-trounces-team-bus-in-annual-crosstown-bus-challenge) | Real public races can be close, or pedestrians can win on a slow crosstown corridor. One 2019 report says bus ahead by **five seconds**; 2025 report says pedestrians ahead **eight minutes** in one local challenge. | These are **different races, roads, conditions**. No inference about average bus performance or this model's 5/15-minute conditional wait. |

Narration includes only conditional calculations and carefully labeled **survey preference** (05m/10m); no claim that the modeled journey actually happened.

## YouTube evidence and negative signals

Indexed public cards/reports checked on **2026-11-20**. View counts are **cached/indexed values, not live current counters**; no video watched, no transcript or comment thread fetched. Duration was not provided for the cards: `UNVERIFIED`. Language: English for the named videos. Each is real, but not a controlled matched sample.

| Link / video ID | Creator; published date; known format | Indexed public views | Relevance, comparison limit |
|---|---|---:|---|
| [Frustrated Manhattan Pedestrians Race The Crosstown M14 Bus](https://www.youtube.com/watch?v=mVXMSJxNGec) / `mVXMSJxNGec` | Gothamist, **2019-02-20**, actual walking-vs-bus challenge/news short-form length unknown | ~12,002 | Direct choice and suspense; single busy NYC corridor rather than timed wait before the ride |
| [Pedestrians walk faster than NYC crosstown bus](https://www.youtube.com/watch?v=YDdqWCaqjFU) / `YDdqWCaqjFU` | FOX 5 New York, **2025-08-08**, news item, exact length unknown | ~9,228 | Independent author, same type of real-world juxtaposition; local advocacy event, not general audience model |
| [WALKING An Entire NYC Bus Route (Bx 32)](https://www.youtube.com/watch?v=MjlqLfatCpc) / `MjlqLfatCpc` | The Neon Shift, **2019-07-20**, POV/hyperlapse, exact length unknown | ~414 | Walked full route in advance of possible bus race; title does not prove a completed A/B comparison |
| [Watch As One Man Attempts To Clean This Subway Station](https://www.youtube.com/watch?v=GxOgSA2YUdU) / `GxOgSA2YUdU` | Gothamist, **2019-03-08**, roughly same era / NYC public-space short film, length unknown | ~101,402 | **Same-author rough baseline ONLY**, different subject/genre; it outperforms bus race but not a clean controlled topic comparison |

FOX 5 similar-format same-age baseline was **not established**. Recent matching YouTube results (last 30–90 days) **not established**; FOX 5 2025 is evergreen/older news, Gothamist 2019 much older. A 2026 NYC bus-lane community post exists, but is **not** a tested direct wait-vs-walk video. Comparison cannot establish demand, current velocity, CTR, thumbnail conversion or retention. Comments/transcripts not read. **YouTube demand: UNVERIFIED**, neither zero nor an invented 8/10. User/channel analytics not consulted; no authorized measured channel uplift inferred. Connected vidIQ balance on 2026-11-20: **0 credits**, no paid queries or purchases.

## Story promise and real counterpoints

- Opening 02m exact: “Should I wait for this bus, or walk the rest of the way?” Visual intent: one stop, one destination, A/B decision before any clock outcome.
- Opening 05m exact: “I'm at a bus stop with one ordinary problem.” Then same two methods and target door; choose A/B before reveal.
- Opening 10m: bus physically faster, yet bus absent. Models marked models, not “we raced.”
- Beats 02m: fixed start → choose → 5+10=15 vs20 → reset one input → 15+10=25 vs20 → break-even10 → completed rule → loop back to same choice.
- Beats 05m: above → at 9/10/11 minutes threshold → questionnaire choice mismatch at exact time tie → countdown uncertainty / change ride time → conclusion and real-life limits.
- Beats 10m: above → controlled vs uncertain arrival → conditional mean vs fixed walking route → risk of late arrival → excluded hybrid and intermediate-stop alternatives → whole-trip fairness → bounded public racing illustrations → conditional conclusion.
- **Strongest objection:** consumer-friendly short calculation does not automatically justify ten minutes. 10m has self-contained new analysis but weaker pace; do not treat length as merit. Exact editorial scores in `story-review.md`.

No third invented street experiment. No copyrighted transcript/phrases reused. Media footage and its permissions **not** retrieved; only original narration and hypothetical illustrations proposed.
