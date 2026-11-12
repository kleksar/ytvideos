# Grain Test 02 — усиленное зерно

Статус: `PRIVATE_YOUTUBE_READY_AWAITING_USER_REVIEW`. Отдельный приватный тест Paper Detour 030; общий production preset не меняется.

Поручение пользователя: первое зерно почти не видно; усилить его, повторить тот же15-секундный YouTube тест и удалить предыдущий тест локально и на YouTube. Удаление относится к `PD030_GRAIN_01_15S_2160P.mp4` / video ID `8PwziOHGxag` и его временным визуальным QA-файлам. Чистый71.533-секундный источник параллакса, сцены, монтаж, скрипты и журналы сохраняются.

Изменения относительно Test01: luma RMS1.2→4.8 (×4), Gaussian sigma0.68→1.0 UHD px (FWHM ядра≈2.35px). Сохранены seed20261102, AR(1)rho0.65, monochrome/luma-only, limited-range яркостная маска, 4K/30p и target45Mbps H.264/tune grain. Это тестовая настройка, не гарантия сохранения зерна на YouTube. Чистые исходные кадры берутся заново; зерно не накладывается поверх старого зернистого MP4.

Тот же источник, source frames811–1260: V07–V09, ровно450кадров/15с; существующие параллакс и camera motion не пересчитываются. AAC копируется без нового звука/микса. Сценовые PNG и Palmier не изменяются. Как в Test01, эффект применяется к готовому изображению вместе с бумажными акцентами.

Команды из корня проекта:

```sh
automation/image_motion/.venv/bin/python channels/paper_detour/videos/030_clothing_history/Edit/Grain_Test_20261102/render_grain.py channels/paper_detour/videos/030_clothing_history/Edit/Grain_Test_20261102_v02/preset.json
automation/image_motion/.venv/bin/python channels/paper_detour/videos/030_clothing_history/Edit/Grain_Test_20261102/verify_local.py channels/paper_detour/videos/030_clothing_history/Edit/Grain_Test_20261102_v02/preset.json
```

До удаления прежней выдачи: проверить новый локальный результат и приватную обработанную YouTube загрузку. Для удаления использовать существующий manage-token с youtube.force-ssl; перед записью проверить channels.list(mine=true), владельца обоих видео и точные IDs, после videos.delete204 проверить отсутствие старогоID и сохранность нового. [Документация videos.delete](https://developers.google.com/youtube/data/reference/rest/v3/videos/delete). При неизвестном результате не повторять запись вслепую.

Применены текущие root/channel правила, ytv-video-qa (техническая проверка эффекта) и ytv-youtube-release → youtube-upload. Для этого эпизодного уточнения используется действующее разрешение CURRENT_CONTEXT пропустить повторный Extra High для030; общеканальный стандарт не меняется. Субъективная оценка эффекта остаётся за пользователем; независимый review и полный AV просмотр не заявляются.

Метаданные технического preview: английские title/description; category27; язык en; made-for-kids=false и synthetic disclosure=false сохранены из предыдущего принятого технического upload-контракта. Hashtags/Tags не назначены, custom thumbnail и плейлист не запрошены; автоматический кадр YouTube не выдаётся за принятую обложку.

Локальные технические проверки PASS:450кадров/15.000с,3840x2160/30p,H.264High, BT.709 limited, фактическое видео45.43Mbps; полное декодирование без ошибок. Скопированные AAC-пакеты побайтно совпали с тем же trim исходника. SHA-256 чистого источника и decoded samples80/243/400 совпали с Test01. Pre-encode RMS4.12-4.80; Cb/Cr до кодирования неизменны. Диагностическая проекция добавленного шума после локального H.264 на плоских полутонах0.59-0.70 (в Test01 было0.30-0.38); это не процент субъективной видимости. Просмотрены final-file samples80/243/400 как full-frame thumbnails и UHD1:1 crops. Отдельно просмотрен pre-encode crop80 clean/Test01/Test02. Полный AV playback и независимая приёмка не заявляются.

## Итог

[Новый приватный Test02](https://www.youtube.com/watch?v=4ZkHRuUEaYE), ID4ZkHRuUEaYE, каналPaper Detour/UCMVfdfaNxV3ZkI3_J3Eejzw. API readback: private, processed, processing succeeded, принятые title/description/languages/category/audience/tags совпали. Плеер:2160p4K,3840x2160@30,VP9(313),BT.709; один экранный кадр музейной сцены просмотрен. Это не полный субъективный AV review и не сравнение1080p. [Квитанция](youtube_receipt.json).

Старый Test01 удалён с YouTube: DELETE204; первое немедленное чтение ещё вернуло старый ресурс, повторной записи не делали. Последующее чтение двухID вернуло только новый ролик; старыйID отсутствует, новый private/processed/succeeded сохранён. [Удаление YouTube](previous_test_delete_receipt.json). Локально удалены15устаревших MP4/YUV/PNG/JPG файлов Test01,200206316байт; отсутствие проверено. Чистый параллакс-источник, новый MP4, код/пресеты и журналы сохранены. [Локальная очистка](previous_test_local_cleanup.json).

Ожидается оценка пользователя. Пресет остаётся экспериментальным, общий skill/production flow не изменён.
