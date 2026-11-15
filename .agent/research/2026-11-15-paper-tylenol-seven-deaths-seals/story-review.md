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