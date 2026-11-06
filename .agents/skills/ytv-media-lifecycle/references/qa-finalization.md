# Автоматическое завершение QA

Контракт относится к выборкам кадров, созданным для [внутренней проверки MP4](../../ytv-video-qa/references/export-review.md) или адресного аудита. Создавать выборку по плану QA. Технический receipt не подменяет перечисленные ниже свидетельства frame review. Обычный scratch очищает workspace clean по своему контракту.

Новые проверки используют managed-режим `inspect_video.py --episode --run-id --owner` по [QA contract](../../ytv-video-qa/references/helper-contract.md). Helper эксклюзивно создаёт отдельный синхронный QA-run, пишет кадры в `Work/<run>/scratch/qa`, отчёт/логи/рецепт в `Edit/QA/<run>`, пакетно регистрирует точные кадры и завершает writer. Не использовать ID production/render run. Ошибочная проверка остаётся failed; фоновый writer этим helper не запускается. Безопасная очистка не выводится из exit code или `technical_status`.

## До проверки

В QA plan зафиксировать `required_review_checks` — полный список применимых обязательных проверок из профиля и frozen export contract. Минимум: `stream_metadata`, `full_decode`, `frame_sampling`. Для Paper дополнить применимыми scene/edit, cue, motion, text composition, audio signal/mix, SRT проверками из профиля. Неприменимые проверки обосновать в review, не включать в обязательный список. Слух/independent не превращать в PASS, если они не выполнялись. Helper сохраняет план в отчёте; finalize запрещает сокращать зафиксированный список.

## После фактического review

Сохранить отдельный неизменяемый `Edit/QA/<run>/review.json`, не переписывая технический report. Формат ниже иллюстрирует структуру, а не утверждает реальные результаты:

```json
{
  "version": 1,
  "run": "qa-film-v02",
  "file": "/absolute/episode/Deliverables/film.mp4",
  "sha256": "ACTUAL_MEDIA_SHA256",
  "report_sha256": "ACTUAL_TECHNICAL_REPORT_SHA256",
  "verdict": "PASS",
  "freshness": "CURRENT",
  "reviewer": "actual reviewer",
  "writer_finished": true,
  "required_checks": ["stream_metadata", "full_decode", "frame_sampling"],
  "checks": {
    "stream_metadata": "PASS",
    "full_decode": "PASS",
    "frame_sampling": "PASS",
    "subjective_audio_listening": "UNVERIFIED"
  },
  "inspected_frame_indices": [0, 149, 299],
  "retain_indices": [0, 149],
  "reconstruction_verified": true,
  "evidence": ["Edit/QA/qa-film-v02/edit-binding-and-rebuild-proof.json"]
}
```

`inspected_frame_indices` должен покрывать весь запрошенный набор, а не только извлечённые или размещённые на листе кадры. `retain_indices` — непустой набор нужных реальных кадров; helper копирует их в `Edit/QA-Retention/<run>/` до удаления выборки. Контакт-листы и другие полезные доказательства заранее сохранять в Edit и перечислять в evidence. Исторический frame map сохраняется; finalization manifest связывает его с сохранёнными копиями и удалёнными временными путями.

Evidence содержит фактическую привязку к актуальному edit/dependency/export contract и проверку восстановления кадров из сохранённого видео. `frame_recipe` хранит точный argv FFmpeg, версию, поток, basis и FPS. При проверке восстановления направить последний output argument в **новую** принадлежащую QA-run папку, сравнить реальные кадры/хеши с исходной выборкой и сохранить команду, покрытие и результат. Не исполнять argv из чужого отчёта автоматически. Поле `reconstruction_verified` — свидетельство выполненной проверки, не замена ей. Скрипт проверяет identity и структуру свидетельств, а не достоверность заявленного человеком визуального review или актуальность edit за пределами доступных metadata.

## Одна завершающая команда

```sh
python3 .agents/skills/ytv-media-lifecycle/scripts/workspace.py --episode /absolute/episode finalize-qa \
  --run qa-film-v02 --owner actual-owner --review Edit/QA/qa-film-v02/review.json \
  --root . --policy /absolute/episode/Edit/MediaLifecycle/policy.json --execute
```

После профильного PASS координатор вызывает её автоматически в действующем разрешении; нового вопроса для каждого disposable кадра не требуется. Без `--execute` — проверка/план без копирования и удаления. Встроенный свежий live dependency scan выполняется один раз для набора; невозможность чтения/discovery сохраняет файлы. Source/report/evidence хешируются один раз за операцию, не по одному разу на кадр. Пакетная регистрация пишет manifest один раз; финализация использует append-only журнал prepared/complete на файл и сохраняет итоговый manifest также при исключении.

Успешный результат сообщает число удалённых файлов, logical bytes и `kept` с причинами; physical reclaim APFS неизвестен. Pins/imports/current/другие managed consumers остаются. Смена file identity, source, review/evidence, ошибки scan и незавершённая/failed/abandoned работа блокируют операцию. Проверка обязательных статусов использует итоговый профильный PASS; необязательное UNVERIFIED сохраняется как ограничение. Неизвестные внешние потребители остаются ограничением bounded scan.

После сбоя между prepared и unlink/complete повторная команда сначала сверяет фактические файлы и журнал. Отсутствующий файл без собственного prepared event не принимается за успешное удаление; воссозданный путь отклоняется. При сбое копирования до durable preparation сохраняются исходные кадры; не удалять неизвестную partial retention папку автоматически. Generic `clean` не удаляет batch QA и его сохранённый source.

## Первоначальная регистрация старой выборки

`workspace ... register-qa --run ID --owner OWNER --report Edit/QA/old/report.json --legacy` регистрирует точный frame map существующего завершённого run. Это запись metadata, не удаление/перенос и не закрытие чужого writer. Для старого отчёта без recipe использовать `--recipe Edit/QA/old/reconstruction.json`: отдельный сохранённый JSON с фактическими `argv`, `ffmpeg_version`, `required_review_checks`. Старый отчёт не переписывать. Несовпадающий source, чужая папка кадров, повторная регистрация и незавершённый/failed run не обходятся. После регистрации применяются те же review и finalize; старое UNVERIFIED не повышается автоматически. Рендеры MP4 и исходные активы этим режимом не удаляются.
