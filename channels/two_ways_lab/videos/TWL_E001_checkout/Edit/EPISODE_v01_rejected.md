# TWL_E001 — Which Checkout Line Wins?

**Format:** English Short, vertical 9:16. **Revision:** v01. **State:** exported for local review.

## Story and audience

Two checkout lines are in view. The viewer instinctively chooses two shoppers over five. Reveal the overlooked cost: two full carts contain more than five small baskets. With quick payments the baskets win; with slower payments the five separate transactions reverse the result. The viewer can now look at basket size and time per customer, not just heads. No knowledge of queuing theory is assumed.

The [input](experiment/input.json) fixes goods per shopper, one server per lane and no new arrivals or delays. The clock stops when the hypothetical next shopper can start; the viewer's own items aren't counted. Both rounds use the same shoppers/order and identical scan speed. This is a model rather than store data.

## Narration EN · v01

<!-- narration:en:start -->
Two people or five, which checkout line would you pick?
The line with two shoppers has twenty-five items. The other has just fourteen.
In our model, each item takes two seconds to scan. Each shopper takes four seconds to pay.
The five-person line clears in forty-eight seconds. The line with two takes fifty-eight.
Let's run it again. Same shoppers, same items. Now give each shopper twelve seconds to pay.
This time, the line with two clears in seventy-four seconds. The other takes eighty-eight.
Fast payments favor the line with fewer items. Slow payments can flip it.
So next time it's
<!-- narration:en:end -->

Text seam: “So next time it's | two people or five, which checkout line would you pick?” The comma is the pivot into the question; the hook makes sense on first play, and the conclusion lands before the link. This is a text check; audible seam is checked on the export.

## Image and edit score · v01

Open on the contrast in K02: two bulky carts against five light baskets, the warm amber lane visually longer. An elevated camera frames both simultaneously. Fixed horizon, two counters and fixed left/right lane landmarks carry through cuts. Use only discrete event states at exact model times. The navy wall holds high-contrast typographic overlays; no painted words in any source. Keep feet, cart wheels and basket grips visible at phone scale. Show both winner times long enough to read. Final line returns visually to the opening two lanes.

| Scene | Anchor (chronological spoken order) | Asset and model evidence | On-screen job |
|---|---|---|---|
| S001 | Two people or five | K02 full start | 2 PEOPLE OR 5? |
| S002–004 | The line with two shoppers | K00 → K01 → K02 | Reset visual; A: 25 items, B: 14 items |
| S005–006 | In our model | K02 → K03 (R1, 18 s) | 2 s per item + 4 s per payment; then model clock |
| S007 | The five-person line clears | K04 (R1, 48 s) | Show line B empty, A still busy; compare 58 s / 48 s |
| S008 | Let's run it again | K02 reset | Same items; change payment to 12 s |
| S009–010 | Now give each shopper → This time | K05 (R2, 40 s) → K06 (R2, 74 s) | Model clock and visible remaining shoppers; A 74 s / B 88 s |
| S011 | Fast payments favor → So next time it's | K02 | Explain flip, then return to opening composition |

## Sound

M001: friendly English narration above a quiet repeating original mallet/pluck figure. Subtle scan beeps and a small resolving accent mark each race's decisive event. Avoid register chatter and a loud victory sting. Keep narration intelligible and the repeat join continuous. Source, timing and rights are recorded with the mix.

## Evidence

- Model: [input](experiment/input.json), [events](experiment/events.json), and `python3 -m unittest discover -s experiment -v` from this episode directory.
- [Image gate and lineage](Edit/image_manifest_v01.json) · [timeline](Edit/timeline_v01.json) · [sound](Source/Audio/v01/mix-evidence.md) · [export contract](Edit/export_contract_v01.json) · [QA](Edit/QA/REVIEW_v01.md) · [reproduction](REPRODUCE.md). User acceptance applies to the exact review file when given.
