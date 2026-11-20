# Banco Río — exact triple, factual review correction (2026-11-19)

**EDITORIAL_CANDIDATE_UNREGISTERED; independent reviewer UNVERIFIED.** Important baseline finding: all six 02m/05m/10m texts **already existed** at `de7fdb05c8c82476e7219ed10b954358101f2811`. The owner-required three-duration package was not actually missing. Their older README/PR descriptions did not index or evaluate the six files under the new standard. Preserve all strong story structure: 05m is byte-for-byte unchanged; 02m and 10m retain their original composition, with a **targeted correction** to how a TV phone number led investigators toward other SIMs/handset IDs. Only that passage changes in each bilingual pair. See [research.md](research.md) for contemporary trial evidence.

## Exact full files / SHA-256 of current UTF-8 bytes

| Target | Full EN / SHA-256 | Full RU / SHA-256 | Words EN / RU | Editorial length estimate |
|---|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) `0fbd1ffbdb6e86b527fa8bbf416e175c66d12ea60aa0819212ba7b5aaf77b2c7` | [RU](variants/02m/script.ru.txt) `b2900bc5eb0550e0c600d390a9fa6f01a81a62882e855544279ff878ba89ccf3` | 314 / 272 | Long 16:9, ~2–3m at hypothetical 120–155 spoken English wpm; actual TTS not measured |
| 05m | [EN](variants/05m/script.en.txt) `05dbb45352765b163973e58c93f563afd9eed74aebb6b3797a6bb17f18d0494a` | [RU](variants/05m/script.ru.txt) `5c2401ef6e48ce2e68cd5e6240a4d4c6a2ea450ab7e6e0d378194f181211b2af` | 512 / 417 | Long 16:9, ~3–5m (5m may undershoot) at hypothetical 120–155 spoken English wpm; actual TTS not measured |
| 10m | [EN](variants/10m/script.en.txt) `658e73b85aa9179c2f3f9dc9e5ae4d139450b54389c5168b0243c280f010402f` | [RU](variants/10m/script.ru.txt) `0933fe535641fc8c7b6f659a3e0ab2221d8f1a0a4122cfd843819d3f292beb0f` | 1361 / 1082 | Long 16:9, ~8–11m at hypothetical 120–155 spoken English wpm; actual TTS not measured |

Baseline existing blobs at `de7fdb05c8c82476e7219ed10b954358101f2811`: 02 EN/RU `7064e63a43a88a5a5819cc56f08faa40a72441cd` / `7d5b99eaab27b277f02757125cf098a4d42dda2d`; 05 EN/RU `6e0e66c0404901a9acdce3551b7408851776f344` / `135c0a2de96d6fc8cf92e904dab2ac5ee665e2b9`; 10 EN/RU `947d7c77d459df1044ae2c2676172db0a66df7f6` / `5ceeb755472b340a006689163aa888bc7ac72933`. The original *root* master files are unchanged; 05m uses the same spoken paragraphs but the historical variant file has a distinct trailing newline. Consequently old root storyboard scenes are bound **only** to exact root bytes, not automatically to a different 05m hash.

## Three complete story maps

- **02m:** question of impossible cordon escape and TV call → 23 hostages → gray-suited negotiator while others open boxes → storm drain boats → live hostage release → a newsroom number leads to **handset/SIM cross-match**, with spouse lead distinct → convictions and disputed harmless-toy-gun claim → two-route payoff. New technical clause requires care in VO but avoids false direct trace.
- **05m (unchanged):** questions and 23 hostages → gray suit and visible negotiations → hidden passage and boats → Sileo's suspicious guard observation → hostages released alive → number and separately spouse's evidence → prosecutions and ethical consequences → mirrored tunnel/phone final. Source text strong for human tension; estimated length may be short.
- **10m (focused edit):** questions → hostage stakes → planning and earlier bank reconnaissance → basement/drain and engineered water level → negotiated standoff, birthday song and guard suspicion → 140+ boxes and escape vehicle → physical searches → **TV number, SIM registration and handset identifier** → spouse lead → distinct classes of investigative evidence → documented four convictions, gray-suit separate proceeding → hostage impact and uncertain haul. Keeps the original 10m's distinct physical evidence, verdict details and conflict; changes only the inaccurate implication that the TV SIM had directly produced calls during the heist.

## Eight editorial criteria, each exact version independently

| Criterion | 02m (evidence; limitation; confidence) | 05m (evidence; limitation; confidence) | 10m (evidence; limitation; confidence) |
|---|---|---|---|
| Interest/meaning | **8/10**: 23 people in hostage crisis; crime genre competitive; medium | **8/10**: choices faced by Sileo and captives; familiar event; medium | **8/10**: full rescue, police and legal consequences; scope narrower than universal; medium |
| Opening | **8/10**: two concrete questions immediately; phone clue named early; medium | **8/10**: watched doors vs unknown exit; hints route quickly; medium | **8/10**: questions, meaningful hostage immersion, underground major hook; three initial questions a load; medium |
| Development | **8/10**: bargain/escape → phone/SIM reversal; new detail compressed; medium | **8/10**: guard surprise, boats and separate tip; some staging lines; medium | **8/10**: planning, dam, getaway vehicle, material find, phone trace and trial; procedural middle long; medium |
| Payoff | **8/10**: escape and investigation both answered; handset may need a graphic; medium | **8/10**: complete dual route and real hostages; concise legal outcome; medium | **8/10**: both mysteries and consequences resolved, no invented weapon certainty; final legal tail less tense; medium |
| Fresh angle | **6/10**: TV callback, not merely the tunnel; repeatedly filmed event; high | **6/10**: same investigative reversal, commonly dramatized; high | **6/10**: identification mechanism adds precision, not exclusivity; high |
| Visual | **8/10**: overhead cordon vs storm drain + phone tree; storyboard not rendered; medium | **8/10**: paper cutaway and negotiation action; actual assets missing; medium | **8/10**: dam, vehicle access, trail and consequences; paper detail can overload; medium |
| Natural speech | **8/10**: direct sentences with one dense SIM passage; no listening; medium | **8/10**: concrete action, old 33 scenes, still some explanatory turns; no listening; medium | **7/10**: precise actions and sources but technical/justice exposition dense; no listening; medium |
| Verified viewer demand | **UNVERIFIED**: no matched baseline; low | **UNVERIFIED**: no own retention metrics; low | **UNVERIFIED**: historical analogue views cannot establish 10m appetite; low |

## Hard checks / best length / evidence status

**Author-only fact review:** important correction confirmed by 2010 trial reporting from https://www.infoban.com.ar/19/03/2010/descubren-un-error-en-la-ejecucion-del-robo-del-siglo/ : newsroom number used a SIM with false registration; handset identifier exposed different SIM lines. This must not be flattened to direct number trace. The other documented details retain their historical source boundaries in research. **Independent fact review UNVERIFIED.**

**EN/RU:** all 3 scripts are full, same event and matched sequence; edited 02m and 10m phone passages checked for the same SIM/handset mechanism and uncertainty, rest retained. Author PASS; independent bilingual review UNVERIFIED. **Format:** each Long 16:9 supported by Paper Detour's current ChannelSpec. **Loop N_A**; Shorts AV seam N_A. **Owner approval, runtime registration, pinned review, real TTS/MP4, comparator audience data:** UNVERIFIED. A CI software run is not those checks.

**02→05 adds** the guard suspicion, hostage-side tension and richer trial consequences. **05→10 adds** bank reconnaissance, physical escape engineering and divers' motor evidence, exact verdicts and evidence types; after the police begin collecting material traces, narrative speed drops while resolution remains postponed. **Recommend 05m** as most balanced, provided actual narration duration confirms it is sufficiently close to target. Two minutes may be the stronger deliverable when runtime is strict; 10m has independently supported details but risks losing audience after the escape. Recommendation is author-only, not approval.

**Storyboard binding:** S001–S033 references the exact original root EN/RU hashes. Those root files have not changed. The 02m and 10m changed hashes invalidate any hypothetical dependent review/scene spans. The existing 05m is the same spoken text but distinct file hash and requires exact binding before production. No media generated.

---

## Original historical author card (applies only to exact unchanged root/05m)

# audience-first-v1 — author editorial card

**Class: STRONG_CANDIDATE (author-only; experimental UNVERIFIED comparative demand).** This is not an independent review, official ytv-script-review-v1, script approval or production authorization. Scoring after complete EN/RU revisions, before scene prompts. Method: two author reads for hook, middle and actual payoff, speech edit for concrete causality, source-to-claim comparison and bilingual equivalence. No recorded audio or outside reader. Version: exact EN Git blob **2ab656c1a7f7e47ec13a0ce4a3283d293014a295**, exact RU Git blob **e80bdb7d48dc0d0db98c90803bbdb005f1f0a76b** (Git object hashes, NOT official ytv SHA256 receipt). Base main 5d3222c8888c775d2195c8b2949949f2d992e98d.

| Criterion | Author score 1–10 / UNVERIFIED | Confidence | Concrete evidence | Main limitation |
|---|---|---|---|---|
| (1) Audience value | 8 | medium | Hostages behind a cordon plus later evidence that reveals apparent escape; danger and investigation give a general audience a reason to care. | True-crime is crowded and viewer willingness to watch a paper reinterpretation is not measured. |
| (2) Honest beginning | 9 | medium | Opening immediately shows 23 hostages, watched doors and hidden alternate exit; no false claim of immediate capture. | It reveals the broad escape concept early; a fast viewer may expect a simple tunnel explainer. |
| (3) Development / reason to finish | 8 | medium | Turns from hostage bargaining to unseen drain, negotiator's recorded suspicion, the TV callback number, spouse's tip, then convictions. | Mechanical passage-to-boats section may slow; extra reversals are documented but narration stakes must remain clear. |
| (4) Payoff | 8 | medium | Final concrete contrast: concealed exit avoided the cordon while volunteered phone contact and a tip reopened identification; consequences for hostages are not erased. | Several factors, not one clever detective, drove arrests; a simpler single culprit would be a false neat ending. |
| (5) Fresh angle | 6 | high | Centers accidental public phone trail after a physical escape and hostages' exposure, rather than "perfect tunnel crime" alone. | Widely dramatized Banco Río event; repo has several crime/fraud candidates. |
| (6) Visual expressiveness | 8 | medium | Paired paper cutaway street/drain vs police at bank, mirrored phone link and recovered evidence tell the cause visually. | Easy to overdecorate paper diagrams or invent maps/real call details; source assets/pixels unverified. |
| (7) Natural EN/RU speech | 8 | medium | Concrete "Officers watched the doors" to "gave the newsroom a mobile number" causal language; EN/RU preserve 23 hostages, >140 boxes, ~$19m and ambiguity of spouse motive. | Some explanatory lines sound like script exposition; no real spoken listener test. |
| (8) Measured/comparable viewer interest | UNVERIFIED | low | Public 2014–2026 YouTube analogs of varying strength, and weaker anniversary-news example; no trustworthy same-author comparable age/format baseline. | No matched baseline, own search terms/retention or independent video viewing; not proof of present demand. |

Critical floor: #1=8, #3=8, #4=8; scores **do not** represent probability of success, views, CTR or retention. No 10 awarded; low comparative evidence is not hidden by averaging. Main choice vs strong alternative is in research.md. Version B of #20 and #25 was read directly at requested exact commits for concrete natural language only; no text copied.

## Hard checks separately

- Factology: **author PASS with named uncertainties**, not independent fact-check. All essential figures/actions from the cited source table; 140+ boxes avoids disputed count, ~$19m is explicitly contemporary estimate, no claims of verified personal motives or universal replica guns.
- Duplicate/owner refusal: **author PASS** against current 107 PR titles and named rejections at prewrite; final remote check still needed.
- Channel/format: **PASS**, Paper Detour active English illustrated recipe and Long 16:9 profile.
- EN↔RU equivalence: **author PASS** for same 33 sequential propositions, actions, limits and result; independent translator assessment **UNVERIFIED**.
- Rights/assets: **UNVERIFIED**. Only text and proposed paper art; no actual media/reference bytes, rights receipts or manufacturing permissions.
- Required narrative Short loop: **N_A (Long)**. No AV seam claim; all 33 spans are exact authoring spans, not measured timing.
- Fresh **independent reviewer**: **UNVERIFIED / unavailable**: sessions.independent reviewer & pinned local host absent in current execution environment. Author changing role would not count. No ytv-script-review-v1 fabricated; no official gate completed.
- Actual spoken listening: **UNVERIFIED**. No TTS or media produced. Review must be redone for changed EN Git blob/hash.

Two meaningful author passes applied (content write and one rhythm/fact-boundary check); do not iterate scores merely to pass floor. Exact master unchanged since recorded blobs.
