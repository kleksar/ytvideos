# Runtime и независимые сессии

Приложение выдаёт задачи и сохраняет их исходы. Фактическое выполнение обеспечивается доступным host/tool bridge: он создаёт независимую сессию или вызывает разрешённый инструмент, передаёт context packet, получает результат и сохраняет receipt. Не предполагать наличие API только потому, что в UI можно открыть новый чат.

## Capabilities

`doctor` должен показывать capabilities с evidence, а не список пожеланий:

- Исполнитель GPT-6 Luna и доступные tools, независимые sessions/subagents и реальные concurrency caps.
- Image generation: submit/wait/poll/reconcile, job handles, ограничения контекста и reset/reuse.
- TTS: нужный voice ID, аккаунт, формат и квота; renderer/FFmpeg/ffprobe, разрешённые encoder/font/profile.
- `audio.listen`: доступное реальное прослушивание narration и финального микса. Анализ сигнала/word map не подтверждает эту capability.
- Workspace/artifact storage, права чтения/записи и доступность нужных immutable inputs.
- YouTube channel OAuth, API quota и обязательные Studio functions; календарная политика/timezone.
- Approval: по умолчанию локальный координатор записывает явное решение владельца через `approve`, без ключей/hooks. `doctor` показывает `approval.local_session`; при настроенном публичном ключе — signed verifier и состояние внешнего bridge.

Missing release capability не блокирует research/script. Missing image capability не отменяет уже созданный звук. Не превращать отсутствие одного backend в глобальную остановку.

Для provider/tool observation различать три состояния: `unobserved` (`available: null`) — в run ещё нет проверенного наблюдения; `available` (`true`) — доступность подтверждена; `unavailable` (`false`) — зафиксирована реальная недоступность. `doctor` не обнаруживает все host tools автоматически. При `unobserved` исполнитель проверяет каталог текущей сессии и доступный deferred discovery, читает task `context`, сохраняет результат через `capabilities` с evidence и снова вызывает `next`. Поле `next_action` указывает этот шаг; отсутствующую запись нельзя предъявлять пользователю как отсутствующий инструмент.

Перед `pool initialize` сохранить observation `sessions.independent` через `capabilities`: `available: true`, фактический `runtime_key` и целочисленный `max_sessions`. Эти два значения должны точно совпадать с initialize payload; `evidence` указывает источник измерения. Все runs одного runtime используют один key и общий лимит. Новый key не создаёт дополнительную физическую capacity. Billing изображений проверяется отдельно; доступность sessions не означает бесплатную генерацию.

## Продолжение незавершённого run в локальном Codex

Hooks необязательны и отвечают только за продолжение сессии. Они не регистрируют согласие; отсутствие hook trust не блокирует `approve` или ручное продолжение через `next`.


[Project hooks](../../.codex/hooks.json) проверяют попытку завершить конкретную production-сессию. `start` и успешный `resume` связывают run, project, workspace и store с фактическим `CODEX_THREAD_ID`; ответ содержит `session_guard`. Для другого host можно явно передать его настоящий `--session-id` в `start`/`resume` и в `claim` для учёта leases. `status`, `plan`, обычный `create` и `claim` сами binding не создают. Ни один hook не выбирает последний или первый run из общей БД.

Если модель вообще не вызвала `start` и не привязала run, guard разрешает остановку: он не может отличить новую production-задачу от maintenance и не придумывает поручение. Для детерминированного входа интегрирующий host должен сам вызвать `start` с фактическим поручением и каналом, связать session ID и передать первый pinned packet **до model generation**. Файл hooks этого не выполняет; отдельный полный host runner здесь не реализован.

**Активация требует действий владельца локального host после проверки изменений.** Установить locked environment по [development](../development.md#локальный-вход), открыть Codex в доверенном checkout, затем в `/hooks` просмотреть и доверить точные четыре определения: `UserPromptSubmit`, `Stop`, `SubagentStop`, `Interrupt`. Новое или изменённое определение требует новой проверки. Репозиторий не меняет host trust/security и не активирует hooks автоматически. Это интеграция локального Codex; наличие файлов не подтверждает работу hooks в ChatGPT Cloud или другом collaboration host. Источник поведения и trust: [официальный hooks contract](https://learn.chatgpt.com/docs/hooks.md).

`Stop` читает текущее сохранённое состояние и проверяет code/context pins. Для готовой задачи или ещё не проверенных capabilities он возвращает `decision: block` с run ID, точной командой `context`, следующим действием и требуемой границей завершения. Это continuation текущей работы, а не новое разрешение. Script/MP4 gate, отмена, подтверждённые blockers, UNKNOWN, чужие leases и исчерпанный применимый бюджет разрешают остановку; независимая доступная задача остаётся поводом продолжить. После проверенного MP4 hook не инициирует release/upload.

Счётчик допускает максимум **три** продолжения одной пользовательской задачи. Он записывается атомарно в локальном ignored workspace проекта и не сбрасывается от нового run version, повторного `start`/`resume` или автоматического continuation turn. `UserPromptSubmit` сохраняет цепочку только для точного `reason`, ранее выданного guard; новый пользовательский запрос снимает прежнюю binding. Для продолжения выпуска в новом запросе нужен `resume`. `SubagentStop` использует `agent_id`, не ID родителя: independent reviewer не возобновляет работу координатора. `Interrupt` снимает binding и не перезапускает исполнение.

SQLite читается в `mode=ro`; PostgreSQL — ограниченным по времени read-only соединением без `Store.initialize`, schema changes или provider calls. Для PostgreSQL настроить `YTV_DATABASE_URL`: binding сохраняет только имя переменной и digest, не DSN/credentials. Отсутствие или изменение reference, недоступная БД/workspace и несовпадающие pins дают явное `inspection unavailable`, без подмены состояния. Команда hook использует Git root и `uv --offline --no-sync`, в том числе из подкаталога; зависимости должны быть уже установлены. Истечение host timeout также не доказывает готовность работы.

Hook сохраняет ownership фактически выданных CLI claims уже привязанной сессии. Активный свой lease следует завершить или проверить по существующему provider handle; просроченный — восстановить штатно, сохраняя UNKNOWN. Hook сам не вызывает `claim`, `resume`, providers или approvals. Environment IDs служат correlation, не authentication: это прямо оговорено в [exec-server metadata contract](https://github.com/openai/codex/blob/main/codex-rs/exec-server/README.md#command-metadata). Guard не удостоверяет качество результата и не защищает от намеренного изменения локальных файлов. Его проверки и receipt gates дополняют фактического независимого reviewer.

Проверка через вызов `session_guard.decide` с записанными host events является **симуляцией host integration**. Live-проверкой считается наблюдённый запуск доверенных hooks в целевом Codex с сохранённым trace; unit tests и вручную переданный continuation этого не подтверждают.

## Параллельные изображения

Использовать отдельные короткие задачи без полного контекста родителя. Пул начинает с одного worker и добавляет capacity по измеренной генерации и времени приёмки координатором. Если очередь результатов растёт, новые slots не открываются; при насыщении/429 cap уменьшается. Верхнюю границу брать из фактического runtime/provider и бюджета, не из числа «10 каналов».

Освободившийся slot сразу получает следующую готовую сцену без барьера всей партии. Независимые каналы обслуживаются справедливо. Координатор хранит общий storyboard/visual bible и actual review; worker получает exact scene packet. Повторное использование slot допустимо только при подтверждённом reset; иначе новая сессия. Смешивать контекст сцен нельзя.

Обложки используют тот же image pool: `add-thumbnail-task` создаёт `thumbnail:<id>` после готового packaging. Задача зависит от packaging/script approval и не входит в зависимости render; MP4 можно закончить раньше обложки. Готовность созданных thumbnail tasks требуется до upload. Source extracts для `licensed_clips` подготавливать реально доступным host tool с capability `media.licensed_clip`; текущий `execute-media` не содержит clip extraction. Core принимает и проверяет подготовленный extract; image pool обслуживает изображения и обложки.

Наличие collaboration tools и возможность создавать свежие независимые сессии проверять на целевом host по фактически доступной схеме инструмента и наблюдённому результату. Не подставлять имя инструмента, параметры очистки контекста или лимит из документации другой среды. ChatGPT UI, API sessions и обычный image tool — разные механизмы; adapter проверяет именно используемый механизм. При отсутствии подтверждённого session backend сохранить blocker, а не выдумывать session IDs.

Долгая tool promise без provider job ID не даёт durable poll/recovery автоматически. При потере ответа исход становится UNKNOWN. Сохранённый контекст позволяет продолжить очередь, но не гарантирует восстановление потерянной provider генерации. Не повторять платную попытку, пока исход не установлен либо отдельно не разрешена новая.

## UI и безопасность контекста

Если backend использует браузер, работать только в опознанных принадлежащих заданию tabs/chats. Не менять общий clipboard, чужие drafts, личные окна или неизвестный composer. Capture/проверка фактического состояния требуются перед отправкой; блокировка composer предотвращает две одновременные записи. Исход отправки с потерянным ответом сверять в существующем chat, а не отправлять повторно в новом.

Если взаимодействию мешает окно расширения браузера, сначала самостоятельно попытаться закрыть это окно или, когда это безопасно, закрыть созданную текущим заданием вкладку и открыть её заново. Не закрывать чужие вкладки, страницы с несохранённым вводом или незавершёнными действиями; это не способ обойти запрет инструмента или повторить операцию с неизвестным исходом. Обращаться к пользователю, если восстановление требует его действий или безопасно продолжить не удалось.

Иные модели/режимы консультации использовать по конкретной задаче и доступности; основной production author остаётся Luna. Недоступность консультанта не запрещает независимую работу и не разрешает выдумать independent review.

## Развёртывание

Для работы без открытой основной сессии нужен реально запущенный executor и наблюдение за ним. Для нескольких хостов — PostgreSQL, общий artifact storage и проверенный backup/restore. Выбор Temporal, Agents API или другого executor требует capability prototype и отдельного решения; поддержка sessions не гарантирует сохранность killed commands/files.

Пока worker/bridge не настроен, приложение может хранить готовые задачи и показывать blocker. Сообщать пользователю сохранённое ожидание честно; не обещать, что задача сама выполнится ночью.

После подтверждённого schedule приложение сохраняет `verify_public` и применимый `ab_test` как pending deferred actions. `deferred-actions --run RUN_ID` возвращает эти записи; команда не запускает scheduler. `verify_public` имеет `not_before=publish_at`, A/B зависит от фактической Public-проверки. Их выполнение и read-back требуют подключённого durable host dispatcher и поддерживаемых adapters.

После отмены сначала записать фактические provider outcomes через `observe-operation`, затем закрыть оставшийся claim командой `settle-cancelled`. Это settlement бюджета и состояния без requeue; UNKNOWN остаётся зарезервированным. Полные параметры — [task contract](task-contract.md).


## Готовность фермы и общий бюджет

[Матрица готовности](readiness.md) отделяет проверенные software contracts от live-подключений. Общий `runtime_key` ограничивает активные/UNKNOWN native slots между runs; денежные резервы сейчас принадлежат отдельному run. Адаптивные service-time оценки остаются per-run. Для суммарного review backlog существует отдельный `shared_review_capacity`, настраиваемый через PoolService; native image host требует его до dispatch. Это **не** общий денежный бюджет или API quota, и старые executors без этого guard его не соблюдают.

До совместного production запуска host должен обеспечить проверенный общий лимит расходов/квот и backpressure координатора либо явно сериализовать admission выпусков. Нельзя выдавать десять отдельных лимитов за один общий бюджет. Следующий интеграционный этап проверяет именно multi-run нагрузку, а не только десять синтетических профилей.

## Исполняемый native image host

Для локального Codex App Server добавлен [native-image-host](native-image-host.md): JSON-lines transport, явный выбор модели, новые независимые threads, durable dispatch journal и readback native image items. Он использует существующий общий session/review limit и требует его настройки. Это конкретный image executor, не новый полный production orchestrator: он не подписывает approvals, не принимает собственный artwork, не выполняет TTS/YouTube и не подменяет QA.

Наличие adapter не является live capability observation. На целевом host отдельно проверяются установленный protocol/model, ChatGPT authentication, native image tool, доступные limits и получение реальных bytes. Не считать App Server и произвольный ChatGPT UI взаимозаменяемыми.
