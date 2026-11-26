# Story review — exact 2/5/10-minute bilingual scripts

**EDITORIAL_CANDIDATE_UNREGISTERED** — writer's own evaluation; **no independent reviewer, no official `ytv` script gate, no approval**. Assessed 2026-11-22; current 10m revision 2026-11-24 (see latest section). One story: 1988 TACA Flight 110 dual flameout, grass levee, and June 6 ferry departure from a repurposed former runway-road.

## Exact files, language and time estimate

| Version / format | English narration master (SHA-256 of exact UTF-8 bytes) | Full semantic Russian (SHA-256) | Actual count; estimated length | Editorial classification |
|---|---|---|---|---|
| 02m / proposed **Short** | [EN](variants/02m/script.en.txt) · `9281d376a2d87fbb5ed2a3e552a66f86cba465a7dc78ef1ba7a6983e0492f60d` | [RU](variants/02m/script.ru.txt) · `61bd6db12240e2dc497f58f55497fb0b450a01cea40fb31338b9c6446a8f1345` | EN 274 words, ~1.71–2.07 min at hypothetical 145–160 wpm plus pauses; no real audio | **REVISED, text-only seam promising; independent and AV UNVERIFIED** |
| 05m / proposed **Long** | [EN](variants/05m/script.en.txt) · `c3c18e9d5a3a1eeefa8c55c72ba9441d1fe35e07ecde9aed3231ab8394943570` | [RU](variants/05m/script.ru.txt) · `023df0d81d1b4c7be1a44c60a27b63d6fc18460c58c2091d0d32047d88777fd3` | EN 699 words, ~4:40–5:15 with pauses | **STRONG_CANDIDATE — recommended** |
| 10m / proposed **Long** | [EN](variants/10m/script.en.txt) · `1956342d2649f9cf3ce85825ccbda3408076ada786589c492ed0e8addf74ffee` | [RU](variants/10m/script.ru.txt) · `0ed137fb8dd085c980cc80ebc6765a388711556e04d93fcd3ee3a549f7f4ce0b` | EN 1404 words / RU 1160 words, estimated only | **REVISED — REWORK for pace; 05m recommended** |

Duration is **not measured**: no real voice audio, no listening, no edit. WPM range and pauses are author assumptions, not provider measurements; actual configured voice is 1.10x, but effective WPM unknown. The English text, not the Russian review translation, is production master.

### Exact hashes — origin

Calculated over the six final Git blobs as literal UTF-8 bytes (not normalized or line-wrapped). Historical Git blob IDs at the 2026-11-22 assessment in order 02m EN/RU, 05m EN/RU, 10m EN/RU: `679cc7929c9f92216b13a267ad6bacdce8ec2f32`, `8793f7bacfc8e13cb33d35a878dbc4b34f0b6f60`, `dda238581e38aa0711d03ed3cd14f5972518f31e`, `ff9b00d5fd9d2d6e82709b15dea15383230106fa`, `2c70ba92507234e3d31f59cc47a609648ab261f1`, `2f0d0f7215d9dd02e5ea17009afef26b683a3128`. Current 10m Git blob IDs (EN/RU): `c90d839c9608d6549d4b96849c1371303d3ff014`, `65340364a29b1f56a5d239bba2d3c7fbf8d670fa`. The first four blob IDs are unchanged. Any new edit invalidates the associated hash-bound assessment.

## Eight editorial criteria per exact completed version

**Authorship:** same drafting writer and **self-review**, confidence **moderate** for text structure, **high** for source-linked basic events, **low** for response of an actual first listener. Scores are editorial judgements from the listed literal lines and source chain, **not** probabilities, viewer data or measured retention. `UNVERIFIED` is not zero.

### 02m — proposed Short, substantive revision of 2026-11-22

**Exact baseline:** original 284-word EN, SHA-256 `dcb503348469a23b8c925d804ba90e0e01aace7ab17e1934cb16baf08754afb4`; original RU `e7e37ff044841fdccf6026507162db58a67227c24c0e4d7919e1e8ef6e03fdee` at PR HEAD `266b458a8aab66f3063cc2e913cef223f379d9d6`. **Current:** EN `9281d376a2d87fbb5ed2a3e552a66f86cba465a7dc78ef1ba7a6983e0492f60d`, RU `61bd6db12240e2dc497f58f55497fb0b450a01cea40fb31338b9c6446a8f1345`. No alteration to 05m/10m, original sources, or approvals.

| Criterion | Score / evidence and confidence |
|---|---|
| Interest / significance | **8/10**, moderate — two linked concrete problems, powerless jet with 45 on board and a stranded airliner, backed by FAA and 1988 UPI |
| Opening | **8/10**, moderate — “A Boeing 737 was gliding toward a strip of grass beside a canal. Neither engine was producing usable thrust.” gives a cold viewer both danger and visible destination; less surprise left for touchdown |
| Development / reason to continue | **8/10**, moderate — hail → failed airflow relight → ignition without stable idle → inaccessible airport → water contingency → levee → recovery on former runway-road; each event changes the next problem |
| Payoff | **9/10**, moderate — “Seventeen minutes later, they reached New Orleans airport.” answers the practical second-flight question rather than leaving the plane stranded |
| Freshness of angle | **7/10**, moderate — planned ferry flight after the landing is a distinct follow-through, though other aviation accounts exist |
| Visual expressiveness | **8/10**, moderate — grass levee beside canal, NASA grounds and old runway-road are distinct, documentable visual intents; source-image rights and actual shots unverified |
| Speech naturalness / clarity | **8/10**, moderate — names the two engines' lack of *usable thrust*, avoids saying an ignition was a successful restart; the final ground-ahead transition needs actual listening to judge |
| Verified viewer interest | **UNVERIFIED**, low — no creator-matched retention, CTR, fresh demand or actual commentary; public video counts are not a grade |

**Was → now:** earlier 02m opened by revealing the successful landing, repeated “both engines” in successive lines, and finished with the symmetrical grass/road aphorism. This text begins at the still-unresolved approach, shows the failed restart before the landing, makes the stranded-aircraft recovery a second practical decision, and contrasts the emergency with a deliberately prepared ferry flight. Same evidence, no invented feelings, quotations or touchdown details.

**Text-only Short loop:** full English and Russian narratives were authored with a return from “the pilots had only the ground ahead” / “оставалась только земля впереди” to the first visible approach to the grass strip. There is a concrete temporal/visual dependency, not just a repeated keyword, colon or a compulsory final question. **Author assessment: provisional continuity, not independent PASS.** Two complete cycles by an independent first-time reviewer and exact AV seam remain **UNVERIFIED**. A meaningful weakness is that the reprise still revisits an already resolved emergency and could feel repetitive in performance.

**Format:** 02m Short supported by current Nuviko ChannelSpec. Full resolved human/aircraft outcomes occur before the return beat. Actual voice timing, image rights, viewer response and runtime gate **UNVERIFIED**.

### 05m — recommended Long

| Criterion | Score / evidence and confidence |
|---|---|
| Interest / significance | **9/10**, moderate — the audience has two understandable unanswered problems, survival and recovery, not just a puzzling technical failure |
| Opening | **8/10**, moderate — “What do pilots do when both engines of a passenger jet go silent?” followed by two related questions; clear promise, perhaps slightly many questions for short Long |
| Development / reason to continue | **9/10**, moderate — windmill→APU ignition without idle→glide→levee→NASA old runway→ferry departure; each event changes what a listener expects |
| Payoff | **9/10**, moderate — “It lifted off and flew about seventeen minutes to New Orleans International Airport.” closes recovery; final contrast separates emergency from planned flight |
| Freshness of angle | **8/10**, moderate — emphasizes documented June 6 road departure, a genuine second act which standard emergency-landing snippets omit |
| Visual expressiveness | **8/10**, moderate — sequence can be illustrated as distinct weather, cockpit *without invented dialogue*, levee, NASA facility and road/old runway; source photo rights unresolved |
| Speech naturalness / clarity | **9/10**, moderate — “The engines had not just switched off like lights”; explanation grounds ignition vs useful thrust without technical jargon taking over |
| Verified viewer interest | **UNVERIFIED**, low — 2026 summer video is outside 90-day fresh interval; no measured Nuviko audience response |

**Main flaw:** a few explanatory phrases around “fuel and hail” and the FAA conclusion are less visceral than the landing, and the two introductory questions plus third promise may use 15–20 seconds. Still a coherent one-story five-minute narrative. **Judgement:** **STRONG_CANDIDATE** because interest 9, causal development 9, payoff 9, with concrete evidence; this classification does **not** grant approval, independent PASS, or production permission.

### 10m — historical assessment (superseded by 2026-11-24 section below)

| Criterion | Score / evidence and confidence |
|---|---|
| Interest / significance | **8/10**, moderate — two unusual airfields plus lasting engine-safety changes |
| Opening | **8/10**, moderate — clear questions “Why would a Boeing 737 need a flood levee…?” but the later science answer is less immediately personal |
| Development / reason to continue | **7/10**, moderate — second half accurately differentiates rain, hail, fan/core and certification, but prolonged after survival and ferry flight |
| Payoff | **9/10**, moderate — definite no-injury landing, real prepared transfer flight, and hardware/FAA changes resolve all three introductory questions |
| Freshness of angle | **7/10**, moderate — investigation is informative but longer technical breakdown overlaps existing aviation explainers |
| Visual expressiveness | **7/10**, moderate — physical aircraft/levee/road vivid; core-flow explanations risk prohibited generic diagrams and repeated metal closeups |
| Speech naturalness / clarity | **8/10**, moderate — plain analogy for gliding; “certification testing” paragraphs more essay-like than live oral story |
| Verified viewer interest | **UNVERIFIED**, low — no creator-matched baseline for a technical 10-minute cut, no transcript or content analysis |

**Main flaw:** “But the more important technical question had not disappeared…” begins extended explanation **after** the ferry payoff; despite additional verified detail, narrative energy falls. **Judgement:** `REWORK` because development 7, even with strong payoff. Do not force a 9 to improve the average. All three versions are *complete standalone scripts*, even though 02m and 10m do not clear editorial recommendation.

## Historical comparison (2026-11-22; see current revision below)

- **2 → 5:** revised 02m now preserves ignition without stable idle and the water-landing contingency, but 05m adds spatial and physical explanation of glide, damage inspection, NASA runway constraints, and a fuller transition from rescue to repair. At the 02m fast hardware-summary line the audience may not absorb why earlier tests failed; 05m stays the recommendation.
- **5 → 10:** 10m adds original test conditions, airspeed/fan speed effects, spinner/splitter/bleed-valve modifications and procedural changes. Genuine researched material, **not padding or another story**, but too much after the landing and road flight; at “Earlier certification tests had not reproduced…” a general-interest listener may stop waiting for the next human event.
- **Recommendation:** **05m, illustrated Long**, Nuviko supports Long in ChannelSpec. 02m is stronger as a cold Short after substantive revision but awaits an independent full two-cycle review and actual AV seam; 10m suits engineering-focused audiences only after a reasoned reordering or tighter research-film brief. No preference for length itself.

## Historical checks — separate from editorial grades (10m superseded below)

| Check | 02m | 05m | 10m | Boundaries |
|---|---|---|---|---|
| Fact/causality, self cross-check | PASS (writer's source mapping only) | PASS (writer's source mapping only) | PASS (writer's source mapping only) | FAA flight/hail and UPI recovery; contemporary occupancy conflict recorded in research; this is not independent fact review |
| EN↔RU semantic equivalence, writer | PASS (author check) | PASS (author check) | PASS (author check) | Same event order, 45, repaired vs emergency, road/levee, uncertainty; native-reader QA unavailable |
| Channel/format compatibility | PASS for proposed Short | PASS for illustrated Long | PASS for illustrated Long | Nuviko ChannelSpec permits both; *not* runtime registration |
| Natural spoken Short loop | **AUTHOR TEXT-ONLY PROVISIONAL; independent two-cycle and AV UNVERIFIED** | N_A | N_A | Return to visible approach after complete landing and ferry payoff; not proof of audible seamlessness |
| Unverified extra claims / licensing | UNVERIFIED | UNVERIFIED | UNVERIFIED | Actual photography/film rights not checked, generated reference bytes none |
| Independent first-listener review of exact text | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | Fresh independent session/reviewer capability unavailable in this run |
| Actual audio length, sound, image and MP4 | UNVERIFIED | UNVERIFIED | UNVERIFIED | None produced, no narration playback or timed frames |

**Revision attempts:** 02m received a second, substantive narrative writing pass; 05m/10m remain first-pass complete texts. No independent revision cycle or fabricated reviewer. The text-only seam is provisionally coherent but not independently validated. No approval requested or inferred. Existing accepted source scripts/active runs untouched.

## Historical story map: expectation → evidence → payoff (10m superseded below)

- **02m revised** opens while the jet is still approaching the grass; hail → two distinct failed restart approaches → water contingency → levee landing → no-injury passenger payoff → stranded plane → planned road ferry → limited technical explanation → ground-ahead reprise. Spoken seam author-only, independent full double cycle and AV UNVERIFIED.
- **05m** introductory questions → ordinary flight → 30s hail and failed restart (main hook) → levee and no injuries → airplane recovery problem → old road runway takeoff → why hail tests mattered → complete conclusion. Questions answered inside story.
- **10m** asks three linked questions → descent details → engine loss → failed restart and glide → emergency landing → logistical ferry → why certification misread hail → modified hardware → bounded conclusion. At the marked post-ferry explanatory section, interest may fade.

**Production blocker / next evidence:** on a local host run `uv run ytv start --channel nuviko_history --format long --intent '<authorized story selection>'` and read `plan_summary`, `read_next`, `task_guide` and pinned reference documents; do not claim the Git-only drafts are an approved run. For an exact owner-selected source use the documented source-import path after an actual selection message. Obtain independent reader's literal two-cycle input for a Short, record the actual schema response and new hash. For the recommended Long obtain independent review before detailed storyboard/preproduction, validate actual channel refs, then report the exact master for owner decision. Nothing here authorizes TTS, images, MP4 or upload.

## 2026-11-24 — current 10m substantive revision (supersedes ONLY old 10m assessment and comparison)
**Baseline** `85731c3ab0c142bee18abf7c9414f703a299f34e` (old 10m EN/RU SHA-256 `f9688fef7a15918377ba298a249b6a1c9f0877e217d0dd3d7cb7849f52072c55` / `295d126bd7c7ce91f0a0a74476fb9f98fad633ea708909807c101bef1181dd10`). Baseline four other exact scripts, 02m/05m evaluations above retained. New 10m [EN](variants/10m/script.en.txt) SHA-256 `1956342d2649f9cf3ce85825ccbda3408076ada786589c492ed0e8addf74ffee` (1404 words); [RU](variants/10m/script.ru.txt) `0ed137fb8dd085c980cc80ebc6765a388711556e04d93fcd3ee3a549f7f4ce0b` (1160 words). Duration estimate 9.06–11.23 min of speech at hypothetical 125–155 effective wpm, plus pauses and 10s Long end screen, exact TTS UNVERIFIED. No change to approved channel voice speed. Prior 10m verdict/hash is history, not review of this manuscript. Source main a6023668001421b689a8142cebc0bd436545be6b; #124 merged.
 
**Was → now:** after the road takeoff the former story repeated the premise and delivered a long general engine lesson. Now investigators find right turbine damage but no visible left-engine damage; ground checks, tow and a test departure form a real second act; the temporary May 30 rule precedes June 6. The previous 1987 incident and the left-engine experimental reproduction resolve the earlier certification contradiction, with final regulatory consequences in 1998. No invented cockpit or passenger reaction. The original 05m has the clearest double payoff and remains the recommendation.

| Current exact 10m criterion | Score and concrete evidence / confidence |
|---|---|
| Interest / significance | 8/10 moderate — safe evacuation and the left/right engine contrast give two human/practical problems, not an abstract weather lecture |
| Opening | 8/10 moderate — three questions promise levee, dual failure and departure; concrete descent power matters before the hook; slight risk of three questions in succession |
| Development | 8/10 moderate — the inspection gives a different result for each engine, tow/repair and power checks lead to departure; the post-ferry precursor and test still form a slower investigation act |
| Payoff | 9/10 moderate — people safely evacuated, employees witness departure, seventeen-minute trip completed; surviving engine reproduces the problem, revised standards give lasting answer |
| Freshness | 8/10 moderate — asymmetric engine damage and testing the left engine are distinct from a familiar miraculous-landing clip; competing aviation coverage remains |
| Visual expressiveness | 8/10 moderate — wet grass, working exits, inspection probe, tow, workers watching; later technical details risk repetitive engine closeups, no actual assets |
| Natural speech | 8/10 moderate — concrete actions, cause-linked explanation; the airflow paragraph is still dense and the last technical act may need a shorter reading |
| Confirmed viewer interest | UNVERIFIED low — no actual audience measurement, comments, creator baseline or current comparable data |

**Story map / proposed scene spans (paragraph numbers 1-based, not measured; no storyboard or media):** 1–6 questions, route, reduced power, hail and power loss (weather/737, no invented radar reading); 7–13 control and unsuccessful restart/ditch contingency (cockpit reconstruction without invented dialogue); 14–17 grass landing and evacuation (landward grass, wet surface and used exits); 18–22 inspection, two different engines and tow/ground checks (inspection, tow and NASA site, no invented repair tools beyond source); 23–27 departure preparation, May 30 directive, June 6 ferry (private former runway, employees watching); 28–33 safety investigation and outcome (1987 precursor shown distinctly; source-led engine cross-section or real rights-checked images, not fake archive). Verify actual spans and timing for any selected master; no scene prompts, actual assets or storyboard claimed. Paragraph count 33 per language; spans are rough editorial groups.
 
**Hard checks:** author source/causal check against shared research incl. new ledger: no reported injuries, 45 (official injury matrix), 2,552 ft rounded, ~2 miles / ~3 km, 6 and 13 day intervals, 17-minute ferry, right vs left damage, May 30 interim change, 1987 earlier flight, 1998 rule. Author EN/RU paragraph pair check: same actions, uncertainty and outcome; independent bilingual/first listener UNVERIFIED. ChannelSpec supports Long, loop N_A for 10m; preserved 02m two-cycle independent/AV still UNVERIFIED. Actual duration, selected storyboard, voice, rights, runtime registration, actual lease, owner decision and audience demand remain UNVERIFIED; no independent review receipt. Exact old 10m timing/review invalidated. 
   
**Finished text comparison (02m and 05m preserved):** 02m compact standalone complete action; 05m adds distinct engine restart and ferry logistics without lengthy forensic act; 10m now adds inspection asymmetry, prepared ferry, interim directive, 1987 warning and test reproduction. After the June 6 payoff, the turn to "There had been a warning the year before" risks loss of attention among general-history viewers; that new evidence is valuable but shifts genre toward investigation. 05m still recommended rather than rewarding length. 10m is revised candidate, REWORK for pace until independent first listener; timing estimates not measured. Status three versions prepared -> author checked -> 05m recommended, not approved. Next: exact-hash independent review if a real reviewer becomes available, working canonical runtime transfer before one master; continue remaining backlog, not another cosmetic pass. No media/merge.
