# Exact story review — editor only · 2026-11-19

**All six scripts have been written as standalone full narratives.** This file is **author self-review**, not independent `ytv-script-review-v1`. Editorial 1–10 scores are judgments **about exact text**; not measured viewer retention, view probability or CTR. 8 dimensions in order: **I** interest/significance, **H** opening, **D** causal development/reason to stay, **P** payoff, **F** freshness of angle, **V** visualization, **N** natural narration/clarity, **S** audience-demand proof. `UNVERIFIED` is never silently converted to zero or eight.

| Exact draft | UTF-8 bytes SHA-256 | Words, scope, estimates | I | H | D | P | F | V | N | S | Working classification |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| [02 EN](variants/02m/script.en.txt) | `ecc0ad20789002f906b9cedea75e54b12b9eef5643cee05aa3b23e1ef5880136` | 272 words; 1.8–2.3 min @125–155 wpm and pauses, Short | 8 | 8 | 8 | 8 | 6 | 9 | 8 | UNVERIFIED | REWORK |
| [02 RU](variants/02m/script.ru.txt) | `271f030fbdbdc0a6a2dd8131eb63ed87393293fded97c45df469b1b70e53364e` | 237 words; full translation; estimates not voice timings | 8 | 8 | 8 | 8 | 6 | 9 | 8 | UNVERIFIED | REWORK |
| [05 EN](variants/05m/script.en.txt) | `f92d007b5225b0780e9083b3c805615309b2ce225b73076a00aead7e40de21e0` | 720 words; ~4.8–5.7 min @130–150 wpm with natural pauses, Long | 9 | 9 | 9 | 9 | 7 | 9 | 8 | UNVERIFIED | **STRONG_CANDIDATE — recommended** |
| [05 RU](variants/05m/script.ru.txt) | `9aec593d9fdf900c6de8960c3408e27af95212b88955b8eaec80eab34b0437df` | 617 words; full translation | 9 | 9 | 9 | 9 | 7 | 9 | 8 | UNVERIFIED | STRONG_CANDIDATE |
| [10 EN](variants/10m/script.en.txt) | `71c9582aa2309d8758fdb4f4ae3edee01a981096f47829dfb2830bde2aa7efbb` | 1,220 words; ~9–11 min @115–135 wpm incl pauses, Long | 9 | 8 | 8 | 8 | 6 | 9 | 8 | UNVERIFIED | REWORK |
| [10 RU](variants/10m/script.ru.txt) | `1d098204e92dc71f974b9dd0b3f6e56e88fd17ca18403dd8186454f53884c7be` | 998 words; full translation | 9 | 8 | 8 | 8 | 6 | 9 | 8 | UNVERIFIED | REWORK |

Hashes are local pure-JS SHA-256 of fetched exact Git blob UTF-8 text, checked against the known `abc` test vector. **Not** recorded TTS timing. Even at 9–10 minutes the tempo is not guaranteed before actual Lawrence voice test.

## Why each dimension got its score, for each exact language text

| Draft | I / H / D / P — concrete textual evidence | F / V / N — specific evidence, chief defect, confidence |
| --- | --- | --- |
| 02 EN | I8: 32 dead and stranded lifeboats; H8: `A cruise ship was lying on its side`; D8: route → rock → power → shore report → late evacuation; P8: closing visual contrast. | F6: heavily covered Netflix topic; V9: paper ship at 65°; N8: accessible `launch`/rope action. **Defect:** `Look at the Costa Concordia...` merely restarts opening; loop author FAIL. Confidence moderate. |
| 02 RU | I8: `Погибли 32 человека`; H8: `Круизный лайнер лежал на боку`; D8: удар → запоздалый приказ → невозможность спуска; P8: `Спасательные шлюпки были прямо там`. | F6: знакомая катастрофа; V9: образ лайнера у острова; N8: обычная речь, но `Приветственный проход` требует контекста. **Defect:** `Посмотрите ещё раз` не образует честной естественной петли. Confidence moderate. |
| 05 EN | I9: understandable human/escape stakes; H9: three distinct questions; D9: new fact from shore call after first explanatory announcement, then angle prevents launches; P9: `The lifeboats were there...`. | F7: specific delay/lifeboat physical angle against saturated captain angle; V9: visible lifeboats and 19-hour rotation; N8: readable action sequence, `parbuckling` explained only with next context. **Defect:** engineering passage may feel like second story after victim count. Confidence moderate. |
| 05 RU | I9: судьба пассажиров; H9: `почему береговая охрана узнала через тех, кто на суше`; D9: сообщение семье → берег → задержка → крен; P9: `время ... уже прошло`. | F7: причинное, а не биографическое, объяснение; V9: наклон корпуса/шлюпки; N8: простой связный русский; сложный `парба́клинг` представлен сразу с объяснением. **Defect:** финальный абзац суда может задерживать развязку. Confidence moderate. |
| 10 EN | I9: large human cost and second engineering struggle; H8: clear questions but more reading before decisive hit; D8: well-supported 22:06/22:54 and parbuckling mechanisms; P8: equipment lost opportunity. | F6: already covered by Netflix; V9: paper model with hull and ballast supports; N8: smooth explanatory syntax. **Defect:** middle-to-late salvage can dominate the evacuation question; 10min value not certain. Confidence low–moderate. |
| 10 RU | I9: человеческая катастрофа и поиск погибших; H8: три вопроса; D8: временная последовательность + восстановление; P8: `возможность использовать их может исчезнуть`. | F6: нет подтверждённого нового угла для длинной версии; V9: парбаклинг; N8: доступная, без стилистических обрывков речь. **Defect:** после развязки долго идёт технология удаления; риск снижения интереса. Confidence low–moderate. |

Each row contains the eight evaluations with specific examples above. **Author** = this writing agent, not an independent reviewer. Confidence is in editorial diagnosis, not future performance. No fabricated reviewer, ratings, listening, video play or comments.

## Scope and separate gates

| Check | 02 | 05 | 10 | Evidence/limit |
| --- | --- | --- | --- | --- |
| Factual assertions | PASS — author/source only | PASS — author/source only | PASS — author/source only | Italian Civil Protection timeline, documented investigation, 2017 court report, caveats in research; independent fact check UNVERIFIED |
| EN/RU semantic equivalence | PASS — author compare | PASS — author compare | PASS — author compare | same main events/claims/caveats; 02/05/10 own complete story, not same master fragments |
| ChannelSpec production format | PASS for Short length target pending TTS | PASS for Long 16:9 | PASS for Long 16:9 | actual recorded duration UNVERIFIED, recipe `illustrated` |
| Rights/image references | UNVERIFIED | UNVERIFIED | UNVERIFIED | no historical footage/media bytes, no archive rights confirmed |
| Narrative loop | FAIL — thematic repeat, not clear last→first | N_A — Long | N_A — Long | 02 EN/RU cold open works but last `Look again` is not seamless; no AV seam |
| Independent review | UNVERIFIED | UNVERIFIED | UNVERIFIED | no separate reviewer input or native result; self-review does not count |
| Runtime/start/official script gate | UNVERIFIED / BLOCKED | UNVERIFIED / BLOCKED | UNVERIFIED / BLOCKED | `ytv` executable absent; no run/lease/receipt/approval |

**Author revisions:** 05m underwent one substantive additional pass to clarify lower-compartment reports, shore contact chronology, and lifeboat mechanism (from 561 EN/460 RU to exact final 720 EN/617 RU); 02m and 10m one author full draft each. At most two editorial passes were allowed; no artificial upward scoring. No independent pass was attempted or impersonated.

## Added value and recommendation

- **02→05:** visible paradox becomes a genuinely causal chain: 21:45 crash, lower compartment reports, shore/police contact 22:06, public abandon 22:54, geometry of launching mechanisms, island rescue, 19-hour righting, legal outcome. More complete and substantive, not filler.
- **05→10:** details on two simultaneous information lines, survivor movement through slanted decks, longer offshore salvage stages and 2014 last victim. All cited but the legal/salvage tail shifts attention away from the principal evacuation paradox. **10m REWORK**; no assumption that longer equals better.
- **Recommend exact 05 EN text** (`f92d007b…21e0`) for an editorial Long. This is an author's proposal only; not a user's choice, runtime master, independent reviewer pass or TTS approval. Significant doubts: Netflix 2026 and no comparable fresh search metrics. For 02m, a true complete repeat loop must be rewritten and then freshly reviewed before any Short production.
