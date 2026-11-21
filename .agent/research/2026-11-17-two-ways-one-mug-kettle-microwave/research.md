# Research & selection — one mug: kettle vs microwave

**Observed:** 2026-11-17. **Channel:** Two Ways Lab. **Remote policy:** merged main at initial preflight `247ebe9245091972c5a93ecb84ce55ad8c15a211`; #124 is **merged** (2026-11-16), so no proposed policy is substituted for main. Public searches were generic and revealed no private repo details. No purchased credits, provider renders or channel analytics.

## Selection, not a quota

Screened ten genuinely different everyday A/B decisions. These are **screened ideas**, not ten researched finalist proofs: (1) kettle vs microwave for one mug (chosen); (2) stairs vs elevator when a lift is delayed; (3) shopping-list order vs mapped aisle route; (4) batch cooking two dinners vs sequential cooking; (5) one shared queue vs two service queues (**overlap with existing checkout pilot, excluded**); (6) packing by weight vs by shape; (7) folding group-photo combinations by guest list vs minimizing movements; (8) towels air-dry vs tumble-dry; (9) cold vs warm wash for stains; (10) electric heater vs heat pump under a fixed heat demand. Already queued zipper merge #148, idling #157, gift wrapping #162 and dishwashing #168 excluded from new-work selection. Model feasibility, mass comprehension, distinctive payoff, factual constraints and overlap were screened before scripting.

| Finalist | Stop / first spoken line | What changes after the hook? | Earned payoff | Strongest objection |
|---|---|---|---|---|
| **One mug, kettle or microwave — selected** | “One mug of hot water. That's all I want this morning.” Visible kettle's 500 mL MIN beside a 250 mL mug | At equal 250 mL the kettle wins on assumed energy efficiency; because minimum fill is 500 mL the less-efficient microwave wins, then a lower-minimum kettle flips it back | Check **actual volume and safety limits**, not wattage or appliance slogan. At model efficiency 0.8/0.6: B 38.8 Wh vs A 58.1 Wh; lower minimum 250 mL makes A 29.1 Wh | Existing explainers, small public view counts, safety concern for microwaved water and model assumptions. No measured video demand for this particular delivery |
| **Shopping route: list order vs aisles** | “I bought six things. Why did I walk past the same shelf three times?” Exact fixed shelf map, entry/checkout | Route length can be computed; a late cold-item constraint can alter the optimum | Organise a known store route while respecting the refrigerated-last requirement | Requires trustworthy actual store layout and cold-chain caveats. Same-category nearby checkout/parking content; no adequate directly comparable YouTube baseline verified in this run |
| **Stairs vs elevator** | “The elevator is still upstairs. Do I wait or start climbing?” Same arrival/start/end floor | The lift's wait and stair speed form a break-even threshold; accessibility/capacity alter who can choose | Decision conditioned on wait and mobility; no universal stopwatch winner | A/B physical ability and accessibility are inherently different; no grounded matching real elevators/stair timings, and the model can look rigged |

**Strongest alternative:** mapped grocery route, more broadly useful across many purchases, but with weaker direct A/B audiovisual evidence and hidden actual-store constraints. The kettle's **exact visible reversal at the manufacturer's minimum** gives a cleaner first image, preannounced electricity metric and reproducible model. Winner selected as an editorial experiment, not a measured 9/10 YouTube opportunity. Source video counts below are modest counter-signals.

## Model declared before any winner

Same need: **250 mL useful water**. Start 20 °C; theoretical target 100 °C in a mathematical heating model, 80 K rise. Not an instruction to microwave plain water or a performed heating trial. `c = 4.186 kJ/(kg·K)`, density approximated 1 kg/L. Useful heat `Q = V_L × 93.022 Wh/L`. Illustrative fixed **water-heating** efficiencies `eta_A = 0.80`, `eta_B = 0.60`; they are **not measured efficiencies** for the pictured or an owned machine. Electrical energy `E = Q/eta`. Model is intentionally simple: no separate warm-up, cup absorption, standby, cooling, automatic shutoff or steam loss; real results may differ. The metric is **Wh taken from wall per useful task**.

| Case | A kettle fill, eta .80 | B microwave fill, eta .60 | Calculated Wh | Outcome |
|---|---|---|---|---|
| 1 mug, kettle MIN=500 mL | 500 mL | 250 mL | A 58.14 / B 38.76 | B by 19.38 Wh |
| Same mug, kettle permits MIN=250 mL | 250 mL | 250 mL | A 29.07 / B 38.76 | A by 9.69 Wh |
| Two 250 mL mugs, original MIN | 500 mL | 500 mL | A 58.14 / B 77.52 | A by 19.38 Wh |
| Sensitivity: MIN=300 mL | 300 mL | 250 mL | A 34.88 / B 38.76 | A |
| Sensitivity: MIN=400 mL | 400 mL | 250 mL | A 46.51 / B 38.76 | B |

Break-even kettle fill for one-mug B `V_A = 0.25 × eta_A / eta_B = 0.3333 L` **in this constant-efficiency model only**. If eta_A=.70 and eta_B=.60, threshold ≈.292 L. Source literature supports overfill/minimum-fill as meaningful, **not** these illustrative eta values. At illustrative $0.25/kWh, 19.38Wh costs $0.004845 per occurrence; repeated once daily 365 days is ~$1.77, not a prediction. Both countries' currency conventions are merely math units.

## Factual sources and exact scope (accessed 2026-11-17)

1. [Energy Saving Trust — “Avoid these seven common mistakes that waste energy”](https://energysavingtrust.org.uk/energy-mistakes-to-avoid/), section **“Filling the kettle every time you want a cuppa”**: unnecessary water costs energy; many kettles have a **minimum of around 500 mL**, more than one standard mug. A general statement, not a certification of a particular product. Evergreen, page date not independently verified.
2. [Philips manufacturer instructions](https://www.documents.philips.com/assets/20210512/dcdce46a3ccf4e2aad97ad260118fe24.pdf), safety instruction **minimum fill**: under-minimum volumes differ across flat-element, spiral and metal models; exact values depend on device/indicator. Manufacturer's manual, do not assume all have 500 mL.
3. [Eldom C415 manual](https://www.notice-facile.com/en/manual/627122/eldom%2Blimea-c415), English **Technical data** and capacity instructions: model C415 permits 0.5–1.7 L; establishes an actual 0.5 L example but does not claim we own/test it.
4. [Durand et al., Fraunhofer/Swedish Energy Agency, *Sustainability*, 2022](https://www.mdpi.com/2071-1050/14/20/12963), abstract and §4.1: user-related factors, heating excess water and low-minimum indicator (e.g. 0.25 L) offer savings; no universal 80/60-percent efficiencies are taken from this work.
5. [US FDA — “Microwave Ovens”](https://www.fda.gov/radiation-emitting-products/resources-you-radiation-emitting-products/microwave-ovens), **“Avoiding Injuries from Super-Heated Water”**: plain water heated alone in microwave can be superheated and erupt when disturbed; observe manual's precautions and times. **Do not recommend overheating plain water.**
6. [Energy Saving Trust — “Home appliances and energy efficiency ratings”](https://energysavingtrust.org.uk/advice/home-appliances), **Kettles**: avoid overfilling; guidance cites a 2021 UK government survey and potential household savings. Not a measured result for our comparison.
7. `4.186 kJ/kg/K` heat capacity and kJ/Wh factor 3.6 are standard elementary physics constants; the model's Q and threshold are explicitly **original arithmetic**. Difference between appliance input watts and energy Wh explained as model definitions. No appliance-specific 80/60 measurement was found.

**Safety blocker for physical follow-up:** no exact manufacturer manuals, compatible meter, experimental setup or safety approval; do not film a real microwave water boil based on this model. It is an illustrated conditional calculation.

## Public audience / YouTube comparators — search evidence, not viewing

Observation date **2026-11-17**. Search engine supplied accessible **YouTube page title/description/metadata**, not playback, comments, independent retention data or transcripts. All three videos are English-language energy experiment/explainer *Long*, **not** illustrations/Shorts; comparator mismatch is material.

| Author · URL · ID | Publication (observed) | Observable | Limit / counter-signal |
|---|---|---|---|
| [Energy Myths — “Microwave? Kettle? Hob? Which is cheaper to boil water?”](https://www.youtube.com/watch?v=8_cDsVlnmcs), `8_cDsVlnmcs` | **2022-09-13** | Search index: **3,608 views**, 53 followers, 89 likes; duration UNVERIFIED; channel says measured water | Small audience/no clear breakthrough; other same-author comparable uploads **UNVERIFIED** |
| [Your Energy Answers — “Most Energy Efficient Way to Boil Water”](https://www.youtube.com/watch?v=XMpC6tbrERM), `XMpC6tbrERM` | **2024-02-25** | Search index: **7,320 views**, ~52,100 followers, 194 likes; chapter markers 0:00–5:08, actual full duration UNVERIFIED | Low views relative to known channel followers is a **counter-signal**, not a legitimate retention or CTR calculation; same-author typical 2024 Long baseline UNVERIFIED |
| [Portland General Electric — Switch Labs, Episode 3 “Boiling Over”](https://portlandgeneral.com/energy-savings-videos), embedded [YouTube ID `z69qRjUWG-g`](https://www.youtube.com/watch?v=z69qRjUWG-g) | publisher describes older **2013** series; precise YouTube publication date UNVERIFIED | Publisher's own text: comparison of mug vs kettle quantities, electric vs stove vs microwave; `youtube.com/embed/z69qRjUWG-g` extracted from its iframe | Direct YouTube fetch **throttled**, no views/subscribers/duration/comments or footage confirmed; not counted as viewed video |

**Baselines:** relevant same-author typical-upload results, matched upload ages/formats and actual viewers' comments **UNVERIFIED** after free search. PGE's “this was the question you asked most” is the publisher's statement, not accessible raw questions. No accessible own YouTube Analytics/CTR/retention or fresh 30–90-day matching video signal. Evergreen interest supported, current demand **UNVERIFIED**; published source freshness is not YouTube growth. The two observed YouTube view counts should lower confidence rather than be inflated into a viral claim. vidIQ charges not invoked; no quota inference.

## Exact hook, escalation, payoff and risk

- Stop: one mug vs visible **half-litre minimum mark**. The audience can infer a conflict without knowing electrical engineering.
- Stay: fixed **same task and metric**, first B wins (39 vs 58), then lower-minimum A wins (29 vs 39); optional two-mug A win makes the mechanism causal rather than a memorised number.
- Payoff: choose by actual safe minimum and needed volume; model thresholds don't generalize, safety overrides marginal savings.
- Main objection: A and B heat different *total* volumes. This is **intentional for comparing the same useful one-mug output under mandatory minimum-fill constraints**, not a comparison of equal full appliance loads. All alternatives spelled out.
- Rights: original narration and abstract illustrated calculations; no copying footage, author text or brand assets. Real brand visuals, character sheets and typography unavailable, production rights check still UNVERIFIED.
