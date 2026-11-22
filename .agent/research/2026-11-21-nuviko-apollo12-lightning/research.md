# Nuviko History — Apollo 12: lightning in the first minute
Research observation: 2026-11-21 (Europe/Belgrade). Editorial Git-only investigation; no runtime run or provider purchase.

## Selection before the scripts

**Audience:** English-language general-history/space-curiosity viewers; no assumed knowledge of flight-control terminology. The hook is two lightning strikes during a Moon launch. The middle must **not** stop after the familiar "SCE to AUX" phrase: there are separate problems with telemetry, disconnected fuel cells, disturbed navigation, in-orbit verification, and a scientifically significant landing. Payoff: the switch did not restart a failing rocket; it restored data, allowing a team to diagnose and correct the spacecraft while a separately guided launcher flew on.

Actual first-stage coverage: **12 distinct real events/topics, not 12 confirmed finalists**. Queries checked against actual remote open and closed GitHub PR and issue search on 2026-11-21. This is not a claim of 12 fully sourced studies.

| Candidate | Distinct interest; disposition |
|---|---|
| **Apollo 12 lightning, 1969** | An unexpected electrical failure after 36.5 sec, memorable human diagnosis, clear correction and lunar payoff; **finalist** |
| **St. Francis Dam, 1928** | A dam inspected hours before its collapse; catastrophic consequences and an overlooked geological weakness; **strong finalist** |
| **General Slocum, 1904** | A fire on a passenger steamer, with inaccessible/defective lifesaving equipment; concrete series of failed precautions; **finalist** |
| SS Eastland, 1915 | Strong human stakes and comparison available, but **duplicate** Nuviko PR #306, no new PR |
| Halifax explosion and Vince Coleman, 1917 | Existing Nuviko PR #72; separate aftermath PR #150; evidence on impact of train warning requires caution |
| Lake Peigneur, 1980 | Existing Nuviko PR #24 |
| Gimli Glider, 1983 | Existing Nuviko PRs #86 and #137 |
| Sultana, 1865 | Existing Nuviko PR #343 |
| Damascus Titan II, 1980 | Existing Nuviko PR #173 |
| Palomares bomb search, 1966 | Existing Nuviko PR #155 |
| Apollo 13, 1970 | Owner-accepted work #46, protected; no new topic |
| New York blackout, 1965 | No equivalently sourced character-level development established in this pass; not promoted as a finalist |

Rejected owner angles #13 (telegraph) and #88 (bridge-before-canal) were not reconsidered. Previously approved S-5 #20 and Lawnchair Larry #25 read at exact owner-accepted B commits for speech style, not used as demand metrics.

### Three properly competing pitches

**1. Apollo 12 — selected, experimental demand hypothesis.**
Opening Short: "Lightning struck Apollo 12 just thirty-six seconds after launch." Long opening asks why the instruments failed, what John Aaron recognized, and why the crew could go on. Development: separate rocket guidance continues → three fuel cells disconnected → signal conditioning corrupts ground data → Aaron recognizes a pattern from testing → Bean selects AUX → controllers can finally diagnose and reconnect cells → orbit checks → precisely targeted lunar landing. Final payoff: the switch restored telemetry, not rocket power; rocket-triggered lightning prompted weather rule changes. **Strong objection:** the switch anecdote is already known to space fans, and a new video on the exact event was published 2026-11-19; lunar aftermath might turn a 10-minute story into a general mission summary.

**2. St. Francis Dam — strongest alternative.**
Opening: the engineer inspected a troubling leak, then the dam failed that night. Development: earlier leakage/warning, dam collapse, flood reaching the Pacific, later investigation of the unstable hillside and consequences for engineering oversight. Payoff: concrete alone does not make a dam safe if the rock holding its ends is unstable. Strong objection: fatal disaster requires care to victims, geological uncertainty, and substantial explanation; PBS released a 27-minute documentary in 2025 and 2026 coverage is active. Sources: [PBS SoCal Lost LA episode (2025-01-07)](https://www.pbs.org/video/when-the-st-francis-dam-collapsed-wj8esw/) and [PBS American Experience Flood in the Desert (2023)](https://www.wpbstv.org/flood-in-the-desert-full-documentary-american-experience-pbs/), [USBR dam failure overview](https://www.usbr.gov/damsafety/risk/BestPractices/Chapters/C1-ConsequencesOfDamOrLeveeFailure.pdf). The PDF has NOT been page-inspected in this run; the PBS page/transcript is the actually read source for the pitch. 2026 videos cited below as demand signals, not historical evidence.

**3. General Slocum — another strong alternative.**
Opening: passengers discover during a steamer fire that supposed lifeboats and fire equipment cannot be used normally. Development: fire, smoke, failed extinguishing, inaccessible safety equipment and water evacuation. Payoff: the disaster exposed failures of safeguards that existed mostly on paper. Strong objection: tragic death toll, several contested secondary anecdotes about defective vests, and tonal overlap with the current Nuviko marine-disaster queue (#343 Sultana, #346 Grimalkin). Sources: [1908 court decision, Van Schaick v. United States](https://openjurist.org/159/f1d/847/van-schaick-v-united-states), [Brooklyn Public Library history](https://www.bklynlibrary.org/blog/2025/06/16/general-slocum-disaster). Primary decision was discoverable; individual legal findings not systematically excerpted this run. Not promoted to script.

**Choice, same yardstick:** all three can stop a general viewer with a specific event. St. Francis has higher raw human stakes and some public 2026 search signals. Apollo has the cleaner chain of distinct recoverable actions, a verified non-tragic outcome and a double payoff (fixing the spacecraft and the rocket creating its own lightning). That is an editorial choice, **not a measured victory in Nuviko's audience**. The chosen story is weaker if the viewer already knows the famous switch; the 10m version may be too dispersed. The strongest alternative is preserved rather than made deliberately weak.

## Actual fact evidence: one shared research for all three versions

- **NASA technical contemporaneous account:** Eugene Kranz and James Covington, [SP-287, What Made Apollo a Success?, chapter 5, paragraph beginning "Apollo 12 lifted off"](https://klabs.org/history/reports/sp287/ch5.htm), NASA history mirror; accessed 2026-11-21. It records exact times: first lightning **36.5 sec**, second/crew's platform report **52 sec**, initial return of tracking at **60 sec** (not normal data), the **SCE switch at 98 sec** restoring **all telemetry**, first two fuel cells at **144 sec**, third at **171 sec**, independent Saturn launch guidance operating normally, target parking orbit. This distinction matters: a radio/telemetry reacquisition at 60 sec is not the 98-sec usable-data restoration.
- **NASA primary historical review:** [NASA, Lightning Strikes Twice (2019)](https://science.nasa.gov/resource/lightning-strikes-twice/); both strikes and John Aaron's auxiliary setting, crew reaches Moon and back. The SCE AUX action restores usable signal conditioning; **do not claim a single switch directly re-powered the fuel cells or saved a tumbling rocket**.
- **NASA history timeline and destination:** [NASA, 55 Years Ago: Apollo 12 Makes a Pinpoint Landing on the Moon (2024)](https://www.nasa.gov/history/55-years-ago-apollo-12-makes-a-pinpoint-landing-on-the-moon/), section on Nov 14 departure and Nov 19 landing; Bean, Conrad, Gordon roles; Surveyor 3 proximity (~160 m), lunar work and safe return.
- **Transcript, not video watched:** [Apollo Flight Journal, Day 1 Launch and Reaching Earth Orbit](https://www.apollojournals.org/afj/ap12fj/01launch_to_earth_orbit.html), corrected 2025-02-22, index 00:00:36/52/01:36, contemporaneous crew/ground transcript plus retrospective commentary. Its editorial copyright is stated: only a three-word operational call is repeated; no audiovisual reuse authorized.
- **Detailed engineering interpretation:** [Apollo Flight Journal, More than SCE to AUX](https://www.apollojournals.org/afj/ap12fj/a12-lightningstrike.html), updated 2025-02-15: SCE converts sensor signals, secondary power, separation of independent launcher guidance and Apollo command module faults. This is later interpretation alongside original radio transcript, not an additional eyewitness. Some popular accounts overstate the switch's physical effect.
- **NASA background:** [NASA SP-4206 chapter 12](https://www.nasa.gov/wp-content/uploads/static/history/SP-4206/ch12.htm) and [NASA Apollo 12 landing history](https://www.nasa.gov/history/55-years-ago-apollo-12-makes-a-pinpoint-landing-on-the-moon/): post-launch analysis found rocket/environment triggered lightning; weather launch policy tightened. Sources do not support treating launch weather as a rule violation at the time.
- **Competing natural event interpretation:** some sources use "two lightning strikes" while detailed incident analyses describe distinct discharge paths. Narration calls them discharges/strikes without inventing exact geometries.

**Causal evidence chain for all three:** rocket ascends through charged weather (NASA) → electrical discharge affects spacecraft (NASA SP-287) → fuel cells disconnect/backup batteries on (NASA SP-287) → ground data becomes unusable and later navigation reference upset (NASA SP-287/Apollo Flight Journal) → independent Saturn guidance continues (NASA SP-287) → Aaron recognizes earlier data signature (Apollo Flight Journal/NASA) → Bean sets AUX, telemetry restored by 98 sec (NASA SP-287) → cells are separately reconnected at 144/171 sec (NASA SP-287) → orbit equipment checks before departure (NASA history/flight journal) → landing near Surveyor 3 and safe return (NASA history) → launch-weather restrictions revised (NASA review).

**Uncertainty:** We have not inspected any current original NASA media bytes, their resolution, licenses, individual frame provenance, or channel-specific retained assets. The cited Apollo Flight Journal transcript and secondary interpretation contain copyrighted editorial text; do not copy passages or film. The exact non-visible health of each sensor beyond the nine NASA-listed lost measurements remains outside the narration. Claim that the crew would certainly have aborted without AUX is unsupported and deliberately excluded. No invented dialogue, fear, frantic actions or instantaneous complete electrical restoration.

## Audience demand, separate from factual verification

Observed public search metadata **2026-11-21**, not first-hand viewing, transcript or comments for the YouTube videos below:

| Exact URL | Author / language / observed publication | Format / duration | Observed views | Comparison/limit |
|---|---|---|---|---|
| [Flashback: Apollo 12's Rocket Struck By Lightning Twice During Launch](https://www.youtube.com/watch?v=5GJhtyI2Fj0) | VideoFromSpace, EN, **2019-11-14** | YouTube clip, precise duration UNVERIFIED | **35,382** | Same-day same-author baseline [Apollo 12/14/17 landing sites](https://www.youtube.com/watch?v=9snQsyIAcv8), 2019-11-14 **13,218 views**; related [Apollo 12 landing-site visualization](https://www.youtube.com/watch?v=oajFbcnLGWg), 2019-11-19 **6,233**. Same channel format varies; all total views measured years later, not retention. |
| [Apollo 12 Lightning Strike & SCE to AUX](https://www.youtube.com/watch?v=JoEr4Y75bks) | October Sky, EN, **2019-11-18** | YouTube clip, duration UNVERIFIED | **1,577** | Single title result; comparable same-author uploads not established; no outlier claim |
| [APOLLO 12 STRUCK BY LIGHTNING](https://www.youtube.com/watch?v=ajOsHVK11Lw) | Michael Lennick, EN, **2010-02-28** | Extract from documentary series, duration UNVERIFIED | **98,493** | Distinct author, much older and different historical distribution; no baseline established |
| [Apollo 12: Struck Twice by Lightning](https://wonderminute.com/videos/IXuRlIQbwl4.html) | Wonder Minute, EN, **2026-11-19** | Page reports chapters ending 7:04, actual exact YouTube duration UNVERIFIED | **UNVERIFIED** | Fresh *content* in last 30 days, **not fresh viewing demand**. It is a direct same-story competitor, not a watched video or verified YouTube transcript |
| [ESA: Apollo 12, Pinpoint for Science](https://www.esa.int/ESA_Multimedia/Videos/Undated/Apollo_12_Pinpoint_For_Science) | ESA, EN, date on page **2011-02-24** | Documentary **28:30** | **9,548 on ESA page** | Useful official complete mission treatment, not YouTube view count/baseline and not a like-for-like 5m comparison |

**Freshness:** the 2026-11-19 Wonder Minute publication is fresh supply, not evidence that 30–90 day demand grew. NASA's 2019 archival clips illustrate evergreen curiosity, not current Nuviko demand. The 2019 same-author VideoFromSpace figures are observational, not a controlled channel baseline. No reliable own-channel analytics, CTR, stayed-to-watch, retention, comment-content analysis, or matched contemporary 2026 growth measurements were obtained: **UNVERIFIED**. Reddit comments and exact viewer questions were not authenticated on the selected videos. The topic stays a named **experimental hypothesis**. No paid provider credits used.

**Comparable alternative signal:** [Forrest Haggerty, 1928 St. Francis Dam Collapse, YouTube published 2026-06-07](https://www.youtube.com/watch?v=vFi_hvfzWvk), observed **68,949** public views, ~105k follower channel; different author/length and subject. [PBS SoCal 2025 episode](https://www.pbs.org/video/when-the-st-francis-dam-collapsed-wj8esw/), 27:05 and its transcript. These make the dam a serious competitor; they do not prove our audience would prefer it.

## Intended delivery and excluded fabrication

Only editorial texts; exact narration lengths require voice synthesis, which is forbidden in this run. Short has a tested-in-text conceptual ending→opening connection; AV seam UNVERIFIED. Long titles/visuals are *briefs*, not generated source frames. No production is authorized by this research. Never use third-party copyrighted YouTube pictures/transcripts as production assets without rights confirmation.


## 2026-11-22 targeted 10m evidence verification (new exact script, not a fresh topic)

Verified against primary NASA 2024 Apollo 12 mission history, https://www.nasa.gov/history/55-years-ago-apollo-12-makes-a-pinpoint-landing-on-the-moon/ : after systems verification in Earth orbit, Mission Control authorized translunar injection; S-IVB fired a second time; Gordon separated CSM, turned around, docked with lunar module Intrepid still on the stage and pulled it free; crew later inspected Intrepid during translunar coast for lightning damage. These events change what still had to be done after the 98-second telemetry repair. The source does not justify inventing a required abort decision or asserting damage to the lander.

Verified against Apollo Flight Journal retrospective technical study (updated 2025-02-15), https://www.apollojournals.org/afj/ap12fj/a12-lightningstrike.html : unstable primary inertial platform shut down during ascent; realigned later using star observations and data update; independent backup attitude indication remained available; nine specialized sensors were permanently lost, not the essential fuel cells. The journal's causal electronic explanation is retrospective analysis and is not claimed as a verbatim 1969 transcript. NASA SP-287 https://klabs.org/history/reports/sp287/ch5.htm provides independently matching fuel-cell/telemetry chronology and separate Saturn guidance. No borrowed dialogue or unverified interior motives were used.
