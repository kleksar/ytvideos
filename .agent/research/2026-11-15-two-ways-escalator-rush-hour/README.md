EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

## 2026-11-19: substantive 2/5/10-minute editorial revision

Same escalator A/B, three independent complete stories, six texts. Baseline untouched: PR branch HEAD `50d04fd1c07a6424791633376d3b78b71fff1894`; original root Short EN blob `22329cafcb78c606c2db4aba953b7c1b2608b06a` / RU blob `10e71b24fd19515dfe2d148f0bcd733419c30db5`. The root Short is a strong ~one-minute candidate, **not** a genuine 2-minute version; it remains available as a separate original rather than being passed off as 02m.

| Editorial target | Full RU | Full EN | EN words | Intended format | Author decision |
|---|---|---|---:|---|---|
| 2m | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | 290 | illustrated Short 9:16; longer than usual channel 35–50s | Strong compact explanation; text loop author-only |
| **5m** | **[RU](variants/05m/script.ru.txt)** | [EN](variants/05m/script.en.txt) | 733 | **Long — UNSUPPORTED by current ChannelSpec** | **Editorial recommendation** |
| 10m | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | 1648 | Long — UNSUPPORTED by current ChannelSpec | Complete educational breakdown, less efficient pacing |

Recommendation **05m**, not owner approval. Long production is explicitly **BLOCKED**: `channels/two_ways_lab/channel.json` has only an operative Short recipe, while `production.formats.long.video.canvas/fps` are null. Do **not** configure Long, start a Long runtime task or change channel parameters under this editorial assignment. Script variants are Git-only **EDITORIAL_CANDIDATE_UNREGISTERED**; actual `uv run ytv start` and independent reviewer unavailable to this GitHub-connected run. Old storyboard spans belong solely to original root EN/RU blob, not to any of the six new scripts. No media assets or existing media approvals affected.

No measured duration: English reading rate assumed roughly 125–155 spoken words/minute plus natural pauses; 290 ≈1.9–2.3 min, 733 ≈4.7–5.9 min, 1648 ≈10.6–13.2 min. RU rates unknown. Channel's normal Short editorial target 35–50s is an additional production-fit concern for 02m, not a reason to hide the longer editorial script. Timing, voice and MP4 all UNVERIFIED.

Status for **this one story**: unprocessed 2/5/10 contract → **six exact texts prepared** → **author script/model checks only** → **05m editorial recommendation**, independent listening/bilingual review/runtime unavailable. Do not mark entire PR production-ready or all open PRs reviewed.


---

EDITORIAL_CANDIDATE_UNREGISTERED: не соответствует официальному ytv script gate.

# Two Ways Lab — Walkers or Standing on Both Sides?

Only a prospective, researched editorial candidate, not production-authorized. The current host has a GitHub connector but no checked-out private repository at which `uv run ytv start` could be executed, so there is no authentic ytv run ID, plan_summary, read_next, task_guide, pinned reference_documents, lease or script approval. Independent reviewer via sessions.independent is also not available; author-only notes are not independent acceptance.

**Full scripts:** [English narration](script.en.txt) · [полный русский перевод](script.ru.txt).

Read [research](research.md) before adopting the claimed Holborn rates. Read [story-review](story-review.md) for author scores and unverified demand/independent review. [Storyboard](storyboard.md) is preliminary, not a media-production instruction. [Packaging](packaging-brief.md) is only a promise brief. [Handoff](handoff.md) gives the exact migration route.

This candidate must be transferred through the local project host: use current `main`, read the channel packet, run `uv run ytv start --channel two_ways_lab --format short --intent 'editorial candidate: escalator rush-hour comparison'`, ingest the exact EN/RU versions, obtain the real task packet and independent reviewer, and seek explicit script approval before media.

## 2026-11-25 revision
10m rewritten in EN/RU with concrete 2015 crowd-control and trial events, primary paper checked, 2017 press throughput explicitly treated as modeled input. 02m/05m unchanged. Current hashes and per-version comparison in [story-review](story-review.md). 05m recommendation unchanged; Long unsupported. No production or independent reviewer.


## 2026-11-25 — current 02m/05m correction
Both EN/RU revised: 02m completes answer then a new train returns the narrator to the same choice; 05m adds actual crowd holding and both separate press throughput from modeled boarding. See [current review and exact hashes](story-review.md). 10m and root/storyboard unchanged. 05m still recommended editorially; Long unsupported, no independent reviewer/runtime/approval. Previous changed-text hashes and timings are historical.
