# Therac-25 / Fritz Hager — three-duration editorial review

**EDITORIAL_CANDIDATE_UNREGISTERED — AUTHORIAL ONLY.** No independent reviewer response, owner approval, run receipt, production, measured audio, MP4 or viewer retention. Text revision performed against original PR #112 baseline `2efd74a567b064e4ac6011c6832ec4cbc3b71d19`; canonical standards read at main `67d9ed5dd63adc27250b6a286fdf40544b9a73c0` (PR #124 merged). Main is a rule reference, **not** a migration of existing runtime pins.

## Complete text manifest (UTF-8, SHA-256 of actual bytes)

| Duration | EN exact file / SHA-256 | RU exact file / SHA-256 | Words EN | Format and timing estimate |
|---|---|---|---:|---|
| 02m | [EN](variants/02m/script.en.txt) — `838a41c90d73e7058fd72ca2f3244286700d21eba5389f5d482c31ea55cd8bc0` | [RU](variants/02m/script.ru.txt) — `73d052a7010b949c6aab374e019f9f1ba041e0aa2b298b58b24fe952c8eefe4c` | 277 | Long 16:9, ≈1:59–2:20 at 120–140 English wpm excluding uncertain pauses |
| 05m | [EN](variants/05m/script.en.txt) — `a138710c019af94fcbfbda426e2cd801da0e42fa05bd3414d656c04f88a6f52c` | [RU](variants/05m/script.ru.txt) — `bc707d59631e10028ec77ce05f88ca3bfaf892cdba7f1cda9512bd72ce4de47d` | 570 | Long 16:9, ≈4:04–4:45 at 120–140 wpm excluding uncertain pauses |
| 10m | [EN](variants/10m/script.en.txt) — `198574015df1924bcef6669c44ce70a8ebb0548d0dd5719c946ecec77fb95e97` | [RU](variants/10m/script.ru.txt) — `aee9a40f08961f63fb3390ee915c8dc0464c3ae7c1db541b196a2ca2755be527` | 1221 | Long 16:9, ≈8:43–10:11 at 120–140 wpm excluding uncertain pauses |

**Exact 05m evidence retained:** Both files are byte-identical to root `script.en.txt` and `script.ru.txt` at baseline. Root EN blob `55ae8790d9193cc7a89133c87ee0fbaabacea3da`, RU blob `35a3f0671b01a8b4d8afb42ed1382cc101f08610`. Existing 26-scene `storyboard.json` remains tied to these root hashes only, not to 02m/10m. No attempt to validate or inherit old timings for modified scripts.

## Three story maps / actual textual differences

**02m:** questions about apparent safety and reuse → March patient injured, ambiguous Malfunction 54 → failure not reproducible / apparatus reused → second injury → Hager tests empty room, discovers fast X-ray-to-electron correction → measurement and outside reproduction → other incidents have other causes → physical protection and surviving clinical lesson. Completed human consequence before ending. No Shorts-loop is required or claimed for **Long**.

**05m:** three documentary questions → empty-room meter mystery → March injury, return to service, April injury and death → after-hours experiment with mode correction → mismatch between console and actual hardware → other instrument, callbacks to clinics → Georgia prior injury, six cases and multiple defects → safeguards and the exact transferable empty-room test. This is the original strong questions-first master, retained without cosmetic rewriting.

**10m:** opening questions about machine safety and proof → explain only necessary physical difference between electron and X-ray modes → two Tyler injuries → delayed reproduction, fast correction and measured pulse → Georgia recognition → earlier Georgia/Hamilton/Yakima incidents and shortcomings of communication → second Yakima defect differs from Tyler → loss of independent interlocks → regulators demand hardware plus software changes → six-accident systemic investigation → concrete safety consequence. The central Tyler discovery remains the main hook, not replaced with an opening lecture.

## Individual eight-criterion assessment — 02m

| Criterion | Author /10, confidence | Concrete justification and defect |
|---|---|---|
| Interest / significance | 8, medium | Two patients harmed in a clinical procedure and a reproducible failure; audiences may recognize the famous case |
| Opening | 8, medium | “How could a radiation machine say...” promises screen contradiction and repeat harm; abstract concept arrives before a character |
| Development / reason to continue | 8, medium | Injury → engineers fail → reuse → second injury → test; fast correction comes after consequences, though three incidents are compressed |
| Payoff | 8, medium | Meter measurement, outside confirmation and independent safeguards explain both question and outcome; fewer details of policy response |
| Freshness of angle | 6, high | The screen vs hardware distinction is specific; existing large EN videos cover the subject |
| Visual expression | 7, medium | Empty table, modal screen and off-scale detector are legible paper dioramas; physical accuracy reference bytes UNVERIFIED |
| Natural spoken clarity | 8, medium | 277 English words, concrete cause and outcome without glossary; timing may be above exactly two minutes |
| Verified viewer interest | UNVERIFIED, low | Earlier indexed comparable videos have no checked same-creator same-age baseline; no channel CTR/retention |

Principal risk: rapid change from two injured patients to Georgia and regulation in final third may need audible pauses that push beyond two minutes. No measured TTS.

## Individual eight-criterion assessment — 05m

| Criterion | Author /10, confidence | Concrete justification and defect |
|---|---|---|
| Interest / significance | 8, medium | The March warning is followed by actual reuse and another injury; retains strong human stakes |
| Opening | 8, medium | Three specific questions before meter hook; early “one night” scene might precede needed identity of Hager |
| Development / reason to continue | 9, medium | Empty-room test is held until patients and failed investigation are established; all major turns are causal |
| Payoff | 9, medium | Reproduced failure, calls to other clinics, multiple different faults and transferable test; cannot restore the two patients |
| Freshness of angle | 6, high | Fritz Hager's replicable experiment is distinctive within well-covered Therac-25 history |
| Visual expression | 8, medium | Screen X→E, mechanical position, external meter and colleague verification suggest discrete visual beats; accuracy/refs not checked |
| Natural spoken clarity | 8, medium | Original spoken sentences explain mode mismatch without a long technical digression; specialist and screen segment may be cognitively dense |
| Verified viewer interest | UNVERIFIED, low | Cached public views are not own CTR or retention and no controlled creator baseline was obtained |

Principal risk: the explanations of X-ray target and electron mode in adjacent paragraphs remain dense for first listening, requiring independent first-listener check.

## Individual eight-criterion assessment — 10m

| Criterion | Author /10, confidence | Concrete justification and defect |
|---|---|---|
| Interest / significance | 8, medium | Broadens a two-patient mystery into systemic responsibility at several clinics; high consequence but more technical than original |
| Opening | 8, medium | Questions lead to physical mode explanation before Tyler incidents; risk that necessary opening immersion becomes lecture |
| Development / reason to continue | 7, medium | Tyler test and outside reproduction are substantial; chronology jumps back to 1985 after main hook, lowering momentum |
| Payoff | 8, medium | Shows why one keyboard fix was insufficient and what separate interlocks changed; final safety explanation may sound like a lesson |
| Freshness of angle | 7, medium | Hamilton recommendations and second Yakima counter bug add less-covered verified material, not just longer retelling |
| Visual expression | 7, medium | Multiple clinics, timeline and physical interlock need distinct paper-world treatment; risk of repeated console pictures |
| Natural spoken clarity | 7, medium | Plain language except the two software mechanisms; many institutions and dates add listening burden |
| Verified viewer interest | UNVERIFIED, low | Same incomplete public comparison; no direct demand signal for ten minutes versus five |

Principal risk: precisely **after the Georgia recognition and Tyler reproducible test**, the script returns to 1985 Hamilton/Yakima history. That is informative but the resolved primary mystery reduces curiosity. Avoid deploying the 10m as default without independent evidence of its attention value.

## Comparative judgment: added value and exact loss points

| Transition | Genuine addition | Where attention can be lost |
|---|---|---|
| 02 → 05 | Detailed two-mode hardware conflict, the actual fast-correction test, independently checked short pulse and calls across clinics | 05m: adjacent technical passages beginning “The X-ray mode required...” and “But the internal control...” require visual/audio support |
| 05 → 10 | Earlier incidents in Marietta, Hamilton and Yakima; repeated “no dose” errors, Canadian interlock recommendation, separate 1987 setup-counter fault, regulator response | 10m: after “The repeated test gave investigators a way...” story returns to 1985, weakening forward drive; later regulator paragraphs may become an explanatory tail |

**Recommendation: 05m Long**, preserving the previous questions-first master intact. The new 02m is complete and can be an alternative where short attention is more valuable. The 10m has real source-grounded details, but its added backstory weakens the linear escalation. Recommendation is **not** owner selection, permission to make three videos, or measured preference.

## Hard gates and evidence limits

| Check | 02m | 05m | 10m |
|---|---|---|---|
| Full EN+RU narration, same one story | AUTHOR TEXT CHECK | Original paired EN+RU retained | AUTHOR TEXT CHECK |
| Evidence for all new claims | Source-map below; PRIMARY DEPOSITIONS UNVERIFIED | Baseline research and references | Additional 1992 Leveson/Turner transcript/map; primary depositions UNVERIFIED |
| Source caveat: all six incidents do NOT share one bug | PASS in text | PASS in text | PASS in text; counter bug different |
| Compatible format | Long 16:9, configured | Long 16:9, configured | Long 16:9, configured |
| Required Short text loop | N/A, Long | N/A, Long | N/A, Long |
| Actual TTS duration / auditory attention | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Independent blind reader + bilingual reviewer | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Owner approval / pinned runtime / media | UNVERIFIED | UNVERIFIED | UNVERIFIED |

This table records **authorial text examination**, not blind independent review. Do not copy scores into reviewer input; request independent assessment on exact text hashes before any official script gate. No simulated reviewer IDs or receipts.
