# Short 02: ремейк 2 ноября 2026

**Последнее локальное review-видео:** v04, с анимированными верхними акцентами: [MP4](../../Work/short02_accent_motion_fix_20261102_v01/previews/PAPER_DETOUR_001_SHORT02_ACCENT_MOTION_REVIEW_20261102_v04.mp4). В v04 исправлены девять акцентных PNG-клипов V2: вход снизу вверх с одновременным появлением, неподвижная выдержка, выход вверх с затуханием. Голос/A1 и дорожки V1/V3 не менялись; аудиопакеты AAC скопированы из v03 без перекодирования. Технические метаданные и полный decode — PASS; целевой визуальный QA акцентной анимации — PASS; итоговый QA остаётся UNVERIFIED до проверки слышимой синхронизации субтитров. [Отчёт](../QA/short02_accent_motion_fix_20261102_v01/technical/report.json), [кадры входа/выхода](../QA/short02_accent_motion_fix_20261102_v01/technical/c01_entry_exit_frames.jpg), [контакт-лист девяти акцентов](../QA/short02_accent_motion_fix_20261102_v01/technical/accent_motion_contact_sheet.jpg), [план и квитанции правки](../QA/short02_accent_motion_fix_20261102_v01).

Прежние v02/v03 остаются историческими review-кандидатами. Ничего не продвигалось в Deliverables и не загружалось на YouTube.

Базовый MP4 до текущей доработки титров: `../../Deliverables/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_20261102.mp4` (SHA-256 `460e308754dc3cdb7d477d37e3e1d0e816c3114bb51eb3e9eb9a00df30c0fc7c`). Palmier project `31F93804`, canonical timeline `7537BAE9`. Новая рабочая версия сохранена snapshot `Short02 scene07 v03 and ASR subtitle review draft 20261102` в 16:58 2 ноября; это не финальный мастер. Семь цельных диорам вместо старой послойной компоновки, прямые склейки; целокадровое движение, depth-параллакс, зерно g08. Девять бумажных акцентов заново примерены к сценам. В текущем таймлайне сцена 07 заменена на v03, а титры установлены отдельной дорожкой V3. Название/описание и принятая обложка сохранены с оговоркой об отсутствии независимого повтора.

Дорожка — исходный готовый премикс, служивший основой опубликованного микса до добавления звуков появления букв. Посэмпловая проверка вычитания SFX доказывает совпадение основы в пределах 1 единицы PCM24. Речь и музыка по смыслу/таймингу сохранены; финальный AAC 48 кГц 256 кбит/с закодирован заново. Новых аудиоэлементов нет.

`FINAL_QA.json` относится к более раннему экспорту без текущего V3 ASR-тайминга. Старый публичный ролик `7DygREwtxfY` и частная копия `1PdhvePinFg` в текущем проходе не менялись.

## Субтитры и повторная проверка — 2 ноября

Первая автоматическая разметка и превью подготовлены в `subtitle_build_20261102/` и `subtitle_preview_20261102/`. Синхронизация по слуху не подтверждена.

При просмотре последних групп найдено перекрытие карточек субтитрами в сцене 07. Вариант v02 отклонён; выбран v03 с более высокой композицией, отчёт и provenance — `Source/Images/renewal_20261102/SCENE_REVIEW_v03.md`. Кандидат проверен в движении по восьми точкам с титровым наложением и заменил сцену 07 на timeline `7537BAE9`.

### Текущий титровый черновик

Пословная Whisper-проверка на точном базовом MP4 выявила, что прежние группы начинались с задержкой. Подготовлен review-only overlay `Assets/Generated/renewal_20261102/short02_subtitles_asr_timing_review_20261102.mov`, SHA-256 `6d67a23acb47dd67a3d038d4410797682ab6aea779abff841bdbf189f1e11ca2`, ProRes 4444, 1080×1920, 30 fps, 1098 кадров, без аудио. Он установлен на V3 в Palmier; текст, группировка, дизайн и позиция сохранены. Cue map и карта слов лежат в `subtitle_asr_retime_20261102/`.

ASR — оценка, не подтверждение на слух. Границы фразы “one hundred and two” распределены по токену Whisper `102` пропорционально старому выравниванию и требуют отдельной слуховой сверки. `audible_sync: UNVERIFIED`; поэтому текущий слой, timeline snapshot и прежний MP4 остаются review-материалами, не финальным выпуском. Озвучка и A1 не изменялись. Старый публичный ролик `7DygREwtxfY` и частная копия `1PdhvePinFg` не менялись в этой доработке.

### Повторный визуальный QA кандидата v03

Проведён повторный просмотр всех 403 кадров, запрошенных QA-планом: контакт-листы 01–21 покрывают все семь сцен, 87 пословных групп, девять акцентов, входы/выходы титров и границы склеек; ключевые точки титра `SOFTWARE AS SOUND`, перехода к сцене 07 и последнего слова `Avenger` дополнительно открыты в полном разрешении. Видимых обрезаний, наложения акцента на субтитры или дефекта границы сцены не обнаружено. Самопроверка зафиксирована в `Edit/QA/short02-provider-timing-review-v03-20261102/review.json`; технический отчёт не переписывался.

Ревью-кандидат v03: `Work/short02-provider-alignment-review-20261102/previews/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v03.mp4`, SHA-256 `bd5d071beb1465db056f6c2746da778b74602814675d3f04b2de425ec4685d6f`. Технические проверки потока и полного декодирования — `PASS`; визуальная выборка — `PASS`. Итог `UNVERIFIED`: синхрон на слух, полный аудиосигнал/микс и отдельная проверка движения остаются непроверенными. Это только локальный review-рендер: `Deliverables/current.json`, старые YouTube-версии и публикация не менялись; новый ролик не загружался.

Фактический файл титрового слоя хранится в общих ресурсах выпуска 001: `../../Assets/Generated/renewal_20261102/short02_subtitles_provider_timing_review_20261102.mov`, SHA-256 `2b201b2ed905abea882d9e71ebe8fd619db820d7402467a280d6f14789afd9f3` (119794141 bytes); он импортирован в Short 02 как Palmier mediaRef `1A56E075`.

### Ревью-рендер v02

`Deliverables/PAPER_DETOUR_001_SHORT02_RENEWAL_EN_REVIEW_20261102_v02.mp4` — локальная ревью-копия нового таймлайна, не финальный мастер. SHA-256 `629644be7a4f6c0ca6accd567cd0409c00556f948062846609c00cc52f6da01b`. Технический QA: метаданные, полный decode и извлечение кадров `PASS`; просмотрены все семь сцен по start/mid/end и 41 титровая группа по midpoint, включая motion scene 07. Геометрия титров и проверенные композиции прошли самопроверку. Полное числовое сравнение исходного A1 с MP4 показало нулевой сдвиг и корреляцию `0.99958`; субъективное прослушивание и синхрон титров на слух остаются `UNVERIFIED`. Итог QA `UNVERIFIED`, independent review отсутствует.

Параметры AAC ревью-рендера — engine-managed: AAC-LC stereo, 44.1 кГц, 116107 бит/с. Сравнение с исходным миксом доказывает сильное числовое соответствие, но не воспринимаемое качество и не синхронизацию титров. Текущий MP4 создан только для ревью. Экспортный паспорт и точные QA receipts: `EXPORT_REVIEW_CONTRACT_20261102_v02.md`, `../../../../Edit/QA/short02-review-v02-qa-20261102/`.

### Forced-alignment сверка

Для уточнения “one hundred and two” построен отдельный WhisperX forced-alignment draft по аудио точного ревью-рендера v02 и дословной принятой narration. Все три карты содержат 87 слов в точном порядке. Forced alignment близок к исходному conformed provider alignment (медианное расхождение начала +13 мс; три слова >150 мс), а ASR систематически раньше (медианное расхождение с provider −131 мс; 41 слово >150 мс). В “one hundred and two” провайдер и forced alignment расходятся по началу максимум на 100 мс; ASR начинает слова примерно на 0,3–0,4 с раньше. Это основание для нового review-only кандидата на provider timing, не доказательство синхронизации на слух. Подробная квитанция: `subtitle_forced_alignment_20261102/COMPARISON.md`. `audible_sync` остаётся `UNVERIFIED`; v02 и текущий V3 остаются материалами ревью, не финальной выдачей. Озвучка и дорожка A1 не менялись.

### Targeted motion/framing QA — 2 ноября

По отдельному review-проходу просмотрены пять кадров каждой из семи сцен (35 кадров, включая оба края каждого клипа) именно в локальном v03 MP4. Patch matching по видимым текстурам подтвердил направления панорам и последовательное увеличение масштаба в сценах S03 и S06; результаты сохранены в `../QA/short02_motion_review_20261102_v01/patch_matching.json`. В sampled frames пустых границ, неожиданного обрезания важных объектов, видимых разрывов краёв, деформаций или столкновения субтитров с акцентами не обнаружено. Targeted motion/framing — PASS; это не покадровая проверка всех 1098 кадров. Слуховая синхронизация остаётся UNVERIFIED, общий QA не закрыт, локальный кандидат не продвинут и не загружен. Полный отчёт: `../QA/short02_motion_review_20261102_v01/motion_review.md`.

## Проверка пауз и финала — 3 ноября 2026

На существующем review v04 выборочно проверены кадры в девяти паузах между группами (более 0,25 с по provider cue map) и в финале 36,5 с: предыдущий титр остаётся видимым, последнее слово Avenger в финале выделено жёлтым. Фактические точки и контакт-лист: `../../Work/subtitle_audit_20261103/gap_points.json` и `../../Work/subtitle_audit_20261103/gap_contact.jpg`. Это выборка, не доказательство точного timing на слух или проверки всех кадров. Исходное видео, таймлайн и YouTube не изменялись.


2026-11-03: Accepted review uploaded privately; processing succeeded. Exact video ID, source hash, playlist, thumbnail state and QA limitations: `channels/paper_detour/research/2026-11-03-accepted-shorts-upload/RECEIPT.md`. No previous upload or source deleted.

2026-11-03: User requested public release after disclosure of incomplete checks. New upload is Public (verified API and public oEmbed); detailed receipt `channels/paper_detour/research/2026-11-03-accepted-shorts-upload/RECEIPT.md`. QA limitations remain unchanged; old videos and sources preserved.

2026-11-03: Superseded YouTube versions deleted by user request, new public version verified. Local media cleanup incomplete: Palmier dependency discovery unavailable. Exact IDs, records and audit locations: `channels/paper_detour/research/2026-11-03-accepted-shorts-upload/RECEIPT.md`.
