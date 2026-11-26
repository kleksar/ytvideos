# Research — Subway car nearest my exit, or nearest my entrance?

**Observed:** 2026-11-21. **Channel:** Two Ways Lab, English first-person illustrated comparison. **Type:** explicitly hypothetical timing model, not footage or measured public-transport experiment. **Editorial source:** live main `131ef24068d75967b1e43aa88e5f1370f6775054`. #124 merged; do not treat proposed 7d6bdf7 as a separate production pin.

## Actual search coverage and shortlist

Preliminary screening of 12 distinct everyday comparisons from the current channel backlog, repo PR/Issue search and public interest searches:

1. **Choosing the boarding car for the destination exit (#89)** — SELECTED. A seemingly smart early walk can save 100 seconds, cost 140, or save 40 *after missing a train*, depending on departure and headway. Real commuter question, visually legible A/B, honest deterministic payoff. Counter-signal: urban transit audience narrower than universal household tasks; no directly matched entertainment baseline.
2. **Backpack by item category versus next-use order (#16)** — finalist. Hook: searching for an urgent item buried under neatly grouped clothes. Development: repeated withdrawals, unexpected change of usage order. Payoff: rearrangement counts under a declared model. Serious challenge: whether 10 minutes adds substance without arbitrary retrieval events; existing travel gear creator interest is not a direct A/B demand signal.
3. **Office printer first-come-first-served versus short jobs first (#80)** — finalist. Hook: one long print traps three people with short jobs. Development: change order, compare average finish versus fairness of the longest wait. Payoff: same total work, very different average waiting. Counter-signal: educational scheduling already well covered; #217 shortest tasks vs deadlines is adjacent, so originality weaker.
4. First-fit versus snug-fit household drawers (#23) — valid mathematical A/B but needs stronger personally significant payoff.
5. Replenishment-first vs biggest-item-first containers (#30) — repeat work more salient than one day's count, data weak.
6. Robot-vacuum dock at entrance vs centre (#36) — plausible model, real battery curves absent, likely contrived.
7. Shop alone vs split grocery aisles (#66) — common question, overlaps #344 labour allocation mechanics, limited novelty.
8. Wait for one bus vs make a connection (#86) — strong stakes, resembles #285 missed transfer; avoid duplicate.
9. Packing by unloading order vs maximal fill (#20) — two legitimate metrics but difficult to compare fairly on one metric.
10. Storing older items up front (#9) — educational, thin dramatic progression for three distinct texts.
11. Colour-sorting laundry (#2) — fewer searches but similar existing #246 laundry-order A/B.
12. Phone and cable assignment by flexibility (#6) — **existing #230** direct duplicate; excluded.

Also checked repo duplicates before authoring: #207/#262 weigh-pack puzzles, #186 three-room cleaning, #237 grocery route, #121 group photos, #230 cables, #217 tasks, #133 bathroom, #175 stairs/elevator, #118 escalator, #127 parking. No existing matched title/angle for boarding-car-to-exit in open/closed PR search. Search is not exhaustive semantic duplicate detection; repeat immediately before push.

## Three rival pitches at comparable specificity

| Finalist | Exact cold entry | What happens *after* entry | Full payoff | Most damaging objection |
|---|---|---|---|---|
| Subway car | “I have one minute before my subway train leaves.” At destination the stairs are at the opposite end | A/B same station; slow-departure B wins; imminent departure A wins; short headway even lets B miss one train yet finish first in longer variant | The car is not inherently optimal: waiting overlap, departure deadline and headway determine result | Synthetic geometry/headways; travel audience specificity; public videos mostly unrelated travel advice |
| Backpack | “My passport is at the bottom of my perfectly organized bag.” | Sorting by type vs use order, time of retrieval and one changed requirement | Number of displaced items under known access assumptions; no universal best pack | Arbitrary item requests, weak 10-minute expansion, relative weights/comfort not covered |
| Printer queue | “One person's 30-page job makes three one-page jobs wait.” | First-in versus short jobs first, time each person finishes, fairness objections | Average completion time drops while first arrival waits longer; fixed workload | Widely taught SPT principle; adjacent existing tasks PR; less visually distinctive |

**Choice:** Subway wins on the specific reversal that a passenger may finish earlier despite missing a train, *without* fabricated events. Its initial 2-minute version contains a complete loss/win reversal; the 10-minute variant earns a third scenario (60-second headway). Printer and backpack remain legitimate alternatives, not owner-rejected themes. Strongest alternative on general-audience breadth: backpack; strongest on clean maths: printer. No empirical evidence of CTR, retention or guaranteed viral appeal.

## Evidence: real commuter interest versus entertainment-market inference

**Primary/product confirmation, not independent retention:**
- Citymapper official [Phase 1 Elizabeth Line](https://citymapper.com/news/2522/phase-1-of-elizabeth-line-is-now-open) (2022): advertises route **best entrance and best carriage** information, explicitly says this avoids a long destination-platform walk. This supports the real user problem, **not** our model numbers.
- Citymapper official [Voice instructions](https://paris.citymapper.com/news/2395/citymapper-in-your-ear): best carriage and platform guidance. No verified claim that suggestions include precise boarding deadline.
- [Fast Company, 2015-09-01](https://www.fastcompany.com/3050485/plan-your-speedy-exit-from-the-subway-with-this-app): contemporary explanation of why best-carriage info can save exit or transfer walking; secondary source.
- [r/AskNYC, 2025-10-13](https://www.reddit.com/r/AskNYC/comments/1o5wb91/how_we_choose_which_subway_car_to_board/): **actual public discussion**; a highly upvoted response describes choice #1 for exit but an exception when train approaches early. Another mentions using Citymapper; comments are a convenience sample, not retention evidence.
- [r/nycrail, 2025-01-28](https://www.reddit.com/r/nycrail/comments/1ibl8il): people explain selecting cars for exit stairs/transfer, occasionally losing time reaching them. Not YouTube comments.

**YouTube metadata, obtained via publicly indexed results, NOT playback or transcript analysis:**

| Exact URL / ID | Author/language/published | Type / reported views / known length | Role and limitation |
|---|---|---|---|
| https://www.youtube.com/watch?v=GsTo9W5QmJw — GsTo9W5QmJw | Japan BackpackersXpress / likely JP-EN mixed / 2017-02-24 | Transit exit guide; 3,938 publicly indexed views; length UNVERIFIED | Most directly analogous promise; reported creator following 401k but never use views/followers as ratio |
| https://www.youtube.com/watch?v=g5DkgAyUSxc — g5DkgAyUSxc | Jon Barr / EN / 2018-10-24 | NYC subway tips; 470,315 publicly indexed views; length UNVERIFIED | Wider subway appeal, NOT a matched A/B experiment |
| https://www.youtube.com/watch?v=CwR2Brlj9k8 — CwR2Brlj9k8 | Pictures of New York / EN / 2025-03-26 | NYC subway tutorial; ~205,600 views from third-party indexed page; 19:12 | Recent-ish but outside 30–90d, large-guide format not comparable |
| https://www.youtube.com/watch?v=kQrcRfbcIPM — kQrcRfbcIPM | Jon Barr / EN / 2024-09-08 | 2024/25 NYC travel compilation; 474,179 indexed views; multi-hour | **Same-author baseline attempt**, not comparably aged/formatted; does not control for author audience or format |
| https://www.youtube.com/watch?v=3xm6MrZvF5A — 3xm6MrZvF5A | Let's_Talk_ Ops_Mgt / EN / 2018-10-22 | Job sequencing (printer alternative); 10,461 views; duration UNVERIFIED | Education niche, not leisure competition |
| https://www.youtube.com/watch?v=eN2mSgZsgwk — eN2mSgZsgwk | DexTutor / EN / 2015-09-22 | Shortest-job-first lesson, 33,456 views; duration UNVERIFIED | Different publisher; educational interest |
| https://www.youtube.com/watch?v=jBDido6uX9k — jBDido6uX9k | REI / EN / 2018-12-11 | Backpack packing; 968k views **third-party indexed**; duration UNVERIFIED | Backpack alternative; tutorial, not exact categorical A/B |
| https://www.youtube.com/watch?v=Tpz2Ld6PfV0 — Tpz2Ld6PfV0 | Reysu / EN / 2025-08-23 | Travel bag organisation; ~135.9k **third-party indexed**; duration UNVERIFIED | Different author and format; no author baseline |

Sources: public player result metadata for Japan BackpackersXpress and Jon Barr (2026-11-21 search), third-party metadata pages for other channels. Some source titles/dates/pages may not refresh in real time; view counts are observation snapshots, **not** measured growth, current demand, retention, CTR or performance in this channel. No watched video, independent transcript, YouTube comment thread, per-author truly comparable age/format baseline or exact 30–90-day matched entertainment performance available. **Demand / channel audience match = UNVERIFIED.** The story is an openly labelled experiment in editorial interest, not a proven trend. No vidIQ paid request, credit or subscription used. Own YouTube analytics not connected in this run.

## Exact shared model; reproducible calculation

All lengths use **one model**, and different runs only change the declared departure interval. Times below are seconds from the narrator arriving at the origin platform; not actual train statistics.

- Origin x=0; origin platform length 180m, fixed A boarding door at x=0 and B at x=150; destination stairs at x=180 with same coordinate projection. All doors exist and are safely boardable when open. Both methods use same train vehicle/route and 300s ride.
- Narrator walks 1.5 m/s, no crowd, delays, accessibility constraint, luggage, door spacing ambiguity or interruptions. This is a **declared assumption**; not real passenger measurement.
- A: enter at nearest x=0, walk 180m after ride, **120s**.
- B: walk 150m before boarding, **100s**; after ride walk 30m, **20s**. Same overall walk (180m) in both methods.
- Train arrives 15s before departure in each scenario. Departure times are always explicitly predeclared.
- Model B sticks with walking all the way to x=150, so if it cannot reach the car before departure it misses. A practical adaptive third policy is **not simulated**.

| Controlled scenario | First dep. | Next dep. after first | A exit = first dep + 300 + 120 | B exit = first/next dep + 300 + 20 | Winner |
|---|---:|---:|---:|---:|---|
| plenty of time | t=165 | +240 (irrelevant) | 585 = 9:45 | 485 = 8:05 | B saves 100s |
| tight, 4-min service | t=75 | +240 | 495 = 8:15 | 635 = 10:35 | A saves 140s |
| tight, 1-min service | t=75 | +60 | 495 = 8:15 | 455 = 7:35 | B saves 40s despite missing train |

Python arithmetic sanity check executed independently of prose: `assert 180/1.5==120, 150/1.5==100, 30/1.5==20`; exit results `(585,485), (495,635), (495,455)`. That is authorial deterministic check only, not audience review.

**Generalized within model:** if both board same train, B gains 100s; if B misses one and service headway is H, B's relative result is H−100s. If departure is less than 100s away B definitely misses according to this fixed rule; **real boarding needs additional margin**. Do not recommend deliberately missing a train. Opposite exit location may eliminate the gain; accessibility and safety override time models.

## Cause/change/payoff map; sourcing boundaries

Initial practical conflict (Citymapper + commuter discussions) → known exit opposite entrance → two competing boarding rules → 100s walk shifted from destination into origin wait → safe same-train scenario B wins → near departure makes fixed B miss → headway changes sign of winner → actual lesson: departure slack and service interval, not permanent "best car".

No reported commuter, schedule, measured duration or dialog is invented: all actions and times belong to narrator's explicitly disclosed **model**. Broad travel advice (look up actual exit/car position, don't rush doors or platform edge) is precaution, not claimed empirical result. No third-party clips are proposed. Actual playback/comments and viewer response UNVERIFIED.

## Opposition/decision

Strongest surviving objection: this is a math story about a restricted model, whereas real stations have varying layouts and foot traffic. A viewer might leave after the first 100s improvement. Countermeasure: establish the near-departure failure as the second event rather than bury it in caveats; avoid turn-by-turn formula narration in Short. 10m third case is legitimate new understanding, but review judges its added explanation slower than its insight. 2m wins editorially by immediate stakes and two valid outcomes without unrelated tutorials.

Exact reading for the selected 02m text remains subject to independent first-listener judgment, native loop and measured TTS.