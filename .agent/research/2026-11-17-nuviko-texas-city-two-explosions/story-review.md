# Story review — three finished variants, six exact texts

**Type:** author-only editorial evaluation, 2026-11-17. **NOT** an independent reviewer result. Editor: GPT-6, self-review; confidence moderate on literary judgment, high on basic documentary chronology, low on any unobserved audience or TTS claims. Baseline source commit: `6c436f4931aef33b745b74be2864a93c1db46362`. Sources and conflicts: [research.md](research.md). `EDITORIAL_CANDIDATE_UNREGISTERED`: no official `ytv start` / runtime task / independent session / receipt / approval.

## Exact immutable text identities (post remote read-back)

Paths relative to this folder. Git blob SHA identifies exact Git objects; SHA-256 below was computed on the full fetched UTF-8 text including final newline using a tested SHA-256 implementation.

| Variant | Production EN / SHA-256 | Review RU / SHA-256 | Git blob EN / RU | Count EN / RU |
|---|---|---|---|---|
| 02m | [script.en.txt](variants/02m/script.en.txt) — `343cbaf5d035c7639a3c9bc40b9e1f7f7dcdf0d1dcb6cdc154ff718774507288` | [script.ru.txt](variants/02m/script.ru.txt) — `97a887077036abe1996f9114962d10e3b880a0c656e62024658c821fbbe299be` | `9091cabafc0db181da52efb8d7241aae4c4703ee` / `7d77fa3a72e11f0539e0a9bf6954ca33e33233c1` | **320 / 262** |
| 05m | [script.en.txt](variants/05m/script.en.txt) — `f688900b14b5533aa0e7b5aea2745d7c83d107cf96514d9ef39b6d251b5e0b02` | [script.ru.txt](variants/05m/script.ru.txt) — `897911f05cf275817abbdda8004037ba56a238fc017e0f85cf9f4d9e5ca1c632` | `9b605663fa4225db3f0bc69f97f635344cb4bc22` / `9ed031df40a88d13f9ce299c837875bcba3f0c79` | **703 / 563** |
| 10m | [script.en.txt](variants/10m/script.en.txt) — `6e98aa7edf1a336d77ea71a0ab532fb91b81aaad2232b704b099359bf2420f37` | [script.ru.txt](variants/10m/script.ru.txt) — `e62aa4157fd41bf8943862017f58c321e3f2404d1beaff1f4c3bd745a41239bd` | `ff093bea0516ff862336e9213bfc12894611e2f0` / `4622e2766cc34c8bddbef7a383654ec054dff01b` | **1383 / 1133** |

**All three versions are full narrations** with own opening/causal middle/ending; not chapter outlines or cut-down master. Word counts use whitespace split on UTF-8; Russian numbers are not direct time proxies. Estimated EN speech-only intervals at **hypothetical 140–170 natural words/minute**: 02m 1:53–2:17; 05m 4:08–5:01; 10m 8:08–9:53. Add natural pauses, then for Long a **10-second end screen**. Nuviko configured ElevenLabs speed `1.1`; no known measured words/min at that setting. These are **estimated bands**, not actual voice duration and do not authorize changing speed to hit a target. Exact TTS and MP4 lengths `UNVERIFIED`.

## Canonical eight-dimensional editorial scoring

Score definitions from `docs/standards/editorial.md#пакет-одной-истории`. Each number is **subjective author judgment** with a concrete cue, not measurable retention/CTR/likelihood of success. The **view-interest confirmation** dimension is `UNVERIFIED` for all three: presence of comparable videos is observed but same-author baselines, private metrics and distinct angle demand are not established.

| Dimension | 02m — evidence / score | 05m — evidence / score | 10m — evidence / score |
|---|---|---|---|
| **1. Interest / significance** | **9** — two separate ship explosions, failed ship rescue / successful withdrawal; civilian disaster with recorded 581 toll | **9** — same stakes plus people actively choosing evacuation amid rescue | **9** — damaged town, injured schoolchildren, second ship, human and regulatory aftermath; no invented hero |
| **2. Opening** | **8** — “How could a ship full of fertilizer destroy a city?” clear question but brief Long exposition may sound familiar | **9** — three specific promises (fertilizer force, second blast, lives saved) mapped to answers | **8** — three questions and harbor setup, but long-form history context briefly delays the first smoke |
| **3. Development / reason to stay** | **8** — ineffective steam → 09:12 blast → High Flyer burning → tug failure → evacuation; compact but secondary vessel enters late | **9** — smoke and chemistry cause the first explosion; ruined firefighting capacity alters response; stranded High Flyer forces new decision | **7** — rich first and second act, but after second blast there are several report, litigation and memorial paragraphs; risk that promise is fulfilled before tail |
| **4. Payoff** | **8** — “getting people away before it exploded saved lives” exactly answers why second blast was less fatal, but sacrifices emotional time | **9** — “The attempts to tow High Flyer failed. The decision to get people away did not.” directly completes the human-choice question | **8** — “They could stop more people from standing in its path.” closes main thesis, but longer post-climax detour reduces force |
| **5. Freshness of angle** | **7** — second explosion is known to previous documentaries; focus on changed casualties is a proposal, not proven unique | **8** — opposed outcomes (cannot move ship vs can move people) anchor whole middle; no exclusive original discovery | **7** — same angle plus detailed aftermath competes with several 2022 documentary retellings |
| **6. Visual expressiveness** | **9** — steaming hatch, orange smoke, blast, ruined engines, tugboats, evacuation | **9** — clear separate spatial positions Grandcamp / High Flyer / Wilson B. Keene and progression of two nights | **9** — dock industries, damaged firefighting equipment, shelters, vessel drifting, aftermath memorial; historical props require source-accurate reconstruction |
| **7. Naturalness / clarity** | **8** — named vessels introduced by role, short actions; may need another sentence defining nitrate | **8** — ordinary causal narration with “The anchor would not come up”; a few abstract chemistry sentences need first-listener check | **7** — precise report conflict handled ethically, but “accounts differ” and legal aftermath risk becoming an academic report |
| **8. Verified viewer interest** | **UNVERIFIED** — relevant videos from multiple authors are public; no matched performance | **UNVERIFIED** — 2022 English Long analogues, no real retention/CTR, comment texts unavailable | **UNVERIFIED** — 2026 Ben Miles upload not a verified Long baseline; long audience appetite unmeasured |

### Independent per-text editorial diagnoses, iterations and classification

**02m — STRONG_CANDIDATE** (subjective interest/development/payoff = **9/8/8**; confidence moderate). Opening line: “How could a ship full of fertilizer destroy a city?” The first explosion leads to a fresh threat, which produces the complete evacuation payoff. Principal weakness: exposition and two ship names crowd 320 English words; climax can feel swift. No further speculative scenes added. **Author pass 1 only**, no independent observer.

**05m — STRONG_CANDIDATE, RECOMMENDED** (interest/development/payoff = **9/9/9**; confidence moderate). Opening asks explicitly what the response could save. The second ship drifts toward Wilson B. Keene; the crew cannot raise anchor; tugs cannot shift High Flyer sufficiently; the docks empty, answering the opening. Principal weakness: the chemical paragraph risks sounding explanatory rather than visual, but prevents misrepresenting fertilizer as universally explosive. **Author pass 1 only**. No claimed measured first-30-second retention.

**10m — REWORK** (interest/development/payoff = **9/7/8**; confidence moderate on weakness). Complete documentary script with genuine additional source-grounded detail: ordinary cargo/war conversion, exact engineering damage, 1947 conflicting reports, rescue logistics, extended aftermath/claims. Principal weakness: the post-second-blast section may be too long once main human payoff is clear, and early question structure is less sharp. **Not** promoted to STRONG_CANDIDATE by averaging scores. One substantive edit should move or remove weaker post-payoff history, **without inventing new events or ignoring the requested ten-minute independent value**. Maximum two meaningful author reworks before reevaluation/REJECT; none done yet.

## Finished-text comparison: marginal value of duration

| Transition | New meaningful information | Cost / probable audience risk |
|---|---|---|
| 02m → 05m | Geography of three ships, sulfur/nitrate cargo of High Flyer, anchor stuck, tugboat failure, organized relief workers, clearer human decision | +383 EN words for verified obstacles and altered expectations; worthwhile, not redundant |
| 05m → 10m | Post-war origin of fertilizer, school glass injury, industrial debris, discrepancy 100-foot tow vs “barely moved,” attribution of second death count, legal aftermath and unnamed victims | +680 EN words, some contextual insight, but detailed post-climax investigations dilute the strongest ending; review classification **REWORK** |

**Recommendation:** use the **05m English** as proposed production master **only after independent review and explicit user approval**. 02m remains a standalone suitable shorter documentary Long; 10m remains a complete but weaker editorial alternative, not a blocked partial text. Don't create 3 runs.

## Story maps by exact version

- **02m:** two opening questions → smoke in Grandcamp's cargo → steam/closed hatches → detonation at 9:12 → local firefighting destroyed → High Flyer burning and stuck → withdrawal of people → detonation at 1:10 → fewer second casualties → “getting people away ... saved lives.”
- **05m:** three questions → harbor and nitrate → steam failing and orange smoke → first blast → destroyed responders and volunteers → damaged High Flyer drifting toward Keene → anchor and tug failure → evacuation choice → second blast → comparative toll → decisive contrast.
- **10m:** three questions → port context and postwar cargo → hidden chemical crisis → first blast and industrial extent → relief despite destroyed fire equipment → three-ship geography → failed anchor → disputed tow distance → decision to clear area → second blast → uncertainty of records → regulatory and remembrance context → final human payoff.

All three first lines are actual spoken questions, not a pre-story chapter title. The main hook follows initial meaningful action (first blast); no forced one-minute intro on 02m. For **Long**, narrative loop is **N_A**, not a fabricated Short loop; channel has actual Long support in `channels/nuviko_history/channel.json`.

## Distinct factual/format/review gates (author evidence, not runtime receipts)

| Check | 02m | 05m | 10m | Basis and limits |
|---|---|---|---|---|
| Key event chronology / core causality | **PASS (author fact map)** | **PASS (author fact map)** | **PASS (author fact map)** | 1947 report + City of Texas City + TSHA; disagreement on towing and second death count bounded/attributed, not ignored |
| EN/RU meaning and key caveats | **PASS (author comparison)** | **PASS (author comparison)** | **PASS (author comparison)** | Six full parallel versions, dates/causes/casualties/passive claims checked; independent translation reader `UNVERIFIED` |
| Long format / ChannelSpec | **PASS (editorial design)** | **PASS (editorial design)** | **PASS (editorial design)** | Nuviko active, `long` 16:9/30fps supported; no actual runtime start/format pin |
| Short narrative seam | N_A | N_A | N_A | These texts are designated documentary **Long**, even 02m |
| Actual AV seam / spoken time | UNVERIFIED | UNVERIFIED | UNVERIFIED | No TTS, audio listening or MP4; final 10s end-screen placement also unmeasured |
| Rights of narration | **PASS (original text claim)** | **PASS (original text claim)** | **PASS (original text claim)** | Original narration, no borrowed passages or media bytes; third-party image/audio licensing and provenance `UNVERIFIED` |
| Independent first-listener review | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** | No independent session/capability result, no genuine `ytv-script-review-v1` |
| Actual script approval / runtime gate | **UNVERIFIED / not run** | **UNVERIFIED / not run** | **UNVERIFIED / not run** | Git-only editorial scope; no `ytv start`, run ID, lease, claim, receipt, gate or owner approval |

Review cannot be labeled independent merely because an author has checked the texts. A future reviewer must see each exact input without this score table or beat map, give native response and then receive source list. Any changed text hash invalidates review and related scene timings. No storyboard timing, image, voice or MP4 created.
