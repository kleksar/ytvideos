# Story review — Flight 232: flying with throttles, not a miracle landing

EDITORIAL_CANDIDATE_UNREGISTERED — **author's editorial assessment**, not independent first-listener review or official script approval. Reviewed 2026-11-17, Nuviko History, factual research in [research.md](research.md). Ratings are opinions about the exact text, not CTR, retention or a probability of success.

## Exact texts and estimated timing

| Version | Complete EN master | EN SHA-256 | Full semantic RU | RU SHA-256 | EN words | Estimated English spoken + end screen | Author classification |
|---|---|---|---|---|---:|---|---|
| 02m | [script.en.txt](variants/02m/script.en.txt) | `d7cdb9512161dd5d802b9aa45ebeaade84946c81f29130dd0aa96b03b85dd35c` | [script.ru.txt](variants/02m/script.ru.txt) | `e0d1f426bd67a1195b489ebc651dc3aee84d0c8bb436bbe64793671e5bb28e4e` | 314 | ~1:54–2:20 speech, plus 10s Long end screen | STRONG_CANDIDATE |
| **05m** | [script.en.txt](variants/05m/script.en.txt) | `ed05e78f4a5da7987bc332b1edd28e281ddca61d07d2c69e3c05aebf74e0dcc2` | [script.ru.txt](variants/05m/script.ru.txt) | `21151dfc657acfeef538b5ba6ab22e83da696e5271ee7a0f1c225828f6fa3c42` | 693 | ~4:12–5:08 speech, plus 10s Long end screen | **STRONG_CANDIDATE — RECOMMENDED** |
| 10m | [script.en.txt](variants/10m/script.en.txt) | `82f8e6445de577b116efb6e2fe3becf39182c967fb2589fc1bd4e91a1a78afa0` | [script.ru.txt](variants/10m/script.ru.txt) | `6364e66cfeaf35418a36f4fa7b222cadf423bc2e338609e8771058fb19f30ac8` | 1449 | ~8:47–10:44 speech, plus 10s Long end screen | REWORK (full, pacing weakness) |

Estimates divide word counts by an assumed **135–165 effective EN words/minute** including normal delivery pauses only approximately; channel voice speed 1.10x is configured but not played, so actual pace, end-screen audio and completed running time are **UNVERIFIED**. All three are proposed **illustrated Long 16:9**, not 2-minute Shorts; Nuviko has a Long format in ChannelSpec. Each EN/RU script is a complete distinct narrative with its own introduction, causal middle and result, not a cut of a master. Git SHA-1 blob IDs are recorded in [handoff](handoff.md); the SHA-256 above is of exact complete UTF-8 bytes, including final newline.

## Distinct story maps (exact files above)

- **02m:** three concrete opening questions about engine-only control → blast in tail → hydraulic redundancy destroyed → asymmetrical thrust as last remaining direction control → Denny Fitch helps → Sioux City approach → wing-first crash → 111 killed/185 survived → simulator finding and limited, honest payoff. One tight chain, with minimal investigative aftermath.
- **05m:** three opening questions → ordinary flight and apparently survivable engine failure → unexpected common-cause hydraulic loss → discovery of thrust steering → delay/instability → emergency coordination and Fitch's throttle role → intended runway 31 versus reachable 22 → terrible crash/survivors → fatigue-crack forensic answer and critical redundancy lesson. The investigative answer changes understanding of the opening, rather than repeating it.
- **10m:** opening proposes redundancy/engines/runway paradox → routine departure → engine rupture and cockpit control failure → first asymmetrical thrust discovery → detailed reason thrust is too slow → emergency/Fitch task allocation → pilot choice of runway → wingtip crash and rescue → manufacture defect, missed inspections, three hydraulics hit by one fault → simulator/industry consequences → bounded final answer. This is fully resolved, but the long retrospective explanation may test a viewer's patience after survival is known.

## Eight independent *dimensions* per authored version (not an independent reviewer)

### 02m — STRONG_CANDIDATE (author judgment, confidence medium)

| Editorial dimension | Author score | Exact evidence or honest limit |
|---|---:|---|
| Interest/significance | 9 | “How can two engines become your only way to turn?” plus an airliner with 296 people gives an understandable, consequential contradiction |
| Opening | 8 | Three direct questions signal controls, propulsion and human stakes; first scene can depict still-working wing engines against an unresponsive wheel |
| Development / why remain | 8 | Engine explodes → *all three hydraulics* fail → captain tests a left-thrust change → Fitch takes throttles → right wing drops at Sioux City |
| Payoff | 9 | “The crew did not achieve a safe landing. They achieved something different” explicitly rejects a miraculous safe landing and credits arrival where rescuers could reach survivors |
| Freshness of angle | 8 | Thrust-as-steering and the *limitations* of an improvised approach foregrounded; 2019–2026 competitor coverage means topic itself is not new |
| Visual expressiveness | 9 | Tail-engine rupture, cockpit reaction, differential engine thrust, Sioux City runway, wingtip strike, crash investigation offer distinct reconstructable sequences |
| Natural speech / clarity | 8 | “It is nothing like normal flying” follows a specific mechanical explanation; caution: “hydraulic systems” remains mildly technical |
| Verified audience interest | UNVERIFIED | Search metadata gives publisher coverage but no matched same-author/age baseline or Nuviko audience analytics |

**Main weakness:** 314 EN words leaves little time to explain why three separate hydraulic systems could all fail; that answer appears quickly in the opening and only briefly returns at the end. Strong compressed story, not a 2-minute trailer. **Authorship:** GPT-6 authorial review, not external first listener; **confidence:** medium for causal structure, low for measured viewer interest. Interest/development/payoff >= 8 based on exact narrative, not an averaged composite.

### 05m — STRONG_CANDIDATE / recommended (author judgment, confidence medium)

| Editorial dimension | Author score | Exact evidence or honest limit |
|---|---:|---|
| Interest/significance | 9 | “What if a passenger jet loses every hydraulic flight control at once?” frames a meaningful system failure with 296 people aboard |
| Opening | 9 | “Could you turn it using only its engines?” plus “why ... reach an airport at all?” defines two answers the story will actually give |
| Development / why remain | 9 | Thrust steering discovery → delayed responses → Fitch arrives → cannot turn enough for the longer runway → approach remains too fast → wing strike |
| Payoff | 9 | “Flight 232 was not a successful landing” and official simulation outcome complete the promised answer without erasing the 111 deaths |
| Freshness of angle | 8 | Emphasis on impossible rescue-as-flight-control paradox rather than clickbait “miracle”; prior well-known coverage is an originality constraint |
| Visual expressiveness | 9 | Cockpit throttle hands vs disabled wheel, independent hydraulic circuits, 31-to-22 alignment, right wing contact and fractured titanium disk support material change |
| Natural speech / clarity | 9 | “They cannot simply point the nose at a runway and hold it there” translates the aerodynamic constraint into everyday language |
| Verified audience interest | UNVERIFIED | Same-author comparable-format age baseline, current public pace, comments and private channel retention unavailable |

**Main weakness:** introductory three questions risk feeling rehearsed and the fatigue-disk explanation after crash needs a visually specific pivot to preserve momentum. The narration deliberately says the landing was *not* successful. **Authorship:** GPT-6 authorial review; **confidence:** medium editorial, low audience. Threshold interest/development/payoff >= 8 independently met.

### 10m — REWORK, completed text (author judgment, confidence medium)

| Editorial dimension | Author score | Exact evidence or honest limit |
|---|---:|---|
| Interest/significance | 9 | Opening contrasts “three separate systems” with “one engine failure destroys all three” and a survivor question |
| Opening | 8 | “If the pilots reach an airport, does that mean they can land?” offers a distinct second promise, but the familiar catastrophe might be recognized before details |
| Development / why remain | 7 | Engine failure → throttles → Fitch → runway change is strong, but long manufacturing-and-inspection explanation follows after complete crash payoff |
| Payoff | 9 | “You cannot reliably land a DC-10 by steering with two engines alone” and 185 survivors close the promise without inventing a successful landing |
| Freshness of angle | 8 | Common-mode redundancy failure and accountability of inspections are more useful than replaying the crash, though already documented by FAA |
| Visual expressiveness | 9 | Two-stage cockpit and investigative sequences have clear contrasting physical objects, but engineering details could become visually repetitive |
| Natural speech / clarity | 8 | “It is not a trick that gives them their airplane back” is plain and precise; after the crash, “This was not simply a story about a pilot missing a button” risks a secondary lecture |
| Verified audience interest | UNVERIFIED | No validated 10-minute Nuviko analogue or current matched YouTube audience demand |

**Main weakness:** by “Now ask a different question: how could three supposedly independent hydraulic systems fail together?” the dramatic resolution has occurred. The second half risks feeling like an appended technical report. It is **complete**, not a filler-padded five-minute draft; its extra material has factual value but weaker likely editorial pace. **Authorship:** GPT-6; **confidence:** medium for mechanism, low for demand. Development 7 means **NOT STRONG_CANDIDATE** despite other ratings.

## Comparison on completed versions, with independent loss points

| Transition | What the viewer actually gains | What they risk losing |
|---|---|---|
| 02m → 05m | More cause/effect: why throttle adjustment cannot replace the wheel, Fitch's role, runway 31 vs 22, and disk-fatigue explanation of all-three systems failing | Tighter 02m payoff arrives sooner; 05m technical investigation arrives after impact |
| 05m → 10m | Real manufacturing and inspection failure chain; limitations of redundancy, safety recommendations, fuller visual sequence of landing choices | Investigative tail begins after survival figures. Long answer competes with earlier completed emotional climax |

**Recommendation: 05m** based on meaningful new obstacles and a second scientific payoff without 10m's prolonged post-impact section. No assertion that its 9/10 editorial ratings predict retention or that 10m must be chosen. Likely scroll-away/click-off points: **02m** initial third question and the quick shift from hydraulics to Fitch; **05m** disk explanation immediately after rescue; **10m** the extended inspections and regulatory aftermath. Those are author hypotheses, not real viewer measurements.

## Separate gates/checks (self-check only)

| Gate | 02m | 05m | 10m | Evidence boundary |
|---|---|---|---|---|
| Core facts and bounded causal language | PASS (author-source check) | PASS (author-source check) | PASS (author-source check) | NTSB accident brief + FAA lessons-learned detailed mechanism; check official source again before approved master |
| EN ↔ RU important facts/uncertainty | PASS (author semantic read) | PASS (author semantic read) | PASS (author semantic read) | Same 296/111/185 and thrust-vs-control distinction, not syntactic translations |
| Channel format | PASS (proposed Long) | PASS (proposed Long) | PASS (proposed Long) | Current active `nuviko_history` ChannelSpec has long 16:9; no production run |
| Long intro / payoff | PASS (author review) | PASS (author review) | REWORK (pacing) | Short question promise first, whole causal story; fact explanations must remain compelling |
| Narrative Short loop | N_A | N_A | N_A | All are Long; no fictitious AV loop |
| Media rights and actual historical reference images | UNVERIFIED | UNVERIFIED | UNVERIFIED | No images, media assets or licence checks in this Git-only draft |
| Actual voice/timing/MP4 seam | UNVERIFIED | UNVERIFIED | UNVERIFIED | No TTS, scene generation or render |
| Independent first listener `ytv-script-review-v1` | UNVERIFIED | UNVERIFIED | UNVERIFIED | No authorized separate independent reviewer session/receipt; self-check not equivalent |
| Official runtime script gate / owner approval | UNVERIFIED | UNVERIFIED | UNVERIFIED | No local `ytv start`, pinned packet, or approval; Draft is not production authority |

**Review iterations:** initial full versions and authorial scoring only (0 additional major rework passes); no invented independent reviewer verdict. The next step is actual independent reading of exact immutable hashes, first without this story map and author scores, and only then the source ledger. If the text changes, new hashes require a new review. No attempt to add a faux reviewer JSON.
