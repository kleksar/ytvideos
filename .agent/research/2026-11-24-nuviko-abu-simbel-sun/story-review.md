# Author review — exact drafts

Author: current editorial agent, not an independent reviewer. Confidence medium on narrative judgement, high on core event, low on audience demand. No viewer/CTR/retention claims. One authoring pass, one editorial text inspection; no separate reader or audio. Exact source files and UTF-8 SHA-256 (LF, final newline):

| File | Words (whitespace-delimited) | SHA-256 |
|---|---:|---|
| [variants/02m/script.en.txt](variants/02m/script.en.txt) | 290 | `a332ad16e526634b70a0230dc99efbdce1f4f602f0c824dfa1b14feaba57686f` |
| [variants/02m/script.ru.txt](variants/02m/script.ru.txt) | 235 | `f95579fadc24b2c69a4392ab465239c90f0ae52e1b70e113877d80cbb08cfd9f` |
| [variants/05m/script.en.txt](variants/05m/script.en.txt) | 696 | `efb4f8a9da1c81406a74afd146880d6e8c2e14b710c7fb080fee336360ced37e` |
| [variants/05m/script.ru.txt](variants/05m/script.ru.txt) | 547 | `55544fe05c8f8334d37648c2659c2f61208e64f9ea9e2a12289b8d7fdac08af3` |
| [variants/10m/script.en.txt](variants/10m/script.en.txt) | 1200 | `2e2776704c5bf1fdd8455d3bf241ee38e0b1e8c90ea4a190eb6b70efa8cc448c` |
| [variants/10m/script.ru.txt](variants/10m/script.ru.txt) | 959 | `a1fa2b055eee35963d640d9debc05b0466ec52466518932fe0c19b64c04be578` |

| Variant | EN production text | RU review text | Editorial verdict |
|---|---|---|---|
| 02m | [EN](variants/02m/script.en.txt) (290 words) | [RU](variants/02m/script.ru.txt) (235 words) | STRONG_CANDIDATE |
| 05m | [EN](variants/05m/script.en.txt) (696 words) | [RU](variants/05m/script.ru.txt) (547 words) | STRONG_CANDIDATE — recommended |
| 10m | [EN](variants/10m/script.en.txt) (1200 words) | [RU](variants/10m/script.ru.txt) (959 words) | REWORK (complete draft, weaker pacing) |

Timing assumptions: EN roughly 125–150 spoken words/minute, estimate not a measured approved voice; production voice configured 1.10x exactly once (do not alter). Short has no end screen; Long adds 10s end screen, exact story-linked intro dependency not resolved. For each EN word count approximate narration range:
- 02m: 1.93–2.32 min speech; pauses/visual breathing can extend this; Short 9:16; actual timing UNVERIFIED.
- 05m: 4.64–5.57 min speech; pauses/visual breathing can extend this; Long 16:9, add 10s end screen; actual timing UNVERIFIED.
- 10m: 8.00–9.60 min speech; pauses/visual breathing can extend this; Long 16:9, add 10s end screen; actual timing UNVERIFIED.
RU review translation, not separate TTS plan.

| Criterion | 2m | 5m | 10m |
|---|---|---|---|
| Interest/significance | 8: impossible move of sunlight | 9: temple is also a functioning instrument | 8: competing solutions and wider costs |
| Opening | 8: “cut a temple ... path of the sunlight” | 8: two concrete questions, colossal statues immediately | 8: three options plus criterion of success; slower question sequence |
| Development | 8: water → disassembly → geometry → dome | 9: original jacking scheme, fragile sandstone and lost material, load-bearing new hill | 8: earlier choice → monitored excavation → thin cuts → depot reinforcement → concurrent foundations → survey and frames; technical density remains |
| Payoff | 9: three lit figures, fourth shadowed | 9: exact figures plus revelation of modern structure behind cliff | 9: preserved orientation and explicit limits of preservation |
| Angle freshness | 8: sunlight vs popular moved-temple fact | 8: moving the function, not only masonry | 8: same angle plus competing projects |
| Visual expression | 9: saw, giant head, beam | 9: barrier, cut detail, block store, new dome, beam | 8: detailed works but funding, settlement and campaign harder to depict without repetition |
| Voice/clarity | 8: simple chronological action | 8: analogy about kerf clarifies stakes, some institutional names | 8: shorter background and more worker actions; some technical density |
| Audience evidence | UNVERIFIED | UNVERIFIED | UNVERIFIED |

2m STRONG_CANDIDATE: precise opening/action, keeps one question, payoff before return. Main weakness: early lifting plan is mentioned without its tradeoff. Literal closing → opening: “Why did the engineers have to recreate more than just the stones?” → “Workers cut a temple in Egypt into pieces, but they also had to move the path of the sunlight inside it.” RU: “Почему инженерам пришлось восстановить не только сами камни?” → “Рабочие разрезали египетский храм на части, но вместе с ним им предстояло перенести и путь солнечного света внутри.” Full text read in sequence and seam inspected authorially; question returns to the functional distinction already answered; wording is metaphorical, not movement of sun; no new chronological claim. Authorial text seam plausible, independent and AV UNVERIFIED. Other possible openings: “Three statues in an Egyptian temple still receive sunlight after the entire temple was moved” (gives result immediately); “The temple was carved into a cliff that was going underwater” (loses functional distinction); chosen opening gives concrete work and central question. Cold entry names temple/Egypt; payoff before final question. 

5m STRONG_CANDIDATE: questions → four colossi/inner hall → dam → proposed lift replaced → cofferdam and fragile stone → hand saw loss → labelled blocks → alignment and concrete domes → three lit statues and hidden modern structure. Main weakness: engineering/geometry explanation requires clear visual composition; the original relocation is a known topic. Answers opening questions at reassembly and modern illumination paragraphs. Recommend 5m because the audience gains a meaningful choice between methods and an explanation of both material and orientation constraints; unlike the 2m it shows why preserving the beam is an engineering challenge rather than merely asserting it. 

10m REWORK: revised from baseline 36e32a7c780420c8977f66297d31a824eb04a2ee, original EN 1437 words SHA-256 b202d6b2195051393b2e46e9360b4a6405970a55f8057fa31ca6370f74ae9c5a, RU 1132 words SHA-256 541e9d23a4e1365b84f10c54f4611d9e189bb2f4dfee1e88527241483868c96a. Shortened context before the choice; added monitored excavation, thin cuts, concrete backing and steel anchors, the temporary settlement, simultaneous foundation work, theodolite checks and frames. Modern sunlight payoff precedes wider campaign and displaced-community coda. New 10m adds a genuine construction sequence but risks losing attention at “The numbered pieces were laid out...” and the campaign coda. 05m remains the provisional recommendation; 02m and 05m unchanged. Author confidence medium, source support medium–high, audience UNVERIFIED. Previous 10m assessment historical; independent review required on new hashes. 

10m visual intent in reading order: questions/colossi/inner sanctuary → dam/options/cut decision → temporary dam/monitored excavation/hand and mechanical cutting → depot and anchors → temporary town and two sites → sightline and survey/frames → domes and reopened temple → modern beam → wider rescue/community loss → final cliff. Editorial beat map only; no storyboard or measured timing. Existing 05m packaging remains bound to unchanged 05m. 

| Check | 2m | 5m | 10m |
|---|---|---|---|
| Author factual support (research claim map, no invented dialogue) | PASS | PASS | PASS with caveat: permanent barrier risks and resettlement are contextual, no precise costs or counts |
| EN/RU semantic parity (author) | PASS | PASS | PASS |
| Format compatibility by current channel.json | PASS Short | PASS Long | PASS Long |
| Rights of future visual/audio | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| Narrative loop | UNVERIFIED independent + AV; author text seam reviewed | N_A Long | N_A Long |
| Independent first-listener | UNVERIFIED | UNVERIFIED | UNVERIFIED |
| TTS/MP4 timing | UNVERIFIED | UNVERIFIED | UNVERIFIED |

No existing review receipt. No script gate passed. No storyboard spans/timings or prompts invented; detailed planning awaits verified text and actual references. Recommendation is editorial only, no approval.
