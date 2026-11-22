# Research — backpack access A/B, Two Ways Lab

**Observation 2026-11-22.** Source main 131ef24068d75967b1e43aa88e5f1370f6775054; PR #124 merged 2026-11-16; current editorial applied. Search queries anonymized. Selection is editorial, not proof of demand.

## Funnel: twelve different everyday tasks

1. **Backpack:** group by category vs predicted use order — **SELECTED**. Strong opening at bus stop, reproducible stack, two different winners, but simplified physical constraints.
2. **Suitcase:** place bulky vs heavy items first — **FINALIST**. Visually stronger spatial puzzle, but no verified common dimensions/orientations to support a fair comparable model.
3. **Grocery bags:** distribute by weight vs unload-location categories — **FINALIST**. Realistic trip to kitchen, but primary metric (carry strain or unloading actions) not honestly resolved.
4. Shelve books immediately vs sort a batch — potential measurable movements, weaker instantaneous conflict.
5. Vertically fold T-shirts vs stack — visible access comparison, familiar angle and potential shallow result.
6. One parcel at a time vs grouped picking — batch setup friction, overlaps existing #344.
7. Tool tray grouped by type vs retrieval frequency — similar model, narrower audience.
8. Return kitchen items one-by-one vs carry grouped loads — dependent on unknown kitchen layout.
9. Fragile objects separately vs dividers — physical drop protection needs unavailable actual safety data.
10. Laundry sorting upfront vs on demand — overlap existing #246, reject.
11. Two people one bathroom scheduling — duplicate existing #133, reject.
12. Gift wrapping cut orientation — duplicate existing #162, reject.

Other current PRs screened include #230 cable allocation, #350 socks, #353 voice vs typing, #186 cleaning, #347 subway. Searches of all-state GitHub PRs for backpack, umbrella, bag organization, suitcase and shopping bags on 2026-11-22 produced no direct backpack match; not proof that every unpublished draft or private episode is known.

## Three substantive competing proposals

**Backpack:** viewer commuters/travelers/students. Opening exactly “I open my backpack at the bus stop. My yellow umbrella is sitting on top of the ticket I need.” Next: A/B fixed stacks, four retrievals produce A9/B6, two repeated umbrella requests change to A9/B12. Payoff is that access frequency matters more than visual tidiness for these exact inputs. Counterargument: chosen category priority and static-return rule are artificial; no measured seconds.

**Suitcase:** opening a full suitcase with one important item outside. Compare packing orientation with identical verified shapes and equal bag capacity; payoff a clear fit count. Counterargument: without genuine dimensions, any surprising fit result would be invented. Equal promise strength but facts less ready.

**Grocery bags:** opening bags that look equally full but require different unloading routes. Predeclared one metric and fixed grocery/room geometry needed; payoff a tradeoff in carrying versus putting away. Counterargument: a story whose winner changes based on a metric introduced afterward would be dishonest; primary metric unresolved.

**Decision:** backpack alone has a verified *computable* shift in winner and first-person recognizable situation without invented physical claims. Suitcase has attractive visuals, groceries a broad audience; neither has settled valid inputs. This does not establish that backpack has greater actual demand. Independent reviewer may reject the premise.

## Single fixed simulation: reproducible computation

One same top-opening compartment; eight loose items; no side pockets; objects returned to their original depths after **each** request. Count the number of other objects ABOVE the requested one, each obstacle once per request. Do not call this time or claim a filmed experiment.

- A top to bottom: umbrella (U), ticket (T), water (W), snack (S), headphones (H), charger (C), notebook (N), sweater (R).
- B top to bottom: ticket (T), snack (S), charger (C), umbrella (U), water (W), headphones (H), notebook (N), sweater (R).
- Initial requests: T, S, C, U. Extra umbrella U repeated twice. Optional counterfactual two charger C requests after that; not additional real-world measurements.

| Step | A obstacles | B obstacles | Cumulative A/B |
|---|---:|---:|---|
| Ticket T | 1 | 0 | 1 / 0 |
| Snack S | 3 | 1 | 4 / 1 |
| Charger C | 5 | 2 | 9 / 3 |
| Umbrella U | 0 | 3 | **9 / 6** |
| Repeat umbrella U | 0 | 3 | 9 / 9 |
| Repeat umbrella U again | 0 | 3 | **9 / 12** |
| Counterfactual one more C | 5 | 2 | 14 / 14 |
| Counterfactual another C | 5 | 2 | 19 / 16 |

For extended 10m only, possible **unscored** future hybrid stack U,T,S,C,W,H,N,R yields T1,S2,C3,U0,U0,U0 = **6** obstructions. Not part of this A/B. Each extra U shifts the A-vs-B difference by three toward A; each extra C by three toward B. Entire result depends on this stack, request sequence and replacement rule.

## Public viewer-interest context, not measured audience validation

YouTube **indexed cards/descriptions only**, observed with web search 2026-11-22; **no video watched, no transcripts or YouTube comments read**, language/format/duration and same-author age-matched baselines UNVERIFIED:

| Video / URL | Publisher & publication | Indexed metadata | Relevance and counter-signal |
|---|---|---|---|
| https://www.youtube.com/watch?v=MlE_Hc0MCnE | Gohar Khan, 2024-07-24 | about 4,626,512 views, 205k likes | Evergreen backpack organization, big author; not direct A/B and no controlled baseline |
| https://www.youtube.com/watch?v=SWOJj4-uhFA | DECATHLON, 2026-08-26 | about 22,122 views, 367 likes, channel ~404k followers | Recent 30–90d published tutorial; about space/creases, not item access, no evidence of recent view acceleration |
| https://www.youtube.com/watch?v=dZT2Xa6CB_0 | PGYTECH, 2021-06-24 | about 57,542 views, channel ~55.4k followers | Product-specific pocket tutorial, weak size/format comparison |
| https://www.youtube.com/watch?v=TgruAeiiaMY | Jessica Sousa, 2026-01-26 | about 114,215 views, channel ~3.33m followers | School packing, large audience scale, not evidence of this model's CTR/retention |

Index snapshots may be stale; no computed VPH from them. **Fresh 30–90d publication** exists, **fresh momentum UNVERIFIED**. **Evergreen** older organizing videos and questions exist; public popularity of big channels proves neither click-through nor retention for a small Two Ways Short.

Real community questions and disagreements, NOT YouTube comments:
- https://www.reddit.com/r/onebag/comments/1iixzzh/ (2025-02-06): travelers ask whether to group by day, outfit, type; replies value category grouping.
- https://www.reddit.com/r/onebag/comments/123o9p7/ (2023-03-27): pouches can make people remove several things onto the floor; some users unpack to keep daily access.
- https://www.reddit.com/r/onebag/comments/hzaxsi/ (2020-07-28): users explicitly prioritize quick access to toiletries/electronics, noting bag-specific differences.
- https://howcast.com/videos/386959-how-to-organize-your-backpack/ recommends first-needed items near the top; advice, not controlled evidence.

**Provider/own analytics:** Free vidIQ balance inspected 2026-11-22: total 0 credits (renewal 2026-12-06); paid search/video comments/analytics not called. No own CTR, stayed-to-watch, retention, private queue or comparable author baselines available: UNVERIFIED. Actual viewer demand for this exact A/B concept is an experimental hypothesis.

**Claim boundaries:** Original arithmetic only, not factual travel times. No invented missed bus, measured stopwatch, physical tests or general optimal packing assertion. No third-party media/assets copied.