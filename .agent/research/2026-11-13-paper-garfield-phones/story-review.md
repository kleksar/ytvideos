# 2026-11-18 — duration variants editorial assessment

**Owner's 2/5/10 directive:** canonical `docs/standards/editorial.md` (merged PR #124). Status `EDITORIAL_CANDIDATE_UNREGISTERED`. All scoring and hard checks below are AUTHOR review on these exact files, **not** a first-listener/independent receipt, audio review or owner approval.

## Baseline and exact SHA-256 (UTF-8)

Source PR #30 head `e6afabc434b0aedda5d938d689f7c458a8efbd0a` (before changes). Original root scripts preserved byte-for-byte: [EN](script.en.txt) Git blob `8aafc5bae7137df8f62ed3f625ae8cf25ce8c0b1`, SHA-256 `05796f25575fd8eb12c2311826a30eb4363090aa4bab0de4d45f5e30e4bb2cb6`; [RU](script.ru.txt) Git blob `eb88b700437ab322521528af82f4b47752e2710a`, SHA-256 `cd523efa42af3293d44b015f347afd77df2eaed4c251d404186993808e449f1a`. Old 14 scene spans remain pinned ONLY to root version, not new 02m.

| Target | EN exact complete script, SHA-256 | RU complete semantic translation, SHA-256 | EN/RU words | Format |
|---|---|---|---:|---|
| 02m | [EN](variants/02m/script.en.txt) `03619fac6e367a984fa63ed41c95389fbe4fd46a5f21b7e62144989dc232e504` | [RU](variants/02m/script.ru.txt) `4ef991280facce9041e2954d8bf04a12b6ba80f20b30b2c60bcc9e35c0e05296` | 243/205 | short |
| 05m | [EN](variants/05m/script.en.txt) `ecb542776693eb0464b2b708d1bae25285b50ae647ffe28a40f53149011f5230` | [RU](variants/05m/script.ru.txt) `130bb6334c8804eea62f5ce3c9b7871d848ce3fcdeaaf67b7b395519c05e602d` | 657/566 | long |
| 10m | [EN](variants/10m/script.en.txt) `d63490b478db0dd7669fc7e45e3c5ee252e94ddcb41ac9efc12c230553b01e0c` | [RU](variants/10m/script.ru.txt) `f7e38a25e845cc4c431725f36079434a516dde451345d2ccdb575cbbf1faaebc` | 1417/1166 | long |

**Time assumptions:** 130–155 EN words/min before pauses ⇒ 02m 1.6–1.9 min; 05m 4.2–5.1 min; 10m 9.1–10.9 min. These are estimates, voice profile/speed unchanged, no TTS/MP4. Actual measured duration UNVERIFIED. Both format modes exist in Paper ChannelSpec, but no production clearance follows.

## Three independent story maps and exact hook/payoff

**02m:** concrete cold open `An orange Garfield telephone washed up on a beach in France.` → 35-year recurring fragments → volunteer cleanup fails to stop arrivals → container hypothesis → Morvan's remembered cave → tide constraint → 23 complete phones & mostly empty container → unknown ship/second-container possibility → continuing cleanup → last `And on a later cleanup, just as before,` → literal next initial. Main answer occurs before final line. Opening visual: intact paper Garfield landline at surf line, not a toy/mobile. No missing answer hidden in replay.

**05m:** explicit questions `How can a beach keep finding the same telephone for more than thirty years?` / `... does that finally stop them washing ashore?` → real gadget/2018 >200 pieces → attempted location search and no precise place → **main hook** Morvan remembers physically seeing a container → cave entrance/low-tide/weather delays → rust, 23 intact handsets → **reversal** container mostly empty, already-dispersed cargo → unknown ship/quantity → children's awareness and continued cleanup → payoff `A telephone mystery had an answer. The cleanup did not have an ending.` The opening questions are answered in the narrative.

**10m:** opening questions concern repeated finds, tracing moving evidence and whether discovery prevents pollution → particular 1980s Tyco-style landline, regular Ar Viltansoù work and count → no underwater search location → 2019 publicity and meeting during stranded-dolphin cleanup → **main hook** Morvan has long known the cave → 1980s testimony and knowledge gap → delayed March 22 visit through tidal entrance → 23 complete handsets, metal → **reversal** source nearly emptied → possible second shipment / original carrier unknown → aftermath: more 2019 finds and Garfield's education role → payoff `A puzzle about the origin of a phone had been solved. The ocean had already carried its consequences far beyond the answer.` New details support the same incident; not a different third history.

## Exact-text eight-criteria scores (author-only, 1–10)

| Criterion | 02m | 05m | 10m |
|---|---|---|---|
| Interest / significance | 8 — striking recognizable discarded product and real cleanup cost | 8 — solved mystery collides with unsolved pollution | 8 — broader human/educational value; more abstract later |
| Opening | 8 — object on the beach immediately understandable without narration context | 9 — two distinct questions answered by the finished narrative; phone image then actual fragments | 8 — three questions clarify inquiry but initial exposition takes longer |
| Development / reason to continue | 8 — witness, cave access, recovered phones, but compressed obstacle | 9 — repeated pickups, failed search, witness, hazard, concrete physical discovery | 7 — credible side beats, but post-cave explanation slows momentum |
| Payoff | 8 — 23 handsets and emptied source plus continuing cleanup before loop | 9 — inability to prevent plastic after finding container is strong causal reversal | 8 — source/recovery/uncertainty fully closed, but exit longer than 05m |
| Freshness of angle | 8 — distinctive object, although publicly reported in 2019 | 8 — shift from whodunit to why cleanup did not end | 7 — additional education/unknown-cargo angle familiar in long environmental explainers |
| Visual clarity / paper staging | 9 — bright phone, separate components, low-tide cave | 9 — coherent varied actions: bag, sea, farmer, fissure, 23 handsets | 8 — staging possible, but extra verbal explanation after climax needs care |
| Naturalness / clarity of EN+RU | 8 — plain action verbs; ending depends on a deliberate syntactic continuation | 8 — human actions and consequences rather than abstract commentary; geography slightly dense | 7 — accurate clauses, but final third sometimes explanatory; no audio self-listen |
| Verified audience demand | UNVERIFIED — old press/Reddit engagement only; no comparable YouTube views/retention | UNVERIFIED — no independent test of medium runtime | UNVERIFIED — no viewer data establishing benefit of length |

**Confidence and shortcomings:** all first seven scores are subjective *medium confidence* editorial judgments by the author. 02m risk: the repeating first phone could sound like a restart in actual TTS; 05m risk: diving/geography segment before Morvan may lose interest; 10m risk: after the cave the explanation of shipment uncertainty and volunteer messaging could become a reference tail. Eighth criterion lacks measured evidence: no honest numerical 1–10 given; do not substitute press mentions or Reddit votes for retention. No scored version has an independent PASS.

## Separate hard checks and limits

- **Facts / causal implication:** author checked source IDs G10-1…G10-9 in [common research](research.md). Morvan's words are reported recollection, not a definitive archive of the 1980s. Exact ship, year, number of original phones or containers and current 2026 frequency remain unknown. Any second container is a *hypothesis*, not a reveal. No invented quotes or private thoughts.
- **Language:** author compared complete EN/RU texts for persons, chronology, quantities 23 and >200 in 2018, low tide, farmer's memory, physical evidence, uncertain ship and post-expedition 2019 debris. Russian is full adaptation, not prose outline; independent bilingual first-listener UNVERIFIED.
- **Short 02m loop:** author textual double-pass of full EN and RU (not independent). Literal EN end→start: `And on a later cleanup, just as before, / An orange Garfield telephone washed up on a beach in France.` Literal RU: `И во время одной из следующих уборок, как прежде, / На пляж во Франции вынесло оранжевый телефон в виде Гарфилда.` Cold opening understandable; complete answer before repeat; new find logically continues prior scene. It remains **provisional**, audible rhythm and actual visual/audio seam UNVERIFIED. Root 14-scene loop evidence not inherited.
- **Long 05m and 10m:** narrative loop N_A, no expected Short end seam. Intro questions precede main hook. Paper channel supports Long; no scene image, storyboard, TTS, timing or publish approval for these variants.
- **Independent first-listener reviewer/receipt:** not available in this GitHub connector-only host; cannot call a fresh independent model session or official local `ytv` runtime. No fake reviewer choice or approval. Selected exact variant needs independent reading *without this scoring text*, then sources and old version only after first read. Changed hash invalidates any old receipt.

## Comparison of completed versions

| Transition | Actual added value | Where interest may weaken |
|---|---|---|
| 02m → 05m | Regular collectors and 2018 count, unexplained search failure, Claire/René human line, delayed tide, practical hope of stopping supply | 05m: diver-search explanation just before witness; could tighten after actual reviewer feedback |
| 05m → 10m | Eye mechanism, fishing-waste context, farmers' long-known location, dolphin cleanup encounter, media coverage, shipment uncertainties, educational outcome | 10m: after 23 handsets and empty container; later origin/education explanation is less dramatic than the reveal |

**Recommendation: 05m Long** (657 EN words, provisional), because it has the clearest causal story, the strongest reversal and least post-climax material. 02m remains a useful self-contained Short; 10m is a complete, evidence-based option, but not the strongest and not automatically approved. No measured CTR/retention guarantee. Owner has NOT selected any exact master. Status: `three versions prepared → author-checked → 05m provisionally recommended; independent/run/approval UNVERIFIED`. Next: independent review, real runtime registration, owner approval for one hash, then new storyboard.

---
## Archived original single-Short self-review (2026-11-13; preserved)

# Story-review — Paper Garfield phones
**Точный scope:** self-review редакционного кандидата, не independent-review, не script gate. Дата 2026-11-13.

## Авторское чтение ДО раскадровки
- **Интерес остановиться — условный PASS (author only):** первое предложение даёт невозможную комбинацию: морская пена + наземный телефон в форме известного кота. Не нужен заранее известный контекст Бретани.
- **Причина остаться — условный PASS (author only):** не просто повтор выброшенного мусора, а последовательность уборки без результата → известная гипотеза → фермер сообщает новый ключ → ограничение отлива → реальные остатки контейнера → контейнер почти пуст.
- **Отдача — условный PASS (author only):** географический ответ получен до последних строк; последний поворот — уже утекший пластик нельзя убрать находкой источника. Не представляем экологию как радостную окончательную победу.
- **Потенциальное место потери интереса:** после S005 зритель мог уже угадать «контейнер». S006–S012 обязаны оправдать просмотр конкретным фермером, труднодоступной пещерой, найденными трубками и почти пустым грузом; если независимый слушатель назовёт эти детали недостаточным развитием, сюжет возвращается к отбору, не косметически удлиняется.
- **Ясность — авторский PASS:** каждый термин понятен без кадров; «Garfield» в английском объясняется объектом в кадре и словом «telephone» с первого предложения.
- **Фактология — авторский PASS с оговорками:** имена и числа S006–S013 проверены по современным репортажам и интервью; S007 — reported testimony, не архивный факт; год судна, количество контейнеров, загрязнение в 2026 не утверждаются.
- **Структура — авторский PASS:** ответ и отдалённая физическая находка не зачитываются в хуке, развязка дана, повтор не требует искусственного обрыва.
- **Независимый `ytv-script-review-v1`: UNVERIFIED;** подлинный свежий reviewer, хеш EN, буквальное двукратное чтение и receipt не доступны в этом host. Ни авторская смена роли, ни это описание не заменяют reviewer. `awaiting_script_approval` не достигнут.

## Точное текстовое кольцо Short: две последние → две первые реплики

**EN end→start:**
```text
But most of the cargo was already gone. Thirty years of tides had carried it out to sea.
They had solved the mystery, not the pollution. At the next cleanup, the same strange sight greeted them:
An orange Garfield telephone washed up on a beach in France.
Then another. And another. It kept happening for more than thirty years.
```

**RU end→start:**
```text
Но большая часть груза уже исчезла. За тридцать лет приливы унесли её в море.
Они раскрыли тайну, но не избавились от загрязнения. На следующей уборке их ждала та же странная картина:
На французский пляж вынесло оранжевый телефон в виде Гарфилда.
Потом ещё один. И ещё. Так продолжалось больше тридцати лет.
```

**Author text seam: PASS, provisional.** Кольцо после полного ответа: «найденный контейнер не очистил море» → новая уборка → снова телефон на пляже. Первая фраза понятна новичку без просмотра финала; после просмотра телефон воспринимается как след долгой истории. Риск: S014 и S001 оба говорят о новом телефоне; независимый слушатель может счесть возврат очевидным повтором — тогда редакция петли нужна прежде, чем script gate. **Independent seam: UNVERIFIED. AV/audio seam: UNVERIFIED**, поскольку TTS/изображения/рендер запрещены в этом scope.

## Смысловая эквивалентность EN/RU — авторская проверка
- S001–S005: тот же объект, тридцать+ лет, части глаза/клавиатура, уборка, версия контейнера.
- S006–S010: 2019, фермер, его свидетельство о брате/шторме в 1980-х, пещера/отлив и переход по скалам.
- S011–S013: остатки контейнера, 23 трубки, почти исчезнувший груз; перевод не меняет хронологию и оговорку о свидетельстве.
- S014 → S001: тайна разгадана, загрязнение осталось и уборка повторилась; нет более эффектной альтернативной развязки на русском.
- **Author semantic parity: PASS. Independent bilingual review: UNVERIFIED.**
- Хеши и голосовые тайминги намеренно не выдумываются. Проверка связности сцен/текста — локальный JS exact string match, без repo check/CI.

## Проверка после первого чтения
В отсутствие внешнего независимого reviewer нет отдельного first-listener verdict. Источники и сильнейшая альтернатива перечислены в `research.md`; их не использовали как подсказку фиктивному reviewer. Художественное принятие владельцем: UNVERIFIED.

## 2026-11-13 — exact Shorts seam / source-frame correction

Previous ending only returned to the phone thematically. A cold replay could feel like the narrator starting over. Now the last sentence explicitly introduces the familiar discovery shown in the first line:

**EN:** They had solved the mystery, not the pollution. At the next cleanup, the same strange sight greeted them: An orange Garfield telephone washed up on a beach in France.

**RU:** Они раскрыли тайну, но не избавились от загрязнения. На следующей уборке их ждала та же странная картина: На французский пляж вынесло оранжевый телефон в виде Гарфилда.

S014 is now **planned to reuse** the exact approved S001 paper artwork and matching whole-frame final/start crop; no redundant independent final image. Full repeated listen, independent reviewer, TTS/music/subtitle/AV seam remain **UNVERIFIED**. The factual resolution that the plastic pollution continued is unchanged. This remains an unregistered editorial candidate, not an approved production stage.
