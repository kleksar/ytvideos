# Story review — exact scripts / 2–5–10 minutes

2026-11-19. **Authorial/self review only**, not independent listening. Numbers are editorial judgments, not measured demand, CTR, retention or probability. Production uses EN; RU is a complete semantic editorial counterpart. Model calculations independently rerun with a deterministic scheduler, not a physical experiment.

## Exact bytes, source Git blobs and estimated spoken length

| Variant | EN words, pace estimate | EN file SHA-256 / Git blob | RU words, pace estimate | RU file SHA-256 / Git blob |
|---|---|---|---|---|
| 02m | 278; ~111s at 150 wpm | `2a2d503238b3d66670bd1fa0ff29b07323b1283ba0c22e781c866d69567ddd1d`; blob `d6a5d87a9ddaaeceddc8cb08cf263bcd54ae10d1` | 259; ~111s at 140 wpm | `137e222e5ddd2581887ca9c975b6c6b9a2305ab9f5590d19f31fbcf2c0c892bc`; blob `dcdb830ad3128cbef6fddd3abc447238d362bf14` |
| 05m | 795; ~318s at 150 wpm | `4d1d7cb8fde5fb876df168c777fa3eba52f296a3adcd60ad7664e24b09ba9690`; blob `1f1c430c0e8ac1a199ddb4a31a08d2bc7153d5fa` | 681; ~292s at 140 wpm | `c6341ef7f3d0920f3f6a93f4023c239bad97add08c5117aef4c412faa4922a43`; blob `1758cec95fa699b342db2456b528758351a498d3` |
| 10m | 1570; ~628s at 150 wpm | `70f00a28aaa932e8030fc5c96d482723f05ac06c190614ba5b60a2a8a6e5c736`; blob `f81a43f1a38ba22ea95761037b56ddaf09150e44` | 1522; ~652s at 140 wpm | `c4692689e1a698ac1aef48c108eb4ebbe901e74d6277122f2731907cbf0d71d7`; blob `657390b6389ac1063fd3469765abdd28a4265899` |

Word counts and SHA-256 are from a zero-credit text-length/hash check on the **exact uploaded blob content, including trailing newline**; verification by later Git tree read-back still required. Times are mathematical pace estimates, not measured ElevenLabs audio and not a command to change the voice speed. Pauses may increase actual duration. Internal/production timing evidence remains UNVERIFIED.

## Story map and authorial eight-criterion review: 02m

**Version:** `variants/02m/script.en.txt` exact bytes with companion `script.ru.txt`. Opening EN: “The dryer helps decide whether I start with shirts or towels.” Ending EN: “So when I choose the first basket, which machine should I check?” The ending asks for a machine, opening supplies the dryer; the substantive A/B answer (A140 vs B165, then B130 vs A140) has already been given before that bridge. Proposed image seam: the two completed schedule strips disappear into the original two baskets and empty dryer. No actual AV test.

Beat map: choice of what to wash first → announce fixed makespan metric and equal setups → original shirts/towels timings → A makespan140 → B makespan165, washed shirts wait wet → controlled change shirts dry45→10 → B makespan130 vs A140 → condition-bound closing question. The 20-minute tie appears before final line. Payoff: “Now B wins by ten minutes.”

| Criterion (editorial /10) | Concrete evidence and reasoning |
|---|---|
| Interest / significance **8** | A25min advantage and reversal B10 with the **same two baskets**; practical one-washer/one-dryer question. Narrow hypothetical times prevent 9. |
| Opening **8** | “The dryer helps decide…” names both the daily task and the machine behind it immediately; not a generic scientific tease. |
| Development / why stay **8** | B forces clean shirts to wait wet fifty minutes, then changing only shirt-dry duration flips the result; two actual causal changes. |
| Payoff **9** | Full two-method finish times plus threshold of 20 minutes; no missing reveal reserved for repeat. |
| Angle freshness **7** | More specific than broad “laundry hacks”; no proof a comparable published A/B explanation is rare. |
| Visual expression **8** | Two parallel washer/dryer lanes and waiting baskets show machine occupancy without implying a physical test. Exact image feasibility not checked. |
| Natural speech / clarity **7** | First person, ordinary objects, no fake personal test; several “one-forty” style spelled times are number-heavy for an ear-only listener. |
| Verified viewer interest **UNVERIFIED** | Laundry demand discussions and videos are not a comparable Two Ways narration/Short baseline. |

**Principal weakness:** repeated spoken numerical times and ~111s target versus channel usual 35–50s Short. **Author:** this agent, 2026-11-19; medium confidence in editorial judgments, high confidence in deterministic arithmetic; no separate first listener.

Working decision **STRONG_CANDIDATE** (interest 8, development 8, payoff 9); *preferred editorial length*, conditional on actual Short-length/loop/production review and owner approval, not ready for automatic production.

## Story map and eight-criterion review: 05m

**Version:** `variants/05m/script.en.txt` and independent full semantic RU. Opening EN asks whether the same laundry can finish half an hour apart and what adding one basket changes. Three-load A `shirts→blanket→towels` **195**, B `towels→blanket→shirts` **225**. New material: dryer never has a gap after initial start (175min dry total; starts at minute20 vs50); controlled shirt-dry10 change returns a two-load B win but **three-load A185 vs B190** — third basket flips winner back. Payoff: “The result for two loads cannot just be copied onto three.”

| Criterion (editorial /10) | Evidence |
|---|---|
| Interest / significance **8** | Another basket changes the apparent winning rule: people with several loads can recognize this exact issue; model values hypothetical. |
| Opening **8** | Two precise questions promise equal inputs and an additional basket without implying real measurement. |
| Development **9** | A195/B225 waiting progression and a **second** switch of winner when the blanket returns; material not just verbose 02m. |
| Payoff **9** | Full three-basket result and exact reason for delay (dryer starts 30 minutes later, 175-minute continuous total). |
| Angle freshness **8** | A third job changing a two-job recommendation is a genuinely different layer; not verified as unique in YouTube. |
| Visual expression **8** | Two-row schedule with explicit queue and rerun offers clear states, though many numeric labels risk phone legibility. |
| Speech / clarity **7** | Ordinary first-person English; many numbers and repeated model transitions slow comprehension without exact visual schedule. |
| Viewer interest **UNVERIFIED** | No comparable narrator 5m YouTube baseline/retention available; public ASMR views are not this genre. |

**Principal weakness:** 5m adds real value but makes the audience track three queues and an earlier experiment; unlike 02m, **Long recipe is missing**. **Author:** this agent, medium confidence. Working decision **STRONG_CANDIDATE** on content, **production BLOCKED**, no implicit Long authorization.

## Story map and eight-criterion review: 10m

**Version:** `variants/10m/script.en.txt` with full meaning matched in RU. Opening poses three questions. Complete and independently structured: two-load A140/B165 → shirt-dry10 reverses to A140/B130 → 20-minute tie and “urgent shirt vs all laundry” objective mismatch → three loads A195/B225 then fast shirts A185/B190 → four loads A215/B235 → enumerate 24 orders and find **205** for S→B→T→X → conditional takeaway. No invented home test.

| Criterion (editorial /10) | Evidence |
|---|---|
| Interest / significance **7** | A/B alone does not inherently sustain ten minutes; metric conflict is useful but may be niche. |
| Opening **8** | Three answerable questions preview two controlled reversals plus a four-load counterexample. |
| Development **7** | Real additional tests, yet after three loads the chain becomes operational-research tuition; high chance of scrolling. |
| Payoff **8** | A215 vs B235, then different order 205 shows **both** heuristics can be improved; clear limitation of A/B victory. |
| Angle freshness **7** | Johnson-style two-stage scheduling is established; novel packaging for everyday laundry is a hypothesis. |
| Visual expression **7** | Four-lane orders with waiting time make a defensible visual, but labels and timings become dense on a phone. |
| Speech / clarity **6** | 1570 EN words of scheduling values; some technical repetition after the strongest result. |
| Viewer interest **UNVERIFIED** | No public evidence an audience wants a ten-minute narrated laundry optimization. |

**Principal weakness:** rising number load/complexity, weak added audience value after 05m, and no Long production configuration; no attempt to falsely score it 9/10. **Author:** this agent, medium-low confidence. Working decision **REWORK**, complete textual proposal but **not** recommended for production or formal pass.

## Direct 2 → 5 → 10 comparison

| Exact version | Adds substantive value | Main point of likely interest drop | Format gate | Decision |
|---|---|---|---|---|
| **02m** | Complete model and controlled winner reversal with two loads, plus exact tie | Repeating spoken minute figures in both lanes before payoff | Illustrated Short supported; duration much longer than customary 35–50s; actual fit/AV loop UNVERIFIED | **Recommend 02m**, keep full text unchanged pending independent review/owner selection |
| 05m | Third load reverses a two-load conclusion; explains uninterrupted dryer time and initial bottleneck | Second cycle of timelines after A195/B225 | **Long recipe absent**; do not create fabricated Long run | Strong content, production blocked |
| 10m | Different metric, sensitivity, 24-order audit shows both A and B non-optimal | Four-load schedule and result after the audience already has a usable rule | **Long recipe absent**; spoken burden/retention unknown | REWORK; do not stretch by adding facts |

The short is recommended for better question/reveal ratio and actual channel format, **not** because longer is forbidden in principle. More minutes aren't automatically an upgrade.

## Separate checks for the exact versions

| Check | 02m | 05m | 10m | Method/limitation |
|---|---|---|---|---|
| Underlying mathematical model, inputs, results | **PASS** | **PASS** | **PASS** | Independent deterministic recurrence/24-permutation verification; model input values arbitrary, not actual machine measurement |
| Unsupported personal experiment avoided | **PASS** | **PASS** | **PASS** | Exact texts explicitly say simulated/model values |
| Material semantic EN/RU pair | **PASS (author)** | **PASS (author)** | **PASS (author)** | Actions, outcomes, conditions and caveats aligned; RU 10m gives an extra illustrative reminder about missed machine beep, with no contradictory results |
| Original writing / rights | **PASS for author-generated text** | **PASS for author-generated text** | **PASS for author-generated text** | No third-party narration quoted; music/visual asset rights **UNVERIFIED/N_A** (none created) |
| Channel format compatibility | **UNVERIFIED** Short target length >35–50s | **BLOCKED** Long parameters absent | **BLOCKED** Long parameters absent | No ChannelSpec modification or fictitious Long recipe |
| Narration loop | **AUTHOR-PLANNED** (semantic question→answer); exact double-read/AV seam **UNVERIFIED** | N_A (Long) | N_A (Long) | A textual plan is not a measured audio/video transition |
| Independent story/loop reviewer | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No separate reviewer/reading input/receipt; self-review above is not independent |
| ElevenLabs timing, final AV, retention/CTR | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No TTS, media or publication |
| Formal ytv script gate/approval | **NOT RUN / NOT APPROVED** | **NOT RUN / NOT APPROVED** | **NOT RUN / NOT APPROVED** | Git-only editorial candidate, not an official run |

**Author revision cycles:** 02m first/last lines rewritten once to make an explicit semantic last-question → first-answer seam; duration rechecked after change. 05m and 10m had first full written editions and author pacing checks; 10m tightened by removing repetition before exact upload. Maximum two editorial revisions is respected. Every changed byte invalidates the relevant future reviewer hash.

**Needed next:** provide the exact chosen text (02m recommended) to a *new independent reviewer* before storyboard; first give opening and full text without these scores/beat map, then reveal sources for fact/model check. The reviewer can reject interest. Save authentic existing-schema result, do not synthesize one. Textual seam may pass while audio/video seam still fails; no MP4 exists.
