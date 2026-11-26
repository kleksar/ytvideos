# Research — fixed carbon cost of a hand dryer

Observed **2026-11-21**. Channel: Two Ways Lab, English first-person and full Russian translation. Git-only editorial hypothesis, not a filmed or physical experiment; no video, transcript, audience comments or own YouTube Studio analytics actually accessed.

## Screening (12 different practical situations, not 12 thoroughly researched topics)

1. **Electric hand dryer vs paper towels** — FINALIST SELECTED. Familiar choice, hidden manufacturing versus visible waste, numerical study and fresh 2026 LCA, a conditional model reversal.
2. **40 socks: immediate matching vs color sorting first** — FINALIST. Reproducible comparison counts, but result sensitive to assumed arrangement; no matched video demand.
3. **One flexible phone and USB-C-only laptop: first-come chargers vs least-flexible first** — FINALIST. Can model two connectors and devices fairly, but the outcome arrives too quickly to support meaningful 5/10-minute variants.
4. **Electric kettle vs gas hob for one liter** — interesting energy/cost tradeoff, but neighboring #171 kettle-versus-microwave creates duplication risk, and tariff/efficiency inputs not sufficiently controlled.
5. **Single queue vs separate supermarket lines** — familiar, but multiple existing queue PRs; no distinct new reversal confirmed.
6. **Roll clothes vs fold into suitcase** — genuine problem, yet exact same-case fit requires unavailable comparable geometry measurements.
7. **Short congested route vs longer empty route** — conventional conditional timer; nearby queue/transport coverage.
8. **Cotton tote versus disposable bags** — covered by #329.
9. **Dishwasher versus hand washing** — covered by #303; Eco vs Express already #313.
10. **Thermostat setback versus constant heating** — covered by #317.
11. **Garden hose versus conveyor car wash** — covered by #338.
12. **Pressure washer rent versus buy** — covered by #335.

Actual remote all-state GitHub PR searches: hand dryer, paper towel, electric dryer, hand-drying, handdry, socks; no matching story-title hand-dryer PR returned, though some searches matched #329 via body. File-only duplicate search is not exhaustive. Most recently authored story PR observed #341 Paper; next channel under actual last-created rotation is Two Ways.

### Three pitches compared before writing

**A. Dryer versus towels (selected).** Opening: "I have two ways to dry my hands: a warm-air dryer or paper towels. Which one has the smaller carbon footprint?" Picture: same wet hands, cyan paper side and amber dryer side, neither outcome announced. Stay: manufacturing machine's fixed 113kg -> low-traffic A/B -> high-traffic rerun, all other inputs unchanged -> threshold and broad-LCA caveat. Payoff: partial-scope 5/day paper ~112 vs dryer ~130kg; 50/day paper ~1118 vs dryer ~286kg. Strongest objection: the partial *asymmetric* inventory cannot establish a total ecological winner, and no verified matched YouTube demand for this model angle.

**B. Socks (strongest simple visual alternative).** First line: "I have forty socks, and the sorting might take longer than finding the pairs." Same initial pile for both; method A searches matches one by one, method B groups colors first then pairs. Payoff is count of hand movements/comparisons and why distribution changes winner. Objection: entirely modeled sock arrangement and low viewer interest after first count; 5/10-minute story extension has no compelling verified new events or inputs.

**C. Charging devices (strongest very-short puzzle).** First line: "I have two chargers and two devices, but one wrong cable leaves my laptop dead." Phone compatible with either connector; laptop requires USB-C; A first-come, B least-flexible first. Two completed charges under B. Objection: all payoff emerges in two assignment choices, unproven 5/10-minute expansion without a different problem. All three have unverified audience demand; A wins on grounded causal development and a real current research disagreement between narrow model and full lifecycle results, not on visual ease.

## Opened primary / peer-reviewed sources and exact supported claims

**S1 — Coller, Schiavon, Ragazzi, Environmental and economic sustainability in public contexts: the impact of hand-drying options on waste management, carbon emissions and operating costs. Published 18 January 2021.**
https://link.springer.com/article/10.1007/s10668-020-01109-x
Read sections 2.3, 2.4 and 3.1–3.2, eqs 1–6, table descriptions. Paper describes *numerical simulated* restrooms with equivalent use, n=250 open days, modeled average three paper towels, 1600 W machine, 21 sec drying, five years. Cites manufacturing of dryer **113 kg CO2eq**, virgin paper towel **5.96 g CO2eq each** (both sourced to Montalbo et al 2011), historical EU2018 grid **296 g CO2eq/kWh**. Financial break-even **57 daily uses** is NOT the same metric as emissions. Broader paper scenarios include waste and transportation; not included in script's simplified internal tally.

**S2 — CE Delft, 2026 update of hand-drying systems LCA.**
https://cedelft.eu/publications/environmental-impact-of-hand-drying-systems-2026-life-cycle-assessment-update/
https://ce.nl/publicaties/milieu-impact-van-handdroogsystemen-update-levenscyclusanalyse-2026/
English landing page **October 2026**, Dutch original **September 2026**. English summary, actually read, finds electric hand dryers lowest **overall environmental impact** among evaluated systems, particularly modern low-power/short-time dryers on low-carbon power. Material and number of paper towels matter. Full report Dutch; not independently translated/read in full. Does NOT confirm the narrow quiet-room paper win.

**S3 — Joseph et al., 2015 peer-reviewed LCA abstract** https://pubmed.ncbi.nlm.nih.gov/25704267/
Conventional 1800 W, under 30 sec, versus TWO recycled unbleached 4g towels, Ontario 2010 power assumptions. Dryer favorable in three of four environmental impact categories. Different system from this script and abstract read only.

**S4 — Reynolds et al. hygiene literature review, online 2020** https://sfamjournals.onlinelibrary.wiley.com/doi/10.1111/jam.14796
23 included hygiene studies; 2 generally favor dryers, 7 towels, 9 mixed/not statistically significant, 5 non-direct comparisons; authors find insufficient support for a broad health superiority claim. Not evidence about greenhouse-gas emissions.

## Deterministic partial model — author recalculation (not observed emissions)

Same public restroom, five years, 250 open days/year = 1250 open days; every visit ends with equally dry hands (physical equivalence UNVERIFIED). Paper A: 3 virgin towels each, 5.96g manufacturing each =17.88g per visit. Dryer B: one machine, 113000g manufacturing; 1.6kW * 21sec / 3600 =0.0093333 kWh/visit; at historical 296g/kWh =2.762667g/visit of electricity.

If N visits per open day:
- **Paper partial kg = (1250 N *17.88)/1000 = 22.35 N**.
- **Dryer partial kg = 113 + (1250 N *2.7626667)/1000 = 113 + 3.4533333 N**.
- At N=5: paper 111.75 kg; dryer 130.2667 kg, so paper lower by 18.5167 kg *in this partial tally*.
- At N=50: paper 1117.5 kg; dryer 285.6667 kg, so dryer lower by 831.8333 kg *in this partial tally*.
- Crossover 113/(22.35-3.4533333)=**5.9799 uses/day**. If only 2 towels, paper=14.9 N and crossover **9.8719 uses/day**.

**BOUNDARY WARNING:** paper-side excludes waste treatment/transport; dryer side excludes standby, repair, etc. These are not equal full life-cycle inventories. None of the quoted model kg values can be called the verified *total* environmental impact for a real restroom. Physical equivalent drying quality not measured. Carbon vs finance vs hygiene are three distinct metrics.

## Public comparable YouTube metadata — search results only

Search date 2026-11-21, pages/titles/metadata indexed, NO watching or transcript/comment analysis and no own analytics.
- **Dr Karl**, "Hand Dryer VS Paper Towels - Which is Better for the Environment?", EN, published 2025-04-12: https://www.youtube.com/watch?v=9WTHkZmomCg ; indexed 4529 views/48 likes at crawl ~6mo earlier, **duration UNVERIFIED**, related environmental question. Matched creator baseline UNVERIFIED.
- **Scienced**, "The Hand Dryer vs Paper Towel Myth", EN Short, published 2025-04-25: https://www.youtube.com/watch?v=kmmAkBi84FE ; indexed 12,697,346 views at crawl ~11mo earlier; **hygiene** instead of carbon and may be a huge creator/outlier effect. NOT evidence of this proposed video's demand. Same-author comparable baseline UNVERIFIED.
- **Life Cycle Thinking & Environmental Management**, "Life cycle assessment (LCA) of paper towel", EN educational, published 2020-11-24: https://www.youtube.com/watch?v=M6QE1hI-aJQ ; indexed 1506 views/58 likes at crawl ~2mo ago; paper-only, not exact matched format. Baseline UNVERIFIED.
- **Jennifer Hudson Show**, "Something's Gotta Go: Paper Towels or Hand Dryer?", EN entertainment, published 2023-01-31: https://www.youtube.com/watch?v=ZBKeshV9l7U ; indexed 49,411 views at crawl ~4mo ago; celebrity entertainment not science-format baseline.

Strong signal for viewer interest NOT established; no two-to-four truly matched videos with known same-creator usual results. Recent 30–90-day audience demand, viewer questions/comments, actual durations/views now, CTR, retention, views/hour and our own channel fit **UNVERIFIED**. CE Delft's 2026 research freshness does not measure YouTube demand. vidIQ balance checked **zero credits** on 2026-11-21; paid YouTube search/comments not called.

## Story constraints and copyright

Narrator says "I/я"; model not live physical test, metric before selection, concrete A/B before result, change only N from 5 to 50 per day; a clean full payoff and why it happens. On-screen art uses Two Ways brand, NOT Paper diorama, no invented source photos or report charts. All cited studies are paraphrased, original tables/images not copied. No unsupported medical conclusions. No brand-name machine claimed to be personally used. Full LCA broader evidence explicitly contrasts narrow numerical example.
