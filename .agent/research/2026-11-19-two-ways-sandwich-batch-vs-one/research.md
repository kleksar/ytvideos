# Research: Four sandwiches, two finish lines
Observed 2026-11-19. Original conditional mathematical model; NOT a measured kitchen test. Channel: Two Ways Lab. No user-private values used in external searches.

## Selection before script
Audience: anyone who has made lunches or waited for the first item while a whole batch is prepared. Main metric announced before results: time for four identical wrapped sandwiches; secondary metric: time until the FIRST is wrapped. The strong twist is not a new sandwich recipe: the method that completes all four first finishes a single lunch 100 seconds later.

11 different backlog tasks screened (numbers refer to channels/two_ways_lab/docs/BACKLOG.md):
1. #51 four packed lunches, item-by-item vs stage-by-stage — SELECTED, both metrics and deterministic inputs.
2. #11 suitcase, bulk-first vs heavy-first — strong broad visual demand, but physical geometry/compression and matched measurements absent.
3. #52 two burners/four dishes, sequence for simultaneous serving — strong kitchen urgency, but safety/recipe timing data absent and adjacent to existing two-machine #246.
4. #60 pizza oven, first bake early vs fill batch — relatable, needs grounded cooking cycle/preheat inputs.
5. #80 printer long job vs short inserts — defensible waiting-time model but less universal.
6. #31 room tidy by item vs collection — overlaps room cleaning PR #186.
7. #23 first-fit vs tightest drawers — novel but overlaps first-compatible cable assignment PR #230.
8. #18 photo album grid vs variable height — layout can be modeled, weaker immediate stakes.
9. #41 meetings, chronological vs window-fit tasks — overlaps scheduling PR #217.
10. #93 six family photographs — ALREADY a story in PR #121; rejected as duplicate.
11. #37 two people/one bathroom — ALREADY a story in PR #133; rejected as duplicate.

### Three strongest finalist pitches
1. Sandwiches: open on a hungry person waiting while I start four lunches; show honest single-worker timelines, full-order winner B (157 vs186) and then first-serving winner A (42 vs142); payoff is that the objective, not intuition, decides the method. Strong objection: arbitrary switching/setup seconds; public real comparison is opposite under different conditions. No actual experiment implied.
2. Suitcase: same bags and objects, pack bulk-first vs weight-first, show one choice blocking access or wasting corners; payoff must be objectively measured useful capacity and access. This has arguably stronger visual/public interest, but neither comparable measured capacities nor real reference assets are available. Modeling fabricated dimensions as actual space-saving would mislead.
3. Two burners: four dishes should be warm simultaneously, schedule long vs short recipes with two busy burners; payoff a feasible time table or discovery that metric changes with equipment. Strong human stake but real cook-time/temperature data absent, and concept duplicates scheduling function of laundry PR #246.

Chosen sandwich after comparing strongest viable model and strongest visual rival. This is an experimental editorial hypothesis, NOT verified superior audience appeal. It can be rejected by independent reviewer if numbers feel like a lesson without human stakes.

## Actual public YouTube observations (checked 2026-11-19)
Only public search and video descriptions examined; no video footage or comments watched, no transcript accessed, no subscriber denominator mistaken for demand. All views are observed snapshots, may differ at a new date.

| Video ID and URL | Creator / published | Language, format, length | Views observed | Baseline, relevance and counter |
|---|---|---|---|---|
| https://www.youtube.com/watch?v=zmc7P8295AU — LEAN at home: sandwich making | John van Aarssen / 2013-07-28 | English title, standard video, listed edit through 5:33; full duration otherwise UNVERIFIED | 11,500 | Direct A/B description: batch 8:33, one-piece 7:45 (real reported order OPPOSITE to toy B win). No reliable normal-channel comparison. Description not playback. |
| https://www.youtube.com/watch?v=9xXny_QbFLQ — Breakfast sandwich meal prep | Noah Perlo / 2026-05-31 | EN title, Short/length UNVERIFIED | 72,121 | Food-prep adjacent, not A/B. Different audience and format. |
| https://www.youtube.com/watch?v=S8fGIWBq2_k — Your new favorite breakfast sandwich meal prep | Breakfast For One / 2026-06-20 | EN title, third-party listing says ~1min Short, UNVERIFIED actual length | 3,639 via YouTube index; ~4.1k third-party | Third-party channel median ~7.6k last 30: https://verbatext.io/channel/%40breakfastforone. Unmatched ages/mix, below median counters inflated demand. |
| https://www.youtube.com/watch?v=WpaslQEENwo — Meal Prep Breakfast Sandwiches That Blow Minds | Noah Perlo / 2026-01-25 | EN title, duration UNVERIFIED | 125,393 | Same-author rough older comparator to May; no normalized format/age baseline. |
| https://www.youtube.com/watch?v=c1fIh_4u5eQ — Do Packing Aids Actually Save Space? | Emerald's Daily Carry / 2026-05-15 | EN title, 16:16 per third-party repost (not watched) | UNVERIFIED | Rival luggage experiment, stronger tangible measurement; secondary https://www.bilibili.com/video/BV16rLs6LEwu is not proof of original data. |
| https://www.youtube.com/watch?v=d5Kh08NRaBQ — How to cook two great meals in the same timeframe! | Come On In! / 2022-05-01 | EN title, video length unknown | 4,964 | Cooking-task rival, not exact A/B; normal creator median unknown. |
| https://www.youtube.com/watch?v=2VQXr_1kPj0 — Fast two-course meal under 20 minutes | Wok with Tak / 2019-08-05 | EN title, length unknown | 416 | Second rival author; not exact A/B; counter to easy assumed demand. |

These are evergreen/Jan–Jun 2026 signals, NOT confirmed fresh 30–90 day trend. Genuine viewer comments/questions, exact like-for-like creator baseline, algorithmic growth rate, click-to-view CTR, actual retention and Two Ways first-party data: UNVERIFIED. The one relevant direct A/B video publicly reports one-piece quicker; our contrary model depends on documented input changes. No vidIQ credits or paid operations used, and no third-party wording is copied into narration.

## Fixed mathematical model, no real timing claim
One worker, four identical sandwiches, each bread preparation 10s, filling 15s, wrap 5s, each station switch 6s; A does one sandwich completely then returns to bread; B prepares all breads then all fillings then all wraps and pays 25s initial tray setup. No overlap, one station per operation, initial worker at bread costs zero, nothing after last wrap. All inputs invented but declared before outcome. Same finished 4 wrapped sandwiches.

For n sandwiches:
A all-ready = 30n + 6(3n - 1) = 48n - 6.
B all-ready = 25 + 30n + 2*6 = 30n + 37.
A first-ready = 42. B first-ready = 25 + 10n + 6 + 15n + 6 + 5 = 25n + 42.
n=1: A42, B67. n=2: A90, B97. n=3: A138, B127. n=4: A186, B157 (first A42, first B142). n=8: A378, B277 (B first242). Each n includes same operations, no hidden simplification. A finished-item checkpoints for four: 42, 90, 138, 186. Local Python checked arithmetic in this run.

Single-factor sensitivity: changing ONLY each station switch from6s to1s gives n4 A=120+11=131, B=25+120+2=147; winner reverses. At n10 and 1s, A329, B327. This is a sensitivity model, not a real new measured experiment.

## Dramatic map and refusal conditions
Hook: someone can receive a completed lunch early while the group waits longer overall. A/B declared, then inputs and metric, first ready, last ready, surprising first/last trade, clear conditional decision. Two-minute payoff completes before any proposed loop. Five minutes adds count threshold and switch-cost reversal. Ten minutes adds n8, general n and why transfer to real kitchens is uncertain; risk of a lecture after primary result.

No existing specific sandwich model PR found in public linked GitHub title search by 2026-11-19; latest #251 Nuviko, #248 Paper, #246 Two Ways. Recheck remote immediately before branch writing. Owner-rejected #13 telegraph and #88 bridge, accepted #25 Larry / #46 Apollo, and current running scripts untouched. Production requires real local runtime, fresh independent review and exact master approval.
