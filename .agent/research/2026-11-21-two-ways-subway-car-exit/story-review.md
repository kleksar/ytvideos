# Story review — exact 2/5/10m scripts

**Author:** current editorial assistant, 2026-11-21. **Confidence:** medium in causal editing and deterministic math, low in empirical YouTube demand and spoken pacing. **No independent first listener, no real TTS/MP4.** These scores are subjective author opinions, **not** real retention, CTR or probability of viral performance.

## Exact six revisions and runtime assumptions

Word counts use whitespace-separated words in Git blob bytes; SHA-256 computed on the full actual UTF-8 text read back from stored Git blobs, not from a copied summary.

| Version | EN exact SHA-256; words | RU exact SHA-256; words | Assumed EN time, excluding unknown real TTS pauses | Format |
|---|---|---|---|---|
| 02m | `54e83472efa95791ffeef73fa0359888599d6ed2b5c42db30623cd02a1dfe727` — **314** | `d353c3af4b0dc20da94678262e48f009ffb0719d3de77c31154096371a47d2a0` — **273** | ~1:55–2:20 at 145–165 English wpm + variable pauses | Short *candidate*, channel typical 35–50s exceeded, actual TTS & seamless AV **UNVERIFIED** |
| 05m | `07b45e205bdff24d10fa4a6d262a43b85e99facc80981da566c992e53b8cd245` — **768** | `576ea7bd43760d7e289ed2d44a38a1cc9d3ba48b85c2eeec6167b05b285924d8` — **635** | ~4:40–5:30 at 145–165 wpm + variable pauses | Long editorial only; ChannelSpec canvas/fps unresolved: **PRODUCTION BLOCKER** |
| 10m | `b9dfc4d2bfc415961c180f390511e13663840668bae29f160f73383bc7718028` — **1607** | `6fa737494dc05bceae717fa065206ed97d46b54b90408c94b98b27ff2381edc0` — **1328** | ~9:45–11:30 at 145–165 wpm + variable pauses | Long editorial only; **PRODUCTION BLOCKER**, duration may run long |

The range is a rough narration estimate, not a measured recording, and the exact channel voice speed is **not** changed to force a target. RU editorial is natural semantic translation, not a separate performance script. All three are independently complete stories with known inputs and explicit payoff, not fragments of a longer master.

## Eight criterion scores — 02m exact EN/RU

| Criterion | Score | Observable textual basis and objection |
|---|---:|---|
| Interest/significance | **9** | First line “I have one minute before my subway train leaves”; universally recognisable *for train users*, but excludes many non-commuters |
| Opening | **9** | A door decision plus arrival clock immediately; no unknown place/name or unexplained term |
| Causal development / reason to finish | **9** | “This train leaves in seventy-five seconds” makes the initially clever advance walk miss a departure; later “change just one thing” inverts the winner |
| Payoff | **9** | “Moving it into waiting time is what saves me time” shows what caused the 100s result, not only the result |
| Freshness of angle | **8** | Adds missed-train penalty to established “best carriage” advice; consumer travel hacks already common |
| Visual expressiveness | **8** | Two platform ends, moving character, doors closing, two clocks; the 4-min delay must be shown without fictitious live UI |
| Spoken naturalness/clarity | **8** | Concrete first-person choice and ordinary verbs; three different clock totals risk numerical density |
| Confirmed audience interest | **UNVERIFIED** | Reddit/Citymapper verify real commuter issue, but no matched short A/B audience response, comment baseline, CTR or retention |

**Classification: STRONG_CANDIDATE (authorial); recommended 02m.** Required interest/development/payoff >=8 individually; no average used to cover unverified empirical demand. Main deficiency: spoken numbers can exhaust listener; natural loop depends on actual cadence. Strongest first-listener rejection rationale: “I understand the maths but don't want a 2-minute calculation.” Demand still UNVERIFIED.

**02m narrative map:** hook—near departure with exit far away; goal—reach staircase earliest; causal constraint—100s walk versus 75s departure; act/result—B misses first and loses 140s; new controlled condition—165s deadline; second result—B gains 100s on same train; closing lesson—move walking into unavoidable wait only with boarding margin. Literal short text return: last “On my next trip, that countdown gives me a very familiar problem. It says...” → first “I have one minute before my subway train leaves.” RU mirrors this “Написано...” → “До отправления...”. **Authorial text-only seam provisional PASS**; full two-cycle independent read, actual video seam and its visual composition are UNVERIFIED. Loop reuses real model state as a new day; no missing payoff.

## Eight criterion scores — 05m exact EN/RU

| Criterion | Score | Observable textual basis and objection |
|---|---:|---|
| Interest/significance | **8** | Opening questions about door closest to exit and unexpected train arrival; focused, but less immediate pressure than 02m |
| Opening | **8** | First two questions give concrete stakes before station geometry; no long backstory |
| Causal development / reason to finish | **8** | Same-train overlap → unexpectedly missed departure → opposite result; the model rules occupy more middle space |
| Payoff | **8** | “The decisive question is whether the walking can fit into time I already have before departure” explains actionable condition |
| Freshness of angle | **8** | Unlike generic carriage advice, explicitly measures whole journey, not just stairs |
| Visual expressiveness | **8** | Dual clocks and 150/30 path split can be staged clearly with separate station geography |
| Spoken naturalness/clarity | **8** | Conversational “Am I really saving time, or just moving my walk?” but repeats model inputs and clock totals |
| Confirmed audience interest | **UNVERIFIED** | No matched 5-minute A/B creator baseline for this format |

**Classification: STRONG_CANDIDATE editorial, not producible in current Long recipe.** Main deficiency: between “Here's the part…” and the second result is lengthy for a strictly entertaining format; no real 5-minute measured voice. Own score for ending is conditional on model not being overexplained.

**05m narrative map:** questions → arrival at platform → explicit A/B → pending train → full-result explanation → closer train → missed service → loss calculation → practical safe-margin decision and caveats. A true completed narrative rather than an expanded intro.

## Eight criterion scores — 10m exact EN/RU

| Criterion | Score | Observable textual basis and objection |
|---|---:|---|
| Interest/significance | **8** | Opening “could missing one train ever put me at the station exit earlier?” presents a deeper paradox, but 10-minute audience narrower |
| Opening | **7** | Three initial questions feel more educational than dramatic and delay the first clock |
| Causal development / reason to finish | **8** | Three controlled scenarios: B +100s, then −140s, then **+40s despite missing one train** |
| Payoff | **9** | “the delay until the next departure versus those one hundred seconds of walking saved” genuinely changes earlier conclusion |
| Freshness of angle | **8** | Adds headway reversal; no false field experiment |
| Visual expressiveness | **8** | Three related platform/day states, next-train clock and controlled changes can be drawn distinctly |
| Spoken naturalness/clarity | **7** | Lines after third result on alternative strategy, changed exits, crowded cars and safety slow the ending |
| Confirmed audience interest | **UNVERIFIED** | No comparable long A/B entertainment baseline or real retention curve |

**Classification: REWORK** (complete standalone script, **not** STRONG_CANDIDATE recommended). Main weakness: after the strong third twist, long methodology/safety segment reduces urgency; the English ~1607 words could exceed target with natural pauses. At most two *substantive* rewrites, none automated under this check; no fake inflation to 9–10. The central third twist is real mathematical added value, not filler.

**10m narrative map:** questions → model and A/B → slow-train B win → close-train missed B loss → altered headway changes winner → simple break-even rule → not-yet-tested adaptive third choice → limits and final answer. Full beginning, causal middle and payoff; not a clipped 05m.

## Incremental-value decision

| Change | What new understanding is earned | Where interest could drop |
|---|---|---|
| 02m alone | Two opposite outcomes on one declared model; move walking into waiting, or lose an entire train | The clock totals if recited mechanically |
| 02→05 | Explains threshold (100s to distant door), full common-walk identity, safety margin, and why train ride duration cancels | Long input exposition before second reversal |
| 05→10 | Adds third controlled 60s-headway outcome **B wins even after missing a train**, formal H−100 relation, and why route/exit orientation may change car choice | Explanation following the third payoff, plus unresolved Long recipe |

**Recommendation: 02m (Short editorial target)** for first test; it ends with the core insight instead of several additional abstract branches. 05m is suitable as a substantive *editorial* follow-up only if Long format becomes supported. 10m needs a tighter post-third-twist narrative rather than an assumption that longer is better. User/owner still chooses one exact master after independent review; this is not approval.

## Independent PASS/FAIL/UNVERIFIED checks (each exact revision)

| Check | 02m | 05m | 10m | Meaning / evidence |
|---|---|---|---|---|
| Model arithmetic | PASS (author/tool) | PASS (author/tool) | PASS (author/tool) | Independent-of-prose Python numerical assertions for 585/485, 495/635, 495/455 |
| Factual provenance | PASS for conditional maths; UNVERIFIED live-platform relevance | same | same | Citymapper proves such advice exists; **no real travel measurements** in narration |
| EN/RU substantive correspondence | PASS author | PASS author | PASS author | Same distances, clocks, conditions, win margins and crucial caveats |
| Format / production | UNVERIFIED actual Short runtime, supported config | BLOCKED Long recipe | BLOCKED Long recipe | No manual approval, no real TTS/audio file |
| Short text loop | Provisional author PASS; independent UNVERIFIED | N/A (Long) | N/A (Long) | Last→first EN/RU text plausible, no video seam claimed |
| External media rights | UNVERIFIED | UNVERIFIED | UNVERIFIED | Original authored words; no external media/brand reference bytes actually selected |
| Independent `ytv-script-review-v1` | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No separate reviewer; author self-review != independent |
| Measured audio / visual review | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No TTS, image, video, SRT, render or audience analytics |

No PR status, CI, recommendation, average score or author note can convert independent UNVERIFIED into approval.