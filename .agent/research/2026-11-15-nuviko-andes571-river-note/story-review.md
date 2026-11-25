# Editorial duration comparison — Flight 571 / the river note

**Status:** EDITORIAL_CANDIDATE_UNREGISTERED; no runtime, owner approval, independent reviewer or media. Авторская оценка, не измеренные просмотры. Исторически запрос владельца применён по proposed #124 `7d6bdf7702a2a241a33a21677fce29f26ada9b72` (позднее merged; теперь canonical main). Historical main at reading: `b1be73fbcd2a87dafe34ad65c479d337a26ebd80`. Baseline PR head `1c3e9b786764851a29bbcc764dd59b2ab3e6e7e2`.

**Baseline:** `script.en.txt` SHA-256 `d41c5b39ecef0ad2d6cb5163d9a16d0870e74c4b78e0429a765c713d3c9ab0a0`, `script.ru.txt` SHA-256 `63eda5b97b19fa83b096ef4e63a35ec41d308a5edca7cbe44eb8dff6bc2d673d`. Оба исходных файла и исторический `storyboard.md` **не изменены**, storyboard привязан только к этим исходным bytes; никакой вариант не наследует его сцены, timings, review или approval. Исходная версия сильна сценой с запиской, но для Long не содержит вступительных вопросов и перегружает повторным payoff; варианты написаны с новым композиционным обещанием.

| Версия | Точный текст EN / RU | EN words | Конструкция / хронометраж (не TTS) | Статус |
|---|---|---:|---|---|
| 2m | [EN](variants/02m/script.en.txt) / [RU](variants/02m/script.ru.txt) | 320 | 145–165 wpm + паузы, ~1:50–2:20; **Long 16:9** | полный текст, авторская проверка |
| **5m** | [EN](variants/05m/script.en.txt) / [RU](variants/05m/script.ru.txt) | 709 | 130–150 wpm + паузы, ~4:25–5:20; **Long 16:9** | **рекомендован автором**, без approval |
| 10m | [EN](variants/10m/script.en.txt) / [RU](variants/10m/script.ru.txt) | 1512 | 140–155 wpm + паузы, ~9:20–10:55; **Long 16:9** | полный текст, авторская проверка |

**Exact SHA-256 UTF-8 LF (не заменять хэшем git commit):**

| Версия | EN SHA-256 | RU SHA-256 |
|---|---|---|
| 02m | `267a4a99d8ab9601638381cee811c1582e122c3ba568b84f8052a3942deb8754` | `3420179b0c05c07ddc11c52ef4cb04234ec5cdf73db347b920f5ad4bb3966b95` |
| 05m | `ffe0e60b446a9488e4185a67c91de538466d66192c9682fe2bc523cac75f22ee` | `b0e17903f3b5768221732b791caa71025f7c2f7e7b0fe3f8ad4c93a3d3e5495a` |
| 10m | `23ea655103483634a22e25a017ef533c02780b682eba5bf1649ba72030121dd6` | `ff9fd17b30821bc95a8ebf2ebe88de2048b663f686c64f916ab17304eba69783` |

## Story maps — самостоятельное повествование

- **02m:** вопросы о связи с внешним миром → катастрофа/отмена поиска → голод и лавина → пеший выход втроём/возврат Висинтина → новые горы → пастух передаёт бумагу/карандаш → ответ с камнем → дальний путь Каталана к полиции → вертолёты/16 спасены. Человеческая линия — четырнадцать ожидающих и двое посланцев; минимум биографического контекста.
- **05m:** три вопроса о прекращённых поисках, переходе и реке → ошибка пилотов/импровизированное укрытие → радио/прекращение поисков → тяжёлое решение и лавина → совместная подготовка спального мешка → трое в путь, возврат Висинтина → двое спускаются → Каталан передаёт письменные принадлежности → ответ → Каталан везёт сведения полиции → Паррадо направляет вертолёты → 16 спасены и 29 погибли. Содержательная добавка: аварийное решение о маршруте, практическая подготовка, навигация вертолётов.
- **10m:** вопросы → условия рейса/ошибка навигации → студенты-медики и импровизация укрытия → семья Паррадо, потери и первые попытки выживания → самолёты не замечают группу/радио прекращает надежду → дебаты о пище → лавина и дни под снегом → разведка и снаряжение → недооценённый подъём, развилка Висинтина → хребет разрушает ожидания → длительный спуск/следы человеческой жизни → обмен бумагой/карандашом и письменным ответом → путь Каталана к полиции → поиск с воздуха/ночь ожидания/спасение → ограниченная перспектива воспоминаний и итог действий. Добавка: как каждый выбор влиял на следующую возможность, а не лекция о героизме.

## Авторские оценки — 8 критериев отдельно, 1–10, основания и ограничения

Уверенность оценок художественной силы — **low/medium**, пока не читает независимый first-listener. Цифры не измеряют "человечность" и не прогнозируют retention, CTR или спрос. Последний критерий без валидного одинакового baseline остаётся UNVERIFIED.

| Критерий | 02m | 05m | 10m |
|---|---|---|---|
| Значимость / интерес | **8** — поиск прекращён, но 14 ждут | **8** — дополнен разворот с лавиной | **8** — персональные потери и решения, риск известности темы |
| Начало | **8** — вопрос о человеке за рекой, payoff не раскрыт | **8** — три разные ставки: поиск, переход, река | **7** — вопросы конкретны, но третья ставка уже намекает на механизм |
| Развитие / причина досмотреть | **7** — маршрут сильно сжат | **8** — новая трудность меняет задачу на каждом этапе | **7** — середина с выживанием длинная перед выходом |
| Payoff | **8** — Каталан и вертолёты замыкают обещание | **9** — записка только начало, затем ещё нужно найти лагерь | **9** — показана цепочка сообщений, проводника и эвакуации |
| Свежесть угла | **5** — знакомая история, фокус на физической передаче | **6** — расширение роли Каталана и Паррадо | **5** — подробности ближе к известным пересказам |
| Визуальная выразительность | **8** — карта/фюзеляж/река/камень | **8** — лавина, мешок, путь и река | **8** — человеческие и географические масштабы, нет actual assets |
| Ясность устной речи | **8** — повседневные действия; пара чисел | **8** — понятные акторы, умеренный темп | **7** — больше имён и условий, возможна перегрузка |
| Реальный зрительский спрос | **UNVERIFIED** — нет сопоставимого baseline | **UNVERIFIED** — нет analytics | **UNVERIFIED** — нет analytics |

## Жёсткие проверки / конкретные риски

- **Fact-check:** ключевая хронология/числа привязаны к [F1]–[F3] и дополнениям [F8]–[F9] в `research.md`; 10m требует большего доверия к *личному рассказу* Паррадо о первых днях, не к независимому архиву. Ни одна версия не воспроизводит дословную записку или внутренние мысли без источника.
- **EN/RU equivalence:** вручную пройдены все 9/15/29 соответствующих параграфов и причинные тезисы; числовые утверждения, неизвестность маршрута, два дня эвакуации и различие 14 у обломков vs 16 всего сохранены. Перевод смысловой, не буквальный.
- **Long opening:** во всех трёх вопрос(ы) → условия катастрофы и поиска → основное событие/опасность, без повторения вопросов после каждого абзаца.
- **Format:** Nuviko History поддерживает `long 16:9` по `channels/nuviko_history/channel.json`; 2m выбран как compact Long, не Short. Поэтому loop **N_A**; AV seam и видеомонтаж **UNVERIFIED**.
- **Independent reviewer:** UNVERIFIED — реальная `sessions.independent` и `ytv-script-review-v1` недоступны в GitHub-only исполнении. Передать чистый exact EN без этого авторского review, получить подлинные замечания и только потом показывать источники.
- **Timing:** скорость 1.10× профиля не изменена; числа минут — редакторские диапазоны, TTS/паузы ещё не проводились.
- **2m attention risk:** предположительная потеря ясности при переходе от радионовости сразу к тяжёлому решению без времени на отношения в группе.
- **5m attention risk:** описание недостатка еды перед лавиной можно сократить при прослушивании, если замедляет события.
- **10m attention risk:** от семейной истории Паррадо до решения о пище — длинный участок до начала экспедиции; зритель может переключиться, если ждёт разгадки записки. Это гипотеза, не retention.
- **Actual performance/reviews:** audience/CTR/retention, TTS duration, images, MP4 and AV QA remain UNVERIFIED; никакого review receipt/approval не создавалось.

## Сравнение и решение

**2 → 5:** + причина столкновения, реальный расчёт спасения, значение возвращения Висинтина и поиск лагеря с воздуха. Версия 5m отвечает на вопрос «почему записка *ещё не* была спасением сама по себе». Это содержательная ценность, а не растяжение.

**5 → 10:** + история Паррадо и сестры, студенты-медики, работа под лавиной, попытки выйти раньше, несбывшиеся ожидания на хребте и двухэтапная эвакуация. Сильнее личная ставка, но часть материала уводит от физического механизма передачи помощи и воспроизводит знакомую широкую историю катастрофы.

**Рекомендовано редактором: 5m,** не автоматически longest. Она сохраняет личную и событийную линию, доходя до записки без длинной экспозиции. 2m жизнеспособна при более плотном формате. 10m полноценна, но нуждается в отдельном cold-read тесте на отрезке после семейных потерь. Рекомендация не owner approval и не запуск трёх производств.

## Было → стало и progress

- **Было:** один исходный EN/RU ~27 абзацев с фактическим payoff, но первый абзац уже в сцене с пастухом без обязательных Long questions; старые авторские 9/10 не сравнивали хронометражи. 46 сцен лишь для исходного текста.
- **Стало:** три законченных EN/RU на одну историю, отдельные story maps, фактические основания и редакционные недостатки; исходный master и storyboard сохранены без изменения, 6 вариантов хранятся отдельно.
- **Progress:** `не переработан → 3 версии написаны → авторская fact/EN-RU проверка → 5m рекомендована`. Independent first-listener и официальный script gate — **UNVERIFIED**; никакой сценарий не принят. Следующая непроверенная сюжетная ветка: `#109 Chowchilla` или `#106 Tylenol`, с повторной проверкой remote HEAD и статуса в производстве.
- **Exact head:** baseline `1c3e9b786764851a29bbcc764dd59b2ab3e6e7e2`; resulting head записать после read-back коммита в комментарии PR, не подставлять предполагаемый SHA.

---


## Revision 2026-11-19 — missing causal bridge restored

**Before → after.** Ранее все три версии переходили от встречи с пастухом к уже готовой записке, не показывая, как именно возникла возможность писать и почему подтверждение дошло до полиции. Теперь Каталан перебрасывает письменные принадлежности, Паррадо возвращает текст на камне, Каталан добирается до полиции, а Паррадо помогает вертолётам найти оставшихся. В 10m уточнён недоказанный эпитет «раненые» применительно к обоим ходокам и заменён отвлечённый финальный комментарий на подтверждённую связь выживших с Каталаном. Original root scripts and 46-scene storyboard unchanged.

**Current exact SHA-256 (EN / RU):** 02m 267a4a99d8ab9601638381cee811c1582e122c3ba568b84f8052a3942deb8754 / 3420179b0c05c07ddc11c52ef4cb04234ec5cdf73db347b920f5ad4bb3966b95; 05m ffe0e60b446a9488e4185a67c91de538466d66192c9682fe2bc523cac75f22ee / b0e17903f3b5768221732b791caa71025f7c2f7e7b0fe3f8ad4c93a3d3e5495a; 10m 23ea655103483634a22e25a017ef533c02780b682eba5bf1649ba72030121dd6 / ff9fd17b30821bc95a8ebf2ebe88de2048b663f686c64f916ab17304eba69783. EN words 320/709/1512; aligned EN/RU paragraphs 9/15/29. All durations estimate only; no measured TTS.

**Updated story maps.** 02m: search canceled → survival/avalanche → three walkers → two reach river → Catalán supplies paper → Parrado replies → police → helicopters → 16 safe. 05m: flight error → search canceled → hard survival choice → avalanche → sewn sleeping bag → ridge surprise → two-way note → police skepticism → helicopter navigation → all rescued. 10m: same causal spine with family losses, medical response, improvised survival, long climb and descent; added human aftermath tied to Catalán instead of general moralizing.

| Editorial criterion / 10 | 02m | 05m | 10m |
|---|---|---|---|
| Значимость / интерес | 8: 14 stranded; familiar event | 8: roles of all rescuers; familiar event | 8: losses and decades-long bond; familiar event |
| Вступление | 8: river and abandoned search; thin context | 8: three questions tied to answers | 7: many promises and slower start |
| Развитие / досмотр | 7: compressed climb but clear exchange | 8: four successive obstacles | 8: extra police obstacle; early middle still long |
| Payoff | 8: note and helicopters both shown | 9: written relay makes rescue possible | 9: rescue and bond, some overlong final |
| Свежесть угла | 6: specific two-way relay | 6: Catalán's actual work | 6: known story with deeper supporting actions |
| Визуальность | 8: stone/paper/river/helicopter, unrendered | 8: mountain vs police journey, unrendered | 8: rescuer and survivor contrasts, unrendered |
| Речь | 8: concrete action but dense ending | 8: clear causes, natural pauses | 7: many actors and names, needs listener |
| Зрительский спрос | UNVERIFIED: no comparable baseline | UNVERIFIED: no retention/CTR | UNVERIFIED: no retention/CTR |

**Hard checks:** [F1/F2/F10/F11] author-level factual attribution; no invented dialogue or verified exact time of the note; 02m and 05m have intentionally short treatment of long journey, 10m risks losing attention before the expedition. Author checked all corresponding paragraphs for EN/RU meaning and numeric agreement; bilingual independent review UNVERIFIED. All Long 16:9 allowed by ChannelSpec, narrative loop N_A; same storyboard cannot cover these hashes. Independent first-listener/reviewer receipt, owner approval, runtime registration, timings, audience metrics and all AV/media remain UNVERIFIED. **Recommended: 05m** for concrete human actions and a balanced approach to the river; 02m compresses major loss, 10m still spends too long on early exposure. This editorial recommendation is not approval.

## Preserved author baseline review (historical; applies to legacy script only)

# story-review.md — audience-first-v1, самостоятельная авторская оценка

Дата: 2026-11-15. Канал Nuviko History. `English Long 16:9`. Класс **STRONG_CANDIDATE** (только авторская рекомендация). Автор: модель — автор этого текста; настоящий независимый reviewer **не привлекался**. Полный EN master SHA-256 `d41c5b39ecef0ad2d6cb5163d9a16d0870e74c4b78e0429a765c713d3c9ab0a0`, RU SHA-256 `63eda5b97b19fa83b096ef4e63a35ec41d308a5edca7cbe44eb8dff6bc2d673d`, оба exact UTF-8 с LF в конце. Оценка относится именно к этим bytes; после изменения реплики её надо провести вновь, как и проверку EN/RU сцен.

| Критерий | Балл | Конкретное основание | Главный недостаток | Уверенность |
|---|---|---|---|---|
| 1. Интерес и значимость | 9/10 | Зритель узнаёт, как люди без связи и поиска находят способ вывести помощь к другим четырнадцати; моральная тяжесть решения о погибших — реальная, не выдуманная. | История известна из Society of the Snow; часть аудитории знает исход заранее. | medium |
| 2. Честное начало | 9/10 | “A Chilean herdsman looked across a river and saw two strangers waving at him” — наблюдаемое действие, объясняет центральный вопрос о четырнадцати, не обещает неизвестного убийцу или чудо. | Нужно без ошибок показать расстояние через реку; кадр может показаться обычной встречей. | medium |
| 3. Развитие и причина досмотреть | 9/10 | Поиски остановлены → голод и трудное решение → лавина → сшитый спальник → уход трёх и возвращение одного → за гребнем только новые вершины → физическая передача записки. | Средний участок аварии/снежной изоляции слишком узнаваем по экранизациям. | medium |
| 4. Payoff | 9/10 | Записка описывает оставшихся четырнадцать и передаётся Каталану → вертолёты находят обломки → все шестнадцать живых спасены после 72 дней. Обещание «как дошла весть» выполнено. | Зритель, ожидающий подробностей последующей жизни, не получит их в этом Long. | medium |
| 5. Свежесть и отличие | 5/10 | Река, камень, записка и точная причинность спасения — чёткий предметный угол, отличается от #97 Shackleton (шлюпка и неоднократные рейсы). | Уже есть известный фильм и множество аналогов, оба сюжета рассказывают о выживании и походе за помощью. | high |
| 6. Визуальная выразительность | 8/10 | Смена замкнутого корпуса, лавины, хребта без прохода, людей на разных берегах и рукописной записки действительно раскрывает препятствия и решение. | Нужны корректные география/одежда и реальные фото-референсы эпохи, а не случайные горы и позы. | medium |
| 7. EN/RU ясность и речь | 8/10 | “There was no road and no town in sight.” / “Ни дороги, ни города не было видно” — действие и понятный ритм; в обеих версиях без служебного рассказа о фактах. | Авторская вычитка, без прослушивания/независимого EN/RU first listener; не вся плотность гарантированно подойдёт темпу TTS. | low |
| 8. Доказательства зрительского интереса | UNVERIFIED | Проверены реальные публикации Mighty Monk, INTO THE BLACK BOX, ABC News, Todo Noticias и противосигналы; у ТВ TVN была аудитория 2023, Netflix готовит документальный сериал к декабрю 2026. | Нет валидного same-author same-format same-age baseline, доступных комментариев/транскриптов или собственных канал-аналитик; нельзя выставить измеренный балл. | low |

Рабочий порог **1=9, 3=9, 4=9** (не среднее и не эмпирический порог вирусности). Единственная сильная заявка из трёх, выдержавшая сравнение по новому физическому звену спасения и моральной сложности; при этом свежесть всего **5**, зрительский спрос **UNVERIFIED**. Высокие баллы не равны CTR, retention, доле досмотревших или вероятности просмотров.

**Проверка естественности после написания, автор, не independent:** после открытия конкретным пастухом история расширяется до 1972; первая угроза из поиска и голода, тяжёлое решение сказано прямо, не романтизируется; середина меняет условия при лавине и на гребне; финальный камень несёт материальное объяснение спасения четырнадцати. Самое вероятное место потери внимания — два абзаца о еде и лавине, когда опытный зритель уже знает историю. Потенциально отредактировать фразу “The terrain gradually became less frozen” по итогам настоящего first listener, но нельзя менять без нового hash. Этот разбор не выдаётся за `ytv-script-review-v1`.

## Hard checks — отдельно от оценок
- **Фактология: PASS (авторская сверка)** для 45/16/72 дней, хронологии, лавины, похода трёх/возвращения одного, записки о четырнадцати и роли Каталана — NatGeo/TVN, интервью Parrado; ряд связующих обстоятельств остаётся пересказом, не реконструкцией точных движений.
- **Отсутствие буквального дубля и прямого отказа: PASS (GitHub PR/Issue list + main tree 2026-11-15)**; тематическая близость к #97 явно признана. Нельзя трактовать соперника в прошлой выдаче как запрет.
- **Канал: PASS** — `channels/nuviko_history/channel.json`: active, en, illustrated, long 16:9. Не музыкальный nuviko_videos.
- **EN/RU эквивалентность: PASS авторской сверкой 27 пар** (действия, числа, причины и конец), независимый переводчик UNVERIFIED.
- **Exact spans: PASS author / generated from canonical master**; все 27 мастер-абзацев реконструируются из 46 последовательных EN/RU spans. Оценки 4–6s/композиция — не TTS duration и не фактическая длительность.
- **Short loop: N_A** — Long, отдельный AV seam без MP4 UNVERIFIED.
- **Права:** Draft-research-only PASS; **нет** одобрения на media, TTS, imagegen, render, upload, merge, publication или статус канала.
- **Реальный first listener / sessions.independent:** **UNVERIFIED / not performed**, не создано `ytv-script-review-v1`. Изменение EN требует reviewer на новый hash.
- **Официальный `uv run ytv start` и gate:** **NOT ENTERED** — в данном хосте отсутствует локальный checkout с исполняемым проектом и persisted `plan_summary/read_next/task_guide/pinned reference_documents`; нет run ID/lease/receipt/approval.
- **Собственная аудитория:** Studio trends/search terms, CTR/retention UNVERIFIED. vidIQ: 0 credits; публичный YouTube baseline того же автора UNVERIFIED. Никакой видимости в закрытой чужой аналитике.
- **Графика/тайминги:** это текст; actual визуальные PNG героев и кадры, фактический TTS/AV, thumbnail QA и end screen остаются UNVERIFIED.


## 2026-11-25 — reciprocal help replaces recap (current variants)

Baseline 84ab9ef0b75f7d99af1e0f972b3a54170da7a5ed; canonical main a6023668001421b689a8142cebc0bd436545be6b, #124 merged. Original 02m and legacy root/storyboard retained. Previous 05m/10m assessments and timing estimates historical only. **Before:** 05m repeats the rescue chain after the outcome; 10m generalizes friendship then repeats that chain. **After:** documented 2007 medical assistance and reunion complete the relationship established at the river. 10m also removes contested mileage. Sources [F13–F15], no speculative motives or dialogue. Existing core rescue payoff remains before the coda.

| Exact current variant | SHA-256 | Words | Paragraphs |
|---|---|---:|---:|
| variants/02m/script.en.txt | `267a4a99d8ab9601638381cee811c1582e122c3ba568b84f8052a3942deb8754` | 320 | 9 |
| variants/02m/script.ru.txt | `3420179b0c05c07ddc11c52ef4cb04234ec5cdf73db347b920f5ad4bb3966b95` | 279 | 9 |
| variants/05m/script.en.txt | `c845dbeb7fe9c0018bbce8d9c3a30b5d6eb6053de8a8396154fd1dccaae25e83` | 712 | 15 |
| variants/05m/script.ru.txt | `61711e942d887bc133346d51e3c212f7614624e3e0f6e465be75130ab956677e` | 601 | 15 |
| variants/10m/script.en.txt | `46a3cf65f56cba0795278b771ff7df462a2051799f5a113e2707fb605e648059` | 1518 | 29 |
| variants/10m/script.ru.txt | `cbd89e0a84f04e7f866a6497f6b4cb5786abbd8462b935e8e0247d1bf869fbe6` | 1235 | 29 |

| Editorial criterion | 02m unchanged | 05m revised | 10m revised |
|---|---|---|---|
| Interest | 8: rescue of others; familiar event | 8: relationship continues beyond rescue | 8: human stakes and reciprocal action, familiar crash |
| Opening | 8: clear river question; compressed context | 8: questions establish search and river; multiple promises | 7: three questions, slow lead-in |
| Development | 7: compressed expedition | 8: failed search, climb, note, airlift, later assistance | 8: family loss, avalanche, expedition, police, surgeon; prolonged early middle |
| Payoff | 8: all sixteen safe, direct note answer | 9: full rescue then concrete later reversal, no recap | 9: rescue then reunion of clubs whose original match was interrupted |
| Freshness | 6: known disaster | 7: medical reciprocity is a distinct angle | 7: former opposing player becomes surgeon; familiar first half |
| Visual | 8: river and aircraft, unrendered | 8: contrast rescue with later reunion; references needed | 8: clinic/reunion/mountains; archive details and rights unverified |
| Speech | 8: short causal spine | 8: plain verbs, coda adds event | 8: clearer close; early exposition still long |
| Demand | UNVERIFIED | UNVERIFIED | UNVERIFIED |

Author judgment only; confidence medium on text structure and source-grounded coda, low on audience reaction, actual pacing and speech. No averaged pass or fake review. Long 16:9 supported by ChannelSpec; loop N_A. Estimated 05m EN 712 words, 10m EN 1518 words; at assumed 135–155 effective wpm before pauses/end screen, 4.6–5.3 and 9.8–11.2 min, not measured. Actual runtime, independent bilingual/first-listener review, audience demand, permissions, AV and owner approval UNVERIFIED.

**Story maps / paragraph span candidates (EN/RU aligned, not storyboard):** 02m unchanged 1–2 river/stranded group, 3–4 crash/search/avalanche, 5–6 trek and ridge, 7–9 exchange/rescue; 05m 1–2 questions/river, 3–8 crash/shelter/search/food/avalanche/bag, 9–10 expedition, 11–14 note/police/helicopters/rescue, 15 medical help/reunion; 10m 1–4 questions/crash, 5–16 injury/loss/shelter/search/food/avalanche/equipment, 17–21 expedition, 22–27 written relay/airlift/losses, 28–29 surgery/reunion. Visual intent: match the two-way exchange, avoid invented readable note, preserve historical separation of hospital/reunion from 1972; no invented footage or exact medical scene. Legacy 46 scenes are not valid for these variant hashes. No detailed storyboard before selection and review.

**Comparison:** 02m remains a complete compact Long without extended aftermath. 05m provides the meaningful rescue dependencies plus short reciprocal outcome; 10m supplies Jugo's 1972 connection and the commemorative game, but the pre-expedition shelter/food passage still risks losing viewers who expect the river. Recommend 05m provisionally. New 05m/10m hashes require fresh neutral reviewer, source check and selected-version storyboard after owner choice; prior reviewer/timing not carried forward. EDITORIAL_CANDIDATE_UNREGISTERED. Next: other open Long including #106/#109 and technical conflict scope; no production or merge.
