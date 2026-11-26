# Fan near the window vs deeper inside — research
Observed 2026-11-26. Source main 7c779c4b2fd379c85166ae1b164fa53d1ea08843; #124 merged. English audience, ordinary household cooling, experimental demand hypothesis.

## Selection
Actual broad scan, not eight completed studies:
| Candidate | Potential | Constraint |
|---|---|---|
| Fan distance from one window | Same appliance, visible reversal: mixing vs cooling | CFD only; no guarantee |
| Wireless vs cable charging | Convenience vs electricity and standby | Small annual household gain, setup-specific |
| Laundry dehumidifier alone vs with fan | Time until dry, added fan can save hours | Manufacturer-sponsored tests; room and end condition |
| Fridge door vs shelf | Temperature and food storage | Survey, not matched A/B; avoid safety overclaim |
| Pot temperature shelf/location | Different local temperatures | Single apparatus, weak audience evidence |
| Dish towel vs air dry | Contamination transfer | Different endpoint from prior sponge/brush but adjacent; avoid |
| Extra spin before drying | Residual water and drying cost | Incomplete paired inputs |
| Cold vs warm wash | Energy vs washing result | Need matched cleaning endpoint |

Finalists:
1. Fan — opening: “I can put my fan one metre from the window or five metres back.” Same outward direction and height, window-only reference, flow returns near facade, then endpoint 24.43 vs 26.07. Counter: this does not compare against flush-mounted or inward fans, only two placements in a single CFD case. Wins on no new purchase and intelligible spatial mechanism. 
2. Wireless charging — opening: “I can plug in the same phone or leave it on a charging pad.” Compare wall energy to full, then separate standby. iFixit 2024 test reports 18.25 and 23.33 Wh (difference 5.08 Wh; own arithmetic 27.8% of wired baseline, not the source's percentage). https://www.ifixit.com/News/94409/wireless-charging-trading-efficiency-for-convenience . Follow-up 2026 https://www.engadget.com/2200186/wireless-charging-wastes-electricity-why/ . Biggest objection: cost at phone scale is low; different hardware and denominator errors; no matched audience sample. Strongest competing angle is laundry, which offers tangible hours saved rather than small bills.
3. Laundry — opening: “My shirts are still wet. Do I add a fan to the dehumidifier?” Same 13 shirts, rinse/spin and room in reported manufacturer test; desiccant setup 4h25 vs 1h40 with fan, 2h45 difference. https://www.meaco.com/pages/dry-laundry-fast-meaco-experiment . Biggest objection: commercial source, not laboratory conditions, residual water/end-point and humidity comparability need examination. Viewer question https://www.reddit.com/r/Dehumidifiers/comments/1hbt91a (Dec 2024, asks why drying takes over 6 hours); Meaco videos https://www.youtube.com/watch?v=a5_SaJEotLU (2023-05-18, 58,672 indexed views), https://www.youtube.com/watch?v=epIDY-3X91k (2023-04-27, 9,268); second author Sassito https://www.youtube.com/watch?v=bKDcWHHsfwA (2025-09-20, 35,027 indexed views, Short, no controlled comparison). No representative matched baseline. Sponsor bias outweighs otherwise stronger practical payoff. 
Remaining exploratory leads: https://journals.asm.org/doi/10.1128/AEM.02430-09 ; https://www.mdpi.com/2076-3417/16/23/11675 ; https://pubmed.ncbi.nlm.nih.gov/12878380/ ; https://partners.gorenje.com/fts/htmlNavidila/964247en.html . Not used as established script facts.

## Audience observation — UNVERIFIED
Public indexed metadata observed 2026-11-26, not actual real-time view counts or videos watched. No transcripts or YouTube comments obtained.
| Video | Date | Indexed views | Format/language/duration | Relevance |
|---|---|---:|---|---|
| [Matthias random stuff](https://www.youtube.com/watch?v=1L2ef1CP-yw) | 2021-06-30 | 11,468,365 | EN Long ~6:28 | Air movement between rooms, not same thermal setup |
| [Entdecker-Lab](https://www.youtube.com/watch?v=NsTA1fjC3kg) | 2026-06-27 | 94,887 | language/duration unverified; German channel | Two opposite windows, different geometry |
| [Window fan setup](https://www.youtube.com/watch?v=wtCKo5LwnhA) | 2016-08-07 | 197,515 | duration/language not verified | adjacent setup, no matched temperature trial |
| [Same author Matthias — fan balance](https://www.youtube.com/watch?v=moo95i_6QZs) | 2021-06-07 | 392,397 | ~2:21, EN | selected popular listing, not ordinary baseline |
| [Same author Matthias — heater repair](https://www.youtube.com/watch?v=DI80FQDZBKw) | 2020-04-16 | 431,684 | ~6:14, EN | similar duration but repair, popular listing bias |

Cannot infer relative typical performance, CTR, retention, growth or today's demand. Neither representative baseline nor second author baseline available. Older questions indicate evergreen confusion: https://www.reddit.com/r/explainlikeimfive/comments/141oprv/eli5_with_bernoullis_principle_in_mind_i_think/ (2023-06-05, asks about optimum distance and single-window basement); https://www.reddit.com/r/explainlikeimfive/comments/1h61opk (2024-12-03, direction); counter-signals https://www.reddit.com/r/NoStupidQuestions/comments/vkbq8l (2022-06-25, sealed vs set-back) and https://www.reddit.com/r/fans/comments/1u5w162/am_i_doing_this_correct_fan_positioning_in_windows/ (2026-06-14, two-fan setup and wind). No verified 30–90-day fan-placement trend. Wireless alternative matched videos/comments not obtained. No paid credits.

## Claim mapping
Primary case study: https://www.sil3x.fr/en_GB/articles/simulation-thermique-aeraulique-cfd-appartement ; French mirror https://www.sil3x.fr/articles/simulation-thermique-aeraulique-cfd-appartement . Read geometry/method, Table 2, Tables 3–4, Figures 5–11, discussion and limitations. Reconfirmed numerical endpoints via indexed full result and French result on 2026-11-26; direct EN re-open timed out on repeat.
- Code_Saturne 3D numerical case; 8×3.5×3 m, one 1.4×1.4 m window, internal partitions, outdoor potential temperature 22°C, initialized around 30°C; facade flow ~0.9 m/s. First recorded values at 10 s differ; don't say they are equal or use them for causal baseline. Fan 30 cm model pressure curve, not resolved blades. Same mesh/settings; A coordinates (1,2.5,2.45) and B (5,2.5,2.45), same orientation extracting; duration 3600 s. Low near (1,2.5,1.75).
- Table 4: A 24.43, B 26.07, low 24.85, no fan 26.68. Subtractions calculated from displayed endpoints: 1.64; 2.25; 0.61; height 0.42. Source prose 2.26 from underlying rounding; not used as exact subtraction. 2/5m narration rounds to one decimal; 10m keeps precision.
- Table 3 no fan average 26.90 at 15 min, 26.72 at 30, 26.68 at 60; final bottom window probe 26.42 and upper room 27.50. No pure calm natural convection claim. Rapid initial cooling and slower later, warm walls, mixing vs cooling and return flow: Figures 5–11 and limitations.
- No passive tracer/air age, no documented mesh convergence, no physical replication or independently verified CFD. Mass-balance explanation and proposed home temperature test are general reasoning, not observed events. Do not infer effective air change from net/gross opening flow. No inward, flush or second-window comparison; no universal optimum. Personal comfort and safety not measured.
- Model.json contains reported endpoints and reproducible arithmetic only; not a new CFD run. All narration original paraphrase/own explanation. Rights to use source graphics not established; do not copy them.

## Duplicates and owner decisions
Actual 441 PRs via paginated all-state listing, newest #441 Nuviko open Draft → Two Ways next. No same fan-distance title; adjacent #320 car AC/open windows, #317/#195 heating, #359 router location, #439 onion and #436 sponge. GitHub issue search returned empty; releases endpoint empty (not equivalent to published YouTube). Main channel videos E001–006 (checkout, socks, carrying, toast, ribbons, parking). Publication queue dated 2026-11-12, live archive/analytics UNVERIFIED. #13 and #88 rejected, #20/#25 exact accepted reference revisions read, #46 accepted source protected. No modification of any existing PR or release.
