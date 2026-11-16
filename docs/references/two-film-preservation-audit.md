# You But Weird: сохранность двух фильмов, 16.11.2026

Это evidence-аудит, не новый production preset и не утверждение, что будущие заставки уже готовы. Пользователь переделывает intro обоих фильмов. Сценарии и принятые визуальные версии остаются неизменными. Общий художественный индекс и точные visual-source hashes: [два эталона](mind-reading-benchmark.md). История звука: [Everyone](everyone-wants-you-sound.md). Правила хранения: [storage](../standards/storage.md).

## Актуальные версии, не previews

| Фильм | Master | Размер / SHA-256 | Source sound bundle |
|---|---|---|---|
| Mind Reading, утверждённая звуковая V2 | `MIND_READING_FINAL_SOUND_V2_1080p30.mp4` | 62139681 / `ba8899e015c308bb491383cbb01c1da3afc374403445719289f4c304fa35a92d` | `MIND_FINAL_SOUND_V2_SOURCES.zip`, 243198613 / `ebb55fa3410e8a38a8780b04b18adccad01fcc5b5289ee0570b15f1e6f41cfc1` |
| Everyone Wants You, последняя доставленная V9 | `EVERYONE_WANTS_YOU_SOUND_V9_1080p30.mp4` | 85898742 / `56fd8a9c475e4077234179d52b389b908497d2d2b7fcb95ad7db9dab1bf9f88c` | `EVERYONE_REFERENCE_SOURCE_V9.zip`, 110879350 / `93738a1dc21952c39173e33256d191476b4cf851724a2d0c6183b63f8dbf4317` |

Оба master — 1920×1080, 30 fps; Mind 208.4 с / 6252 кадра, Everyone 206.6 с / 6198 кадров. Source bundles и master ранее переданы в Library и на Mac с проверкой SHA; этот аудит заново проверил **локальные** ZIP bytes/CRC, включая вложенные ZIP. Не выдавать эту проверку за повторное скачивание Library/Mac или новый restore-render. Полный покомпонентный [inventory](two-film-preservation-inventory.json) содержит hashes и сохранённые source/license records без приватных access IDs.

V9 заменяет v6 как последняя доставленная сборка, но исторический approval v4 и художественное одобрение двух фильмов не расширяются на неизвестные будущие bytes. После жалобы на звук пользователь сообщил, что на YouTube всё хорошо, и остановил расследование. Это не доказывает причину прежнего искажения. Диагностический raw-voice вариант не подменяет V9.

## Как восстановить, не потеряв картинки и права

Sound bundles и visual bundles имеют разные роли:

- **Mind:** sound V2 содержит `final_mix.wav`, SRT, manifests, scripts, реальные SFX/страницы прав, исправленную сцену 081 и вложенный `previous_sources.zip` → `base_sound_sources.zip`. Цепочка содержит готовые MP4, а не все 110 original PNG. Для пересборки с картинок нужны immutable baseline + EN 1.1 derivative + dialogue delta из общего индекса; 35 изменённых PNG дополняют 75 baseline PNG. Исправление 081 сохранять поверх правильной версии, не поверх произвольной старой сцены.
- **Everyone:** V9 sound bundle содержит `rebuild.sh`, исходный готовый freeze MP4, assets, scripts V2–V9, права, SRT и QA. `rebuild.sh` восстанавливает микс и видео из сохранённого MP4. **Это не восстановление из 122 PNG.** Для него нужен `DESIRE_EN_PRODUCTION_SOURCE.zip` из общего индекса с storyboard/prompts, EN narration, timing и render scripts.
- Для Everyone текущие receipts находятся в `desire-sound-v9/`; корневой `RESTORE_VERIFICATION.json` исторический V5. Не использовать старый receipt как проверку V9. Точный master хранится отдельно: новый encode не обязан давать те же MP4 bytes.
- У Mind полные generation invocation IDs исторически неполны. Не изобретать их задним числом. Новые A/B и Flow generations сохранять как новые inputs с собственными hashes, параметрами, исходными bytes и решениями пользователя.

Музыка обоих фильмов — Kevin MacLeod: **Miami Viceroy**, **Constance**; у Everyone также **Chase Pulse**. Исходные MP3/лицензирование сохранены в пакетах. Прямые источники: [Miami Viceroy](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Miami%20Viceroy.mp3), [Constance](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Constance.mp3), [Chase Pulse](https://incompetech.com/music/royalty-free/mp3-royaltyfree/Chase%20Pulse.mp3), [лицензирование](https://incompetech.com/music/royalty-free/licenses/). Обязательный точный `YOUTUBE_MUSIC_CREDITS.txt` брать из пакета своего фильма, включая CC BY 4.0 и изменения произведений. Source records SFX включают авторов, source URLs, CC0 evidence и hashes; сайт/ID сам по себе не является лицензией. Отдельные cues синтезированы или составные: не описывать их как натуральные актёрские записи. `source_records` в inventory сохраняет исходные утверждения пакета, а не новое юридическое заключение или повторную проверку веб-страниц.

## Звуковые решения V7–V9, которые нельзя потерять

Точные времена и уровни принадлежат scripts/manifest соответствующей версии, не округлённым сообщениям:

- После `Alone` пауза перенесена сразу за слово, выдох удалён, пауза сокращена примерно на 33%; относительно V6 удалены 23 кадра. Все downstream события/SRT сдвинуты вместе. Не возвращать случайный вздох на 17-й секунде.
- Вздох облегчения `Finally` уменьшен до 0.67 прежней амплитуды. Различать смысловой foreground и фон, не нормализовать каждый effect одинаково.
- Капюшон V9: 126.040–126.680 с; шарф V8: 126.900–127.620 с. Оба используют разные участки сохранённого `cloth_soft_CC0.mp3`; источник IENBA, Freesound 850705, CC0. Вне изменённого окна PCM не менялся.
- Ручки дверей звучат в течение соответствующей картинки, а не один короткий щелчок; шаги и ткань не маскируют narrator. Удары, двери, `Quick`, окно и приземление привязаны к действию; `fold` в Mind — 69.072727 с, не поздний общий cue.
- Английский голос Bryan `K60rGfHNsqGiO3nscQV3`, скорость 1.1 применяется один раз. Исторические RU записи и 1.0 raw не использовать как финальную речь.

## Почему начало нельзя назвать native 1080p

Исходные Flow `Hand_removing_card_to_reveal_5d2ceff6_720p.mp4` и `Woman_lowering_card_revealing_scene_4ced0759_720p.mp4` были **1280×720, 24 fps, 119 кадров / 4.958333 с**. Последующий 1080p30 export не добавляет исходных деталей. Mind использовал fps30/Lanczos и удержание конца; Everyone — ранее подготовленный 1080p30 intro и freeze. Начало narration на 3.000 с, переход через удержание последнего actual video frame вместо скачка к другой картинке сохраняет удачный замысел, но не устраняет низкое разрешение исходника.

Изменения не всегда собирались заново из PNG: intro/timing правки повторно кодировали готовые MP4 H.264 CRF18. Поздние audio-only V2 Mind и V8/V9 Everyone копировали видеопоток. Поэтому нельзя обещать «потерь не было» только по 1080p в ffprobe. Отдельный сбой V7 preview: он строился из старого V6 preview, не из нового master. Средний bitrate статичного фильма сам по себе не доказывает качество.

В YouTube Studio у Everyone (`pW9pqAYF4WI`) обнаружено имя загруженного файла `EVERYONE_WANTS_YOU_SOUND_V9_PREVIEW.mp4`: 1280×720, 17968814 bytes. Это не master. Для Mind (`Ff0oBdI-AxE`) имя загрузки не подтверждено из-за ошибки Studio. Не переносить вывод первого фильма на второй и не объяснять всё задержкой HD processing.

Следующая пересборка должна использовать сохранённые оригинальные сцены и новые принятые intro, а не chat preview и не цепочку старых master. Поступившие повторно intro также проверены: оба 1280×720/24 fps, 119 кадров/4.958333 с. Новый Mind `Removing_card_to_reveal_scene_7ca19ea2_720p.mp4` (2079824 bytes, SHA-256 `0ede264232afdea915dd033803a09fd1cb7b5f2dda13b76ff5031114b9876aec`) — новый дубль, но снова 720p. Everyone `Woman_lowering_card_revealing_scene_4ced0759_720p(1).mp4` (3349602 bytes, SHA-256 `1dc963b795c65ab382ec54915b8ec8e074ee29f964b9c32b32cb1802a91ee844`) побайтово совпадает с прежним intro. Native 1080p inputs ещё не получены; новая финальная сборка не выполнена. До новой сборки и проверки держать старые inputs; не удалять единственные копии под обещание будущего восстановления.

## Остаточные ограничения

Аудит архива — не listening QA: агент не прослушивал фильмы. Текущий source sound inventory не устраняет неполный mapping imagegen IDs. Новое качество intro не подтверждено: повторно полученные файлы всё ещё 720p; не помечать native1080 заставки готовыми. Исторические visual archive проверки приведены в общем индексе, в этом проходе их remote bytes заново не скачивались. Нет основания объявлять все версии/публикации окончательно сверенными. Корзину и исходные зависимости этот аудит не удалял.

Отдельная локальная проверка новых входов подтвердила декодирование 110/110 Mind PNG и 122/122 Everyone PNG, наличие storyboard/prompts, timing/render scripts, Mind motion plan/исправления 081, последних PCM и SRT. Это подтверждает доступность inputs для полной пересборки визуала, но не выполненный rerender/синхрон нового результата. Требуется перенести intro/hold и итоговые 31 кадр Alone-паузы, сохранив 6252 кадра Mind и 6198 Everyone.
