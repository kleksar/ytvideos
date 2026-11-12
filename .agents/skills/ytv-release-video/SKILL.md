---
name: ytv-release-video
description: "Develop thumbnail hooks, AI composition drafts and full-card QA after script approval; schedule a YouTube release after exact MP4 approval and interpret experiment follow-up. Use for packaging, metadata, upload or retesting."
---

# Упаковать и назначить публикацию

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Прочитать task context, [release standard](../../../docs/standards/release.md) и профиль канала. Для `packaging` MP4 approval не нужен. Для `upload`, `configure_release`, `schedule` адаптер обязан проверить точный MP4 approval и scope. Credentials и private signing key остаются в trusted host.

## Packaging после script approval

1. Сверить принятый текст/фильм, artifact hashes, channel ID, язык и права. Прочитать переданную research note. Начать упаковку параллельно с production по [thumbnail standard](../../../docs/standards/thumbnails.md).
2. Сохранить концепты в одном supporting artifact со стабильными IDs; для long — три существенно разных: у **каждого** точное название, полное description, надпись и strict brief `{id,prompt,visual_intent}`. Для каждой пары записать аудиторию/поверхность, promise, жанр/настроение, первое подтверждение, отдельный payoff, вероятное ложное прочтение и выбранный крючок/приём. В long-наборе одна концепция опирается на предмет/действие интро. При переносе референса указать основание; `format_id`, если выбран, сверить с канальным каталогом.
3. Самостоятельно выбрать основной concept ID, если пользователь не указал его. Из его сохранённых title/description собрать strict ReleaseSpec; неизвестные optional hashes опустить. Перед `complete` **выполнить программную сверку exact файлов**: для long сохранены три концепта, все description непустые; title/description ReleaseSpec равны выбранному концепту; QA-title каждого brief совпадает с его концептом. Вычислить длины/UTF-8 bytes и hashes по окончательному ReleaseSpec после последней правки и записать фактические результаты в metadata-check массива `receipt.checks`. Сохранить проверку `thumbnail_plan`; supporting note и briefs остаются отдельными артефактами. `complete` проверяет схему и receipt contract, но само по себе не подтверждает эту сверку.
4. После завершения packaging зарегистрировать обложки через `add-thumbnail-task`; для long — основную и две альтернативы. Сверить все три long IDs в состоянии run. При недоступном image provider задачи остаются pending. В `prompt`/`visual_intent` передать смысл, направление внимания, критерий читаемости черновика и exact title как контекст QA, отдельно от надписи; точные строки копировать из сохранённого концепта.
5. Пройти проверку AI-черновика до детализации по стандарту; первый подходящий файл использовать без лишней генерации. Выполнить QA exact files и полной карточки. С готовым MP4 сверить первое подтверждение/payoff и тон; hashes/bytes связать при `prepare-release`. MP4 review не ждёт упаковку; отдельного approval gate нет.

## Выпуск после exact MP4 approval

1. Сверить capabilities YouTube/API/Studio и календарную политику. Не заявлять доступность функции из старого скриншота. Продолжить независимые части при конкретном blocker.
2. Связать exact MP4/spec и реальные assets через `prepare-release --asset`. Получить `operation-payload`, зарезервировать совпадающий request/current claim через `begin-operation`. Использовать API для поддерживаемых полей, разрешённый UI adapter для остальных. Загружать явно Private.
3. Сохранить resumable session/video ID и actual observation с exact `attempt_id/task_input_hash`. При timeout reconcile существующий handle; не повторять upload вслепую. Shorts thumbnail отправлять только после processing succeeded.
4. Проверить 100% применимых полей: metadata, языки, категория, declarations, thumbnail, manual SRT serving/not draft, playlist, chapters, end screen/related video, права/обработка. Длины строк/UTF-8 bytes и hashes для receipt вычислять командой по exact output; не вписывать оценочные числа как измерения. N_A требует причины из политики/формата/содержания; недоступная обязательная capability остаётся blocker.
5. Прочитать фактический календарь, зарезервировать подходящий слот по действующей политике и сохранить future publishAt. Не задавать дополнительный вопрос о времени, когда политика разрешает выбор. Перечитать channel/video/privacy/date/timezone и сохранить receipt.
6. Сообщить ссылку и подтверждённое расписание. Выполнить разрешённое архивирование по [storage](../../../docs/standards/storage.md). Для thumbnail experiment различать сохранённый plan, фактически настроенный test/readback и отдельный result; записывать mode и точные варианты, не приписывать CTR/watch-time-share чужому варианту и не выводить победителя самостоятельно. Следующий тест готовить по [порядку итераций](../../../docs/standards/thumbnails.md#следующий-тест-и-аудитория): завершённый verdict, выбранный контроль, конкретное изменение или наблюдаемая смена аудитории; сохранять проигравшие, stopped и неопределённые исходы. Через `deferred-actions` проверить сохранённые pending Public/A/B follow-ups; для выполнения нужен подключённый durable host dispatcher. Не выдавать pending за работающий scheduler или scheduled за published.

При узкой metadata-правке сохранить остальные поля, доступ и действующий эксперимент. Дополнительные публикации/посты и изменения чужого календаря не следуют из поручения выпустить один ролик. Честно указывать отсутствие фонового runtime, если последующая задача пока только сохранена.
