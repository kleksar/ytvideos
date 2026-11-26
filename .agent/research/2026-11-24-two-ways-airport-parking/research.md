# Research — a two-dollar tariff change flips a five-day trip

Observed 2026-11-24. Intended audience: English-speaking everyday travelers who own a car and can order rides, not exclusively Sacramento residents. No claim of channel analytics or measured demand.

## Selection

Remote main a6023668001421b689a8142cebc0bd436545be6b; latest created story Draft #408 Nuviko History (head 5a1920c847a297b8d1d2457ffe55f828c00079a9), so Two Ways Lab next. Five pages of all PR metadata (100+100+100+100+8); five pages of all issues returned only PRs, release collection empty. Main contains E001 checkout, E002 socks, E003 carrying, E004 toast, E005 ribbons, E006 parking. Publication queue observed in Studio 2026-11-12 is stale; current publication state UNVERIFIED. E006/#127 is parking spot search/walking time, not airport transport round-trip cost; #406 split rail fares, #403 card conversion, #397 flight booking, #307 cheaper fuel detour, #400 EV charge are distinct. No title match for airport parking versus paid rides. Source calibration read exact EN/RU #20 at 78b375bf0004fdeb45722e6106f2919f09e82fe1 and #25 at 28862598989045cd02990e654b086afae28fea59; preserve conversational causality, do not imitate endings. Owner rejects #13 and #88; no reuse.

Ten distinct candidate problems screened against backlog, current titles and potential comparative mechanics:
1. Airport parking vs two paid rides: real tariff change, return quote uncertainty; selected.
2. Rental car prepaid tank vs self-refill: partial tank value and actual contract exceptions; finalist.
3. Pay checked baggage ahead vs within 24 hours: prepaid nonrefund risk vs fee discount; finalist.
4. Annual vs monthly subscription: familiar but needs a useful real cancellation/use pattern, not a chosen winner.
5. Airport bus vs rideshare for a group: cost/time depends on first-mile connection and service hours; model alone risks hiding feasibility.
6. Ship suitcase vs check it: comparable delivery date and both real quotes unavailable.
7. Hotel breakfast package vs buy breakfast: menu prices/consumption not secured.
8. Home airport vs more distant airport: same flight timing and real fare/ground transport comparison needed; adjacent to several travel PRs.
9. Buy or rent occasional specialist luggage: useful break-even but comparable rental availability/fees not verified.
10. Move items in one load vs batches: already near E003/#362; no new angle sufficiently distinct.
Items 4–10 preliminary screening, not full web evidence. Targeted searches for three finalists only; no paid calls.

| Finalist | Opening/action | Development | Payoff | Strong objection |
|---|---|---|---|---|
| Parking vs rides | “I have a five-day trip coming up. Should I leave my car at the airport, or pay for two rides…” | Real $12→$14 tariff flips same trip; return fare changes; lot fallback | Exact $43 return-fare limit conditional on availability | $3 base margin is tiny and assumed ride costs; tariff reversal is a near-tie model, not universal savings |
| Rental fuel | “I can pay for a full tank now or refill what I actually use.” | Prepay leaves unused fuel, self-refill requires stop, possible contract-specific exceptions | Compare consumed fuel with paid tank; estimate convenience separately | Terms differ by jurisdiction, and fuel remaining could be chosen to force any winner |
| Bag fee | “I can pay for my suitcase now or wait until I know I need it.” | Early discount vs losing payment if bag no longer needed | Pay when certainty exceeds a threshold given terms | Fees and exemptions vary; official indexed page may predate the November hike |

Parking beats nearest rental fuel candidate because an actual recent tariff change provides a concrete fixed-input reversal and real audience questions directly ask whether length changes the answer. Rental fuel is valuable but its contractual exception dominates a short comparison. Bag fees are timely but exact current tariff conflict (AP search result versus cached airline page) would require a fresh route-specific quote. No conclusion about view performance.

## Facts and source locations

- https://flysmf.gov//to-and-from/parking — official page opened 2026-11-24, top notice effective Nov 19 ($14 economy, $19 daily, $28 garage); General Parking Information: no reservations, closure/alternative lot, shuttle required; South/East/West Economy section: daily maximum per 24h, shuttle. No assumption about residual fractional day pricing.
- https://flysmf.gov/articles/smf-parking-rate-changes-support-new-garage-and-customer-improvements — official release published 2026-09-17, opened 2026-11-24. Old and new daily tariffs $12→$14, $14→$19, $21→$28. Timing tied to Garage 2 opening; no need to claim why beyond this.
- https://www.uber.com/us/en/marketplace/pricing/upfront-pricing/ — accessible text on price estimates, route/duration/demand and possible adjustments; page explicitly notes some features differ in California. No live fare, surcharge, or availability estimate derived; $35/$40/$60 are hypothetical all-in prices. No attribution to Uber's Sacramento exact rules.
- https://www.hertz.com/us/en/blog/resources/refueling-your-rental-car — opened, 2023-06-29, prepaid full tank/no unused refund except stated ≤75-mile case; self-refuel. https://help.hertz.lv/hc/en-001/articles/36697438074141-What-are-the-fuel-policy-options-for-my-clients — opened, no unused fuel refunds under described FPO, market-specific. Alternative only.
- https://www.jetblue.com/help/checked-bags and https://www.jetblue.com/help/adding-bags — accessible indexed official text: earlier addition can save up to $10 for first two bags; fee generally refundable only if entire reservation canceled before departure, and fares vary. AP indexed report https://apnews.com/article/75bafdfceadcbdc8525dd4db1c099efa (November 2026 change; direct open failed) conflicts with cached table on exact current dollar amounts. Alternative only; no narration claims.
- Calculation and all assumed inputs: [model.json](model.json). Formula A = parking days × daily rate + fuel; B = outbound + return. Old 5×12+8=68; current 5×14+8=78; B=35+40=75. Tie return 78−35=43. Four days 64, six 92; higher return B=95; fallback daily A=103, garage A=148; extra wear A=88, return threshold 53. Verify direct cash only, not total ownership cost. No arbitrary delay or probability. No actual experiment.

## Viewer signals — observed 2026-11-24

Public indexed metadata only (not watching a video or reading its comments). English watch URLs; exact durations and format classification unverified except where chapter timestamps show a minimum runtime.

| Topic / video | Author | Publication | Indexed views | Observation |
|---|---|---|---:|---|
| https://www.youtube.com/watch?v=VhEBBGi4d7U | ZachusTravel | 2020-11-09 | 97,975 | English airport parking tips, description explicitly compares parking and rideshare; evergreen, exact duration unknown; direct page fetch failed |
| https://www.youtube.com/watch?v=o1-o-x1Xpqw | Aviation Approved | 2025-11-29 | 105 | English parking/transport savings guide, duration unknown; throttled direct fetch; counter-signal |
| https://www.youtube.com/watch?v=Egz2zUj13Q8 | KCRA 3 | 2025-07-16 | 3,096 | Local parking construction news, weak format match |
| https://www.youtube.com/watch?v=-_EiRuc8Rkk | FOX40 News | 2024-10-01 | 1,173 | Local lot closure, adjacent not comparable |
| https://www.youtube.com/watch?v=_kmvriQ8meU | AutoRentals | 2025-10-31 | 113 | Rental fuel guide, chapters through 1:51, no exact duration or watch |
| https://www.youtube.com/watch?v=8I0_dPbwVxI | WFAA | 2026-03-31 | 755 | Bag fee news, not experiment |
| https://www.youtube.com/watch?v=hMuAJxhT4ZU | NBC10 Boston | 2026-11-06 | 299 | Recent bag-fee news, weak format match |

No age/format-matched creator baseline. ZachusTravel channel indexed welcome video (five months old, 44 views) is not comparable with a 2020 how-to. Aviation Approved third-party channel profile does not expose comparable individual metrics; no baseline established. Neither a view/subscriber ratio nor old accumulated views infer CTR or demand velocity. Own analytics not available. All demand scores UNVERIFIED. No vidIQ paid requests.

Fresh signal 2026-11-22: https://www.reddit.com/r/Sacramento/comments/1y2yann/new_parking_at_smf/ indexed actual discussion about new fees; one comment says parking is still cheaper than Uber, a reply notes that it depends on trip duration. Indexed +164 post / +34 and +62 comments, not guaranteed live values. Direct open disabled, indexed excerpts only. Strong fit with conditional comparison, no general audience proof. Evergreen questions: https://www.reddit.com/r/Sacramento/comments/1o3yh6g (2025-10-11) asks drive vs Lyft/Uber amid parking availability concerns; https://www.reddit.com/r/Sacramento/comments/1rrgp7h/how_is_the_parking_garage_at_smf/ (2026-03-12) asks garage availability for a short trip because rides became expensive; https://www.reddit.com/r/folsom/comments/119dope (2023-02-22) discusses duration and ride reliability. These are individual anecdotes, not probabilities. Counter-signal: some travelers value convenience over small savings; transit can be cheaper. Alternative baggage question https://www.reddit.com/r/jetblue/comments/1ay6g41 concerns early payment vs free-bag eligibility. Rental fuel viewer comments not retrieved. Experimental topic, not proven demand.

## Story design

Same person, same five full parking days, same fuel and assumed ride pair. A/B decision before outcome; metric declared. First reveal uses historical tariff as counterfactual; second changes tariff only. Final threshold answers future price risk. The 5m variant adds duration and fallback; 10m adds accounting scope, partial-day caveat, uncertainty without invented probabilities. No fake quotes, actual rides, or waits. Audience objection is addressed by stating small margin and conditional feasibility. Alternative hook pairs considered: “A parking rate went up by two dollars” (cold context weak); “I have a five-day trip…” (chosen, clear decision); “My car used to be cheaper…” (spoils result before A/B). Short ending asks which two options after explaining full journey cost; next opening answers in first person. No actual MP4; AV seam UNVERIFIED. Related-video candidate E006 parking spot time comparison from dated publication queue; availability and exact intro unverified, so no invented teaser. Use native Related video only after verifying target/authority; no tail that breaks loop.
