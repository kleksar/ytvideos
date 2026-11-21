# Research: eight gift bags, one missing chocolate
Observed: 2026-11-19 (Europe/Belgrade). Model evidence is arithmetic authored here, **not a physical experiment**.

## Decision and 11-topic screening (separate actual concepts)
1. Gift bag with missing chocolate / batch weighing — **selected**. Familiar party task, visible A/B with a true metric reversal when action costs change; uncertainty: viewers may see it as an old coin puzzle.
2. Sort 40 socks now or search only when a pair is needed — strong alternative; practical but model needs meaningful repeated-use requests and credible handling costs.
3. Rotate gift-wrap paper diagonally to save material — promising clear visual payoff, but exact physical sheet/wrapping constraints require independently validated geometry.
4. Roll versus fold clothes in a suitcase — high public attention but physical packing volume cannot be inferred honestly without measurements.
5. One shared service queue versus separate queues — excluded as overlapping checkout queue pilot and requiring genuine service-time scenario.
6. Nearest grocery item versus aisle sweep — duplicate of PR #237.
7. Single-item versus batch sandwich preparation — duplicate of PR #253.
8. Assign rare USB-C cables first — duplicate of PR #230.
9. Longest task first on a shared workstation — generic timing and recent task-priority overlap.
10. Grocery bags by destination versus balanced load — real load distribution unknown.
11. Family group photograph by people versus by poses — strong potential visuals, but camera/setup cost assumptions and runtime storyboard need evidence.

Only 3 finalists were advanced. The remaining topics were screened, not claimed as fully researched.

## Competing pitches
| Candidate | Concrete opening | After the hook | Full payoff | Strongest objection |
|---|---|---|---|---|
| **Gift bags / scale** | "Eight gift bags. One missing chocolate. Which check wins?" | Individual checks locate bag #6 in six readings, group checks in three but move seven bags instead of six; the cost model flips the winner | 54 vs 31 seconds with slow readings, **54 vs 59** when moving costs more; method choice depends on metric and case | Classic logic puzzle recast as gifts; public appetite in a comparable illustrated format is weak/unverified |
| Sock sorting vs on-demand search | "I spent longer organising socks than finding the pair I needed" | First pair versus repeated searches changes savings | Explicit break-even count under fully declared sock locations | Too close to everyday organisation advice without actual observed timings; abstract invented scenario |
| Diagonal wrapping vs regular | "Same box. Same sheet. One rotation reaches the corners" | Fold geometry and offcut tradeoffs | Area/scrap comparison for specified box and paper | Real wrapping needs folds, overlap and tape, not area alone |

Selected over sock sorting because the first-result reversal is visible and the extra bag move is a meaningful second cost; sock sorting may ultimately reach a broader audience. Over gift wrapping, the mathematical assumptions can be stated without pretending a real packaging test. Strongest alternative retained: sock sorting and repeated requests. **NO claimed measured CTR, retention, shorts demand, or success probability.**

## Audiences / comparable YouTube evidence
English-speaking everyday puzzle and comparison viewers. Actual reachable page/description evidence only; **no playback, transcripts, comments or private Analytics were accessed**. All public counts are observed search-index snapshots on 2026-11-19, not real-time analytics, and can change.
| Video / URL | Author, published, language/format | Observed evidence | Baseline and counter-signal |
|---|---|---|---|
| [10 Bags Puzzle](https://www.youtube.com/watch?v=6a8uG9M3-bo) | LOGICALLY YOURS, 2017-10-01, EN instructional puzzle; runtime not independently verified | Indexed 86,341 views; 301k followers, at indexed crawl, not fresh velocity | Closest bag-specific concept, **different** challenge (ten coin bags, single weighing); author's age/format-matched normal output not established — UNVERIFIED |
| [TED-Ed counterfeit coin](https://www.youtube.com/watch?v=tE2dZLDJSjA) and [TED lesson](https://ed.ted.com/lessons/can-you-solve-the-counterfeit-coin-riddle-jennifer-lu) | TED-Ed / Jennifer Lu, 2017-01, EN animated educational Long, 12 coins | TED lesson indexed 9.26m lesson views, **not YouTube video views**; different resource & 9-year evergreen history | Large established education brand and established format, not transferable Two Ways Short signal; author's Long baseline not usable |
| [8 balls, 2 weighings](https://www.youtube.com/watch?v=JGlAp76fY7E) | Ms nata club, published 2026-07-14, English title, format not confirmed | Indexed 122 views (crawl ~2026-08) | Negative small sample, regular same-author baseline unavailable |
| [8 balls riddle](https://www.youtube.com/watch?v=DVzxrXsNiK8) | NExtIn, published 2025-02-07, English title, described #Shorts; 60 views, 2 likes | Different channel, poor observable audience evidence | Another direct counter-signal: puzzle uploads can receive very little attention |
| [Gift-wrap diagonal tutorial](https://www.youtube.com/watch?v=y_Jy61zjzqc) | Justin's Toys, published 2013-11-14, EN craft demo | Indexed 377,413 views; 281k followers | Strong competing visual promise but no matched baseline, physical verification required |

No credible 30–90-day *fresh growth* evidence. Search pages cannot establish retention, CTR, comments, watched footage, full runtime, or owner-channel performance. Baseline data absent for matching age+format of the cited authors. All popularity comparisons remain **UNVERIFIED**, and the chosen angle is an experimental creative hypothesis.

## Model: exact, reproducible
Inputs: 8 numbered bags, full weight 120g, one missing chocolate of 10g in bag **#6**, no noise; unlimited exact digital scale; exactly one deficit; measurements report summed mass. Each method resets to identical starting conditions.
- A: weigh 1, 2, ... until first 110g; if first 7 are all 120g, infer #8. Case #6 = 6 readings, 6 placed bags.
- B: weigh [1,2,3,4] => 480g, so missing is among [5..8]; weigh [5,6] => 230g; weigh [5] => 120g, so #6. 3 readings, 4+2+1=7 placements.
- Each "placement" includes set-on and remove as one modeled bag-handling unit (same convention both paths). Readings and placements charged once per modeled operation; no parallel work or distinct handling setup.
- Costs read r, bag movement p. A = 6r+6p; B = 3r+7p; B faster iff 3r > p, tie iff 3r=p.
- Slow-reading hypothetical r=8 sec/p=1 sec => A=54s, B=31s.
- Slow-handling hypothetical r=1 sec/p=8 sec => A=54s, B=59s.
- For #1 under r=8/p=1: A=9s, B=31s; for #8: A=7 readings, B=3.
- Under uniformly distributed missing position A mean readings and placements = (1+2+3+4+5+6+7+7)/8 = 4.375; B always 3 and 7. At r=8,p=1 A mean 39.375sec, B31; at r=1,p=8 A mean39.375, B59.
- For 16 bags, B 4 group readings and 15 placements (8+4+2+1); A max15, uniform mean (1+...+15+15)/16 = 135/16 = 8.4375.
- If zero or two bags are deficient, or bag masses differ, the single-defect inference is not valid; do not claim general reliability.
These are author's calculations, reproducible from table and formulas, not externally measured numbers.

## Promise / proof / answer
Early on-screen proof: eight numbered bags and a scale, with identical 120g reference bag. Show bag #6 as hidden until both choices replayed. A's 6th reading, B's three group readings, then handling ledger. Payoff: fewer readings can cost more total time, so compare both labor and measurement, with limits. No real images, references, comments, user analytics or experiments generated in this research.
