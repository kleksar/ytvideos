# Editorial review — USS Squalus rescue (author-only)

**Status: `EDITORIAL_CANDIDATE_UNREGISTERED`.** 2026-11-23. The numbers below are an author's editorial judgments, **not predictions of clicks/retention or independent-review scores**. No external independent text reviewer, audio or video was used. Each row refers to the exact EN/RU content blobs identified by the following SHA-256 hashes.

## Exact six scripts and estimated durations

| Target · format | EN full script SHA-256 | RU full script SHA-256 | EN words; estimated delivery | Author class |
|---|---|---|---|---|
| **02m · Short** | `010d4e8ae5c8d5d488bc669cc7821912ece50711541abf9a58b6e414f6dd7f30` | `6ba9cec015281808406fff53f4c8bc50bdde77e56fa4455064e759ffe975f283` | 273 EN words; 1:49–2:06 at 130–150 wpm, before ~5–12s natural pauses; measured TTS **UNVERIFIED** | STRONG_CANDIDATE (conditional, loop independent UNVERIFIED) |
| **05m · Long** | `8da96f2f246b9795e09fe336c2cd6dbf797b787c2643366acc0dedd36556eefe` | `1039347ec8908a783737f31ed5709bf4ea0875b82ba9d18d466e0ba76b7b0a89` | 690 EN words; 4:36–5:18 at 130–150 wpm + 10–20s assumed pauses and channel's 10s end-screen; exact **UNVERIFIED** | **STRONG_CANDIDATE — RECOMMENDED** |
| **10m · Long** | `b7edcf56283406707bab782f4fa19bd6a663988ffac025d2b118bd67ffb11d7d` | `e837136df6902e5df1309b6d565056c3f6481f13264156e92ea5915ac6380e9a` | 1485 EN words; 9:54–11:25 at 130–150 wpm + ~10–30s pauses and 10s end-screen; exact **UNVERIFIED** | REWORK_PACING |

Target durations are planning labels, NOT validated durations, and the Nuviko voice speed must stay at its ChannelSpec value (1.10× once). No host TTS, no retimed audio. Format compatibility: both illustrated Short and Long supported by `channels/nuviko_history/channel.json`.

## Eight criteria scored separately by exact version

Scale 1–10; author = this story-writing assistant; confidence high for visible text structure, medium for viewer response, low for the unknown market. **Viewer-demand score is UNVERIFIED**; do not map unknown demand to zero or eight.

| Criterion | 02m Short: score + exact grounding | 05m Long: score + exact grounding | 10m Long: score + exact grounding |
|---|---|---|---|
| 1. Interest / significance | **9** — eight people in a chamber whose rescue line jams; 26 real deaths prevent a false total-survival ending; confidence medium | **9** — an apparent successful rescue turns into its own second emergency, “rescue the rescue chamber”; medium | **8** — same event plus technological aftermath; substantial but less immediate first-act action; medium |
| 2. Opening / hook | **9** — “Then its cable jammed” after a chamber with eight aboard; cold scene already understandable; high | **8** — two promised questions before 1939 test dive, both answered; measured first minute UNVERIFIED; high | **8** — three different questions, clear payoffs but longer runway to central jam; high |
| 3. Development / reason to remain | **8** — 25 rescued → final eight board → 1st jam → 2nd cable fails → buoyancy adjustment; high | **9** — search, dry passage, three successes, fourth failure, diver cut, remaining wire, delicate buoyancy adjustment; high | **8** — 1927 design rationale and salvage develop understanding; some procedural middle risks slowing narrative; medium |
| 4. Payoff | **9** — “Now the cable only had to guide it” followed by full 33 saved and 26 deaths acknowledged; high | **9** — 00:23 surface, final eight and fifth check; final sentence clearly resolves method; high | **8** — the final line links design to improvisation and preserves fatal losses; aftermath is useful but not as powerful as chamber rescue; high |
| 5. Freshness of angle | **8** — attention on failure of rescue device rather than the initial wreck; competing 2022 Dark Seas long documentary exists; medium | **8** — reset of climax at last chamber ascent; possible overlap with 2026 new written reconstructions; medium | **7** — more conventional full history/salvage arc; medium |
| 6. Visual storytelling | **8** — tight chamber, split hull, lines, ballast, ship; relevant 2D host / photoreal world possible without invented archive; medium | **9** — distinct physical states (seal, three returns, fouling, manual buoyancy), suitable for illustration with sources; medium | **8** — more cutaways/slow mechanical explanations and 1927 setup; actual references/images UNVERIFIED; medium |
| 7. Natural speech / clarity | **8** — full sentences and concrete verbs; jargon “retrieving cable” explained by role; author-only; medium | **8** — actions move forward, admits 26 dead; end explanation a little technical; author-only; medium | **8** — connected narration, extra nautical terms; spoken TTS check not done; medium |
| 8. Viewer interest evidence | **UNVERIFIED** — no comparable Nuviko sample; 325k Dark Seas public views do not imply Shorts outcome | **UNVERIFIED** — 2022 Dark Seas competes but its author baseline/CTR unavailable; no verified format comparison | **UNVERIFIED** — no normal long-video baseline, 30–90d growth, analytics or comments; confidence low |

**Rule threshold:** For 02m and 05m author's interest, development and payoff are each >=8 **with the exact evidence above**. The 10m also carries >=8 on those three but gets **REWORK_PACING**, not automatic strength, because additional mechanistic paragraphs after the core payoff risk attention loss and its duration is more variable.

## Concrete story maps (one history, different writing)

| Edition | Opening → setup | Change after hook → decisive action | Full end; weakest line/section |
|---|---|---|---|
| 02m | “A rescue chamber began climbing ... Then its cable jammed.” → Squalus sinks, 26 lost, 33 trapped, chamber seals | 25 saved; last eight board; jam, diver cuts, retrieval cable nearly fails → ballast changed in small steps | All 33 surviving people return, 26 mourned; worst risk: dense 2-line explanation of two cables, plus unverified spoken loop |
| 05m | “How do you lift people ... ? And what happens ...?” → valve and separate sections, Sculpin locates hull | seal and dry transfer; 7+9+9, then jam and near-snap → measured buoyancy and manual guidance | 00:23/00:25 rescue, later fifth flooded-compartment check, Sailfish coda; worst risk: one passage explaining chamber mechanics |
| 10m | “How could ... ? How ... ? And why ... ?” → flood, 1927 S-4 origin, search, detailed docking | successive successful trips → fourth fault, wire almost parted → delicate balance rather than winch force | all 33, fifth no extra survivors, 1939 salvage / 1940 return, fatal loss retained; weakest section: early background through repeated docking steps |

**Short text loop evidence, author-only** (NOT independent PASS):
- Opening EN: “A rescue chamber began climbing from a sunken submarine with eight survivors inside. Then its cable jammed.”
- Ending EN: “The last eight had boarded the chamber believing the hard part was over. That was exactly when their second emergency began.”
- Opening RU: “Спасательная камера поднималась с затонувшей подлодки. Внутри были восемь человек. И вдруг трос заклинило.”
- Ending RU: “Последние восемь вошли в камеру, когда казалось, что самое трудное позади. Именно после этого началась вторая авария.”
- **Link (not only repeated noun):** last line fixes the chronological point after boarding; first line enacts that just-described beginning of their second emergency. Cold open names what/where/how many without any preceding context; payoff of rescuing all 33 already occurs before final return. Whether repeated aloud **twice** has natural prosody and whether AV seam preserves chronology: **UNVERIFIED**; independent reader must challenge possible circular restatement.

## Comparative decision

**2 → 5 minutes gains:** who was separated by the watertight doors; how wreck found, why the chamber must seal dry; the exact pattern of increasingly familiar trips; and a clear post-rescue fifth check. These details build why the final jam mattered and how the solution works.

**5 → 10 minutes gains:** 1927 submarine S-4 as a preparation reason, a more physical explanation of docking/pressure, differences between temporary passenger transfers and wreck salvage, Sailfish second life. It answers more questions, but after the core fourth-ascent climax the long version risks losing viewers in recovery context. The long text is complete, **not** an unfinished outline, but has editorial pacing debt.

**Recommendation:** 05m Long. It has the strongest proportional causal development and concrete final payoff; not because five minutes always wins. 02m works as a shorter independent arc. 10m can be reconsidered after independent listener's line-specific feedback, without padding or inventing incidents. No master has been selected/approved by the owner.

## Separate compliance and QA statuses

| Gate / dimension | 02m | 05m | 10m | Basis |
|---|---|---|---|---|
| Historical core facts | PASS **provisional** | PASS **provisional** | PASS **provisional** | NHHC historical pages/indexed primary report and corroboration; official full direct read timed out, passenger-trip ambiguity recorded in research |
| Channel format | PASS specified Short | PASS specified Long | PASS specified Long | Actual Nuviko ChannelSpec available; no production operation run |
| EN/RU semantic equivalence | Author PASS; independent UNVERIFIED | Author PASS; independent UNVERIFIED | Author PASS; independent UNVERIFIED | Same names/counts/actions/caveats/end in both full texts |
| Narration originality / archive rights | Original text PASS; images UNVERIFIED | Original text PASS; images UNVERIFIED | Original text PASS; images UNVERIFIED | No third-party script copy; real 1939 source image reuse needs rights audit |
| Narrative Short loop | author-provisional; independent/AV UNVERIFIED | N_A (Long) | N_A (Long) | Literal opening/closing above; no two-cycle fresh-reader or MP4 |
| Independent first listener | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No isolated `sessions.independent` tool reached; self-evaluation is NOT review |
| Measured voice duration / 10s native endscreen | UNVERIFIED / N_A | UNVERIFIED / UNVERIFIED | UNVERIFIED / UNVERIFIED | No TTS/AV; timing from word counts only |
| Official runtime / user approval | UNREGISTERED / NO | UNREGISTERED / NO | UNREGISTERED / NO | `ytv` executable missing; no run/lease/receipt/approval |

**Revision attempts:** one complete composition for each text + one manual author review; no independent review, no fake reviewer ID. Do not claim scored 9–10 as a probability. If major objections are found, no more than two meaningful author rewrites; new bytes invalidate this review/scene spans and require a fresh independent review. See [research](research.md) for primary/YouTube evidence and contradiction about per-trip passengers.
