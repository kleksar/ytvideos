---
name: ytv-release-video
description: "Prepare packaging and finish a fully populated scheduled YouTube release after exact MP4 approval. Use for metadata, thumbnails, captions, upload, scheduling and post-publication checks."
---

# Упаковать и назначить публикацию

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Прочитать task context, [release standard](../../../docs/standards/release.md) и профиль канала. Для `packaging` MP4 approval не нужен. Для `upload`, `configure_release`, `schedule` адаптер обязан проверить точный MP4 approval и scope. Credentials и private signing key остаются в trusted host.

1. Сверить принятый текст/фильм, artifact hashes, channel ID, язык и права. Подготовить все применимые поля. После packaging создать `add-thumbnail-task` для обложок в общем image pool независимо от storyboard/render. Для long — три разные концепции; самостоятельно выбрать основную, если пользователь не указал её. Отдельного approval gate нет.
2. Сверить capabilities YouTube/API/Studio и календарную политику. Не заявлять доступность функции из старого скриншота. Продолжить независимые части при конкретном blocker.
3. Связать exact MP4/spec и реальные assets через `prepare-release --asset`. Получить `operation-payload`, зарезервировать совпадающий request/current claim через `begin-operation`. Использовать API для поддерживаемых полей, разрешённый UI adapter для остальных. Загружать явно Private.
4. Сохранить resumable session/video ID и actual observation с exact `attempt_id/task_input_hash`. При timeout reconcile существующий handle; не повторять upload вслепую. Shorts thumbnail отправлять только после processing succeeded.
5. Проверить 100% применимых полей: metadata, языки, категория, declarations, thumbnail, manual SRT serving/not draft, playlist, chapters, end screen/related video, права/обработка. N_A требует причины из политики/формата/содержания; недоступная обязательная capability остаётся blocker.
6. Прочитать фактический календарь, зарезервировать подходящий слот по действующей политике и сохранить future publishAt. Не задавать дополнительный вопрос о времени, когда политика разрешает выбор. Перечитать channel/video/privacy/date/timezone и сохранить receipt.
7. Сообщить ссылку и подтверждённое расписание. Выполнить разрешённое архивирование по [storage](../../../docs/standards/storage.md). Через `deferred-actions` проверить сохранённые pending Public/A/B follow-ups; для выполнения нужен подключённый durable host dispatcher. Не выдавать pending за работающий scheduler или scheduled за published.

При узкой metadata-правке сохранить остальные поля, доступ и действующий эксперимент. Дополнительные публикации/посты и изменения чужого календаря не следуют из поручения выпустить один ролик. Честно указывать отсутствие фонового runtime, если последующая задача пока только сохранена.
