# audience-first-v1 — авторская карточка

Дата: 2026-11-15; класс **STRONG_CANDIDATE (только авторская редакционная рекомендация, не официальный script gate)**; автор: автор этого текста (модель), независимого reviewer **нет**. Канал Paper Detour, English Long. Exact EN master SHA-256 **`8468a81a4379051b388671b2774a2119d8124b41e5e8911f3b187ac8e7e62ea1`** (LF в конце `script.en.txt`). Любая правка master инвалидирует оценки/spans/возможные reviews и требует новый hash.

| № | Критерий | Балл | Точная причина | Слабое место | Уверенность |
|---|---|---|---|---|---|
| 1 | интерес/значимость | **9/10** | обычная упаковка лекарств касается практически каждого, а семь жертв делают вопрос важным | Tylenol более знаком англоязычной аудитории США, чем мировому зрителю | medium |
| 2 | честное начало | **9/10** | «Seven people took a familiar painkiller and died. The killer was never identified.» не обещает разгадку, сразу обозначает событие | могут ждать классический true-crime сюжет вместо дизайна защиты | medium |
| 3 | развитие/досмотр | **8/10** | семья Янус → лаборатория → угроза неизвестного числа бутылок → 31 млн отзыва → письмо без доказательства убийства → FDA | блок о расследовании может прозвучать отчётом без сильной постановки | medium |
| 4 | payoff | **9/10** | три действительных барьера, child-resistant против tamper-evident, practical «do not use if the seal is broken» | зритель, ожидавший личность преступника, не получит её | medium |
| 5 | свежесть угла | **7/10** | причина знакомого фольгированного барьера вместо очередного hunt for killer; события нет в очереди | аналогичные объяснения уже публиковались; есть соседние crime/safety PR | medium |
| 6 | визуальная выразительность | **8/10** | полка, карта разных семей, 31 млн флаконов, физически видимые три барьера сами раскрывают механизм | бумажная постановка может сделать опасность эстетизацией трагедии | medium |
| 7 | естественность EN/RU речи | **8/10** | «Police cars drove...», «The foil was another warning» — конкретные действия и вариативные предложения | это авторская языковая вычитка, без стороннего listener review и TTS | low |
| 8 | доказательства зрительского интереса | **6/10** | независимые Zack, Jon Solo, WTTW + WTTW 4-роликовый baseline и актуальный 2026 documentary interest | 408729 против WTTW median ~420067 — НЕ breakout; независимые baseline, comments, own retention UNVERIFIED | low |

**Порог:** значимость=9, развитие=8, payoff=9 (каждый ≥8), среднее не использовалось. Не прогноз просмотров/CTR/retention. WTTW public Tylenol всего примерно на уровне медианы четырёх примерно ровесников, не выдаём его за доказательство успеха. Предварительный выбор до сценария и полноценные сравнения — research.md.

**Холодное авторское чтение после полного текста:** первый слушатель узнаёт что семь людей погибли, убийца неизвестен, а обещание связано с упаковкой. Место возможной потери внимания — длинный переход между письмом и постановлением FDA; удерживающая содержательная причина — как помочь потребителю без найденного отравителя. Конкретная отдача: «A tamper-evident seal is about a different question: has somebody opened this before me?» Неестественно может звучать нагромождение рядом стоящих трёх объяснений барьеров. Это НЕ независимое чтение и не ytv-script-review-v1.

## Hard checks отдельно от восьми баллов

- Документальные ключевые факты **PASS author checked** (FBI, FDA, Washington Post 1982, AP 2026); отравитель/место вмешательства UNKNOWN и не изображены как установленное.
- Дубль/отказ **PASS на проверенном GitHub open/closed PR/Issues 2026-11-15**; скрытые собственные процессы UNVERIFIED.
- Соответствие каналу **PASS** по свежему ChannelSpec `status=active, language=en, recipe=illustrated`, Long. Не Nuviko Videos.
- EN/RU эквивалентность **PASS авторская сверка 41 пар без пропусков**, независимая переводческая проверка UNVERIFIED.
- Storyboard exact spans **PASS по детерминированной проверке включения и порядка**, реальный timing/image evidence UNVERIFIED.
- Permissions **PASS редакционная заготовка/Draft PR**, no authorization for media, TTS, imagegen, render, upload, merge, publication, channel mutation.
- Narrative Short loop **N_A**: это Long.
- Audience measurement **PARTIAL**, собственные analytics/CTR/retention UNVERIFIED, YouTube comments UNVERIFIED, 0 vidiq credits.
- Actual independent sessions.independent review **UNVERIFIED / NOT PERFORMED**; ytv-script-review-v1 отсутствует, невозможно назвать writer self-assessment независимым.
- Official runtime gate **NOT ENTERED**, текущий GitHub-only host не предоставляет рабочий локальный `uv run ytv start`, `plan_summary`, `read_next`, `task_guide`, pinned reference_documents. Любые run/lease/receipt/approval отсутствуют и не придуманы.
- Paper plane/reference assets actual PNG bytes, voice/music/subtitle/MP4 seam **UNVERIFIED**.

**Независимого verdict и подлинного user approval нет**. Нужен локальный перенос по handoff.md, реальный review на exact hash и только после этого официальный text gate.

## Варианты 2/5/10 после прямого редакционного поручения — 2026-11-16

Baseline PR #106 `072736b139cd600d267526ebd210fd7b9c0b0002`; первоначальные master EN/RU, research и 41 сцен storyboard **сохранены**. Старый EN master SHA-256 `8468a81a4379051b388671b2774a2119d8124b41e5e8911f3b187ac8e7e62ea1`. Предлагаемый контракт: Draft PR #124 `7d6bdf7702a2a241a33a21677fce29f26ada9b72`, **не утверждать его уже слитым в main**. Версии — законченные самостоятельные сценарии одной истории, статус `EDITORIAL_CANDIDATE_UNREGISTERED`, не approval.

| Длительность | Full EN | Полный RU | EN слов | EN SHA-256 | RU SHA-256 |
|---|---|---|---:|---|---|
| 02m | [EN](variants/02m/script.en.txt) | [RU](variants/02m/script.ru.txt) | 250 | `9b849d8cd58754f6f43180014b0a832fe3407f4d720b2e510b6ac918ddeac050` | `b351b4149d8874477347d8c787427463b90177939440787a8ed1d9606e2f729e` |
| 05m | [EN](variants/05m/script.en.txt) | [RU](variants/05m/script.ru.txt) | 653 | `09aa51e83d5cccc9863f9f761d4698fa3bb85b4bdcf3013c23bc1faacfd4b429` | `4b4ead1fb6f1fbc96bea5d4a8ebe61199f0d0e85536c7a74144ac323532948cc` |
| 10m | [EN](variants/10m/script.en.txt) | [RU](variants/10m/script.ru.txt) | 1450 | `0c5eb62cba600034a528139f2b52b4e70f8497aec46003b820eacc229e816ab7` | `39a78e7a3012ecb52bcc9e2c180c33647736783fe1ca06693814cd9a80fa7e55` |

### Сюжетная карта, история изменений и сравнение

**Было:** исходник раскрывал смерти до явной постановки документальных вопросов, а в конце повторял смысл пломбы и нераскрытость дела. **Стало:** у каждого Long сначала конкретные вопросы, затем человеческая причинная история и полная предметная отдача. Старый master оставлен доступной альтернативой без перезаписи.

| Текст | Самостоятельная story map | Добавочная ценность и точное место риска ухода |
|---|---|---|
| 02m | Фольга? → три смерти семьи Янус → Дженсен и флакон → цианид → отзыв → FDA → три барьера | Быстрый завершённый механизм; краткость почти убирает реальную работу медсестры и безрезультатность письма |
| 05m | Три вопроса → семья → доказательство Дженсен → неизвестное число опасных бутылок → отзыв → письмо без обвинения за убийства → правила → барьеры | Нужное развитие и человеческая линия; у перехода от extortion к FDA нужен ясный монтажный вопрос |
| 10m | Исходные вопросы → следственная связь → масштаб риска → неопределённость подозреваемого → конструкция упаковки → правила 1982/1983/1989 → поздняя зацепка 2026 → два разных исхода | Больше проверенной истории, но глава о нормативной поправке и поздняя гипотеза могут выглядеть как справочный хвост после payoff |

**Сравнение готовых текстов:** 02→05 добавляет находку чека/шести капсул, реакцию на угрозу, письмо и разницу child-resistant/tamper-evident: 403 EN слов с новыми причинными шагами. 05→10 добавляет фактические ограничения конкретных действий, уточнения 1983/1989 и 2026, но 785 дополнительных слов после раскрытия ключевой защиты создают риск перегрузки. **Авторская рекомендация — 05m**. 02m не отклонён, 10m закончен, но требует особенно критического независимого чтения. Это не прогноз retention.

### Восемь отдельных редакционных критериев на точных хэшах

Оценки автора, confidence и слабые места приведены ниже, без замены независимого reviewer.

| Критерий | 02m | 05m | 10m | Обоснование, недостаток, confidence |
|---|---:|---:|---:|---|
| Значимость/интерес | 8 | 8 | 8 | Семь погибших и привычная пломба; true-crime зритель не получает имени виновного; medium |
| Честное вопросное начало | 8 | 9 | 8 | Во всех версиях вопросы до погружения; в 10m три вопроса увеличивают входную нагрузку; medium |
| Причинное развитие | 7 | 9 | 8 | 02m сжимает Дженсен; 05m меняет ожидание после каждого свидетельства; 10m поздняя техническая глава; medium |
| Payoff/последствия | 8 | 9 | 8 | Конкретная работа трёх слоёв и честное ограничение безопасности; medium |
| Свежесть угла | 7 | 7 | 6 | Пломба вместо поиска убийцы; десять минут ближе к традиционному объяснителю; medium |
| Визуальная выразительность | 7 | 9 | 8 | Флакон, чек, слои; поздние законы и новый подозреваемый трудно показать без неподтверждённой инсценировки; medium |
| Естественность речи EN/RU | 8 | 8 | 7 | Действия, обычная грамматика, темп; 10m длиннее объяснения, нет слуховой проверки; low |
| Данные зрительского интереса | 6 | 6 | 6 | Предыдущий WTTW около baseline (не breakout); собственные CTR/retention отсутствуют; low |

**Hard checks:** вопросы до основного documentary hook AUTHOR PASS; человеческая линия и payoff AUTHOR PASS с различной глубиной; фактологическая уверенность ограничена источниками в research; RU сохраняет смысл EN AUTHOR PASS; loop N_A (это Long 16:9, ChannelSpec подтверждён); storyboard/scene spans для **новых** редакций UNVERIFIED/NOT PREPARED — прежние 41 сцена относятся к старому hash. Новые текста не наследуют старые timings/reviews/approvals. Ни одной независимой оценки или receipt нет. Для 02/05/10 длительность **оценочная**, EN words 02m:250, 05m:653, 10m:1450; ориентир 135–155 wpm + паузы, не TTS. Реальный голос/длительность/MP4/AV seam и спрос UNVERIFIED. Git-only не означает `awaiting_script_approval`.

### 2026-11-19 substantive 10m revision on exact hashes

Baseline HEAD 300feed5fa63676fbed61c8861f0ab1d11ea0e85. New EN SHA-256 0c5eb62cba600034a528139f2b52b4e70f8497aec46003b820eacc229e816ab7; RU SHA-256 39a78e7a3012ecb52bcc9e2c180c33647736783fe1ca06693814cd9a80fa7e55; EN 1450 words, RU 1215 words, 21 meaning paragraphs per language. 02m, 05m and root unchanged.

Story map 10m: three opening questions → Kasia with father in store → Janus losses and named other victims → Jensen bottle and cyanide → uncertain danger/recall → FDA and three physical barriers → Kasia's adult consequences → still unsolved criminal question and practical tamper warning.

10m eight author scores (not independent): interest 8/10 medium (seven victims, but no perpetrator revealed); opening 8/10 medium (questions sincere but numerous); development 9/10 medium (family to evidence to practical solution, but regulations slow middle); payoff 9/10 medium (daughter examines packaging, killer unresolved); novelty 6/10 medium (many Tylenol documentaries); visuals 8/10 medium (store/flowers/three layers, reconstruction not archival); spoken naturalness 8/10 low (concrete action; TTS unheard); audience evidence 6/10 low (WTTW non-breakout benchmark, no own CTR/retention).

Hard checks: factual link and EN/RU meaning AUTHOR CHECKED against research; Long questions before main hook AUTHOR CHECKED; loop N_A; independent first-listener, bilingual independent review, TTS, AV and real timing UNVERIFIED. Original storyboard 41 scenes applies only to unchanged root EN SHA-256 8468a81a4379051b388671b2774a2119d8124b41e5e8911f3b187ac8e7e62ea1. Rewritten 10m invalidates previous author review/hash, old spans not carried over.

Comparison exact scripts: 2→5 adds Jensen's contested discovery, public recall, letter and how barriers work. 5→10 now adds the family shopping trip, other victims and Kasia's adult consequences; loses pace during 1989 regulatory detail after package payoff. 02m is compressed, 05m is balanced but letter→FDA needs pace, 10m has more human value yet more regulatory tail. Recommend 05m Long, not owner approval. EDITORIAL_CANDIDATE_UNREGISTERED.
