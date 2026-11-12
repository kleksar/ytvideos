---
name: ytv-release-video
description: "Prepare packaging after script approval and complete a fully populated scheduled YouTube release after exact MP4 approval. Use for metadata, thumbnails, upload, scheduling and evidence-based experiment follow-up."
---

# Упаковать и назначить публикацию

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Прочитать task context, [release standard](../../../docs/standards/release.md) и профиль канала. Для `packaging` MP4 approval не нужен. Для `upload`, `configure_release`, `schedule` адаптер обязан проверить точный MP4 approval и scope. Credentials и private signing key остаются в trusted host.

1. Сверить принятый текст/фильм, artifact hashes, channel ID, язык и права. После script approval начать packaging параллельно по [thumbnail standard](../../../docs/standards/thumbnails.md): для long сохранить три разных концепции, у каждой title, brief и полное description, и самостоятельно выбрать основную, если пользователь не указал её. Сверить promise/payoff с текстом; раннюю research note при необходимости прочитать по переданному artifact ID/path. Завершить strict ReleaseSpec с metadata основной пары, опустив неизвестные optional hashes, с проверкой `thumbnail_plan` в `receipt.checks`; остальные концепции/briefs хранить отдельно. Затем через `add-thumbnail-task` получить реальные файлы, выполнить QA и связать hashes/bytes при `prepare-release`. MP4 review не ждёт упаковку; отдельного approval gate нет.
2. Сверить capabilities YouTube/API/Studio и календарную политику. Не заявлять доступность функции из старого скриншота. Продолжить независимые части при конкретном blocker.
3. Связать exact MP4/spec и реальные assets через `prepare-release --asset`. Получить `operation-payload`, зарезервировать совпадающий request/current claim через `begin-operation`. Использовать API для поддерживаемых полей, разрешённый UI adapter для остальных. Загружать явно Private.
4. Сохранить resumable session/video ID и actual observation с exact `attempt_id/task_input_hash`. При timeout reconcile существующий handle; не повторять upload вслепую. Shorts thumbnail отправлять только после processing succeeded.
5. Проверить 100% применимых полей: metadata, языки, категория, declarations, thumbnail, manual SRT serving/not draft, playlist, chapters, end screen/related video, права/обработка. N_A требует причины из политики/формата/содержания; недоступная обязательная capability остаётся blocker.
6. Прочитать фактический календарь, зарезервировать подходящий слот по действующей политике и сохранить future publishAt. Не задавать дополнительный вопрос о времени, когда политика разрешает выбор. Перечитать channel/video/privacy/date/timezone и сохранить receipt.
7. Сообщить ссылку и подтверждённое расписание. Выполнить разрешённое архивирование по [storage](../../../docs/standards/storage.md). Для thumbnail experiment различать сохранённый plan, фактически настроенный test/readback и отдельный result; записывать mode и точные варианты, не приписывать CTR/watch-time-share чужому варианту и не выводить победителя самостоятельно. Через `deferred-actions` проверить сохранённые pending Public/A/B follow-ups; для выполнения нужен подключённый durable host dispatcher. Не выдавать pending за работающий scheduler или scheduled за published.

При узкой metadata-правке сохранить остальные поля, доступ и действующий эксперимент. Дополнительные публикации/посты и изменения чужого календаря не следуют из поручения выпустить один ролик. Честно указывать отсутствие фонового runtime, если последующая задача пока только сохранена.
