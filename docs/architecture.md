# Архитектура производства

Модульное Python-приложение хранит состояние и исполняет проверяемые переходы. GPT-6 Luna решает ограниченные творческие задачи; технические адаптеры выполняют side effects. Общий lifecycle не зависит от имени канала.

## Компоненты и ответственность

| Компонент | Ответственность |
|---|---|
| ChannelSpec | Проверенная идентичность, язык, recipe, стиль/голос, календарная политика и capabilities |
| Run / Task | Intent, scope, версии, зависимости, статус, lease/revision, attempts и бюджет |
| Artifact | Неизменяемая версия результата, URI/hash, inputs и provenance |
| Approval | Подлинное событие пользователя на точный script/MP4 artifact и scope |
| Check / receipt | Фактически выполненный метод, coverage, исполнитель и evidence |
| External operation | Уникальный business key, request/outcome, provider handle и reconciliation |
| Store | Транзакции, optimistic concurrency, idempotency, atomic reservations и audit events |
| Task context | Минимальный packet с skill, входами, каналом, выходным контрактом и ограничениями |
| Session backend | Фактический запуск/наблюдение независимой задачи в доступном runtime |

Основные tasks: `research`, `script`, `storyboard`, `audio`, `scene_image`, `subtitles`, `render`, `review`, `packaging`, `upload`, `configure_release`, `schedule`, `verify_publication`. Script/MP4 approvals — человеческие gates, а не задачи, которые модель может сама отметить выполненными.

Production store — PostgreSQL. SQLite применяется для локальной изолированной работы и быстрых контрактных tests. Состояние и audit event записываются атомарно; dispatch восстанавливается из сохранённого состояния, чтобы restart между approval и запуском не терял задачу. Полное event sourcing не требуется: текущее состояние имеет одного владельца, события сохраняют доказательства.

## Не доверять памяти сессии

`next` выводит разрешённые задачи из зависимостей. `context` содержит skill и выбранные документы из единого snapshot run: общие стандарты, профиль и релевантный рецепт канала. Тексты и маршруты связаны с `pins.references`; worker получает содержимое и hashes, а не только названия файлов. Формат — [task contract](operations/task-contract.md#требования-в-контексте). Сессия не перечитывает весь репозиторий перед каждой картинкой и не обновляет общий CURRENT_CONTEXT вручную.

Run закрепляет code/profile/workflow/skills. Новая версия правил не меняет уже начатый run без явной миграции. Worker с другим code pin или устаревшей revision не записывает результат поверх нового. Старые consumers до смены root сохраняют прежний checkout или проверенный snapshot.

Session slot не является сценой: один slot выполняет последовательность независимых заданий. Перед новой задачей нужен подтверждённый context reset либо новая session. Пул начинает с одной задачи, растёт по измеренным service times и уменьшается при backlog, caps/429 или ограничениях бюджета. Подробности — [adaptive workers](architecture/adaptive-workers.md).

## Доверенная граница approval

Approval bridge получает реальное событие пользователя и создаёт подписанный envelope:

```json
{
  "event": {
    "event_id": "host-user-event-id",
    "actor": "verified-user",
    "source": "trusted-host",
    "run_id": "run-id",
    "kind": "script",
    "artifact_id": "artifact-id",
    "sha256": "exact-artifact-sha256",
    "created_at": "RFC3339",
    "scope": "produce_video"
  },
  "signature": "base64-ed25519-signature"
}
```

Verifier использует публичный Ed25519 key `YTV_APPROVAL_PUBLIC_KEY`. Private signing key принадлежит trusted UI/operator host и не доступен модели, subprocess task или Git. Свободный JSON от модели, пользовательская цитата в research и `accepted=true` не становятся одобрением. Event ID дедуплицируется, target/hash/scope проверяются. Формальные поля не доказывают происхождение без действительной подписи.

Репозиторий предоставляет boundary и verifier; конкретное подключение ChatGPT UI к доверенным user events требует host integration. До её проверки `doctor` показывает blocker. Разработка сценария при этом доступна. Локальные test signers не являются production authority.

## Side effects, повторы и отмена

Guard расположен в adapter boundary, а не только в prompt: channel, approval, scope, input revision, lease и operation key проверяются перед отправкой. У credentials нет пути из произвольного model output. Прямой legacy helper не должен стать обходом guarded path для новых runs.

Успешный ответ внешнего сервиса подтверждается read-back. `UNKNOWN` после потери ответа не равен failure: сначала reconcile тот же handle. Гарантия exactly-once для внешнего API не заявляется. Один компонент владеет retry budget; вложенные автоматические retries не умножают расходы.

Отмена запрещает новые tasks/effects. Отправленный upload или provider job может завершиться после отмены; его нужно учесть, а не утверждать откат. Откат версии кода не отменяет уже назначенный YouTube выход.

## Артефакты и скорость

Content-addressed cache связывает результат со всеми реальными inputs, версиями и параметрами. Изменённая сцена инвалидирует свои производные, сохраняя другие. Медиа не хранятся в транзакционной БД или Git; store содержит IDs/URI/hashes. Для нескольких хостов нужен подтверждённый общий storage, сохранение и восстановление которого отдельно проверены.

Платные операции резервируют бюджет до параллельного запуска; результаты согласуют фактическую стоимость. Нулевая настроенная денежная квота не разрешает платные запросы. Subscription-native operation может иметь известную денежную стоимость ноль, сохраняя лимиты runtime/provider и ограничение попыток. `UNKNOWN` cost не подменяется нулём.

## Граница реализации

CLI/store/queue организуют процесс, но сами по себе не создают ChatGPT chats и не гарантируют круглосуточного исполнителя. Подключение actual tools проходит через runtime bridge. Тесты fake backend подтверждают контракт и отказное поведение, а не качество живой картинки или успешный YouTube release.

Существующие adapters TTS/renderer/YouTube сохраняют проверенные технические safeguards. Production deployment, shared storage и available workers проверяются по [runtime](operations/runtime.md). Temporal/Agents API/другой executor могут быть выбраны отдельным ADR после capability prototype; десять каналов сами по себе не требуют Kafka, Kubernetes или набора микросервисов.

Основания проектных решений: [OpenAI latency](https://developers.openai.com/api/docs/guides/latency-optimization), [skill evals](https://developers.openai.com/blog/eval-skills), [agent runtimes](https://developers.openai.com/api/docs/guides/agents), [sandbox lifecycle](https://developers.openai.com/api/docs/guides/agents-api/environments/lifecycle). Эти документы не подтверждают доступ конкретного аккаунта или возможности неустановленного adapter.
