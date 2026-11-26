# Operation Jaque — substantive 2/5/10 editorial review (2026-11-16)
**Status:** EDITORIAL_CANDIDATE_UNREGISTERED / UNVERIFIED (not runtime, not user approval). Author: ChatGPT editorial audit, not independent first-listener. PR #103 baseline `fd471f4cbc7314c3e5778a69ced26247a71c2ec3`. Canonical three-duration rule now on `main` (`e8f2b5488b266ebc89ea7ef48360df7584088e82`); its original proposed PR #124 / `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is merged. Source master and its existing `storyboard.json` unchanged.

## Exact six texts
| Variant | EN full | RU full | EN words | RU words | SHA-256 EN | SHA-256 RU |
|---|---|---|---:|---:|---|---|
| 02m | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 247 | 209 | `1fa1bff2d2c050ebc50de665a4b066d534ddf2549cf96de1f700c91c9adb1bd1` | `8f99db43a0ef875d2497603322ca6d99ca28d6db852f4e0ab0b53f948be9258e` |
| 05m | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 691 | 568 | `32ee00391140e46494a16fe41ef7fb9603ef84703b968d50a2cc5c9f8aa65189` | `6d501b0647f75eb2a87dfaacb588ea001d841711cc1a5d36bef48db79c929d0e` |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1259 | 1010 | `d63270cea7a2f2fbd26f5ba872fa520a6dc1763e407219cf94c8ca116a28bf19` | `b365deacd347b77a4211d2f792bed880ae87a7bd5290634b77909402e37302b1` |

No TTS measured. At a hypothetical 145–175 English words/min before actual voice speed/pauses: 02m 247 words, 05m 691 (~3.9–4.8 min without pauses), 10m 1259 (updated 2026-11-25; see new estimate below). This does not establish actual duration, which needs approved TTS and montage; no voice speed change is authorized.

## What changed (old → new)
- Baseline `script.en.txt` blob `7413851f1368dd42ac76766f8a2013c2642e0866`, RU `37ca2d9a6f7ccdcbed7162928801bfba0abd0e4d`, 569 EN words: strong documented agency reversal, actual rescue and humanitarian emblem postscript; **preserved unchanged** with its original 44 aligned storyboard spans.
- Former opening revealed the rescue before questions and provided a 569-word single narration. Now every Long version begins with precise viewer questions before historical immersion and progressively reveals command spoof → credible aid disguise → prisoners and captors boarding → midair reversal → consequences.
- 02m is an independent closed rescue story, not just a trailer. 05m adds actual January humanitarian precedent and the guard's decisive choice. 10m adds distinct sourced mechanisms (three separated hostage groups, radio imitation and background sounds, individual captivity history, later conflicting footage and disputed claims) rather than repeating a summary. Ten-minute factual expansion has limits and must not be portrayed as reconstructed actual radio dialogue.
- Neither old master nor its existing storyboard/approval/timings are applied to the new texts. No independent reviewer, runtime or production created.

## Causal story maps & hard checks
**02m:** questions (why captors board/why no gunfight) → multi-year captivity motivates avoiding an armed raid → reported false command + cover → bound boarding with both guards → airborne reversal → 15 freed without shots → actual misuse of protected emblem acknowledged → final return to those boarding. Human line is prisoners, not hypothetical quotes. Possible weak point: little time with people before rescue.

**05m (revised 2026-11-19):** questions → fifteen captives, remote holding and raid risk → Betancourt's captivity and other prisoners → military-attributed false FARC instruction → January 2008 humanitarian handover precedent → disguises and government-described fictitious NGO website/phone → helicopter arrives with soldiers posing as aid staff → César and second commander escort the bound hostages → midair arrests → Betancourt and others' documented relief → acknowledged Red Cross emblem misuse and conditional harm to real aid workers → final reversal. Main weaknesses: government order detail cannot be independently authenticated from the cited radio bytes; ethical coda follows emotional climax.

**10m (revised 2026-11-25):** questions → Betancourt's capture and families' years apart → Stansell's radio messages / Gonsalves's chess set → army chooses rescue without battle → attributed false order and humanitarian appearance → captors accompany prisoners → freedom → two family reunions and chess set seen after release → emblem misuse and disputed accounts → chess set payoff. Main risk: three late ethical/dispute paragraphs after emotional reunion.

**EN/RU comparison:** all six texts were author-read against their language pair for same subject, agency, temporal order, number of freed captives, asserted vs reported facts, absence of invented direct quotation. Bilingual independent verification UNVERIFIED. Specific 10m nuance: later video reporting undercut an initial spontaneous-emblem explanation; no settled insider motive is asserted.

**Narrative checks:** Long questions before immersion PASS (author text inspection); distinct standalone payoff PASS (author inspection); Long loop N_A; source claim ledger covered for added detail; sound/visual synchronization, actual spoken timing, thumbnail and filmed sequence UNVERIFIED; independent script review UNVERIFIED; owner approval **NOT GIVEN**. Original `storyboard.json` belongs only to original `script.en.txt` and `script.ru.txt` Git blobs above; there are **zero** verified scene spans for the variants. This is a pre-production editorial bundle.

## Eight editorial criteria — author assessment, not measured audience behaviour
Scores are judgement of exact new scripts, not retention probabilities. Last criterion is UNVERIFIED for each variant.
| Variant | Criterion | Score /10 | Concrete evidence | Main weakness | Confidence |
|---|---|---:|---|---|---|
| 02m | Interest/significance | 8 | 15 prisoners and 2 guards board same rescue flight | unfamiliar English-audience setting | medium |
| 02m | Opening | 8 | paired questions state voluntary escort and no gunfight | limited context for FARC at cold start | medium |
| 02m | Development | 7 | false order → aid cover → boarding → overpower | intermediate obstacle compressed | medium |
| 02m | Payoff | 8 | all fifteen freed before ICRC coda | emotional exit passes quickly | medium |
| 02m | Freshness | 7 | guards voluntarily entering rescuers' aircraft | historical rescue already covered publicly | medium |
| 02m | Visuals | 8 | misleading helicopter and midair role reversal | archival rights/references absent | medium |
| 02m | Spoken clarity | 8 | consecutive active verbs, no abstract moral | terms César/FARC need clean pronunciation | medium-low |
| 02m | Verified viewer demand | UNVERIFIED | indexed public videos only | no comparable CTR/retention | low |
| 05m | Interest/significance | 8 | Betancourt, 3 Americans and 11 Colombian uniformed captives under guard; human relief after years | other prisoners are not individualized | medium |
| 05m | Opening | 8 | rescue without gunfire, voluntary escort and humanitarian ethics promised | third promise competes with rescue stakes | medium |
| 05m | Development | 8 | raid risk → apparent internal order → January precedent → NGO disguise → escort → midair rescue | website is attributed to government, not known to have been visited by César | medium |
| 05m | Payoff | 8 | hostages' reported tears/embraces and detention of their guards before ICRC consequence | protected-symbol coda could lower momentum after rescue | medium |
| 05m | Freshness | 8 | fake NGO website and phone are specific 2008 government-reported cover steps | claims about what guards verified would be speculation | medium |
| 05m | Visuals | 8 | held passengers, crew masquerade, escorted boarding, airborne detention | no licensed footage or verified new storyboard | medium |
| 05m | Spoken clarity | 8 | specific actions and named captives before explaining the disguise | some long sentences still need first-listener review | medium-low |
| 05m | Verified viewer demand | UNVERIFIED | public YouTube snapshot only | no comparable English-channel baseline, CTR or retention | low |
| 10m | Interest/significance | 8 | Stansell hears his children without seeing them; Betancourt's children grow up during captivity | the rescue outcome is already promised | medium |
| 10m | Opening | 8 | three concrete questions about rescue, captors and apology; captive stakes follow | third question competes with family line | medium |
| 10m | Development | 8 | individual captive experiences → high-level official deception → escort and release → reunions | paragraph beginning 'The appearance of a humanitarian flight' may slow progression | medium |
| 10m | Payoff | 9 | radio voices become a real meeting; chess set returns as tangible object | emblem dispute interrupts emotional peak | medium |
| 10m | Freshness | 8 | Stansell's first meeting and Gonsalves's set expand the familiar rescue angle | chess connection is editorial, not naming evidence | medium |
| 10m | Visuals | 8 | radio, chess pieces, adult children on aircraft steps, family meeting | no licensed reference shots / no verified storyboard | medium |
| 10m | Spoken clarity | 8 | short actions, named people, explicit timeline and fewer repeated mechanism explanations | political names and final dispute still need first-listener check | medium-low |
| 10m | Verified viewer demand | UNVERIFIED | historical indexed public results only | no actual comparable audience data | low |

## Comparison of actually finished texts
| Upgrade | New verified value | Exact retention risk / where editor would inspect |
|---|---|---|
| 02 → 05 | Betancourt timeline, January 2008 legitimate humanitarian precedent, why César accepts the transfer, dramatic role reversal in flight | paragraph beginning “The aircraft also had to look credible”: distinguish a government-described fake website from evidence anyone checked it; keep emblem section short after full rescue |
| 05 → 10 | Stansell's children and radio messages, Gonsalves's chess set, Betancourt's reunion, later emblem-video dispute | "The appearance of a humanitarian flight" and the three paragraphs starting "The rescue was celebrated" after emotional resolution |

**Editorial recommendation: 05m, revised exact SHA-256 as above.** Enough causal proof for the human rescue and the serious ICRC consequence, without taking ten minutes before the final answer and without skipping the guard's reason for accepting the flight. 02m is a worthy tight alternative if independent listening finds the ethical chapter too long; 10m is conditional on fresh review and actual voice timing, not presumed better due to length. No version approved for production, no independent verdict.

## Claim evidence (one shared research)
See `research.md` original detailed contemporary sources and 2026 audience snapshot; added source ledger and uncertainty in its 2026-11-16 supplement. No original footage watched; no direct radio transcript, payment proof, or actual AV reference; demand and real reviewer UNVERIFIED. Review status by exact SHA-256 above; new hash invalidates review of previous variant only. Next unprocessed Long in historical review queue: PR #101 Tunnel 57, pending fresh status and no conflicting actor.


## 2026-11-19 substantive existing-PR revision
- **Before → after:** baseline PR #103 HEAD `2986761d12d25ff81f142c245f4f692ed4e71e46`; previous 05m EN/RU SHA-256 `716d0661fc28d2157e01af896753f25307f01abf9622d97ac00c312397825837` / `0ad582d211bb280b21e4f9a474aa5b40e6ba726c0129a333cbf812bb73b1283f`. The old 05m second paragraph disclosed the hidden military crew before the viewer understood the captive risk, and the rescue aftermath relied on summary. The revised 05m first shows the captives and danger, explains the apparent FARC order and why a humanitarian transfer seemed plausible, then resolves the voluntary boarding/airborne detention and Betancourt's reported human reaction. The cover now includes the specifically attributed fake NGO website/phone with no fabricated claim the guards inspected them. No other script version changed.
- **Full exact 05m files:** [EN](variants/05m/script.en.txt) (32ee00391140e46494a16fe41ef7fb9603ef84703b968d50a2cc5c9f8aa65189, 691 words); [RU](variants/05m/script.ru.txt) (6d501b0647f75eb2a87dfaacb588ea001d841711cc1a5d36bef48db79c929d0e, 568 words). Eleven meaning-aligned paragraphs in both languages. Other hashes in table unchanged; original source master and storyboard are protected.
- **Three versions compared:** 02m has complete reversal but omits the humanitarian precedent and team cover; revised 05m adds the decisions making that reversal credible and personal relief, with a brief ethical consequence. 10m previously added separated groups/radio background and video controversy; the 2026-11-25 revision below supersedes that assessment. **Recommend 05m editorially**, not as a production approval.
- **Checks:** author-read full EN/RU text and source-ledger matches; documentary Long opens with questions before immersion and its central hook; all 11 EN/RU paragraphs matched for action, agency, numbers, certainty and ending. Estimated duration only. Independent first-listener, second bilingual reviewer, exact narrated timing, scene spans, visual/media rights, audience data and owner decision **UNVERIFIED**. This remains `EDITORIAL_CANDIDATE_UNREGISTERED`, not `awaiting_script_approval`.
- **Next untouched work:** PR #101 Tunnel 57 (verify live head/protection before editing); technical PR #77/#78 code and conflicts are still in scope.


## 2026-11-25 — 10m human-line revision (canonical main a6023668001421b689a8142cebc0bd436545be6b)
- Baseline PR #103 `1ac0c5540ead1ab8d72df9ebee0984223580d3c6`, 10m paths `variants/10m/script.{en,ru}.txt`, baseline SHA-256 EN `e201ca753a560847661590702e348da702d372784e6ec62c5176d88ff7c4c7b0`, RU `81f8f876c9db08218f9f61461e94c5e7909022ecaa50b42d2584827fbb2d6c0e`. New SHA-256 EN `d63270cea7a2f2fbd26f5ba872fa520a6dc1763e407219cf94c8ca116a28bf19`, RU `b365deacd347b77a4211d2f792bed880ae87a7bd5290634b77909402e37302b1`; 1259 EN / 1010 RU whitespace-delimited words, 20 matched paragraphs. Root master, root storyboard, 02m and 05m unchanged. Previous 10m text-only assessment superseded, not inherited. No approval or independent reviewer claimed.
- Added human line: Stansell hears his children through radio in captivity, then meets them after release; Betancourt reunites with her adult children; Gonsalves's chess set gives a concrete object connecting captivity and freedom. Reduced repetitive operational explanation and competing codas; kept protected emblem dispute and uncertain payment allegation. No invented dialogue or connection between chess set and operation name. Historical mechanism is kept at high level, not a reconstruction of exact tactical actions.
- EN pacing assumption 130–155 words/min, 8:07–9:41 before pauses/end-screen; Nuviko Long end screen 10s additional, no actual timing or speed change.

### Exact editorial spans (not storyboard or measured shot timing)
| Paragraphs EN/RU | Visual intent | Function |
|---|---|---|
| 1 | helicopter / question, no real ICRC affiliation implied | promise |
| 2–3 | roadblock, passage of years, aircraft incident aftermath | captivity and stakes |
| 4–5 | radio and homemade chess set, no invented private dialogue | human-line setup |
| 6–9 | rescue decision, abstract command context, humanitarian distinction | main hook and explanation |
| 10–12 | arrival, prisoners, captors, liberation | central payoff |
| 13–16 | family reunions and chess set | emotional consequences |
| 17–19 | protective emblem issue; attributed reporting, no claim of later harm | ethical consequence |
| 20 | chess set / departure motif, no assertion of name origin | final human image |

Author hard checks: documentary Long questions before immersion then principal hook in paragraph 6; all three promises answered in 11–12 and 17–19. EN/RU 20/20 paragraphs compared by agency, dates, quantities, causation and uncertainty. Existing research supports historical rescue; new claims supported by the dated source supplement. Long loop N_A; timing/rights/native runtime/independent reviewer/owner approval UNVERIFIED. Scene spans here are paragraph-level planning, not timed storyboard. Future 10-second linked end screen requires actual selected compatible next-video input, UNVERIFIED; do not invent target/clip. Format supports Long; no production initiated.

**Comparison:** 02m is complete but gives little time to families; 05m supplies causal context and relief with fewer post-rescue turns; 10m uniquely shows lost years via the twins, adult children and chess set. After the reunion, the emblem/video dispute may feel like a second ending; recommend **05m** for pace, 10m for a human-focused documentary if independently reviewed and actual duration fits. Not an approval. Remaining: fresh independent reader, runtime registration, selected version, actual timing and production handoff. Next: inspect next unaccepted Long #104 and technical conflicts #77/#78 at fresh heads; no duplicate production.
