# Clever Hans — editorial variants, current status

## 2026-11-20 — substantive 10m Long revision (unapproved editorial alternative)

**Baseline:** PR #21 HEAD `199cd39d3b79e2b968ef4643c5715c12aae10ac6`; root scripts/13-shot storyboard and 02m/05m variants preserved byte-for-byte. Previous 10m SHA-256 EN `da092c0c9ffe987b559110add2826f93fc4e5a6e509c2e38e5956906fdc5b034`, RU `0782ec4dc60cf0f2a616c772ad84c885d4418bd7a0264f4464f44f9ca89324b2` superseded **only for 10m**.

**Before → after:** the written-word paragraph repeated the already understood known/unknown-card result. The 10m now shows Pfungst's *split-addend* arithmetic experiment: von Osten and Pfungst whisper different addends to Hans so neither knows the sum (3/31 correct), then repeat with humans knowing the sum (29/31). Later the two competing examiners supply two observable outcomes, 5 versus 8 and 7 versus 4; when Pfungst walks away, Stumpf can elicit his number again. These are new specific actions, not a second version of the same fact. The opening questions → immersion → core experimental hook remain, and the later bodily-signal reversal remains the climax. Added evidence is from Pfungst's original Ch. II, not inferred motives.

**Six exact files and SHA-256:**

| Target | Complete RU / EN | EN words | SHA-256 EN | SHA-256 RU | Status |
|---|---|---:|---|---|---|
| 02m / Short | [RU](variants/02m/script.ru.txt) · [EN](variants/02m/script.en.txt) | 190 | `7e053631046138ae48664c25c91f26becf8c90953bd219c5b695ff652ed759e2` | `3f8055c050e2f40820e8d813cd46e864dedd292af475a374239f8c5a13ba77ae` | Unchanged; provisionally recommended; loop independent/AV UNVERIFIED |
| 05m / Long | [RU](variants/05m/script.ru.txt) · [EN](variants/05m/script.en.txt) | 667 | `1f872d933deb459eff802ab455f101eb8e037c824963984dda0cbca9f8039a13` | `8959d978b857ac7bf5522f2392862e074d13525a3d2508927c57974a5d40a2b9` | Unchanged; extra controlled cue testing |
| 10m / Long | [RU](variants/10m/script.ru.txt) · [EN](variants/10m/script.en.txt) | 1398 | `4ca7f0d4a130f3a03b801f2dde036d970c91b689ee14a076dbd9718a2421cbbf` | `7bb5f973632e2443dcd8ece91df34138a47c3518ff10babf326f310aaf82ab7c` | Revised; evidence-backed split-sum and two-questioner experiments; not owner-approved |

**Story maps:** 02m: visible head change → owner absent → human knowledge withdrawn → visual cue blocked → Pfungst imitates → return to head movement (unchanged). 05m: questions → commission limitation → card 98/8 → silence → visual 89/6 → micro-cue → thirteen becomes twenty → human re-creation (unchanged). **10m revised:** questions → trainer's conviction and commission limits → card control 98/8 → *two whispered addends, hidden total, 3/31 versus 29/31* → silent-question test → blinder test 89/6 → first visible involuntary head cue → deliberate 13→20 manipulation → *Pfungst/Stumpf simultaneous expected numbers and Pfungst's exit* → physical movement record → Pfungst as human Hans → limits of conclusion. Each is the same single historical story.

**Eight editorial scores for the exact revised 10m (author judgment, not independent attention measurements):**

| Criterion | Score /10 | Evidence, weakness and confidence |
|---|---|---|
| Interest/significance | 7 | Real epistemic trap is broadly useful, but a horse experiment becomes specialist over ten minutes; MEDIUM |
| Opening promise | 7 | Three explicit questions precede the 1904 horse and introduce honest doubt, but the first observable hoof tap comes after setup; MEDIUM |
| Development/reason to continue | 7 | Split whispered addends changes the meaning of arithmetic proof; competing humans and walk-away outcome provide a later distinct test; number series still risk repetition; MEDIUM |
| Payoff | 8 | Deliberate 13→20 over-tap and human hand imitation demonstrate the involuntary mechanism; conclusion does not claim animals are unintelligent; MEDIUM |
| Freshness of angle | 7 | Specific blinded summands and competing observers extend the well-known horse anecdote without asserting a new discovery; MEDIUM |
| Visual expressiveness | 8 | Two whispering questioners, an unknown sum, horse selecting Stumpf versus Pfungst, hoof taps and tiny head gestures support different paper scenes; proposed scenes not produced; MEDIUM |
| Natural oral clarity | 7 | Sequential concrete actions replace abstract 'word tests'; four fractions/percentages and multiple names may still challenge a first listener; MEDIUM |
| Independently measured audience interest | UNVERIFIED | No comparable own-channel Long impressions/CTR/AVD, watch curves or external reviewer evidence |

**Three-duration comparison:** 02m gives the complete mystery and a deliberate replay after payoff. 05m adds measured accuracy, sight and deliberate overshoot but risks slowing when two statistical series follow each other. Revised 10m adds **two distinct tests unavailable in 05m**: neither human knowing an arithmetic sum, and the same horse switching which examiner controls it. The probable loss of attention remains after the deliberate 13→20 test, where head-motion recording and laboratory recreation extend an already-solved mystery. **Editorial recommendation remains 02m** for first-time Paper viewers, with 10m as a defensible documentary alternative, not forced production. Counts estimated at 125–155 English wpm plus pauses; 10m estimated 9.0–11.2 minutes before pauses/end-screen; NOT_MEASURED.

**Hard checks:** full 10m EN/RU cause/order/numbers AUTHOR_CHECKED; 02m full-text loop retained unchanged, independent twice-through EN/RU UNVERIFIED and AV seam UNVERIFIED; 05m unchanged; 10m Long loop N_A; first-listener and bilingual independent reviews UNVERIFIED for exact new hashes; TTS/audio timings UNVERIFIED; audience demand UNVERIFIED; owner approval NOT_RECEIVED. Storyboard S001–S013 remains scoped ONLY to unchanged root; no 10m scene spans, timing or visual media exist. `EDITORIAL_CANDIDATE_UNREGISTERED`, no official `ytv start`/receipts. New exact 10m hash requires fresh independent review. Next action: independent first-listener receives scripts without scores/verdict, then source for factual checks; only after owner selection use canonical runtime/pins to register one script; other PRs, especially #77/#78 technical, remain pending.

---


## 2026-11-18 — substantive 02m Short revision (unapproved alternative)

**Why this revision:** The previous 02m copied the 199-word root and ended on a colon before its opening question. That was a syntactic continuation, not adequate evidence of a meaningful twice-through loop. The separate 02m version now opens on the *observable result* (a head moves; Hans stops at eight) and ends **after the complete explanation** with an invitation to inspect precisely that head. Literal textual join: EN `Watch the questioner's head.` → `The man's head moved. The horse stopped after eight taps.`; RU `Посмотрите на голову спрашивающего.` → `Человек чуть шевельнул головой. Лошадь остановилась после восьмого удара копытом.` The closing directive gives the opening action a new, causally understood meaning rather than relying on shared keywords or punctuation. This is an **authorial textual check**, not an independent double-read PASS or an AV-loop PASS.

The new 02m independently tells the full progression: owner absent → examiner lacks the answer → examiner hidden → tiny involuntary cue → Pfungst reproduces the mechanism with a hand tap. Illustrative `3 + 5` is *not* represented as a verbatim recorded historical exchange. No new factual claims beyond the shared Pfungst research. English narration is 190 words (estimated ~1:15–1:45 at 130–150 wpm plus pauses, **NOT_MEASURED**). The full natural Russian equivalent is separately written.

**Exact current six-text table:**

| Target | Full RU | Full EN | EN words | SHA-256 EN | SHA-256 RU | Editorial position |
|---|---|---|---:|---|---|---|
| 02m / Short | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | 190 | `7e053631046138ae48664c25c91f26becf8c90953bd219c5b695ff652ed759e2` | `3f8055c050e2f40820e8d813cd46e864dedd292af475a374239f8c5a13ba77ae` | **Revised; provisionally recommended**, independent EN/RU and AV loop UNVERIFIED |
| 05m / Long | [RU](variants/05m/script.ru.txt) | [EN](variants/05m/script.en.txt) | 667 | `1f872d933deb459eff802ab455f101eb8e037c824963984dda0cbca9f8039a13` | `8959d978b857ac7bf5522f2392862e074d13525a3d2508927c57974a5d40a2b9` | Unchanged, richer measured controls, slower at percentages |
| 10m / Long | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | 1329 | `da092c0c9ffe987b559110add2826f93fc4e5a6e509c2e38e5956906fdc5b034` | `0782ec4dc60cf0f2a616c772ad84c885d4418bd7a0264f4464f44f9ca89324b2` | Unchanged, more experiments but repeated knowledge-dependence |

**Preserved evidence:** the 199-word root EN/RU, old root-only 13-shot `storyboard.json`, research, old root-related review and artwork plan remain intact. Previous 02m SHA-256 EN `778133d5c2f39a5f47e31e1b2a8b13d24feb26961c6c54fe777b60681e54f745`, RU `fb4505fec1bd233f9104408f2e3ce84aae28d28d6ce343bf737fc549d0cc3e21` are historical **root** provenance only. The revised 02m is **not scene-covered** by `storyboard.json`: S001 now needs the examiner's head gesture and horse stopping, and the ending needs a visual return to that action. No old scene spans, timing, reviewer receipt or approval applies to new hashes. Do not manufacture 13 adapted scenes or regenerate media until actual approval.

**Gate status:** `EDITORIAL_CANDIDATE_UNREGISTERED`; no independent first listener, no bilingual reviewer, no signed `ytv-script-review-v1`, no runtime selection, no owner approval, no voice measurement, no MP4 or verified AV seam. These stay `UNVERIFIED`.

## Original README retained as historical context

# Clever Hans — editorial duration variants (2026-11-18)

**Provisional choice:** ~2m Short. The original short is more focused on the horse puzzle and already has full payoff. Five and ten minutes have full, independently structured source-grounded EN/RU narrations, but growing methodology slows the immediate story. The 02m colon seam is **not a verified loop** until a genuine twice-through first listener and MP4 check.

| Target / format | Full RU | Full EN | EN words | SHA-256 EN | SHA-256 RU | Status |
|---|---|---|---:|---|---|---|
| ~2m / Short | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | 199 | `778133d5c2f39a5f47e31e1b2a8b13d24feb26961c6c54fe777b60681e54f745` | `fb4505fec1bd233f9104408f2e3ce84aae28d28d6ce343bf737fc549d0cc3e21` | EDITORIAL_CANDIDATE_UNREGISTERED |
| ~5m / Long | [RU](variants/05m/script.ru.txt) | [EN](variants/05m/script.en.txt) | 667 | `1f872d933deb459eff802ab455f101eb8e037c824963984dda0cbca9f8039a13` | `8959d978b857ac7bf5522f2392862e074d13525a3d2508927c57974a5d40a2b9` | EDITORIAL_CANDIDATE_UNREGISTERED |
| ~10m / Long | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | 1329 | `da092c0c9ffe987b559110add2826f93fc4e5a6e509c2e38e5956906fdc5b034` | `0782ec4dc60cf0f2a616c772ad84c885d4418bd7a0264f4464f44f9ca89324b2` | EDITORIAL_CANDIDATE_UNREGISTERED |

**Status:** `EDITORIAL_CANDIDATE_UNREGISTERED`. Independent first listener, bilingual reviewer, official runtime, owner approval, TTS, imagegen, MP4 and publication: NOT_RUN/UNVERIFIED. Full story maps, eight criteria and explicit deficiencies are in [story-review](story-review.md); one shared source evidence ledger in [research](research.md). 02m is the exact unchanged root narrative.

**Scene provenance:** [storyboard.json](storyboard.json) and [packaging brief](packaging-brief.md) cover **ONLY** unchanged root/02m and still have provisional 13-shot timings. No 05m/10m spans or storyboard have been created, and none should be inferred from that old scene grid.

**Safety:** Root scripts and approvals/media/pins remain unmodified. New Longs are alternatives, not replacement masters; selecting one requires a real owner decision and the documented runtime workflow.

---
## Earlier one-version packet (historical)

**Совместимость с main 96c8fa1573c0:** старый текстовый Draft PR, не `ytv start` run. До производства необходимо выполнить независимый `sessions.independent` review, подтверждённый `awaiting_script_approval`, получить owner approval; предварительная раскадровка не готовый stage. [Handoff](handoff.md).

# Paper Detour — Clever Hans: The Horse Who Read the Questioner

**[Читать весь русский сценарий](script.ru.txt)** · **[Full original English narration](script.en.txt)**

## Logline

A Berlin horse seemed to solve arithmetic even for other people, but two carefully changed experiments revealed the answer was leaking through involuntary movements of whoever asked. Then the psychologist replicated the trick using his own hand.

## Status

**Draft textual preproduction only. No owner acceptance.** Intended channel `paper_detour` in current main is active; this does not automatically authorize a run, TTS, imagegen, render, upload or merge.

## Artifacts

- [research.md](research.md) — 10 real different-event candidates, 3 detailed finalists, historic primary claims, external demand observations vs unverified own analytics.
- [script.en.txt](script.en.txt) — entire 199-word English narration (future exact TTS/SRT master).
- [script.ru.txt](script.ru.txt) — whole natural Russian reading translation.
- [story-review.md](story-review.md) — explicit attention/clarity/payoff/loop gates, independent cold review UNVERIFIED.
- [storyboard.json](storyboard.json) — 13 proposed EN/RU-aligned shots and self-contained prompts for ONE complete physical paper/card diorama per shot, 4–6 sec tentative grid, S013 reuse of S001, S007 paper plane.
- [packaging-brief.md](packaging-brief.md) — three distinct title+large paper lettering+thumbnail-promise directions.
- [handoff.md](handoff.md) — actual production preconditions, sources and owner permissions.

## Loop

The last spoken words are `It was in the mind of the person asking a simple question:` and the first are `What's three plus five?`. The full answer is already established before this restart. Final image reuses S001 and must match the opening crop/pose in an actual render. All AV measurements are **NOT_RUN**.
