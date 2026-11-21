# Exact-variant story review — Mars Climate Orbiter

**Author:** automation editorial author, self-assessment on 2026-11-21; not independent review. **Source main:** 131ef24068d75967b1e43aa88e5f1370f6775054; **policy:** PR #124 already merged, current main editorial standard applies. **No official run or reviewer receipt.** Scores are editorial judgments on the **exact text bytes**, not audience metrics or predicted CTR/retention.

## Six exact texts and estimated durations

| Version | Full EN narration / SHA-256 | Full RU review translation / SHA-256 | EN words and hypothetical duration | Recommendation status |
|---|---|---|---|---|
| 02m | [script.en.txt](variants/02m/script.en.txt) / deea64018af0f7d566bb5312f2be6799624e89ce8f5f91b42cecd4fb3b28fbd0 | [script.ru.txt](variants/02m/script.ru.txt) / cf976dd31836cee93b5877af50bdb43a923b0d433ed0b4d55776fdc01936567e | 284 words; 1:54–2:12 at 150–130 wpm plus 5–8s pause | **REWORK** — payoff exists, but Short spoken seam FAIL |
| 05m | [script.en.txt](variants/05m/script.en.txt) / d5f97666fc36f9e7d7337b7625d1f1d6901a325606aeb5613587ebfed09c5bcf | [script.ru.txt](variants/05m/script.ru.txt) / 6eb47a98243c7b296f95a1aeaed7e5a651d29751e0b77983b05b3c50bc2088e8 | 634 words; 4:19–4:58 at 150–130 wpm incl. ~5–10s pauses | **STRONG_CANDIDATE — RECOMMENDED** |
| 10m | [script.en.txt](variants/10m/script.en.txt) / cd11d9597f4797990c84141c8d6451ad2a7daf8fc332abb75c34531ed11cd3ea | [script.ru.txt](variants/10m/script.ru.txt) / 2302d3e6861cd627690368469a178eb2613b8e99104ae1facadb3bc20d3c06e9 | 1,513 words; 10:10–11:46 at 150–130 wpm incl. ~5–8s pauses | **REWORK** — exceptionally dense technical middle; duration at faster bound approaches 10m |

Ranges are unaudited reading estimates, NOT Lawrence 1.10× measured TTS. The user-requested labels 2/5/10 are targets, not proof of exact duration. Actual speed and pauses await recorded audio. No shortening by unauthorized voice-speed changes.

## Eight independent criterion scores **per exact variant** (1–10, or UNVERIFIED)

Criteria per editorial.md. Every score points to a visible narrative element, with a distinct primary weakness below. Confidence for scores is **medium (author)** unless otherwise specified; verifiable historical facts have high source confidence, which is not viewer-demand confidence.

| Editorial criterion | 02m exact text | 05m exact text | 10m exact text |
|---|---|---|---|
| 1. Interest / significance | **8** — probe reaches Mars then no signal, meaningful loss, but common joke | **9** — warnings before a costly loss add consequence beyond units | **8** — more institutional detail, central loss unchanged |
| 2. Opening | **8** — immediate vanished spacecraft, understandable without NASA vocabulary | **8** — three useful Long questions, first actual event comes immediately after | **8** — questions, radio blackout scene; opening is longer |
| 3. Development / reason to continue | **8** — array, misread file, unresolved discrepancy, reconstruction | **9** — unexpected extra thruster firings → wrong file → warnings → unready TCM-5 → radio silence | **8** — deep Doppler and mission procedures introduce friction during middle |
| 4. Payoff | **8** — 57-km reconstruction and multiple layers of failure, but loop weak separately | **9** — 57 km against planned 226 km; official causal finding, practical correction | **9** — explicit 57/226 and postmortem explain why file checks matter |
| 5. Freshness of angle | **7** — foregrounding silent signal plus warnings differs modestly from unit-meme | **8** — residual-warning and unavailable last-correction story instead of only unit factor | **8** — uncovers why desaturation pulses mattered and multiple near-misses |
| 6. Visual expressiveness | **8** — paper Mars, offset solar panel, two unit cards, lost path | **9** — paper physical objects / path diverging, radio antenna, trajectories | **8** — several abstract software/data passages require visual restraint |
| 7. Natural / clear spoken language | **8** — short declarative narrative, though abstract at end | **9** — normal verbs and concrete actions without caricatured fragments | **7** — terms like Doppler and reaction wheels may overload non-specialists |
| 8. Confirmed viewer interest | **UNVERIFIED** — video existence not demand | **UNVERIFIED** — no comparable same-author baseline/own analytics | **UNVERIFIED** — same evidence, 10m potential not measured |

No average score used to hide a weak element. For 05m interest/development/payoff respectively **9/9/9**, satisfying minimum 8 editorial threshold; nothing here passes actual independent gate. 10m not classified strong merely because there are more facts.

### Standalone structure and where interest may be lost

**02m**: opening radio disappearance → explain thrusters/imperial-versus-metric → ground warnings → 57km loss → review finding. Standalone payoff clear. Weakness: final “disappearing behind Mars” and first “A NASA spacecraft went behind Mars” form a repeated *scene*, **not a natural spoken continuation**; literal seam is an isolated restart, not a genuine loop. **Short loop author FAIL**, not disguised as PASS; AV seam untested. To improve requires another authorial revision and fresh review.

**05m**: Long introductory questions → informative flight setup → primary hook at frequent attitude-control corrections → interface/unit mismatch → ignored/conflicting trajectory signals → TCM-5 cannot safely be executed → early signal loss → reconstructed 57km → systems engineering conclusion. Main risk: section about Doppler solutions may be heard as jargon before the danger threshold appears. The line “Both numbers could not be equally right” is a useful comprehensible turning point. Full payoff occurs before quiet close. Long loop N_A.

**10m**: Long questions → silent encounter → hardware, reaction wheels and asymmetric solar array → small forces interface → alert chain → exact final week and last hour → unready TCM-5 → timeline → reconstructed loss → board findings and aftermath. Unlike 05m this supplies genuinely new context but risks fading in the explanations of wheel unloading and multiple estimates before radio silence. Ten-minute narration would benefit from one more authorial trim; this is **REWORK**, not a claim of production readiness. Long loop N_A.

### Exact initial/final spans for loop audit

**02m EN first:** “A NASA spacecraft went behind Mars exactly as planned. Twenty minutes later, it still hadn't come back.”
**02m EN last:** “The final radio silence looked ordinary at first. That was the cruel part of the mistake: the last thing operators saw was the spacecraft doing exactly what it had been told to do — disappearing behind Mars.”

EN last → first: “disappearing behind Mars. A NASA spacecraft went behind Mars exactly as planned.” This repeats the action, not a conversational continuation. RU likewise returns to the same event without a genuine spoken seam. **FAIL**. Reading the complete text twice by the author does not count as independent review.

### Added value: 02 → 05 → 10

- **02 → 05:** new causal steps, verified navigation deviations, dates, the unready course correction, and the decision context around failure. This materially changes why the viewer understands the loss.
- **05 → 10:** more of the hardware mechanism, Doppler tracking alternatives, minute-by-minute finale, and review recommendations; real information but higher density and little additional emotional or causal turn after the loss.
- **Recommendation:** 05m, not 10m by default and not 02m while the spoken seam fails. If a genuine independent listener does not find the mid-story escalation worth five minutes, reconsider selecting any master rather than padding.

## Required separate gates / real status

| Gate | 02m | 05m | 10m | Evidence/limit |
|---|---|---|---|---|
| Fact source correspondence (author) | provisional PASS | provisional PASS | provisional PASS | NASA Phase I PDF sections, 1999 JPL statements as traced in research; author checks only |
| EN/RU meaning equivalence (author) | provisional PASS | provisional PASS | provisional PASS | Same event, numbers and uncertainty in each full paired translation; no external bilingual reviewer |
| Eligible format (ChannelSpec) | Paper Short proposed, conditional on loop; **FAIL loop** | Paper Long configured | Paper Long configured | ChannelSpec allows short and long; no actual production approval |
| Rights/media clearance | UNVERIFIED | UNVERIFIED | UNVERIFIED | No archival image, music, font or reusable rights inspected |
| Narrative spoken loop | **FAIL** | N_A (Long) | N_A (Long) | 02m literal seam restarts; actual AV seam always UNVERIFIED |
| Independent review, exact hash | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No independent reviewer invocation, no ytv-script-review-v1 receipt |
| Runtime script gate/owner master selection | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No ytv CLI, no persisted task/approval |

**Review ownership and confidence:** all numeric grades are the drafting author's own 2026-11-21 editorial judgments at **medium confidence**; viewer-demand score remains **UNVERIFIED** rather than fabricated 8. No listener reported reactions, no retention measurements, no non-existent review JSON, no scene/timing reuse. Two authorial revision passes were not exhausted simply to make scores attractive.
