> **Актуальная смысловая редактура, 2026-11-16.** Сценарий ниже повторно сокращён по требованию владельца: каждое предложение должно добавлять ценность зрителю, а длительность нельзя добивать словами. **Все численные оценки и Git blobs в историческом ревью ниже относятся к прежней редакции и являются STALE для актуальных сценариев.** Независимый first-listener не выполнялся.

## Current exact script — density-first revision

- **EN:** `script.en.txt`, blob SHA `5e17e15abdea3c4408cd48d67bce8fdbc546a17c`: **636 слов**, прежде 1 362 (−53%).
- **RU:** `script.ru.txt`, blob SHA `34fb56a4526f09c67a8c281605c0d27093b553d5`: **538 слов**, прежде 1 110 (−52%).
- **Структура:** 16 парных смысловых абзацев EN/RU, два вопроса до погружения, первый поворот — документированная реплика Мёрса, далее причинная последовательность без повторного старта.
- **Сохранено:** взрыв/перенаправление и занятая рулёжная дорожка; C3/C4 с неопределённостью причины пропуска; различие маршрутного и взлётного разрешения; тормоза до `O.K.`; наложение сообщений; **слышимый** вопрос бортинженера; 13 секунд до столкновения; примерно 9,5 секунд для экипажа Pan Am; 583 погибших/61 выживший; официальные выводы и требования к радиообмену.
- **Убрано:** повторные введения после хука, дубли последствий и предупреждений, вторичная лекция о каждом факторе катастрофы, справочный и морализаторский хвост. Приоритет — факт/действие/необходимая причина/поворот/отдача в каждой реплике.
- **Хронометраж:** 636 EN слов → приблизительно **3:51–4:54** при *условных* 130–165 словах в минуту, без измеренной озвучки/пауз. Это **не подтверждённые 5 минут**. Запрещено добавлять воду ради круглого числа; для самостоятельного 10m потребуется новый существенный проверенный материал, иначе `REWORK`.
- **Текущая авторская проверка:** 16/16 EN/RU структурных блоков, сохраняемые факты из существующего `research.md`; без независимого fact-check или blind review. **Не измерены и не гарантированы:** retention, CTR, first-listener score, TTS timing, storyboard spans, production media, AV, CI.
- **Workflow:** `EDITORIAL_CANDIDATE_UNREGISTERED`; прошлые reviewer remarks не подтверждают новую редакцию. Требуются независимое чтение точных blobs и реальный script approval; никакого автоматического merge/production.

---

# Tenerife 1977 — editorial review of revised Nuviko History Long

**EDITORIAL_CANDIDATE_UNREGISTERED — NOT production-ready.** This note records a user-provided critique of the **earlier** narration and an author-only correction check of **new** exact scripts. **No official independent reviewer of the new scripts has run**, no formal `ytv-script-review-v1` receipt exists, and the script approval gate has not been reached.

## Revision and provenance

| Artifact | Original exact Git blob | Revised exact Git blob |
|---|---|---|
| EN narration | `3c1bf3118f4dffe829f3d238d90317b5b7a38db4` | `f22bb6a8a4389e520c64216e0db6c5ada7142ecf` |
| RU owner reading version | `7648fa053dab6b54e18523f3879178768aaea920` | `221e56d9782d0081a9d0d9b3d016782535a3c26a` |

Revised: **37 aligned paragraphs; ~1,363 English words**. No TTS or actual listening was run. History of original bytes is preserved in this PR's Git commits; do not silently overwrite already approved production run artifacts.

The user-supplied external editorial critique assigned **topic 9.5/10, old script 6.5/10**, with low marks for conformity to opening structure (3/10), main hook (4/10), human involvement (4/10), payoff (5/10). These are editorial opinions, not measured audience results. The pasted critique itself ended with an incomplete final line; no missing text was inferred. Its concrete observations were cross-checked with the [FAA](https://www.faa.gov/lessons_learned/transport_airplane/accidents/PH-BUF) and [PBS transcript](https://www.pbs.org/wgbh/nova/planecrash/minutes.html).

## Corrected structural/factual deficits

| Old defect identified by reviewer | Revised exact narrative behavior | Remaining uncertainty |
|---|---|---|
| Opened with dramatic runway scene **before** the questions | First paragraph asks three specific viewer questions; no full accident scene is shown first; immersion covers bombing, diversion, congestion, taxiing and fog; main hook is Meurs pointing out missing clearance | Audience understanding and listening **UNVERIFIED** |
| Primary hook was an abstract early catastrophe instead of a human intervention | First officer's recorded warning enters after ~173 English spoken words of question+immersion; other pilots' actions follow causally | Spoken duration and real edit timing **UNVERIFIED** |
| Pan Am failed to take C3 “because it didn't turn”, with no mechanism | The third exit's sharp turn, easier fourth exit, repeated radio confirmation and uncertainty in the crew's reasoning are described; **not** claimed physically impossible | Single proven reason for missing C3 is **not** available |
| “O.K.” risked sounding like the cause of rolling | Brake release and engine acceleration are explicitly **before** tower “O.K.”; separate ATC route clearance is explained before the fatal decision | None for reported sequence, but narration perception untested |
| “Two warnings disappeared” was too coarse | Simultaneous Pan Am/tower calls become interference; **later, audible** Pan Am clearance-status exchange leads flight engineer Schreuder to question the captain | Whether listeners distinguish the warnings **UNVERIFIED** |
| No human roles | Captain van Zanten, first officer Meurs, engineer Schreuder and Pan Am captain Grubbs introduced with an action, not biographies. No invented thoughts or dialogue. | Hypothesis about seniority is *attributed as investigative possibility* |
| Flat final seconds | Approx. 13 seconds from captain's assurance to crash, approx. 9.5 from Pan Am seeing KLM; the crew's actual evasive actions are described without a fake real-time countdown | Edit pacing **UNVERIFIED** |
| Ending repeated only the two-clearance distinction | Consequences, official findings and team/phraseology changes compressed; final meaning tied to **all warnings that failed to stop action** | Still may sound didactic in unreviewed TTS |

This is a **review of a revised text**, not a claim that a second actor independently evaluated that exact text. The first-reviewer opinion is independent of the earlier draft's author, **but it predates the new revision**.

## Narrow author-only diagnostics for the updated bytes

| Criterion | Writer's provisional reading | Concrete reason | Remaining risk |
|---|---|---|---|
| Start and audience promise | **8/10** | Three questions on two planes, unauthorized takeoff and ignored warning; first content gives location and cause of diversion | 173 pre-hook EN words is approximate word count, not measured 60-second performance |
| Immersion → main hook | **8/10** | Meurs' actual recorded warning, rather than premature collision teaser; Pan Am exit creates a necessary question after the hook | The transition to Pan Am briefly returns to simultaneous action; needs independent first-listener QA |
| Causal developments | **9/10** | C3 vs C4 → clearance distinction → brakes before “O.K.” → radio overlap → later engineer warning → last seconds | Mid-script procedural terminology may still need shortening for non-pilots |
| Human stakes | **8/10** | Four real participants connected to observable decisions and statements, no unrecorded mental states | Emotional experience still depends on voice/performance |
| Payoff | **8/10** | 583 deaths and 61 survivors followed by attributed Spanish/Dutch findings and short summary of safety changes; last line about words failing to change action | Concluding lesson may still be too abstract; reviewer may recommend ending earlier |
| Historical checks | **8/10 provisional** | FAA/PBS recorder timeline, incident count and report conclusions used; case-specific source map in `research.md` | A new independent claim audit is **UNVERIFIED** |
| Natural EN/RU speech | **7/10 provisional** | Paired semantic order across 37 paragraphs; specific verbs/actions in both versions | No human listening, no independent bilingual comparison |
| Comparative YouTube demand | **UNVERIFIED** | Prior public competing video has significant lifetime views | No controlled age/creator baseline, owner retention or live vidIQ credits |

These are **not** measured retention, predicted views, CTR, or a certification. New text could score lower after blind review; author scores must not override that outcome.

## Exact acceptance checks / blockers

- **PASS / source inspection only:** factual chronology and third-exit ambiguity compared with FAA and PBS; fact-to-source links in `research.md`. No 3rd-party fact audit.
- **PASS / script structure inspection only:** first questions precede verified events; the main hook uses the co-pilot's missing clearance line; later statements preserve that “O.K.” was **after** brake release.
- **PASS / manually paired written versions:** EN and RU have 37 aligned paragraphs, same roles, causal steps and ending; not independent translation QA.
- **UNVERIFIED:** fresh independent review of the **revised** Git blobs, cold-listener promise and attention, exact voice performance and length, scene geometry, TTS, SRT and MP4.
- **NOT RUN:** formal `uv run ytv start`, pinned task packet/receipts and `awaiting_script_approval` state, because this GitHub-connector host cannot access the production runtime/store. If the production coordinator has an existing Tenerife run, **resume** rather than restart it.
- **NOT AUTHORIZED:** production generation, release, merge or fabricated approvals.
- Long narrative loop: **N_A**.

The existing `ytv-write-script` skill and `docs/standards/editorial.md` were inconsistent with the owner's required questions-before-hook order. Those instructions and `hook-patterns.md` are revised **in this same PR** without changing schemas, adding a gate, or reprocessing other pinned runs.
