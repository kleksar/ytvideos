# Editorial self-review — NOT independent script acceptance
EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

**Method/limits:** author-only full-text reading and external documentary fact checking; no independent sessions reviewer; no original `ytv-script-review-v1`, no actual TTS or MP4. Narrative Short textual seam self-reviewed twice on **each full** EN and RU master. No script `PASS` in official ytv gate.

## Interest — author tentative / independent UNVERIFIED
Cold action S001 is an unusual verified traffic maneuver. S004–S005 reverse audience expectations with an advisory referendum defeated by a subsequent parliamentary decision. S006–S010 show mechanisms rather than repeating the switch; S012 adds the observed Stockholm complication and S013 finishes the main answer. Strongest weakness: S001 may give away all that a viewer wants; the interest of road signs and bus renovations is a hypothesis, not an audience result. Reviewer can choose `revise` or reject topic.

## Clarity — author PASS (limited) / independent UNVERIFIED
At first use, “the vehicles still allowed” prevents the false all-cars-on-the-road claim. S010 explains the ban; S011 clarifies 05:00 limited and 06:00 mostly general reopening. S012 is local, not national congestion. There are some longer numerical sentences; need actual oral reader to evaluate. Exact numbers are museum-derived and described in research.md.

## Factual/casual links — author PASS (limited) / independent UNVERIFIED
Source chain: official Swedish transport museum derived from traffic commission records for vote/decision/signs/buses/ban/times, and Guardian's first-day report for crowd congestion and minor accidents. “So even reaching the next country meant switching sides” is an ordinary practical inference about neighboring traffic patterns, not a quote by any specific driver. No fake citations inside narration; no mortality or CTR claims.

## Speech — author PASS (limited) / independent UNVERIFIED
Concrete action in every step, normal English idiom and full Russian equivalence; mixed paragraph lengths, no synthetic threat. A first listener may find S007 360,000 road signs hard to take in at spoken speed, or S002 and S011 overly similar; this is a live test blocker, not a silently “fixed” concern.
EN whitespace words: 278; RU whitespace words: 244. Estimate only, no measured runtime.

## Narrative ring — AUTHOR tentative PASS (text), actual independent/AV UNVERIFIED
**Literal EN ending then opening:**
```
It had all begun with one carefully timed move by the drivers who were allowed out before sunrise.
At 4:50 a.m., the vehicles still allowed on Sweden's roads stopped on the left, moved carefully across to the right, and waited.
```
**Literal RU ending then opening:**
```
А началось всё с одного точно рассчитанного манёвра тех водителей, которым разрешили выехать до рассвета.
В 4:50 утра машины, которым ещё разрешалось ехать по дорогам Швеции, остановились слева, осторожно перестроились вправо и замерли.
```
The last sentence specifically names the single timed move by permitted drivers before sunrise; the next (cold-opening) sentence **supplies the maneuver**, 04:50 stop-left, cross-right and wait. This is more than repeated subject matter and is grammatically a cause/explanation continuation, not a withheld answer. S012–S013 already reveal congestion resolved, some minor accidents and successful switch. Self-review joined full EN+EN twice back-to-back, then full RU+RU back-to-back, and examined S014→S001 plus whole flow. **Potential failure for independent reviewer:** the backward “It had all begun” may still sound like a new start; reviewer can FAIL despite our author reading. This text-level judgment is not a real independent `PASS`.
Real voice, music, caption and AV seam: **UNVERIFIED**; no MP4 existed.

## Missing capability and local gate
Actual repo checkout and executable `ytv` missing from runtime, thus no `uv run ytv start`, no actual `plan_summary/read_next/task_guide`, and no sessions.independent reviewer capability. No reviewer identity, fake hash, leases, approval, session ID, or accepted production gate is claimed. Follow handoff.md for official local registration.


---
# 2026-11-17: substantive three-version review (author only)

Baseline PR HEAD 8655800603d1992956f2d1dadf618ec30c1c295f, original source EN blob 6db3750fdbb1a8df6db15899fc735ac6506330bb, RU blob 257a15b0b77e4da16c3a7f169904855fc99e99ed. Existing source EN/RU and S001–S014 storyboard are preserved. Original storyboard binds only to the identical 02m source, NOT to new Longs. All six exact UTF-8 blobs were re-read before writing this section. SHA-256 over file content:

| Version/language | SHA-256 | Git blob SHA | Words | UTF-8 bytes |
|---|---|---|---:|---:|
| 02m/en | 2bafab1f4476d18b63ee884d0dac574f24bab976d8ab7b2476ba54020053d680 | 6db3750fdbb1a8df6db15899fc735ac6506330bb | 278 | 1720 |
| 02m/ru | a06f6e812fcaf2a14d1e81b3a5e5cf7ba00ff9e7ca4fac9547b56c46faa32246 | 257a15b0b77e4da16c3a7f169904855fc99e99ed | 244 | 3290 |
| 05m/en | 9e24198decc97d149813a5e9ab6471f1f014402d0c88d2eb5a10360fc8bfc086 | dc73031316cb26e0aedbd0618a5f23de809b7d35 | 539 | 3245 |
| 05m/ru | 10399eabd43e4c63fca1e48ae849e66c4f992d277a51b26cc0d2bd888ea09253 | bc58bada85fee026936f8b1bad356c546f09f38b | 471 | 6030 |
| 10m/en | 7a8a20894108d071461921e6c98fd4b7b7c097e8aeb6b16d54eed24a38f9e0a0 | 49acdc95acd1a6b2dae64aa4f3871be4bb737b87 | 1207 | 7350 |
| 10m/ru | 7c7a65e359f9a3c832ca65d916975395170f712d2bf64040aa28a1b4c6068031 | f02e72afb72b5a4062c37bad3a260af3041117b4 | 1019 | 13652 |

Full texts: [RU](variants/02m/script.ru.txt) / [EN](variants/02m/script.en.txt) · [RU](variants/05m/script.ru.txt) / [EN](variants/05m/script.en.txt) · [RU](variants/10m/script.ru.txt) / [EN](variants/10m/script.en.txt).

## Exact story maps
**2m preserved:** permitted vehicles stop/cross at 04:50 → border mismatch → 1955 NO / 1963 parliamentary YES → buses, signs and public information → staged ban and resumption → Kungsgatan traffic jam / limited crashes → backward loop. Strong cold fact but little secondary uncertainty; its ending may sound like another opening.

**5m:** opening how/why questions → left/right border contradiction → rejected 1955 advisory ballot → 1963 approval with four-year deadline **main hook** → bus doors on wrong curb → covered road signs coexist with live rules → driver reflexes and outreach → worker night and 01:00–06:00 traffic restrictions → 04:50 crossing, 05:00 limited resumption, 06:00 public return → spectator jam, police restore traffic → payoff why ten minutes were possible. Added value is mechanism and causality, not statistics.

**10m:** three questions → geographic mismatch and road design → decades of political debate → 1955 NO and concerns → 1963 294–50 decision **main hook** → nationwide coordinating commission → eight thousand buses, city one-way systems and signs → staged new/old coexistence → special vehicle tax → human reflex and deliberate delay of right-hand instruction → outreach including translation/accessibility and final radio/TV intensification → final road crews → temporary ban and 04:50/05:00/06:00 → spectators jam Kungsgatan, minor accidents → cautious payoff. Added value is planning as an operational and human learning problem. The tax/education section risks reducing anticipation of the switch.

## Eight editorial criteria, separately rated on exact files
Numeric scores are AUTHOR assessments, confidence moderate-low without first-listener. No automatic 9/10. Real viewer interest/CTR/retention UNVERIFIED in every column.

| Criterion | 2m | 5m | 10m | Concrete justification and weakness |
|---|---:|---:|---:|---|
| Interest / significance | 7 | 8 | 8 | National change despite NO vote; in 2m the switch is already answered, 10m may overfocus policy |
| Opening | 7 | 8 | 8 | 2m begins in a precise 04:50 action; Long questions promise how/why, but first minute is more expository |
| Development / reason to watch | 6 | 8 | 7 | 5m links political choice to physical problems then street disruption; 10m tax/education delays street scene |
| Payoff | 7 | 8 | 8 | All resolve actual road change; 5m/10m explain why timing worked, without invented national catastrophe |
| Angle freshness | 7 | 8 | 8 | 5m emphasizes covered signs while old road rules operate; 10m adds deliberate timing of instruction |
| Visual potential | 8 | 8 | 8 | Paper bus door, covered signage and 04:50 clock readable; 10m policy section risks static scenes |
| Naturalness / clarity | 7 | 8 | 7 | 2m list and backward loop awkward; 5m concrete and compact; 10m dense statistics risk lecture |
| Verified audience interest | UNVERIFIED | UNVERIFIED | UNVERIFIED | One old long-form car video in research is not demand evidence for these precise scripts |

## Hard gates and uncertainty
2m: original bytes preserved; the previously recorded full double reading on EN and RU is author-only; text-loop self-assessment is tentative. Independent Short loop PASS and actual AV seam UNVERIFIED. The story does finish before repetition. The existing 14-scene text plan is tied to this exact EN/RU only.

5m: full EN/RU same narrative facts, no unsupported named driver/quote; question-first Long, initial factual immersion and 1963 deadline main hook; no loop requirement. 539 EN words suggest approximately four to five minutes depending speaking rate and pauses; actual audio not measured.

10m: EN/RU corresponding factual expansion; question-first Long; 1955 turnout, parliamentary vote, extra reminder signs, tax, deliberately timed education, last-night crews all verified in shared research below. 1207 EN words suggest roughly nine to eleven minutes depending speech rate; actual audio not measured. Not a Short.

For both Longs, Paper Detour current ChannelSpec contains long, but actual runtime readiness UNVERIFIED. Source claims have author alignment to museum/Guardian sources, not independent factual validation. Creative confidence moderate-low; audience/demand data UNVERIFIED.

**Comparison:** 2→5 gains meaningful action: physical bus/curb geometry, two simultaneously prepared sign systems, staged vehicle movement. 5→10 gains how politicians funded/organized the switch and why detailed driving instructions waited until late August. The 10m version risks losing interest specifically between vehicle-tax explanation and radio/TV programming, before the 04:50 event. **Recommended 5m**, not owner approval; even 2m is preferable if a fresh first listener finds the Long overexplains its single central event.

**Next gate:** fresh independent reviewer must see complete exact text first without these author ratings, then sources; save authentic response bound to SHA-256 in the project's existing review schema. No session or receipt was created. Git-only candidates have no official ytv start or awaiting_script_approval; local worker must register a selected exact candidate in official runtime with canonical pinned context and apply ordinary checks. 05m/10m need distinct storyboard and visual intent only after version choice. No media or publishing authorized.
