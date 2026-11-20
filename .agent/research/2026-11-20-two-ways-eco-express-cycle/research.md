# Research — Two Ways Lab / the quick dishwasher button costs more energy

**Observed:** 2026-11-20 UTC. **Channel:** `two_ways_lab`. **Status:** EDITORIAL_CANDIDATE_UNREGISTERED (Git-only, not an official run). One story: A=Express 65°C / 1h, B=Eco 50°C / 3h35 on one Bosch SMS4EMI06G. **Owner of editorial decisions:** GPT-6, author research; external audience metrics unverified.

## Selection and actual coverage

Ten distinct *directions*, not ten verified successes; duplicates rejected before deeper spending. Several came from the channel's current 100-topic backlog or fresh general consumer questions.

| Candidate | Why someone might stop / stay / get something | Strong objection or result |
|---|---|---|
| 1. Same dishwasher, Eco vs Express | A familiar one-hour/three-hour contradiction → energy flips expectation → water, cleaning, practical deadline → a repeatable decision rule | Significant existing content; consumption numbers don't prove comparable cleanliness |
| 2. Laundry at 20°C vs 40°C | Can half the temperature preserve clean clothes? → energy savings vs stains → limits | Strong: Which? June 2026 reports 62% average energy saving at 20°C; needs same-load test for a clean winner |
| 3. Dehumidifier + airer vs tumble dryer | A long overnight dry might cost less than a hot short cycle → energy vs time/moisture → real constraint | Strong but results depend on dryer tech, ambient room conditions, dehumidifier duty and moisture; 2026 comparison describes such limits |
| 4. Heat-pump vs conventional tumble dryer | Different tech for same laundry → efficiency and payback | Purchase price and load assumptions vary; needs acquisition-cost and lifetime model |
| 5. Induction vs gas for the same pot | Power input vs useful heat at food → practical energy/carbon questions | Different energy units, local price and cooking setup; cross-fuel comparison without measurements weak |
| 6. Lid versus no lid for boiling water | Obvious small action → boiling time, steam loss, energy | Single answer arrives early, 10m value questionable |
| 7. Preheat oven versus cold-start pizza | Must finish the same food safely → time vs power | Many foods have manufacturer-specific instructions and safety; cannot assert equivalent cooking |
| 8. Same-laundry batching versus one load at a time | Machine cycles versus time to first clean item | Distinct from #2, but laundry-order story already occupies PR #246; overlap risk |
| 9. Washing dishes by hand versus machine | Compare time/water/energy | Already PR #168 and #303: reject as substantial duplicate |
| 10. Quick grocery checkout routing | Waiting versus walking → arrival time | Already represented in #136 and related queue variants; reject as duplicate |

**Three viable non-duplicate pitches compared:**

1. **Eco vs Express — selected.** Audience: ordinary English-speaking dishwasher owners. *Specific opening:* “Does the one-hour dishwasher cycle really use less electricity than the three-hour one?” First visible action: two program buttons, one unit, same theoretical load. *After hook:* manufacturer table reverses energy intuition; water agrees; time constraint can reverse practical choice; independent test cautions against assuming equal cleaning; a four-hour Silence program refutes a simplistic “longest is cheapest” rule. *Payoff:* Eco wins energy and water **for the stated Bosch model**, Express wins finishing time; cleanliness of exact pairing UNVERIFIED. *Strong objection:* an existing consumer explainer already covers the general fact; a single Bosch and a separate Which? sample cannot yield a real cleaning outcome. **Why stronger for 2/5 than #2:** same appliance, concrete surprising 2× energy ratio, one easy-to-draw panel, and a second real choice at a deadline, while keeping exact A/B state.
2. **20°C vs 40°C laundry — closest runner-up.** Hook: “Can my clothes get clean if I turn the wash down twenty degrees?” Development: Which? published energy differences of about 62% at 20°C vs 40°C, plus implications for heavily soiled loads. Payoff would be a conditional temperature choice. Objection: preserving cleaning score for the same stain and detergent across temperatures requires matching test data not yet obtained; already widely explained. Source: [Which?, 2026-06-09](https://www.which.co.uk/news/article/cut-your-laundry-costs-by-151-this-year-an6GD2M0Hgnn), [Which? washing-temperature guide](https://www.which.co.uk/reviews/washing-machines/article/washing-machine-temperature-guide-aLiyf2p96y4d). **Potentially stronger than selected** in broad everyday reach; selected wins on currently grounded and reproducible same-model inputs.
3. **Dehumidifier + rack vs tumble dryer — serious alternative.** Hook: “If I run a dehumidifier all night, did I really save power over a two-hour dryer?” Development: two machine energy totals, moisture removed, room conditions, heat-pump exception. Payoff: cost crossover under measured conditions, not a universal winner. Objection: humidity duty cycle and matched drying-to-the-same-level measurements missing; can't claim honest winner from a manufacturer watt rating alone. 2026 contextual source [energy.org.uk, 2026-10-03](https://energy.org.uk/articles/drying-laundry-energy-cost); EU [tumble-dryer guidance](https://energy-efficient-products.ec.europa.eu/product-list/tumble-dryers_en).

**Selection constraint:** this is a **hypothesis of viewer appeal**, not verified CTR or retention. The winner is chosen on concreteness and completed payoff, not asserted viral probability. Previous PR #168/#303 cover machine-versus-hand, *not* two programs on the same model; PR #246 concerns laundry order, *not* temperature.

## Primary numbers and audit trail

Source A: [Bosch original quick reference 9001913439 (040923), p.1, Programmes table](https://media3.bosch-home.com/Documents/9001913439_C.pdf), read in full page text and visually checked against the page image on 2026-11-20. Standard: EN 60436, guide conditions, run time may vary.
- Eco 50°C: 03:35, **0.645 kWh, 9.0 L**.
- Express 65°C: 01:00, **1.300 kWh, 10.5 L**.
- Silence 50°C: 04:00, **1.050 kWh, 10.8 L**; note identifies quiet night use.
- Default Favourite 00:15, 0.050 kWh, 4.0 L is **pre-rinse**, not full cleaning: [Bosch model-specific operating manual, §6.2](https://s3-eu-west-1.amazonaws.com/media.markselectrical.co.uk/manuals/SMS4EMI06G.pdf). The Favourite button is reprogrammable; use **factory-default** framing only.
- Manufacturer official service [Bosch SMS4EMI06G](https://www.bosch-home.co.uk/supportdetail/product/SMS4EMI06G/01) separately confirms Eco 0.645 kWh, 9 L, 3:35 and 14 place settings. No inferred cleaning score on this machine.

Source B: [Which?, 2026-01-19, main vs quick vs eco](https://www.which.co.uk/news/article/main-vs-quick-vs-eco-wash-which-dishwasher-program-is-the-best-akubJ2t3A6gi), examined exact report. **2024 snapshot on three other big-brand machines**, not the above Bosch. Average cleaning main **83%**, eco **79%**, quick **74%**; drying main **82%**, eco **76%**, quick **76%**. Illustrative annual *electricity* costs at five washes weekly, UK Jan-2026 tariff 27.69 p/kWh: main **£71.01**, eco **£52.13**, quick **£73.93**. **Not extrapolated as Bosch cost or Bosch cleaning score**. Which? prose describing quick as the most water-intensive appears inconsistent with its own reported rounded water figures; avoid categorical water comparison from that report.

Source C (mechanism): model-specific [SMS4EMI06G usage manual](https://s3-eu-west-1.amazonaws.com/media.markselectrical.co.uk/manuals/SMS4EMI06G.pdf), program descriptions Eco lower-temp/longer soaking, Express higher-temp/time-optimised, Silence quiet. Not a second-by-second wattage measurement; don't claim exact pump/heater phases as observed in this model.

**Independent calculations, not source measurements:**
- Extra Express electricity: 1.300 - 0.645 = **0.655 kWh/cycle** (Express/Eco ~2.0155).
- Water: 10.5 - 9.0 = **1.5 L/cycle**.
- Time: 03:35 - 01:00 = **2h35m**.
- Hypothetical 20 cycles/month: Express 26.0 versus Eco 12.9 kWh, difference 13.1 kWh; at deliberately **illustrative** USD $0.25/kWh, **$3.275 ≈ $3.28**.
- At 240 cycles: 157.2 kWh, **$39.30** under same hypothetical tariff, **360 L** water. Excludes water charges, detergent, machine depreciation, actual settings/tariffs; no external currency exchange.
- Scenario 1 no deadline: choose Eco on stated energy/water objective. Scenario 2 clean plates needed within 75m: Eco cannot meet deadline, Express can **by nominal program length**; both outcomes are *modelled choices*, not recorded experiments.

## Audience and comparable public YouTube evidence

**Observation date 2026-11-20**, indexed metadata / search cards only. YouTube pages/tracks/transcripts/comments were **not** accessible for direct watching. Durations not confirmed; do not pretend otherwise. Different languages, production scales and ages mean this is context, not matched proof of demand.

| Video link / ID | Published; language / content | Observed metadata | Why relevant / baseline / counter |
|---|---|---|---|
| [ARD Marktcheck / WDR, xsv3wPC6BnU](https://www.youtube.com/watch?v=xsv3wPC6BnU) | 2026-05-10, DE, Eco vs Intensive household check | Indexed 293,801 views, 4,100 likes; channel ~819k followers | Strong preexisting subject/large media channel; no same-author age/format baseline confirmed, so no outperformance conclusion |
| [AmicaAGD dishwasher-program tutorial, DaM-ThMxr3Q](https://www.youtube.com/watch?v=DaM-ThMxr3Q) | 2025-05-06, product tutorial, EN metadata | Indexed ~536 views; channel ~11.2k followers | Other creator, but manufacturer help video rather than narrative; read only metadata. **Same-author same-day baseline:** [filter cleaning, 3jdtZkb1yQA](https://www.youtube.com/watch?v=3jdtZkb1yQA), indexed ~418 views; [reset, f2EVItUdUjI](https://www.youtube.com/watch?v=f2EVItUdUjI), ~737 views. These are tutorials, not viral-story benchmarks |
| [Spareka, a4lFJCq4qTA](https://www.youtube.com/watch?v=a4lFJCq4qTA) | 2022-08-04, FR appliance tutorial | Indexed ~16,281 views, duration unknown | Other creator and older evergreen; normal comparable baseline unavailable |

**Recency:** none of the above comparable videos are verified as published within the last 90 days (2026-08-22 to 2026-11-20). WDR May 2026 is ~six months old, so **not fresh 90d evidence**. Actual video durations, views at upload, ongoing growth, average-view baselines for WDR/Spareka, own-channel analytics, CTR, impressions, retention and Short stayed-to-watch are **UNVERIFIED**. Video headlines cannot count as viewing or content analysis.

**Real questions / community reactions, not performance measurement:**
- [2026-05-23 r/Appliances question: why does Eco appear idle and take longer?](https://www.reddit.com/r/Appliances/comments/1tl9qme/why_does_my_dishwasher_do_nothing_at_the_end_of/) Users dispute the eco benefit; one reports model-app numbers for *his own* machine, not our Bosch.
- [2026-05-15 r/NoStupidQuestions: “Do you use 1hr dishwasher cycle?”](https://www.reddit.com/r/NoStupidQuestions/comments/1tdk4za/do_you_use_1hr_dishwasher_cycle/) Some prefer overnight, others prioritise a short wash.
- [2026-08-01 r/AskBrits: “Does anyone use the different wash settings?”](https://www.reddit.com/r/AskBrits/comments/1vcgsv0/does_anyone_use_the_different_wash_settings_on/) Real preferences diverge; does not prove EN channel audience demand.
- [2026-02-04 r/Appliances: does Eco actually clean better?](https://www.reddit.com/r/Appliances/comments/1qw0aqx/does_eco_mode_for_dishwasher_clean_dishes_better/) Conflicting anecdotes; cannot turn into cleaning data.
- [2026-08-26 r/firstworldproblems: why a four-hour setting?](https://www.reddit.com/r/firstworldproblems/comments/1vz8big/why_does_my_dishwasher_have_a_setting_that_makes/) Indicates recognisable frustration, not measured conversion.

**Counterevidence:** The point is already explained by established videos and Which?; a 2026 German independent [ETM Gorenje report](https://etm-testmagazin.de/tests/die-gv6g63a60h-von-gorenje-im-test-2026/) reports different model/program dynamics. No universal "every quick cycle uses twice the energy" claim is justified. Content may feel informational rather than dramatic; 10m faces a serious repetition risk.

## Promise → first proof → payoff

- Audience: English-speaking people choosing their dishwasher program, zero prior appliance knowledge.
- Thumbnail promise (editorial, no image): same two actual dishwasher program labels, a **1:00** and **3:35** juxtaposition, question “WHICH COSTS MORE?” The answer is per-model electricity, not secret universal cleanliness.
- First visible proof: original Bosch table values on one machine; user must not be shown a forged physical meter reading. Graphical digits during future production require actual generated graphic assets per Two Ways visual profile, not programmatic text.
- Main twist: on one machine a quick cycle uses over twice the published kWh; second useful reveal: deadline changes practical winner, four-hour Silence doesn't conserve as well as 3:35 Eco.
- Payoff: conditional rule, explicitly limited to published energy/water and a declared time constraint. **Cleaning of exact pairing remains UNVERIFIED** and cannot be shown as a measured win.
- Actual next-video intro asset / clickable channel link **not yet selected or verified**; editor must not invent a real linked-video scene.

## Constraints / scope

No subscription, paid vidIQ, TTS, images, MP4, upload or posting. Git-only editorial queue; no registered `ytv start`, no independent reviewer. Long versions are editorial only until channel Long recipe exists. Source content is for fact checking; narrative language is original, not copied from any external video or article.
