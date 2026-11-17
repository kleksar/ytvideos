# Story review — exact completed editorial variants

**Reviewer identity:** writing assistant, **self-review only** (2026-11-17). No independent reviewer session, `ytv-script-review-v1` receipt, actual narration listening, runtime script gate or owner approval; these are all `UNVERIFIED`. Source `main`: `fe4460045cae21f192b6d539ac9bfe36b536fd6c`. This is not a measured prediction of CTR or retention. Scores are editorial judgments, NOT audience metrics.

## Exact version identities

| Editorial target / channel format | EN words, SHA-256 | RU words, SHA-256 | Verdict |
|---|---|---|---|
| 02m / Long 16:9 | [294 EN](variants/02m/script.en.txt), `9cd6b0ed99c5db5c1e4aa089b032e31eccd6380aa09e17c4a6d364cb119d8b1f` | [247 RU](variants/02m/script.ru.txt), `c8fa560a1472e1d345b6c9d3d051d5ec8e0fa2f59e2bfe9a16c53bc497e46aa6` | STRONG_CANDIDATE |
| **05m / Long 16:9** | [553 EN](variants/05m/script.en.txt), `ae9f50e33ca5aa3332ee602ae62c4f9f3fb8dc3ca5c3de3f9e70cec9156ab446` | [474 RU](variants/05m/script.ru.txt), `db645b8e863b8d067aaf5559829f90ed4d844e462f708ba6846e4d9adf648485` | **STRONG_CANDIDATE — recommend** |
| 10m / Long 16:9 | [1,158 EN](variants/10m/script.en.txt), `438bb53382beba5c6eaf0d95bcd3baaf6f28fc820c2289ce6c4ed0566805eb57` | [941 RU](variants/10m/script.ru.txt), `d427a2343e03d8b1d9ec224b5e25717b7aee8f252bf091cb877b6663d907e8dd` | REWORK |

All English prose is production-language narration, all RU are complete semantic translations, not summaries. EN and RU lengths differ naturally by language, not a missing version. Links/hash identities refer to byte-exact current files at this commit. If edited, hashes and review require renewal.

## 8 editorial dimensions (1–10 or UNVERIFIED)

The observations cite exact phrases in the respective full EN texts. Confidence: *medium* for author artistic judgments, *high* for checked direct textual observations, *low/UNVERIFIED* for audience demand. Author: writing assistant. Scores do not substitute for blind independent review.

| Criterion | 02m: judgment + evidence | 05m: judgment + evidence | 10m: judgment + evidence |
|---|---|---|---|
| Interest/significance | **9**: “within moments the other two stopped”; real everyone-survived stakes | **9**: all engines die, and the pilot later faces an unusable view | **9**: multiple distinct technical emergencies and full survival |
| Opening | **8**: precise question on engines/radar, but three questions densely packed | **9**: “And why did the crew still have to invent a way to land almost blind?” promises second turn | **8**: three meaningful questions, but the story needs more time before all four fail |
| Development / reason to continue | **8**: failure → altitude choice → restart → opaque glass, very compressed | **9**: extra oxygen-mask pressure and 12,000-ft decision materially change stakes before second landing problem | **7**: useful added mechanics, but the extended ash/radar explanation slows momentum after the main emergency |
| Payoff | **9**: distance/chart calls and landing answer both promises | **9**: distance/height improvised guidance answers the new conflict | **9**: landing is earned through specific procedural actions, not a generic miracle |
| Freshness of angle | **7**: 'no storm on radar' is common in existing coverage | **8**: frames **two problems caused by one cloud**, especially nearly blind landing | **7**: lengthy mechanics overlaps available Mentour-style content |
| Visual expressiveness | **9**: glow, instruments, descending airplane, damaged windshield | **9**: distinct ash mechanisms and cockpit distance/altitude dialogue | **9**: photo-real historic environment + 2D outside narrator can explain mechanism without impersonating witnesses |
| Naturalness/clarity of speech | **8**: accessible, though compact engineering summary | **9**: short connected actions; “The emergency appeared to be ending. Then…” signals the honest second conflict | **8**: sentences are generally speakable but some explanatory paragraphs become dense |
| Verified viewer demand | **UNVERIFIED**: disparate indexed videos are not matching-performance evidence | **UNVERIFIED**: outliers among different-sized channels; no own analytics | **UNVERIFIED**: Mentour 40m success does not validate our 10m variant |

**Main weakness per exact version:** 02m compresses emergency crew decisions so rapidly that it may play as summary despite full payoff. 05m has limited distinct action between the failure and relight; 553 EN words may play shorter than 5m at the pinned voice pace. 10m is a complete text, but its detailed technical middle can sound educational after the central surprise; 1,158 words may fall short of 10m at the real voice speed. All judgments by writing assistant, medium confidence.

## Story map per version

- **02m**: initial radar-versus-engines questions → odd glow → four failures → potential ditching at 12k → relight → opaque glass/ILS complication → computed approach → safe Jakarta landing → ash/radar mechanism.
- **05m**: questions promise second problem → glow/smoke → engine loss → altitude and oxygen-mask choice → ditching boundary → ash explanation → restarts → visual/ILS failure → distance/height calls → safe landing and two-stage understanding.
- **10m**: three questions → explanation of storm-radar limit → strange symptoms → four engine failures → finite-altitude glide → mountains and oxygen issue → 12k choice → ash erosion and melting mechanism → restart → single engine shut down → damaged windows and unavailable ILS vertical guidance → improvised distance/height approach → landed safely → causal synthesis.

All variants: documentary Long question-led intro followed by substantive situation before the central failure, no Short loop claimed; `loop=N_A` as Long. No separate end-card narration is included; channel profile requires a **10-second Long end screen** after story end.

## Incremental value and loss of attention

| Transition | What is gained | Where attention could be lost |
|---|---|---|
| 02 → 05 | Oxygen-mask problem, reason to descend faster, clearer ash mechanism, distinct landing puzzle, more comprehensible calculated approach | Between 12k decision and engine restart if explanation takes too long |
| 05 → 10 | Detailed limits of radar, why gliding costs height, separate effects of abrasion and engine deposits, full distance/height approach chain and cabin context | Just before the ash science block and again during the retrospective recap after landing |

**Recommendation: 05m** editorially, not the longest by default. It preserves interest/development/payoff >=8 on concrete events. 02m remains equally legitimate for a shorter release. 10m REWORK; further material needed to make the longer explanation compelling without repeats. Maximum author revisions performed here: initial drafting and one self-edit, **not** two fictional external reviews.

## Orthogonal gates

| Check | 02m | 05m | 10m | Evidence/limit |
|---|---|---|---|---|
| Fact/source match | PASS (author source check) | PASS (author source check) | PASS (author source check) | Source-to-event matrix in [research](research.md), not independent historical peer review |
| EN/RU meaning match | PASS (author check) | PASS (author check) | PASS (author check) | Same 4-engine sequence, altitude decisions, ILS failure, outcome; no contradictory extra scenes |
| Channel format | PASS (editorial 16:9 Long) | PASS | PASS | `channels/nuviko_history/channel.json` supports illustrated Long. Does not assert runtime registered |
| Shorts narrative loop | N_A | N_A | N_A | All three designated Long, not mislabeled Shorts |
| Independent blind review | UNVERIFIED | UNVERIFIED | UNVERIFIED | Separate reviewer unavailable; **no invented first-listener result** |
| TTS runtime exact timing | UNVERIFIED | UNVERIFIED | UNVERIFIED | No TTS; pinned voice 1.10×, pauses unmeasured |
| Rights / visual provenance | UNVERIFIED | UNVERIFIED | UNVERIFIED | No generated/downloaded/archive image bytes. Actual Nuviko references must be checked before visual production |
| Script approval / official gate | UNVERIFIED | UNVERIFIED | UNVERIFIED | Git-only editorial queue; no `uv run ytv start` or approval |
| AV seam | N_A for Long | N_A | N_A | No Short loop; actual end-card assembly also unverified |

Nominal timing based on EN speech rate 115–150 words/minute plus a **separate** 10s Long end-screen yields broad rough ranges 2.1–2.7 / 3.9–5.0 / 7.9–10.2 min. Actual timing cannot be claimed. The 10m editorial target could be shorter than ten minutes; do not add empty narration or alter voice speed to force an exact number. If real TTS misses target materially, revise only with proven new content and re-review on changed hashes.

## Independent review handoff

Give a fresh reviewer **only one pair of exact full scripts per task without this scorecard or author's beat map**, starting with opening and then full text. Ask for unprompted audience/interest verdict, concrete sentence where watching would stop, paraphrase of what changed after engines came back, and exact payoff. Supply factual sources **after first read**. For Long do not fabricate loop review. Reviewer must write authentic existing-schema result; a self-check cannot make this PASS. A revised hash invalidates the old result.
