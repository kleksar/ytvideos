# Coffee milk timing — one shared research packet

**Observation date:** 2026-11-17. **Channel:** Two Ways Lab under remote main `ba18d78f633d3829b85fa85123efc9ad635dac8f`, existing `short` 1080×1920 profile. **Status:** EDITORIAL_CANDIDATE_UNREGISTERED. All external queries used generic public terms without private repository information. No metered vidIQ call; no credits purchased.

## Audience problem and actual choice

An ordinary morning decision: coffee is too hot, I have ten minutes, and I want a milky drink. Compare **A: cold milk now**, **B: same cold milk at the deadline**. Same starting coffee mass/temperature, final milk fraction, room and wait. For B the milk remains refrigerated until mixing. Declare metric before reveal: **temperature of the completed mixed drink at t=10 min**, lower wins for cooling. Second interpretation changes **goal**, not starting states: for keeping coffee hot, the higher final temperature wins. This is an illustrative mathematical model, NOT a recorded experiment or claimed measurement.

First line of recommended exact EN: “My coffee is too hot. Should I add the cold milk now, or wait until I'm ready to drink?” After the question, the middle has unequal heat loss, the trap of checking before the final pour and the exact finished-mug comparison; payoff is 54.7 vs 53.8 °C and opposite recommendation when preserving warmth. The biggest objection: real mugs do not share one fixed time constant as their fill and evaporation change; the result is sub-one-degree and not a universal kitchen effect.

## Actual candidate funnel (11 distinct everyday situations)

The following is a **screen**, not 11 individually verified experiments or evidence of demand. Each candidate compared on recognizable problem, verifiable equal initial state, genuine late change and nonfabricated payoff.

| Candidate | Decision / why screened |
|---|---|
| Coffee milk timing | Chosen: everyday, counterintuitive, published experiments, reproducible explicit model; demand unverified |
| Two laundry loads: sequential wash+dry vs overlapping | Strong contender; valid shared-machine timing but win is predictable, little new after hook |
| Shortest pedestrian route vs fewer crossing delays | Strong contender; clear delay threshold, but arbitrary signal timing dominates the illustrative model |
| First parking spot vs hunting closer | Unknown vacancy probabilities make a universal winner false without observed arrivals |
| Roll versus fold a suitcase | Real material compression/fabric and geometry need measurements not available here |
| Self-checkout vs assisted cashier | Prior queue pilot/adjacent backlog; overlap with TWL_E001 |
| Find a lost item systematically vs probability-first | Hypothetical location probabilities are hard to ground in a real everyday case |
| Sort socks by color first vs match one by one | Repeatable comparison counts; weaker stakes and limited meaningful development |
| Kitchen batch preparation vs cook each serving | Needs measured operation times; hard to produce a surprising outcome without hand-picked model |
| Dishwasher vs hand washing | Already captured in story PR #168; duplicate family |
| Walk or run in rain | Story PR #179 exists; direct duplicate |

### Three close proposals, checked on equal terms

**Coffee milk timing:** Hook above; development follows the uncompleted comparison and different cooling losses; payoff reverses based on metric. Biggest objection: tiny modeled difference, physical confounders and several existing educational videos; offer a precise conditional explanation, not a sensational reveal.

**Laundry overlapping cycles:** Exact possible opening, “I washed the second load while the first was drying. How much time did I really save?” Development would model one washer, one dryer, transfer delay, dryer bottleneck for a third load; payoff is total end time, not an invented measurement. Objection: obvious benefit for two loads and no compelling second surprise without extra assumptions; better suitable to a short standalone tip than three complete scripts.

**Walk route with signals:** Opening “The longer route got me there first—even though I never walked faster.” Development: fixed route distances, pedestrian speeds and explicit light phases; payoff is a threshold crossing delay at which the detour wins. Objection: fabricated lights/weather can make either route win, and the setup resembles existing wait-time story #175. This cannot be represented as a city observation.

**Selection:** Coffee offers the stronger question, supported explanatory mechanism, and a second meaningful decision about *keeping* heat. The laundry candidate is strongest nearby alternative if this premise is rejected. The chosen story still faces material doubts: ~0.9 °C is a low-stakes payoff and The Action Lab published an adjacent video in March 2026. Classification is a hypothesis about interest, not verified performance.

## Reproducible model, all quantities defined

Toy assumptions: initial black coffee `T0=90 °C`, milk `Tm=5 °C`, room `Ta=20 °C`; milk fraction by **final mass** `f=0.15`; waiting time `t=10 min`; both paths assigned **same illustrative effective** time constant `tau=20 min`; equal per-mass heat capacity, instant mixing, constant room, no losses from milk while stored in fridge, and no change in cooling coefficient when milk changes total liquid volume. The latter is knowingly unrealistic: a pedagogical assumption, NOT measured physics. One mug's initial coffee mass equals the other's, and each gets the same final milk mass.

`mix=(1-f)*T0+f*Tm = 77.25 °C`

`A(t)=Ta+(mix-Ta)*exp(-t/tau)`

`B(t)=(1-f)*[Ta+(T0-Ta)*exp(-t/tau)]+f*Tm` (cold milk added at exactly t).

| Wait | A final °C | B final °C | A−B °C |
|---|---:|---:|---:|
| 0 min | 77.250 | 77.250 | 0 |
| 2 min | 71.802 | 71.588 | 0.214 |
| 5 min | 64.586 | 64.089 | 0.498 |
| 10 min | 54.724 | 53.839 | 0.885 |
| 15 min | 47.043 | 45.856 | 1.187 |

At ten minutes, black coffee **before B's final mix** is 62.457 °C. Do not compare that directly against finished A: it is not the declared end state. With `Tm=Ta=20 °C` in this toy and the rest unchanged, final A and B become equal by algebra. If objective is instead **higher** final temperature, A wins from the exact same results. Do not reuse these numbers as thermometer readings or imply real mugs must follow them.

## Primary and external literature supporting the mechanism

- Rees, W. G., Viney, C. **“On cooling tea and coffee,” American Journal of Physics 56, 434–437 (1988)**, DOI `10.1119/1.15572`, bibliographic record/abstract: https://openalex.org/W2157893741 . This paper states black coffee cools faster than white, and *under most but not all circumstances* early milk helps retain heat. Accessible abstract; detailed full-paper methods not verified here.
- **Vernier, “Cooling Coffee” (May 16, 2011):** https://www.vernier.com/vernier-ideas/cooling-coffee/ . Educational temperature-logging example: milk early led to warmer cup at experiment end. Conditions not asserted to match our model.
- **Richard Fox, Irish Science Teachers' Association (2016), classroom investigation:** https://www.ista.ie/wp-content/uploads/2016/10/Sc-v51-3-May-16.pdf . Most groups reported milk-last colder after waiting 5–10 min; fair-test confounders highlighted. Published classroom report; not our measurement.
- **Mathematics Magazine, “Cooling Coffee without Solving Differential Equations” (2017):** https://www.tandfonline.com/doi/abs/10.4169/math.mag.86.3.204 . Mathematical generalization notes that real evaporation/radiation violate Newton's simple law; abstract reviewed.
- **Modernist Cuisine, “The Physics of Coffee & Cream” (Dec 12, 2012):** https://modernistcuisine.com/mc/the-physics-of-coffee-cream/ . Early cream preserves warmth; viscosity/evaporation are real-world mechanisms; article is explanatory, not our controlled experiment.
- **VideoPhysics, “When to add milk to your coffee” calculator:** https://www.videophysics.com/newtons-law-of-cooling . Public transparent preset `90/20/20 min/0.15/5/10 min` produces `54.7` vs `53.8 °C`, matching independently recomputed toy formula. A public calculator's preset does not validate its parameterization for real mugs.

## YouTube relevance: observed public evidence, not predicted demand

**Search performed** 2026-11-17 for milk-first/milk-last tea and coffee physics, cooling experiments and comparable science demos. These entries are publicly indexed video metadata/descriptions; the YouTube **video content was not watched** in this run, and comment archives/transcripts were not retrieved.

| Video URL/ID | Channel / language | Publication date | Format/length | Public views observed | Evidence, limitations |
|---|---|---|---|---|---|
| https://www.youtube.com/watch?v=FDJpe54FC-A | The Action Lab / EN | 2026-03-07 | Long; 7:30 from third-party archive | ~189,658 in indexed YouTube result | “The Weird Physics of Adding Cream to Coffee.” Direct same-topic overlap; 2026 video but over 90 days old |
| https://www.youtube.com/watch?v=CCuaWqhVvIc | Stand-up Maths / EN | 2016-08-12 | Long; exact duration UNVERIFIED | ~298,674 in indexed YouTube result | “Milk first or last?” Description includes audience-reported concerns about unequal water quantities and spoon temperatures. These are **creator-reported comment objections**, not comments independently read here |
| https://www.youtube.com/watch?v=KOsYsrhnODs | Higgsino physics / EN | 2019-04-20 | Video; exact duration UNVERIFIED | ~16,000 from Filmot indexed page | Broader “Best Method to Cool Coffee”; adjacent cooling-method interest but not a milk-timing comparison, not direct evidence for angle |

**Comparable creator baseline, not an apples-to-apples controlled test:** The Action Lab's 2026-02-28 “How Salt Fingering Helps The Oceans” https://www.youtube.com/watch?v=qzv8ElahBA4 has ~94,707 indexed YouTube views; its 2026-03-14 “What Is The Speed of Surface Tension?” has ~192,158 in a public archived channel listing; “I Built Feynman's Reverse Sprinkler...” 2026-03-29 ~1.4m from another archived listing. All are EN science longform by the same larger creator, similar age but very different topics and packaging. The coffee video is *not* an obvious outlier blockbuster, and millions from a large channel cannot establish demand for our illustrated 2-minute piece. Stand-up Maths' 2016 baseline of similarly aged videos was **not recovered**, so no relative-performance claim is made.

**Fresh 30–90d vs evergreen:** No relevant 30–90-day YouTube performance series was verified in the accessible search; March 2026 and 2016 entries are evergreen/older. An October 2026 math explainer exists (https://surroundedbymath.com/world/how-fast-does-coffee-cool/), but it is *article freshness*, not YouTube velocity. Live 2026-11-17 view counts, CTR, retention, shares, actual audience questions beyond indexed description, and own channel analytics are **UNVERIFIED**. No views-per-subscriber or views-per-age extrapolation.

## Duplication and rights

GitHub PR / issue and default-branch searches for `coffee milk cooling` and `milk` found no matching already proposed story; this is a scoped discovery result, not proof no hidden local drafts exist. Earlier Two Ways PRs #168, #171, #175 and #179 cover other comparisons; E001 already covers supermarket queues. PR #138 remains a **draft unmerged proposal** to change channel identity/storytelling; the active main profile here is the A/B Two Ways Lab. No hidden data copied into external search. Script is newly written in our own language; physics concepts and public title metadata are facts rather than a license to reuse footage, thumbnails, transcript or someone else's formulas as rendered media. Do not use external video frames or quotes in production without rights review.

**Strong objection to face honestly:** even with a sound physical phenomenon, the toy's assumed equal tau and tiny difference could make the video look more authoritative than it is. Show “MODEL — NOT MEASURED” on any prospective graphic; never depict a thermometer reading as filmed evidence.
