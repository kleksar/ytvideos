# FFmpeg montage

`montage.py` собирает готовые изображения, полный звук и экранные субтитры. ChannelSpec выбирает `visual_profile`; `paper`/`nuviko` остаются aliases технического renderer, а не перечнем допустимых production каналов. Полномочия новой run проверяет guarded media adapter.

Нужны Python/Pillow, FFmpeg/ffprobe, доступный encoder и утверждённые fonts. На Mac можно использовать `h264_videotoolbox`; на другом worker явно выбирать доступный encoder, например `libx264`. Наличие default в CLI не подтверждает его работоспособность. `doctor` проверяет конкретное окружение.

Two Ways Lab использует `channel: "two_ways_lab"`, `format: "short"`, 1080×1920 и 30 fps. Локальная конфигурация не подтверждает YouTube ID и не разрешает публикацию. Сцены длятся не менее двух кадров, допускаются статичные кадры и горизонтальный pan. Для готового изображения надписи `lettering_motion` ограничен 2% масштаба и 2° поворота; `x` задаёт смещение от центра, `y` — верх слоя. Проверять края и текст на финальном видео. Необязательный `minimum_scene_frames` задаёт целый минимум от двух кадров для конкретного плана любого канала.

## План

Относительные пути разрешаются от JSON. Для illustrated recipe интервалы `[start_frame,end_frame)` целые, непрерывные, 30 FPS. Paper/Nuviko сцены 120–180 кадров; `role: end_screen` допускает последнюю композицию 300 кадров в long. `enforce_scene_duration: false`/нестандартный canvas — только явно заданная техническая проба, не новый production default.

План содержит `channel`, `format`, `audio`, `audio_contract`, `scenes`, `subtitles`. `audio_contract` связывает exact final mix SHA-256, фактически применённую скорость и файл evidence. Renderer не выбирает музыку, не доказывает скорость по числу и не исправляет неизвестный mix.

У каждой сцены source image, start/end, `direction` (`left_to_right`, `right_to_left`, `none`) и `zoom` (`in`, `out`, `none`). Соседние pan directions и zoom types проверяются независимо. `camera` содержит focus, subject/reason и start/end center/scale. Координаты 0…1 относятся к изображению после приведения к аспекту; scale>1 — теснее. Движение окна вправо означает экранное движение изображения влево. Геометрия проверяет края/focus, но не целое лицо/предмет.

Геометрия/цвет/codec — [delivery](../../docs/standards/delivery.md), художественное движение — [visual](../../docs/standards/visual.md). Paper Frame v03 — архивный ресурс для прежних версий; в новых Paper роликах внешняя декоративная рамка не применяется. Nuviko не принимает произвольные overlays: сценовый текст внутри источника, сверху только штатные subtitles.

## Субтитры и привязка входов

Word map относится к окончательному mix после всех скоростей/обрезок/пауз, с exact transcript. Отдельные source/conform receipts сохраняются. Проверка текста/порядка/frames не доказывает слуховой sync. Семантика/проверка — [audio](../../docs/standards/audio.md).

Код использует pinned channel и format profiles. Paper Short — короткие группы до трёх слов; long — sentence-first grouping с измеренной шириной и синтаксическими ограничениями без жёсткого лимита слов. `subtitles.phrases` и `keep_together` уточняют группы, не меняя точный текст. Exact boundary exceptions содержат измерение/причину; не отключают все constraints.

`--prepare-subtitles` создаёт те же states, `caption_groups.json`, `subtitle_contract.json` и draft `subtitle_review.json`, что полный renderer, без video encode. Fingerprint включает actual inputs, fonts/profiles/code и intervals. Review начинается UNVERIFIED. После реальных semantic/sync/placement checks передать его в `subtitles.review` полного плана. Изменившиеся inputs требуют новой связки checks.

Первое активное слово — `ceil(start_seconds*fps)`. Paper Short сохраняет строку с frame0 до конца, hold предыдущей до новой и последний highlight в паузе. `subtitles.end_frame` — explicit exclusive end для допустимого немого хвоста; hold не растягивает word timings. Смысл, sync и геометрия проверяются отдельно.

## Запуск и contract

```bash
python3 automation/ffmpeg_montage/montage.py --help
```

`--plan-only` сохраняет план, не доказывая export readiness. `--check-settings --export-contract FILE` сравнивает паспорт с действительными arguments без encoding. Полный render требует заполненный `READY_TO_RENDER` export passport и реальные checks. Использовать новые owned `--output`/`--work-dir`, не перезаписывать accepted artifact.

Шаблон паспорта: [export-contract.template.json](../helpers/video-export/assets/export-contract.template.json). В нём нет пользовательского approval. Source/runtime пути задаются окружением; approved font можно явно разместить и указать `font_override:{path,index}` либо `YTV_FONT_OVERRIDE_PAPER/NUVIKO` + `YTV_FONT_INDEX_PAPER/NUVIKO`. Файл/hash фиксируются. Это выбор конкретного разрешённого font asset, не молчаливая замена другой гарнитурой. Тестовый DejaVu не production-эталон.

## Приёмка и загрузка

Рядом с MP4 создаётся `VIDEO.mp4.delivery.json`, привязанный к exact media SHA-256 и frozen render provenance. Сохранять command/passport/code/profile/font snapshots и фактические input hashes. Новая версия рабочего кода не доказывает дефект исторического файла; проверяется его собственный frozen contract.

Delivery record — свидетельство идентичности и выполненных checks, не художественное одобрение. Требуемые user approval/QA/audio/subtitle сведения проверяются adapter/application boundary. `stage-private` старых upload helpers не является разрешением обойти новый MP4 gate.

QA сравнивает фактический MP4 с contract: decode, timestamps/CFR, frame count, geometry/codec/color/range, полный mix и perceptual checks. Не считать равные `r_frame_rate/avg_frame_rate` доказательством CFR и не сравнивать VBR measured average с target как фиксированное равенство. `AUTO_ENGINE_MANAGED`, `STREAM_COPY` и UNKNOWN различаются.

`--scene-cache DIR --scene-cache-max-bytes N` включает bounded cache сценовых clips (default budget 2 GiB). Ключ включает image hash, motion/duration/canvas, encoder/bitrate, engine и FFmpeg identities; смена позиции сцены без изменения её содержания не сбрасывает cache. Hit копируется в owned work directory; LRU удаляет только cache, не исходники. Принятые сценовые inputs и обязательный QA остаются. Замер живого ускорения отделять от синтетических cache tests.

Tests: `python3 -m unittest discover -s automation/ffmpeg_montage/tests`. Синтетические tests не доказывают качество живого ролика или наличие утверждённых fonts на production worker.
