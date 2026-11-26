# Research — two registers, one common queue vs two separate lines

EDITORIAL_CANDIDATE_UNREGISTERED. Observation date: **2026-11-16**. Channel: Two Ways Lab; English first-person illustrated experiment, **fictional deterministic model**, not footage, sampled customer data or empirical wait-time prediction.

## Selection and actual coverage

Ten distinct concrete candidate tasks checked against the channel backlog, recent Draft PRs (#127, #130, #133), E001 checkout pilot and earlier proposals:

1. Shared line for two registers vs two separate checkout lines (backlog #71): **finalist**; familiar irritation, two measurable clocks, observable idle register and a personal-vs-group twist. Strong objection: queue topic overlaps E001's different question (two carts vs five baskets), and an April 2026 creator already demonstrated queue pooling with 100 customers; we must not reproduce that video or its broken-register event.
2. Shop by list order or by aisle order (backlog #64): **finalist**; high real-life utility, obvious route geometry, fresh coverage about shop layouts. Objection: the optimal aisle-sweep answer is often clear before a story begins; demand and actual saved distance vary by store.
3. Suitcase: rolling vs folding versus packing cubes (backlog #11): **finalist**; recognizable travel task, identifiable genuine comparisons from different creators. Objection: a simulated 2-D fit cannot honestly establish real volume or fabric compressibility, while a physical measurement would be outside this run.
4. Find sock pairs immediately vs sort by color (backlog #1): deterministic move count possible; weak immediate payoff versus queue and existing batching topic.
5. Put books on a shelf as they arrive vs sort the whole batch (#4): more operations than personal stakes, possible invitation batching overlap (#130).
6. Carry groceries one bag at a time vs use a basket (home task): transport distance easy to model, but object capacity assumptions dominate.
7. Choose nearest subway car vs car by exit (#89): accessible everyday problem, but station and train timing would have to be invented.
8. One queue at a buffet vs separate stations (#99): fair capacity model possible, yet variable portion selection obscures a clean comparison.
9. Dish sorting by room vs collection tray (#31): honest distance metric possible, but limited development after reveal.
10. Route two friends by geographic proximity vs ready time (#90): car driving, schedules and traffic multiply unverified inputs.

Shortlist is three independent tasks, not three titles for the same fact. **Strongest alternative: suitcase packing.** Its video demand signals are better than the queue competitor's, but with no physical test available it cannot honestly promise a volume winner; the queue's numerical model is reproducible and has a more surprising dual-outcome payoff. The recommendation is conditional: the subject is not novel and its measured audience interest is UNVERIFIED.

## Finalist promises and explicit objections

| Task | Specific opening / first visible action | After hook | Full payoff | Strongest objection |
|---|---|---|---|---|
| Pool vs split checkout | “Would one long checkout line get six shoppers out faster than two short lines?”; six figures, two open tills, A/B layouts | Slow cart makes left register unavailable; common line keeps right till active; split lines trap two customers while the other till is idle | A finishes entire group at 5 vs B at 7, but shopper six personally finishes B at 3 vs A at 5; under equal service both tie | The 2026 comparable video already tests pooling; single mini-case is not universal |
| Shop-by-list vs aisle sweep | Two paths through same five aisles shown at a common entrance | List order forces return walks; revised path shortens travel | Same items, shorter computed distance, with restrictions on available cross-aisles | Reveal is foreseeable; a real store may move products |
| Pack rolled vs folded garments | Identical suitcase silhouette and fixed item set | Different arrangements create leftover spaces, but compression undermines a strict drawing | A verified geometry-only win, not claimed physical fabric volume | Need real-world tests to tell viewers anything about actual fabric |

### Model ledger — actual arithmetic, no claims of real measurement

All six shoppers arrive at t=0; two registers have fixed speeds and no switching costs. Shoppers 1..6 service durations: **[5,1,1,1,1,1] minutes**. Both methods start with shoppers 1 and 2 at opposite tills. Shared A dispatches next arrival to first available register (left wins ties). Split B fixes left queue = [1,3,5], right queue = [2,4,6], no transfers.

| Shopper | Duration | A register/start/end | B register/start/end |
|---|---:|---|---|
| 1 | 5 | L 0–5 | L 0–5 |
| 2 | 1 | R 0–1 | R 0–1 |
| 3 | 1 | R 1–2 | L 5–6 |
| 4 | 1 | R 2–3 | R 1–2 |
| 5 | 1 | R 3–4 | L 6–7 |
| 6 (I) | 1 | R 4–5 | R 2–3 |

- Entire-group finishing time: A=5; B=7; shared gains 2 model minutes.
- My own completion: A=5; B=3; split gains 2 model minutes.
- Waiting (before service) by shopper: A=[0,0,1,2,3,4] total=10, mean 10/6=1m40s; B=[0,0,5,1,6,2] total=14, mean 14/6=2m20s.
- During B minutes 3–7 R cashier is idle while L can have queued work. Specifically minutes 3–5 before L first finishes and minutes 5–7 while L handles shoppers 3 and 5.
- Counterfactual service 1 duration 3: A last finish 4, B 5; me A4/B3.
- Service 1 duration 2: A last finish 4, B 4; me A4/B3.
- All durations 1: A=3, B=3, me=3 both.
- Move duration 5 from shopper 1 to shopper 5, others duration 1: A=7, B=7, shopper 6 finishes 3 in both. This is a separately identified counterfactual, not the same run.
- All outputs are computable from the fixed rules. No claim about real store times, moving customers, aisle congestion, staff behavior or shopper decisions. No invented experiment/approval/provider results.

## Observable research evidence and counter-signals

All below reflect **metadata/articles actually accessible**, not viewing the full YouTube player, transcripts or comments unless specifically stated. No copied narration.

- [V DONUT, “market Queue Showdown! Which line is fairer?”](https://www.youtube.com/watch?v=A5v4Spl4XdU), **2026-04-09**, EN educational video, duration not verified, observed **7,382 views**, **20 likes**, channel about **297,000 followers** as indexed on 2026-11-16. Its description discusses one shared vs separate queues, a 100-customer simulation and a broken register; those are **description claims, not watched content**. This is a substantial overlap and a **weak performance counter-signal** relative to size of creator. Comparable recent (within 12 months), NOT fresh 30–90 days.
- [Engineer Guy / Bill Hammack, queueing theory video](https://www.youtube.com/watch?v=F5Ri_HhziI0), original discussed in [Mr Honner](https://mrhonner.com/archives/3023) and [FlowingData (2010-12-24)](https://flowingdata.com/2010/12/24/why-the-other-lines-always-seem-to-move-faster-than-yours/); English educational explainer, upload date, duration, views and modern baseline **UNVERIFIED**. Link from secondary source, YouTube watch inaccessible today. It shows a long-lived interest angle, not measured recent demand.
- [“PACKING CUBES VS. ROLLING”, Erin's Travels](https://www.youtube.com/watch?v=sAFwLHt_c9w), **2018-06-04**, EN travel video, **20,070 views**, author ~26,500 followers, duration not verified. Competing packing finalist.
- [“Best Packing Method? Side-by-side”, Tas's Travel Tips](https://www.youtube.com/watch?v=6RNBUJvSr6Y), **2019-06-28**, EN travel comparison, **218,911 views**, author ~2,130 followers, duration not verified. Strong evergreen counter-signal for competitor's demand; not automatically transferable to simulated packing.
- [“How Supermarkets Force You to Walk More”, The Hustle](https://finance.yahoo.com/video/supermarkets-force-walk-more-203238221.html), **2026-11-07**, EN news-explainer with transcript visible on the third-party page; YouTube URL/views and author baseline **UNVERIFIED**. A recent interest signal for store navigation but this is not an A/B route video.
- [“Map Grocery Shopping Method”, Apartment Therapy](https://www.apartmenttherapy.com/map-grocery-shopping-method-37496209), published approx 2025; personal essay that claims route savings; these are self-reported, not measured evidence for our model.
- [Scientific American, “The Science of Getting Through a Checkout Line Faster”](https://www.scientificamerican.com/article/the-science-of-getting-through-a-checkout-line-faster/), 2016: experimental behavior can change results; an important real-world counter-signal, not a substitute for our arithmetic.
- [2026 pedestrian queueing study](https://journals.sagepub.com/doi/abs/10.3233/ATDE251491): the abstract reports delays to distant registers and potential reversal at high loads. Abstract accessible; full study/effect size not independently read. It limits any universal “common queue always wins” claim.

**Comparability / missing data:** 2 directly topical YouTube leads by different authors; one recent video view count, one no verified count. Videos were not streamed or transcribed; comments and same-author ordinary-format/age baseline were not accessible. No own Studio analytics. No available 30–90-day direct performance samples. CTR, retention, growth velocity, viewer satisfaction, comparative uplift and current search demand **UNVERIFIED**, not scored numerically. No vidIQ credits used.

## Coverage, ownership and originality

The earlier Two Ways Lab E001 contrasts **two carts vs five baskets**; #127 parking, #130 invitations and #133 bathroom are separate tasks. This proposal examines **pooling two cashiers against fixed separate queues** and a dual metric, not E001's basket-size selection, the external video's 100-person sample or breakdown scenario. Deterministic invented service values are original modeling inputs, not copied empirical figures. Existing draft PRs and the main spec were checked before writing. Rights for future images, hero reference bytes, accurate graphic digits and any music remain **UNVERIFIED**; no external media accessed or generated.

## Promise, title image and payoff

English-first global audience. **Promise:** the apparently long common line finishes all six people sooner, while I personally finish sooner in one of the two shorter lines. **Genre:** light counterintuitive everyday calculation, not a real-world measurement. First visible proof: both registers, exact shared versus divided lanes and one conspicuously large cart. Payoff: two results and explicit scope, not “one method always wins”. Proposed 2m opening is a comprehensible standalone question; final return to that question is editorial text-only and not a checked AV loop.
