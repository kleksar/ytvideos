---
name: ytv-release-video
description: "Develop thumbnail hooks, AI composition drafts and full-card QA after script approval; perform an explicitly authorized YouTube release after exact MP4 approval. Use for packaging, metadata, upload and retesting."
---

# Упаковать и выполнить порученный выпуск

До действий выполнить [обязательную процедуру](../ytv-start/references/task-execution.md): прочитать pinned skill/требования/точные входы и проверить описанный способ. Пробел или неразрешённый конфликт — blocker затронутого этапа; не подставлять свои defaults и не менять правила ради продолжения.

Прочитать профиль и [release](../../../docs/standards/release.md); для run также task context. Узкая правка без run сначала получает полный набор через `ytv instructions --channel CHANNEL_ID --stage packaging --format short|long`, затем открывает реальные входы, сохраняя scope; команды и gates production ниже относятся к run. `packaging` начинается после script approval. Для `upload`, `configure_release`, `schedule` требуется прямое поручение на выпуск и одобрение точного MP4 в соответствующем scope. Credentials/signing key остаются в trusted host.

## Packaging

1. Сверить script hash, channel ID, язык, права и переданные research artifacts. Разработать концепты по [thumbnails](../../../docs/standards/thumbnails.md#обещание-и-концепты), параллельно production. Требования к AI, приёмам, интро, смыслу и QA принадлежат этому стандарту и профилю.
2. Подготовить [Tags и хештеги](#tags-и-хештеги) по сюжету выпуска. Сохранить концепты со стабильными IDs; для long — три разные пары с точными title, полными descriptions и briefs по [thumbnail contract](../../../docs/operations/thumbnail-contract.md): exact title, prompt/visual intent и зарегистрированные references либо явная причина их отсутствия. Выбрать основной ID самостоятельно, если пользователь не выбрал его. Из сохранённых metadata основной пары собрать strict ReleaseSpec; неизвестные optional hashes опустить.
3. До `complete` программно сверить exact файлы: комплект long-концептов, непустые descriptions, совпадение title/description выбранного концепта с ReleaseSpec и QA-title каждого brief со своим концептом. Вычислить длины/UTF-8 bytes/hashes после последней правки. Сохранить фактические результаты в metadata-check и структурированном `thumbnail_plan` receipt по [thumbnail contract](../../../docs/operations/thumbnail-contract.md). Runtime проверяет комплект, точные metadata и literal duplicates; смысловую разницу и правдивость проверить отдельно, не выдавать schema pass за редакторский verdict.
4. Зарегистрировать thumbnail tasks по [thumbnail contract](../../../docs/operations/thumbnail-contract.md), для long — основной и два альтернативных IDs. Передать в brief конкретный смысл и точный title отдельно от надписи. Недоступный image provider оставляет задачи pending.
5. Проверить AI-композицию до полировки и выполнить [QA точной карточки](../../../docs/standards/thumbnails.md#qa-файла-и-пары) до показа её как готовой. Независимый reviewer сам сохраняет JSON-результат `ytv-thumbnail-review-result-v1`; не писать verdict за него и не заменять его пересказом. Обязательный `thumbnail_review` дословно связывает этот результат с exact artwork/title, concept ID, фактическим текстом на изображении, actual references и canonical phone/crop previews; схема принадлежит [thumbnail contract](../../../docs/operations/thumbnail-contract.md). Пригодный первый файл не регенерировать ради формального финала. После появления MP4 сверить обещание/тон/payoff и связать exact assets через `prepare-release`. MP4 review не ждёт упаковку.

### Tags и хештеги

Для каждого нового выпуска и при порученной правке этих полей выполнить [release standard](../../../docs/standards/release.md#tags-и-хештеги).

1. По сценарию выписать точные имена, прозвища, события и запросы, связывающие героя с действием. Учесть подтверждённые варианты написания и частые ошибки.
2. Для языка и рынка выпуска проверить текущие поисковые подсказки YouTube и релевантность выдачи. Если хештеги выбраны, отдельно проверить подсказки после `#` или выдачу по точной метке. vidIQ использовать по [правилам кредитов](../../../docs/operations/vidiq-credits.md). При ограниченном доступе использовать доступные бесплатные сигналы и подтверждённые названия, указать покрытие.
3. Отобрать точные употребимые варианты, убрать повторы внутри каждого набора и учесть профиль. Заполнить `metadata.tags`; хештеги необязательны, по умолчанию без блока.
4. В metadata-check сохранить дату, язык, рынок, запросы, источники, наблюдения и итоговые списки. Различать подсказки, выдачу и оценки vidIQ. Перед отправкой сверить поля с записью. Перепроверить устаревшие сигналы и любые изменения темы, языка или рынка.

## Выпуск

1. Проверить актуальные YouTube/API/Studio capabilities и календарь. Подготовить exact spec/assets по [task contract](../../../docs/operations/task-contract.md#media-изображения-release); получить `operation-payload`, зарезервировать совпадающий request/current claim через `begin-operation`.
2. Загрузить явно Private. Сохранить resumable handle/video ID и observation с exact `attempt_id/task_input_hash`. При timeout сверить существующую операцию. Shorts thumbnail отправлять после processing succeeded.
3. До Public или расписания для Short и long с речью открыть отдельный SRT по финальному звуку и перечитать дорожки по точному video ID через `captions.list`. При отсутствии ручной дорожки нужного языка загрузить SRT. Подтвердить `serving`, `isDraft=false` и сохранить ID дорожки и SHA-256 SRT в квитанции. Для ранее опубликованного видео при порученной правке дорожки сохранить его доступ. Проверить остальные [требования выпуска](../../../docs/standards/release.md#release-specification) по фактическому read-back.
4. До завершения upload сверить главы с exact MP4 по [release](../../../docs/standards/release.md#главы-и-компактные-credits), сохранить описание и прочитать его обратно. Подготовить и настроить применимый end screen в порученном scope: проверить целевой ID/доступ/релевантность, совпадение с сюжетным мостом и размещение без перекрытия важных деталей; сохранить и проверить элементы, тайминги и target ID. Не выдавать план за настройку; при недоступности записать blocker, не повторять неизвестный результат вслепую.
5. При порученном расписании выбрать разрешённый будущий слот по проверенному календарю, сохранить и перечитать channel/video/privacy/date/timezone. Дополнительный вопрос о времени нужен только при отсутствии применимой политики или существенной неоднозначности.
6. Сообщить ссылку и подтверждённое состояние, включая сохранённые Tags, выбранные хештеги и назначение плейлиста либо статус каждого незавершённого поля. Сохранить receipts и выполнить разрешённое архивирование по [storage](../../../docs/standards/storage.md). Отдельно отметить pending Public/A/B follow-ups из `deferred-actions`; запись не означает подключённый фоновый dispatcher.

Для тематических Shorts → Long, Community Posts, End Screens и плейлистов прочитать [cross-promotion](../../../docs/operations/cross-promotion.md). После подтверждения Public сформировать read-only `cross-promotion-plan` по реальным channel/video/playlist IDs. Community Post готовить как необязательный `ReleaseSpec.community_post` только при самостоятельном полезном угле; он остаётся pending `after_publish` до поддерживаемого Studio execution/read-back. Не заменять UI-операции ссылкой в описании. Фактический playlist membership сверять через API и избегать повторных insert после UNKNOWN.

Для A/B/readback/повторного теста прочитать [thumbnail experiments](../../../docs/operations/thumbnail-experiments.md). Различать plan, подтверждённую настройку и result. При узкой metadata-правке сохранять остальные поля, доступ и действующий эксперимент; выпуск одного ролика не разрешает дополнительные публикации.
