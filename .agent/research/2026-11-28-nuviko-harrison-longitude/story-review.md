# Author review — exact text, not independent reviewer
2026-11-28; author ChatGPT; confidence medium for editorial judgment, not empirical audience interest. Exact UTF-8 files with final newline. Hash implementation SHA-256 self-test abc passed. Author read both language versions in full and compared event sequence, opening, payoff and additions. No actual listening or runtime test. All proposed Long, 2m deliberately not Short (no forced loop; story uses question-led documentary structure). ChannelSpec supports long, 10s endscreen. No AV/timing claim. 

| Variant | Language | Words | SHA-256 |
|---|---|---:|---|
| [02m/script.en.txt](variants/02m/script.en.txt) | EN | 264 | `2ae6e79798745a1e55d395d87f0858be3b0466b76a5c2b343da493a71e213e92` |
| [02m/script.ru.txt](variants/02m/script.ru.txt) | RU | 228 | `d4078e3be8d90a7da8a6d8782d44927ef5002eea274f7addf6b845d187a2b9a3` |
| [05m/script.en.txt](variants/05m/script.en.txt) | EN | 682 | `dbdd555daf4832b1948903c2e25b22a2a3d7f724d1bf622571aa7c2018019ec2` |
| [05m/script.ru.txt](variants/05m/script.ru.txt) | RU | 598 | `661b950bf42513d3643931913f1825191789013004a4d74dc1e46319836522fd` |
| [10m/script.en.txt](variants/10m/script.en.txt) | EN | 1471 | `4973af232a8beab340ae66a4b2b1e72693a5664cd32938e444bbd1c525e21a49` |
| [10m/script.ru.txt](variants/10m/script.ru.txt) | RU | 1290 | `fb0b142d72b19e48181eb322050ee642ccce4b9905fef8a2dc9dc8b80d04bbfd` |

Estimated effective English narration range 125–150 words/min, not measured, configured voice speed 1.10x applied once in actual production, not here. Allow 10s endscreen and natural pauses; exact duration may require editorial pacing review, not speeding up words. RU word count is a separate reading aid, not a production timing claim.

## 02m — STRONG_CANDIDATE
| Criterion | Score / concrete basis |
|---|---|
| Interest/significance | 8 — concrete navigation problem |
| Opening | 8 — two specific questions, but no human action until paragraph 3 |
| Development | 8 — switch of scale, two tests, new replication requirement |
| Payoff | 9 — Cook praises copy and final distinction |
| Freshness | 8 — replication instead of lone genius |
| Visual expression | 8 — sun, ship, watch, copy |
| Natural speech | 8 — compact, last two lines plain |
| Audience evidence | UNVERIFIED — research has indexed videos and qualitative questions but no comparable creator baseline |

Main weakness: loses H1 headland and rival method; risk the first astronomy sentence is dense. Confidence medium; self-assessment only. Facts: author PASS on stated claim ledger, independent corroboration/reviewer UNVERIFIED. EN/RU equivalence: author PASS on same causal events and material qualifications. Format: PASS against current ChannelSpec, not pinned run. Rights: UNVERIFIED, no media chosen; loop: N/A Long; independent review: UNVERIFIED. Endscreen source and actual native target UNVERIFIED. No approval.

## 05m — STRONG_CANDIDATE
| Criterion | Score / concrete basis |
|---|---|
| Interest/significance | 9 — recognizable lost position and two real landfall corrections |
| Opening | 8 — unusual buying question answered by captain's request |
| Development | 9 — H1 result → H3 dead end → H4 → new condition → K1 |
| Payoff | 9 — Cook's three-year test and cost barrier |
| Freshness | 8 — two separate proofs, not a villain story |
| Visual expression | 9 — two headlands, large clock vs watch, two voyages |
| Natural speech | 8 — conversational but commission terms are dense |
| Audience evidence | UNVERIFIED — research has indexed videos and qualitative questions but no comparable creator baseline |

Main weakness: legal paragraph may be where a listener disengages; visual clarity required. Confidence medium; self-assessment only. Facts: author PASS on stated claim ledger, independent corroboration/reviewer UNVERIFIED. EN/RU equivalence: author PASS on same causal events and material qualifications. Format: PASS against current ChannelSpec, not pinned run. Rights: UNVERIFIED, no media chosen; loop: N/A Long; independent review: UNVERIFIED. Endscreen source and actual native target UNVERIFIED. No approval.

## 10m — REVISED_CANDIDATE
| Criterion | Score / concrete basis |
|---|---|
| Interest/significance | 9 — H1 correction and Cook's decision bookend practical navigation stakes |
| Opening | 9 — questions P1, coastal context P2, actual headland correction P3 |
| Development | 9 — P10–14 engineering, P15–22 dispute and replication, P25–28 real limitations and payoff |
| Payoff | 9 — actual St Helena landfall and comparison P27–28; P30 returns to first decision |
| Freshness | 8 — same replication lens plus documented stale-rate calculation and complementary methods |
| Visual expression | 9 — headlands, H4/K1, sealed box, Wales observations, island approach; board still abstract |
| Natural speech | 8 — shorter setup, no defensive essay commentary; P17–20 and P25–26 remain dense |
| Audience evidence | UNVERIFIED — no comparable creator baseline or actual channel analytics |

Author ChatGPT, confidence medium, not independent. Facts and EN/RU meaning author PASS against revised ledger; P25 conditional estimate using old rate, P28 Cook's reported comparison of longitude differences, not absolute whole-voyage error. Format PASS against current ChannelSpec, not pinned runtime; loop N_A Long. Exact duration/AV, independent reviewer, rights, actual native endscreen/target UNVERIFIED. Estimated English speech 588–706 s + 10s endscreen; pauses unmeasured. Do not manipulate voice speed to hit duration.

## Revision and comparison
Baseline commit `c7950f663b4ff8ff2290fb0e41cf15980862c0d4`; original 10m EN `027cfcb12553673a18b61d7c849c7980bd630cc7ba8923f7072d45e3176e0dc3`, RU `aeb769975c9faa70553bf6a98506c2f46f3b5011dbd1e93adb92c5361adb705e` (SHA-256, paths above). Prior 10m review and timings superseded for changed bytes; baseline remains in Git history. 02m/05m preserved byte-for-byte: each independently resolves the question of longitude and repeatability. 02m P2 dense; 05m P13–14 legal terms potential attention drop. 10m before: H1 payoff P11, prolonged setup, lunar detour and abstract commentary, Cook reduced to praise. After: P3 H1 result, press campaign, sealed box, K1 inscription, Cook/Wales rate limitation, direct course and island landfall with concrete comparison. 02 → 05 earns H1, H3 and Madeira; 05 → 10 earns real voyage test, calibration and complementary methods. Possible 10m attention loss P17–20 (Barbados/legal terms), P25–26 (conditional calculation), but latter earns its place by explaining actual use. Recommend **05m** for general-history audience: complete payoff and higher event density. Exact 05m EN unchanged: `dbdd555daf4832b1948903c2e25b22a2a3d7f724d1bf622571aa7c2018019ec2`. Revised 10m is distinct editorial alternative, not accepted master.

## Story maps (exact manifest; paragraph spans EN/RU)
Editorial visual intent only, not detailed storyboard or measured timing. Actual references and rights pending.

| Version | Paired spans | Intent |
|---|---|---|
| 02m | P1–3 | Questions, noon/reference clock and obstacle |
| 02m | P4–6 | Carpenter, H4, Madeira and second trial |
| 02m | P7–8 | Repeatability condition and K1 voyage |
| 02m | P9–10 | Compensation and proof |
| 05m | P1–4 | Captain question, compass/noon, rolling ship |
| 05m | P5–7 | Reward, headlands, H2/H3 dead end |
| 05m | P8–10 | Jefferys watch, H4 and Madeira |
| 05m | P11–15 | Second trial, payment dispute and test |
| 05m | P16–20 | K1 voyage, compensation, cost and close |
| 10m | P1–3 | Questions, context, real H1 correction |
| 10m | P4–9 | Mechanism, earlier work, trial context |
| 10m | P10–14 | Funding, failed clocks, H4 and Madeira |
| 10m | P15–20 | Public dispute, lunar method, Barbados and new law |
| 10m | P21–24 | H4 test, identifiable copy, expedition and compensation |
| 10m | P25–28 | Rate limitation, direct course and result |
| 10m | P29–30 | Cost and return to first voyage |

| 10m paired span | Visual intent |
|---|---|
| P1 | Opening questions, watch and sea. |
| P2 | Hypothetical coastal navigation. |
| P3 | H1 correction; distinct headlands, no invented rescue. |
| P4 | Noon and reference clock; illustrative example. |
| P5 | Two-minute hypothetical error, equator only. |
| P6 | Flashback to land clock and workshop. |
| P7 | Halley refers Harrison to Graham. |
| P8 | H1 opposed balances. |
| P9 | Trial context and ship transfer, no replay of hook. |
| P10 | Funding and promise. |
| P11 | H2 flaw, H3 long effort. |
| P12 | Jefferys small watch. |
| P13 | H4 and fast balance; authentic object geometry. |
| P14 | William's Madeira prediction and captain's request. |
| P15 | Press and astronomy; no fabricated headlines. |
| P16 | Lunar observations and tables; distinct from Jupiter method. |
| P17 | Barbados independent reference. |
| P18 | Accuracy threshold met. |
| P19 | Two-stage payment. |
| P20 | Dispute and new act. |
| P21 | Sealed box and Greenwich test; no sabotage implication. |
| P22 | K1 and H4 comparison; exact inscription reference required. |
| P23 | K1 voyage and cost. |
| P24 | H5 and parliamentary compensation. |
| P25 | Wales observations; old-rate conditional calculation. |
| P26 | Compare old versus recent rate; not perfect accuracy. |
| P27 | Direct course and documented landfall. |
| P28 | Actual comparison of longitude differences; not overall voyage error. |
| P29 | Later designs; no invented price trajectory. |
| P30 | Payoff H1 to K1; no exclusive watch-only claim. |

No independent session or runtime registration available. Detailed storyboard deferred; no prior storyboard asserted reusable. Recommendation is not approval.
