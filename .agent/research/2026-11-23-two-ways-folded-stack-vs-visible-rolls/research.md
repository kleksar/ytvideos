# Research — Folded stack vs visible rolls (23 November 2026)

## Scope, status and original promise
**EDITORIAL_CANDIDATE_UNREGISTERED**. This is a first-person EN illustrated Two Ways Lab **conditional mathematical model**, not a performed trial, a claim about packing capacity, or a measured productivity effect. Audience: a traveler choosing how to organize clothes without unpacking the case every morning. Promise: **the method which loses on packing time can win on total packing + retrieval time; the winner reverses if there is only one retrieval**. Viewer chooses A/B before the model result. No true experiment, private analytics, full watch of competitor videos, retention or comment sample is asserted.

Source main: `a6023668001421b689a8142cebc0bd436545be6b` (remote read 2026-11-23). Canonical #124 merged; read `AGENTS.md`, documentation index, writer skill, full editorial and narration, workflow/development/task-contract, Two Ways channel spec, AGENTS, README, BACKLOG, SCENE_PLANNING and VISUAL_PROFILE. Review of accepted #20 S-5 version B and #25 Larry version B used to preserve concrete conversational grammar rather than imitate any particular loop.

## Candidate funnel — actual coverage (10 distinct tests/angles)
The shortlist was not chosen from three deliberately weak topics. Each item below was screened for what the viewer would choose, what changes after hook, whether the result can be calculated without fake measurements, and overlap with existing open/closed PRs.

| Candidate | Hook / possible development / payoff | Decision / evidence issue |
|---|---|---|
| 1. Folded stack vs individually visible rolled shirts | The quicker pack loses over three mornings; three unknown shirt draws, then one-draw reversal; explain threshold | **Finalist / selected**; precise reproducible model, strong everyday relevance; risk of old evergreen premise and artificial timings |
| 2. Walk to bus stop vs wait for later direct bus | Should I walk to an interchange? Route/transfer delay changes result; later bus may win | **Finalist**, strong intuitive choice and transition; specific route/timetables are locality-dependent, no verified matching schedules |
| 3. Clean room-by-room vs batch same task across rooms | Which saves switching time? Count tool switches, movement; threshold changes with room distance | **Finalist**, strong visual comparison but less decisive without real home measurements |
| 4. First parking space vs nearer entrance | Driving farther can lose despite shorter walk | Existing near-duplicate [#127](https://github.com/kleksar/ytvideos/pull/127) |
| 5. Nearest item vs aisle sweep when shopping | A short detour can save a full aisle return | Existing near-duplicate [#237](https://github.com/kleksar/ytvideos/pull/237) |
| 6. Folding gift wrap orientation | Sheet orientation changes usable cuts | Existing gift-wrap angle [#162](https://github.com/kleksar/ytvideos/pull/162) |
| 7. Dishwasher vs handwashing | Water or duration comparison changes at fill level | Existing [#168](https://github.com/kleksar/ytvideos/pull/168), [#303](https://github.com/kleksar/ytvideos/pull/303) |
| 8. Checkout/switch lines | Smaller line can be slower; switches incur cost | Extensive existing work [#368](https://github.com/kleksar/ytvideos/pull/368), [#376](https://github.com/kleksar/ytvideos/pull/376) |
| 9. Start short laundry or long drying load first | Sequence and shared dryer reverse makespan | Existing [#246](https://github.com/kleksar/ytvideos/pull/246) |
| 10. Coffee milk now or later | Cooling changes with time and mixing | Existing [#182](https://github.com/kleksar/ytvideos/pull/182) |

### Equal-strength finalist arguments
**A — clothes, selected.** Exact opening EN: “I can fold these eight T-shirts faster than I can roll them. So why would I roll them for a trip?” After hook there is a verifiable apparent advantage for A, first/second/third searches, inversion, then reversal for one-day trip. Payoff: A 100 s vs B 78 s for three unknown requests; A 63 s vs B 74 s for one. Strong objection: an organized folded file or planned outfits eliminates stack search, so model cannot imply rolling generally wins.

**B — walking vs direct bus.** Exact proposed opening: “The bus I can board first might get me home last.” The viewer chooses a departure, discovers transfer/wait risk, then route schedule drives the winner. Strong objection: without verified timetable/boarding connection, fabricating transport outcomes would be misleading. Stronger in movement imagery, weaker in immediately available verifiable inputs.

**C — room-by-room vs batching.** Exact proposed opening: “I cleaned fewer rooms per hour by cleaning each room only once.” Development: number of tool switches and extra crossing steps, then crossover in a long corridor. Strong objection: the planned numbers would be unmeasured switching time in a fictitious house, and likely less emotionally resonant than repeatedly digging into a suitcase.

**Strongest nonchosen alternative: the bus.** It could beat folding on public recognition and tension if a real timetable and matched current evidence were gathered. Chosen packing story offers a transparent, reproducible mechanism and a two-regime payoff **now**; no invented travel schedule. Selection confidence: medium editorial judgement, not measured popularity.

## Transparent deterministic inputs
- Same eight identical-for-timing shirts, same suitcase, fixed left/right layout. A = one flat stack; B = eight separate visible upright rolls.
- Preparation per item: A 5 s fold; B 9 s roll. Reach for any accessible target = 2 s.
- In A only, for each obstructing folded item: 3 s move aside + 3 s restore after removing the selected shirt. Remaining stack order preserved.
- Initially uniform random choice over remaining shirts on each of three successive mornings (sequential without replacement). The same distribution, retrieval rule and action times are applied to A/B.
- There is no actual randomness drawn/filmed. Values in narration are **expected outcomes** over possible equally likely targets, not one stopwatch result. No actual observed seconds.
- With n remaining, expected shirts above target = (n-1)/2, hence A retrieval expected = `2 + 6*(n-1)/2`; B = `2`.
- n=8,7,6: A retrieve 23+20+17 = 60 s, prep 40 -> **100 s**; B prep 72 + 2*3 = **78 s**. B wins 22 s.
- One request: A 40+23 = **63 s**, B 72+2 = **74 s** (A wins 11). Two: A 40+23+20 = 83, B 72+4 = 76 (B wins 7). Cross-over at second access.
- For three requests and n=8, exactly nine expected obstructing items total, moved twice = 18 timed moves. A total `46 + 18*t`; B 78; tie `t=32/18=1.777...s`. At t=2: A82 B78; at t=1.5: A73 B78.
- n=4 and three draws: A prep20 + expected six moves*3 =18 + grabs6 = **44**; B 4*9+6=**42**. n=3 and three draws: A prep15 + three expected moves*3=9 + grabs6 = **30**; B 3*9+6=**33**.
- The model is intentionally not evidence about rolling's physical compression, wrinkles, safety, convenience or universal packing speed.

## YouTube interest scan (source metadata read on 2026-11-23; no playback claimed)
| URL / author | Published | Language/format/duration/views observed or limit | Relevance & counter-signal |
|---|---|---|---|
| [SmarterTravel — FACE OFF: Rolling vs. Folding](https://www.youtube.com/watch?v=XLLUn-WXLDw) | 2018-10-23 | English video; runtime **UNVERIFIED**; indexed ~31,927 views | Direct A/B comparison, old evergreen interest; baseline same-author comparable result **UNVERIFIED** |
| [catherine jane — Rolling vs Folding--The Big Packing Debate](https://www.youtube.com/watch?v=iMXRQ7yXzBY) | 2019-01-17 | English video; runtime **UNVERIFIED**; indexed ~73,498 views | Another author; framing likely packing efficiency, not specifically repeated retrieval; baseline unavailable |
| [Travel Fashion Girl — How to Pack a Suitcase like a Pro](https://www.youtube.com/watch?v=EiJK-aB9aJU) | 2019-08-04 | English video; runtime **UNVERIFIED**; indexed ~17,345 views | Context, not same experiment; broad luggage interest doesn't establish demand for model |
| [Better Homes and Gardens — How to Pack Clothes](https://www.youtube.com/watch?v=RENSoGtpJcA) | 2013-03-14 | English video; runtime **UNVERIFIED**; indexed ~46,443 views | Context, older; big channel results not controlled demand proof |

These are pages/search metadata, **not a claim that the video or its audio, transcript or comments was viewed**. Public-view counts can change; dated snapshot is not growth, CTR, retention, performance vs same-author baseline, or paid vidIQ signal. 30–90 day *fresh* comparable performance: UNVERIFIED. Ordinary same-author videos of matched format/age, length, real questions/comments and privately measured audience retention: UNVERIFIED. No paid provider request or purchase. This supports only an **experimental evergreen hypothesis**. Biggest counter-signal: rolling versus folding is a saturated old premise, and model results may interest fewer people than practical physical demonstrations.

## Evidence and rights
All timing values and distribution assumptions originate **only from this fictional reproducible model**, not cited as physical measurements. The mathematical calculation is independently recomputable. Video links evidence only existence of comparable titles/pages, not performance claims. No third-party frames, music, logos, voice or thumbnail images copied; image copyrights / reference bytes must be evaluated if production is authorized. No external instructions were treated as authority.

## Rejected and unverified
Alternative full model of vertical filing folds is deliberately **not** masqueraded as A. True fabric volume, wrinkle severity, actual motor timings, viewer intent and AV seam are UNVERIFIED. If a real measured comparison is required before editorial approval, perform physical repeat testing rather than change the model's numbers to force a winner.

## Subsequent 10m model review — exact paths, no real-world frequency claim (2026-11-23)

10m now tests **expected vs realized** outcomes of the same A/B packing story, replacing the lower-value smaller-suitcase calculation. Original model and timings are unchanged. With 8 then 7 then 6 equiprobable remaining shirts, there are **8×7×6 = 336** equiprobable ordered shirt requests (not observed samples). Let S be the total number of shirts above the chosen target across three mornings. Exact realized A = **46+6S seconds** (40 packing, 6 for grabs, 6 per obstruction), B = **78 seconds**. A wins iff S≤5. Direct triple-loop enumeration over ranks 0..7, 0..6, 0..5 returns **56/336=1/6** A victories and **280/336=5/6** B victories, no ties. Best repeated top-draw path A=46/B=78; worst repeated bottom-draw path A=154/B=78. These are conditional math results, **not measured trip frequencies** or a survey of people.

A separate controlled **information-rule change** is now explicit: if the first three outfits are known before packing and stacked in intended retrieval order, the folded stack requires A=40+6=46, rolls B=78. It is no longer a uniform unknown-target experiment; changing what is known at pack time changes the choice. No claim is made about the performance of vertical-file folds, packing cubes, garment wrinkles, or real motor speed. Earlier 02m/05m artifacts are unchanged; original 10m blobs and SHA-256 remain in git and story-review for traceability.
