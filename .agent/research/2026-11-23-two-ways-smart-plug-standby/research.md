# Two Ways Lab — The smart plug that uses more power than it saves

**Observed 2026-11-23. EDITORIAL_CANDIDATE_UNREGISTERED.** Research and scripts are an illustrative first-person A/B simulation, NOT real household measurements, consumer advice, independently reviewed work or a production-approved episode. All external research queries generalized; no repository/private identifiers submitted.

## Selection: actually screened 12 directions, duplicates and alternatives

Audience: English-speaking casual viewers familiar with the temptation to buy a smart-home device to save money. Core value: the promised *saver* could increase energy use because the controller itself draws electricity; a declared changed device reverses the winner. Must not pretend this is universal or a physical test.

| Direction | Finding at screening; no claim to complete audience analytics |
|---|---|
| **A/B: leave efficient TV in standby / schedule smart plug off** | **Selected editorial candidate**. Concrete counterintuitive result and honest change of winner with receiver; actual plug/device readings unknown |
| **Roll vs fold the same clothes in a suitcase** | **Strongest competing finalist**. Highly visual and proven evergreen curiosity, two authors' demo videos below; cannot honestly score fit/wrinkles with no measured garment sizes or identical physical test |
| **Print long job first vs shortest print jobs first** | Third finalist. Same jobs and fixed queue math yield distinct finish-time and mean-wait metrics, but far less broadly relatable and 10m would be lecture-heavy |
| Idle phone charger with smart plug | Adjacent to selected concept; could be a separate specific case, but no separate storyline beyond the selected break-even rule |
| Switch laundry cycle priority | Existing [#246](https://github.com/kleksar/ytvideos/pull/246), duplicate territory |
| Dishwashing by hand vs dishwasher | Existing [#168](https://github.com/kleksar/ytvideos/pull/168), duplicate |
| Router central vs desk | Existing [#359](https://github.com/kleksar/ytvideos/pull/359), duplicate |
| Setback thermostat vs steady heat | Existing [#317](https://github.com/kleksar/ytvideos/pull/317), duplicate territory |
| OLED light theme vs dark theme power | Existing [#332](https://github.com/kleksar/ytvideos/pull/332), duplicate |
| Kitchen air fryer energy vs acquisition payback | Existing [#299](https://github.com/kleksar/ytvideos/pull/299), duplicate |
| Older appliance vs new appliance purchase price | Another theme, dependent on actual prices/lifetime/usage; no comparable verified inputs selected |
| Elevator vs stairs from same starting floor | Existing [#175](https://github.com/kleksar/ytvideos/pull/175), duplicate |

Last story Draft before selection was [#378 Nuviko](https://github.com/kleksar/ytvideos/pull/378), after [#377 Paper](https://github.com/kleksar/ytvideos/pull/377), so Two Ways is next. No existing PR found for the precise smart-plug standby comparison in repository-wide PR title/keyword inspection 2026-11-23. This is not proof no same idea is buried in a different title or inside an Issue. Previous accepted / rejected owner calibration remains protected.

### Three finalist pitches, competing fairly before text drafting

| Candidate | Exact initial question + first visible event | What changes after hook | Full payoff | Strongest objection |
|---|---|---|---|---|
| **Smart plug** | “Can a smart plug use more electricity than it saves?” Same TV and schedule, cyan A wall socket vs amber B Wi-Fi plug | TV standby 0.3 W gives A 6 Wh vs B overhead 17.6 Wh; explicitly substitute a hypothetical 8 W idle receiver with same schedule | A wins TV by 11.6 Wh/day; B wins receiver by 142.4 Wh/day; boundary 0.88 W, not universal | A hypothetical comparison of assumed wattages can feel less compelling than real meter footage; dated competition and weak evidence of demand for illustrated model |
| **Fold vs roll** | “Can I fit more of the *same* clothes by rolling them?” Two identical luggage outlines and matched pile | Repeated packing/space/wrinkle outcomes under physically identical clothes | Actual volume remaining and retrieval/wrinkle tradeoff **only if measured** | No actual garments, luggage/measurements/physical review; inventing an answer would fake results |
| **Printer scheduling** | “Why is my one-page print stuck behind a 90-page job?” Two identical print queues | Single large job blocks first result, shortest-first changes mean completion and arrival expectations | Earliest sheet vs completion of all pages can favor different strategies | Too much setup, arithmetic, and no strong mass audience evidence; long editions padding risk |

**Selection trade-off:** suitcase has stronger proof of pre-existing video interest and physical payoff but depends on a measurement not available; smart plug can offer an accurate *conditional* surprise and useful rule using declared inputs, so it is chosen as an **experimental** editorial candidate. The competing topic is not rejected by owner and not banned forever. A genuine first reader may find the smart-plug idea too obvious or low stakes: reject/rework rather than inflate scores.

## Viewer evidence, competitors and constraints

Dates below are video **publication dates** shown on accessible indexed YouTube metadata, not dates when the videos were actually viewed. This research observed those metadata/pages on **2026-11-23**. Exact YouTube player, full transcript, audience comments on those videos and actual AV were NOT accessed; video titles/descriptions are not a claim of having watched a video. For comparable videos by *the same authors* of similar age/length and baseline, reliable samples were not available: **UNVERIFIED**. Views are indexed snapshots, not current views velocity or CTR.

| Video or audience question | Author, language, published | Observed format / length / views | Meaning and counter-signal |
|---|---|---|---|
| [Can Smart Plugs Really Help You Save Money on Your Energy Bills?](https://www.youtube.com/watch?v=uqC53ovDBrw) (ID uqC53ovDBrw) | Dr Chris J Barnett, EN, **2023-02-10** | Video, precise duration UNVERIFIED; indexed ~1,220 views / ~1,310 followers | A direct energy-savings question, low public-view signal; author baseline UNVERIFIED |
| [Smart Plugs Can Save You Money (Reduce Power Bills)](https://www.youtube.com/watch?v=yMIBRDW6PQc) (ID yMIBRDW6PQc) | Cheese Turbulence, EN, **2024-10-19** | Long YouTube video, description chapters through 14:32; ~8,700 views / 53k followers | Competitor actually describes household measurements (in listing), unlike our simulated model. Novelty/relevance challenge; video not watched |
| [Smart plug. With energy monitor. How to save on your electricity bill](https://www.youtube.com/watch?v=F8IWA9RQdn0) (ID F8IWA9RQdn0) | McGregor, EN, **2021-09-17** | YouTube video; duration UNVERIFIED; ~7,276 views / ~1,910 followers | Another author's evergreen subject, not matched format, not a measured response to proposed version |
| [FACE OFF: Rolling vs Folding](https://www.youtube.com/watch?v=XLLUn-WXLDw) (ID XLLUn-WXLDw) | SmarterTravel, EN, **2018-10-23** | Demonstration video; duration UNVERIFIED, ~31,927 views / ~8,189 followers | Strong rival topic has demonstrations; more directly visual; not evidence for plug video |
| [Smart plug idle question](https://www.reddit.com/r/homeautomation/comments/1hsgm61) | r/homeautomation, **2025-01-03**, English | Public comment thread; users discuss energy draw and half-watt experience | A genuine viewer question. Comments are anecdotal, not representative data |
| [Smart plugs to cut idling chargers?](https://www.reddit.com/r/ElectricalEngineering/comments/1mtn7gk) | r/ElectricalEngineering, **2025-08-18**, English | Public question and comments about whether smart controller costs more than device | Direct practical objection; likely technically oriented audience, not a measured Shorts sample |
| [Smart plug drain measurement thread](https://www.reddit.com/r/homeassistant/comments/z7h5zy) | r/homeassistant, **2022-11-29**, English | Individual reported multimeter readings, commenter questioned assumed power factor | A useful caution that an anecdotal low-power reading is NOT laboratory proof |

**30–90 day signals:** newly published 2026 consumer blog discussions exist ([Oct 2026 explanatory page](https://roofandrouter.com/guides/do-smart-plugs-save-electricity)) but there is **no verified recent on-YouTube surge** or comparable short-form author baseline. Distinguish evergreen questions from fresh measured demand. No YouTube transcript/comment consumption, no vidIQ charge/purchase, no own-channel analytics/readback, no CTR, view-to-impression ratio, retention, stayed-to-watch or future performance observed. **Demand: UNVERIFIED.** A published 14-minute appliance/meter experiment is counterevidence that our invented model offers enough entertainment; independent reviewer must decide.

## Primary factual basis and safeguards

1. [ENERGY STAR current television criteria](https://www.energystar.gov/products/televisions/key_product_criteria): standby-passive ≤0.5 W, network-standby ≤1.0 W for qualifying models under specified tests. Accessed **2026-11-23**. This demonstrates low-standby specifications exist; it does NOT verify a measured 0.3 W for our hypothetical TV, nor describe every TV. We do not claim TV is certified.
2. [US Department of Energy: Purchasing Energy-Efficient Televisions](https://www.energy.gov/cmei/femp/purchasing-energy-efficient-televisions): explains standby draw and energy purchase efficiency; accessed 2026-11-23. Does not validate this scenario's plug watts.
3. [Smart-plug energy use discussion, real comments](https://www.reddit.com/r/homeautomation/comments/1hsgm61): on/off networked smart-plug electronics require electricity; anecdotal half-watt readings, not a specific model verification. Accessed 2026-11-23.
4. [CC2.tv plug measurements program](https://cc2.tv/432.php): German text says its tested plug drew ~0.7W when output off and ~1.3W when on; **not used as proof** for our 0.7W OFF / 0.9W ON pair. Program not watched. This external example is only a plausibility bound, not source of our model.
5. [SmarterTravel packing comparison](https://www.youtube.com/watch?v=XLLUn-WXLDw): listed real other-topic demand for finalist. Its physical results were not read or borrowed.
6. **Model inputs** 0.3, 0.7, 0.9, 8 W, 4/20 hours, $0.25/kWh, $15 purchase are all **invented and explicitly declared as illustrative assumptions**. None attributed to an actual model, household, manufacturer or experiment. No borrowed narration, graphics, music, video frames, voice or imagery.

### One fixed conditional A/B model and audited arithmetic

Metric **Wh/day at the wall**, comparing A (device in standby when idle) and B (smart plug removes device standby power when output off). For the same device both methods have the **same active device consumption**, assumed unchanged when power passes through plug, so that term cancels. Inputs stated before result: 4h active; 20h idle; plug self-use 0.7W when output OFF and 0.9W when ON. Both versions start with the same day and same appliance. Plug ON/OFF output states are distinct from whether the plug itself is powered; assume it retains scheduling.

| Model | A idle energy | B plug's own full-day energy | Winner and difference |
|---|---:|---:|---|
| Hypothetical TV idle **0.3 W**, four hours active | 0.3×20=**6 Wh** | 0.7×20+0.9×4=**17.6 Wh** | **A** by 11.6 Wh/day |
| **Separately announced scenario:** replace TV with receiver idle **8 W**, same schedule/plug | 8×20=**160 Wh** | **17.6 Wh** | **B** by 142.4 Wh/day |

A conditional device change is a newly disclosed run, not a hidden mid-run switch or measured reversal. Break-even standby under **same conditions** is 17.6/20 = **0.88 W**. Greater than 0.88W B saves; less A saves; exactly equal tie.

**Long-only additional sensitivity:** 8h active, 16h idle => plug overhead 0.7×16+0.9×8=**18.4 Wh**; 18.4/16=**1.15 W** break-even. Alternate *hypothetical* more efficient plug off=0.1W, on=0.2W => 0.1×20+0.2×4 = **2.8 Wh**, TV savings 6−2.8=**3.2 Wh**. These are new declared inputs with **separate** comparisons, never observed device behavior.

**Optional long-only invented price model:** 11.6Wh/day extra = 4.234 kWh/yr; $0.25/kWh -> ~$1.06/yr additional energy cost. 142.4Wh/day saved = 51.976kWh/yr -> ~$12.99/yr savings. If hypothetical acquisition cost $15, payback $15/12.994 ≈ **1.15 yr** for the receiver case, electricity-only, not an actual consumer return. Never claim universal utility tariff, purchasing price, payback, or safety.

**Material safety limitation:** some televisions perform maintenance, network activity, recording or software tasks while in standby. A permanently power-disconnected device may lose functions or, for particular hardware, be unsuitable. Do not generalize from modeled energy to a recommendation to cut mains to an actual model; consult real manual and appropriate measurement. Never switch equipment requiring continuous power just to save theoretical Wh.

## Story promise → early proof → payoff, no fabricated measurements

- Working title: **“The Smart Plug Used More Power Than My TV (In a Model)”**. No real plug/TV experiment claimed.
- First semantic frame: an ordinary dark TV with standby light, one A wall outlet vs B scheduled plug shown from the SAME state; cyan A and amber B according to Two Ways brand (no actual images produced).
- Cold hook exact EN from 02m: “Can a smart plug use more electricity than it saves?” Viewer picks A/B before seeing watt-hours.
- After hook: 20h idle vs 4h active established, TV standby surprisingly small at six Wh; plug continues consuming when output OFF, causing first reversal of expectation.
- Full payoff: A 6Wh vs B 17.6Wh, B wastes +11.6Wh/day. Then disclosed different idle draw for receiver flips B to −142.4Wh/day. Practical criterion actual idle watts vs controller overhead, not universal advice.
- Biggest editorial objection: an assumed-input mathematical result is not a real outcome and may feel low stakes. The 10m text may overexplain conditional sensitivity and pricing. The exact model, not real shopping recommendations, must be visible.
- Storyboard/prompts: deferred until exact script passes checks, reviewer sees it cold, and actual image-reference bytes available; no existing timings/spans inherited.

No actual channel-owned performance data, media, provider output, independent reading, or AV loop measurement.