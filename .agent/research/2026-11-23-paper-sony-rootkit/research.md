# Paper Detour — Sony BMG's hidden CD software (research)

Research read/observed: **2026-11-23 UTC**. This is an independently authored **editorial hypothesis**, not an approved production or measured audience forecast. All external query terms were public, generic and contained no private repository details.

## Selection: 12 distinct stories screened, three finalists

| Concrete story | Potential reason to watch | Decision / strongest drawback |
|---|---|---|
| Sony BMG copy-protected CDs, 2005 | A store-bought album installed software that hid in Windows; even removal tools introduced security holes | **SELECT**: relatable computer ownership conflict with verified technical and legal reversals |
| Max Headroom signal intrusion, Chicago 1987 | One masked pirate appeared on two TV broadcasts; first stopped, second continued | **FINALIST**: extraordinary visuals, but the identity remains unknown and the ending risks being anticlimactic; primary analog footage rights unverified |
| BBC spaghetti-tree April Fools' broadcast, 1957 | A television item presented spaghetti growing on trees; viewers asked how to grow it | **FINALIST**: delightful visual payoff, but sparse new verified development for 10 minutes, high risk of padding |
| Hitler diaries forged and authenticated (1983) | Newspapers and experts confronted forged historical documents | Long paper trail; not studied enough this round to claim verified winner |
| Mona Lisa stolen from the Louvre (1911) | Missing painting, suspect investigation and recovery | Known evergreen subject; deeper source comparison not funded this round |
| 2007 Boston Mooninite LED advertising panic | City mistook an illuminated cartoon promotion for threats | Duplicate: existing PR #114 |
| 1990 Gardner Museum theft | Two people impersonating police stole works still missing | Duplicate: existing PR #172 |
| McDonald's Monopoly rigging | Security insider controlled high-value prizes | Duplicate: existing PR #100 |
| Pepsi Number Fever 349 | Winning-number promotion led to disputed prize expectations | Duplicate: existing PR #102 |
| Cleveland Balloonfest 1986 | Mass balloon launch created problems after release | Duplicate: PR #67 |
| Caltech cannon transported to MIT | Students used mover paperwork to take the cannon | Duplicate: PR #366 |
| Pepsi Harrier jet promotion | A prize advertisement became litigation | Duplicate: PR #51 |

The selection is **not** 12 thoroughly researched finalists. There were 12 distinct screened stories, 3 substantive finalists; the duplicate list is explicitly rejected without repackaging. Additional GitHub all-state searches for “Sony rootkit”, “rootkit CD”, “2005 CDs”, “Max Headroom”, “Spaghetti trees” did not reveal an exact story PR at observation time. Privately scheduled/non-indexed YouTube episodes: **UNVERIFIED**.

### Three competing one-paragraph pitches (similar scrutiny)

**Sony (selected).** First line for 2m: “A music CD from a store could hide software on your Windows computer.” Follow-on: Russinovich uses his rootkit detector → XCP hides more than its own files → researchers uncover pre-consent MediaMax installation → Sony's uninstallers introduce their own vulnerability → recall/FTC conditions. Payoff: the purchased music item could transfer control of a customer's computer. Objection: technical subject could become jargon-heavy and there is already substantial coverage. Counter: tangible CD, missing file and a failed remedy give causal steps; tell the human-machine control story, not a kernel tutorial.

**Max Headroom (runner-up).** Proposed opening: “Someone replaced the evening news with a man in a plastic TV mask. They did it again the same night.” Development: WGN interruption → engineers restore signal → WTTW interruption continued until intruder stopped → investigation without identified perpetrators. Payoff: analog broadcast links were vulnerable to stronger competing signals. Objection: culprit unknown, so a mystery may promise an identification it cannot deliver; archival footage rights uncertain. Background: [Ars Technica, Sean Gallagher, 2017-11-22](https://arstechnica.com/information-technology/2017/11/thirty-years-later-max-headroom-tv-pirate-remains-at-large/).

**Spaghetti trees (runner-up).** Proposed opening: “A BBC programme showed spaghetti hanging from branches. People asked where to plant it.” Development: crafted fake footage → authoritative TV presentation → viewer inquiries → admission of April Fools' trick. Payoff: the perceived reliability of television gave a planted absurdity credibility. Objection: the trick's answer is immediately evident to many modern viewers; stretching it to ten minutes without repetition would be unjustified. [Ars Technica retrospective](https://arstechnica.com/gaming/2020/04/that-time-the-bbc-fooled-its-audience-into-thinking-spaghetti-grew-on-trees/), further archive authentication not completed.

**Why Sony beats Max:** a second verified surprise (unsafe removal) and a documented remedy give Sony a specific resolution rather than an unidentified perpetrator. **Why Sony beats spaghetti:** meaningful new mechanisms and consequences support five minutes without speculating about participants' thoughts. **Strongest case against Sony:** DRM explanations can eclipse the everyday tension; avoid broad security generalizations and explicitly keep XCP and MediaMax separate.

## Primary and near-primary fact register

All links below were opened/read, not treated as mere search snippets.

1. **J. Alex Halderman and Edward W. Felten, “Lessons from the Sony CD DRM Episode,” USENIX Security Symposium 2006.** [Paper](https://www.usenix.org/legacy/event/sec06/tech/full_papers/halderman/halderman_html/index.html). Sections 1–3: October 31 Russinovich discovery, two different products/vendor names, millions of CDs, PC installation mechanics. Sections 4 and 7: consent flaws, XCP concealment and third-party malware abuse. Section 8: uninstall vulnerabilities for **both** systems. Conclusion: additional security/privacy burdens with ineffective copy protection. **Use**: main technical authority for all six versions. **Limit**: historical assessment, not contemporary security advice.
2. **Mark Russinovich, “Inside Sony's rootkit,” Virus Bulletin, 2005-12-01.** [First-person technical account](https://www.virusbulletin.com/virusbulletin/2005/12/inside-sony-s-rootkit). Introduction: RootkitRevealer test, hidden registry/files, album *Get Right With the Man* by Van Zant, EULA accepted for XCP. “System call hooking”: driver operation. **Use**: agency and chronology; crucial qualifier: do **not** falsely say XCP never presented an EULA.
3. **US Federal Trade Commission, “Sony BMG Settles FTC Charges,” 2007-01-30.** [Official FTC release](https://www.ftc.gov/news-events/news/press-releases/2007/01/sony-bmg-settles-ftc-charges). Allegations: undisclosed limits/security risks, uninstall difficulty, listening data/marketing. Proposed terms: prominent disclosure, consent, exchange, removal, up to $150 reimbursement to eligible buyers for directly caused damage. **Caveat**: settlement proposal, NOT judicial admission of violations; FTC webpage contains an internally impossible “June 31” deadline, not repeated.
4. **Washington State Attorney General, 2006-12-20.** [Official multi-state settlement notice](https://www.atg.wa.gov/news/news-releases/mckenna-announces-4-million-settlement-and-consumer-refunds-sony-bmg-music-case). Distinguishes MediaMax installation despite refusal and separate 2006 state actions. **Use**: 10m legal chronology; do not conflate with FTC settlement.
5. **Electronic Frontier Foundation, Sony BMG litigation archive.** [EFF chronology](https://w2.eff.org/IP/DRM/Sony-BMG/). Advocacy participant, not neutral evaluation; corroborates timeline, exchange demands, company initial statements. Do not treat advocacy opinion as uncontroversial fact.

**Precision exclusions:** avoid exact number of affected buyers or installations; publications report different counts for shipped CDs vs protected titles vs actual PC installs. No invented number of infections or privacy events. Avoid implying all CDs, operating systems or DRM versions behaved alike. When saying “malware could hide,” distinguish demonstrated ability from proof of any specific infection. The paper documents uninstall vulnerabilities; narration does not claim a named customer was actually attacked. Do not place a security tutorial demonstrating malicious exploitation in visuals.

## Viewer-interest observations (not proof of demand)

Date observed **2026-11-23**. Public YouTube search index only. YouTube watch pages failed to open (disabled/error), so **no actual video, transcript or comments watched/read**. All durations except a title-level claim remain UNVERIFIED; views are snapshots with unknown collection lag. Baselines against other videos from the *same* creators in matched formats/age could not be established.

| URL/ID | Author / language | Publish date | Public index observation | Fit / limitation |
|---|---|---|---|---|
| [MShnfhacCZ4](https://www.youtube.com/watch?v=MShnfhacCZ4) | HiFi Review HUB, English title | 2026-05-04 | 1,232 views, 40 likes; title claims “Under 3 Minutes” | Near-short history, actual runtime unverified |
| [0X9OMwiezA0](https://www.youtube.com/watch?v=0X9OMwiezA0) | Xataka, Spanish | 2025-05-29 | 7,132 views, 333 likes (search index) | Cross-language technology explainer; runtime unverified |
| [Qp4KjFILdus](https://www.youtube.com/watch?v=Qp4KjFILdus) | Matthew Flatt, English | 2025-04-05 | 82 views, 976 followers | Lecture category; low comparability to narrative paper video |
| [imMRzBzQm1U](https://www.youtube.com/watch?v=imMRzBzQm1U) | Today I Found Out, English | 2022-04-06 (secondary video listing; metadata unverified) | Views UNVERIFIED | Evergreen established explainer; cannot treat channel-size outlier as success |

Counter-signals: modest indexed engagement for the shortest comparable and lecture, language/genre mismatch, known creator/format differences. **No verified last-30–90-day growth signal**; existing attention is primarily evergreen. No Paper Detour private YouTube Studio analytics, impressions, CTR, retention, stayed-to-watch or traffic-source breakdown supplied. Demand for **Paper Detour's paper diorama presentation** is a testable hypothesis, **UNVERIFIED**, not a scored 8/10.

## Honest promise and narrative map

Audience: English-speaking viewers interested in unusual real-world technological mishaps; no operating-system expertise assumed. Promise: “How did a store-bought CD hide risky software, and how did even the fix backfire?” Visible first confirmation: familiar CD case inserted into Windows-era computer; paper-diorama depiction labeled as stylization, not archival footage. Major escalation: XCP hides files/processes, MediaMax installs parts despite declined agreement; uninstallers expose new risks. Full payoff: recall plus consent/removal obligations, and shift from **copying music** to **ownership of the computer**.

**2m:** one immediate object → Russinovich discovery → two mechanisms → defective remover → settlement; full answer, textual loop “Sometimes it was” → “A music CD…” is **grammatically broken** on literal concatenation; the 2m is full but **REWORK** for Short loop; AV seam UNVERIFIED.

**5m (recommended):** questions → ordinary CD purchase → XCP discovery → concealment mechanism → MediaMax consent → uninstall reversal → recall/FTC; more real narrative context and two independently sourced reversals. No forced loop (Long).

**10m:** questions → period-specific purchase model → autorun and media delivery → Russinovich detector → XCP generalized hidden filename mechanism → MediaMax pre-EULA installation and listening-data concerns → technical/uninstaller failure → security/consumer reactions → state and federal settlements → why DRM did not justify the risk. Full documentary resolution, though legal follow-up may dilute narrative momentum.

## Research limitations / rights

- Original retail packaging, company logos, CD artwork, historic screenshots, Russinovich's blog figures, and archival TV/YouTube stills are **NOT cleared for reproduction**. Research URLs are not media licenses or actual asset bytes.
- Brand-approved paper reference bytes and paper-plane reference media are not available in this GitHub text-only execution; confirm actual assets and rights before any scene production.
- No actual timed narration/TTS, no verified 5/10-minute spoken duration, no MP4 or two-cycle AV seam.
