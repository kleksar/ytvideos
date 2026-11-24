# Story review — author only
| Target | RU | EN | Author verdict / format |
|---|---|---|---|
| 2m | [RU](variants/02m/script.ru.txt) | [EN](variants/02m/script.en.txt) | STRONG_CANDIDATE — recommended editorial Short; exceeds channel's 35–50s target |
| 5m | [RU](variants/05m/script.ru.txt) | [EN](variants/05m/script.en.txt) | STRONG_CANDIDATE — proposed Long, production blocked |
| 10m | [RU](variants/10m/script.ru.txt) | [EN](variants/10m/script.en.txt) | REWORK — proposed Long, production blocked |

| Variant | EN words / SHA-256 | RU words / SHA-256 |
|---|---|---|
| 02m | 271 / `c1302ca127d37fe00ce32c8c080f9e359291a5f5ea42e8b102a5a5bc9f195b08` | 245 / `597a0afa7c54ea8eac6eb0b16ef400dc49fa728d8fda427ce53e582197b80c5d` |
| 05m | 759 / `396ebd1e403b45128b1c4b8e93cbfba657390addbaa132702c0989746d091e8a` | 668 / `c1ded6d780fa5dc62a7dd7bb940fe6f5ac70c42879c36be0e8fc5d13fc7aedf1` |
| 10m | 1296 / `976db5842ccbb62ebde824500de280989effcf7f4edac17422b99beb79d992dd` | 1157 / `1709d70241b18f459e7f62435155c8fc7e62b9e3e604730d87f238d27becc207` |

Timing estimates, not measured: EN 130–155 words/min, RU 110–140, illustrative assumptions; natural voice speed unchanged. Allow additional pauses (02m 3–8s; 05m 5–15s; 10m 10–25s). EN 02m 1.7–2.1 min; 05m 4.9–5.8 min; 10m 8.4–10.0 min before pauses. RU 02m 1.8–2.2 min; 05m 4.8–6.1 min; 10m 8.3–10.5 min before pauses. No TTS/listening. Channel 35–50s usual Short target distinct from editorial 2m request; exact format/timing UNVERIFIED; 5/10 Long canvas/fps undefined.

| Criterion | 02m | 05m | 10m |
|---|---|---|---|
| Interest / significance | 8 — equal reserve, time on a real-life type of trip | 8 — asks when extra stop stops paying | 8 — travel planning, narrower EV audience |
| Opening | 9 — "One long charging stop or two short ones?" immediate choice | 8 — "would I actually arrive earlier" concrete but slower | 8 — “Could two charging stops get me home faster than one?” and whether a slow-station loss can be rescued; still needs route inputs |
| Development | 8 — last ten take twenty; B returns to fast band, queue flips | 9 — A passes at50%, B exact finish, slow rate and queue interact | 8 — a losing B is rescued by changing energy allocation; meal and feasibility alter decision, still calculation-heavy |
| Payoff | 9 — 45 vs65, same road/reserve, q25 reverses | 9 — 3h33 vs3h53, threshold and slower station | 9 — first B loses, optimized B wins with equal reserve; 3-minute queue defeats it again; answers both questions |
| Fresh angle | 8 — time reversal rather than universal 80% rule | 8 — equal finish charge and two delay factors | 8 — optimizing the two-stop plan rather than declaring a winner from fixed strategies |
| Visual expression | 9 — two battery states, same destination, waiting reversal | 8 — exact finish clocks, more labels | 8 — visible 60→80 first departure and 20→40 second arrival, fewer unrelated price labels; multiple route resets |
| Natural voice / clarity | 8 — one choice, concrete verbs; many spoken numbers | 8 — numbers follow steps; clock arithmetic dense | 7 — concrete charging choices but many spoken minutes/percentage points |
| Observed viewer interest | UNVERIFIED | UNVERIFIED | UNVERIFIED |

Authorship: current author; confidence medium in editorial judgments, high in arithmetic under inputs, low in audience reaction. Not measured retention or CTR. Main weakness 02m: mental arithmetic in A and narrower audience than card-terminal alternative. 05m: slower clock exposition. 10m: stronger second payoff at the slow charger; later lunch/consumption calculations still risk loss of attention; REWORK although complete. Baseline 02m/05m retained byte-for-byte. Queue revision compresses 10m setup, introduces the optimized B counterexample with an explicit second-station rate of 0.8 pp/min, removes separate price coda and repetitive final summary, and clarifies the lunch-overlap assumption. New 10m hash invalidates any former review/timing; no independent response existed. Scores apply to these exact texts. No independent reviewer.

Story maps:
- 02m: choice → equal reserve and model → A last ten slow → B low band twice → 45/65 payoff → queue counterexample → choice principle. Two full text cycles examined by author, not listened to. End "Before plugging in on another trip, I ask the same question." → "One long charging stop or two short ones? Which gets me home sooner?" RU "Перед тем как подключить машину в другой поездке, я задаю себе тот же вопрос." → "Одна долгая зарядка или две короткие? Как я быстрее доберусь домой?" End sets up next-trip decision, payoff already complete; cold opening stands alone. Alternative result-first spoils the choice; technical why-question changes metric. AV and independent loop UNVERIFIED.
- 05m: threshold question → route/setup → A taper + finish clock → B low charge + exact finish → slow station and queue flip → rule. Additional value: exact elapsed time, power+wait interaction. Possible attention loss at "two hours and forty-eight minutes of driving".
- 10m: same question plus slow-station challenge → constraints/curve → equal-reserve timelines → wait/power reversal → B at 60 loses (67.5 vs 65) → transfer 20 points to first station, B at 80 wins (62.5) → 3-minute queue reverses → meal overlap → station unavailable → increased consumption → planning decision. New understanding: charge allocation itself matters, not just number of stops; preserve reserve and feasibility. Weakest at "What if each leg needs five more percentage points of energy than expected?" after the second payoff; narrower audience and calculation density remain. 02m preferred.

| Gate | 02m | 05m | 10m |
|---|---|---|---|
| Facts/model | PASS author arithmetic, explicit assumptions | PASS author | PASS author |
| EN/RU | PASS author same inputs/results/limits | PASS author | PASS author |
| Format | UNVERIFIED — editorial Short above usual 35–50s target | FAIL production, Long undefined | FAIL production, Long undefined |
| Rights | UNVERIFIED actual assets/voice | UNVERIFIED | UNVERIFIED |
| Loop | author text candidate, independent/AV UNVERIFIED | N_A proposed Long | N_A proposed Long |
| Independent review | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Demand | UNVERIFIED | UNVERIFIED | UNVERIFIED |

Recommend only 02m editorial master, no runtime approval. Actual references and independent review before detailed storyboard.

## Queue revision 2026-11-24
Baseline commit `1b46b4cf4521cc8779e88f96b4b906017269847e`, exact 10m paths linked above, previous EN SHA-256 `8f6ec4930a9628f986889ff55a8ae4ddf137cc1229bff634337229de879d1946`, RU `8b59f9478bb6ea1ade96f45f61f9585d1763993c8e7cc0424ee0fa0499577319`. Status: three full variants prepared → author checked exact six texts → 02m recommended; 10m revised, REWORK, Long production blocked. 02m/05m retained: compact equal-reserve choice and exact threshold respectively, no demonstrated defect requiring rewrite. 10m opening asks two related questions; first full answer at "B wins by twenty minutes", second at "I arrive with the same reserve, two and a half minutes ahead of A." New model checks: 17 initial assertions plus 16 final assertions including 0.1-point grids for slower station and lunch overlap. Piecewise slope proves continuous minimum at 80 with fixed two stops, no queue; lunch optimum is 65. Final text clarifies minimum intermediate reserve and exact destination reserve, shortens initial clock sequence and replaces fixed lunch result with optimized B comparison. Source and calculation in research.md. Full 02m EN/RU read twice as text; existing seam remains a text candidate (not measured AV). Exact 10m EN/RU read against the same model and outcomes; no prior timing or independent review transfers. Visual intent for 10m only: keep route and clocks fixed between resets; show B first departure 60→80, second arrival 20→40, departure 50 and destination 20; for lunch reset original speeds, show 65 first departure, 25 second arrival, 50 second departure and 20 destination; compare stop time rather than driving time. No storyboard spans or graphics exist for revised 10m; 02m packaging unaffected. Related-video intro/target unavailable; no fictional next-video bridge. Next: independent blind review and real runtime/format selection, not media.
