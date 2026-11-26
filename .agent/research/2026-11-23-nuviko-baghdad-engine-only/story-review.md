# Exact script review — DHL Baghdad A300
Author of subjective scores: AI writer self-review on 2026-11-23, medium confidence in story/editing judgement; **not** independent viewer. Independent reviewer: **UNVERIFIED**. All hash values calculated from exact UTF-8 text with a trailing LF (not Git blob SHA-1). No reviewer result or approval is invented.

| Variant / proposed ChannelSpec format | EN words / SHA-256 | RU words / SHA-256 | Status |
|---|---|---|---|
| 02m / Short 9:16 | 278 / `742d920f00787dca72e0e2aa594fe6051ce791d4b91aa1efe06f414c493bddc0` | 230 / `50ba72aae67352345292c34da089274862ba5e49ace41c129191757bd2c3395b` | REWORK — closing loop weak |
| 05m / Long 16:9 | 710 / `b9040bb3403506878e70b22b51fd7b29bcd3ea21cc0b066e93d6de824087a5ca` | 549 / `5a8ec743c7a344bf5fc670f2ea60706112088f41da527b83a7215b7e677a9253` | **STRONG_CANDIDATE, recommended** |
| 10m / Long 16:9 | 1661 / `8c03cb9cca153357037c3ef6183bb97e22747747e676a59966ed499b61012e80` | 1372 / `b33020e192baf102c5a9d47af9e43c42ca40548d4c144fdfd1d198317b49d92e` | REVISED_LONG_CANDIDATE — source chronology corrected; reviewer UNVERIFIED |

Estimated EN TTS rate only: 130–150 spoken words per minute plus pauses (not an observed voice speed); configured channel voice speed 1.10x untouched. 02m, 05m, 10m are **editorial targets**; actual audio, end-screen and runtime fit UNVERIFIED. If text count makes target incompatible, require an edited exact version and fresh review instead of changing voice speed.

## Eight criteria (1–10, author evaluations; each based on exact event/line)
| Criterion | 02m | 05m | 10m |
|---|---|---|---|
| Interest/significance | **9**: missile disables all controls, three survive | **9**: burning wing and impossible control problem | **9**: real stakes preserved; three survive complete hydraulic failure |
| Opening | **9**: “The pilot moved the controls. The cargo jet barely responded.” | **9**: clear questions about land, speed and runway | **8**: concrete questions, final one technical |
| Development/why remain | **8**: throttle discovery → gear → switch → landing | **9**: dynamic learning, fuel, gear, crosswind and runway choice | **9**: pitch discovery → gravity gear >270kt → delayed bank → fuel/crossfeed → runway switch → two final controls |
| Payoff | **8**: twenty-five-minute thrust-only landing and three survivors | **9**: 33L touchdown, sand stop and mechanism answer | **9**: separate corrections at 250 and 100 feet, touchdown, survival |
| Freshness of angle | **8**: improvised steering not generic missile headline | **8**: story told through changing control conditions | **8**: engine controls become a progressively learned flight-control system |
| Visual expressiveness | **9**: burning left wing, thrust, runway, sand | **9**: wing fire, cockpit levers, landing gear and runway decision | **9**: wheels deployed, 30° banks, runway change, final unequal thrust |
| Natural spoken language | **8**: active plain language, awkward closing | **9**: actions and consequences without technical lecture | **8**: new action-led middle but still demanding aerodynamics |
| Confirmed audience demand | **UNVERIFIED**: no comparable Nuviko Short | **UNVERIFIED**: mismatched public YouTube counts | **UNVERIFIED**: no own-channel retention or comparable 10m baseline |

**02m primary flaw:** closing returns to the first attempt to use the controls but restates the start rather than producing a naturally forward-moving spoken seam. Full payoff **does** occur before this. Author loop verdict **REWORK**; actual AV seam **UNVERIFIED**. Short format exists, measured two-minute duration UNVERIFIED.

**05m primary flaw:** a five-minute aviation story can feel cockpit-heavy; fuel monitoring and runway choice must be visually distinct. Strongest line of causal change: “The aircraft drifted away from that approach, so Gennotte chose the nearer, shorter runway instead.” Main payoff: “The aircraft stopped ... The three crew members got out alive.” Interest, development and payoff 9/9/9 with explicit evidence → STRONG_CANDIDATE.

**10m remaining limitation:** despite a corrected event chain (gear and speed before learning bank) and distinct 250-ft/100-ft interventions, the detailed engine-control explanation may still slow a first-time listener. Revised edition remains an editorial candidate, not approval.

## Whole-story and comparison
| Duration | Independent story path | Likely attention-loss point | Added value |
|---|---|---|---|
| 02m | Wheel fails → hit/wing fire → thrust learning → gear/fuel roles → runway switch → risky touchdown and survival | Many distinct functions in few lines | Full central answer without background |
| **05m** | Question-led intro → cargo takeoff → hit and loss → improvised pitch/roll → fuel and gear → runway drift → high-speed touchdown and dust | Paragraph explaining speed after throttle adjustment | Explicit cause-and-effect, runway choice, full human payoff |
| 10m | Questions → departure → strike → pitch learning → emergency gear at >270kt → delayed bank and 30° roll → crossfeed dilemma → long approach and runway switch → 250-ft pitch + 100-ft lateral correction → sand stop → qualified Airbus lesson | Dense middle: thrust dynamics still need independent reading | Verified step order and two different final interventions support added time |

**Increment 02→05:** shows why normal landing configuration is impossible, what different crew members do, and why the original runway target has to change. More than elaborating the same fact.

**Increment 05→10:** the emergency gear decision makes lateral learning possible; distinct pitch and heading corrections in the last 250 feet add a real second climax. Useful additional mechanics from the Airbus technical report, but more technical cognitive load than 05m; recommendation remains **05m**.

**Checks per variant**
| Gate | 02m | 05m | 10m |
|---|---|---|---|
| Core factual sequence grounded in Airbus presentation | PASS — author source comparison | PASS — author source comparison | PASS — author source comparison |
| EN↔RU meaning and material qualifications | PASS — author line-by-line reading | PASS — author line-by-line reading | PASS — author line-by-line reading |
| ChannelSpec supported format | Short supported; duration UNVERIFIED | Long supported; measured length UNVERIFIED | Long supported; measured length UNVERIFIED |
| Spoken Short loop | REWORK (self) | N_A | N_A |
| Actual media/reference rights | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Independent reviewer without verdict/beat map | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| TTS duration and MP4 AV review | UNVERIFIED | UNVERIFIED | UNVERIFIED |

No independent review. Two author cycles: (1) timeline/evidence and causal structure; (2) spoken language, uncertainty and aligned RU translations. Not a production gate. The proposed 05m source remains an editorial **recommendation**, not approval.


## Substantive revision of 10m (2026-11-23; same PR, new script hash)
- **Before:** lateral steering and fuel crossfeed were described *before* emergency gear, although Airbus pp. 3–4 says gear at above 270 knots brought speed toward 210 and only then pilot mastered direction. The final 100-ft lateral power change was reduced to a generic sentence; five explanatory paragraphs followed survival.
- **After:** steering follows gear and speed recovery; added sourced roll excursions just beyond 30°, crossfeed decision as human task and distinct right-engine reduction near 100 ft with left thrust retained. Replaced repetitive tail with connected crew roles and Airbus's qualified post-event safety lesson. Shared research retained.
- **Exact baseline:** PR head `de124dd53aa329f27d61d1b8262ce713b1b9cb03`; 10m EN former SHA-256 `9c25a598eba97c87a51feb0eee38d12257e7aab6fc870af33f9d5c026b5bf4ea`, RU `31774a798d1ebae33233d379405d7eff2ec3c7ae95fcfa73ce5108cf11dd2b0f`. New 10m EN `8c03cb9cca153357037c3ef6183bb97e22747747e676a59966ed499b61012e80` (1661 words), RU `b33020e192baf102c5a9d47af9e43c42ca40548d4c144fdfd1d198317b49d92e` (1372 words). 02m and 05m files were not modified.
- **Fact anchors:** Yannick Malinge, Airbus/ISASI 2004, PDF p.3 for gear at >270kt / ~210kt and delayed bank / >30° roll p.4; p.4 for 250 ft and 100 ft engine actions; p.5 for landing and right-slide evacuation; pp.6–7 for limits of identical-scenario training. Re-read paper plus visual page 3–4. No inferred motives or simulated cockpit dialogue.
- **Eight author criteria for revised exact 10m:** interest 9/10 (three surviving against disabled controls); opening 8/10 (three questions, last technical); development 9/10 (gear unlocks ability to learn bank, later fuel and runway constraints); payoff 9/10 (two last-moment manoeuvres and survival); fresh angle 8/10 (two-throttle causal chain); visual 9/10 (gear, damaged wing, rolls, parallel runways); spoken naturalness 8/10 (action-oriented but still numeric); audience demand UNVERIFIED (no qualified own-channel comparator). Confidence: medium on editorial judgements, high on document-to-event ordering. These are **author self-ratings**, not a reviewer result.
- **Hard checks:** source event order author PASS; EN↔RU action, thresholds and qualified statements author PASS; Long ChannelSpec 16:9 supported; full 02m loop still REWORK, AV UNVERIFIED; 05m Long untouched and provisionally recommended; independent blind-first review, voice timing, media rights, selected source registration and owner approval all UNVERIFIED. ~11.1–12.8 min spoken before pauses; no voice generated. Existing script/scene timings for old 10m invalid; no 10m storyboard exists to inherit.
- **Choice:** 05m remains preferred for clarity per minute. 10m offers more physical reasoning but demands an independent fresh reading of exact new EN/RU before any approval. Recommendation is not permission to produce three films.
