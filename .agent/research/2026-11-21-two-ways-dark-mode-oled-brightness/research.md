# Research — Two Ways Lab: Dark Mode or Light Mode?

Observed 2026-11-21 (Europe/Belgrade). Editorial-only Git queue; no official ytv run, no owner approval, no playback or measurement. EN master is original narration, not a translation of another creator's text. **Primary discovery constraint:** vidIQ balance check returned 0 available credits; paid YouTube search/comments/channel baselines deliberately NOT called. Free public web research performed; fresh 30–90d matched EN Two Ways Shorts demand **UNVERIFIED**.

## Audience, hypothesis and promise

Ordinary smartphone user who has heard "dark mode saves battery" but may not know screen technology. Interest: phone dying during the day; choice of a setting already available, with a large condition-dependent change in magnitude. Hypothesis, not demonstrated CTR or retention. One unchanged task and OLED device, A = light UI, B = dark UI; **metric total phone power at equal screen brightness**. Distinguish absolute power, percentage of phone power, OLED panel power and day-long battery life. No made-up user measurement: all percentages are explicitly from published researchers, and two distinct published methodologies are never mixed or averaged.

Precise first sentence (02m): "Will dark mode save my phone's battery?" Initial frame idea: same illustrative phone/task, interface A light left/B dark right; settings and brightness identical, no invented meter readout. Progression: dark should dominate -> 3–9% at indoor brightness -> 39–47% at 100% OLED brightness -> LCD and different apps limit generality. Payoff: OLED/high brightness more compelling; indoors comfort and brightness matter. Strong objection: evergreen question answered by large 2019 channels; novelty is conditional contextual reversal, not a new discovery. Long 10m is more explanatory than dramatic; lower independent verdict permitted.

## Broad selection; genuine candidates, not PR-filler

Eleven distinct everyday A/B ideas checked against current repo PR inventory, feasibility of evidence and watch/payoff mechanism:

| Idea | Editorial discovery status and real objection |
|---|---|
| OLED light/dark interface at different brightness | **Finalist/selected:** Purdue direct-source multi-device comparison and Mobile Enerlytics task-specific evidence; clear conditional swing, public old videos; high familiarity |
| Wi-Fi versus mobile network while browsing | **Finalist/not selected:** everyday recognizable battery choice; baseline signal strength and operator conditions can change both networking and app behavior; no sufficiently comparable verified total-energy test in this pass; must not invent a winner |
| Full washing machine versus two half-loads | **Finalist/not selected:** easily understood household consequence; energy and washing effectiveness depend on exact appliance/program/loading; no matched published result for chosen baseline; cannot claim measured delta |
| Indoor drying rack versus electric tumble dryer | plausible energy/time tradeoff, but unequal drying time/humidity and not yet verified same final dryness, so no robust single comparable metric |
| Reuse one shopping tote vs plastic bags | duplicate editorial PR #329; protected queue |
| Air conditioner vs windows in a car | duplicate PR #320 |
| Thermostat setback vs constant heating | duplicate PR #317 and earlier #195 |
| Kettle vs microwave for a mug | duplicate PR #171 |
| Idle car vs restart | duplicate PR #157 |
| Group-weighting a lighter packet | duplicates #207/#262 |
| Stairs vs lift at different wait times | duplicate PR #175 |

Only **one** candidate supported both a conditional numerical effect and a defensible A/B narrative in this pass. Do not pretend the two less-proven finalists passed the same fact threshold. They remain possible future research, not rejected owner themes. This funnel yields one evidence-ready winner and does not fill a second PR by habit.

## Directly inspected sources; exact claims

1. **Purdue University, 2021-07-28**, "Dark mode may not save your phone's battery life as much as you think", https://www.purdue.edu/newsroom/archive/releases/2021/Q3/dark-mode-may-not-save-your-phones-battery-life-as-much-as-you-think,-but-there-are-a-few-silver-linings.html ; *Fact: Dark mode only makes a noticeable difference* paragraphs. Four OLED Android phones Pixel 2, Moto Z3, Pixel 4, Pixel 5, six apps Maps/News/Phone/Calendar/YouTube/Calculator, 60s activities. At 30–50% brightness, 3–9% average **total-phone power** saving; at 100% brightness, 39–47% average phone-power saving. At Pixel 5 Google News, 20%-brightness light / 50%-brightness dark drew similar power in the cited setup. Not every phone/app, not 39–47% extra lifetime, not the author's own test.
2. **Purdue ECE first-party exposition, 2022-01-25**, https://engineering.purdue.edu/ECE/News/2022/shedding-light-on-dark-mode-to-save-energy ; paragraphs "Our findings contradicted" through "OLED profiling tool". Explains 3–9% of whole phone power for indoor normal use, why brightness matters, roughly factor-of-ten difference in **OLED display power only** 100% vs 50% in their study. Do not apply factor-of-ten to whole device. Describes per-frame profiling to account for coloured pixels rather than relying on one battery-drain aggregate.
3. **Mobile Enerlytics original test report, 2019-08-19**, https://mobileenerlytics.com/dark-mode/ ; table "Apps and Dark Mode testing scenarios" and "Testing methodology". Nexus 6 OLED at 38% brightness, stable Wi-Fi; repeated each scenario five times in each theme. **23.5% total phone energy saving** Google News reading, **1.8%** YouTube full-screen playback, intermediate other scenarios. Different method/device from Purdue; not combined as single mean. Its R/G/B non-additivity experiments support need for accurate power models. Authored by research vendor, methodological self-report, not independent replication.
4. **9to5Mac, 2019-10-20**, https://9to5mac.com/2019/10/20/dark-mode-iphone-battery-life-test/ ; secondary reporting of PhoneBuff robotic iPhone XS test: light phone expired while dark phone still showed 30% charge. **Not** direct viewing of video; no extrapolation to generic 30% day-long gain.
5. LCD vs OLED physical distinction substantiated by Purdue sources 1–2, not an invented LCD percentage. Models and research dates are historical, not 2026 lab measurements.

## Comparable public YouTube evidence and limitations

Found metadata/search-page description only, **NOT watched**, and no transcript/comment analysis claimed.

| Link / video ID | Author / language / age | Known views / duration / observation | Comparison and counter-signal |
|---|---|---|---|
| https://www.youtube.com/watch?v=qbxdHpD5jWw / `qbxdHpD5jWw` | PhoneBuff; English; video cited in article 2019-10-20 | Published date inferred from 9to5Mac secondary; views/length **UNVERIFIED**; URL confirmed via article link on 2026-11-21 | Older controlled endurance video, not Two Ways illustrated short; 30% remaining charge when alternative died is scenario-specific |
| https://www.youtube.com/watch?v=dkLHJgZfVfE / `dkLHJgZfVfE` | Engadget; English; 2019-10-21; large established publisher | approx 41,881 views in crawled public YouTube search metadata; duration **UNVERIFIED**, observed 2026-11-21 | Reacts to PhoneBuff rather than a new independent experiment; 1.44m followers. Views are old cumulative, cannot infer current demand |
| https://www.youtube.com/watch?v=GKv2CTegBOo / `GKv2CTegBOo` | Encore Technical; English; 2019-10-30; small creator | approx 12,730 views in older crawled public search metadata; duration **UNVERIFIED**, observed 2026-11-21 | Phone XS Max demonstration, not age-/format-matched to new channel; old cumulative views, uncertain source freshness |

**Baseline:** Search surfaced very different creator scales (large Engadget vs 234-followers Encore), so normalized 2019 age-matched within-author typical video performance could not be established; **baseline UNVERIFIED**, not 0. No claim about CTR, retention, fresh 30–90d demand or performance of current Two Ways Shorts. Old public views and followers don't establish search volume, upload velocity or watch interest in 2026. Comments in these videos were not accessible with zero vidIQ credits; free social comments on 2019 Reddit threads discuss OLED-only caveat and desire for genuine controlled measurements, but do not quantify video demand (e.g. https://www.reddit.com/r/ios/comments/dk1o88/ and https://www.reddit.com/r/apple/comments/dkctgl/). Searches for newer directly comparable **EN illustrated A/B Shorts** did not yield a verified like-for-like baseline. Purely evergreen **experimental angle**.

## Evidence-linked story map and alternatives

- 02m: direct question -> fair equal-brightness A/B -> OLED explanation -> Purdue indoor 3–9% -> same study maximum brightness 39–47% -> LCD exception -> conditional answer, complete payoff before last-to-first spoken loop. A/B winner is dark for tested OLED, **not** a fabricated reversal. The **magnitude** reverses expectations; never falsely claim light mode won indoors.
- 05m: questioning intro -> indoor reader -> OLED vs LCD/whole-device power -> modest indoor result -> sunlight change -> app content (different study) -> Pixel 5 brightness comparison -> conditional action. No falsely observed first-person experiment.
- 10m: viewer's expectations -> the meaning of "power" -> four-phone Purdue method -> brightness and high-brightness result -> Mobile Enerlytics scenario differences -> methodological pitfalls (battery endurance vs frame power, confounded brightness) -> how dark-grey/content change savings -> final conditional action. Adds genuine research method, but can feel instructional after core verdict.
- Strongest alternative: **Wi-Fi versus mobile data while browsing**; also an actionable A/B battery question with relatable payoff. A defensible conditional winner might be more surprising than dark mode, but cannot be proved from matched data currently consulted. Do not fabricate it or classify as owner rejection.
- Rights: original EN narration, RU semantic version, no quotations from video creators or source paper, YouTube URLs used only as research metadata. No borrowed media or re-enacted lab footage.
- Freshness: old 2019–22 primary and public-video evidence; no verified 2026 viral/new claim. Confidence high in faithfully stated research claims, moderate in editorial utility, low in fresh audience appeal.

## Source and working-scope integrity

GitHub remote main rechecked before writing: `131ef24068d75967b1e43aa88e5f1370f6775054`; recent #331 Nuviko, #330 Paper, #329 TwoWays establishes this rotation. GitHub PR search `"dark mode"` found no story duplicate on 2026-11-21. Owner-rejected #13 telegraph / #88 bridge angle not reused; approved #20 S-5 B and #25 Lawnchair Larry B only referenced for normal spoken action, not to imitate their formula. #124 merged; canonical current main editorial applies. Production data, private names and credentials were not placed into external web queries.