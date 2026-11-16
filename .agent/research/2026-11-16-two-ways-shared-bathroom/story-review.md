# Story review — author-only scores for six exact texts

**Author:** automated editorial draft author, 2026-11-16. Confidence **high** in arithmetic because event ledger is deterministic; **medium/low** in script appeal and natural delivery; independent reviewer, measured TTS pacing, actual YouTube demand, exact AV loop all **UNVERIFIED**. Eight per-variant scores are editorial opinions about exact text, not CTR/retention or performance probabilities.

## Exact files and SHA-256

| Редакция | Полные EN / RU | EN / RU words | EN SHA-256 / RU SHA-256 | Статус |
|---|---|---:|---|---|
| 02m | [EN](variants/02m/script.en.txt) · [RU](variants/02m/script.ru.txt) | 322 / 288 | `6e95a4dfa8c6cbc49a72ef0d1d0b3931b1813370db164fb19da8a05e22d01e96` / `071ad7cf2a87c976c1023ad69ba9f9406d068533e4102dd600a28a2b165bc743` | STRONG_CANDIDATE, recommended |
| 05m | [EN](variants/05m/script.en.txt) · [RU](variants/05m/script.ru.txt) | 877 / 701 | `fbf773b0e876b0d5459b1ea4f986e00e5c239eff477053a390bff512447d99b7` / `9b34a79345e1651c3dd1988c885e75c7ba7b88d3bba4048bbef83baac178d09a` | STRONG_CANDIDATE, editorial Long / production BLOCKED |
| 10m | [EN](variants/10m/script.en.txt) · [RU](variants/10m/script.ru.txt) | 1969 / 1568 | `91ced491b1fe7b09e8da636a79fe3fac28a78b637fbef77b594f42524e0c3980` / `ce9125001d1256f86395d828b9d8aa57e1d8fda8e90bb9079cfc84732f7a2128` | REWORK, complete editorial Long / production BLOCKED |

Hashes are SHA-256 of UTF-8 text with final newline (self-tested SHA-256 `abc` vector). New bytes invalidate corresponding score and future reviewer/scene pins.

## 02m — STRONG_CANDIDATE, recommended

1. **Interest/significance 8/10**, medium: “we both got ready three minutes faster” converts abstract room usage into the concrete 08:00 lateness; the three-minute margin is small, not a life-or-death stake.
2. **Opening 9/10**, medium: “I left our only bathroom empty for seven minutes” is specific and initially contradictory; pair and deadline arrive early.
3. **Development 9/10**, medium: busy fourteen-minute room → 08:02 failure → empty seven minutes → 07:59 success. New information, not repeated hook.
4. **Payoff 9/10**, medium: “same fourteen minutes of actual bathroom work” resolves mechanism and answers which rule wins; note the result assumes zero return overhead.
5. **Angle freshness 8/10**, low: familiar time-management technique reframed as utilization paradox, not a claim of unique original discovery.
6. **Visuals 9/10**, medium: two beds/dressing spaces, shared bathroom door and two clocks make alternate trajectories explicit; no frames generated or QA performed.
7. **Oral clarity 8/10**, medium: natural I-voice and ordinary actions; 320 EN words and several numeric steps may still be dense at 2m; not listened to.
8. **Audience demand UNVERIFIED**, low: older indexed morning-routine videos + genuine audience questions, not comparable own-video baselines.

**Map**: time pressure → A/B choice → fixed tasks → full occupancy but lateness → deliberate empty room → early shared finish → parallel-dressing explanation. **Weakest point:** verbal numbers cluster in middle; the illustration must reinforce them without substituting for the text. **Loop author check:** ending “If Sam asks what I changed ... I can finally give a precise answer:” → opening “I left our only bathroom empty for seven minutes.” Direct question/answer in a natural new cycle, payoff before repeat. It's more than a matching object or colon, but an independent two-cycle reading and AV seam are UNVERIFIED.

## 05m — STRONG_CANDIDATE (editorial Long), production BLOCKED

1. **Interest 8/10**, medium: visible deadline and same-amount-of-work paradox; a five-minute explanation costs some immediacy.
2. **Opening 8/10**, medium: two concrete questions about empty room and extra minutes; audience knows the promise before detail.
3. **Development 8/10**, medium: 07:44 handoff / 08:02 miss → 07:46 early dressing / 07:59 exit → three-minute setup reversal. Each changes interpretation.
4. **Payoff 9/10**, medium: base A vs B plus counterexample with specified new cost and conditional recommendation.
5. **Freshness 8/10**, low: idle room can improve person flow is a useful framing, but task scheduling is established.
6. **Visuals 8/10**, medium: two timelines and a conspicuously empty doorway; simulated clocks need image-generation rules, no frames checked.
7. **Oral clarity 8/10**, medium: 877 EN words, read as a cohesive first-person demonstration; model values need visual breathing room; TTS speed not measured.
8. **Demand UNVERIFIED**, low: no measured A/B scheduling video performance / studio data.

**Map:** questions → one-bathroom deadline → fixed jobs → A's failure → B's anomalous room idle time → departure winner → setup penalty exception → actual useful rule. **Weakest point:** 5m elaborates exact timestamps that might be better handled visually; cannot silently cut them after approval. **Loop:** N_A for Long.

## 10m — REWORK, complete editorial Long; NOT recommended

1. **Interest 7/10**, medium: personally relevant 08:00 story, but task itself is small for ten minutes.
2. **Opening 8/10**, medium: asks empty-room paradox and its reversal; questions are anchored in one model.
3. **Development 7/10**, medium: the inverse conclusion at h=3 is useful, but 1984 English words repeat 02m/05m core before the sensitivity and metric distinctions.
4. **Payoff 8/10**, medium: answers both base and changed-input cases precisely, but incremental gain over 05m is modest.
5. **Freshness 7/10**, low: alternative starting order and personal-vs-joint metric deepen mechanism but are not separate new dramatic events.
6. **Visuals 8/10**, medium: time bars, two actors and busy/idle intervals work if designed well; sustained similar scenes could bore.
7. **Oral clarity 7/10**, medium: complete first-person script, yet 1984 EN words likely >10 minutes at moderate voice speed; real reading UNKNOWN and no speed increase allowed.
8. **Demand UNVERIFIED**, low: no comparable ten-minute audience evidence.

**Map:** three promised questions → task ledger → A continuous busy failure → B idle success → difference in clocks and last-finisher → who-goes-first counterexample → independent vs joint deadline → setup h=1/2/3 reversal → applicability boundaries → explicit resolution. **Weakest point:** some material restates same relationship; a future independent reviewer may recommend rejecting 10m. **Loop:** N_A, Long.

## Comparison of actual completed scripts

| Transition | Material new value | Cost / likely drop |
|---|---|---|
| **02→05** | Exact human timeline, no-hidden-head-start demonstration and return-cost counterexample flip | After first result, repeating wall-clock labels can shift interest into tutorial mode |
| **05→10** | Why swapping first person in A doesn't help, alternative individual metric, sensitivity h=1/2/3 and explicit critical-resource interpretation | Very long for small stakes, some explanatory rephrasing, poor Long visual variety |

**Recommendation:** 02m, not because it is shorter by default, but because A's failure, B's paradox and reason land with fewer repeated timestamps. 05m is a reasonable full editorial alternative if the owner wants explanatory precision. 10m is complete but editorial REWORK; do not spend production resources on it. Recommendation != script approval.

## Independent checks, not blended with scores

| Check | 02m | 05m | 10m | Basis |
|---|---|---|---|---|
| Internal toy math | PASS | PASS | PASS | Deterministic schedule ledger in research; no measured-world claims |
| Source-backed real-life measurement | N_A | N_A | N_A | Explicit fictional durations / model |
| EN/RU semantic equivalence | AUTHOR PASS | AUTHOR PASS | AUTHOR PASS | Same actors, 4/3/10/1, 5/2/10/1, A/B ordering, 08:02/07:59 and conditional exception |
| Format feasibility | Short PROFILE supports 9:16; duration unmeasured | BLOCKED | BLOCKED | Current Long canvas/fps null, recipe undefined |
| Rights for future assets | UNVERIFIED | UNVERIFIED | UNVERIFIED | No media or licensing completed |
| Shorts loop | AUTHOR TEXT CHECK; independent UNVERIFIED | N_A | N_A | Exact end→start shown above; no MP4 |
| Independent first-listener | UNVERIFIED | UNVERIFIED | UNVERIFIED | No fresh separate reviewer session or real schema receipt |
| Actual pacing/TTS/AV | UNVERIFIED | UNVERIFIED | UNVERIFIED | No recording, frames, video |

There was one author revision of 02m ending for a genuine question/answer seam, and one wording clean-up of 10m. No fabricated reviewer, independent opinion or provider check.
