# Shared research — grocery route: nearest-next vs left-to-right sweep

EDITORIAL_CANDIDATE_UNREGISTERED. Observed 2026-11-18. Original English narration, full editorial Russian translations; **not a recorded store experiment**. Source remote `main`: `67d9ed5dd63adc27250b6a286fdf40544b9a73c0`. Historical policy proposed revision in merged PR #124: `7d6bdf7702a2a241a33a21677fce29f26ada9b72` (not the current main SHA).

## Actual selection and duplicates

Checked recent remote open/closed PRs and issue titles, actual Two Ways Lab six-episode queue as dated 2026-11-12 (not verified live today), and the channel's current `BACKLOG.md`. Most recently created story PR: Nuviko #236; prior Paper #232, Two Ways #230. Consequently this turn serves Two Ways.

Ten **distinct concrete problems** were screened, not keyword variants:
1. **Grocery route:** nearest remaining item vs sweeping product positions left-to-right, including checkout, modeled path length; **selected** after reproducible counterexample.
2. **Suitcase:** roll vs fold the same garments, packed usable volume; **strongest alternative**, stronger public videos, but no honest physical measurement of compression/wrinkles for a controlled result.
3. **Group photo:** shoot groups in request order vs arrange overlapping participants to reduce people entering/leaving; finalist, but exact member sets must be sourced/declared, and payoff easily turns into abstract counts.
4. **Packing parcels:** one order at a time vs batch trips to shelves; feasible but similar to existing task-distribution stories.
5. **Robot vacuum dock:** corner versus center, deadhead path; needs actual room obstacles/charging constraints to avoid a rigged geometry.
6. **Two burners/four dishes:** short jobs or long jobs first; reproducible schedule, but results depend on assigned invented cooking times.
7. **Single shared screwdriver:** monopolize tool or hand off between workers; waiting and switch costs dominate with arbitrary inputs.
8. **Laundry transfers:** one item at a time vs shared basket, walked distance; close to published E003 carrying and #186 cleaning, rejected for overlap.
9. **Printer queue:** arrival order versus shortest jobs first, mean wait; sound queue model but adjacent to existing #217 deadlines and E001 queue.
10. **Parking:** first space vs searching for closer space, total walk/time; duplicate of existing story PR #127 and Two Ways E006, excluded.
Also excluded wrapping/ribbons (E005 and #211), checkout (E001), and USB-C (#230). No rejected Paper #13/#88 repackaged.

## Three serious candidate pitches (pre-script)

| Candidate | Exact first line / first visible event | What changes after the hook | Complete payoff | Strongest objection |
|---|---|---|---|---|
| Grocery route | “I followed the nearest item in a grocery store. Somehow, I walked almost twice as far as I needed to.” Cart arrives near checkout, one item left at far-left back | Same five locations: nearest-next picks near oil then must return for coffee; sweep wins 22 to 40. Move only oil; nearest-next wins 24 to 28 | Nearest next item is not guaranteed shortest *complete* trip; nor is fixed sweep universally optimal | Simulated unobstructed grid could feel like a math lesson rather than actual shopping; no demand confirmation |
| Suitcase roll/fold | “Same clothes, same case. Why won't the lid close this time?” Identical set beside an open suitcase | Change fold/roll placement under fixed weight and accessible-item conditions, then count which items fit *physically* | Complete A/B with visible packed capacity and ease of access | Requires repeatable actual measurements or valid 3D packing, not available; invented fit would determine result |
| Group photographs | “Why did I call the same guest back to the camera six times?” A guest returns repeatedly | Show participant sets for each requested group, compare order and entry/exit events | Count person-transitions, then explain when grouped scheduling can save time | Sets could be artificially chosen and result look predetermined; relevance narrower |

**Choice against strongest competitor:** roll-versus-fold has stronger *observed topical reach* on YouTube, and its first image can be more physical. But no actual garment/case fit measurements or accepted geometry evidence is available here. A fictional invented winner would violate the experiment contract. Grocery route has a real everyday question, reproducible arithmetic, a second-layout reversal with one condition changed, and a full result. **Still experimental**: no verified audience interest in this Two Ways treatment, no live reviewer, and the long versions risk becoming mathematical instruction.

## Current public signals, not CTR / retention

Observed by public search on **2026-11-18**; YouTube pages could not be opened directly (throttled) and none of these videos were played or their own subtitles/comments inspected. Counts come from returned indexed public metadata, not Studio today. Format length generally UNVERIFIED.

| Direct URL / video ID | Publisher and publication | Language / observed type and length | Public indexed reach / limitations |
|---|---|---|---|
| https://www.youtube.com/watch?v=G0Xo7sjp8Tk (`G0Xo7sjp8Tk`) | **Howcast**, 2012-02-06 | English grocery quick tip, exact duration UNVERIFIED | 9,704 views, 44 likes reported; very large 9.4m-follower creator; description explicitly advises organizing list by supermarket sections. Huge creator mismatch, old evergreen |
| https://www.youtube.com/watch?v=SiZ7eLVn7BI (`SiZ7eLVn7BI`) | **Natarajan Meghanathan**, 2020-04-15 | English educational nearest-neighbor traveling-salesman discussion, duration UNVERIFIED | 5,515 views, 23 likes reported, 4,160 followers; relevant to the algorithm but not grocery entertainment |
| https://www.youtube.com/watch?v=iMXRQ7yXzBY (`iMXRQ7yXzBY`) | **catherine jane**, 2019-01-17 | English fold-vs-roll luggage demonstration, duration UNVERIFIED | 73,498 views, 609 likes, 691 followers (indexed); important strong alternative, different physical-format niche |
| https://www.youtube.com/watch?v=8PQx5fXlA2w (`8PQx5fXlA2w`) | Afar, previous public metadata indexed 2022-11-14 | English packing, duration UNVERIFIED | Earlier indexed estimate 299,420 views, **not refreshed here**; no present-day comparator |

A directly relevant **non-YouTube source** is https://justinppearson.com/pages/shortest-path-grocery-shopping/ by Justin Pearson, dated **2020-04-19**, describing geometry of store aisle paths and shortest visiting routes. It is a real technical explanation **not a validation of this fictional map**. Real aisle-list tools advertise the problem: https://sortl.de/ (page privacy notice dated June 2026) and https://breezl.app/en/ (observed 2026-11-18), **self-described product claims only**, not independent measured outcomes, YouTube reach, or permission to reuse assets.

Latest search did not yield a reliable same-creator baseline of similarly aged/formatted uploads. There is **no established creator-normalized uplift**, no verified current 30/90-day view velocity, no owned view/CTR/retention data, no native audience questions/comments examined, and no measured audience demand for the exact A/B angle. All these are **UNVERIFIED**, not zero. Recent public grocery-list services indicate an ongoing practical problem, *not* a fresh YouTube trend. Free search only; **no vidIQ credits spent and no paid calls**.

## Exact reproducible fictional model — declared before comparing A/B

Grid nodes all `(x,y)` with integer `0≤x≤10`, `0≤y≤6`; every horizontal/vertical edge between adjacent nodes is walkable. Start `S=(0,0)`; checkout `T=(10,0)`. Cost `d((x1,y1),(x2,y2))=|x1-x2|+|y1-y2|`; no diagonals. Unblocked uniform grid, no 3D shelves, no item-pickup delay. Goal: **total complete walking units** for all five pickups **plus arrival at T**, not number of turns, elapsed time, waiting, or real supermarket distance.

| Item ID | Product | Baseline | Changed layout |
|---|---|---|---|
| D | bread | (1,2) | (1,2) |
| B | coffee | (2,6) | (2,6) |
| E | oil | (4,3) | **(6,3)** |
| C | pasta | (5,0) | (5,0) |
| A | eggs | (8,0) | (8,0) |

Method **A**: at each step choose the nearest remaining item by Manhattan distance; recalculate after each pickup. Method **B**: take items by increasing x-coordinate regardless of current location. Distinct x-coordinates in both layouts; none of the actual A choices tie. Both have exact same fully known layout, movement, starting and checkout costs.

**Baseline — calculated, verified:**
- A: `S→D(3)→E(4)→C(4)→A(3)→B(12)→T(14)` = **40**.
- B: `S→D(3)→B(5)→E(5)→C(4)→A(3)→T(2)` = **22**.
- B wins by 18 / A distance 45%; `40/22≈1.82`, hence “almost twice” in hook is defensible.

**Changed layout: only E moved two x columns right:**
- A: `S→D(3)→B(5)→E(7)→C(4)→A(3)→T(2)` = **24**.
- B: `S→D(3)→B(5)→C(9)→E(4)→A(5)→T(2)` = **28**.
- A wins by four units. Same A/B algorithms, items, endpoint and metric.

For optional 10m value, independently enumerated all **5! = 120 pickup permutations** on each layout, computing each consecutive leg plus checkout. True minimum **baseline 22** (order D,B,E,C,A) and **changed 24** (also D,B,E,C,A). Baseline B and shifted A achieve their respective minima **only in these exact layouts**. A's local rule not generically optimal; B's left-to-right also not. This exhaustive verification was a **deterministic offline model calculation, not a real experiment or independent script review**.

Pseudocode to reproduce:
```python
from itertools import permutations
P = {"D": (1,2), "B": (2,6), "E": (4,3), "C": (5,0), "A": (8,0)}
def d(p,q): return abs(p[0]-q[0])+abs(p[1]-q[1])
def score(order, loc):
    pts = [(0,0)] + [loc[k] for k in order] + [(10,0)]
    return sum(d(x,y) for x,y in zip(pts,pts[1:]))
for loc in (P, {**P, "E": (6,3)}):
    best = min((score(order,loc), order) for order in permutations(loc))
    print(best)
```

No animation time was derived from grid units. Real aisle barriers, crowding, checkout delays, shelf search, time, safety, cold-chain priorities, actual merchandise, and app behavior remain out of scope.

## Promise, arc and objection

**Audience:** someone who makes grocery lists and has at least once doubled back for forgotten items. No need for graph theory.
**Main question:** “Is the nearest thing to buy next the shortest way to finish shopping?”
**First visible action:** reveal five product symbols and the checkout, A cart apparently nearing checkout with unchecked coffee back at entrance (model on-screen disclosed).
**Development:** A makes locally shorter choice and strands coffee → B clears it while near entrance → B wins 22 vs 40 → oil moved two columns → A wins 24 vs 28. Longer 10m only: test all 120 orders to distinguish beating the other heuristic from absolute optimum.
**Payoff:** no universal winner: both methods respond to layout, and final checkout matters. “Nearest” is not the same as shortest *complete* trip.
**Main negative:** a five-product grid with no blocked aisles may seem made up and academic; 10m version in particular probably loses attention after flip. Reviewer has authority to reject the topic. No actual YouTube demand, measured retention, AV seam or rights-cleared images claimed.

## Protected state and downstream

No existing PR/workflow/owner rejection modified; #124 **merged** and current canonical editorial/skill applied. No exact owned video package or real production permissions assumed. 02m Short proposed editorially, but exceeds the channel's 35–50 second target; 05m and 10m are **editorial Long proposals only**, no configured Long recipe. All scripts require local runtime registration, actual independent reading, exact master approval, factual model QA read-back, audio timing and future storyboard anchored to accepted script hash. No media/TTS/Flow/MP4/upload/publication.
