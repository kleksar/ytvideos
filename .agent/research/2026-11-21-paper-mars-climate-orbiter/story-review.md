# Exact-variant story review — Mars Climate Orbiter

**Author:** automation editorial author, self-assessment revised on 2026-11-21 against exact 02m EN/RU bytes; not independent review. **Source main:** 131ef24068d75967b1e43aa88e5f1370f6775054; **policy:** PR #124 already merged, current main editorial standard applies. **No official run or reviewer receipt.** Scores are editorial judgments on the **exact text bytes**, not audience metrics or predicted CTR/retention.

## Six exact texts and estimated durations

| Version | Full EN narration / SHA-256 | Full RU review translation / SHA-256 | EN words and hypothetical duration | Recommendation status |
|---|---|---|---|---|
| 02m | [script.en.txt](variants/02m/script.en.txt) / 71eb4a796d8cc8fb1ab99b16ce835c4ecad4f0bf4447663e905addb09a3f0caa | [script.ru.txt](variants/02m/script.ru.txt) / 92c3c5ff45a701725a72e19ce20bea3523e8fda95f240263649bc128384a8c87 | **256 words**; ~1:47–2:05 at 150–130 wpm plus 5–7s pause (not measured) | **REVISED CANDIDATE** — author-only text seam provisionally passes, independent / AV seam UNVERIFIED |
| 05m | [script.en.txt](variants/05m/script.en.txt) / d5f97666fc36f9e7d7337b7625d1f1d6901a325606aeb5613587ebfed09c5bcf | [script.ru.txt](variants/05m/script.ru.txt) / 6eb47a98243c7b296f95a1aeaed7e5a651d29751e0b77983b05b3c50bc2088e8 | 634 words; 4:19–4:58 at 150–130 wpm incl. ~5–10s pauses | **STRONG_CANDIDATE — RECOMMENDED** |
| 10m | [script.en.txt](variants/10m/script.en.txt) / cd11d9597f4797990c84141c8d6451ad2a7daf8fc332abb75c34531ed11cd3ea | [script.ru.txt](variants/10m/script.ru.txt) / 2302d3e6861cd627690368469a178eb2613b8e99104ae1facadb3bc20d3c06e9 | 1,513 words; 10:10–11:46 at 150–130 wpm incl. ~5–8s pauses | **REWORK** — exceptionally dense technical middle; duration at faster bound approaches 10m |

Ranges are unaudited reading estimates, NOT Lawrence 1.10× measured TTS. The user-requested labels 2/5/10 are targets, not proof of exact duration. Actual speed and pauses await recorded audio. No shortening by unauthorized voice-speed changes.

## Eight independent criterion scores **per exact variant** (1–10, or UNVERIFIED)

Criteria per editorial.md. Every score points to a visible narrative element, with a distinct primary weakness below. Confidence for scores is **medium (author)** unless otherwise specified; verifiable historical facts have high source confidence, which is not viewer-demand confidence.

| Editorial criterion | 02m exact text | 05m exact text | 10m exact text |
|---|---|---|---|
| 1. Interest / significance | **8** — 49-second early blackout is a small human-readable clue; famous unit story still familiar | **9** — warnings before a costly loss add consequence beyond units | **8** — more institutional detail, central loss unchanged |
| 2. Opening | **9** — starts at a documented timing discrepancy, then the unexpected permanent silence | **8** — three useful Long questions, first actual event comes immediately after | **8** — questions, radio blackout scene; opening is longer |
| 3. Development / reason to continue | **8** — panel → thrusters → unit file → contradictory navigation readings → unready correction | **9** — unexpected extra thruster firings → wrong file → warnings → unready TCM-5 → radio silence | **8** — deep Doppler and mission procedures introduce friction during middle |
| 4. Payoff | **8** — reconstructed 57 km versus intended 226 km, with exact fate explicitly unknown | **9** — 57 km against planned 226 km; official causal finding, practical correction | **9** — explicit 57/226 and postmortem explain why file checks matter |
| 5. Freshness of angle | **7** — warning signs and false-normal blackout differ from the familiar unit joke, but are not new subject matter | **8** — residual-warning and unavailable last-correction story instead of only unit factor | **8** — uncovers why desaturation pulses mattered and multiple near-misses |
| 6. Visual expressiveness | **8** — offset paper panel, repeated impulses, two unit labels, diverging trajectories and blacked-out radio | **9** — paper physical objects / path diverging, radio antenna, trajectories | **8** — several abstract software/data passages require visual restraint |
| 7. Natural / clear spoken language | **8** — observable verbs replace a repeated abstract moral; one 4.45 number still needs careful delivery | **9** — normal verbs and concrete actions without caricatured fragments | **7** — terms like Doppler and reaction wheels may overload non-specialists |
| 8. Confirmed viewer interest | **UNVERIFIED** — no comparable channel data or measured interest | **UNVERIFIED** — no comparable same-author baseline/own analytics | **UNVERIFIED** — same evidence, 10m potential not measured |

No average score used to hide a weak element. For 05m interest/development/payoff respectively **9/9/9**, satisfying minimum 8 editorial threshold; nothing here passes actual independent gate. 10m not classified strong merely because there are more facts.

### Standalone structure and where interest may be lost

**02m, revised**: documented 49-second early loss of signal → visible solar-panel imbalance and frequent small pulses → ground-unit interface error → unresolved track discrepancies → unready last correction → 57-km reconstruction and fate uncertainty. The causal chain has concrete actions and the required answer before the loop. The close names an *ordinary blackout* as the last clue; reopening with its 49-second anomaly provides new information rather than repeating the scene. The full EN and RU were author-read in two textual cycles; the end-to-start transition is **provisional author text PASS**, not independent listening or a real AV seam. 256 English words may still exceed a two-minute voice window with pauses. Weakness: the unit conversion remains exposition, and the final callback may still sound constructed to an independent listener.

**05m**: Long introductory questions → informative flight setup → primary hook at frequent attitude-control corrections → interface/unit mismatch → ignored/conflicting trajectory signals → TCM-5 cannot safely be executed → early signal loss → reconstructed 57km → systems engineering conclusion. Main risk: section about Doppler solutions may be heard as jargon before the danger threshold appears. The line “Both numbers could not be equally right” is a useful comprehensible turning point. Full payoff occurs before quiet close. Long loop N_A.

**10m**: Long questions → silent encounter → hardware, reaction wheels and asymmetric solar array → small forces interface → alert chain → exact final week and last hour → unready TCM-5 → timeline → reconstructed loss → board findings and aftermath. Unlike 05m this supplies genuinely new context but risks fading in the explanations of wheel unloading and multiple estimates before radio silence. Ten-minute narration would benefit from one more authorial trim; this is **REWORK**, not a claim of production readiness. Long loop N_A.

### Exact initial/final spans for loop audit (revised 02m)

**EN first:** “The radio signal from NASA's Mars Climate Orbiter vanished 49 seconds earlier than predicted.”
**EN last:** “And the final clue arrived during what was supposed to be an ordinary radio blackout.”
**Literal EN seam:** “...ordinary radio blackout. The radio signal from NASA's Mars Climate Orbiter vanished 49 seconds earlier than predicted.” The second line answers which clue, without repeating the same event description or requiring a colon.

**RU first:** “Радиосигнал с аппарата NASA Mars Climate Orbiter исчез на 49 секунд раньше расчётного момента.”
**RU last:** “А последняя подсказка появилась во время, казалось бы, обычного радиомолчания.”
**Literal RU seam:** “...обычного радиомолчания. Радиосигнал с аппарата NASA Mars Climate Orbiter исчез на 49 секунд раньше расчётного момента.” Cold open is independently intelligible; payoff and uncertainty occur before the final return. **Author textual PROVISIONAL_PASS, twice through each full story; independent double-read and actual AV seam UNVERIFIED.** No storyboard/timings carry over to revised hash.

### Added value: 02 → 05 → 10

- **02 → 05:** 02m now includes the unresolved discrepancy and unavailable correction in compressed form; 05m still makes the sequence of warning signs, timing and failure of contingency more legible. Extra runtime buys comprehension, not a new event invented for length.
- **05 → 10:** more of the hardware mechanism, Doppler tracking alternatives, minute-by-minute finale, and review recommendations; real information but higher density and little additional emotional or causal turn after the loss.
- **Recommendation:** still **05m Long**, because the detailed warning-to-contingency chain is clearer and the text has more breathing space. Revised 02m is now a legitimate Short contender on author-only reading, not an approved master; 10m technical middle remains less accessible. If a genuine independent listener does not find the mid-story escalation worth five minutes, reconsider selecting any master rather than padding.

## Required separate gates / real status

| Gate | 02m | 05m | 10m | Evidence/limit |
|---|---|---|---|---|
| Fact source correspondence (author) | provisional PASS | provisional PASS | provisional PASS | NASA Phase I PDF sections, 1999 JPL statements as traced in research; author checks only |
| EN/RU meaning equivalence (author) | provisional PASS | provisional PASS | provisional PASS | Same event, numbers and uncertainty in each full paired translation; no external bilingual reviewer |
| Eligible format (ChannelSpec) | Paper Short configured; **revised 02m author text loop provisional** | Paper Long configured | Paper Long configured | ChannelSpec allows short and long; no actual production approval |
| Rights/media clearance | UNVERIFIED | UNVERIFIED | UNVERIFIED | No archival image, music, font or reusable rights inspected |
| Narrative spoken loop | **PROVISIONAL_PASS (author text only)** | N_A (Long) | N_A (Long) | EN/RU full double textual read by author; independent judgment and actual AV seam UNVERIFIED |
| Independent review, exact hash | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No independent reviewer invocation, no ytv-script-review-v1 receipt |
| Runtime script gate/owner master selection | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No ytv CLI, no persisted task/approval |

**Review ownership and confidence:** all numeric grades are the drafting author's own 2026-11-21 editorial judgments at **medium confidence**; viewer-demand score remains **UNVERIFIED** rather than fabricated 8. No listener reported reactions, no retention measurements, no non-existent review JSON, no scene/timing reuse. 02m revision is a single new authorial pass. Independent reviewer may still reject either or both 02m cuts; score revisions are not a review receipt.

## Exact 2026-11-21 02m edit record

- Baseline `bb308f938ede17009ee678e52603e70a7ab81da2`; original 02m EN Git blob `e843a094a630ee74834b0efddeb0b757f68e7561`, RU blob `55a4ba842a9406bcc12e95eef8ec9b968f057d13`. Baseline SHA-256 EN `deea64018af0f7d566bb5312f2be6799624e89ce8f5f91b42cecd4fb3b28fbd0`, RU `cf976dd31836cee93b5877af50bdb43a923b0d433ed0b4d55776fdc01936567e`.
- Before: 284 EN words; ending retold the opening and the Short speech loop **FAIL**. After: 256 EN words; begins with the verified **49-second early occultation**, moves through the unchanged physical failure and unresolved data, and returns to that *small clue* after supplying the full 57-km / 226-km payoff.
- Revised 02m exact SHA-256 EN `71eb4a796d8cc8fb1ab99b16ce835c4ecad4f0bf4447663e905addb09a3f0caa` and RU `92c3c5ff45a701725a72e19ce20bea3523e8fda95f240263649bc128384a8c87`. 05m and 10m EN/RU, research and packaging tied to 05m remain unchanged; no new factual claim beyond existing NASA source ledger. Revised 02m has no existing storyboard; future scene mapping must bind to this hash.
- Editorial path: original 02m REWORK → revised 02m candidate → author EN/RU/source/format check → **05m remains provisional recommendation**. Independent review/loop, real VO duration, AV, audience interest, selected master, production run and owner approval UNVERIFIED.
