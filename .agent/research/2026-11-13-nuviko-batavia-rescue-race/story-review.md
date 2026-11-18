
# Batavia 1629 — three independent editorial versions

Status: **EDITORIAL_CANDIDATE_UNREGISTERED**. Owner has **not** approved any new exact script. No production, TTS, MP4, measured audience data, or independent reviewer receipt.

Baseline original PR #29 HEAD: `964d88b6836aca9bff583fb98181bd18e959f384`. Original root manuscripts (unchanged): EN Git blob `44f3b9dfd804055dc099aed5f8def3ad8ccef395`; RU Git blob `f7b43c376ea011c84fc4175394e99f8ecc7c2b52`. The 10m variant preserves those texts exactly rather than fabricating new incidents to fill a nominal duration.

## Exact text files and audit
| Candidate | EN / SHA-256 | RU / SHA-256 | Estimated speech / format | Status |
|---|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) / `5c66273835b971bea2eab1730783a8ec3d641a9da6e0b8bb27835947d3002c6b` | [RU](variants/02m/script.ru.txt) / `a3b28614dc61db697307f820e5b0b1b92683c07c0d6d09aac672e52f901bae11` | 274 EN words; ~1.6–2.2 minutes assuming 120–155 wpm and pauses; Nuviko Long 16:9 | AUTHOR-REVIEWED / INDEPENDENT UNVERIFIED |
| 05m | [EN](variants/05m/script.en.txt) / `7b99a657152f023951a8eb983904355ccf7cb67d6cea41c0fcd68c4e60e6ca8b` | [RU](variants/05m/script.ru.txt) / `b1eddf49ccbbd04d4b9e5128f6bbb01e4b3ee068f43c24121354d44af064d8c8` | 649 EN words; ~4.8–5.9 minutes assuming 120–155 wpm and pauses; Nuviko Long 16:9 | AUTHOR-REVIEWED / INDEPENDENT UNVERIFIED |

| 10m | [EN](variants/10m/script.en.txt) / original Git blob `44f3b9dfd804055dc099aed5f8def3ad8ccef395` | [RU](variants/10m/script.ru.txt) / original Git blob `f7b43c376ea011c84fc4175394e99f8ecc7c2b52` | 1195 EN words, ~8–10+ minutes depending on real voice/pauses; Nuviko Long 16:9 | SOURCE PRESERVED / INDEPENDENT UNVERIFIED |

**SHA-256 of the unchanged 10m files:** must be independently computed from remote read-back before accepting hashes; the Git blob identifiers above are **SHA-1 Git object IDs, not SHA-256**. Do not substitute them for hashes or claim six verified SHA-256 until they are computed.

## Story maps / promises
- **02m:** questions about murder and competing boats → 1629 reef/water crisis → commander leaves → Cornelisz captures boats and disarms 22 → Hayes finds water → warning/defences → capture of leader but renewed attack → Sardam appears → rowboat race → Hayes warns first → arrests/punishment. The full outcome is included; standalone two-minute *Long*, not a Shorts loop.
- **05m:** three questions → exact shipwreck context, silver and pre-existing plot → water search / 33 days to Java → Cornelisz captures council/boats → disarmed Hayes group finds water and food → murders and escapee warning → coral wall / two failed attacks → Cornelisz captured but Loos attacks with muskets → arrival of Sardam → incompatible claims / boat race → Hayes first, arrests, aftermath and surviving stone structures.
- **10m:** questions → opposing boats early (winner withheld) → historical departure/navigation → wreck and islands → departure → council/mutiny → disarmed soldiers → murders → defensive construction and repeated battles → Cornelisz taken but another attack → Sardam and boats → Hayes reaches Pelsaert first → punishments and archaeological discoveries. Preserves original 83-block coverage.

## Individual eight-criterion author scores (1–10; not measured demand)
| Criterion from editorial standard | 02m | 05m | 10m |
|---|---|---|---|
| Interest / significance | **8**: rescue becomes a moral conflict, but little context | **8**: escalating survival and trust stakes | **8**: wider collapse of order, high stakes; violent content limits breadth |
| Opening / promise | **8**: two questions quickly establish stakes | **8**: three specific questions, answered | **8**: strong questions and conflicting boats; introductory chronology later slows |
| Development / reason to continue | **7**: several necessary turns compressed | **9**: discovery of water and capture of Cornelisz reverse expectation twice | **8**: detailed but 83 micro-beats can dilute focus |
| Payoff | **8**: warning arrives first; punishments and unknown exile fate | **9**: boat race resolves control of rescue; material consequences remain | **8**: complete rescue, but aftermath repeats the outcome |
| Freshness of angle | **8**: murderer/defender race, not only the wreck | **8**: competing stories rather than generic shipwreck | **8**: same uncommon historical angle |
| Visual potential | **8**: reef, stone defence, two boats | **9**: clearly changing island geography and competing boats | **9**: original 83 shot concepts, many need verified references |
| Natural spoken clarity | **8**: few names and direct verbs | **8**: roles repeated, no invented dialogue | **7**: five named figures and numerous short transitions |
| Verified viewer demand | **UNVERIFIED**: no comparable viewer measurements | **UNVERIFIED**: no comparable viewer measurements | **UNVERIFIED**: no comparable viewer measurements |

Scores above are **editor's subjective judgements with medium confidence**, not an independent viewer, predicted CTR, retention, or real popularity. Demand is unscored, so no overall 9–10 average is claimed. Most important weakness 02m: Loos enters quickly; 05m: Pelsaert’s journey briefly diverts from Hayes; 10m: names/navigation before island danger and report-like tail after rescue. Specific drop points to test: 02m after the Cornelisz capture; 05m at pre-wreck conspiracy exposition; 10m after the trial account.

## Hard checks, separate from scoring
- **Fact basis:** AUTHOR-CHECKED against common [research](research.md) for the original and adapted versions; independent fact check UNVERIFIED. No exact inconsistent original headcounts; >100 murders; 22 disarmed soldiers; 33-day Java passage; Cornelisz capture preceded Loos assault. Source cross-checks on the 2026-11-18 read are in research.
- **EN/RU semantic equivalence:** AUTHOR-CHECKED for matching events, count, agency, outcome and uncertainty; independent bilingual review UNVERIFIED.
- **Format:** Nuviko History current checked channel.json supports Long 16:9; runtime pin may differ, so production support requires pinned check. 02m also **Long**, not Short. Narrative loop: **N_A** for all three; separate 10-second end screen unproduced.
- **Time:** estimated solely by EN words and an illustrative 120–155 wpm speech rate plus potential pauses, not the pinned actual voice; measured TTS UNVERIFIED.
- **Independent first-listener:** UNVERIFIED (no independent session or authentic reviewer result in GitHub).
- **Storyboard:** original 83 paragraph visual intents and original timing apply **only** to unchanged root scripts / 10m variant Git blobs. 02m and 05m need new scene spans and original visual coverage. No MP4/AV review.

## Compare added value and recommendation
**02 → 05:** explanation of navigation, authority seizure, failed attacks, contested testimony; transitions between Hayes and Pelsaert are clearer. 02m has the quickest escalation but compresses the fight and final judgement.

**05 → 10:** depth of navigation and island movement, more gradual discovery, later archaeology, but the chronology before the wreck and descriptions after the arrests reduce momentum. The original 10m text is protected as a candidate, **not deleted or rejected**.

**Editorial recommendation: 05m Long**, subject to an independent cold listener and owner's exact-version choice. It maintains the two-boat climax without extending the aftermath and avoids compressing the second mutiny attack. Neither recommendation nor PR checks approve production.

## Next gates
- Truly independent first-listener and bilingual fact review of exact six files; reviewer receives texts before this assessment and sources only after their first reading. No reviewer receipt fabricated.
- Owner selects one exact master, then local `uv run ytv start --channel nuviko_history --format long` with canonical `read_next` / pins / receipts and the selected UTF-8 source; no artificial runtime states or approvals.
- New storyboard / visual directions for selected 02m or 05m; original 83-beat shot plan never automatically covers changed scripts. References, TTS, SRT, MP4 and YouTube testing remain NOT_STARTED.
