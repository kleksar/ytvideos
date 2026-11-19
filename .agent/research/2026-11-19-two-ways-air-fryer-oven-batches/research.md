# Two Ways Lab · One basket wins, until dinner needs more baskets

Observed/researched **2026-11-19** (English audience; free public search only). This is **not a filmed experiment**. One real small-load benchmark comes from independent consumer tests. All larger-load oven and repeated-air-fryer figures below are **explicit model hypotheses**, not measurements. No TTS, images, comments API or physical measurements were used.

## Rotation, duplication and selection coverage

Remote `main` at intake: `d7dbf4d8de0a0719e062e72b7e21b7d3748de100`. The last actually created story PRs in GitHub are #283 Nuviko, #282 Paper, #279 Two Ways, #278 Nuviko, #276 Paper, #275 Two Ways. Next in the narrative sequence is **Two Ways Lab**. PR #124 is merged; rules taken from current `main`. Before writing, searched PR/Issue titles for `air fryer`, `fryer`, `oven`: no match; a second check immediately before branch creation returned no duplicate. This does not rule out all unnamed private published videos; their status is UNVERIFIED.

12 distinct possible episodes screened rather than three titles for one idea:

| Candidate | Actual coverage and selection consequence |
|---|---|
| **One air-fryer basket or one oven for a family meal** | Selected: recognizable meal; strong independent measured two-portion starting point; time winner flips with capacity while modeled energy winner can differ; new Oct-2026 consumer evidence |
| **Roll or fold travel clothing into a carry-on** | Finalist, strongest alternative: extremely visual, low intellectual burden, directly testable with measured bag volume; risk: wrinkling/fabric/rolling pressure require physical evidence, not guessed capacities |
| **Pair 40 unmatched socks directly or sort into colour piles first** | Finalist: easy A/B with counting; risk: unless exact sock order and per-action costs are specified, arbitrary inputs predetermine winner |
| Run versus walk in rain | Already story PR #179: same core tailwind model; duplicate, excluded |
| Stairs versus elevator | Already #175: 39-second wait crossover; duplicate |
| One shared checkout line versus multiple | Already #136 and checkout pilot; duplicate |
| One 18-inch versus two 12-inch pizzas | Already #279; duplicate |
| Park at first free space versus closer to entrance | Already #127; duplicate |
| Store route by aisle versus nearest item | Already #237; duplicate |
| Washing by hand versus dishwasher | Already #168; duplicate |
| A single timed heater session versus constant heating | Already #195; duplicate |
| Kettle versus microwave to heat one mug | Already #171; duplicate |

**Why winner versus strongest alternative:** rolling/folding is more immediately visual, and would be a strong topic after a controlled bag-and-clothes measurement. Air fryer/oven has a better **available evidence base today** and a clearer beyond-the-hook causal change: 2 → 6 → 8 portions, serving completion versus electricity. Losing alternative not an owner-rejected topic. **Best objection against winner:** public “air fryer saves energy” comparisons are saturated; a model with hypothetical large-load oven behavior must not be sold as a measured reversal. If a first listener finds the model too abstract, reject the current story rather than raise scores.

## Three finalist hooks / development / payoff

| Finalist | Exact opening idea and first action | What materially develops after hook | Full payoff / strongest objection |
|---|---|---|---|
| **A/B air fryer/oven** | “I have six people waiting for fries. Do I use my little air fryer, or the big electric oven?” Show six identical portions and a two-portion basket | Independent 2-portion test → repeated small basket causes backlog → assumed single large oven cook → different time/energy winner → eight-portion crossover | In *this stated model*, six servings: oven 40 vs fryer 69 minutes, while fryer .861 vs oven .92 kWh; eight servings oven wins both. **Objection:** big-load measurements are assumptions and external demand is not validated |
| **Roll/fold luggage** | “I've got one carry-on and the same pile of clothes. Which way actually fits them?” Show identical clothing/count and suitcase | Compress, stack, unused gaps, folds and accessibility | Winner only after measured bag geometry and clothing thickness. **Objection:** existing search hits are packing tutorials and tests differ by items; no controlled measurement available for honest production |
| **Sock pairing** | “Forty socks on the floor. Can I get twenty pairs faster without sorting?” Show identical sequence on two tracks | Immediate pairing versus first colour buckets; count touches/searches | Need precommitted sequence and cost rule to count a true winner. **Objection:** existing YouTube results emphasize folding or storage, not matching labour; viewer demand UNKNOWN |

## Selected A/B: fixed rules and calculation ledger

**Declared primary metric BEFORE result:** elapsed minutes until **every portion** of the same frozen chips is ready. Secondary, explicitly distinct: electricity used to complete all portions. Cold start, one person, one appliance at a time; no assistance or simultaneous A+B. Nominal portion 160 g. The same total food and target doneness must be used **inside each A/B comparison**. Changed quantity (2/4/6/8 portions) is a new explicitly declared test condition, not a hidden advantage. Food quality/doneness for modelled big loads is not validated.

**Direct independent measured benchmark ONLY for 320g, two portions (Which?, 2026-10-23):** fryer 23 min, **0.287 kWh**; built-in electric oven 33 min, **0.863 kWh**. Source says the tested fryer maker recommended max **500g chips**, so each modeled 320g fryer basket is within that stated cap. Measured cooking quality was uneven for both. These are observations for *specific appliances/food* and do not establish any larger load performance.

**Hypotheses selected openly for the screenplay model:**
- A: each 320g air-fryer round repeats **23 min and 0.287 kWh**, and rounds run **sequentially**. No extra interruption minutes included. This extrapolation may overstate energy for later hot-start batches.
- B: electric oven can cook all food in **one adequately spaced session**. For 640g assume **37 min / 0.89 kWh**; for 960g **40 min / 0.92 kWh**; for 1280g **43 min / 0.98 kWh**. None of these *larger* B figures was measured in the cited test. These are scenario inputs, not empirical extrapolations; if tray capacity/doneness fails, the proposed run is not valid.
- 320g B's measured **33 min / 0.863 kWh** is kept as the genuine benchmark, not replaced with a scenario assumption.
- Price illustration uses 26.32 UK pence per kWh from Which?'s Oct-2026 article; no personal electricity rate is assumed.

| Servings | Mass | A fryer: 320g rounds | A minutes | A kWh | B oven minutes | B kWh | Time winner | Energy winner | Input type |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| 2 | 320g | 1 | **23** | **0.287** | **33** | **0.863** | A by 10m | A | Both measured in specific test |
| 4 | 640g | 2 | **46** | **0.574** | 37 | 0.89 | B by 9m | A | Extrapolation/assumed oven |
| 6 | 960g | 3 | **69** | **0.861** | 40 | 0.92 | B by 29m | A by 0.059kWh | Extrapolation/assumed oven |
| 8 | 1280g | 4 | **92** | **1.148** | 43 | 0.98 | B by 49m | B by 0.168kWh | Extrapolation/assumed oven |

At six: A 0.861 × 26.32 = **22.66p**, B 0.92 × 26.32 = **24.21p**, gap **1.55p**. At eight: A 1.148 × 26.32 = **30.22p**, B 0.98 × 26.32 = **25.79p**, gap **4.42p**. Such small example differences are not real household savings. Power rating is not measured consumption because heaters can cycle; no wattage-to-kWh shortcut silently used.

**False-causality / sensitivity tests:** (1) later air-fryer rounds start warm and may use less than the initial measured 0.287; (2) oven full trays may need longer or not cook evenly; (3) larger/dual basket changes capacity and draw; (4) serving the first plate versus all plates changes the announced time metric; (5) true equality of crispness/cooked food is UNVERIFIED; (6) microwave, gas oven and joint use are out of scope. Neither headline nor narration asserts an empirically observed large-family win. Each scripted numeric comparison is from this exact ledger.

## Sources read and claim mapping

1. **Which? original consumer comparison**, Jamie Mayne, published **2026-10-23**: https://www.which.co.uk/reviews/air-fryers/article/air-fryer-vs-oven-energy-cost-cooking-results-compared-aPpAt8D1Agy5 . Read sections *Is it really cheaper?*, *Chips*, table and method. **Supports:** measured 320g chips A 23min/0.287kWh, B 33min/0.863kWh; max recommended 500g for its fryer; uneven doneness; electricity tariff 26.32p/kWh. **Does not support:** 640/960/1280g oven time/energy, subsequent repeated air-fryer rounds, universal appliance ranking. Independent expert warns batch cooking erodes savings.
2. **Which? how we test**, https://www.which.co.uk/reviews/air-fryers/article/how-we-test-air-fryers-aCHgw2L7PYzU ; read *Machine performance*. Four portions cook at substantially different speeds across fryer models (range given 20–45+ min). **Counter-evidence to generalizing the 23-minute number**. No new trial reported here.
3. **Which? 2022 release** https://www.which.co.uk/policy-and-insight/article/air-fryers-worth-the-hype-which-testing-reveals-aJmjx4P8WNv4 , 2022-12-05: earlier test context and a clear warning that savings can disappear when multiple batches are required. Don't count this as independent confirmation of all 2026 values: this appears related to the same household experiment.
4. **2026 independent content context**: Which? current appliance annual running cost https://www.which.co.uk/reviews/cutting-your-energy-bills/article/how-much-your-appliances-cost-to-run-a7N937v2SWom (2026); not used to attribute annual savings to our A/B model.

## YouTube metadata observed (not watched, no transcript/comment access)

As of **2026-11-19** public search result snapshots. Views are snapshot numbers and cannot be used as channel-normalized demand, retention, CTR or trend velocity. YouTube URLs are direct; durations for these results were *not reliably exposed*; avoid fabricated lengths.

| Video / publisher | Published | Language / format | Public views observed | What it can, and cannot, signal |
|---|---|---|---:|---|
| [Air fryer vs oven — which bakes better?](https://www.youtube.com/watch?v=GdDlOqgjqNY), Diana Kis | 2026-01-31 | EN/non-verified, format/duration UNVERIFIED | 47,584 | Recent in year, but outside 90-day fresh window; result metadata only |
| [Air Fryer vs Oven vs Microwave](https://www.youtube.com/watch?v=ceL_LwloRqc), Grant Wills | 2024-07-23 | EN/title; Shorts-like #airfryer, exact duration UNVERIFIED | 392,915 | Evergreen mixed-three-appliance scope and creator effects; not a baseline for our illustrated A/B |
| [Air Fryer vs Oven — Which Uses Less Electricity?](https://www.youtube.com/watch?v=3kNmrynubAk), Policzona Szama | 2025-06-18 | Polish/format unknown | 51,977 | Relevant question, different audience language |
| [Air Fryer vs Convection Oven Energy Usage](https://www.youtube.com/watch?v=naebC2xDZX8), What Do We Need | 2025-10-11 | EN/duration unknown | 100 | Counter-signal: not all generic comparisons attract attention |
| [Which Is Best? Air Fryer Vs Oven Pros & Cons](https://www.youtube.com/watch?v=2F6I9M_TVU8), Bald Foodie Guy | 2022-03-17 | EN/duration unknown | 22,166 | Mature topic, channel effects; no matched same-author sample |

**Baselines/limitations:** same-author matched published-duration/age baseline is UNVERIFIED (search did not return trustworthy comparable runs). No actual transcript, videos or user comments were successfully read, so no claimed analysis of audiovisual beats, reactions or real viewer questions. Actual search terms `air fryer vs oven electricity cost`, `air fryer vs oven 2026`, `roll vs fold luggage`, `matching socks` are topical and free of internal project identifiers. **Fresh 30–90-day demand UNVERIFIED**: 2026-10-23 *consumer article* is fresh fact evidence, not a 2026 viewer-interest trend. Other creators' millions or isolated views cannot show success on Two Ways Lab. Own analytics and YouTube Studio/vidIQ statistics unavailable; no paid credits spent. Strong **experimental editorial hypothesis**, NOT proven viewer demand.

For finalist luggage, general YouTube packing tutorials were discoverable, but a comparable same-clothes measured head-to-head could not be verified; no audience conclusion. For sock sorting, results chiefly showed folding tutorials, e.g. https://www.youtube.com/watch?v=P9M-KGdaxjs (2015-07-15, MADE.COM; 132,396 snapshot views), **not** an experiment with identical pairing workloads. So their measured popularity cannot be fairly compared to the selected topic. No comments analyzed.

## Story structure, objections and next-video

- **Promise:** “One batch wins; does it still win when everyone wants dinner together?” Viewer receives a complete answer to specific declared model and learns why an appliance slogan isn't a recipe for group meals.
- **First frame:** Six equal 160g plate icons and one visibly limited A basket opposite large B oven. Cyan A, amber B, no Paper/Nuviko elements.
- **Causal chain:** verified small batch A quicker → capacity restricts A → sequential batch queue → assumed large B session → B faster for six → energy still favors A in six-case model → eight-case crossover and validity caveats.
- **Payoff:** At six portions time B by 29m; at six A energy by .059kWh; at eight B both. No real-world measurement claim beyond the two-portion benchmark.
- **Strong objection:** A true chef might not cook eight portions on one oven session to equivalent doneness, and a hot fryer may consume less energy on later rounds. These must remain visible limits, not hidden footnotes.
- **Forward link:** no verified published next-video intro available; current payoff must stand alone. A Short can return to the kitchen's next six-person order; native Related video planned only if a verified relevant episode exists. Do not invent an intro clip or link.

**Selection result:** best candidate **02m** as a concise A/B with multiple real explanatory steps. The Long drafts have editorial value but **no production Long recipe** in Two Ways ChannelSpec. First-listener demand and actual Short loop/AV seam UNVERIFIED.
