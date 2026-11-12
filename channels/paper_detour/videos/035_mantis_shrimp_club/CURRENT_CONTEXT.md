**Хранение 3 ноября 2026:** локальные медиа удалены по поручению пользователя; актуальная [квитанция](STORAGE_CLEANUP_20261103_SCREENSHOT.md), последующие старые ссылки на медиа могут быть историческими.

## Latest production state — 2026-11-02

- The user requested a complete visual refresh for a richer, more dimensional Paper Detour look. Ten selected scene images in `Source/Images/paper_v03/` feed the isolated still edit `D4A45BE0`; whole-image framing-safe camera motion and depth parallax are on motion target `2436013F`, with no grain and no audio changes.
- A new review preview was exported from the current motion target to `Edit/Previews/Paper Detour 035 — Visual Rework v03 Review.mp4`. It is not a final delivery. SHA-256: `b693be4bf26d33ad609ee7edd6668aee2b4de59e7c3ebba124e00f988c2b0e23`; 58,748,646 bytes; H.264 High, 1080×1920, 30 fps, Rec.709, 1325 frames / 44.166667 s; AAC-LC mono 44.1 kHz. The visible Palmier export sheet was bound to the correct timeline. Export job ID was not captured.
- Offline review helper passed metadata and full decode. I visually inspected 86 requested sample frames in a contact sheet and inspected two cue frames at native resolution. No sampled animal/weapon clipping or exposed canvas; sampled accents are legible. This is sampled self-review, not continuous or independent review.
- Remaining: heard cue/last-word sync, subjective audio listening, continuous loop playback, denser/final motion review and user review. Source narration duration is 44.16 s; alignment metadata ends at 44.24 s; export preserves the full measured source-duration audio stream, but heard sync remains unverified.
- Export contract: `Edit/Export/EXPORT_CONTRACT_v02_REVIEW_PREVIEW.json`. QA plan, report, contact sheet and reviewer receipt: `Edit/QA/preview-v03/`. No upload or publication.

# Текущий контекст — Paper Detour 035

- **Тема и scope текущего поручения:** Paper Detour Short 035 об эволюции охотничьих конечностей ракообразных-богомолов — копьё и молот. Пользователь продолжил работу после одобрения голоса; текущий этап — монтаж. Язык narration — EN; обсуждение RU.
- **Последнее указание пользователя, 2026-11-02:** принятую научную реконструкцию рассказывать прямо как историю; не обсуждать в narration улики, предположения, окаменелости как доказательства, научную атрибуцию и теорию проверки. Источниковые основания и пределы уверенности остаются за кадром в рабочих записях. Не изобретать дополнительные события или причины. Канонический владелец обновлённого правила — root AGENTS §11; сценарная процедура и Shorts standard ссылаются на него.
- **Актуальный текст:** `Source/Script/NARRATION_EN_v06.txt`, принят пользователем; 116 лексических слов (117 пробельных токенов, включая отдельное тире). Начало: `A spear in one mantis shrimp. A hammer in another.` Финал: `And that is how one shared hunting limb became:`. Точный неозвучиваемый стык записан в файле; AV-петля ещё не проверялась.
- **Сюжет:** несколько похожих пар охотничьих конечностей → передняя пара выделяется → в разных линиях её конец становится шипастым орудием или утолщённой ударной булавой. Нет прямой последовательности «копейный вид стал молотным», точных дат или придуманной причины отбора.
- **Источники и границы:** `Source/Research/EVOLUTIONARY_STORY_LEAD_20261102.md` — Haug 2010, Van der Wal 2017/2025, Yaraghi 2018. Ископаемая морфология и филогенетика лежат в основе принятого пересказа, не являются прямой записью предков. Weaver 2012 — только современная механика: `FACTS_AND_SOURCE_CHECK_v01.md`, `FACTUAL_AUDIT_COORDINATOR_20261102.md`.
- **Проверки v06:** личная консультация координатора в Google Chrome, видимая маркировка `Очень высокий`; отдельный фактологический запрос дал конкретную правку: описывать специализированный конец конечности, а не всю конечность как короткую булаву. Правка внесена. Координатор также убрал повторную теоретическую оговорку и заменил `could become` на прямое повествование `became`. Отдельный запрос к той же модели не считается независимой проверкой; координатор сопоставил текст с сохранённой источниковой сводкой.
- **Предыдущие решения:** v01–v03 отклонены за пересказ методов статьи; v04–v05 остаются историей разработки. Предыдущая рекомендация оставить в narration одну «ископаемую улику» отменена прямым указанием пользователя о подаче. Не переносить её в новые версии.
- **Журнал:** `Source/Production/CONSULTATIONS_20261102.md`. Разбор сценариев канала — `CHANNEL_STORY_PATTERN_REVIEW_20261102.md`; полный AV-просмотр архива не заявляется.
- **Разрешение на голос:** 2026-11-02 пользователь написал: «го дальше. разрешаю озвучку». Разрешение относится к английской narration Short 035; музыка и SFX не поручены.
- **Раскадровка:** `Storyboard/STORYBOARD_v01.md` — 9 сцен, принята пользователем к продолжению. Хронометраж около 49 секунд предварительный, до записи и word alignment. Два storyboard-ответа Extra High ошибочно разбивали устаревший 137-словный вариант; их реплики и общий тайминг не перенесены. Сцены сверены вручную с точным v06.
- **Визуальные эталоны:** исходный user reference Paper Detour004 и принятый S01_v01 выпуска033 указаны в `channels/paper_detour/brand/SCENE_IMAGE_REFERENCES.md`; они задают бумажную фактуру, глубину и свет, не персонажей/локации этого выпуска.
- **Предыдущий визуальный набор v02:** `Source/Images/paper_v02/` и его motion review сохранены как история предыдущего этапа; он заменён полным набором `Source/Images/paper_v03/`, указанным в latest production state выше. Старые файлы и таймлайны не удалялись.
- **Экранные акценты:** рабочая партитура v02 — пять PNG-акцентов C03 `ONE LIMB. / TWO WEAPONS?` на S01, C01 `THE EXCEPTION` на S03, C04 `SEPARATE PATHS` на S04, C02 `PIERCE ≠ STRIKE` на S06 и C05 `A NEW ROLE` на S07. S02, S05, S08 и S09 оставлены без текста; S09 сохраняет открытость петли. Варианты и функции: `Source/Production/CAPTION_DECISIONS_v02.md`; cue-sheet, размеры, точные словесные интервалы, кадры и QA: `Source/Production/CUE_SHEET_v02.md`. Новые PNG: `Source/Graphics/accent_pngs_v01/C03_*`–`C05_*`; все пять фактических пар scene/cue примерены в `Source/Graphics/render_v04/`. Интервалы вычислены из автоматического character alignment, координатор не слушал запись заново; речь, sync и последний 0.08 s хвост остаются `UNVERIFIED`.
- **Озвучка:** `Source/Voice/en_v01_lawrence/voice_en.mp3`, 44.16 s, English Lawrence, `eleven_v4`, без параметра скорости; `voice_en.alignment.json` соответствует 686 символам входного текста. Технический QA и измерения в `Source/Voice/en_v01_lawrence/GENERATION_LOG.md`. Пользователь принял звучание: «озвучка ок» (2026-11-02). Независимый слуховой QA и финальный loop playback не заявляются. Музыка/SFX не создавались.
- **Принятие голоса:** пользователь написал «озвучка ок» (2026-11-02); правок голоса не поручено. Автоматические времена акцентов вычислены по alignment, но финальная разметка scene/cue и playback остаются впереди.
- **Монтажная карта:** текущие сцены и интервалы — `Storyboard/STORYBOARD_v02.md` и `Source/Production/SCENE_CUTS_v02.md`, `[0,1325)` без пропусков при 30 fps. S09 возвращается к уже показанной S01 при зацикливании; отдельный второй S01 клип не добавлялся. Alignment последней фразы заканчивается на 44.24 s, таймлайн — на 44.1667 s; проверка последнего 0.08 s хвоста остаётся впереди.
- **История предыдущего motion-safe монтажа v02:** базовый still Timeline 1 `5DFC7333` и копии `684CA938` / `CE143DE4` сохранены без изменений; их snapshot/run history и экспорт относятся к старому набору и хронометражу. Текущие edit/motion IDs и результаты приведены в latest production state выше. Grain не включён.
- **Документированная защита от обрезки:** она уже была и остаётся явной в `ytv-scene-images/SKILL.md#motion-safe-composition`, `ytv-image-motion/SKILL.md` и `ytv-video-qa/references/motion-checks.md`: получить camera envelope до генерации, проверить PNG с фактическими zoom/pan/depth/overlay и промежуточными экстремумами до импорта, затем проверить реальные выходные кадры; статичный кадр и только начало/середина/конец не доказывают motion safety. В этом проходе проблема была в неполном исполнении этого гейта. Добавлен низкоамплитудный preset `framing-safe` в `automation/image_motion/presets.json` с описанием в automation reference; он снижает риск, но не заменяет сценовую проверку и не задаёт универсальную безопасную границу.
- **Предыдущая просмотрочная версия v02:** [Paper Detour 035 Motion Safe Review v02.mp4](Edit/Previews/Paper%20Detour%20035%20Motion%20Safe%20Review%20v02.mp4) и `final-qa-v01` относятся к более раннему монтажу; его тайминг получил `FAIL` и не продвигался. Эти receipts остаются историей QA, не описанием текущего image-motion target.
- **История выдачи:** экспорт старого motion target `CE143DE4` имеет SHA-256 `cdb99ded49513d86e4b2ed1bce26dd175cabc5ce7042497943921a15489c131e`. Попытка `final-export-v01` завершилась abandoned; файла в `Deliverables` нет. Новая версия не экспортировалась и не публиковалась.

Текущая техническая очистка2026-11-02: основной монтаж, титры и звук сохранены; для обновлённого edit требуется новый export/QA. Общая квитанция — `.agent/OVERLAY_CLEANUP_20261102.json` от корня проекта.


<!-- storage-rollout-20261102 -->
Storage layout and current local availability were audited on 2026-11-02: [migration record](Edit/MediaLifecycle/rollout-20261102/REVIEW.md). Imported paths and active work are preserved; use `Deliverables/current.json` together with the episode’s QA and current edit.


## Выпуск на YouTube — 2026-11-02

- По прямому поручению пользователя Short загружен на канал Paper Detour в закрытый доступ. ID `MEqYk1BuBeQ`; ссылка: https://www.youtube.com/shorts/MEqYk1BuBeQ. Свежий API readback: `privacy=private`, `upload_status=processed`, `processing_status=succeeded`; ошибок обработки/отклонения нет.
- Выбранное название: `Mantis Shrimp Evolution: Spear or Hammer?`. В Studio сохранены точное название, описание и обложка `Packaging/Thumbnails/v04/UPLOAD_v04.png`; после обновления Studio показала завершённую обработку HD и ярлык доступа `Ограниченный`.
- Значение аудитории — не для детей. Для платформенного вопроса об изменённом/синтетическом контенте Studio показывает выбранное `No`; API поле `containsSyntheticMedia` в readback не вернул. Иллюстрация стилизована как бумажная диорама, без фотореалистичной поддельной сцены/реального лица.
- В существующие плейлисты Short не добавлен по решению в `Packaging/Metadata/v01/PLAYLIST_ASSIGNMENT.md`; отдельный SRT не запрошен профилем Paper Shorts. Публичная публикация и расписание не выполнялись.
- Финальный файл и его SHA остались прежними. QA: технический `PASS`, общий вердикт `UNVERIFIED`; ограничения: нет независимой проверки и субъективного прослушивания координатором, движение/кадры проверены выборочно, петля не проверена непрерывным воспроизведением. См. `Edit/QA/final-v01/reviewer_receipt.json`.
- Release receipt: `Packaging/Metadata/v01/RELEASE_RECEIPT.json`. Post-upload storage audit/plan созданы в `Edit/MediaLifecycle/postupload-audit-20261102` и `postupload-plan-20261102`; coverage ограничен обнаруженными локальными файлами и live Palmier metadata.


## Проба экранных субтитров Shorts — 2026-11-02

- Пользователь поручил добавить субтитры в Short 035 и приложил скриншот интерфейса Shorts как ориентир безопасной зоны. Локальный просмотрочный вариант `Work/subtitles-shorts-review-v01/previews/035_subtitles_review_v04.mp4`; исходный монтаж и загруженный Private ролик не менялись. Подробности и ограничения — `Work/subtitles-shorts-review-v01/REVIEW.md`, карта групп — `cue_map.json`. Тайминг автоматический, слуховая проверка и проверка на реальном интерфейсе не выполнены. Общий стиль Shorts ещё не утверждён.


## Проба субтитров — ниже и по центру

- По запросу пользователя субтитры сдвинуты с x=70, y=580 на x=115, y=900 (overlay 850×190 на 1080×1920); центр теперь x=540. Локальная версия: `Work/subtitles-shorts-review-v02/previews/035_subtitles_centered.mp4`, SHA-256 `7a6db9fa46ccc86065e39bd22b1652620983d920f9a15786077ecd2f8534177f`. На выборке семи кадров строка местами пересекает силуэт животных; пользователь оценивает композицию. Полное декодирование успешно; AAC побайтово совпадает с источником. Тайминг по автоматической разметке, слуховой QA и проверка интерфейса на устройстве не выполнялись.


## Проба субтитров — максимум три слова

- По запросу пользователя субтитры опущены до y=1120 на 1080×1920 и разбиты на группы максимум из трёх слов. Локальное видео: `Work/subtitles-shorts-review-v03/previews/035_subtitles_three_words.mp4`, SHA-256 `730c5ce7782645626779439fce26c97caade5335154c1caefc4cac23341f0e00`. Полный decode и совпадение AAC с источником проверены, семь кадров просмотрены. В некоторых кадрах субтитры проходят по фигурам животных. Тайминги автоматические; слуховая проверка и проверка на устройстве не проведены. Пользователь предложил разработать автоматическую раскладку по ширине, безопасным зонам и словам; текущие смысловые группы составлены вручную.


## Проба субтитров — ниже, одна строка

- По уточнению пользователя проба опущена на 300 px и каждая группа показана в одной строке, не более трёх слов. Превью `Work/subtitles-shorts-review-v04/previews/035_subtitles_lower_single_line.mp4`, SHA-256 `faaf6e976e6b0fcd1c12a0ce85be718a259735bf20aee7a78b03e855335a9800`. Для длинной группы размер шрифта автоматически уменьшен до вхождения в заданную ширину; группировка по-прежнему ручная. Проверены полное декодирование, совпадение AAC и семь визуальных кадров. Проверка фактического интерфейса Shorts и слуховая синхронизация не выполнены.


## Проба шрифта субтитров — 2026-11-02

- По просьбе пользователя сравнены Trebuchet MS Bold, Avenir Next Demi Bold и Verdana Bold на двух кадрах, сравнительный лист `Work/subtitles-font-review-v01/font_comparison.png`. Предложен Trebuchet MS Bold; полный локальный просмотр `Work/subtitles-font-trebuchet-v01/previews/035_subtitles_trebuchet.mp4`, SHA-256 `59a9b8c4fffe7d98916c500e955a7f0bc1e7b87de294f260e4bd1a0178a9710c`. Одна строка, до трёх слов, положение предыдущей пробы. Полный decode и совпадение AAC выполнены; пользователь ещё не утвердил гарнитуру как стандарт. Слуховой sync и реальный интерфейс Shorts остаются непроверенными.


## Субтитры: Chalkboard SE и отступ 416 px

- По запросу пользователя визуально сопоставлены Chalkboard SE Bold, Arial Rounded и прежний Trebuchet на двух кадрах. Предложен Chalkboard SE Bold; местная проба `Work/subtitles-rounded-font-review-v01/previews/035_subtitles_chalkboard_416.mp4`, SHA-256 `9df1ed5bad3318c4ea9073f99df537e9a4a2660b57e5e432a4a98a116b911f49`; сравнительный лист в том же каталоге. Для всех 117 PNG-состояний видимый нижний край текста и обводки расположен ровно в 416 px от нижнего края 1080×1920. До трёх слов и одна строка; пользователь ещё не утвердил гарнитуру как каналовый стандарт. Полный decode и совпадение AAC выполнены; слуховой sync и интерфейс на устройстве не проверены.


## Автоматические субтитры — 2026-11-02

- Подготовка субтитров — по общему subtitle skill и `automation/ffmpeg_montage/montage.py`. Сохранённая локальная проба: `Work/subtitles-auto-review-v04/previews/generated/shorts_subtitles_review.mp4`; подробности `Work/subtitles-auto-review-v04/REVIEW.md`. 116 PNG-состояний имеют alpha-границу в 416 px от низа, единый размер, одна строка, максимум 3 слова; текст и звук источника сохранены. Итоговая смысловая редактура и слуховой sync остаются непроверенными. В предыдущей ручной пробе фактические PNG уже имели точный отступ, но изменяли базовую линию и иногда размер шрифта; новая проба сохраняет размер, при точном выравнивании видимых краёв базовая линия может сдвигаться из-за формы глифов.


## Субтитры — размер +25%

- По запросу пользователя размер Chalkboard SE Bold увеличен с 58 до 72,5 px; последняя проба `Work/subtitles-auto-larger-v02/previews/generated/shorts_subtitles_review.mp4`, SHA-256 `f987c9d724940085de9138907034806a192a26e5df9f0e026e2aefbc9090d5e3`. Все слои: одна строка, не более трёх слов, отступ до видимого alpha-края 416 px, максимальная ширина с обводкой 718 px. Сохранена прежняя смысловая карта за исключением трёх не помещавшихся групп. Полный decode, совпадение AAC и выборка семи кадров проверены; слуховая синхронизация и интерфейс Shorts на устройстве не проверены. Локальная просмотрочная версия; Palmier и YouTube не изменялись.


## Subtitle review: fixed baseline, 72 px

- User requested consistent visual alignment and 72 px font. Preview: `Work/subtitles-baseline-72-v01/previews/generated/shorts_subtitles_review.mp4`; SHA-256 `24c5b24413751731b91c3bf54708e85945b6d38909cca9c69ae2f398aafacf96`. Chalkboard SE Bold 72 px; fixed baseline y=1479, safe lower boundary at 416 px. Individual visible ink gaps range from 416 to 434 px due to glyph descenders. Full decode and source AAC hash match verified; six frames sampled. Heard timing and actual Shorts UI remain unverified.


## Принятие оформления субтитров — 2026-11-02

- Пользователь оценил последнюю пробу: «Все отлично», попросил сохранить и обновить документацию. Визуальное оформление и базовая линия приняты; точная версия `Work/subtitles-baseline-72-v01/previews/generated/shorts_subtitles_review.mp4` закреплена в policy как просмотрочный эталон.
- Paper Shorts skill и automation reference обновлены; по умолчанию helper выбирает Chalkboard SE Bold 72 px и общую baseline. 416 px в 035 — граница безопасной области, не одинаковый видимый край для всех букв.
- Версия с субтитрами остаётся локальным просмотрочным MP4, смонтирована поверх ранее загруженного видео; в Palmier и на YouTube новая версия не поступала. Автоматическая смысловая разбивка остаётся черновой, полный ручной смысловой разбор, слуховая проверка sync и финальный QA для этой версии не подтверждены. Private video `MEqYk1BuBeQ` относится к версии без непрерывных субтитров.


## Release update — subtitles v02, 2026-11-02

User requested only Spear or Hammer: replace old private upload and publish immediately. New video https://youtube.com/shorts/Bfgcq4rxQT8 was uploaded private, processed, and verified public; old private MEqYk1BuBeQ deletion accepted HTTP 204 and subsequent API lookup returned zero items. See `Packaging/Metadata/v01/PUBLIC_RELEASE_SUBTITLES_v02.json` and `DELETE_OLD_SUBTITLES_v02.json`. Final MP4: `Deliverables/035_mantis_shrimp_evolution_en_subtitles_v02.mp4`, SHA256 `ccd804bfae4cd28d33a4bde4da32209fad5d2226ab66714fb0655adb9a84f3d7`. Palmier ACFE2102 timeline 241D7F83; subtitle alpha is an imported dependency at `Assets/Generated/subtitles-final-v02/subtitles_alpha.mov`. Technical decode and sampled frames checked; exact audio stream matches prior video. Full motion/cue inspection and subjective listening remain unverified: see `Edit/QA/subtitles-final-v02/receipt.json`. Custom thumbnail API accepted/matched; Studio visual preview displayed placeholder, so Shorts cover pixels not verified. No separate SRT requested.


## Плейлисты — аудит канала, 2026-11-02

Public финал `Bfgcq4rxQT8` добавлен последним в Public Real Stories & Discoveries `PLEIDCTZ8y2k8` (position11, прежние 11 записей сохранены) и первым в новую **Public** Science & What If `PLebMpVlzs-vY`. Все video поля и доступ совпали с before. После прямого ответа пользователя «Открыть и добавить на главную» Science & What If открыта, а секция добавлена после Real Stories; API и публичная страница проверены. API-порядок проверен; Studio sorting-mode в этом ходе не проверялся. [Квитанция](../../docs/channel-audit-20261102/step03-playlists/RECEIPT.md).


## Shorts cover correction — channel audit, 2026-11-02

User noticed missing cover on public final `Bfgcq4rxQT8`. Public Shorts card showed an automatic single-animal frame: prior standard-thumbnail API receipt had not verified separate Shorts selection. Existing selected `Packaging/Thumbnails/v04/UPLOAD_v04.png` reused through desktop Studio, saved once, and verified after Studio + public channel Shorts reload. Both now show exact `SPEAR OR HAMMER?` cover. API read-back confirms title/description/tags/languages/category/status/media preserved. No new image generation or video changes. [Receipt and evidence](Packaging/Thumbnails/v04/repair-20261102/RECEIPT.md). Desktop live card checked; phone viewport override ineffective, so mobile verification not claimed.
