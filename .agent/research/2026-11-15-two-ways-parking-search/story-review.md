# Author story review — exact script versions

Status: author-only editorial review, **not independent reviewer or measured audience performance**. Date 2026-11-15. Story: original conditional two-method parking model, full EN+RU as committed. Channel: two_ways_lab. Goal: 1–10 editorial judgments with exact evidence; demand and actual audiovisual performance **UNVERIFIED**, never silently scored as zero.

## Exact source hashes (full UTF-8 bytes including trailing newline)

| Variant | Language | Words | SHA-256 |
|---|---|---:|---|
| 02m | [EN](variants/02m/script.en.txt) | 309 | `57e74fe2d54d46b4797871fd1917e22448f6616c65a96b79cfb43ce21701fa90` |
| 02m | [RU](variants/02m/script.ru.txt) | 270 | `2164f3b24b71fc7d7387b4286978cf12761d3ce7f52431be268b4e5db7e1964f` |
| 05m | [EN](variants/05m/script.en.txt) | 826 | `1eb3978d050c81c9e91d6db66257a292673ae69a0db648edd0fa85bd2336f762` |
| 05m | [RU](variants/05m/script.ru.txt) | 692 | `88cc89dcf88418db75f9a45688e2cff32ae03ccb52194ee75ab1841f927687ff` |
| 10m | [EN](variants/10m/script.en.txt) | 1911 | `f8f0bb456751c8d255599c957e9759d4b73837b341e1876891ff0c043f2700b1` |
| 10m | [RU](variants/10m/script.ru.txt) | 1593 | `803ad410de49c37fd1f72d8d4ae68f3cb997edd6d24cb04a1e89e26c24a59775` |

Hash method: deterministic SHA-256 of GitHub-fetched full UTF-8 file content (pure JS implementation self-checked against the standard “abc” digest). File paths/revisions are exact; new content must get new hashes and new review.

## 02m — STRONG_CANDIDATE, recommended

1. **Интерес / значимость 8/10**, medium author confidence: clear human choice “Can the parking space closer to the shop actually get me there later?” with reversal 2:10 vs 2:40; relevant to occasional shoppers, but no audience evidence.
2. **Начало 9/10**, medium: concrete cold question stands without channel lore, immediately introduces the choice.
3. **Развитие / причина досмотреть 9/10**, medium: same-lot A130 → B160 surprises, then explicitly change one vacancy to x40 and B80; genuine second question rather than repeating fact.
4. **Payoff 9/10**, medium: “Saving walking only helps if it pays for the extra driving”; clear no-universal-winner disclaimer before final loop.
5. **Свежесть угла 7/10**, low: similar parking strategy studied in 2019; this exact controlled A/B with reversal and return-time focus is an editorial variation, not provable new discovery.
6. **Визуальность 9/10**, medium: visible first vacancy, near door, two routes and numbers, reset and moved bay; actual render/legibility still untested.
7. **Естественная речь / ясность 8/10**, medium: first-person narration and plain actions, but 309 EN words risk a dense 2-minute voice.
8. **Подтверждённый зрительский интерес UNVERIFIED**, low: no comparable creator baselines/views or own retention, no disguised audience score.

Story map: cold parking dilemma → A chooses x150 → B drives past to x120 and loses → one controlled reset moves vacancy x40 and B wins → lesson about full travel and unknown occupancy → same question naturally repeats. Main weakness: second reset needs visibly explicit graphics, otherwise perceived as moving a spot mid-run. **Loop author check:** last “I face that same question.” → first “Can the parking space closer to the shop actually get me there later?” has natural question setup, payoff occurs before it. Cold entry standalone; exact AV seam and independent double-reading UNVERIFIED.

## 05m — STRONG_CANDIDATE, alternate editorial Long

1. **Интерес / значимость 8/10**, medium: expands original paradox into “when does closer win?” and useful return-trip question, relevant even without 2m.
2. **Начало 8/10**, medium: “Why did I park closer … and still arrive half a minute later?” then asks actionable follow-up; opening longer but quick enough for Long.
3. **Развитие 8/10**, medium: A130/B160 → x40/B80 → break-even x90 → shopping return x120 ties, each changes interpretation.
4. **Payoff 9/10**, medium: measured goal changes conclusion; “how much walking will that improvement really save?” is actionable without claiming universal certainty.
5. **Свежесть угла 8/10**, low: walking home with purchases and metric switch adds legitimate perspective to parking strategy topics, but not an audience-tested novelty.
6. **Визуальность 8/10**, medium: threshold 90 metres and two independent journeys depictable; numerals could become dense at phone size.
7. **Естественная речь / ясность 8/10**, medium: I-driven explanation, natural connective reasoning, but middle calculation is heavier.
8. **Спрос UNVERIFIED**, low: public articles only and no reliable video comparisons.

Story map: question about door vs overall visit → fixed geometry/methods → A/B surprise → rerun at x40 → breakeven x90 → bags and 280/280 tie → change in goal and limits. Main weakness: calculating threshold verbally risks lecture-like pace. **Format: Long production BLOCKED** by current ChannelSpec, despite complete text. Loop N_A for Long.

## 10m — REWORK, complete editorial Long (not recommended)

1. **Интерес / значимость 7/10**, medium: familiar parking choice but audience may not want 10 minutes of symbolic toy geometry.
2. **Начало 8/10**, medium: three specific questions build a promise; some setup repeats before first result.
3. **Развитие 7/10**, medium: A/B → threshold → unknown occupancy → return-trip → slower traffic 2 m/s and different outcome; extra events are real model tests, but the second half risks rehearsing known caveats.
4. **Payoff 8/10**, medium: closes on “entire route … what I do not know about availability”; complete but payoff resembles shorter version.
5. **Свежесть угла 7/10**, low: more sensitivity cases rather than fresh human consequence.
6. **Визуальность 8/10**, medium: clear same-map counterexamples possible, but repeated identical geography loses novelty.
7. **Естественная речь / ясность 7/10**, medium: plain first person, yet 1911 words and repeated conditions make listener track too many quantities.
8. **Спрос UNVERIFIED**, low: no observations supporting 10-minute attention to same model.

Story map: initial paradox → fixed A/B → opposite vacancy layout → threshold → unknown probability → round trip → slower driving reverses winner → practical boundary. Main weakness: additional >5-minute technical material is not evidently worth its duration to general audience; should not inflate rating to force a ten-minute product. **Format: Long production BLOCKED**; loop N_A.

## Comparison and selection (author)

| Transition | True additional value | Cost / strongest concern |
|---|---|---|
| 2 → 5m | exact 90m indifference line and returning with shopping changes the objective | additional mental arithmetic after full 2m reveal; no configured Long |
| 5 → 10m | unknown occupancy, low-driving-speed counterexample and constraints of metric | attention dilution, repeated map, runtime Long blocker |

**Recommendation: 02m** as the only currently supported format. It provides a complete first-watch payoff and conditional result reversal. 05m is a valid longer explanation and maybe worth future editorial use, but not authorized production; 10m is a full version with REWORK editorial status. It is wrong to use three durations as three production approvals. Source policy: [proposed #124 at 7d6bdf7](https://github.com/kleksar/ytvideos/pull/124), not main.

## Checks, authorship, confidence

- **Model arithmetic: PASS (deterministic author check)** with fixed inputs. A130, B(z120)=160, B(z90)=130, B(z40)=80, trip A280/B(z120)=280/B(z40)=120, slow car A145/B(z40)=152; independently recalculated with a small local Python arithmetic invocation. This does not validate physically modeled parking manoeuvres, static occupancy realism or visuals.
- **Facts / historical assertions:** PASS as explicitly fictional quantitative demonstration, not an observed store result. External research about the existence of parking strategy studies is attributed in `research.md`, not borrowed as evidence for invented speeds.
- **EN/RU equivalence:** author PASS (each narration full, first-person, same A/B numbers/limits, same payoffs); independent translation review UNVERIFIED.
- **Voice, final timing, audience reaction, effective title, actual drawings and narration-image sync:** UNVERIFIED.
- **02m Short format:** config supports illustrated 1080x1920/30 and requires loop; text loop AUTHOR CHECK, independent and exact AV seam UNVERIFIED. Short length measured UNVERIFIED.
- **05m/10m Long format:** FAIL/BLOCKED for production because config has null long video canvas/fps and no compatible recipe; scripts are complete editorial candidates.
- **Third-party media rights:** no assets imported; future rights UNVERIFIED, not a completed license check.
- **Independent first-listener `ytv-script-review-v1`: UNVERIFIED.** No fresh distinct reviewer response, no trace, no proof of listening twice; self-scoring not a review receipt.
- **Iterations:** one initial original full set plus one author calculation/read-through; no independent revision rounds completed. Owner has not selected or approved any exact variant.

All numeric 1–10 scores are author judgments with medium/low confidence, NOT CTR, virality probability or measured retention. A failed required gate overrides any average.
