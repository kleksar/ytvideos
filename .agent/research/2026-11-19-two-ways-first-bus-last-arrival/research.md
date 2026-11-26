# Research — Two Ways Lab: The Bus That Leaves First Can Arrive Last
Observed 2026-11-19 (UTC). Editorial-only, one hypothetical A/B transit model, not a report of travelling or of actual bus performance.

## Entry and audience

Target: English-language general audience who sometimes chooses between a direct trip and a transfer. Channel is illustrated first-person A/B, not documentary travel footage. Viewer wants a practical choice when the first available departure may not be the earliest arrival. Question before writing: *Can an apparently faster route turn slower after one missed connection?* Interest is a working editorial hypothesis, not measured demand.

Canonical source main read before ideation: `d7dbf4d8de0a0719e062e72b7e21b7d3748de100`; #124 is merged, so use current main editorial. Latest observed story draft order: Two Ways #279, Paper #282, Nuviko #283; #284 is a non-story caption PR. Therefore next channel is Two Ways. Existing accepted or owner-rejected examples are not being repackaged.

## Breadth and duplicate screening

Twelve concrete choices considered, distinct mechanisms rather than title variations:

| Choice | Quick feasibility / rejection |
|---|---|
| Direct bus later versus immediate two-leg trip | **Finalist A; selected:** real choice, visible deadline and late connection reversal, exact timetable model possible |
| Nearest subway carriage versus carriage beside destination exit | **Finalist B:** opportunity to move while waiting; missing train reverses the gain, but after the first answer the 5/10m expansion is thin; no matched audience evidence |
| Two people sharing one bathroom: each finishes fully versus alternating stages | **Finalist C:** high recognition and genuine overlapping/serial-task stakes; without verified phase durations, long result depends heavily on invented service assumptions |
| First available parking spot versus searching near the door | Existing story PR #127, duplicate |
| Stairs versus elevator | Existing story PR #175, duplicate |
| One combined checkout queue versus separate queues | Existing story PR #136 and E001, duplicate/overlap |
| Grocery trip by closest next item versus aisle sweep | Existing story PR #237, duplicate |
| Laundry scheduling by batches | Existing story PR #246, duplicate/overlap |
| Order four sandwiches as assemblies versus grouped steps | Existing story PR #253, duplicate |
| Walking to the next bus stop versus waiting at the first | Both can catch the exact same bus and arrive simultaneously; risk of false payoff unless the setup proves a real difference |
| Group photograph: rearrange people by a list versus reduce moves | Backlog #93, complex comparison with unclear audience payoff and measurements |
| Pack a carry-on by length versus by weight | Backlog #11, actual usable dimensions and constraints unavailable; cannot honestly declare a winner |

No story Issues were created. Strong losing finalist B is not an owner rejection and remains eligible in another run.

## Three competing applications (before full narration)

**A — Transfer first or wait for the direct bus?** Opening: “The bus leaving first might get me home last.” I stand at one departure board at 08:00. The direct route reaches the destination at 08:35; the first departing transfer route reaches it at 08:30. A first-leg delay causes a missed connection and arrival at 08:40. After hook: calculate all waits and the two-minute walk, then introduce 3- and 5-minute delay, expose the four-minute transfer buffer, and see the result reverse. Payoff: choose B only under the schedule/connection condition; choose A under specified late-B condition; check next connecting departure in real life. Strong objection: a timetable puzzle may sound like schoolwork and the real-world delay rates are unknown. **Selection:** the concrete “five minutes faster / then five minutes slower” reversal, stable A/B inputs, and an actionable recovery rule provide a more complete middle and payoff than B. Do not claim universal reliability.

**B — Get on the nearest carriage or walk down the platform?** Opening: “I can save a minute at the destination by moving now, but I might miss the train.” Same train and station; predeclared arrival time/exit metric; track the platform walk before boarding and after arrival. Payoff depends on actual train arrival vs distance and boarding margins. Strong objection: it often just transfers walking from one station to another and may exhaust its insight in 30 seconds. YouTube targeted search did not provide enough comparable exact videos; **demand UNVERIFIED**.

**C — Two people, one bathroom.** Opening: “We both start getting ready at the same time, but we own only one bathroom.” Option A completes each person's bathroom block; option B alternates independent steps when feasible. Payoff: time until both leave, possibly a reversal if switches themselves take time. Strong objection: fair model requires full durations, resource rules and what can actually occur outside the bathroom; without credible data, the winner is assumption-sensitive. Targeted YouTube search did not yield relevant exact comparable entries; **demand UNVERIFIED**.

## Exact model and arithmetic (authored hypotheses, NOT empirical measurements)

Start = 08:00 at the same point, destination the same; score = actual arrival including all waiting, travel and 2-minute physical transfer. No real transport provider, fares, live disruptions or historical event is claimed.

| Segment | A: direct | B: first bus plus connection |
|---|---|---|
| First departure | 08:10 | 08:02 |
| First arrival/transfer | — | 08:12 |
| Walk to second stop | 0 min | 2 min, ready 08:14 |
| Connecting departure | — | 08:18; next 08:28 (unless sensitivity scenario) |
| Final arrival punctual | 08:35 | 08:30 |
| Total from 08:00 | **35 min** | **30 min** |

Math: A = 10 wait + 25 ride =35. B =2 wait +10 ride +2 walk +4 wait +12 ride =30. If first leg delays 3 min, ready 08:17 and catches 08:18 **provided boarding remains open**; arrival stays 08:30. If it delays 5 min, ready 08:19, misses 08:18, catches 08:28, arrives 08:40. On exact readiness 08:18, boarding is **not assumed guaranteed**, as published departure is not a boarding window.

Further conditional tests (10m only): moving next connection to 08:23 yields delayed-B arrival 08:35, tie A; walking 5 vs 2 minutes shrinks punctual transfer buffer to 1; fixed hypothetical distribution 70% zero delay, 20% 3-min, 10% 5-min gives B mean 0.9×30+0.1×40 =31 minutes from 08:00 and a 90% chance of arrival before 08:36. A, **held on time by design** in that single test, takes 35 minutes and meets that deadline 100% **in-model**, not in real transit. With A itself delayed 6 minutes and B delayed 5, A arrives 08:41 and B 08:40. No probabilities are inferred from operators.

Threshold: normal slack = 08:18 − (08:12 + 2m) = 4m. Safe boarding needs the arrival **before** the departure, with additional buffer in real life. A 5m first-leg delay makes B 10m later than punctual B and 5m later than A. Fastest timetable and reliability for a stated deadline are different optimization problems.

**Reproducibility:** For B, compute `ready=12 + delay + walk` minutes after 08:00; select the earliest connecting departure strictly after `ready`; final arrival is that departure +12 minutes. For A, final =35 minutes unless an explicit independent A delay is introduced. No random trial or measured data.

## Sources read (general mechanics; none validates invented clock times)

1. [Apple Support — Get transit directions in Maps on iPhone](https://support.apple.com/en-tm/guide/iphone/ipha44f57caa/ios), accessed 2026-11-19. Transit journeys expose departure time, connections and fares; used only to establish the practicality of checking itinerary components, **not** as actual data for our timings.
2. [Google Maps team, 2017-12-14 — step-by-step transit navigation](https://blog.google/products-and-platforms/products/maps/never-miss-your-stop-again-step-step-directions-transit-navigation/), accessed 2026-11-19. Official product explanation identifies stop and transfer notifications. Does not validate service probabilities.
3. [BusConnects Cork network-design public consultation](https://publicproject.net/openhouse/bus-network-cork), accessed 2026-11-19. Public-facing discussion of shorter walks vs shorter waits, rather than universal priority for direct service; it is context only, not evidence of this simulation's values.

Source claims in narration: **all exact 08:xx times, delays, boarding margin, frequency and probability inputs are constructed model conditions and reproduced algebraically here**, not sourced real-world events. The real-world caveats on service status, accessibility and fares are conditions to verify rather than claims about a specific route.

## YouTube audience evidence (public search metadata only; not video watched)

Observed via YouTube search indexing 2026-11-19; indexed view totals may predate observation, and indexing is not Studio analytics. Only titles/descriptions/metadata surfaced; direct video fetch was blocked or throttled. No transcript or comments read. Comparable mainly in **transport A/B question**, *not* in Two Ways 2D narrative format.

| Link/ID | Creator; language / format; publication | Indexed views | Use and limitation |
|---|---|---:|---|
| [Bus Vs Train Vs Tram — The Race To Meadowhall](https://www.youtube.com/watch?v=m5R6lk3s5oE), `m5R6lk3s5oE` | And More Central; English; race video; 2021-05-01; precise runtime UNVERIFIED | 17,706 | Small-to-mid transport audience, older evergreen race; not specific to transfers |
| [Korea Express Subway GTX vs Express Bus](https://www.youtube.com/watch?v=wGeZk695cRA), `wGeZk695cRA` | Dosigyotong; Korean; transport race; 2024-05-17; runtime UNVERIFIED | 372,578 | Strong adjacent demand in Korea, much larger/older video; irrelevant as direct English-channel forecast |
| [I cross London using EVERY mode... (Part 1)](https://www.youtube.com/watch?v=1Bmq12MXOWo), `1Bmq12MXOWo` | Backpack Travels; English; travel challenge; 2026-07-04; runtime UNVERIFIED | 2,383 | Relatively newer small creator; not same exact B-vs-A decision |

Baseline attempt: [And More Central channel-introduction video](https://www.youtube.com/watch?v=dKSuw21VMZo), published 2025-07-28, indexed 2,294 views. **Not a format- or age-matched ordinary episode**, so it cannot establish lift. No reliable same-creator same-format same-age baseline retrieved for the other two authors. Thus uplift, baseline-normalized popularity, growth speed, click rate and retention are all **UNVERIFIED**. No 30–90-day exact topic match was confirmed in the limited search; this is NOT a statement that none exists on YouTube. July 2026 ≈4.5 months old, an older signal, not fresh 30–90-day demand. No actual viewer questions/comments accessible — **UNVERIFIED**.

**Counter-signals:** audience may be niche transport enthusiasts; indexed searches do not validate general-interest 2D Shorts; the strongest transport race video is Korean and from a channel with an existing audience; a 30m-versus-35m arithmetic puzzle can feel low-stakes. Use title that asks about the single missed transfer, not exaggerated “shocking” safety claims.

## Decision and editorial boundaries

**Selected as an experimental editorial hypothesis**, not proven high-demand topic. Variant 02m carries a clean, usable conditional payoff and a logical return to the first decision; 05m earns space for buffer/late-connection logic; 10m contains further genuine scenario analyses but its reflective second half may lose viewers and should be graded separately. No explicit owner selection or script approval is implied.

Do not claim real schedules, real delays, race footage, probability findings, true testimonials, measured time, presenter travel, reliable transit guarantees, or preview-CTR inference. No video footage, images, audio, screenshots, user data, or paid vidIQ credits acquired. External search used only generic public transit phrases.
