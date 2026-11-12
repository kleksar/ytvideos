# Paper 038 — текущий контекст

Канал Paper Detour · Short · английский. Пользовательский сценарий принят дословно. Одобрены MP4 v06 и упаковка, вариант 2.

- Видео: https://www.youtube.com/shorts/vBJE5kdGE5o
- Название: Nine Months at Sea. Then Pattaya.
- Плейлист: Real Stories & Discoveries (`PLEIDCTZ8y2k8`)
- Обложка: вариант 2; выбор подтверждён в YouTube Studio.
- Расписание: 3 ноября 2026, 18:00 Europe/Belgrade (`2026-11-03T17:00:00Z`). При назначении YouTube API подтвердил `private` с этим временем; текущее состояние публикации не проверялось.
- Обработка видео: `succeeded`.
- Календарь Paper проверен по видео; API-проверка не раскрывает Community posts.

Квитанции: [выпуск](Packaging/Metadata/release_v02/release_receipt.json), [расписание](Packaging/Metadata/release_v02/schedule_state_20261103.json). Пользователь одобрил вид субтитров в пробном v11: общая геометрия Shorts хранится в `automation/ffmpeg_montage/profiles/short.json`. Это принятие настроек субтитров; отдельное решение о повторной загрузке видео не получено.

## Хранение — 4 ноября 2026

Пользователь поручил очистку исходников опубликованных видео с сохранением аудио и текста. Свежая API-проверка `vBJE5kdGE5o`: `public`, upload `processed`, processing `succeeded`. Из двух завершённых наборов QA-кадров `Work/paper038-en-v07-review-v02/scratch/` и `Work/paper038-en-v07-caption-fix-v03/scratch/` удалены 1 092 PNG общим логическим объёмом 5 037 236 633 байта; каждый файл зафиксирован с SHA-256 и повторно сверенной идентичностью. [Квитанция](Edit/MediaLifecycle/cleanup-20261104-qa-frames.json); удаление всех 1 092 путей проверено. Аудио и текст сохранены. Остальные медиа выпуска ещё не проверены и не очищены: состояние PARTIAL, не TEXT_ONLY. Освобождение физического пространства APFS отдельно не измерено.

Дополнение к хранению, 4 ноября 2026: API повторно подтвердил `vBJE5kdGE5o` как public, processed, processing succeeded. Локальные изображения, финальные и промежуточные видео и собственные производные удалены по точным спискам; текст и аудио оставлены. Старый проект Palmier и его связи с удалёнными медиа переведены в историческое состояние: монтаж не готов к повторному рендеру. Хранение PARTIAL_TEXT_ARCHIVE из-за сохранённого аудио и архивных записей. Квитанции: [план и результаты](../../../../.agent/audits/cleanup-20261104/episodes-plan.json), [дополнения](../../../../.agent/audits/cleanup-20261104/episodes-extra-plan.json), [связанные файлы](../../../../.agent/audits/cleanup-20261104/pattaya-remaining.json) и [результат](../../../../.agent/audits/cleanup-20261104/pattaya-remaining.json.receipt.jsonl).
