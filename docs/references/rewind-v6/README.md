# Rewind V6: утверждённый ориентир и сохранность исходников

17.11.2026 Кирилл назвал V6 эталоном и поручил загрузку: `Sentinel_801cb37cc8b8819184548e60edf4f237`. Отдельно `Sentinel_5f544c4a76cc8191880da482a585f69d` разрешает **720p Flow intro при основном фильме 1080p**. Это не разрешение снизить основной визуал до 720p и не утверждение native1080 деталей заставки. Канальный параметр — [PROFILE](../../../channels/scenes_on_repeat/PROFILE.md#экспорт-you-but-weird). Прежние эталоны/approval сохраняются; этот документ не меняет закреплённые runs и не объявляет YouTube upload завершённым.

## Exact master

- `REWIND_REVIEW_V6_1080p30.mp4`, **95150255 bytes**, SHA-256 `ea28bfe616dce34ab5d6492a8c7868a346f0031d2eeb81259b1bb7fc8ab786e4`.
- 1920×1080,30fps,H.264 High;253.966667 с,7619 кадров;AAC48k stereo,320k encoder target. Master/preview decode PASS; post-AAC −16.8LUFS/−1.1dBTP по receipt сборщика, не универсальная норма.
- Только первые 177 кадров/5.9 с заставки кодировались для финальной геометрии;7442 пакета основного video stream совпали с V5. Original intro720p24 приведён к 1080p30. Речь начинается на 3.000 с, сцена 002 на 5.900 с.
- Master доступен в Library; метаданные чтения повторно подтвердили имя/размер. SHA/probe/full decode подтверждены сборщиком на Mac. Этот docs-аудит не скачивал master повторно и не прослушивал его: listening остаётся UNVERIFIED, пользовательская приёмка записана отдельно.
- Пользовательский локатор: `Desktop/You But Weird — Rewind Production/`. Идентичность задают имя/размер/SHA, не только путь. Library access IDs не публикуются в Git.

## Что сохранено и что НЕ восстановлено

**Sound source:** `REWIND_V6_PROJECT.zip`,159995818bytes,SHA-256 `5ef11da5d5a7bd5152f23f04be1e8e0f53efcf30fdc74e80928000117e86fe25`. Library metadata совпадает с локальным размером. Заново проверены локальные SHA/ZIP CRC и каждый member hash, включая вложенныеV5→V4: [inventory](source-inventory.json). CRC PASS не является новым test-render. Public source records убирают машинный префикс абсолютных путей; hashes относятся к исходным bytes внутри ZIP.

Пакет содержит V5 sound project, V4 source package, raw narration/timings/words, music/SFX, licenses/сохранённые HTML, scripts и V6 delta. Последняя безопасная версия аудио — `REWIND_MIX_V6_FINAL_SAFE.flac`; соответствующий PCM `REWIND_MIX_V6_FINAL.wav` имеет SHA-256 `06a9209a2668808f4ddd590591ef6fde5048da58739c798f309afb81b613ebef`. **Ранний non-safe FLAC не подменяет safe файл.** Сам safe mix хранится отдельно от source ZIP; воспроизводимая цепочка ниже восстанавливает звук, а не оригинальные PNG. Sound master250.966667 с до добавления intro; конечный timeline получает+3 с, отдельный paper cue относится к intro.

**Assembly QA:** отдельный небольшой `REWIND_V6_ASSEMBLY_QA.zip` (128251bytes по сборщику) содержит `build_picture.sh`, `assemble_final.sh`, `export-qa-v6.json`, `PICTURE_QA.txt`, SRT и splice QA image. Его hash/полнота в этом docs-аудите не проверены. Он не является полным визуальным исходником.

**Критический recovery gap:** по повторному осмотру сборщика Mac-папка `frames` пуста. EN `narration.en.txt`, `source.original.md` и `audio/timings.json` доступны на Mac, но 140 исходных PNG и полный exact storyboard/prompts были в утраченном cloud workspace; отдельный большой visual-source archive не подтверждён. Contact sheets и готовый master позволяют сохранить вид результата, **не заменяют оригинальные изображения и prompts**. Не заявлять «все исходники сохранены», «полная пересборка изPNG проверена» или удалять master/оставшиеся inputs. Для закрытия пробела нужно найти original generation outputs/архив, восстановить 140PNG+prompts, сверить hashes/сценовые связи и проверить независимую копию. Новая генерация и извлечение кадров изMP4 не считаются восстановлением исходных bytes.

## Карта эффектов, музыка и последние правки

[Историческая V5 cue-карта](cue-manifest-v5-historical.json) сохраняет 128 событий, источники/отрезки, scene IDs, роли,100msRMS сравнение с голосом и основания. Это V5 map: для **итоговогоV6** применять delta из `revise_v6.py` и [V6QA](audio-v6-qa.json), а дляMP4 учитывать+3 с. Не читать прежние peak/RMS как финальные измерения всехV6cue.

- V4 охватывает бытовые действия/реакции, rewind, driving/crash, cabin water, seatbelt/door/window attempts, roof, restrained effort, rescue/shore и broken phone. Не озвучивать успешное открытие там, где действие не удалось; не добавлять вдох, пока герой задерживает дыхание; не повторять phone crack на следующем close-up. Тишина героя после спасения сохранена. Разговорная фактура получена из коротких обращённых слогов принятого narration, без новых слов/TTS; не называть это отдельным актёром.
- V5 все SFX уменьшены до 0.75 амплитуды **один раз**, включая crash/water; narration/music неизменны. Roof122.22 заменён натуральным металлическим ударом. Air-hunger192–199.18 с и плавный water bridge144.05–146.65 с сохранены.
- V6 мужской gasp6.86 с; женский выдох 45.53 с. Generic female sigh, не специально записанная «скука». Вода в reference95–96 с уменьшена до 0.85 прежней амплитуды; другие водяные слои ограничены плавной 100msRMS/250mslookahead-release огибающей. Это конкретный feedback, не preset для любого видео. Shore/swimming SFX не включены в эту водную группу.
- Roof122.22 с усилен примерно+3.52dBRMS локально, компрессия только этого эффекта; нового общего normalizer/limiter для narration нет. V6QA фиксирует отсутствие clipped samples, исходные окна и ограничения метода.
- Intro paper отдельный: source1.10–3.15 с, overlay1.65–3.70 с intro;30ms fade-in/200ms fade-out. Запись шуршания бумаги, не доказанный звук отклеивания стикера.

**Музыка:** Miami Viceroy и Constance, Kevin MacLeod/Incompetech,CC BY4.0. Обязательная атрибуция из [credits](SOURCE_CREDITS.txt) остаётся в публичном description, несмотря на общее предпочтение описаний без music list. Не считать автоматическое распознавание YouTube выполнением лицензии.

**SFX:** inventory/credits сохраняют Joseph SARDIN/BigSoundBank CC0, Freesound primary pages/авторов и фактический способ получения (HQMP3preview или FSD50k mirror). НовыеV6: [female sigh, morganveilleux, 389992](https://freesound.org/people/morganveilleux/sounds/389992/) и [paper, Spaghetto87, 731482](https://freesound.org/people/Spaghetto87/sounds/731482/),CC0. Original synthesized clock/rewind и brass-like sting не выдавать за записи или узнаваемую музыку. Наличие record не является новым юридическим заключением; сохранённые source URLs/license HTML/hash связывают конкретные assets с evidence прав.

## Восстановление звукового проекта

СохранитьZIP/master/safePCM отдельно, сначала проверить hash и CRC. В отдельной рабочей папке распаковатьV6ZIP, вложенный `rewind-v5/REWIND_V5_PROJECT.zip` в `rewind-v5/`, затем его `REWIND_V4_SOURCE_PACKAGE.zip` туда же. Это формирует соседние `rewind-v5/` и `rewind-v6/`.

1. По V5README скопировать его `reconstruct_targets.py` в `rewind-v5/Sound Design V4/`, выполнить оттуда для промежуточных targets, не менять archived original `mix_v4.py`.
2. Выполнить `reconstruct_water.py` из той же папки (он дополнительно вложен вV6ZIP).
3. Использовать bundled `REWIND_MIX_V5_FINAL.flac`, `REWIND_MIX_V4_FINAL.flac` и `SFX_V5_MASTERED.flac`; при нужде декодироватьFXFLAC вWAV без нового lossy encode.
4. Выполнить `rewind-v6/revise_v6.py` с Python3+numpy+scipy+FFmpeg. Сверить resultPCM SHA и окнаV6QA; сохранить safe output отдельно. Этот docs-проход проверил архивы/код и прежние receipts, **не выполнял новую полную пересборку**.

Реконструкция точныхMP4bytes обеспечивается сохранённым master, не обещанием повторного encode. Новый микс/визуальная правка требуют своих receipts и точной версии; музыкальные credits и исходники сохраняются вместе с ними. Общие требования и cue-level баланс принадлежат [audio standard](../../standards/audio.md), не числам этого примера.
