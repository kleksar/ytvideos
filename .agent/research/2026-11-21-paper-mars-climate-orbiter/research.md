# Research — Mars Climate Orbiter, 1999

**Observed / source access:** 2026-11-21. **Channel:** Paper Detour, English narration. **Choice:** the *failure of several checks after a small-unit interface error*, not a generic "NASA confused miles and kilometres" anecdote. Selected before full scripts. Audience hypothesis: non-specialists who are curious how a perfectly ordinary file can destroy a spacecraft even after the team notices discrepancies. This is editorial judgement, not measured demand.

## Selection: coverage and duplicate filter

Eleven distinct stories considered, not eleven variants of the winner. The full GitHub open/closed PR listing was checked 2026-11-21. This round intentionally excluded already proposed stories rather than reopening or competing against them:
1. Mars Climate Orbiter (1999), units and missed warnings — **finalist**; no matching story PR found by GitHub search for name/mission/metric/imperial.
2. Apollo 12 (1969), double lightning strike, John Aaron and SCE-to-AUX — **finalist**; separate from already accepted Apollo 13 #46.
3. Strasbourg dancing events (1518) and legend versus surviving documentation — **finalist**, but reliable proof of the familiar "danced to death" payoff is lacking.
4. The 1904 Olympic marathon — existing Paper PR #47, duplicate.
5. Alcatraz escape (1962) — existing Nuviko PR #177, duplicate/adjacent.
6. Vasa's maiden voyage and recovery — existing Paper PR #139, duplicate.
7. The McDonald's Monopoly prize conspiracy — existing Paper PR, duplicate.
8. Henry Box Brown's 1849 journey by mail — existing Paper PR #32, duplicate.
9. Cleveland Balloonfest (1986) — existing Paper PR, duplicate.
10. Boston molasses flood (1919) — existing Paper PR #129, duplicate.
11. Boston Mooninite public-art panic (2007) — existing Paper PR #114, duplicate.

These eight excluded examples are genuine competing audience propositions but *not* fresh available story slots. Other searched collisions included the 1986 maple syrup heist (#19), Great Emu War (#314), and the 1984 Michael Larson game show (#330). Owner-rejected #13 telegraph and #88 canal-bridge angle were not revived. Accepted Lawnchair Larry #25 and Apollo 13 #46 were not proposed. Selection means 3 viable finalist *concepts* after duplicate filtering; the documentary evidentiary weakness is counted against the dancing story.

## Three finalist pitches — equal treatment

| Candidate | Exact opening / first image | After the hook — genuine development | Complete payoff | Strongest objection |
|---|---|---|---|---|
| Mars Climate Orbiter | "A NASA spacecraft went behind Mars exactly as planned. Twenty minutes later, it still hadn't come back." Paper Mars / silent antenna | Oddly frequent attitude-control thruster firings; pound-force-seconds passed as newton-seconds; Doppler inconsistencies; unready last manoeuvre; 49-second early signal loss | NASA's 1999 investigation identified a factor-4.45 interface mismatch *and* organizational/software verification failures; reconstructed 57 km vs intended 226 km; precise fate unobserved | Famously retold "imperial versus metric" disaster, low novelty, and recent small-channel examples have weak views |
| Apollo 12 lightning | "Twice in the first minute, lightning struck a rocket carrying three astronauts." Paper launchpad in rain | Power and instrument readings disrupted; ground engineer suggests SCE to AUX, Alan Bean finds switch; confirm navigation/flight can continue | Apollo 12 still reaches the Moon after diagnosis, not automatically a mission abort | More naturally cinematic human rescue; NASA/APOLLO adjacent stories already in queue; finding a novel five- and ten-minute Paper angle without repeating a common Apollo highlight is a challenge |
| Strasbourg dance accounts | "People gathered to watch neighbours who could not seem to stop dancing." Period street, no invented deaths on screen | City response, competing accounts and uncertain historical evidence, question how later writers amplified events | Clear distinction between established 1518 records and later embellished claims, *not* an invented death toll | Popular promise "they danced themselves to death" cannot be made responsibly without a contemporary primary source; ten-minute conflict would risk speculative filling |

**Closest competitor:** Apollo 12. It has a clearer person making an identifiable decision, and may be preferable for a tense rescue channel. Mars wins *this* Paper Detour proposal because its consequences travel across three understandable objects/actions (one solar panel → file units → signal disappearing), the primary mishap investigation provides a complete and unusually concrete multi-stage account, and the central twist is that the wrong unit survived warnings and last-course-correction opportunities. This is not proof it will outperform Apollo 12, and the familiarity of metric/imperial makes it vulnerable to swipe-away.

**Reject condition:** if a cold viewer says that the result is fully explained by the phrase "they mixed units", the five-minute script adds insufficient value; the NASA report's unresolved tracking discrepancy and TCM-5 paragraph must be demonstrably understandable.

## Primary fact chain, chronology, uncertainty

Primary document: NASA, **Mars Climate Orbiter Mishap Investigation Board, Phase I Report**, issued 1999-11-10; PDF https://discovery.larc.nasa.gov/pdf_files/MCO_report_2.pdf . The report was opened and its actual PDF pages were visually inspected, including PDF 0-index pages 5, 12, 15, 18 (printed pages approximately 6, 13, 16, 19). The exact dates of events are **1998–1999**, not the document's later crawl time.

1. NASA's orbiter launched **1998-12-11** to study Martian climate and relay data from Mars Polar Lander. Source: https://science.nasa.gov/mission/mars-climate-orbiter/ and NASA report background.
2. Asymmetric solar array exposed attitude control to solar radiation pressure; angular momentum desaturation firings occurred **10–14 times as often** as navigation team expected, producing unmodelled small pushes. Source: report narrative "Root Cause" and tracking navigation, printed pp. 6–7; this is not a dramatic onboard malfunction.
3. Ground small-force file for navigation supplied impulse values in **lbf·s**, specified in **N·s**. 1 lbf = about 4.45 N; navigation underestimated accumulated impact of thruster pulses. Source: report "Root Cause" (pp. 6–7) and unit-interface analysis (~p. 16). **Do not say** spacecraft's onboard computer itself switched to miles or that this was kilometres-versus-miles.
4. Unresolved tracking-prediction discrepancies reported during spring/summer; one solution using Doppler data suggested lower Mars approach than combined solution. Source: report mission and navigation reconstruction pp. 12–14. Avoid invented private dialogue or claims that a particular engineer knowingly ignored guaranteed proof.
5. TCM-4 calculated **1999-09-08** and **executed 1999-09-15**. Planned first periapsis approximately **226 km**; later estimates **150–170 km**, then **110 km** near final approach. Estimated minimum survivable **80 km**. Source report pp. 12–13. Do not mistake the *initial September 23 press estimate* of planned 150 km for the *pre-TCM-4 reconstruction target* of 226 km; different context and time.
6. Contingency TCM-5 was verbally discussed but not performed due to missing analysis/tests/procedures/time. Source: report contributing causes (~p. 19). There is no documented dramatic decision to sacrifice probe for fuel or save money.
7. Engine fired **1999-09-23 09:00:46 UTC**; signal disappeared **49 seconds earlier** than predicted; none returned despite attempts through **1999-09-25**. Source: report chronology p. 13 and contemporaneous NASA statement https://nssdc.gsfc.nasa.gov/planetary/news/mco_19990923.html .
8. Unit mismatch found **1999-09-29**. Corrected reconstruction ≈**57 km**, below estimated survivability. Exact final fate **not observed**: probable atmospheric destruction or possible escape into heliocentric orbit. Source: report findings, also NASA preliminary release on 1999-09-30: https://www.jpl.nasa.gov/news/mars-climate-orbiter-team-finds-likely-cause-of-loss/ . Do not assert a witnessed crash, explosion or final transmission.
9. Root cause is not the whole lesson; board listed missing interface verification, communication/training/staffing and contingency readiness. Source: report contributing causes and recommendations. Do not narrate an unverified emotional reaction, words or motive.

**A causal chain supported by sources:** solar-panel asymmetry → repeated desaturation thruster pulses → recorded small-force data passed between groups → mismatch of data units → navigation model underestimated effect → discrepancies did not trigger adequate correction → lower than planned Mars passage → no contact. The report documents both root and contributing causes; it does not establish any single person's unobserved intentions.

## Demand and competing videos: publicly observed signals only

**Observation date 2026-11-21.** All rows are metadata from public video pages/search results or the attributed institutional mirror; **no video was played**, and no comments or private analytics were accessible. Distinguish a metadata listing from a watched transcript. Publication dates and counts below are snapshots, not guaranteed canonical real-time counts.

| Public match / URL | Published, language, format / duration | Public views at source observation | Comparable signal and limitation |
|---|---|---:|---|
| National Air and Space Museum, "The Mars Metric Mistake" https://www.youtube.com/watch?v=4DXFurrTM_g ; Smithsonian page https://www.si.edu/object/mars-metric-mistake%3Ayt_4DXFurrTM_g | 2025-04-28 reported, EN, brief educational clip, duration not independently confirmed | **10,425** on institutional mirror's indexed snapshot | Reputable explanation but established institution and education audience are not Paper narrative baseline |
| Sixty Second Sense, "How a Simple Unit Error Destroyed a Mars Probe" https://www.youtube.com/watch?v=IsrznyQirt0 | 2025-08-04 reported, EN, ~60s Short from metadata | **4,483** in public search snapshot | More comparable small creator, but different length, style and age |
| SnapClips, "Mars Orbiter FAILURE: Metric vs. Imperial Units! #shorts" https://www.youtube.com/watch?v=lL8Lls9kYC0 | 2026-01-22, EN, Short; actual duration UNVERIFIED | **3,798** in public listing | 2026 evergreen example, January not a 30–90d fresh signal |
| DatabaseHistory, "The Mars Climate Orbiter: How a Simple Imperial-to-Metric Data Error Destroyed a $125M Mission" https://www.youtube.com/watch?v=I_-NUCxGiOI | 2026-09-09, EN, format/duration UNVERIFIED | **83** at search index's two-month snapshot | Within 90 days before observation; weak recent signal, but age and exposure unknown. Not evidence of flat growth or retention |

**Baseline:** no dependable ordinary-result sample for these *same authors*, of comparable age, format, channel size and video length, could be obtained. The four matches therefore establish that the topic has been covered, **not** relative outperformance. Mixed-format view counts and views/age are NOT CTR/retention/recommendations or proof of current demand. Strong recent counter-signal is the small September 2026 example with only 83 public views at its indexed date. Public comments, actual transcript comparison, creator baseline and Paper Detour channel analytics **UNVERIFIED**. No paid vidIQ credit used. Do not copy scripts or images.

**Apollo 12 alternative source check:** NASA https://science.nasa.gov/resource/lightning-strikes-twice/ and https://www.nasa.gov/history/55-years-ago-apollo-12-makes-a-pinpoint-landing-on-the-moon/ document two lightning strikes and the switch that restored telemetry. Comparable YouTube public videos include VideoFromSpace https://www.youtube.com/watch?v=5GJhtyI2Fj0 (2019, EN, ≈35,382 views indexed) and https://www.youtube.com/watch?v=ajOsHVK11Lw (2010, EN, ≈98,493 indexed). Neither provides channel baseline or a verified current 30–90-day result; nearby Apollo 13 production #46 creates a queue diversity concern but does not forbid Apollo 12.

**Strasbourg alternative:** https://www.history.com/articles/what-was-the-dancing-plague-of-1518 (popular account; use caution), https://mostlyunexplained.com/shorts/dancing-plague-they-couldnt-stop/ (2026-10-16 critical caveats). YouTube public listings https://www.youtube.com/watch?v=m_9Odp9rdCY and https://www.youtube.com/watch?v=Ia3rUoqmyGY offer 2026 coverage, but no comparable author baseline and the often-told mass-deaths story cannot be confidently used as documentarily verified payoff.

## Promise, steps and audience decision

**Promise:** how a spacecraft could function normally, reach its destination and still be lost because the teams' data contract was violated and warning signals went unresolved. **Cold open:** a paper Mars and silent signal, immediately followed by real hardware and action rather than an abstract formula. **After hook:** thruster corrections; units in two connected files; conflicting trajectories; missed TCM-5; final occultation. **Payoff:** 57 km vs 226 km and official finding that a simple mismatch *should have been caught*. **Strongest objection:** familiar metric/imperial meme, possible repetitive explanation if technical exposition overwhelms causality.

This is a **testable experimental evergreen hypothesis** with unverified current demand. No supplied channel-retention, impressions, or comments are represented as evidence.

**Editorial confidence:** high in official event chronology and root cause; medium in audience interest and how accessible deep navigation material will feel to Paper Detour listeners; low in any claim about relative video performance.
