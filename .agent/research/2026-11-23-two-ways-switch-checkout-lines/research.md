# Two Ways Lab — Switch checkout lines when the next register moves first?

Observed on 2026-11-23. **EDITORIAL_CANDIDATE_UNREGISTERED; no runtime, independent reader, measured consumer behavior or production approval.**

## Selection: breadth, duplicates, competing proposals

Audience: English-speaking casual Shorts viewers familiar with waiting for checkout. Goal: a recognizable decision with a fair, reproducible A/B payoff, not a lecture on probability or a claim that one queue always wins. Production master language EN, complete RU review translation.

Twelve distinct screened directions (not twelve publications or tested video metrics):

| Direction | Outcome / reason |
|---|---|
| Personal checkout-line *switch after watching the other cashier finish first* | **Selected**: immediate temptation; comparison changes under explicit future delay, useful boundary |
| Roll vs fold clothes in suitcase | **Strongest alternative**: bigger pre-existing video interest; physical item dimensions/packing experiment inaccessible, pure assumed-volume model could fake result |
| Print one long job vs several short print jobs | Finalist: clear calculation/latency, but lower mass audience and mostly lecture-style video evidence; hard to justify non-repetitive 10-minute story |
| Two shoppers' pooled queue vs split queues | Duplicate of [#136](https://github.com/kleksar/ytvideos/pull/136) |
| Cashier vs self-service lane | Duplicate of [#368](https://github.com/kleksar/ytvideos/pull/368) |
| Parking first vacancy vs searching nearer entrance | Duplicate of [#127](https://github.com/kleksar/ytvideos/pull/127) |
| One shared bathroom, alternating stages | Duplicate of [#133](https://github.com/kleksar/ytvideos/pull/133) |
| USB-C cable assignment | Duplicate of [#230](https://github.com/kleksar/ytvideos/pull/230) |
| Family group photo entry/exit sequence | Duplicate of [#121](https://github.com/kleksar/ytvideos/pull/121) |
| Coffee + milk now vs later | Duplicate of [#182](https://github.com/kleksar/ytvideos/pull/182) |
| Laundry priority and machine order | Existing [#246](https://github.com/kleksar/ytvideos/pull/246); distinct new value not established |
| Wrapping gifts with one sheet | Existing [#211](https://github.com/kleksar/ytvideos/pull/211); new comparison needs physical dimensions/materials |

#136 compares **queue architecture** (one pooled vs two separate). This proposal compares **my decision to leave one existing independent queue at t=60** with unchanged cashier service schedules. #368 compares **two checkout technologies**; this proposal compares two staffed registers. This semantic distinction does not prove the audience will see it as novel: cannibalization **counter-signal**.

### Three finalists on equal footing

| Candidate | Exact cold opening / first visual | After the hook | Complete payoff | Strong objection |
|---|---|---|---|---|
| Switching checkout lines | "Should I switch checkout lines just because the one beside me moves first?" A with two people, B with four; B's first shopper leaves first | At t=60, what work remains at each register; keep/switch, then disclose hypothetical 25-second delay | Stay ends 3:15 vs switch 3:25. With *declared* delay: 3:40 vs 3:25; when to reconsider | Fictional service times; broad theme overlaps existing queue PR, demand for this *angle* unverified |
| Rolling vs folding | "I have the same suitcase and clothes. Do I gain space by rolling instead of folding?" | Compare actual fit, wrinkles and retrieval using real identical garments | Measured usable capacity and trade-offs, *if* physically tested | No actual garment measurements or visuals; made-up volume would make false evidence |
| Printer scheduling | "Why did my tiny printout wait behind a giant job?" | First-in-first-out vs short-jobs-first on identical jobs; check both last completion and mean wait | Different winners depending on metric | Technical/abstract, complex definitions before viewer cares; 10-minute text risks padding |

Selected over rolling only because a transparent deterministic checkout model offers an honest complete payoff *now*, whereas the packing comparison demands an actual test or established physical parameters. This is a tradeoff, not proof the queue theme has more viewer interest. If the independent first reader finds no reason to watch past the first result, reject or rework rather than publish.

## Public audience signals — not performance proof

Actual YouTube viewing/transcripts/comments **NOT AVAILABLE**; observations below are index metadata and public third-party pages, not claims that a video was watched. All recorded 2026-11-23. Views are snapshots when available, not comparable retention/CTR.

| Work / URL | Author/language, published | Format, duration, views | Observed & relevance / counter-signal |
|---|---|---|---|
| [Why the Other Line Always Moves Faster](https://www.youtube.com/watch?v=F5Ri_HhziI0) | Bill Hammack / engineerGuy; English, December 2010 | Explanatory YouTube video; duration and current views UNVERIFIED | [FlowingData, 2010-12-24](https://flowingdata.com/2010/12/24/why-the-other-lines-always-seem-to-move-faster-than-yours/) embeds/discusses the queue question. Video centers on statistical/probabilistic queueing, not our deterministic t=60 switch. Large existing coverage is a **novelty risk**, not evidence of our future reach. |
| [Queue Smarter, Not Longer](https://thekidshouldseethis.com/post/queue-smarter-not-longer-queueing-theory-and-the-math-behind-efficient-lines) | The Pudding, Mureji Fatunde; English, article says ~2025 (exact upload date UNVERIFIED) | Animated explain-it video linked via curated page; direct YouTube ID/duration/views UNVERIFIED | Described as covering single queues and service patterns; original video inaccessible, so no claim about scenes or comments |
| [Why a Single Line is Better](https://operationsroom.wordpress.com/2020/11/19/the-times-they-are-a-changin-whos-next-when-waiting-in-a-single-line-is-better/) | Jan Van Mieghem, English, 2020-11-19 article | Academic video embedded; direct ID and stats UNVERIFIED | Author distinguishes shared queue and jockeying; substantially more academic angle than first-person everyday decision |
| [Rolling vs Folding](https://www.youtube.com/watch?v=iMXRQ7yXzBY) | catherine jane, English, 2019-01-17 | Demonstration YouTube video, 73,498 views in search snapshot; video duration UNVERIFIED | Strong audience-oriented alternative but not our model's evidence |
| [FACE OFF: Rolling vs Folding](https://www.youtube.com/watch?v=XLLUn-WXLDw) | SmarterTravel, English, 2018-10-23 | Demonstration video, 31,927 views in search snapshot; duration UNVERIFIED | Second alternative author; observed listing only, not filmed test |
| [Printer SJF example](https://www.youtube.com/results?search_query=shortest+job+first+printer+queue) | Mixed teaching authors, language/dates variable | Comparability UNVERIFIED; no reliable matching nontechnical baseline | Search mostly returns operating-system shortest-job-first lectures, not broadly familiar printer narratives |

**Real viewer question/reaction sampled:** on [FlowingData, 2010-12-24](https://flowingdata.com/2010/12/24/why-the-other-lines-always-seem-to-move-faster-than-yours/), commenters debate whether side/center lines and queue layout change perceived speed. This is an observable audience question in the accessible article, not an endorsement of the new A/B simulation. Another 2026-11-17 [public checkout simulation](https://geopatternlab.com/tools/checkout-queues) includes switching, a **direct competitive novelty signal**; its existence does not measure audience demand.

**Baselines:** equivalent-length/age ordinary videos from those same authors: **UNVERIFIED** (no reliable complete author catalog or matching formats retrieved). User's own channel CTR/retention/stayed-to-watch: **UNVERIFIED** (no authorized matched performance export). 30–90-day verified interest in the precise switching angle: **UNVERIFIED**; existing large signals are older evergreen, not fresh growth. No vidIQ credit purchased/used; search pages alone cannot establish full YouTube result coverage, views trend, impressions, retention, CTR, comments on individual videos or viewer satisfaction.

## Fixed A/B model: deterministic, not measurements

Metric announced before outcomes: wall-clock seconds from t=0 joining the first line to finishing checkout / leaving the register. Same person, same 45-second personal basket service, same registers and people, same initial instant; choose **at t=60** A stay vs B switch to the *end* of next line. Each cashier works continuously, one shopper at a time, no preemption. Switching takes 5 seconds (t=60..65), overlapping with cashier service in the new line.

- At first staffed register: shopper A1 [0,90) = 90 s; A2 [90,150) = 60 s; my checkout [150,195) = 45 s.
- At other register: B1 [0,40), B2 [40,80), B3 [80,120), B4 [120,160), mine after switching [160,205) = 45 s. At t=60 B has already served B1; A hasn't finished A1. The B register has 100 sec remaining ahead of me (B2 20 + B3 40 + B4 40).
- **Base outcome:** stay t=195 (3:15); switch t=205 (3:25), stay wins 10 sec. Movement is *not* 5 extra seconds at finish because the cashier continues during the walk.
- **Declared counterfactual:** A2 experiences a price-check delay of 25 seconds, affecting the A queue only. Staying t=220 (3:40), switching t=205, switch wins 15 sec. Extra delay 10 s produces a tie.
- **Separate declared late-arrival scenario (10m only):** a B5 enters at t=63 while I cross and joins before I do at t=65, service B5 [160,200), mine [200,245). Staying remains 195, switch t=245, difference 50 sec. Arriving after t=65 instead would put B5 behind me. This is a *new input*, never an unseen mid-experiment twist.
- **Separate optional probability sensitivity (10m only):** invent p for *only* A's 25s delay, B constant. E[stay]=195+25p; switch=205, crossover p=0.40. At p=.25 E[A]=201.25 sec; at p=.5 E[A]=207.5 sec. Probabilities are invented assumptions, not actual store frequencies.
- **Deadline sensitivity (10m):** deadline t=210 (3:30): original stay/switch pass; with A's delay stay 220 misses while switch 205 passes. Metric explicitly changes to deadline feasibility for this subquestion. Not a proof the average and deadline have the same optimizer.
- Source of each number: declared fictional service schedule and arithmetic above. No hidden wait, magic register speed or claimed experimental event.

### Errors guarded against

1. Treating B's first finished customer as my position at the front (false).
2. Adding the 5-second walk to t205 when it already overlaps B's remaining work (false).
3. Silently changing arrival/service rules or treating a price check as observed (false).
4. Declaring the winner with the lowest person count or fastest earlier movement (false).
5. Treating assumed probabilities as measured, or denominator of p formula as an observed data rate (false).
6. Confusing seconds in the model with seconds in the actual video or simulated scene timing.
7. Placing model A's buyer behind me when A already has them in front at t0.
8. Reusing a candidate as a continuation of an accepted/declined owner topic, or borrowing Paper/Nuviko illustrated style.

## Promise and payoff

Thumbnail/title promise: *The Faster Line Was a Trap (In This Model)*. The first visual must show two staffed checkout lanes, A=2 people, B=4, B's first person leaving *first*; viewer is asked to pick stay/switch before seeing output. Payoff must be shown before the Short loop: 3:15 vs 3:25 base, then 3:40 vs 3:25 when one disclosed input changes. Explain *remaining work, not customers already served*. No universal "queues always..." claim.

Important production boundary: actual hero reference images not fetched; don't invent their bytes or reuse the checkout pilot frame as a new exact input. Visual media rights, model display geometry, exact timings and audio/video transition **UNVERIFIED**.
