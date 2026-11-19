# Operation Jaque — substantive 2/5/10 editorial review (2026-11-16)
**Status:** EDITORIAL_CANDIDATE_UNREGISTERED / UNVERIFIED (not runtime, not user approval). Author: ChatGPT editorial audit, not independent first-listener. PR #103 baseline `fd471f4cbc7314c3e5778a69ced26247a71c2ec3`. Canonical three-duration rule now on `main` (`e8f2b5488b266ebc89ea7ef48360df7584088e82`); its original proposed PR #124 / `7d6bdf7702a2a241a33a21677fce29f26ada9b72` is merged. Source master and its existing `storyboard.json` unchanged.

## Exact six texts
| Variant | EN full | RU full | EN words | RU words | SHA-256 EN | SHA-256 RU |
|---|---|---|---:|---:|---|---|
| 02m | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 247 | 209 | `1fa1bff2d2c050ebc50de665a4b066d534ddf2549cf96de1f700c91c9adb1bd1` | `8f99db43a0ef875d2497603322ca6d99ca28d6db852f4e0ab0b53f948be9258e` |
| 05m | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 691 | 568 | `32ee00391140e46494a16fe41ef7fb9603ef84703b968d50a2cc5c9f8aa65189` | `6d501b0647f75eb2a87dfaacb588ea001d841711cc1a5d36bef48db79c929d0e` |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1631 | 1265 | `e201ca753a560847661590702e348da702d372784e6ec62c5176d88ff7c4c7b0` | `81f8f876c9db08218f9f61461e94c5e7909022ecaa50b42d2584827fbb2d6c0e` |

No TTS measured. At a hypothetical 145–175 English words/min before actual voice speed/pauses: 02m 247 words, 05m 691 (~3.9–4.8 min without pauses), 10m 1631 (~9.3–11.2 min without pauses). This does not establish actual duration, which needs approved TTS and montage; no voice speed change is authorized.

## What changed (old → new)
- Baseline `script.en.txt` blob `7413851f1368dd42ac76766f8a2013c2642e0866`, RU `37ca2d9a6f7ccdcbed7162928801bfba0abd0e4d`, 569 EN words: strong documented agency reversal, actual rescue and humanitarian emblem postscript; **preserved unchanged** with its original 44 aligned storyboard spans.
- Former opening revealed the rescue before questions and provided a 569-word single narration. Now every Long version begins with precise viewer questions before historical immersion and progressively reveals command spoof → credible aid disguise → prisoners and captors boarding → midair reversal → consequences.
- 02m is an independent closed rescue story, not just a trailer. 05m adds actual January humanitarian precedent and the guard's decisive choice. 10m adds distinct sourced mechanisms (three separated hostage groups, radio imitation and background sounds, individual captivity history, later conflicting footage and disputed claims) rather than repeating a summary. Ten-minute factual expansion has limits and must not be portrayed as reconstructed actual radio dialogue.
- Neither old master nor its existing storyboard/approval/timings are applied to the new texts. No independent reviewer, runtime or production created.

## Causal story maps & hard checks
**02m:** questions (why captors board/why no gunfight) → multi-year captivity motivates avoiding an armed raid → reported false command + cover → bound boarding with both guards → airborne reversal → 15 freed without shots → actual misuse of protected emblem acknowledged → final return to those boarding. Human line is prisoners, not hypothetical quotes. Possible weak point: little time with people before rescue.

**05m (revised 2026-11-19):** questions → fifteen captives, remote holding and raid risk → Betancourt's captivity and other prisoners → military-attributed false FARC instruction → January 2008 humanitarian handover precedent → disguises and government-described fictitious NGO website/phone → helicopter arrives with soldiers posing as aid staff → César and second commander escort the bound hostages → midair arrests → Betancourt and others' documented relief → acknowledged Red Cross emblem misuse and conditional harm to real aid workers → final reversal. Main weaknesses: government order detail cannot be independently authenticated from the cited radio bytes; ethical coda follows emotional climax.

**10m:** three questions → landing in the armed clearing → Betancourt's 2002 kidnapping / Americans in 2003 / three distinct captive groups → difficulty of location and armed extraction → military-claimed spoof of command → January precedent + described radio mimicry → costume/film cover and guarded landing → César and Enrique Gafas escort → airborne reversal → verified rescue → contrasting accounts of the Red Cross emblem, acknowledged misuse, disputed payment claim explicitly unresolved → why neutral aid depends on trust → agency inversion payoff. Potential slow zone: radio detail and extended postscript; cut without removing uncertainty if first-listener loses interest.

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
| 10m | Interest/significance | 8 | individual captivity and command mechanism add human scope | opening packed with three issues | medium |
| 10m | Opening | 8 | three concrete questions answered by final reversal and emblem issue | ethics may compete with escape promise | medium |
| 10m | Development | 8 | three dispersed groups + radio cover + handover precedent add real steps | explanatory midpoint delays takeoff | medium |
| 10m | Payoff | 8 | full escape and the later media discrepancy resolved only to verified limit | multiple codas may weaken ending | medium |
| 10m | Freshness | 8 | radio wildlife, boots, disputed video reporting, no false conclusion | technical detail not always cinematic | medium |
| 10m | Visuals | 8 | boots, field radio, helicopters, landing, cabin action | no licensed original footage and no art produced | medium |
| 10m | Spoken clarity | 7 | precise agency and attributed testimony | 1631 EN words; sustained oral rhythm needs independent first-listener | low |
| 10m | Verified viewer demand | UNVERIFIED | public indexed views are not comparable | Studio analytics and real viewing absent | low |

## Comparison of actually finished texts
| Upgrade | New verified value | Exact retention risk / where editor would inspect |
|---|---|---|
| 02 → 05 | Betancourt timeline, January 2008 legitimate humanitarian precedent, why César accepts the transfer, dramatic role reversal in flight | paragraph beginning “The aircraft also had to look credible”: distinguish a government-described fake website from evidence anyone checked it; keep emblem section short after full rescue |
| 05 → 10 | separate hostage groups, captivity personal detail, described radio mimicry, contested emblem-video timing, narrow treatment of payment allegation | “According to a 2022 Smithsonian account...” and subsequent intelligence explanation; then multiple post-rescue controversy paragraphs |

**Editorial recommendation: 05m, revised exact SHA-256 as above.** Enough causal proof for the human rescue and the serious ICRC consequence, without taking ten minutes before the final answer and without skipping the guard's reason for accepting the flight. 02m is a worthy tight alternative if independent listening finds the ethical chapter too long; 10m is conditional on fresh review and actual voice timing, not presumed better due to length. No version approved for production, no independent verdict.

## Claim evidence (one shared research)
See `research.md` original detailed contemporary sources and 2026 audience snapshot; added source ledger and uncertainty in its 2026-11-16 supplement. No original footage watched; no direct radio transcript, payment proof, or actual AV reference; demand and real reviewer UNVERIFIED. Review status by exact SHA-256 above; new hash invalidates review of previous variant only. Next unprocessed Long in historical review queue: PR #101 Tunnel 57, pending fresh status and no conflicting actor.


## 2026-11-19 substantive existing-PR revision
- **Before → after:** baseline PR #103 HEAD `2986761d12d25ff81f142c245f4f692ed4e71e46`; previous 05m EN/RU SHA-256 `716d0661fc28d2157e01af896753f25307f01abf9622d97ac00c312397825837` / `0ad582d211bb280b21e4f9a474aa5b40e6ba726c0129a333cbf812bb73b1283f`. The old 05m second paragraph disclosed the hidden military crew before the viewer understood the captive risk, and the rescue aftermath relied on summary. The revised 05m first shows the captives and danger, explains the apparent FARC order and why a humanitarian transfer seemed plausible, then resolves the voluntary boarding/airborne detention and Betancourt's reported human reaction. The cover now includes the specifically attributed fake NGO website/phone with no fabricated claim the guards inspected them. No other script version changed.
- **Full exact 05m files:** [EN](variants/05m/script.en.txt) (32ee00391140e46494a16fe41ef7fb9603ef84703b968d50a2cc5c9f8aa65189, 691 words); [RU](variants/05m/script.ru.txt) (6d501b0647f75eb2a87dfaacb588ea001d841711cc1a5d36bef48db79c929d0e, 568 words). Eleven meaning-aligned paragraphs in both languages. Other hashes in table unchanged; original source master and storyboard are protected.
- **Three versions compared:** 02m has complete reversal but omits the humanitarian precedent and team cover; revised 05m adds the decisions making that reversal credible and personal relief, with a brief ethical consequence. 10m adds separated groups/radio background and video controversy, but the extended explanation between initial danger and airborne rescue plus post-rescue debate risk losing attention. **Recommend 05m editorially**, not as a production approval.
- **Checks:** author-read full EN/RU text and source-ledger matches; documentary Long opens with questions before immersion and its central hook; all 11 EN/RU paragraphs matched for action, agency, numbers, certainty and ending. Estimated duration only. Independent first-listener, second bilingual reviewer, exact narrated timing, scene spans, visual/media rights, audience data and owner decision **UNVERIFIED**. This remains `EDITORIAL_CANDIDATE_UNREGISTERED`, not `awaiting_script_approval`.
- **Next untouched work:** PR #101 Tunnel 57 (verify live head/protection before editing); technical PR #77/#78 code and conflicts are still in scope.
