# Story review — three exact editions of the same cable-assignment experiment

**EDITORIAL_CANDIDATE_UNREGISTERED.** Authorial assessment on 2026-11-18; **author: current editorial agent**, no separate reader, new agent session or authenticated runtime. Confidence: **high** in arithmetic of the explicitly specified model; **medium** in narration/translation, **low** in audience interest and natural timing. No numbers below imply retention, CTR, expected views, probability of success, independent approval or a real-life measurement.

## Exact remote script bytes and estimated speech

SHA-256 are exact UTF-8 file byte hashes including the actual final line endings, computed from remotely fetched branch content; Git blob SHA read-back is separate.

| Target | Full EN / SHA-256 | Full RU / SHA-256 | Whitespace-separated EN / RU words | Estimated spoken duration / format |
|---|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) `a81ff93a867f5325258cff384fafa5a8daff624aa0d643edc541871adf2e3f9e` | [RU](variants/02m/script.ru.txt) `46a71defb9f9da93e9f4254f81cf57df370fd63dd4cfffe4b4194c616c5a02fc` | **313 / 266** | Approx **1:49–2:08** with assumed 155–175 EN wpm plus 2–5s narrative pauses; proposed Short but above 35–50s channel target |
| **05m** | [EN](variants/05m/script.en.txt) `246795af3823aac36a395f4f19e582766b286fc97c2bc7c28dc36152ca478c33` | [RU](variants/05m/script.ru.txt) `01ca06e528a3db6d16ad6233a6d44a334e71cd2dbb09b78ef07de6b49014e97a` | **794 / 611** | Approx **4:40–5:20** with assumed 155–175 wpm plus 8–14s pauses; **recommended editorial Long, currently unsupported format** |
| 10m | [EN](variants/10m/script.en.txt) `90fb611327c015779f9a4f67128f01c08cf4a669d847b62ec77c7ef22feaced7` | [RU](variants/10m/script.ru.txt) `a56f7e548a61eac8ba93f9d19654435b503472acdbde3662ae355fc91bad0987` | **1,731 / 1,422** | Approx **10:02–11:20** with assumed 155–175 wpm plus 8–12s pauses; may exceed 10m, no Long recipe, and editorial REWORK |

No TTS or measured audio exists. The assumed speed range is not an authorized voice-speed change. The Russian is a complete sense-matched reading edition; EN is the intended narration master. Separate SHA-256 is required if either language changes.

## Same math, same stakes — the non-fiction boundary

The model is *authored*, not measured: rack `V,H,D,B`, devices monitor `{V}`, laptop `{V,H}`, drive `{V,D}`, phone `{V,H,D,B}`, with one cable per device, and computer ports/power support assumed. A connects phone→drive→laptop→monitor by first compatible remaining cable; B connects monitor→laptop→drive→phone with the same selection rule. Both start disconnected with identical cable rack. Predeclared metric: number of working devices **after first pass, before any swap**.

A `phone=V, drive=D, laptop=H, monitor=none` ⇒ **3/4**. B `monitor=V, laptop=H, drive=D, phone=B` ⇒ **4/4**. Reassign A's phone cable to monitor and B to phone ⇒ **4/4 after repair**, not a first-pass result. Rack reversed to `B,D,H,V`, A also gets **4/4**. Replace V with another B ⇒ no video-capable cable; at most **3/4** under either method. All claims reproduce by enumerating the defined compatible sets. No assumed observed timings; no statistical extrapolation; sorting by fewest options isn't claimed optimal for all generalized assignments.

**External fact boundary:** Microsoft USB-C troubleshooting supports the premise that same connector does not guarantee display/power/data features, and that port/charger support matters: https://support.microsoft.com/en-us/windows/hardware/usb/fix-usb-c-problems-in-windows . It does not supply the made-up rack, the result, or effectiveness evidence. A real question from a user about “charges but no video” exists at https://www.reddit.com/r/UsbCHardware/comments/1egw2yz (2024-07-31), but does not validate the model or this channel's demand.

## Eight required editorial criteria — exact 02m EN/RU pair

| Criterion | Score and exact ground |
|---|---|
| 1. Interest/significance | **8** — “My phone gets the best USB-C cable ... until my monitor stays black” is a comprehensible, relevant personal mistake. Significance is narrow: a desk, not a universal urgent decision |
| 2. Opening | **8** — first sentence immediately contrasts fitting cable with dark screen; cold entry doesn't need terminology |
| 3. Causal development / desire to stay | **8** — phone consumes V → drive consumes D → laptop consumes H → monitor fails → same reset B produces four successes → changed order can matter. Specific moves, no arbitrary extra delay |
| 4. Payoff | **8** — explicit “Three devices work. One dark screen”, then “Four out of four”, correction by swapping and honest one-pass limitation |
| 5. Freshness of angle | **8** — matching scarce capabilities (not generic USB-C buying list), but cable confusion itself is familiar and the constructed experiment may feel like a puzzle |
| 6. Visual expressiveness | **8** — four visibly labeled cable cards, initially dark monitor, assignments and reset; requires exact visual numbers/text provenance later |
| 7. Natural speech / comprehension | **8** — “I reset every connection” and “I could rescue A by swapping” provide ordinary action and honest rebuttal; abbreviation V/H/D/B not spoken in this brief version |
| 8. Confirmed viewer interest for this exact variant | **UNVERIFIED** — public tech explainers are not matched comparisons to an original illustrated Two Ways Short; no audience data |

**Author verdict: STRONG_CANDIDATE (editorial only).** Interest 8/development 8/payoff 8 individually meet minimum. **Main flaw:** over twice the current channel's 35–50s preferred Short length; 313 words and potential math-heavy structure threaten actual Shorts attention. The deliberate colon at final→first seam may feel engineered. Unmeasured AV seam. Confidence: medium on wording, low on actual Short suitability.

## Eight required criteria — exact 05m EN/RU pair

| Criterion | Score and exact ground |
|---|---|
| 1. Interest/significance | **8** — “exactly enough cables ... still cannot connect everything” directly promises a useful everyday explanation |
| 2. Opening | **9** — two short questions introduce an apparently impossible failure and a fix without a purchase; model disclosed immediately after |
| 3. Causal development / desire to stay | **9** — A's screen failure → visible swap that repairs A but not first-pass score → reset and B works → physical cable-order reversal creates a fair tie → missing V bound |
| 4. Payoff | **9** — “I ran out of the one capability that mattered,” then 4/4 and the counterexample 4/4 tie, followed by “save the rare capability for the device that actually needs it” |
| 5. Freshness of angle | **8** — capability reservation is a distinct narrative form from widespread buying-guide videos; still a hypothetical classroom-scale test |
| 6. Visual expressiveness | **8** — complete reset, four cable cards and three changes in visible outcome; tricky AI consistency on on-screen inscriptions and cable counts |
| 7. Natural speech / comprehension | **8** — physical sequence and “the monitor ... only handles basic charging” are clear; long model setup and exact compatibility table may need an independent listener to confirm cadence |
| 8. Confirmed viewer interest for this exact variant | **UNVERIFIED** — x-kom and Les Tests de Cyril videos do not predict a five-minute original simulation |

**Author verdict: STRONG_CANDIDATE, recommended editorial.** Interest 8/development 9/payoff 9. **Main flaw:** no enabled Two Ways Long production recipe, so an editorially strong five-minute script cannot be treated as a ready-to-render Long. Its middle may feel instructional to a casual viewer. Confidence: medium for text, low for audience response/production.

## Eight required criteria — exact 10m EN/RU pair

| Criterion | Score and exact ground |
|---|---|
| 1. Interest/significance | **8** — same useful dark-monitor mistake, but original question supports a shorter run |
| 2. Opening | **8** — dark monitor and "change the order" promise established early |
| 3. Causal development / desire to stay | **6** — the vivid A/B and reverse-rack counterexample happen well before long later blocks about ports, priority, generalized greedy matching; after the result much of the content explains scope rather than changing the goal |
| 4. Payoff | **7** — three concrete conditional outcomes and valid final conclusion, but repeated qualifications dilute emotional sense of resolution |
| 5. Freshness of angle | **7** — scarcity rule is distinctive but additional material becomes generic cable or optimization explanation |
| 6. Visual expressiveness | **7** — late sections may require repeated text panels rather than new real-world actions |
| 7. Natural speech / comprehension | **7** — intelligible but some paragraphs sound like formal explanations: “I didn't prove that blindly sorting devices ...” |
| 8. Confirmed viewer interest for this exact variant | **UNVERIFIED** — no verified ten-minute audience/retention evidence for this channel or comparable new creator |

**Author verdict: REWORK.** Interest 8/development 6/payoff 7, so cannot be STRONG_CANDIDATE even if its average were high. **Main flaw:** didactic tail and likely >10m measured duration at ordinary voice pacing. This is still a **complete independent text**, not a beat outline or cut-up master. No fabricated incident to extend it. Confidence: medium that it needs editing, low on actual observed viewer patience. No more than two future *meaningful* author revisions; none claimed in this assessment.

## Story map and accurate promise of each complete version

- **02m:** device order first gives V to phone, monitor dark; B reset yields four successes; cheap swap resolves A outside first-pass metric; no claimed seconds saved; last line returns to the habitual choice, leading into first. Source: exact [02m scripts](variants/02m/).
- **05m:** two opening questions → model/metric and limited choices → first device-list allocation fails → repair explicitly demonstrates it's not permanent → B resolves all → reverse cable rack lets A tie → remove V makes both fail → finished conditional practical lesson. Stronger independent factual/payoff chain. Source: [05m scripts](variants/05m/).
- **10m:** first-person desk setup and fair two policy experiment → A/B + repair → reverse rack tie → V-removal impossibility → differences between physical connectors/ports, cost of learning labels, limited generalizability of greedy allocation, priorities → full bounded conclusion. Source: [10m scripts](variants/10m/).

## Finished-text increment comparison

| Comparison | Real additional story value | Where it may lose the viewer |
|---|---|---|
| 02m → 05m | Explains *why* A can be repaired yet loses first-pass score, counts choices for each device, reverses physical cable rack to fairly challenge B, shows impossibility when video capability is removed. A different authored progression, not padded 02m | During complete compatibility table and reset; short-form audience may expect reveal much sooner |
| 05m → 10m | Distinguishes missing capability vs bad order, goes deeper on real ports/chargers, missing labels, difference between optimization and priority, and limitations of local greedy matching | After reverse-rack tie/absence of V, new paragraphs are qualifications rather than new attempts; ending arrives late |

**Recommended duration: 05m, editorial only**, because it adds real fairness tests beyond the first reveal, whereas 10m loses evolving stakes. **02m remains a strong self-contained script** in a format misfit. The recommendation does not authorize choosing the 05m as a runtime master or manufacturing a Long recipe.

## Separate tests — no fake PASS

| Gate/check | 02m | 05m | 10m |
|---|---|---|---|
| Model arithmetic, fixed assumptions (author enumeration) | **PASS (author)** 3/4 vs 4/4, repair | **PASS (author)** includes reverse rack 4/4 and no-V bound | **PASS (author)** same, extended caveats |
| Real hardware distinctions (Microsoft) | **PASS (author)** conditional, no false product performance claim | **PASS (author)** port, cable, charger roles qualified | **PASS (author)** same |
| EN/RU full text and meaning equivalence (author text check) | **PASS (author)** same result/exception, both full | **PASS (author)** same A/B, swap, rack, no-V condition | **PASS (author)** same causal sequence and limits |
| Format against current Two Ways ChannelSpec | **FAIL/blocked** 35–50s Short target vs >100s estimated | **FAIL/blocked** Long video format fields/recipe undefined | **FAIL/blocked** Long video format fields/recipe undefined |
| Narrative Short loop, text-only author review | **PROVISIONAL:** EN closing “my first instinct returns:” → opening “My phone gets the best USB-C cable on the desk.” RU closing “я снова по привычке думаю:” → opening “Телефону достаётся лучший USB-C кабель”. Answer has already occurred; cold start is intelligible. **Independent double-cycle seam UNVERIFIED**, contrived-colon risk | **N_A** Long proposal | **N_A** Long proposal |
| Actual AV seam, voice duration, footage/rights | **UNVERIFIED** no MP4, TTS or reference images | **UNVERIFIED** | **UNVERIFIED** |
| Blind independent first-listener review per actual schema | **UNVERIFIED** no fresh reviewer session available | **UNVERIFIED** | **UNVERIFIED** |
| Official runtime start/plan/pins/receipt and owner script approval | **UNVERIFIED** no local authenticated CLI/store available | **UNVERIFIED** | **UNVERIFIED** |

**No fabricated reviewer feedback, approval, script-gate receipt, published evidence or video analytics.** A self-review is a different thing from an actual reader. New exact bytes/hash require a new reader. No storyboard/scene span production prepared for unsupported Long recommendation. The complete Russian and English scripts are Git editorial source proposals, not TTS-ready approved assets.
