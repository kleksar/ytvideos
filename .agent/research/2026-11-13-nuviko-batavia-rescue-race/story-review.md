
# Batavia 1629 — three independent editorial versions

Status: **EDITORIAL_CANDIDATE_UNREGISTERED**. Owner has **not** approved any new exact script. No production, TTS, MP4, measured audience data, or independent reviewer receipt.

Baseline original PR #29 HEAD: `964d88b6836aca9bff583fb98181bd18e959f384`. Original root manuscripts (unchanged): EN Git blob `44f3b9dfd804055dc099aed5f8def3ad8ccef395`; RU Git blob `f7b43c376ea011c84fc4175394e99f8ecc7c2b52`. The original root scripts remain byte-identical. The 10m *alternative* was substantively revised on 2026-11-20, with independently sourced additional events; it is no longer identical to the original or covered by its 83-beat storyboard.

## Exact text files and audit
| Candidate | EN / SHA-256 | RU / SHA-256 | Estimated speech / format | Status |
|---|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) / `5c66273835b971bea2eab1730783a8ec3d641a9da6e0b8bb27835947d3002c6b` | [RU](variants/02m/script.ru.txt) / `a3b28614dc61db697307f820e5b0b1b92683c07c0d6d09aac672e52f901bae11` | 274 EN words; ~1.8–2.3 minutes assuming 120–155 wpm and pauses; Nuviko Long 16:9 | AUTHOR-REVIEWED / INDEPENDENT UNVERIFIED |
| 05m | [EN](variants/05m/script.en.txt) / `7b99a657152f023951a8eb983904355ccf7cb67d6cea41c0fcd68c4e60e6ca8b` | [RU](variants/05m/script.ru.txt) / `b1eddf49ccbbd04d4b9e5128f6bbb01e4b3ee068f43c24121354d44af064d8c8` | 649 EN words; ~4.2–5.4 minutes assuming 120–155 wpm and pauses; Nuviko Long 16:9 | AUTHOR-REVIEWED / INDEPENDENT UNVERIFIED |

| 10m | [EN](variants/10m/script.en.txt) / `f7d293307fd5b693714b8731b5cc7748dd335540e470a57cfc85426b0461a67f` | [RU](variants/10m/script.ru.txt) / `60abe33c497c82b2bc21af321a15d72cd026684f5e3d640acd53ed28ade7245e` | 1300 EN words; ~8.4–10.8 minutes before unmeasured pauses, 120–155 wpm; Nuviko Long 16:9 | SUBSTANTIVELY REVISED 2026-11-20 / AUTHOR-CHECKED; INDEPENDENT UNVERIFIED |

**SHA-256:** 02m and 05m hashes are unchanged from remote read-back at `8ebec158e452198b29d24e3e6f150d086f3712e8`; 10m SHA-256 values above are computed for the new 2026-11-20 UTF-8 texts and must match post-push read-back. Git blobs have distinct SHA-1 IDs.

## Story maps / promises
- **02m:** questions about murder and competing boats → 1629 reef/water crisis → commander leaves → Cornelisz captures boats and disarms 22 → Hayes finds water → warning/defences → capture of leader but renewed attack → Sardam appears → rowboat race → Hayes warns first → arrests/punishment. The full outcome is included; standalone two-minute *Long*, not a Shorts loop.
- **05m:** three questions → exact shipwreck context, silver and pre-existing plot → water search / 33 days to Java → Cornelisz captures council/boats → disarmed Hayes group finds water and food → murders and escapee warning → coral wall / two failed attacks → Cornelisz captured but Loos attacks with muskets → arrival of Sardam → incompatible claims / boat race → Hayes first, arrests, aftermath and surviving stone structures.
- **10m (new):** questions about murder/disarmed defenders/boat race → silver voyage and disputed shipboard attack → navigational warning dismissed → wreck, water search and Pelsaert's departure → Cornelisz first rations supplies, then captures council and boat access → disarmed soldiers find water and wallabies → separate-island killings and rafts carrying warning → two failed attacks and Cornelisz's capture → Loos uses two previously reserved muskets and kills three → Sardam returns and rival boats approach → Hayes warns first → island court, marooning, silver salvage and physical evidence. Original root 83-block storyboard is **NOT** bound to this new 10m text.

## Individual eight-criterion author scores (1–10; not measured demand)

| Criterion from editorial standard | 02m (unchanged) | 05m (unchanged) | 10m (2026-11-20 revised) |
|---|---|---|---|
| Interest / significance | 8: rescue becomes moral conflict, limited context | 8: escalating survival and trust stakes | 8: on-board provocation, island abuse, and rescue politics enlarge stakes; grim subject limits reach |
| Opening / promise | 8: two questions answered | 8: three specific questions answered | 8: three concrete questions; historical shipboard dispute now develops before the main island hook, but the named officers still demand attention |
| Development / reason to continue | 7: key turns compressed | 9: unexpected water and leader capture reverse expectations | 8: dismissed reef warning, council takeover, wallabies, fugitives and reserved muskets cause successive changes; slower first act |
| Payoff | 8: Hayes warns first, punishments | 9: rowboat race closes two linked dangers | 8: first warning pays off the race; court, marooning and salvage give verified consequences, but post-race energy drops |
| Freshness of angle | 8: race between defenders/killers | 8: incompatible survival accounts | 8: adds how command dispute, control of transport and delayed justice produced a second catastrophe |
| Visual potential | 8: reef, coral defences, boats | 9: changing islands and boats | 9: identifiable reef warning, island boat geography, wallaby food, two muskets and salvage; all reconstructions need truthful treatment |
| Natural spoken clarity | 8: few names | 8: direct role-led transitions | 8: less generic repetition and closer cause/effect; unfamiliar names / three-stage navigation remain a listening risk |
| Verified viewer demand | UNVERIFIED: no observed comparable viewer metrics | UNVERIFIED: no observed comparable viewer metrics | UNVERIFIED: no real retention, comparable audience or independent listener |

All numeric scores are the editor's judgments with **medium confidence** about exact texts, not independent review or CTR/retention estimates. Important weaknesses: 02m rushes Loos's second attack; 05m briefly diverts to Pelsaert's crossing; 10m could lose listeners after the shipboard attack before the wreck, or at the transition from arrest to island trials. No automatic 9–10 or aggregate score.

## Hard checks, separate from scoring
- **Fact basis:** AUTHOR-CHECKED against common [research](research.md) for the original and adapted versions; independent fact check UNVERIFIED. No exact inconsistent original headcounts; >100 murders; 22 disarmed soldiers; 33-day Java passage; Cornelisz capture preceded Loos assault. The former 10m phrase 'two young mutineers' was corrected in the alternative to **Loos and cabin boy Pelgrom** on 2026-11-20. A new independent check of this exact revised script is still UNVERIFIED; the root original is intentionally unchanged. Source cross-checks on the 2026-11-18 read are in research.
- **EN/RU semantic equivalence:** AUTHOR-CHECKED for matching events, count, agency, outcome and uncertainty; independent bilingual review UNVERIFIED.
- **Format:** Nuviko History current checked channel.json supports Long 16:9; runtime pin may differ, so production support requires pinned check. 02m also **Long**, not Short. Narrative loop: **N_A** for all three; separate 10-second end screen unproduced.
- **Time:** estimated solely by EN words and an illustrative 120–155 wpm speech rate before unmeasured pauses, not the pinned actual voice; measured TTS UNVERIFIED.
- **Independent first-listener:** UNVERIFIED (no independent session or authentic reviewer result in GitHub).
- **Storyboard:** original 83 paragraph visual intents and original timings apply **only** to unchanged root scripts. All three alternative durations (including revised 10m) need explicit exact-hash storyboard coverage; none inherit the root spans. No MP4/AV review.

## Compare added value and recommendation
**02 → 05:** explanation of navigation, authority seizure, failed attacks, contested testimony; transitions between Hayes and Pelsaert are clearer. 02m has the quickest escalation but compresses the fight and final judgement.

**05 → 10:** the 2026-11-20 revision earns additional length with a failed attempt to provoke crew punishment, the dismissed reef warning, Cornelisz's gradual control of rationing/boats, wallaby food, rafts with witnesses, two muskets saved for the rescue ship, island court and concurrent silver salvage. The likely point of declining interest remains the post-arrest court/salvage transition. The original 1195-word Long survives untouched as root source; this is a separate 10m alternative, **not** an approved replacement.

**Editorial recommendation: 05m Long**, subject to an independent cold listener and owner's exact-version choice. It maintains the two-boat climax without extending the aftermath and avoids compressing the second mutiny attack. Neither recommendation nor PR checks approve production.

## Next gates
- Truly independent first-listener and bilingual fact review of exact six files; reviewer receives texts before this assessment and sources only after their first reading. No reviewer receipt fabricated.
- Owner selects one exact master, then local `uv run ytv start --channel nuviko_history --format long` with canonical `read_next` / pins / receipts and the selected UTF-8 source; no artificial runtime states or approvals.
- New storyboard / visual directions for selected 02m or 05m; original 83-beat shot plan covers only root bytes, and never automatically covers **any** of the three alternatives. References, TTS, SRT, MP4 and YouTube testing remain NOT_STARTED.

## Progress — 2026-11-20

Before: revised multi-length package existed, but 10m was a byte-copy of a 1195-word script with an immediate two-boat cinematic reveal, report-like aftermath and an identified age error in the marooning claim. Baseline PR head `8d0208fea5458ff18a19270fc6ec9ea234e538a1`, variant blobs EN `44f3b9dfd804055dc099aed5f8def3ad8ccef395`, RU `f7b43c376ea011c84fc4175394e99f8ecc7c2b52`. Root source and root storyboard remain untouched.

After: 02m and 05m remain byte-identical, 10m gets a new complete EN/RU factual narrative (1300 EN words; SHA-256 EN `f7d293307fd5b693714b8731b5cc7748dd335540e470a57cfc85426b0461a67f`, RU `60abe33c497c82b2bc21af321a15d72cd026684f5e3d640acd53ed28ade7245e`). One history, three complete texts with full matching RU; **10m AUTHOR-CHECKED**, independent review **UNVERIFIED**. Editorial preference still **05m**, not owner approval. Detailed new fact ledger is in research.md.

Hard checks: source provenance AUTHOR-CHECKED; EN/RU events, roles and material uncertainty AUTHOR-CHECKED paragraph-to-paragraph; real audio, timings, viewer demand, reviewer, runtime pins, canonical ytv run, acceptance and AV all UNVERIFIED. Long loop N_A. Next: independent blind reader (all exact texts without this scoring first), factual/bilingual review, selection by owner and fresh storyboard for exact chosen hash; do not reuse the 83 root scene spans.
