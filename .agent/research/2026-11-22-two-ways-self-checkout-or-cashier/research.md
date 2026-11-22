# Research · Two Ways Lab · 2026-11-22

## Scope and selection
A familiar task: I have a shopping basket, and I must decide between a staffed cashier and a nearly empty self-checkout area. Same basket, same payment, same start/finish metric. All seconds in narration are **hypothetical declared inputs**; this document distinguishes them from published observations. Audience benefit: a shorter visible line does not necessarily mean an earlier exit; basket size and delay margin decide.

Verified remote main at selection: `131ef24068d75967b1e43aa88e5f1370f6775054`. Last created story Draft PR #367 Nuviko (then #366 Paper and #365 Two Ways); next channel Two Ways. Closed/open PR and issue screening was performed. Related existing PRs were kept untouched. PR #124 merged and its policy is now in main. Reference voices read: exact accepted B USS S-5 (`78b375bf0004fdeb45722e6106f2919f09e82fe1`) and Lawnchair Larry (`28862598989045cd02990e654b086afae28fea59`); they are prose benchmarks, **not demand evidence**. No prior accepted/producing master revised.

### Broad candidate coverage (12 distinct everyday problems)
| Candidate | Funnel result / reason |
|---|---|
| Staffed cashier vs self-checkout *same basket* | **Finalist 1; selected.** Visible expectation reverses at reproducible quantity threshold; model can be stated honestly |
| Roll clothes vs fold clothes in one suitcase | **Finalist 2**; strongest alternative, very visual and immediately relatable; no comparable measured suitcase fit or verified packing-crease outcome, tempting but no factual payoff yet |
| Clean as I cook vs clean only afterwards | **Finalist 3**; relatable process and possible suspense, but with equal work and an unused waiting period the first method dominates or ties unless extra assumptions are introduced |
| Nearest item versus aisle-sweep grocery route | duplicate/occupied by #237 |
| One serpentine checkout line versus parallel lines | duplicate/occupied by #136; materially different from staff-versus-self handling here |
| Directly pair socks versus sort all first | duplicate/occupied by #350 |
| Put backpack items by category versus retrieval order | duplicate/occupied by #356 |
| Check each furniture assembly stage versus only the end | duplicate/occupied by #365 |
| Park nearby versus walk from an open spot | duplicate/occupied by #127 |
| Clean by room versus tool/task in three rooms | duplicate/occupied by #186 |
| Dishwasher versus washing by hand | overlapping existing #168 and #303 |
| Diagonal versus straight gift wrap | occupied by #162 |

Not a quota of weak rivals: top three genuinely compete in audience recognition. If suitcase volume data were actually measured, its visible result could surpass selected checkout; the present candidate wins on **falsifiable and reproducible closure now**, not because folding is unattractive. Cooking might support a cleaner short story but cannot honestly promise a surprise reversal on available input.

### Equal final-stage proposals
| Finalist | Actual first spoken / shown scene | Development beyond hook | Full payoff | Strongest objection |
|---|---|---|---|---|
| Checkout | EN: “The self-checkout line is almost empty. The cashier has a queue. I have eighteen groceries.” Split lanes with same basket, metric declared before revealing result | Wait savings of 60s competes with 4s extra per handled item; 18 items lose 12s; replace basket as a separately reset scenario to reveal six-item reversal; 15-item threshold | Method A 149s vs B 161s at 18; B 77s vs A 113s at six; no universal winner | Completely hypothetical rates; numbers may feel like an arithmetic lesson rather than a real contest; 2m longer than channel Short orientation |
| Pack suitcase | I close a suitcase: neat folds fit, rolled clothes may not; show the exact items and space | Repeated re-packing under one suitcase geometry; then test usable volume and access | Honest measured occupancy/crease/access trade-off, **currently unmeasured** | May change clothing dimensions by camera or compressibility and invent result |
| Clean while cooking | While a pot simmers, I choose to wash used items now or stack them for later | Keep identical number of dishes, washing times and food deadline; compare work overlap and interruptions | Total finish time/time to sit down, if timing data were available | In baseline work-conservation model, waiting time with no other tasks makes clean-as-you-go weakly dominate; a forced loser would be contrived |

## Narrative mechanism and falsifiable model
**Pre-declared metric:** elapsed seconds from joining queue to paid-and-packed completed basket, not scans per second, visible people count, preference, or customer satisfaction. Identical stock-keeping items in each counterfactual comparison (ordinary barcodes, no special produce/age check), one payment method. Separate 18-item and 6-item scenarios clearly reset the universe; never shrink items inside one simultaneous A/B.

- A (staffed): 80s modeled fixed wait + 3s per item scanning **and packing** +15s payment = `A(n)=95+3n`.
- B (self): 20s modeled fixed wait + 7s per item scanning **and packing** +15s payment = `B(n)=35+7n`.
- The two packing stages are included in per-item rates on both sides; no double charging. No real staff or customer clocks were used.
- `n=18`: A=149, B=161. Cashier earlier by 12s despite 60s longer queue.
- `n=6`: A=113, B=77. Self checkout earlier by 36s. These are two declared model scenarios.
- Equality `95+3n=35+7n` ⇒ `n=15`; at 15 both 140.
- For n=14 B 133, A137; n=16 A143, B147; n=24 A167, B203.
- A six-item B with **modeled** assistance +45s ⇒ 122 vs unchanged A113. Disturbance of 36s yields tie.
- For n18, variable A queue `q`: A=q+69; B161 fixed; q=92 tie, q=93 B wins by 1.
- If B per-item rate improves to 5s, n18 B=125 against base A149, B wins by 24.

This proves only arithmetic under assumptions. It does **not** generalize typical queues, actual checkout throughput, errors, accessibility, privacy preference, number of terminals, basket mix, staff assistance or measured user experience. A live study would require repeated observations controlling baskets, queue and payment/packing intervals, with permissions. No such testing is claimed.

## Sources actually opened — factual support and limits
1. **Kwak, Jin Kyung. 2020.** “Empirical Analysis on Comparison between Self-checkout and Regular Staffedcheckout lanes in a Poland Retail Store.” *International Journal of Advanced Culture Technology* 8(1), 56–61, DOI `10.17703/IJACT.2020.8.1.56`. [Publisher abstract and table of contents](https://www.earticle.net/Article/A372337) visited 2026-11-22; the publisher notes limited full-text access. In this **one** store, average self transaction durations longer despite fewer bought items; per-item and fixed transaction components longer. Not a randomized identical-basket comparison, NOT evidence for 3s vs 7s or our 80/20s waits.
2. **Ludin, Daniela, et al. 2025.** “Influence of Innovative Digital Tools in Retail on the Purchasing Behaviour.” *Tehnički glasnik*, 19(Si1), 147–153; [full author-uploaded text](https://www.researchgate.net/publication/391551210_Influence_of_Innovative_Digital_Tools_in_Retail_on_the_Purchasing_Behaviour_An_Empirical_Study_Based_on_a_Customer_Observation_and_on_a_Customer_Survey), visited 2026-11-22, study observes Heilbronn, Germany, Nov 2024. At ordinary time, paper reports **3:10 vs 0:14 queue** (cashier vs self), and **1:08 vs 3:08 processing**; longer self handling, shorter self waiting, with different baskets and observed groups. This actual study concluded the combined self trip shorter in its own setting, a **counter-signal** against universal cashier superiority. Its methodology/time windows cannot validate our counterfactual inputs.
3. **Cardinali, Rebecca, et al. 2025.** “Does automation reduce stigma? The effect of self-checkout register adoption on purchasing decisions.” *Journal of Economic Behavior & Organization* 237, DOI `10.1016/j.jebo.2025.107126`. [Peer-reviewed journal abstract](https://ideas.repec.org/a/eee/jeborg/v237y2025ics0167268125002458.html) and [University of Illinois news release, July 21, 2025](https://www.eurekalert.org/news-releases/1091943), read 2026-11-22. Purchase-data study shows greater self-checkout use for specific stigmatized products; researchers discuss choosing privacy despite time costs. Not proof of our store, scenario, or time rates. In 10m narration this is explicitly a separate preference beyond speed.
4. **Discussion, public opinion only:** [Reddit /r/unpopularopinion 2025-08-09](https://www.reddit.com/r/unpopularopinion/comments/1mlxfhv/grocery_store_selfcheckout_is_actually_slower_for/), visited 2026-11-22. Real disagreement over queue versus slow scans/packing; comments anecdotal, not a representative survey.
5. **Discussion, public opinion only:** [Reddit /r/The10thDentist 2026-07-19](https://www.reddit.com/r/The10thDentist/comments/1v0t39s/self_checkouts_at_grocery_stores_should_be/), visited 2026-11-22. Participants ask about large carts vs express baskets. This fits practical question but not measured demand for an animated 2-minute model.
6. **Official free observations, not privileged analytics:** previous Two Ways Lab channel metadata in repo; no verified owned CTR, retention, stayed-to-watch or published-channel cohort data accessible for this new idea. No actual experiments performed.

### Public YouTube search signals, metadata ONLY (observation 2026-11-22)
The following indexed pages/titles were retrieved by public web search. **No video watched, no transcript analyzed, no live comments extracted, no channel baseline measured.** Published/view data are metadata observations with uncertain freshness, **not** CTR/retention, proof of current growth or direct A/B video demand.

| Video and link | Published (as indexed) | Author/language/format | Views in search metadata | Baseline/limitations |
|---|---|---|---|---|
| [WCCO/CBS Minnesota — self-checkout vs staffed discussion](https://www.youtube.com/watch?v=SJIRXwYwCtI) | 2023-08-01 | WCCO CBS Minnesota; EN; news/video; duration UNVERIFIED | ~2,378 | large broadcaster; typical comparable uploads UNVERIFIED |
| [CBS Boston — self-checkout coverage](https://www.youtube.com/watch?v=uw4wF6WhsoQ) | 2025-10-23 | CBS Boston; EN; news/video; duration UNVERIFIED | ~4,168 | not direct modeled experiment; baseline UNVERIFIED |
| [Walking & Talking With Steve — self-checkout question](https://www.youtube.com/watch?v=spkCcdEsTSo) | 2025-10-20 | Walking & Talking With Steve; EN; conversation/video; duration UNVERIFIED | ~2,006 | subject but different format; baseline UNVERIFIED |
| [Turns Out — self-checkout examination](https://www.youtube.com/watch?v=1IVOSPuSWzg) | 2026-09-13 | Turns Out; EN; long-form ~9m per indexed metadata | ~399 | within 90 days, weak fresh interest signal; baseline UNVERIFIED |
| [Built This Way — self-checkout discussion](https://www.youtube.com/watch?v=5Q9UKaViFRs) | 2026-03-15 | Built This Way; EN; video; duration UNVERIFIED | ~324 | low absolute traction, baseline UNVERIFIED |

2026-09-13 (70 days before observation) is a recent 30–90-day example; the rest are evergreen/older than 90 days. None establishes successful audience reception for a numeric Two Ways Lab A/B story. These video URLs and counts need direct YouTube recheck before any production decision. **vidIQ was not charged:** on 2026-11-22 `vidiq_balance` reported 0 credits, renewal 2026-12-06; required paid YouTube search unavailable. Public sources still used. No subscriptions bought, no credit refill triggered. **Demand remains UNVERIFIED, not zero.**

## Promise, progression and anti-overclaim
- **Stop:** the visibly shorter queue loses, with the same basket.
- **Stay:** handling time steals the queue head start; a six-item replay reverses winner and a 15-item tie exposes the rule. 5m adds bounded delay and wait sensitivity; 10m examines controlled parameter changes and fairness, at cost of tempo.
- **Get:** a full result and actionable question: count remaining work, not only people in queue. No fake empirical claims, no normative “always choose self.”
- **First frame:** two checkout lanes A cyan vs B amber and the same 18 items, queue/wait numbers clearly marked MODEL; no images generated, no real footage or logos assumed. Short editorial outro “I roll ... look up” connects naturally to opening sight; actual AV seam UNVERIFIED.

## Novelty, ownership and blockers
PR #136 concerns *queue architecture* (one shared line versus separate shorter lines), not this *service speed* and basket-threshold comparison. PR #272 concerns value-sized checkout shopping; also distinct. No overlap with #365's furniture check-now story. Query/search completed against open and closed PR metadata and issues, but unindexed long-description duplicates remain possible and recheck before writing.

The official `uv run ytv start` required before research could not start in this environment: executable `ytv` missing (os error 2). This is Git-only editorial exception, no runtime receipts, no lease/approval. Independent reviewer unavailable; exact script hashes not independently reviewed. ChannelSpec only describes production short; Long 5/10 blocked. Short script length exceeds usual 35–50s, so duration compatibility must be resolved before any production work. All media/assets/rights unverified; none generated. No edits to common standards, profiles, existing drafts, or publish schedule.
