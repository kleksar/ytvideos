# TWL_E001 — Which Checkout Line Wins?

**Format:** English Short · **story/narration v02:** draft · **visual direction v02:** draft · **status:** revision after owner feedback. [v01 rejected record](Edit/EPISODE_v01_rejected.md).

## Viewer and story

A shopper wants to reach a checkout sooner. Two people are ahead in one line, five in the other. Counting heads suggests the short line, but the two carts are full and the five shoppers each have a few items. In a simplified model with the same scan speed and quick payments, five shoppers clear first. Restart with exactly the same shoppers and items, and change only payment time: five payments now cost enough to reverse the outcome. The viewer learns to notice both item count and the number of payments. This is a model, not a promise about any real checkout.

Hook: put the viewer inside the familiar choice. Stakes: which line reaches the register first. Turn one: the apparently longer line wins. Turn two: slower payments reverse it. Resolution: both basket size and transactions matter.

## Narration EN · v01 / N001 — retained audio

User explicitly chose to keep existing sound. The retained recording uses this exact text. The v02 narrative above is the staging intent, not a replacement voiceover.

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

Text seam: “So next time it's | Two people or five, which checkout line would you pick?” The outcome is complete before the final link. Subjective listening remains unverified.

## Visual direction v02

One coherent illustrated supermarket, expressive recurring shopper holding a small basket. The viewer always understands that the compared time ends when the next shopper can start, not when the shopper has paid. Cashiers are staff and not counted. A is left, B is right. Model figures derive from [events](experiment/events.json). Three-dimensional clarity through illustration, no Paper styling. The first-viewer test should remain clear without the text overlays: each image shows an action, result or change of conditions. As needed typography is generated as part of an image or as a separate generated graphic, never drawn by code.

| Scene | N001 anchor | Visual action and shot | Text / state |
|---|---|---|---|
| S101 | “You're at the checkout” → “Which do you choose?” | Medium foreground shopper hesitates, eyes move between two readable lanes; two full carts vs five baskets. | Generated “2 OR 5?”; A2/B5. |
| S102 | “The short line looks tempting” → “twenty-five items” | Close on two loaded carts, shopper notices groceries; show a physical sense of volume. | Generated “25 ITEMS” if legible; no claim of visually counting exact contents. |
| S103 | “The five shoppers” → “fourteen between them” | Five distinct shoppers with small baskets, next to counter; visual relation to S102. | Generated “14 ITEMS”; A2/B5. |
| S104 | “Let's model it” → “four seconds per payment” | Same checkout counters and people, first round begins. The model assumptions appear as generated legible graphic cards. | “2s / ITEM”, “4s / PAYMENT”; model assumptions apply equally. |
| S105 | “five-person line clears” → “two-person line takes fifty-eight” | Right lane has cleared, one shopper remains left; our shopper sees that right is free. | “48s” and “58s”, B wins; model time 48s, A1/B0. |
| S106 | “Now rewind” → “twelve seconds” | Return to same start with same seven people; show change of one payment parameter. | “4s → 12s”; A2/B5. |
| S107 | “This time” → “eighty-eight” | Left lane clear; one of the original five remains at right. Our shopper sees left is free. | “74s” and “88s”, A wins; model time 74s, A0/B1. |
| S108 | “Fewer items” → final “when” | Shopper sees both a full cart and basket line; a thoughtful glance conveys both factors and returns to first choice. | Minimal text only when it adds meaning; no invented certainty. |

Camera pass: first scene establishes both choices and hero’s gaze. Subsequent closer views reveal the hidden advantage; outcome compositions return to both counters so who is still waiting is visible. The reset is explicitly signalled, then the opposite outcome is staged from the same spatial orientation. Final returns to the decision. Narration anchors in this first direction pass describe the proposed v02 text; they must be remapped to the retained v01 recording before production. This is a storyboard check, not acceptance of actual images. Inspect the early images individually and in connected order before making the rest.

## Sound

Maintain the same subtitle treatment as v01 while conforming literal captions to the new recording. Use a coherent playful music bed and small checkout accents. The narrator needs a natural pause for the viewer’s choice, contrast at each reveal and an unforced loop seam. Exact music, source, rights and mix are documented after production.

## Evidence and open work

- Experiment source: [input](experiment/input.json), [events](experiment/events.json), model tests.
- New images, edit, export, subtitle fit, phone playback and QA are not yet accepted or complete. The existing voice and mix are retained by explicit user decision. Prior v01 was rejected; preserve its historical evidence without using its title-card builder as a current process.
