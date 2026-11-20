# Research — air fryer energy win versus purchase-price loss

Date observed: **2026-11-20**. Audience: English-speaking general household viewers considering an air fryer, especially owners of existing ovens. Evidence of topical discussion is not evidence of format-specific demand. No paid vidIQ, subscriptions or external production calls.

## 1. Selection (10 genuinely different household decisions, initial screening)

| Candidate | Audience reason | Evidence/limitation | Decision |
|---|---|---|---|
| Air fryer bought today vs keep an owned oven | Paying for a device may reverse an energy win; exact threshold | Fresh Oct 2026 primary lab; credible purchase-range model; YouTube/Reddit signals | **Finalist, selected** |
| Drive to cheaper petrol or refuel locally | Cheap price can disappear in the extra drive | Require regional pump prices, consumption, route distance; all conditional | **Finalist, strongest alternative** |
| Pay shipping or add a product for free delivery | Spending more can appear to save on delivery | Receipt arithmetic robust but low dramatic depth and varying basket utility | **Finalist** |
| Kettle vs microwave to heat one mug | Everyday fast/cheap decision, different heating losses | Appliance- and vessel-dependent; exact comparable measurements not fully read | Screened |
| Dehumidifier vs open windows for damp laundry | Time and energy versus indoor moisture tradeoff | Climate and room conditions determine answer; controlled comparison absent | Screened |
| Coffee machine capsules vs brewing a pot | Ongoing per-cup cost reverses speed/convenience | Consumable pricing volatile and product-specific | Screened |
| Buy pantry staples in bulk vs small packages | Unit price versus waste and spoilage | Need actual perishability evidence for fair payoff | Screened |
| Preheat oven early vs put food in cold | “Minutes saved” may conflict with cooking quality | Recipe-specific; cannot invent food-safe equivalent endpoints | Screened |
| Dishwasher vs handwashing | Counter-intuitive water cost | Already taken by existing GitHub story PR, avoid duplicate | Screened—occupied |
| Direct bus vs transfer | Apparent faster route can miss connection | Already taken by existing story PR #285 | Screened—occupied |

### Equal-strength finalists

**A. Air fryer / existing oven:** Opening EN: “Would buying an air fryer save me money if I already own an oven?” First visual: same 320g chips over two explicitly labelled methods, total purchase+power metric; after hook: small-load meter A wins → purchase invoice reverses winner → repeated dinners catch up → capacity boundary. Payoff: **201 identical batches** in an illustrative £30 at 26p/kWh model; previous oven wins total cash before that. Strongest objection: The actual lab fryer did **not** have verified £30 price; price/performance pairing is hypothetical; all other dishes and family portions unmeasured as a direct A/B. No universal claim.

**B. Cheap petrol detour:** Opening proposal: “I can save five pence per litre, and still pay more at the pump trip.” First visual: two stations and identical tank refill. After hook: add round-trip fuel, driving time and route to same amount of petrol, then find exact price-distance crossover. Payoff: threshold extra kilometres. Objection: no region-specific independently verified price and route, so viewer proof is only model; no newly confirmed 2026 video baseline in this pass. Serious challenger, **not a rejected idea**.

**C. Free-delivery threshold:** Opening proposal: “This ‘free shipping’ order costs me more than the paid-delivery cart.” First visual: same desired product/cart, two checkout methods. After hook: compare shipping fee to extra item price and use-value, then exact threshold; optional second regime where extra item was genuinely needed. Payoff: pay delivery if the unnecessary item is more expensive. Objection: payoff is almost exhausted in one sentence and does not convincingly support full 5/10m without repetition.

**Comparison:** A has real primary measured reversal between operational and capital costs and distinct 2/5/10 layers; B has stronger location-dependent utility but entirely hypothetical result and insufficient fresh analogues. C is intuitive but one-step. Selection is a creative hypothesis, not measured retention. Fresh interest is moderate/UNVERIFIED. Avoid engineering a false secondary energy win for oven when portion mass changes.

## 2. Source register and exact facts

1. **Which? (primary actual instrumented test)**, Jamie Mayne, *Air fryer vs oven: energy usage, costs and cooking results compared*, dated **16 Oct 2026**, read **20 Nov 2026**, https://www.which.co.uk/reviews/air-fryers/article/air-fryer-vs-oven-energy-cost-cooking-results-compared-aPpAt8D1Agy5 . Sections “Chips” and “Our research explained”: each cooked **320g frozen chips**; air fryer 23min, **0.287 kWh**, built-in electric oven 33min, **0.863 kWh**; preheating counted; Morphy Richards Health Fryer 480003 vs Bosch Serie 2 HHF113BR0B. Reviewer reports both somewhat inconsistent chip cooking. Model's fryer recommends max **500g** chips and half-full basket. “What we learned”: observed tested air-fryer market prices **£30–285**, **not** price of this exact tested model. **Cake had a different size** between devices and cannot be used as equal-load evidence. “Roast chicken” (1.3–1.4kg): 0.54kWh/53min vs 1.157/76; “Jacket potato” (~200g): 0.392/48 vs 1.084/68. Pricing table in article based on a prior tariff; model deliberately selects a **round hypothetical 26p** and computes from raw kWh, never lifts rounded retail pence as exact.
2. **Which? (same publisher, earlier study context, not independent lab replication)**, *Air fryers worth the hype, Which? testing reveals*, **5 Dec 2022**, accessed 20 Nov 2026, https://www.which.co.uk/policy-and-insight/article/air-fryers-worth-the-hype-which-testing-reveals-aJmjx4P8WNv4 ; emphasizes small basket and repeated batches, upfront purchase costs. Describes older cost inputs; do not combine its prices with October 2026 readings.
3. **Which? (technical explanation)**, *Are air fryers the healthiest way to cook chips?*, **1 Nov 2022**, accessed 20 Nov 2026, https://www.which.co.uk/news/article/are-air-fryers-the-healthiest-way-to-cook-chips-agV2a3l5x2Km . Air fryer shares forced hot-air mechanism with fan oven; different chamber/circulation, not proof every model saves a fixed percent.

## 3. Verifiable numeric model (not measured device purchase)

Starting state: **existing working oven, £0 incremental purchase**. Method A: purchase a hypothetical fryer for **£30** assumed to replicate Which? measured single-session **0.287kWh**; Method B: already owned electric oven as tested, **0.863kWh**. Both repeatedly cook an identical 320g frozen-chip batch, on illustrative price **£0.26/kWh**, constant across the period. One purchasing decision at t=0; metric total cash **purchase + electricity**. No added labor/lifespan/repair opportunity cost in model.

* A after n batches = £30 + n × 0.287 × £0.26.
* B after n batches = n × 0.863 × £0.26.
* Difference in running cost = (0.863 − 0.287) × 0.26 = **£0.14976 per batch**.
* B still cheaper at **n=200** by about **£0.048**; A first cheaper at **n=201**. At n=100 B ahead £15.024; at 50 B ahead £22.512.
* Hypothetical changed price, same *assumed* consumption: £100 -> first cheaper at n=668; £285 -> n=1904. No tests were performed on these price points.
* Twice/week, 201 batches ≈100.5 weeks (~1.93 years); daily ≈201 days. One/year and product lifetime unknown. These are not an investment guarantee.
* An illustrative 3×320g sequential fryer model: 0.861kWh and 69 min **if** each real subsequent session exactly repeats a single-session measurement. Not comparable to measured oven 320g; matched 960g oven measurement missing → bulk winner **UNVERIFIED**. Fryer max500g for model under test.

## 4. YouTube public metadata, not observed playback/analytics

Observed **20 Nov 2026**; YouTube dates and views supplied by public search result cards; watch time, impressions, audience geography, actual full video and transcripts **not accessed**. Video "duration" only where publisher explicitly gives chapters, otherwise **UNVERIFIED**.

| Author / sample | URL / ID | Published / language / format / observed views | Baseline, mismatch or limits |
|---|---|---|---|
| Diana Kis, “Air fryer vs. oven – which bakes better?” | https://www.youtube.com/watch?v=GdDlOqgjqNY / GdDlOqgjqNY | 2026-01-31; likely non-English? metadata English title, **spoken language UNVERIFIED**, video length UNVERIFIED; 47,584 | Same author baseline below, topic/format differ; cannot infer CTR/retention |
| Diana Kis, “3 quick dinner ideas for an air fryer” | https://www.youtube.com/watch?v=OnsD6Pec77o / OnsD6Pec77o | 2026-03-07; language/length UNVERIFIED; 25,362 | Only same-author ordinary cooking reference, not time-matched format |
| Kitchen Deals 4U, “Air Fryer vs Convection Oven” | https://www.youtube.com/watch?v=K0rVWcYrWO4 / K0rVWcYrWO4 | 2026-02-20; English description, spoken language UNVERIFIED; chapter markers 0:00–8:15+, 2,969 views | Affiliate/product explainer, **not** two-minute illustrated narrative; author baseline unavailable |
| The Review Eye, “Air Fryer vs Oven: Faster, Cheaper, or Just Hype?” | https://www.youtube.com/watch?v=K-rad-hkSE4 / K-rad-hkSE4 | 2026-04-18; English description, chapters to 4:13+, 112 views | Product-promo/affiliate and explicitly AI visual description; author baseline unavailable, **negative demand signal** |
| What Do We Need, “Air Fryer vs Convection Oven Energy Usage” | https://www.youtube.com/watch?v=naebC2xDZX8 / naebC2xDZX8 | 2025-10-11; English title, language/length UNVERIFIED; 100 views | Low views, non-comparable format, text claims not fact sources |

For 30–90 day window there are **no verified comparable strong YouTube hits** from current search. The 2026-10-16 primary lab article is **fresh evidence**, **not fresh YouTube audience-demand evidence**. Own channel CTR/stayed-to-watch/watch time UNVERIFIED; no video analytics connected/read. Only one same-author baseline visible; no manufactured normalized performance.

## 5. Real viewer questions/contradictions

* Reddit r/AirFryTalk, original discussion dated **2026-11-03**, https://www.reddit.com/r/AirFryTalk/comments/1xmbaju/does_an_air_fryer_use_more_electricity_than_an/ — commenters ask about measuring real electricity, one explicitly “Have you ever measured the actual difference with a power meter?” Low-vote anecdotes; **not statistically representative**. This is fresh 30–90d qualitative question signal.
* Reddit r/airfryer, **2022-07-29**, https://www.reddit.com/r/airfryer/comments/wbeo3r — user complains that large baskets require batches, defeating speed; another commenter points to air circulation. Evergreen qualitative counter-signal, not controlled data.
* Reddit r/airfryer, **2025-10-10**, https://www.reddit.com/r/airfryer/comments/1o3csjj — household with existing convection oven asks whether buying another fryer worthwhile; some conflicting comments. The purchase question matches story, not evidence of actual payback.

No Reddit post was treated as a measured savings test. No video comments or transcripts read. No source words copied into narration.

## 6. Promise, causal map, payoff, key counterargument

**Promise:** one repeatable meal and two honest methods, with a clear metric *total cash*, not cherry-picked runtime electricity. **Hook:** “Would buying an air fryer save me money if I already own an oven?” **Early action:** identical 320g bag and actual measured energy results; **turn:** £30 purchase cost erases efficiency win; **development:** cumulative cost crosses near n=201; **payoff:** 201st 320g portion under explicit assumptions, and why price/frequency/capacity change result. **Counterargument:** laboratory didn't measure a £30 fryer; modeled purchase energy assumption may be false. Big-batch crossover unmeasured. This uncertainty is stated in scripts, not hidden in research.
