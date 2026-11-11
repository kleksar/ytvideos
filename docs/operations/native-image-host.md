# Native image host: Codex App Server

## Что исполняется

`python -m ytvideos.runtime.image_host` соединяет image outbox с документированным локальным `codex app-server` через stdin/stdout. `probe` выполняет initialize, проверяет ChatGPT authentication и наличие **точной** настроенной модели в `model/list`. Переход на другую модель или API-key billing не выполняется. `run` обслуживает сохранённые image/thumbnail tasks разрешённых каналов. Stories не включён в пример allowlist; source clips никогда не становятся image-generation заданиями.

Каждая задача получает новый persistent thread, собственный рабочий каталог, точный skill input, утверждённые входы, канальный профиль и visual standard. Fork родительского разговора не используется. Имена tools берутся из протокола, не из предполагаемых функций ChatGPT UI. Это локальная интеграция выбранного runtime; она не превращает любой чат в управляемую сессию.

## Предварительные условия

Использовать отдельный authenticated `CODEX_HOME`/host-профиль без сторонних MCP servers и publication credentials. Не копировать секреты из чужих профилей и не изменять настройки личного приложения. Host проверяет `mcpServerStatus/list` именно созданного thread и не отправляет turn при наличии MCP servers. Все server-initiated tool/permission requests отклоняются. Для worker включены ограниченные read/write roots и выключена shell-network access. Это ограничение инструментов, а не замена изоляции OS accounts. Signing key пользовательских approvals, database credentials и YouTube OAuth не должны быть доступны worker OS identity.

Установленный App Server должен поддерживать использованные поля `sandboxPolicy`, skill input, `imageGeneration` item и durable history. Проверять schema установленной версии через `codex app-server generate-json-schema --out <audit-dir>`; не включать экспериментальные permissions и не ослаблять sandbox ради прохождения smoke test. Различать native ChatGPT authentication и Sign in with ChatGPT external-token preview: доступные tools у них могут отличаться.

Конфигурация: [image-host.example.json](../../ops/image-host.example.json). Заменить placeholder model ID фактическим Luna ID из локального каталога, а `work_root` — отдельным абсолютным каталогом **вне** source checkout и production workspace. `host_id` должен стабильно обозначать этот host/auth profile; не давать один ID разным аккаунтам. `runtime_key` должен совпадать с уже подтверждённым runtime всех обслуживаемых runs. Он не увеличивает физические лимиты.

Пример запуска на подготовленном host:

```bash
uv sync --locked --extra media --extra postgres
uv run --no-sync python -m ytvideos.runtime.image_host probe \
  --config /absolute/path/image-host.json
uv run --no-sync python -m ytvideos.runtime.image_host run \
  --config /absolute/path/image-host.json \
  --workspace /absolute/path/production-state
```

`YTV_DATABASE_URL` задаётся окружением, без credentials в command line или Git. Probe не генерирует картинки и не доказывает доступ к image tool. Настройку подключения, billing и реального session cap подтверждают отдельно; host не создаёт эти observations по предположению. Перед запуском обязательны `pool initialize` и общий `shared_review_capacity` по [task contract](task-contract.md).

В storyboard/thumbnail packet `references` — список зарегистрированных artifact IDs либо объектов с `artifact_id`. Host проверяет и копирует эти bytes, а не извлекает их из непрозрачного имени или произвольного URL. Когда references действительно не нужны, нужен предметный `reference_na_reason`; это не разрешение игнорировать обязательный эталон канала. Отсутствующие references/профиль блокируют только свою ещё не отправленную задачу до native call. Её старый outbox packet инвалидируется, освобождая место другим сценам/каналам; после исправления входа применяется обычный revise/unblock. Уже claimed/dispatched попытки этот preflight-путь не изменяет.

## Очередь, восстановление и проверка результата

Host сначала собирает доступные результаты, затем пополняет очередь одной новой сессией за tick. Уже запущенная генерация не должна завершиться для старта следующей. Общие лимиты sessions/review и round-robin остаются в PoolService; `estimated_units` резервируются тем же task claim. При потере связи новые задачи в этом tick не отправляются.

Журнал `image_host_jobs` сохраняет intent перед созданием thread, наблюдённый thread ID перед turn/start, затем turn ID и terminal observation. Запись защищена optimistic version: поздний worker не может затереть более новое состояние. Restart только перечитывает сохранённые threads; thread/start и turn/start из неопределённого состояния не повторяются. Потеря ответа turn/start восстанавливается по единственному turn с **точно совпадающим** dispatch prompt. Недостаточная/неоднозначная история остаётся UNKNOWN.

Результат — ровно один успешный `imageGeneration` item в завершённом turn с совпадающим input. Принимаются проверенные local `savedPath` внутри своего рабочего каталога или inline base64 bytes. AgentMessage «готово», посторонний path, symlink, несколько image items и один `fileId` без локальных bytes не считаются успехом. Image decoder проверяет файл, после чего bytes импортируются в immutable artifact store до записи terminal observation. Повтор доставки не зависит от старого scratch file и не вызывает генерацию.

**Native completion не равно художественной приёмке.** Host не создаёт visual QA receipt и не вызывает `complete`/`accept` за координатора. Результат занимает review credit до настоящей проверки точного файла. После длительного restart просроченный claim восстанавливается через существующий `reconcile-task` после подтверждённого provider outcome, без нового dispatch. Cancel собирает поздний результат для учёта, но не принимает его в выпуск.

Когда утрачены и ответ thread/start, и thread ID, либо журнал не успел сохраниться после claim, автоматический resend запрещён. Координатор видит UNKNOWN и использует фактические provider сведения для reconciliation. Пустой thread/history не доказывает, что отправка не состоится позже. Никаких timeout-based повторов платной операции.

## Граница готовности

Contract tests проверяют JSON-lines на настоящем fixture subprocess; integration tests проверяют Store/PoolService на SQLite и PostgreSQL с синтетическими native observations. Они не подтверждают доступ аккаунта к Luna/image tool, качество рисунка или работу Mac. Для live-приёмки нужны несколько разрешённых генераций, проверка файлов и восстановления на целевой версии App Server.

Это image executor, **не вся автономная ферма**. Он не реализует trusted approval ingress, автоматический QA, общий денежный/API бюджет, календарь/YouTube release, TTS/render dispatch или Public/A/B follow-ups. Run-бюджеты не складываются в общий account budget автоматически. Постоянный запуск требует настроенного host service; существование этой команды не означает, что service уже запущен. Закрытие stdio процесса может оборвать работу; после перезапуска неизвестные provider outcomes не пересоздаются.

Протокол проверен по официальным источникам 11 ноября 2026 года: [App Server](https://developers.openai.com/codex/app-server), [native image item schema](https://github.com/openai/codex/blob/main/codex-rs/app-server-protocol/schema/json/v2/ThreadStartResponse.json). Перед эксплуатацией сверить именно установленную версию, возможности аккаунта и применимые условия использования; не обходить provider limits.

Дочернему App Server передаётся только allowlist переменных окружения запуска (PATH/HOME/CODEX_HOME, locale и системные каталоги). DB URL, signing/provider tokens и произвольные environment variables не наследуются. Это не защищает секреты в файлах: отдельный профиль и проверенный sandbox/OS boundary остаются обязательными.

## Граница отправки и отказ одного worker

После read-only preflight ещё раз проверяются актуальный claim, отмена, code pin и
hashes скопированных входов, непосредственно перед `turn/start`. Если текущий
вызов доказуемо не дошёл до отправки turn, host сохраняет terminal failure с
`host_preflight_no_dispatch` и нулевыми generation units: слот/резерв освобождаются,
задача блокируется до исправления причины. Это не новая автоматическая попытка.
При рестарте одного старого статуса `thread_created` недостаточно для такого
вывода: исход остаётся UNKNOWN, пока не получены реальные сведения.

Deadline RPC охватывает и запись в stdin, и ожидание ответа. Зависшая/частичная
запись делает transport непригодным для новых запросов; автоматического resend
нет. Ошибка после вызова `turn/start` не становится «не отправлено». Повреждённые
items/content в истории конкретного turn изолируются как blocker этой операции,
не прекращая сбор результатов других каналов. Неопределённая операция продолжает
занимать свой слот и review credit. Неструктурированные provider errors не
печатаются в диагностике как доверенные error codes.

После transport failure host больше не выдаёт новые claims, в том числе когда
утрачен thread ID первой попытки. Наблюдение уже известных сессий остаётся
доступным; для возобновления admission требуется перезапуск исправного host.
Так один обрыв не расходует оставшиеся слоты других каналов на заведомо
неотправляемые задачи. Это не подтверждает остановку прежних provider calls.
