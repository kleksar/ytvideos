# Research — same battery, two electricity bills

Observed 2026-11-27. Source main 7c779c4b2fd379c85166ae1b164fa53d1ea08843; #124 merged 2026-11-16, canonical main applies. Latest actual draft #462 (Nuviko), #461 Paper, #460 Two Ways. Searched all-state title results for Two Ways (including unrelated hits), and targeted all-state PR/Issue searches for wireless charging, MagSafe, handwashing and cold laundry. No wireless charging match in those searches; not proof against unseen titles/content. Adjacent exclusions: #379 standby smart plug, #332 OLED, #400 EV charging, #430 egg start, #427 stove-off spaghetti, #451 lid on/off, #445 toothbrush, #342 hand dryer, #448 dryer spin. No reuse of those concepts. #460 and #457 progress comments read: existing drafts protected. Publication queue lists E001–E006 (checkout, socks, carrying, toast, ribbons, parking); dated 12 Nov, live state and own analytics UNVERIFIED.

## Selection
Ten distinct directions considered at triage; depth is unequal by design. Three finalists received free web evidence. No paid credits.

| Direction | Triage |
|---|---|
| Cable vs magnetic pad | Finalist: same battery, hidden idle draw, large relative change vs small actual bill |
| Cold vs warm handwashing | Finalist: common assumption, published controlled studies; not a sterilization promise |
| Cold vs warm laundry | Finalist: direct household choice; detergent and stain type limit comparability |
| More vs less pasta water | Adjacent #427 and #451; avoid similar kitchen energy treatment |
| Paper vs metal coffee filter | #460 overlaps |
| Dryer spin setting | #448 overlaps |
| Brush vs sponge | #436 overlaps |
| Phone dark vs light screen | #332 overlaps |
| Hand dryer vs paper | #342 overlaps |
| Overnight standby smart plug | #379 overlaps; no additional general standby story |

Finalist A (charging): first line “Cable or charging pad, my phone says one hundred percent.” Two identical full screens and wall meters. After charge, both remain connected; empty wireless pad adds a third accounting period. Payoff: percentage difference translates to surprisingly small individual annual cost, with practical choices. Strong objection: familiar efficiency conclusion, and source is a repair-site commercial test, not a blinded independent replication. The money reframe answers a real question rather than just repeating a teardown.

Finalist B (handwashing): “I have soap and two taps. Does the warm one actually remove more bacteria?” Same soap, different water temperature; no significant difference in tested bacteria. Primary Jensen et al., J Food Prot 2017, PMID 28504614, https://pubmed.ncbi.nlm.nih.gov/28504614/ (abstract); 2024 study https://journals.publisso.de/en/journals/hic/volume19/dgkh000527 (plain-water rinsing, not interchangeable with soap). Audience: everyday hygiene. Objection: easy to overstate into health advice; exact 2017 temperature-specific numerical table not obtained, answer mostly one sentence. Strong contender but weaker development than overnight accounting.

Finalist C (laundry): “I have two identical dirty shirts. Which wash leaves less stain?” Temperature, stain type and detergent performance could change the answer. Source https://onlinelibrary.wiley.com/doi/abs/10.1177/1077727X07308159 (cold-water detergent and one soil, not A/B temperatures); https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1470-6431.1989.tb00005.x (disinfection, not visual stain removal). Objection: comparable exact stain-removal endpoint across temperatures not obtained; no honest numerical winner. Reject this angle until matched data.

Winner: cable vs magnetic pad. It has two separate real comparisons within one goal (charge to full, then whole day), an explicit counterfactual habit, and an absolute-cost payoff. Not proof of virality. Handwashing is strongest alternative.

## Source ledger
S1: iFixit, Shahram Mokhtari with Chayton Ritter and Arthur Shi, 18 Apr 2024, https://www.ifixit.com/News/94409/wireless-charging-trading-efficiency-for-convenience, opened and read 27 Nov 2026. “The Baseline” and “Candidate One”: same iPhone 15 Pro, iFixit 65W adapter, same test equipment, mains meter; wired 130 min, 18.25 Wh, peak ~20 W at 30%, nominal battery 12.7 Wh; MagSafe 23.33 Wh; after full wired ~1.1 W for 4h50, magnetic ~1.5 W for 4h55, empty magnetic ~0.2 W. Reported modeled daily totals 23.6 / 34.13 Wh. Nonmagnetic off-center case 33.93 Wh and nearly four hours. Source acknowledges uncontrolled room temperature and non-laboratory conditions. Recompute percentage from Wh, do not reproduce inconsistent reported percentage labels (23.33/18.25−1 is 27.84%, not 24.4%). Do not call rated capacity measured stored energy. Source's headline and language not copied. No claimed lifetime test. The setup is not a new experiment by channel.

S2: https://www.allion.com/the-new-era-of-unlimited-battery-charging-technology-allion-wired-wireless-charging-test-evaluation-report/ — historical context only; old hardware and unclear energy unit wording, excluded from calculations. S3: https://www.engadget.com/2200186/wireless-charging-wastes-electricity-why/ (June 2026 article) secondary discussion outside 90-day recent-interest window; not a new independent test. S4: https://circuitrywired.com/qi2-wireless-charging (indexed about 2 months before access, secondary discussion, no audience metrics). Evergreen vs current demand separated.

## Reproduction and limits
See model.json. Use rounded reported daily totals, not a purported 24h meter measurement. 5.08 Wh extra to full; 10.53 Wh/day modeled extra; 10.53×365/1000=3.84345 kWh; at arbitrary $0.30/kWh, $1.153035/year. At $0.15/$0.60, $0.5765/$2.3061. Morning power-off: 30.73−23.6=7.13 Wh/day. Both immediately disconnect after charge: 5.08 Wh per full charge. No extrapolation to partial charging, no absolute tariff claim, no battery replacement prediction, no conflating a different nonmagnetic pad with an isolated placement test. 100% charge assumed in all versions; disabled adaptive behavior is a source scenario assumption, not advice to change settings. Actual runtime, meter accuracy and repetition not verified. Two branches same endpoint and 7h window; sensitivity explicitly separate.

## Audience evidence — observed 2026-11-27
Indexed YouTube metadata, not watched video, transcript or live views. Language inferred from descriptions where applicable; exact durations unavailable except chapter lower bounds. No CTR/retention inference.

| Video | Published | Indexed views | Format/language |
|---|---|---:|---|
| https://www.youtube.com/watch?v=vhKVuT8-H1g iFixit | 2024-04-18 | 1,251,877 | EN regular, last chapter 3:55, exact duration unknown; same source as test |
| https://www.youtube.com/watch?v=lYKqxdpVtvE iFixit | 2024-04-23 | 23,529 | EN short-like clip, format/duration unverified |
| https://www.youtube.com/watch?v=PwRunhVvIvQ Tools. Electro. DIY | 2022-08-31 | 106,488 | EN metadata, regular comparison, last chapter 8:04; portable power bank different setup |
| https://www.youtube.com/watch?v=dX6DT7gNogE Dion Schuddeboom | 2018-08-24 | 24,832 | EN metadata, format/duration unverified; older device |
| https://www.youtube.com/watch?v=tCG0_kznsyU Lorraine (handwash) | 2017-11-13 | 1,008 | EN metadata, format/duration unknown |
| https://www.youtube.com/watch?v=_hGTMJppk1U Tide (laundry) | 2025-04-24 | 6,635 | EN metadata, format/duration unknown, branded |
| https://www.youtube.com/watch?v=ugdjlZ5O-XU Discover Petrosains (laundry) | 2026-02-24 | 416 | EN metadata, format/duration unknown |

Baseline attempts: same-author iFixit 2024 battery https://www.youtube.com/watch?v=ktxiDa489ro (2024-09-24, 254843 indexed views) and teardown https://www.youtube.com/watch?v=Enz628JJ9Xg (2024-09-26, 158443); unknown durations/format and different product-news topics make them unsuitable as a defensible comparable baseline. Tools/Dion baseline unavailable. Direct watch-page fetch failed. No verified recent 30–90 day YouTube view trajectory. Demand UNVERIFIED, experimental editorial hypothesis only.

Actual audience questions: https://www.reddit.com/r/MagSafe/comments/oe2j5w (2021-07-05, user asks about electricity bill with unused plugged-in pad); https://www.reddit.com/r/iphone15/comments/16yk6ht (2023-10-03, questions distinction between input and received watts); S1 comment Nick Onorato 2024-04-18 notes small absolute cost and connector wear; Scott 2024-04-20 asks about intermittent top-ups instead of full charges. These directly motivated the annual-cost and routine limits. They are not representative surveys. YouTube comments inaccessible. No fabricated audience signals.

## Packaging/causal map
Same two choices → measured full-charge difference → sleeping past full → empty pad draws → annual conversion reframes stakes. Promise: compare whole-day electricity and actual cost, not charging speed or battery longevity. Separate 5m expansion explains W vs Wh and coils; 10m adds denominator, alternative routines and repeatable measurement design, with weaker pacing. No reference media acquired. Related-video target may be #379 only after actual published status, rights and intro available; no fictitious live related link or extra tail.
