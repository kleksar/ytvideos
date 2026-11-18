# Gemini VIII — substantive 2/5/10-minute editorial review

**18 November 2026 · author-only evaluation · EDITORIAL_CANDIDATE_UNREGISTERED.** This is not an independent first-listener result, a ytv task receipt, a production run, owner approval or measured audience performance. Original root scripts and their 14-scene storyboard are untouched. Main canonical docs at review time: `7c94f825056b98cb65d8de94dd3eec709cc78188` (#124 and #117 merged). Baseline story HEAD: `f2900fe89caa5bbaad7b3fc93afe6ecb9a4fb4ed`. Earlier wording review remains here as historical evidence, replaced by the current exact-variant evaluation below.

## Exact full texts and hashes

| Target | Format (Paper ChannelSpec) | English production candidate | English SHA-256 | Russian editorial equivalent | RU SHA-256 | English words |
|---|---|---|---|---|---|---:|
| 02m | Short, 9:16, narrative loop required | [EN](variants/02m/script.en.txt) | `f38a2525ea99a5df0b546bbba57b5e29a049a7637fa68abf3ec535e780c9931e` | [RU](variants/02m/script.ru.txt) | `67aeaf5c3e2a52382ebf2867edd845402f7858f64547261291670bf92517b9d7` | 240 |
| 05m | Long, 16:9 (supported) | [EN](variants/05m/script.en.txt) | `842f581af7cc3dcae6d298d2cba36f0c8ad187dfe060759d1a833a2b9197fea4` | [RU](variants/05m/script.ru.txt) | `4a1e6441cd635ca7c52ba6d78e090ba2a80e5c88e753549b0747138c10c9c974` | 607 |
| 10m | Long, 16:9 (supported) | [EN](variants/10m/script.en.txt) | `b2950c87d765fc7b2ad7caaa37488ecab4b9bd92a6d41cce9a49712c3c003dd7` | [RU](variants/10m/script.ru.txt) | `f764cf3333212a536b419217aeebf58cf4b17be13ceb5e185c3d61d58329a0cc` | 1387 |

Word counts: whitespace-delimited EN tokens, not TTS timings. Approximate runtime without measured voice: at an *assumed* effective 125–155 English words/minute, the versions take 1:33–1:55, 3:55–4:51 and 8:57–11:06 of speech, respectively, before pauses and any Long ending window. These are **2m / 5m / 10m editorial targets**, not a guarantee; never adjust the approved 1.10× channel voice speed merely to hit the label.

**Baseline preserved:** `script.en.txt` Git blob `1f117e7652919562325b0bbcfce2f7effa8d1f20`, `script.ru.txt` blob `e173e3f08854c09a7e8c79bb1125bd5adbb728f6`, both at HEAD `f2900fe89caa5bbaad7b3fc93afe6ecb9a4fb4ed`; previous review Git blob `602dac1986ae78d16d9e2eff5d8184c52b823b45`. The previous short's concluding `How close had they come to not making it home?` is a deliberate question rather than a natural lexical continuation. The baseline is not discarded; it is not the recommended candidate. Its "They only worked that out afterward" risks obscuring an in-flight fuel-gauge clue, though the exact stuck thruster was diagnosed later.

## Story maps and fact-backed pivots

**02m (independently complete):** (1) cold start with a capsule almost one revolution/second → (2) historic docking and Scott's intended EVA → (3) unexpected rotation, Agena jets disabled, radio gap → (4) Gemini fuel falling, undocking → (5) lighter capsule rotates faster / risk of blackout → (6) independent reentry jets stop the spin → (7) mission-rule abort, safe Pacific return, stuck Gemini thruster identified. Full rescue and price occur before loop phrase. Source ledger: [research](research.md), NASA mission and 2021 chronology.

**05m (independently complete):** (1) opening questions promise stop, separation paradox and mission cost → (2) real docking objective and approach → (3) first docking works → (4) main hook: uncommanded roll during radio gap → (5) fuel gauge and separation make rotation worse → (6) explain smaller capsule / almost 1 Hz risk → (7) Armstrong shuts down orbital controls and uses the independent reentry system → (8) mandatory abort and change of landing ocean → (9) recovery, later thruster finding. Every new section changes danger, knowledge or ability to act. Sources for fuel clue, recovery and crew fate: [NASA 2021](https://www.nasa.gov/missions/gemini/55-years-ago-gemini-viii-the-first-docking-in-space/).

**10m (independently complete):** (1) questions → (2) two launches, rendezvous and docking steps → (3) successful commanded 90-degree roll → (4) uncommanded roll with radio silence → (5) fuel gauge and undocking reversal → (6) separate reentry control saves crew → (7) contingency recovery shift (Atlantic→Pacific) → (8) retrorocket/heat shield/parachute/splashdown → (9) aircraft, water recovery and destroyer rescue → (10) probable electrical fault, later Gemini X use and crew careers. Added launch and post-splashdown logistics are sourced; they also risk postponing the core incident. Source: [NASA 2021](https://www.nasa.gov/missions/gemini/55-years-ago-gemini-viii-the-first-docking-in-space/), [NASA mission](https://www.nasa.gov/mission/gemini-viii/).

## Individual eight-criterion evaluation

Scores are the **author's subjective 1–10 editorial judgment**, not measurements or independent validation. Each reason names a part of the exact text. Confidence for the literary judgments is **medium**; interest demand is **UNVERIFIED** for all.

| Editorial criterion | 02m — score / evidence / weakness | 05m — score / evidence / weakness | 10m — score / evidence / weakness |
|---|---|---|---|
| Interest / significance | **8/10**: future Moonwalker nearly loses control immediately after the first docking; the familiar name may still overshadow Scott | **8/10**: asks three concrete questions of a single rare emergency; niche space hardware may narrow reach | **8/10**: connects mission and rescue operations; added logistics may be for specialists |
| Opening / promise | **8/10**: Earth crossing the window roughly every second is visible without Gemini context; docking is explained soon after | **8/10**: stop, undocking paradox and abort questions each receive a payoff; first action is not delayed for an abstract introduction | **7/10**: three questions are concrete, but launches/rendezvous slow arrival at the primary failure |
| Development / reason to stay | **8/10**: docking success → roll → false suspected vehicle → detach → faster spin → reserve jets | **9/10**: fuel dropping and the lighter capsule produce a causal reversal before rescue; some engineering explanation remains demanding | **7/10**: excellent central crisis, but detailed approach and post-landing chronology reduce density of change |
| Payoff / consequences | **8/10**: capsule steadies, planned EVA cancelled and both survive | **9/10**: the life-saving control system ends the mission; Pacific rescue and postflight cause complete both questions | **8/10**: recovery collar and ship arrival add a human end, but later careers after the safety payoff feel like a tail |
| Freshness of angle | **7/10**: familiar Armstrong story told as the undocking mistake, not lunar hero worship | **8/10**: separation paradox and *rescue caused abort* are two different verified turns | **7/10**: recovery logistics are new detail, but known Gemini chronology is not an unheard-of reveal |
| Visual expressiveness | **8/10**: juxtapose docked Agena and suddenly fast-spinning tiny capsule in tactile paper | **8/10**: separate steering systems, falling needle and separation can be shown as physical paper schematics | **9/10**: launches, orbital approach, two ships, emergency Pacific recovery offer distinct paper compositions; no images exist yet |
| Natural narration / clarity | **7/10**: direct verbs and full cause; deliberate grammatical loop ending `when` still needs independent two-cycle listening | **8/10**: specific verbs and consequences rather than moralizing; some technical nouns require a clear narrator | **7/10**: full clear speech, but launch specifications and legacy paragraph after rescue may sound like a report |
| Verified audience interest | **UNVERIFIED**: no comparable Shorts retention data | **UNVERIFIED**: no matched English Long audience sample | **UNVERIFIED**: no matched public demand measurement |

### Hard checks — separated from scores

| Check | 02m | 05m | 10m |
|---|---|---|---|
| One complete story with cause/payoff | AUTHOR_CHECKED: return alive and fault resolved | AUTHOR_CHECKED: emergency → safe landing → fault finding | AUTHOR_CHECKED: crisis and Pacific recovery complete |
| Factual support of *new* events | NASA chronology + report **author checked**; no fabricated injury | NASA chronology + report **author checked**; no actual blackout | NASA chronology + report **author checked**; more source-backed recovery detail |
| EN/RU semantic correspondence | AUTHOR_CHECKED: same launch, fault, decision, outcome | AUTHOR_CHECKED: same clue, emergency, recovery and uncertainty | AUTHOR_CHECKED: same named people, landing facts, consequences |
| Intro order for documentary Long | N_A: narrative Short | AUTHOR_CHECKED: questions → docking immersion → unexpected roll hook | AUTHOR_CHECKED with pacing concern: questions → immersion → unexpected roll, but the roll arrives relatively late |
| Full EN/RU Short loop | AUTHOR_CHECKED only: EN ends `when` → opening `Neil Armstrong's spacecraft began spinning...`; RU ends `когда` → `Корабль Нила Армстронга раскрутился...`. Cold opening makes sense, full payoff occurs before the seam. Deliberate dangling conjunction could still sound authored; independent two-cycle test **UNVERIFIED** | N_A | N_A |
| Independent first listener and bilingual reviewer | **UNVERIFIED** — no separate reviewer/session or genuine `ytv-script-review-v1` was available | **UNVERIFIED** | **UNVERIFIED** |
| TTS, measured timing, media, AV seam, actual viewer data | **UNVERIFIED** | **UNVERIFIED** | **UNVERIFIED** |
| Owner script selection / runtime run | **NOT_APPROVED / EDITORIAL_CANDIDATE_UNREGISTERED** | **NOT_APPROVED / EDITORIAL_CANDIDATE_UNREGISTERED** | **NOT_APPROVED / EDITORIAL_CANDIDATE_UNREGISTERED** |

## Before → after / additive value

**Before:** only an approximately one-minute root narration, old author self-review and an exact-root 14-scene Short plan. The root is historically retained without modifying its bytes. **After:** six complete independent EN/RU narrations in `variants/`, expanded source ledger and explicit subjective review, without importing any variant as a ytv master.

**02 → 05:** viewer gains the purpose of docking and Scott's intended spacewalk, momentary control attempt, *fuel falling before undock*, a physical explanation of the worsening spin, and the emergency Pacific landing. Most valuable added scene: dropping Gemini propellant becomes a clue immediately before the seemingly sensible undocking worsens the problem. Potential interest loss: the paragraph defining the two sets of jets may need a clear diagram.

**05 → 10:** viewer gains the chase and commanded target roll, in-flight propellant gauge context, the geography and personnel of recovery, plus later use of the Agena and careers. This has verifiable informational value but loses urgency in the approach mechanics **before** the first uncontrolled roll and the final Agena/career appendix **after** rescue. End the chosen version at its own payoff rather than copying the appendix automatically.

**Recommendation: 05m Long** for a *single* prospective master, because it makes the undocking trap and reserve-control decision intelligible while staying close to Armstrong and Scott. The short is valid as an alternative idea and may win if runtime timing or independent reader shows the long to be slow. The ten-minute edition is complete but not automatically preferable. No variant is independently approved; this recommendation authorizes no production, merge, TTS or upload.

## Outstanding external capability and next step

This connector-only editorial session can read and update GitHub text but has **no available genuine independent reviewer host/session tool or saved ytv runtime context/claim**. To progress: import the owner's selected *exact* script/commit/hash via the current `ytv start`/source path, obtain a fresh independently generated first-listener and bilingual review from the canonical helper output (without prior author scores), then await the owner's exact script approval. Produce a new storyboard only for that chosen hash; legacy `storyboard.json` remains exclusively with unchanged root scripts. Do not fabricate run/session IDs, stage receipts, viewer retention or production status.
