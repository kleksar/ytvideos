# Editorial review — USS Squalus rescue (author-only)

**Status: `EDITORIAL_CANDIDATE_UNREGISTERED`.** 2026-11-23. The numbers below are an author's editorial judgments, **not predictions of clicks/retention or independent-review scores**. No external independent text reviewer, audio or video was used. Each row refers to the exact EN/RU content blobs identified by the following SHA-256 hashes.

## Exact six scripts and estimated durations

| Target · format | EN full script SHA-256 | RU full script SHA-256 | EN words; estimated delivery | Author class |
|---|---|---|---|---|
| **02m · Short** | `8713b07fede498ee96dae2c76d026d09aa7477a1b8c1070e15cf9903d0e0cff5` | `c389d9ea8f195eb8ca36e6bea50f49fc1cec600174d008ed7b27f3fff0e3129a` | 269 EN words; 1:48–2:04 at 130–150 wpm, before ~5–12s natural pauses; measured TTS **UNVERIFIED** | STRONG_CANDIDATE (conditional, loop independent UNVERIFIED) |
| **05m · Long** | `8da96f2f246b9795e09fe336c2cd6dbf797b787c2643366acc0dedd36556eefe` | `1039347ec8908a783737f31ed5709bf4ea0875b82ba9d18d466e0ba76b7b0a89` | 690 EN words; 4:36–5:18 at 130–150 wpm + 10–20s assumed pauses and channel's 10s end-screen; exact **UNVERIFIED** | **STRONG_CANDIDATE — RECOMMENDED** |
| **10m · Long** | `e9a37f4173fd8833f5d75561fd0912499c2236f15ed10e3bc042e738478f89a2` | `ae774c7413eae993a7e7a87486f263d3d846a020173658c3de4516ab2a9b1fcc` | 1303 EN words; 8:41–10:02 at 130–150 wpm + ~10–30s assumed pauses and 10s end-screen; **REWORK_UNDERLENGTH risk at faster pace**, exact TTS **UNVERIFIED** | REWORK_PACING |

Target durations are planning labels, NOT validated durations, and the Nuviko voice speed must stay at its ChannelSpec value (1.10× once). No host TTS, no retimed audio. Format compatibility: both illustrated Short and Long supported by `channels/nuviko_history/channel.json`.

## Eight criteria scored separately by exact version

Scale 1–10; author = this story-writing assistant; confidence high for visible text structure, medium for viewer response, low for the unknown market. **Viewer-demand score is UNVERIFIED**; do not map unknown demand to zero or eight.

| Criterion | 02m Short: score + exact grounding | 05m Long: score + exact grounding | 10m Long: score + exact grounding |
|---|---|---|---|
| 1. Interest / significance | **9** — eight people in a chamber whose rescue line jams; 26 real deaths prevent a false total-survival ending; confidence medium | **9** — an apparent successful rescue turns into its own second emergency, “rescue the rescue chamber”; medium | **8** — actual communications and anchor failures lead to a fourth-trip cable emergency; final rescue has human consequence, but prelude is slower than Short; medium |
| 2. Opening / hook | **9** — “Then its cable jammed” after a chamber with eight aboard; cold scene already understandable; high | **8** — two promised questions before 1939 test dive, both answered; measured first minute UNVERIFIED; high | **8** — two concrete questions, “reach thirty-three people” and “machine ... becomes trapped”; both answered after actual rescue operations; high |
| 3. Development / reason to remain | **8** — 25 rescued → final eight board → 1st jam → 2nd cable fails → buoyancy adjustment; high | **9** — search, dry passage, three successes, fourth failure, diver cut, remaining wire, delicate buoyancy adjustment; high | **9** — smoke/phone line breaks → Falcon repositioning → hatch cable obstruction → 7/9/9 → brake fails → diver cuts first line → retrieving wire unravels → two divers cannot replace it → measured buoyancy; medium, too many details may still tire a viewer |
| 4. Payoff | **9** — “Now the cable only had to guide it” followed by full 33 saved and 26 deaths acknowledged; high | **9** — 00:23 surface, final eight and fifth check; final sentence clearly resolves method; high | **8** — 00:23/00:25 recovery followed by fifth no-survivor check; final hull-versus-people contrast returns to the last eight without restating technical moral; high |
| 5. Freshness of angle | **8** — attention on failure of rescue device rather than the initial wreck; competing 2022 Dark Seas long documentary exists; medium | **8** — reset of climax at last chamber ascent; possible overlap with 2026 new written reconstructions; medium | **8** — specific failed attempts to replace the wire deepen the chamber-as-trap angle, but a competing long documentary exists; medium |
| 6. Visual storytelling | **8** — tight chamber, split hull, lines, ballast, ship; relevant 2D host / photoreal world possible without invented archive; medium | **9** — distinct physical states (seal, three returns, fouling, manual buoyancy), suitable for illustration with sources; medium | **8** — source-grounded surface/buoy phone, anchor shift, blocked hatch, stuck reel, diver tangled in cables and ballast; rights/actual images UNVERIFIED; medium |
| 7. Natural speech / clarity | **8** — full sentences, no invented belief about the eight; fourth-trip closing connects to ascent opening; author-only; medium | **8** — actions move forward, admits 26 dead; end explanation a little technical; author-only; medium | **8** — specific actions replace general equipment lecture, but names Sibitzky/Clayton/Duncan and cable roles demand careful delivery; spoken TTS UNVERIFIED; medium |
| 8. Viewer interest evidence | **UNVERIFIED** — no comparable Nuviko sample; 325k Dark Seas public views do not imply Shorts outcome | **UNVERIFIED** — 2022 Dark Seas competes but its author baseline/CTR unavailable; no verified format comparison | **UNVERIFIED** — no normal long-video baseline, 30–90d growth, analytics or comments; confidence low |

**Rule threshold:** For 02m and 05m author's interest, development and payoff are each >=8 **with the exact evidence above**. The revised 10m now carries >=8 for interest, development and payoff, but **not a production PASS**: independent listener and voice duration are UNVERIFIED; at 150 wpm plus assumed pauses/end-screen it may undershoot ten minutes. In particular the salvage after the human climax could still lose attention.

## Concrete story maps (one history, different writing)

| Edition | Opening → setup | Change after hook → decisive action | Full end; weakest line/section |
|---|---|---|---|
| 02m | “A rescue chamber began climbing ... Then its cable jammed.” → Squalus sinks, 26 lost, 33 trapped, chamber seals | 25 saved; last eight board; jam, diver cuts, retrieval cable nearly fails → ballast changed in small steps | All 33 surviving people return, 26 mourned; worst risk: dense 2-line explanation of two cables, plus unverified spoken loop |
| 05m | “How do you lift people ... ? And what happens ...?” → valve and separate sections, Sculpin locates hull | seal and dry transfer; 7+9+9, then jam and near-snap → measured buoyancy and manual guidance | 00:23/00:25 rescue, later fifth flooded-compartment check, Sailfish coda; worst risk: one passage explaining chamber mechanics |
| 10m | “How do you reach thirty-three people ... ? And what happens ... ?” → 18 successful tests, flooding, smoke/phone link broken, 1927 S-4 rationale, Falcon moves anchors and Sibitzky clears hatch | 7/9/9 with changed load plan → motor/brake failure → Squire cuts → retrieving wire strands → Clayton/Duncan fail to attach replacement → 30/15/15-second buoyancy adjustment | 00:23/00:25 rescue, fifth flooded-room check, failed pontoon lift and Sailfish; weak spots: many diver names in short succession, salvage after the human payoff, conditional 10m duration |

**Short text loop evidence, author-only** (NOT independent PASS):
- Opening EN: “A rescue chamber began climbing from a sunken submarine with eight survivors inside. Then its cable jammed.”
- Ending EN: “Three trips had already reached the ship. The fourth was supposed to bring up the last eight.”
- Opening RU: “Спасательная камера поднималась с затонувшей подлодки. Внутри были восемь человек. И вдруг трос заклинило.”
- Ending RU: “Три рейса уже дошли до спасательного судна. Четвёртый должен был поднять последних восьмерых.”
- **Link (not only repeated noun):** closing places the fourth trip after three completed trips without inventing how passengers felt; opening then enacts its climb and jam. Cold open names what/where/how many without any preceding context; payoff of rescuing all 33 already occurs before final return. Whether repeated aloud **twice** has natural prosody and whether AV seam preserves chronology: **UNVERIFIED**; independent reader must challenge possible circular restatement.

## Comparative decision

**2 → 5 minutes gains:** who was separated by the watertight doors; how wreck found, why the chamber must seal dry; the exact pattern of increasingly familiar trips; and a clear post-rescue fifth check. These details build why the final jam mattered and how the solution works.

**5 → 10 minutes gains:** new sourced actions missing in 05m: buoy telephone fails, Falcon must reposition anchors, old marker line blocks hatch, an unplanned nine-person second load changes the third, brake fails after motor, Squire must cut the first line, Clayton and Duncan each fail to replace the second, timed 30/15/15-second ballast changes. This adds real causal obstacles, not repeated mechanics. After the core fourth-ascent climax, the fifth inspection plus failed salvage-pontoon lift still risk pulling the viewer into a secondary story. The 10m is complete but **DURATION/PACING UNVERIFIED**, with an underlength risk at the fast end of the assumed voice pace.

**Recommendation: 05m Long, unchanged and still unapproved.** It reaches the cable/buoyancy rescue with fewer procedural turns and preserves the same full 33/26 outcome. 02m is a tighter standalone Short with a new author-only loop. The revised 10m gains verified failed rescue attempts but risks slowing at the long run-up and post-rescue salvage; request a genuinely blind reader, never add unverified peril to force ten minutes. No master has been selected/approved by the owner.

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

## 2026-11-23 follow-up — preserved baseline and actual editorial change

| Edition | Before: branch HEAD / exact SHA-256 EN, RU | After: script SHA-256 EN, RU | What changed |
|---|---|---|---|
| 02m | `a000ad1f14ca7a2d65c571ed2c58af8431d35106`; `010d4e8ae5c8d5d488bc669cc7821912ece50711541abf9a58b6e414f6dd7f30`, `6ba9cec015281808406fff53f4c8bc50bdde77e56fa4455064e759ffe975f283` | `8713b07fede498ee96dae2c76d026d09aa7477a1b8c1070e15cf9903d0e0cff5`, `c389d9ea8f195eb8ca36e6bea50f49fc1cec600174d008ed7b27f3fff0e3129a` | Removed unfounded claim that the eight *believed* the difficult part was over; closing now places fourth ascent after three successful trips, to link chronologically to opening. Full EN/RU read by author; two-cycle independent/AV UNVERIFIED |
| 05m | `a000ad1f14ca7a2d65c571ed2c58af8431d35106`; `8da96f2f246b9795e09fe336c2cd6dbf797b787c2643366acc0dedd36556eefe`, `1039347ec8908a783737f31ed5709bf4ea0875b82ba9d18d466e0ba76b7b0a89` | **UNCHANGED** | Preserved strongest existing full narrative and 05m-only packaging; previous evidence retains exact hash |
| 10m | `a000ad1f14ca7a2d65c571ed2c58af8431d35106`; `b7edcf56283406707bab782f4fa19bd6a663988ffac025d2b118bd67ffb11d7d`, `e837136df6902e5df1309b6d565056c3f6481f13264156e92ea5915ac6380e9a` | `e9a37f4173fd8833f5d75561fd0912499c2236f15ed10e3bc042e738478f89a2`, `ae774c7413eae993a7e7a87486f263d3d846a020173658c3de4516ab2a9b1fcc` | Replaced generic setup/method recap with primary-sourced search/contact, boat positioning, hatch obstruction, changed passenger loads and two failed replacement-wire dives; compressed duplicate moral/aftermath; 1303 EN words and pacing/underlength risk |

**Story progression after revision:** 02m 25 safe → last ascent jams → damaged cable → near-neutral buoyancy → 33 survivor payoff → last trip becomes first line. 05m unchanged. 10m smoke/contact breaks → anchor and hatch hazards → 7/9/9 → fourth jam/brake fails → wire cut → retriever strands → replacement cable attempts fail → buoyancy in 30/15/15-second bursts → last eight safe → fifth no-survivors check → later failed hull lift and Sailfish.

**Evidence boundary:** NHHC rescue report indexed §§7, 11–18, 1939 Momsen lecture and Coast Guard account used for new claims; direct full NHHC HTML and the entire named passenger log still inaccessible. Detailed first/second/third/fourth flow supports 7+9+9+8, but NHHC's shorter DANFS summary says “last seven” and conflicts internally with 25+8=33. See [research](research.md). Independently reviewed source ledger and all spoken QA remain UNVERIFIED.

**Revision attempts:** original composition + one substantive author revision each for 02m and 10m; one author reading, not an independent reader or listening result. New hashes invalidate old review, timings, scene spans and any hypothetical script approval for those two texts. No actual stage receipt exists. The remaining technical and review checks in the matrix are unchanged. No retention, CTR or audience success asserted.
