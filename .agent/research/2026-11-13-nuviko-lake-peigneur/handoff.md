
## Обновление 18.11.2026: переработанная очередь, без production

**Baseline PR #24:** `ba17060d1da7cc1eba0b6cc71c43e36713da6b3e`; `main` при чтении требований — `7c94f825056b98cb65d8de94dd3eec709cc78188`. Изменения только в папке этой истории. Сначала [README с шестью точными текстами](README.md) и [story-review с SHA-256](story-review.md), затем единый research. Это поздняя заметка выше архивного handoff; старые слова о *единственном Short* описывают исходную ветку, не текущий набор.

**Редакторский результат:** 2m root EN/RU скопированы идентично в `variants/02m`, новые 5m/10m написаны в двух языках; 5m рекомендована, но не утверждена. Все тексты имеют свои hashes. Старые `storyboard.json` / визуальные spans / 76.8 s — **только прежний root/02m**, а не новая 5m/10m production раскадровка. Новая сцена требует точной выбранной версии/hash; числа сцен должны следовать тексту.

**Hard blockers:** независимый cold reviewer и bilingual reviewer (`sessions.independent`) здесь не обнаружены; runtime `ytv start`, актуальный pinned packet, reviewer receipts, owner exact approval, TTS измерения, actual AV seam и media не выполнялись. Статус `EDITORIAL_CANDIDATE_UNREGISTERED`, а не `awaiting_script_approval`. Канал поддерживает Long, но формат 5m и 10m нельзя запускать без отдельного решения владельца; не перепривязывать pins другого run.

**Перенос:** на локальном хосте после явного решения по exact тексту использовать актуальные AGENTS / ytv-start / task contract; зарегистрировать кандидата с полными EN/RU и story-review, получить реальную независимую проверку и ответ владельца. Никаких approval миграций и медиа без соответствующего источника полномочий.

---

## Актуальный workflow — сверено с remote main

Основа требований `main` `96c8fa1573c02e8e7987e272a569bf34f037691e`. Текущий канал Nuviko History **active**, а данный PR — не зарегистрированный `ytv start` run. Собственная `storyboard.json` — предварительный текстовый план сцен, не официальный completed `storyboard`. Ссылки на self-review и будущие voice timings не подтверждают `awaiting_script_approval` или независимый first-listener.

Когда владелец выбирает этот кандидат: `uv run ytv start --channel nuviko_history --format short --intent 'Проверить неутверждённый сюжет PR #24'`, прочитать `plan_summary`, `read_next`/task_guide/pinned docs и запустить актуальные research/script tasks. `script` требует фактическую независимую сессию reviewer, оригинальный `ytv-script-review-v1` для точно сохранённого EN, двойное прочтение Shorts и настоящие CAS/receipt hashes. При отсутствии reviewer — UNVERIFIED, не подменять PASS. До полного gate и подлинного owner approval нельзя начинать imagegen/TTS/MP4. [Workflow](https://github.com/kleksar/ytvideos/blob/main/docs/workflow.md).

Прошлые даты и SHA ветки ниже — historical provenance. Принятый сюжет по-прежнему должен избегать выдуманной точной причины прорыва шахты; RU смысловая редакторская копия, не TTS master; геометрия буровой/шахты, реальные refs и AV seam не проверены. Не мигрировать pins чужих выпусков молча.

---
# Handoff — Nuviko History / Lake Peigneur, 1980

**Status:** TEXT-ONLY, DRAFT, owner has not approved this exact English narrative. PR is an editorial candidate, **not** a registered official episode, media stage, upload or production authorization. No imagegen, voice, subtitles, render, merges or publication in this run.

## Provenance / pinned source

- **Remote main at research start:** `44786bd929473cc06a724aefb4ad122f358c0aeb`, tree `ebceaa244700491efa75dea0524943b64b8f6242`.
- **Fresh PR branch base:** `65066f0869fe6635f1876b70617e17630b26fdf7`, tree `34049728c45a2d69ef9c3f6e1236c1f5061de55a`, after PR #18 merged 2026-11-13T05:03:40Z. Current repo now requires CLI `uv run ytv start` for official new runs and independent review; **this text-only Draft PR is not such a run**. On any later *explicitly authorized* production, follow the actual main `start`/task-contract/approval and obtain a new pinned snapshot; do not invent an approval or operate on old versions.
- **Channel:** `nuviko_history` (not `nuviko_videos` / Nuviko Stories), read `channels/nuviko_history/channel.json`, `AGENTS.md`, `PROFILE.md`, `brand/VISUAL_PROFILE.md`, channel storytelling & pipeline documents and generic standards. `channel.json` was **active** at the researched main, after #12; this does **not** override TEXT-ONLY scope of this task. Older frozen declaration in prompt does not make it production-capable here.
- **Narration:** `script.en.txt` 219 words and 15 blocks, proposed canonical TTS/SRT source only *if accepted*. `script.ru.txt` is exact editorial translation for owner, not a proposed Russian voice. All facts, chronology, four miners, four elevator rides, canal reversal, safe outcome and uncertainty equivalent in both.
- **Script Git blob IDs created during preparation:** `script.en.txt = 4ee16c8deab67716e9dd91b36b09925ab48c01e1`; `script.ru.txt = e17b099234c3a1edc5c9dd0ec08b4af899f35e3d`. These are source Git blob SHAs, not audio approval hashes or media SHA-256.
- **Historical primary:** official 1981 MSHA inundation report mirrored at https://usminedisasters.miningquiz.com/saxsewell/1980_jefferson_island.pdf, investigated locations pp.18–23 and 41–44. Original report says exact initial trigger **indeterminate**. Louisiana Endowment https://64parishes.org/entry/lake-peigneur-drilling-accident and contemporary UPI https://www.upi.com/Archives/1980/11/21/Drilling-rig-breaks-into-salt-mine-cavity-draining-lake/6665343630800/ support visible consequences. Report PDF page visuals **not verified** due HTTP 502 during screenshot; only text evidence used.
- **Research:** `research.md` 9 different events and 3 finalist pitches, why selected vs Mona Lisa, public audience observations separated from claims/projections and duplicate/owner rejection records. `story-review.md` separately marks author interest from independent review, includes exact mandatory last two→first two EN/RU seam text.
- **Provisional scene grid:** `storyboard.json` 15 paired EN/RU narrative blocks, AI prompt per scene, full-frame 9:16 photoreal 1980 reconstruction, roughly 4–6 seconds each **estimated**. Scene duration sum is not speech length; measure after approved final voice to restructure. No separate parallax or vertical pans, S015 must reuse S001 exact accepted image at matching crop to create real loop. No 2D traveler introduced in these prompts; add only with actual accepted Nuviko character reference PNG byte+hash verification. Historical human/period object references likewise verified before generation.
- **Packaging:** `packaging-brief.md` proposes 3 truthful title/thumbnail concepts with different viewer promises and first confirmation. They are not video metadata, a CTR forecast or generated previews.

## Next actions for local agent — AFTER owner's separate explicit production request

1. Review exact full EN narration and full RU translation with owner. Preserve displayed script blob hash and an actual trusted approval event; Draft PR merge alone creates **no** approval.
2. Obtain independent cold reader verdict: why continue, exact point of drop-off, final value; permit a concept FAIL. Independent bilingual review is also UNVERIFIED. On failure revise script and replace exact hashes, re-review. Current author's PASS only checks reasonableness of concept and text.
3. Verify approved current main/ChannelSpec and run IDs, reference assets and provenance, real voice/provider availability, actual stage capabilities/budget; do **not** create invented IDs or manual approval envelope. Set the run within the repo's supported task-contract.
4. On authorized run use voice `5vsgZsi667xMyGinrNIM` with channel speed `1.10` exactly once, then actual word map and exact revised storyboard timing. Use AI imagegen only for newly authorized visuals; check source references for rig, salt mine, 1980 work clothes, Delcambre canal. Never fabricate that a drill bit definitely breached a mine gallery; use physical generic cross-section if explanatory.
5. After real images, SRT and render inspect audio continuity, mid-story attention risk S008/S009 and exact last→first spoken/image seam. Technical success is not independent artistic acceptance.
6. Show exact verified MP4, and **only** on separate approval + direct external-action request consider any upload, schedule or pinned comment.

**No other existing run/branch/PR/docs/skills was touched.** GitHub diff verification and CI status belong to PR finalization and must be recorded separately, rather than asserted in advance.
