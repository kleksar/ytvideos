---
name: ytv-release-video
description: "Develop thumbnail hooks, AI composition drafts and full-card QA after script approval; perform an explicitly authorized YouTube release after exact MP4 approval. Use for packaging, metadata, upload and retesting."
---

# Упаковать и выполнить порученный выпуск

Прочитать task context, профиль и [release](../../../docs/standards/release.md). `packaging` начинается после script approval. Для `upload`, `configure_release`, `schedule` требуется прямое поручение на выпуск и одобрение точного MP4 в соответствующем scope. Credentials/signing key остаются в trusted host.

## Packaging

1. Сверить script hash, channel ID, язык, права и переданные research artifacts. Разработать концепты по [thumbnails](../../../docs/standards/thumbnails.md#обещание-и-концепты), параллельно production. Требования к AI, приёмам, интро, смыслу и QA принадлежат этому стандарту и профилю.
2. Сохранить концепты со стабильными IDs; для long — три разные пары с точными title, полными descriptions и briefs по [task contract](../../../docs/operations/task-contract.md#источники-и-обложки): exact title, prompt/visual intent и зарегистрированные references либо явная причина их отсутствия. Выбрать основной ID самостоятельно, если пользователь не выбрал его. Из сохранённых metadata основной пары собрать strict ReleaseSpec; неизвестные optional hashes опустить.
3. До `complete` программно сверить exact файлы: комплект long-концептов, непустые descriptions, совпадение title/description выбранного концепта с ReleaseSpec и QA-title каждого brief со своим концептом. Вычислить длины/UTF-8 bytes/hashes после последней правки. Сохранить фактические результаты в metadata-check и `thumbnail_plan` receipt; сама команда `complete` не доказывает эту смысловую сверку.
4. Зарегистрировать thumbnail tasks по [task contract](../../../docs/operations/task-contract.md#источники-и-обложки), для long — основной и два альтернативных IDs. Передать в brief конкретный смысл и точный title отдельно от надписи. Недоступный image provider оставляет задачи pending.
5. Проверить AI-композицию до полировки и выполнить [QA точной карточки](../../../docs/standards/thumbnails.md#qa-файла-и-пары) до показа её как готовой. Обязательный `thumbnail_review` связывает exact artwork/title, независимого reviewer, actual references, canonical phone/crop previews и сохранённые наблюдения; схема принадлежит task contract. Пригодный первый файл не регенерировать ради формального финала. После появления MP4 сверить обещание/тон/payoff и связать exact assets через `prepare-release`. MP4 review не ждёт упаковку.

## Выпуск

1. Проверить актуальные YouTube/API/Studio capabilities и календарь. Подготовить exact spec/assets по [task contract](../../../docs/operations/task-contract.md#media-изображения-release); получить `operation-payload`, зарезервировать совпадающий request/current claim через `begin-operation`.
2. Загрузить явно Private. Сохранить resumable handle/video ID и observation с exact `attempt_id/task_input_hash`. При timeout сверить существующую операцию. Shorts thumbnail отправлять после processing succeeded.
3. Проверить [100% применимых требований](../../../docs/standards/release.md#release-specification) и фактический read-back. `N_A` имеет причину по формату/содержанию/политике; недоступная обязательная capability остаётся blocker. Измерения делать по exact outputs.
4. При порученном расписании выбрать разрешённый будущий слот по проверенному календарю, сохранить и перечитать channel/video/privacy/date/timezone. Дополнительный вопрос о времени нужен только при отсутствии применимой политики или существенной неоднозначности.
5. Сообщить ссылку и подтверждённое состояние. Сохранить receipts и выполнить разрешённое архивирование по [storage](../../../docs/standards/storage.md). Отдельно отметить pending Public/A/B follow-ups из `deferred-actions`; запись не означает подключённый фоновый dispatcher.

Для тематических Shorts → Long, Community Posts, End Screens и плейлистов прочитать [cross-promotion](../../../docs/operations/cross-promotion.md). После подтверждения Public сформировать read-only `cross-promotion-plan` по реальным channel/video/playlist IDs. Community Post готовить как необязательный `ReleaseSpec.community_post` только при самостоятельном полезном угле; он остаётся pending `after_publish` до поддерживаемого Studio execution/read-back. Не заменять UI-операции ссылкой в описании. Фактический playlist membership сверять через API и избегать повторных insert после UNKNOWN.

Для A/B/readback/повторного теста прочитать [thumbnail experiments](../../../docs/operations/thumbnail-experiments.md). Различать plan, подтверждённую настройку и result. При узкой metadata-правке сохранять остальные поля, доступ и действующий эксперимент; выпуск одного ролика не разрешает дополнительные публикации.
