# Shared research — six chores, equal count vs equal time

**Observation date:** 2026-11-18 UTC. **Source policy:** repository main `7c94f825056b98cb65d8de94dd3eec709cc78188`; PR #124 merged 2026-11-16, so current main rules apply. **Topic:** original household **simulation**, not historical event. All minutes are author-defined parameters, not measured persons, actual timestamps, or scientific claims. No source dialogue or third-party wording is reproduced in narration.

## Candidate funnel (real distinct story problems)

Main backlog read in `channels/two_ways_lab/docs/BACKLOG.md`, plus recent open/closed GitHub PRs. Actual 11 screened: (1) equal number vs balanced duration for two household helpers (#46; **chosen**); (2) airplane boarding rows vs alternate order (strongest reach alternative but real throughput depends on unavailable passenger/aisle assumptions); (3) suitcase heavy-first vs bulky-first (#11, requires independently specified weights/shape constraints); (4) one bathroom / two people sequential vs alternating (#37, credible but many room-use timings speculative); (5) scarce charger ports first-compatible vs least-flexible-first (#6, small model with less familiar stakes); (6) two burners / four dishes scheduling (#52, nice visual but heat/cook sequencing sensitive); (7) separate vs common supermarket line (#71, already overlapping #136); (8) family photo grouping (#93, duplicate #121); (9) parking first free vs nearer entrance (#88, duplicate #127); (10) chores shortest-first vs deadline-first (#43, recent #217 duplicates); (11) gift paper straight cuts (#15, covered #211). **Only three finalists advanced:** household work, boarding and suitcase; rest screened but not misrepresented as equally researched. Previously rejected telegraph #13 and bridge-before-canal #88 were not reintroduced. No prior selected script displaced.

| Finalist | First spoken/visible event | Development after hook | Full payoff | Strongest objection |
|---|---|---|---|---|
| **Two-person chores** | “Three chores each.” Two clocks end six minutes apart | Equal count fails → rebalance into two 14-minute allocations → room-switch penalty flips outcome | 14 vs 17 without switch; 17 vs 18 at 4m switch; boundary s=3 | Assumed minutes and artificial penalty; viewers may see arithmetic as elementary |
| Airplane boarding | Two boarding plans and a plane full of people | Passenger conflicts, aisle blocking, baggage delays and ordering | Simulated complete boarding times under explicit collision rules | Greater public interest but no comparable defensible actual passenger timings; CGP Grey already demonstrates a powerful version, and simplistic model could mislead |
| Suitcase fit | Same carry-on, six physical objects | Heavy-first vs bulky-first placements and unused void | Number fitted while meeting both weight and geometry constraints | Without precise object dimensions and validated placement solver a ‘winner’ is invented |

**Decision:** chores model is completely auditable and gives a counterexample rather than a generic lesson. Its strongest competitor, boarding, has clearly stronger public evidence of topic interest; chosen is **not claimed to have superior measured demand**. The selected angle is an explicit **experimental hypothesis** about conversational relevance, *not proof of viral interest*. Can be illustrated as a first-person two-column timeline; no need for actual household footage.

## Available YouTube / audience signals (not viewed videos)

Only public search-index metadata and the referenced archival metadata were available. No actual video was watched, no transcript/comment text inspected, no audience interviews, and no YouTube Studio analytics. Published dates and views are recorded as observed by available search sources; counts change. A current video landing-page listing is not evidence of viewing the video.

| URL / video | Author / language / release / type | Public observed metric, source | What comparison really means |
|---|---|---|---|
| https://www.youtube.com/watch?v=luviZ1Iqkw0 | Citytv, EN, 2016-05-18, household advice, video duration **UNVERIFIED** | 29,434 views, verified YouTube search result 2026-11-18 | Everyday problem recognized; advice format != illustrated numerical A/B |
| https://www.youtube.com/watch?v=MTWXHu9jO78 | SciShow Psych, EN, 2017-05-22, housework/roommate psychology, duration **UNVERIFIED** from direct YouTube search | 156,559 views, verified YouTube search result 2026-11-18 | Stronger topical hook but very different production, author size 872k followers |
| https://www.youtube.com/watch?v=jgfUTibT4qQ | The Financial Diet, EN, 2025-09-10, 01:01 housework fairness | 49,200 views and 85 comment **count only** in https://nerdfighteria.info/v/jgfUTibT4qQ/ (index 2026-11-18) | Closest practical topic/short length; not experiment; discussion content **UNVERIFIED** |
| https://www.youtube.com/watch?v=t7WCx6TIQBA | The Financial Diet, EN, 2024-01-31, household equity short, duration **UNVERIFIED** from YouTube | 28,099 views, YouTube search result crawled ~2026-01; direct search checked 2026-11-18 | Same-author topic-format **loose baseline**, upload age differs, cannot normalize or infer trend |
| https://www.youtube.com/watch?v=oAHbLRjF0vo | CGP Grey, EN, 2019-02-04, airline boarding explainer | 37,234,567 views, YouTube public search 2026-11-18 | **Competitor / upper-reach counterexample**, huge creator+age outlier, no forecast for this channel |

**Baseline limitations:** same-author short comparison is 2025 vs 2024 with different topic framing and audience age. SciShow and Citytv are not comparable channel benchmarks; CGP Grey is even less so. No 30–90-day fresh comparable household experiment was verified. Search snippets and comment **counts** do not establish actual audience questions or comment content. Engagement rate, CTR, retention, current velocity, causation, satisfaction, creator-standard median and target channel demand are **UNVERIFIED**; don't infer from views/subscribers. Public search interest is plausibility only. No paid vidIQ/credit operations or purchases.

## Deterministic source model and complete calculations

All six named tasks are independent, atomic; two people start together and work at identical fixed rates. Work cannot be shared or overlapped within a single person. A worker completes only assigned tasks unless a **separately identified sensitivity case** explicitly relaxes assignments. The metric is the **makespan** (time the *last* worker finishes), not average idle time, sum of jobs, number of checks, difficulty or effort fairness. The initial travel to first workplace is equal and excluded in both rules; tool/switch penalty counted only at intra-session room transitions. In B kitchen tasks performed first, then living-room tasks, so one mid-session transition per worker. No travel time measured.

| Location | Task | Assumed duration | A owner | B owner |
|---|---|---:|---|---|
| Kitchen | Dishes | 8m | I | I |
| Kitchen | Wipe counters | 3m | I | Helper |
| Kitchen | Sort shelf | 6m | I | Helper |
| Living | Put away shoes | 2m | Helper | I |
| Living | Vacuum | 5m | Helper | Helper |
| Living | Fold blankets | 4m | Helper | I |

A: kitchen 8+3+6=**17**; living 2+5+4=**11**; finish max=**17m**, helper idle by end=6m. Each gets exactly 3 tasks. B: I 8+2+4=**14**; helper 3+6+5=**14**; finish **14m** when switch cost 0, theoretical minimum total 28 person-minutes/2 people. For additional switch overhead `s` minutes **per B worker**, A=17m, B=14+s minutes. `s=1 → 15`, `s=2 → 16`, `s=3 → 17 tie`, `s=4 → 18 A wins`. This does not mean ordinary walking takes four minutes: `s` may include equipment reset, and is an explicit hypothetical.

10m sensitivity: vacuum task revised to 9m, **after fixed assignment**: A kitchen17, living2+9+4=15 → makespan17. B I14, helper3+6+9=18 → makespan18. If times **known before assignment** and re-optimized: total32, two balanced sets (8+6+2) and (3+9+4) =16 each before switching. Flexible *third rule* (not secretly counted as original A) could assign helper counters3 at minute11 while I works kitchen shelf8–14 after dishes0–8; helper finishes at14; transition and tools would need accounting. These scenarios must be labeled separate, not pooled into an invented filmed test.

**Data limitations:** No empirical task completion or travel durations were recorded. A/B cannot generalize to different homes, people, ergonomics, dependent chores, tool conflicts or fairness feelings. No tested physical optimization is claimed. The model is original arithmetic; source requirements are derivation and explicit assumptions. Scripts should preserve essential condition when results are mentioned.

## Causal map / viewer value

Original six assignments → equal checkbox distribution leaves six minutes of imbalance → balanced sums make both finish fourteen → switching reveals a hidden time cost and reversal → payoff: count total work **plus transitions**, don't confuse counts with equal effort. In 5m lower bound clarifies why 14 is optimal; in 10m wrong estimates and permitted reassignment show where a crisp rule breaks down. Strongest objection is **small mathematical stakes/low novelty**: if blind first-listener says they know the result at first clock, reject/rework rather than boost scores. Status of independent viewer interest **UNVERIFIED**.
