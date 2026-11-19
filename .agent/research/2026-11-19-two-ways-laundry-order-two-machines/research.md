# Research — Laundry order: shortest wash vs longest dry

Observed 2026-11-19 UTC. Git-only editorial, not an official ytv run. Channel: Two Ways Lab. **One problem, two methods**, with a single declared metric and modeled, not measured, durations. All external search queries used generic topics, not private repository or user information.

## Selection / actual breadth

The main branch and **all 245 pull requests** (open/closed pages 1–3) were checked. The latest actually created story PR is Nuviko #245 (2026-11-18 23:25 UTC), preceded by Paper #240 and Two Ways #237. This makes Two Ways next. #124 was **merged** on 2026-11-16, so use current main editorial rather than proposed policy. Don't reopen owner-rejected #13/#88; don't alter accepted #20/#25/#46. An open #138 proposes a new Two Ways profile but is *not merged*; main's illustrated Shorts spec remains canonical.

Actual quick funnel of **11 distinct household problems** (not 11 rephrasings of one task):

1. Two separate machines, multiple loads: shorter wash first vs longer dry first — **finalist**; recognizable bottleneck, explicitly calculable, parameter-sensitive.
2. Packing a suitcase, roll vs fold — **finalist**; powerful visuals, outside videos; actual compression, wrinkles and achievable volume require an unavailable comparable physical test.
3. Two burners and four dinner components, quick steps first vs long steps first — **finalist**; recognizable shared-resource deadline, but realistic recipes, dependencies and warm-food metric require credible duration data.
4. Sorting 40 socks directly vs categorizing first — feasible operations but 5/10-minute expansion looks like a contrived puzzle.
5. Inserting books immediately vs sorting a batch — deterministic shifts, weak visual urgency.
6. Small printer jobs before a large print job — easy simulation, weaker household recognition and prior “three deadlines” topic nearby.
7. Loading a moving vehicle for density vs unloading order — physical volume and unloading effort unmeasured.
8. Pantry stock: oldest product first vs nearest — food-expiry dates and availability can dominate the supposed A/B; unsafe simplification.
9. Group-photo lineup by names vs by minimizing movements — testable, but too close to pre-existing #121 photo-ordering.
10. Shopping bags balanced by weight vs grouped by room — competing objectives; winner can be invented by assigning arbitrary weights.
11. Vacuum serpentine vs edges-first — requires accurate room geometry and coverage assumptions to compare fairly.

Additional dedup checks: #127 already has a parking-distance A/B; #133 shares one bathroom; #136 is checkout queues; #230 has USB-C matching; #237 covers grocery routes. Do not make a second PR on those angles. “Laundry pipeline” does not duplicate #168, which compares dishwasher to handwashing.

## Three finalist pitches (before full drafts)

**1. Selected — two baskets, one washer and one dryer.** Audience: someone who has multiple loads and a blocked dryer. Stop: “Same laundry, 25 minutes difference from order alone.” Opening: “The dryer helps decide whether I start with shirts or towels.” First development: A gets dryer running sooner; B makes clean shirts wait wet. Payoff: A 140 vs B 165, then changing *only* shirt-drying time flips the winner (A 140 vs B 130). The 5m adds a third basket and another reversal; 10m tests four baskets and honestly shows A/B are not globally optimal. **Strong objection:** optimizing the last dry item is a narrow, simplified goal; real cycle lengths and sorting restrictions may dominate. Demand for a *narrated two-method model* is UNVERIFIED, though the audience question is real.

**2. Strongest alternative — suitcase, rolling versus folding.** Stop: does rolling genuinely fit more clothes into the same bag? Development: clear packing demonstration, apparent winner and boundary from different fabric types; payoff requires actual same-bag, same-garment, same-pressure volume measurements. Video evidence includes [SmarterTravel 2018-10-23](https://www.youtube.com/watch?v=XLLUn-WXLDw) (search snapshot about 31,927 views), [Limitless Lauren 2019-03-04](https://www.youtube.com/watch?v=7PfFHBWhgww) (about 61,815). These are old, views time-dependent, not matched creator baselines. The obvious A/B visual may be stronger than laundry, but manufacturing a numerical “winner” from a flat illustration would be less honest. **NO_UPDATE for this candidate without real comparable measurements**.

**3. Two burners / four dishes.** Stop: why does preparing the quickest item first delay the whole meal? Development: burners blocked, cold completed dishes, second cooking order. Payoff could be a verified scheduling result, but without meal-preparation input timings it is an abstract model, and safety/food temperatures are omitted. YouTube counterpart evidence was not sufficiently comparable. This remains a hypothesis, not a weak competitor selected to justify #1.

**Decision:** select #1 as a controlled modeled experiment rather than invent physical measurements. The suitcase alternative has stronger visualization and public how-to signals; that advantage is explicitly preserved.

## Public audience signals: separate observation from inference

What was actually retrieved: search-indexed YouTube metadata/pages, a recent question and replies on Reddit, and explanatory articles for the scheduling algorithm. **No video watched, no transcript read, no YouTube comment thread read.** No channel's private analytics were read. Public views are not creator CTR, retention, growth rate or demand for *our* format.

| Exact video URL / ID | Author, language, format | Publish date | Observed views and source | Meaning and counter-signal |
|---|---|---|---|---|
| [rGYVrZOEHJc](https://www.youtube.com/watch?v=rGYVrZOEHJc) | LaundryLad2006, EN, “3 Minutes ASMR Speed Laundry” (exact uploaded runtime UNVERIFIED) | 2025-03-02 | 332,607 in web search snapshot 2026-11-19; 62,400 channel followers displayed | Topic can attract attention; ASMR montage, not two-method narration; ordinary same-author baseline UNVERIFIED |
| [bHtvDppOD0Q](https://www.youtube.com/watch?v=bHtvDppOD0Q) | Living minimal, EN, “Minimalist Laundry Routine”; runtime UNVERIFIED | 2024-08-06 | 4,922 in web search snapshot; 112,000 followers displayed | Negative/ordinary-strength signal beside a large channel; lifestyle routine, not A/B |
| [ja1GRQLD1wc](https://www.youtube.com/watch?v=ja1GRQLD1wc) | Cleana Meana, EN, laundry-room reset, ASMR without speech; length reportedly ~17:49 in mirrored sidebar, exact runtime UNVERIFIED | 2026-09-10 | YouTube indexed snapshot 12,014 vs a *different, newer mirrored snapshot* 36,218–37,384; these disagree, so exact contemporaneous views UNVERIFIED | 30–90d fresh topical interest; not a Short, narrated math, or experiment |
| [G6oy2Wx0VKY](https://www.youtube.com/watch?v=G6oy2Wx0VKY) | Same Cleana Meana, EN, Home Reset with laundry, ASMR | 2026-08-27 | mirrored snapshot 62,164, also a different observation time | Same-author baseline 1; broader cleaning content, not same experiment |
| [iTA-ZYfsWn4](https://www.youtube.com/watch?v=iTA-ZYfsWn4) | Same Cleana Meana, EN, home reset/laundry/pantry/bathroom ASMR | 2026-07-02 | YouTube indexed 264,115, older than 90d | Same-author baseline 2 and strong **counter-signal** against claiming a 2026 Sep laundry video outperformed author's ordinary posts |
| [jn1Hn4Q4CC0](https://www.youtube.com/watch?v=jn1Hn4Q4CC0) | Jordan Page, EN, personal laundry system tutorial | embedded in dated [author blog](https://lifeonanewpage.com/unconventional-laundry-system/) (2024 entry / page subsequently updated) | precise publish date, views, comparable baseline UNVERIFIED | Big-channel system videos don't validate narrator model or user retention |

Fresh window: 2026-08-21 through 2026-11-19. Sep 10 and Aug 27 fit; July 2 and prior videos are evergreen context only. Metadata from different snapshots must not be silently combined as if captured together. The observations don't prove outlier status, seasonality, creator growth, demand for the Two Ways format, or success likelihood.

Viewer questions (direct textual sources, not video comments):
- [r/laundry, 2026-01-14, heat-pump dryer laundry scheduling](https://www.reddit.com/r/laundry/comments/1qcga9j/folks_with_heat_pump_dryers_how_do_you_structure/): original poster asks how to accommodate long drying cycles and describes sequencing different fabrics; real replies discuss heat-pump dryer times, and also ask about mixed drying options. **This establishes a real question**, not video demand.
- [r/CleaningTips, 2026-01-15](https://www.reddit.com/r/CleaningTips/comments/1qdwfl6/laundry_day_how_to_be_efficient/): user asks why one washer/one dryer takes a whole day; commenters suggest timers and spreading loads. Their solutions are not evidence of a particular A/B winner.
- [r/Appliances, 2022-10-05](https://www.reddit.com/r/Appliances/comments/xw90jk): user specifically asks to synchronize washer/dryer cycles. Another commenter challenges over-optimization. These questions motivate the problem but are not a tested model.

vidIQ balance read 2026-11-19: **0 credits, 0 add-on**, renewable resets 2026-12-06. No paid YouTube search, transcript, comments or analytics; no purchase. Free web research completed. Creator baseline and direct YouTube comments remain **UNVERIFIED**.

## Verified model / reproduction contract

The two methods, fixed before the comparison: **A** sort loads by ascending wash duration; **B** sort loads by descending dry duration. Stable ties by basket label (none in primary cases). Each basket gets one non-preemptive wash followed by one non-preemptive dry; one unit per machine, machines may overlap, same order for wash/dry, wet-load waiting unlimited, immediate transfer whenever dryer available. All inputs available at time zero, no breakdowns/transfer time. Metric fixed **last drying completion minute** (makespan), not first ready garment or energy.

For order `p`, `washFinish = previousWashFinish + wash[p]`; `dryStart = max(washFinish, previousDryFinish)`; `dryFinish = dryStart + dry[p]`. Initial times zero. Independently enumerated all 24 four-load permutations in deterministic JavaScript; no physical laundry measured. Background explanation and constraints corroborated by [Atlas of Engineering, Johnson's Rule, updated 2026-11-07](https://atlasofengineering.com/industrial-and-management-engineering/johnsons-rule-for-a-two-machine-flow-shop/) (sections “State the scheduling model”, “Apply the rule”) and [Algorithm, Johnson's rule](https://algorithm.tamnd.com/johnsons-rule/) (problem, algorithm, proof). We don't copy their example jobs into narration.

| Load | Wash minutes | Dry minutes, normal | Dry minutes, changed-only case |
|---|---:|---:|---:|
| S — shirts | 20 | 45 | 10; also tested 20 tie |
| B — blanket | 35 | 60 | 60 |
| T — towels | 50 | 70 | 70 |
| X — synthetics | 40 | 10 | 10 |

Computed full results (minutes from shared time 0; all end times are modeled):
- 2 loads S,T, normal: A `S→T` = **140**, B `T→S` = **165**; A advantage **25**. Dryer A 20–65, *5-minute gap*, T 70–140. B dryer T 50–120, S 120–165. Do not falsely claim A dryer never idles in 2-load case.
- 2 loads S,T, shirt dry 10: A **140**, B **130** (B advantage 10). At shirt dry 20: **140 / 140**. Sensitivity threshold tied to these inputs only.
- 3 loads S,B,T, normal: A `S→B→T` **195**, B `T→B→S` **225** (A advantage 30). A dryer continuous 20–195; B 50–225. Total dryer time 45+60+70=175.
- 3 loads with shirt dry 10: A **185** (dryer gap 30–55), B **190**; *adding the blanket changes the two-load winner back to A*.
- 4 loads normal + X: A `S→B→X→T` **215**; B `T→B→S→X` **235**, A advantage **20**. A has a dryer gap 135–145. Exhaustively enumerated 24 permutations: `S→B→T→X` gives global minimum **205** (ten faster than A, thirty faster than B); largest **265**. This proves only A vs B among the **defined inputs**, not general optimality of either heuristic.

A separate objective (“shirt must be ready by minute 60”) in the two-load shirt dry10 case gives A shirt ready minute **30**, B minute **130**, even though B wins total makespan; never conflate the objectives.

### Source-grounded limitations

All durations are authored test inputs, **not facts about washer products**. Cannot recommend mixing fabric-care cycles or assuming ten-minute actual drying. Sensors, energy, humidity, machine temperature, transfer delays, load capacity, washable/dryable fabric constraints, sound/light effects, real-life priority and shopping/working time are out of model. If a real user needs a strict laundry recommendation, ask about actual clothing labels and measured cycle times. No false claim of a real experiment.

## Narration / payoff / scope

- Promise/title: same loads, two intuitive starting rules, different last-dry times, with a controlled flip.
- First demonstration confirms scenario rather than inventing personal experience: drawn pair of baskets, washer and dryer, simple two-row timeline with machine occupancy states (not generated image).
- 02m hook: “The dryer helps decide whether I start with shirts or towels.” Development A140/B165. Payoff changing one shirt drying time makes B130 vs A140. Last question “which machine should I check?” leads to first answer. Literal AV seam **UNVERIFIED** without MP4 or independent reader.
- 05m: third load makes A195/B225, visible dryer startup, then 10-minute shirt drying changes the *two-load* winner but adding blanket changes it back (A185/B190). More than a repeated 02m master.
- 10m: preserves full test, adds tie at 20, urgent-shirt objective vs all-loads metric, four-load A215/B235 and exhaustive 24-order counterexample 205. Story is technically complete, but high numeric burden and third reference sequence may weaken viewer value. **REWORK**, not a secretly approved ten-minute production.
- Strongest objection: one appealing 2m result doesn't prove an audience will watch a 10m scheduling tutorial; choose a shorter version unless specific own retention evidence justifies more.

No media, screenshots, voice, audio review, or runtime receipts were generated.
