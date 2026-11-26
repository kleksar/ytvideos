# Research: idle or restart at a safe pickup
Observed 2026-11-16. Original editorial research, not a field experiment or an official runtime result.

## Ten distinct concepts considered, then three finalists
First-pass conceptual screen: (1) parked engine idling vs one restart; (2) dishwasher vs handwashing; (3) debt snowball vs avalanche; (4) laundry now vs batch; (5) space-heater vs whole-house heat; (6) automatic vs fixed phone brightness; (7) fill a freezer vs leave empty; (8) shut off tap while brushing vs running tap; (9) pressure cooker vs conventional pot; (10) immediate grocery run vs larger planned trip. Only the first three received evidence screening; seven are ideas, not evidence-verified or YouTube-verified finalists.

| Finalist | Cold opening | Middle and full payoff | Strongest objection |
|---|---|---|---|
| Engine idle vs restart | My car is parked but still burning fuel | One 90-second comparison, a tiny dollar amount, reversal under a 5-second wait, safety exception for traffic | Two existing well-viewed Engineering Explained videos; demand for our angle is unmeasured |
| Dishwasher vs hand | Is the sink really using more water than a machine? | Same load, water and heating, meaning of "efficient"; full conditional comparison | Recent Which? research has already published the large difference; individual wash habits are incomparable without controlled data |
| Debt snowball vs avalanche | Which bill would I pay first? | Schedule, interest saving vs earlier visible win | Realistic amortization and behavioral claims need additional evidence; financial advice risk; years-old direct YouTube comparators |

Selected **idle vs restart** because it has a legitimately changing answer with wait duration and one surprising limitation: safely parked vs actively moving traffic. The rival dishwasher has a stronger topical consumer interest signal but a weaker new five-minute narrative. Debt is also a serious rival but a higher-stakes financial simulation. Strongest counterargument: the idle myth has already been explained by major automotive creators; avoid retelling their scripts.

## Actually observed audience signals; no invented metrics
- Engineering Explained: https://www.youtube.com/watch?v=dFImHhNwbJo — *Americans Have No Idea How Much Fuel Idling Uses*, 2018-09-05, EN automotive explainer, about 3.76m lifetime views on a third-party indexed crawl observed 2026-11-16; duration not verified. Independent 2018-09-05 contextual publication: https://www.roadandtrack.com/new-cars/car-technology/a22994303/automatic-start-stop-useful-fuel-savings/ .
- Engineering Explained: https://www.youtube.com/watch?v=2YCGnshLIuY — *Does Engine Idling Waste Fuel?*, 2024-03-29, EN automotive explainer, about 2.87m indexed lifetime views (NOT live YouTube); duration not verified. Both videos are the SAME AUTHOR and are not independent creator samples.
- Driving 4 Answers: https://www.youtube.com/watch?v=xnR1oj8crCU — *EVERYTHING on FUEL SAVING*, 2022-04-10, EN broader 24:13 fuel-saving video, ~265k indexed lifetime views. Different creator, but format and topic breadth are not matched.
- Same-creator ordinary baseline at comparable upload age, format and topic: UNVERIFIED. General channel index https://us.youtubers.me/engineering-explained/youtube-videos-stats provides mixed-age snapshots, not a valid control. No 30–90-day direct fresh video verified, no playback, full YouTube transcripts or YouTube comments accessed. These historical views do NOT prove CTR, retention, freshness, demand, or projected success for this adaptation.
- An actual public question on starter/battery wear: https://www.reddit.com/r/SubaruForester/comments/1l2jphc (2025-06-03; anecdote, NOT a YouTube reaction). https://thepublicsradio.org/episode/should-i-idle-my-car-or-stop-and-restart/ covers an audio listener question; not a YouTube transcript.
- Rival factual evidence: https://www.which.co.uk/news/article/which-research-reveals-how-little-water-dishwashers-use-compared-to-hand-washing-aUDng9Y2iK8E (published 2026-09-01); https://www.youtube.com/watch?v=jtgnRJKSJlw and https://www.youtube.com/watch?v=FmMaWQJTxds older debt-payoff examples. Rival YouTube engagement/baselines: UNVERIFIED.
- Proprietary channel analytics/vidIQ check unavailable in this run; no credits purchased or consumed. Demand for our particular format and story: **UNVERIFIED**.

## Fact sources actually read and material limitations
1. Argonne/Gaines et al., *Which Is Greener: Idle, or Stop and Restart?* (2012), pp. 1–2, inspected including both PDF page images: https://afdc.energy.gov/files/u/publication/which_is_greener.pdf . At 21°C one 2011 Ford Fusion 2.5 L tested; fuel break-even about 10 seconds, reported passenger car idle 0.2–0.5 US gal/hour. SINGLE car and small test, not universal, and pollutant comparisons vary.
2. US DOE AFDC, *Light-Duty Vehicle Idle Reduction Strategies*, Driver Behavior section, https://afdc.energy.gov/conserve/idle-reduction-light . Suggest engine off for predictable >10s **except in traffic**; automatic engineered start-stop differs from manually switching off mid-traffic.
3. DOE AFDC, *Idle Reduction Research and Development*, section Idling Versus Stopping and Restarting, https://afdc.energy.gov/conserve/idle-reduction-research .
4. 2022 environmental study of gasoline direct injection engines: https://pubmed.ncbi.nlm.nih.gov/35772619/ reports conditional particulate-emission increases at restarts despite fuel savings. Its measured percentages are NOT transferred to our gasoline model.

## Reproducible toy-model math; one starting state and metric
Warmed-up gasoline car, **parked safely**, no air conditioning/heating load, identical **90-second** wait and departure. Option A idle throughout, B engine off during wait and **one** warm restart. Fuel-only metric in millilitres; not real traffic time, all pollutant emissions, battery wear, maintenance or observed savings.

Assume idle **0.3 US gal/hour** inside Argonne range; assume restart uses amount equivalent to **10 seconds** at that rate. The ten-second restart amount is a modeling approximation informed by observed crossover, not a field measurement for this car. 1 US gallon = 3785.411784mL.

- A = 0.3 * 90/3600 = 0.0075 US gal = **28.3906mL**.
- B = 0.3 * 10/3600 = 0.000833333 US gal = **3.15451mL**.
- A minus B = **25.2361mL** saved per modeled stop, winner B in this scenario.
- 100 identical stops: A 2.83906L, B 0.315451L, saved **2.52361L**, equals 0.666667 US gal; at assumed **$3.50/US gal** (not asserted as current pump price), **$2.33**.
- Alter only wait: 5 seconds -> A uses less fuel by 1.5773mL; 20 seconds -> B saves 3.1545mL; 300 seconds -> B saves ~91.48mL. This sensitivity analysis is a clearly announced new condition, not a second real-world experiment.
- If idle rate 0.2–0.5 gal/h with same ten-second equivalence applied per car, 100 stops would save **1.68–4.21L**; not a confidence interval or a measurement.
- One-restart assumption is invalid when waiting in a stop-and-go queue; no model winner asserted for live traffic. Warm/cold engines and comfort loads vary.

Original self-written EN/RU texts; no external video language copied. No real footage, images, independent review, exact speech timing, registration or approvals.