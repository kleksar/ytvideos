# Subtitle grouping consultation — 2026-11-03

- Tool: ChatGPT.com in Google Chrome, project `YT Видео`
- Visible model label immediately before submission: `Extra High`
- Chat: https://chatgpt.com/g/g-p-6ae147d3975777d0-yt-video/c/6aea2b9f-72c4-83ed-a844-ecd03e328ba7
- Scope: recommend one-line semantic grouping for the exact retained EN narration; preserve all 120 words, punctuation, order and sentence boundaries; no timing or wording changes.
- Prompt: asked for grouping under Nuviko rules: one centered line; sentence-first; adjacent groups read coherently; keep relative pronouns with antecedents and do not strand articles/prepositions where the phrase fits; current spoken word amber and remaining words cream; 1440×2560, 1024 px visible line, Georgia Bold 104 px, 30 fps. Requested no timings.

## Completed answer

```text
When the sick
person was
a stranger,
you could
step away.

But what could
you do
when the person
who fell ill
lived with you?

A home,
where a person
should have been
cared for,
could become
a place
of isolation.

Not everyone
had the means
to leave.

Waiting out
the disaster
in the countryside
required money,
shelter, and people
to provide
for everyday life.

But if everyone
leaves,
who will bring
water to the sick?

Who will
bake bread?

Who will
take away
the dead?

This was
one of
the epidemic's
hardest contradictions.

Staying away
from the sick
could reduce
the danger
to an individual,
yet someone
still had
to care for those
who could
no longer
help themselves.
```

The advisor confirmed the exact 120 words, order and punctuation. It did not measure actual Georgia Bold widths; its grouping is advisory and still requires renderer-fit validation. The retained render will be constructed and validated with the local project helper.


## Geometry decision consultation

- Visible model label before prompt: `Extra High`.
- Same Chrome project chat: https://chatgpt.com/g/g-p-6ae147d3975777d0-yt-video/c/6aea2b9f-72c4-83ed-a844-ecd03e328ba7
- Prompt compared a fixed 74 px Georgia Bold size (33 auto groups; phone-equivalent 18.5 px at 640 px display height) with 104 px (47 auto groups; 26 px phone-equivalent), preserving 1024 px visible width, x=0.472, y=0.762 and current 29 px panel padding.
- Completed answer: select one fixed 74 px size throughout; the 33 groups at 74 are syntactically more connected and reduce single-word/awkward breaks. The 18.5 px phone equivalent is an acceptable readability tradeoff for bold Georgia on the dark panel. Keep `contradictions.` as a deliberate final emphasis if it remains by itself. Check the actual mobile view with Shorts UI.


## Width correction consultation

- Visible model label immediately before prompt: `Extra High`.
- Same Chrome project chat: https://chatgpt.com/g/g-p-6ae147d3975777d0-yt-video/c/6aea2b9f-72c4-83ed-a844-ecd03e328ba7
- Prompt disclosed the exact phrase width conflict at 74 px and compared a fixed 68 px size with a 17 px phone-scale reduction; no narration or timing changes.
- Completed answer: select a fixed `68 px` Georgia Bold size. At 68 px, all 31 auto groups fit, including `should have been cared for,`; 74 px breaks that clause incorrectly. Keep the single `contradictions.` card as a deliberate final beat. The 68 px text has only 3 px of width margin inside the 966 px text-safe width, so verify actual caption-state and composite bounds before render.
