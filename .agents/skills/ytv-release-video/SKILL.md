---
name: ytv-release-video
description: "Prepare packaging and finish a fully populated scheduled YouTube release after exact MP4 approval. Use for metadata, thumbnails, captions, upload, scheduling and post-publication checks."
---

# Упаковать и назначить публикацию

CLI и точные outputs/receipts: [task contract](../../../docs/operations/task-contract.md).

Прочитать task context, [release standard](../../../docs/standards/release.md) и профиль канала. Для `packaging` MP4 approval не нужен. Для `upload`, `configure_release`, `schedule` адаптер обязан проверить точный MP4 approval и scope. Credentials и private signing key остаются в trusted host.

1. Сверить принятый фильм, artifact hashes, channel ID, язык и права. Подготовить все применимые поля. Для long — три разные концепции; самостоятельно выбрать основную, если пользователь не указал её. Точная упаковка не создаёт отдельного approval gate.
2. Сверить capabilities YouTube/API/Studio и календарную политику. Не заявлять доступность функции из старого скриншота. Продолжить независимые части при конкретном blocker.
3. Перед mutation зарезервировать operation key, scope и budget через приложение. Использовать API для поддерживаемых полей, разрешённый UI adapter для остальных. Загружать явно Private.
4. Сохранить resumable session/video ID и перечитать результат. При timeout после отправки выполнить reconcile по существующему handle; не повторять upload вслепую. Shorts thumbnail отправлять только после processing succeeded.
5. Проверить 100% применимых полей: metadata, языки, категория, declarations, thumbnail, manual SRT serving/not draft, playlist, chapters, end screen/related video, права/обработка. N_A требует причины из профиля/формата/capability.
6. Прочитать фактический календарь, зарезервировать подходящий слот по действующей политике и сохранить future publishAt. Не задавать дополнительный вопрос о времени, когда политика разрешает выбор. Перечитать channel/video/privacy/date/timezone и сохранить receipt.
7. Сообщить точную ссылку и подтверждённое расписание. Выполнить разрешённое архивирование по [storage](../../../docs/standards/storage.md). Создать последующие задачи проверки Public и применимого A/B; не выдавать scheduled за уже published.

При узкой metadata-правке сохранить остальные поля, доступ и действующий эксперимент. Дополнительные публикации/посты и изменения чужого календаря не следуют из поручения выпустить один ролик. Честно указывать отсутствие фонового runtime, если последующая задача пока только сохранена.
