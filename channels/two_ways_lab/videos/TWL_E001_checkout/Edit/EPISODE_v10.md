# TWL_E001 — The checkout line that changes its mind

**Channel / format:** Two Ways Lab, English Short. **State:** story revision and review edit in progress. User rejected v07's story and audible seam, and explicitly chose to retain the existing voice for now. [Rejection evidence](Edit/QA/REJECTED_v07.json). New narration below is a writing draft, not the current recording and not permission to synthesize it.

## Story and viewer value

A shopper must choose between two people with full carts and five with small baskets. The obvious strategy is to count people, but the five-person line has fewer items and, under fast payment, clears first. Reset the exact comparison: when each shopper takes longer to pay, five separate payments overwhelm that advantage and the two-person line wins. The viewer can look at the amount of shopping **and** the number of payments rather than relying on queue length alone. Both results are a deliberately simplified model, not a guarantee for a real store.

Both checkouts scan in two seconds per item. The two people have 25 items total and the five have 14. Four-second payments: two-person line 58s; five-person line 48s. Twelve-second payments: two-person line 74s; five-person line 88s. [Input and event proof](experiment/events.json).

## Proposed narration N002 — not recorded

Two people or five: which checkout gets you out first?
The short line looks like the obvious choice. But those two carts are packed. The five shoppers have fewer items altogether.
Let's test both lines. Each item takes two seconds to scan. Each payment takes four.
The five-person line clears in forty-eight seconds. The two-person line takes fifty-eight. The longer line wins.
Now reset: same shoppers, same groceries. Change just one thing. Each payment takes twelve seconds.
Five separate payments add up. Now the two-person line clears first: seventy-four seconds against eighty-eight.
So don't just count people. Look at their groceries and the number of payments ahead of you.

**First listener:** the choice, surprising result, single changed rule, reversal and practical takeaway all appear in the narration. Opening and ending are complete statements. The candidate reset from the final sentence to the initial question is a thematic return, not evidence of a continuous spoken loop. A truly natural continuous seam is not yet established; redesign the start and end together before any new recording and review the actual audio at first play and across two cycles. Do not create a dangling phrase merely to force a loop.

## Retained narration N001 — current voice

The authorised existing v03 voice uses [exact narration](Source/Audio/v03/narration.txt). User wants this voice retained. Because the final words “So next time it's” were identified as an audible interruption, the review edit may remove that unfinished tail and stop after the full conclusion “Slow payments can flip it.” This is a local repair using the existing recording; it does **not** turn N001 into N002. A closed ending followed by a repeated opening is a thematic reset, not a verified continuous spoken loop. Preserve this limitation in QA.

## Visual direction v10 — retained voice

Use existing text-free scenes and separately generated transparent lettering, with the exact framing and ±2% scale / ±2° rotation channel standard. Narration and model truth have priority over the proposed unrecorded N002. The visual edit follows a clear question → hidden advantage → shared rules → first outcome → reset and changed condition → reversal → takeaway. Never imply the cart contents can be counted precisely from illustrative drawings.

| Beat | Voice anchor | Visual action / decision | Generated graphic |
|---|---|---|---|
| Hook | “Two people or five … pick?” | Shopper compares both lanes, deciding where to go. | 2 OR 5? |
| Hidden advantage | “two shoppers … twenty-five” | Close on the two overflowing carts. | 25 ITEMS |
| Contrast | “other … fourteen” | Five people with baskets. | 14 ITEMS |
| Rules | “each item … each shopper” | Same lanes, explicit shared model assumptions. | 2s PER ITEM, then 4s PER PAYMENT |
| First outcome | “five-person … fifty-eight” | Five-person line is clear, one cart still waiting; distinguish the two times. | 2 = 58s / 5 = 48s |
| Reset | “run it again … same items” | Return to both full queues. | 2 OR 5? |
| Changed rule | “twelve seconds to pay” | Same shoppers; payment time alone changes. | 12s PER PAYMENT |
| Reversal | “this time … eighty-eight” | Two-person line clears, one basket shopper remains on the right. | 2 = 74s / 5 = 88s |
| Takeaway | “Fast payments … flip it” | Return to original choice and compare both causes. | ITEMS + PAYMENTS |

## Evidence and gates

- Visual lettering comes from generated transparent PNG, never scripted typography; inspect the exact images and motion at phone scale. New labels and their hashes belong in the edit manifest.
- Existing voice, music and effects remain; only the unwanted trailing fragment is cut and the ending aligned to a full sentence. Update subtitles/SRT/timelines to the retained speech. No fresh speech synthesis.
- This edit is a review draft, not evidence that the requested story rewrite or an independent review has been completed. Naturalness of the audio and of a loop must be actually heard; do not promote the clip or mark loop PASS without that verification.
- YouTube remains deferred.
