# Exact-text editorial comparison

Author: writing agent (not independent reviewer). Date 2026-11-28; confidence medium on storytelling, high on NPS-supported dated events, low on relative demand. One authored pass followed by explicit fact-boundary, language and structure read-through; no generated audio. Exact files, UTF-8 LF including final newline.

| Variant/lang | Words (whitespace tokens) | SHA-256 |
|---|---:|---|
| 02m/en | 302 | `376747be99a22d6a4f964f0136f6dfdef97c212d80c05bb001450880b136c266` |
| 02m/ru | 250 | `a80690f7f589558e52f86172f7065131b8d71d6bebd48d9a615f64476587ff89` |
| 05m/en | 763 | `e3356bef3756d60aa9d5ce8d920d496ae773f79616c436909830c4d9eba1dd71` |
| 05m/ru | 590 | `6c18009c280d69fa5e5488138c3f96e9ff76931511f7e8f20cdcb66fd8bf63dc` |
| 10m/en | 1526 | `357ce7ba1038e8632485fa8592dfc6a97d375e5e9990fafe3ec823a5955d3324` |
| 10m/ru | 1253 | `31175bba6377d893b52c5c589fce041c07dfd0988c8abaf3c7afc4fff0c87388` |

Assumed effective English delivered pace 130–150 words/min (not measured for Lawrence 1.1x), plus meaningful pauses, Long endscreen 10s and unknown exact intro bridge. Narration alone estimates 2.01–2.32 min, 5.09–5.87 min, 10.17–11.74 min. Actual duration UNVERIFIED; preserve speed, not force fit. RU editorial translation, not separate timing master.

| Criterion | 2m | 5m | 10m |
|---|---|---|---|
| Interest/significance | 8 — "voice faded during an hour of play" makes a concrete product failure | 9 — the one-hour failure against individually produced voices has a relatable consumer stake | 8 — concrete failure at paragraph 5; the earlier technical trials now explain it |
| Beginning | 9 — a return and hour immediately create a problem | 8 — questions then torso reveal and how it works, concrete hook at investor warning and returns | 9 — questions, object and consumer promise lead to actual return by paragraph 5 |
| Development | 8 — factory → returns → failed revision → bent ring | 9 — supplier order, pre-release warning, actual returns, attempted financing and recovery escalate | 9 — Paris repairs, train damage, recording recruitment, attempted repair and archive provenance add distinct consequences; recording recruitment can slow pace |
| Payoff | 9 — "a woman's voice reciting Twinkle, Twinkle, Little Star" followed by clear earlier-artifact caveat | 9 — "It had recovered an earlier human performance" answers third question, and final line closes consumer contrast | 9 — digital recovery plus actual 1984 playback distinguish two kinds of historical evidence |
| Freshness of angle | 8 — focus on the product's reliability, not generic spooky doll | 9 — verified pre-launch warning/financial failure contrasted with later preservation | 9 — named evidence from technical failures and actual playback offers a less familiar angle |
| Visual expressivity | 8 — crank, open torso, ring and scan are distinct physical states | 9 — assembly, retailer returns, model approval and scanner add visible consequence | 9 — train journey, damaged wax, recording booths, repair request, curator and cassette create distinct visual events |
| Spoken naturalness/clarity | 8 — ordinary verbs, one dense sentence at the end | 8 — customer complaint and plain finale; "causing a thin diaphragm to vibrate" needs clear visual support | 8 — concrete actions anchor explanations; p10–13 still contain manufacturing context |
| Verified audience demand | UNVERIFIED — indexed public examples and dated Reddit question, no matched baseline | UNVERIFIED — same | UNVERIFIED — same |
| Known scores mean | 8.29 | 8.71 | 8.71 |

Maps:
- 02m: customer returns after voice fades → doll with crank, unique wax performances → multiple faults/stop → replacement not funded → separate bent prototype ring → recovered verse and contrasted lifespan. Main weakness: financing compressed, final question could feel like a restated hook. Author text loop provisional: first line "One customer sent back an Edison talking doll after its voice faded during an hour of play." Final question "What had happened to that customer's doll?" literally answered by opening. RU matching question and answer. Alternative end "The problem was the voice" rejected for thematic-only seam; alternative start "In 1890 Edison made a talking doll" rejected for slow cold start. Full EN and RU author read across two cycles: complete recovery/payoff occurs before end; opening resolves final question without dangling causality, but question is somewhat recap-like. Independent narrative seam UNVERIFIED; exact MP4 audio/visual seam UNVERIFIED.
- 05m: questions → factory and acoustic movement → separate voices and supplier order → investor warning → shop letter (rising stakes) → causes and unsold stock → revised design/debt → separate artifact/optical recovery → customer wanted tomorrow's toy. Main weakness: order figure and inventory explanation can interrupt flow; keep visuals concrete. No narrated loop for Long.
- 10m revised: questions → actual doll and value → Boston return at p5 → rewind to Paris repair and train-damaged wax → recording recruitment and unique performances → sales and multiple failures → attempted repair, debt → cataloged ring, digital scan → actual 1984 playback comparison → preserved voice and consumer contrast. Weakness: p10–13 pause to explain record manufacture and supplier scale; p16 inventory still requires a visual aid. No narrated loop for Long.

Checks by variant (author checks only, not runtime receipt):
| Check | 2m | 5m | 10m |
|---|---|---|---|
| factual support | PASS author, E1–E7 subset | PASS author, E1–E7 | PASS author, E1–E7, distinguish ordered/delivered/sold |
| EN/RU meaning | PASS author, report/sequence/uncertainty preserved | PASS author, price/quantity/date and artifact distinction preserved | PASS author, all key facts, distinctions and answers preserved |
| format compatibility | PASS ChannelSpec Short, actual length UNVERIFIED | PASS Long ChannelSpec, actual length UNVERIFIED | PASS Long ChannelSpec, actual length UNVERIFIED |
| narrative seam | UNVERIFIED independent, provisional author question→answer | N/A Long | N/A Long |
| AV seam | UNVERIFIED no MP4 | N/A Long | N/A Long |
| rights | UNVERIFIED audio/image reuse; own narration only | UNVERIFIED same | UNVERIFIED same |
| independent review | UNVERIFIED no independent session capability observed | UNVERIFIED same | UNVERIFIED same |

Recommendation: 5m. The two-minute version gives the full payoff but little room for evidence of the attempted second launch. Five minutes explains the actual buying problem, the difference between the toy and the historic recording, and closes naturally on the buyer's need. The revised 10m adds firsthand pre-launch failures, performer recruitment, a repair request and two different preservation routes. The strongest new detail is the contrast between actual 1984 mechanical playback and 2011 noncontact recovery; the recording-work/supply block at p10–13 slows the customer story. The 05m remains the recommended default because it resolves the same promise with fewer detours. 10m remains a substantive candidate with timing and independent review unverified. Scores are author editorial judgments, not CTR or retention estimates. New hash invalidates any future review. No prior owner approval. 

## Revision 2026-11-28 — 10m EN/RU only
Baseline commit `0df7f4d6f9317e561c845f29edf7157a6846747a`; exact original 10m paths `variants/10m/script.en.txt` (9eebd59dbaa917c0879b4707860a266aa95d38461dee2d369e652be31d5191fc) and `variants/10m/script.ru.txt` (57f5148badde9a00929a24113d28a49956187ba7692062ecd2fc25e28256991d). Preserved four 02m/05m files and 05m packaging bytes, including prior author assessments (no independent review to preserve). Main 7c779c4b2fd379c85166ae1b164fa53d1ea08843, #124 merged. Former 10m p18 main hook now p5 after questions and concrete immersion. New material: Paris needle repairs, train damage (attributed hypothesis), recruiting performers, San Francisco sample report, July repair letter, archival provenance and distinct 1984 mechanical playback. Removed repeated closing and generic introductory discussion. New counts 1526/1253; no measured timing. 130–150 effective English wpm plus 10s endscreen/pauses, exact length UNVERIFIED. 05m recommendation unchanged. All scores author judgments, medium confidence for narrative; high for sourced dated claims, low for demand. No owner approval in observed Git records; external production/lease inventory unavailable, no evidence of concurrent Git edits at baseline. No official runtime or independent reviewer available. Old 10m evidence not transferred to a new hash as independent review; fresh independent review required.

Exact 10m paragraph spans: each row references the full paragraph in the revised EN and RU file (not timed scenes or storyboard). Visual intent is conceptual only. 

| EN/RU span | Visual / narrative intent | Evidence |
|---|---|---|
| p1 / p1 | Questions / paper doll and ring separated by eras | E1–E7 |
| p2 / p2 | Cutaway of commercial doll and crank | E3 |
| p3 / p3 | Groove and diaphragm schematic | E3 |
| p4 / p4 | Price tag and investor letter | E3/E5 |
| p5 / p5 | Boston letter and returned parcel (hook) | E6 |
| p6 / p6 | Missouri return and freight label | E6 |
| p7 / p7 | Early foil phonograph and smaller prototype | E1 |
| p8 / p8 | Paris repair bench, no invented gestures | E8 |
| p9 / p9 | Train and close view of damaged wax, inferred rubbing labeled as hypothesis | E8 |
| p10 / p10 | Voice-to-groove cutaway | E2/E3 |
| p11 / p11 | Batchelor letter and agency reply | E9 |
| p12 / p12 | Documented recording booth illustration recreated as paper | E9 |
| p13 / p13 | German order and crates, not delivered totals | E4 |
| p14 / p14 | San Francisco sample report | E8 |
| p15 / p15 | Wax faults and crank speed, no diagnosis of Salem doll | E6 |
| p16 / p16 | Warehouse boxes and memo | E4 |
| p17 / p17 | New models and request for fifty mechanisms | E6 |
| p18 / p18 | Repair letter and workshop transfer | E10 |
| p19 / p19 | Debt and unsuccessful financing | E6 |
| p20 / p20 | Museum desk collection and catalog entry, no invented discovery scene | E11 |
| p21 / p21 | Noncontact optical scan | E7 |
| p22 / p22 | Digital waveform and separate early ring, no fake archival sound | E7/E11 |
| p23 / p23 | 1984 visitor playback and cassette recorder | E12 |
| p24 / p24 | Eight catalog records and unnamed speaker, no likeness | E7/E12 |
| p25 / p25 | Contrast returned toy and distinct ring, complete payoff before bridge | E6/E7 |

Answers: price/production p2–4, p10–13; failure p5–9 and p14–19; recovery p20–24; final consumer/preservation contrast p25. Checks: author full paired reading, source boundary check (no claim of same artifact or precise Salem diagnosis), no literal Long loop requirement, no storyboard/timing claims, rights UNVERIFIED. Independent review of all exact versions remains UNVERIFIED. 10m status REWORK → CANDIDATE_REVISED; three full versions prepared and author checked; recommended 05m, no production approval. Next: exact-head CI/read-back; then another eligible changed/Long PR.
