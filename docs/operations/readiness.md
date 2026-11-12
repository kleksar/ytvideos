# Готовность к запуску: контракт не равен живой ферме

Эта матрица связывает исходный запрос с реализацией, проверками и оставшимися границами. Зелёный CI подтверждает software contracts на проверенном commit; он не подтверждает доступ к аккаунтам, качество генерации, постоянную работу host или выпуск десяти каналов.

## Исходные требования

| Требование | Реализация / свидетельство | Граница приёмки |
|---|---|---|
| Новый запрос → самостоятельный полный сценарий | `Production.create/next/context`, `test_workflow.py`; сохранённая одна Luna-проба в `evals/results/2026-11-10-luna-story/` | Требуются live model/web tools. Одна проба не измеряет надёжность всех каналов. |
| Только согласования текста и точного MP4 | Workflow gates, Ed25519 verifier; `test_lifecycle.py`, `test_control_plane_edges.py` | Trusted user-event ingress ещё нужно подключить. Ключ verifier сам по себе не является bridge. |
| Автономное производство и параллельная упаковка | Task graph, media executor, image pool; workflow/media/lifecycle tests | Нужны actual providers, файлы стиля/шрифтов/музыки и подтверждённые права. |
| Независимые image sessions и непрерывное пополнение | `workers/pool.py`, `workers/bridge.py`, `pool_service.py`; `test_workers.py`, `test_pool_service.py` на SQLite/PostgreSQL | Для Codex App Server есть исполняемый native image host и contract tests. Доступность native image tool, получение bytes и восстановление на целевом Mac ещё требуют live-проверки; произвольный ChatGPT UI этим не подключается. |
| Нельзя забыть необходимый skill | Pinned catalog/skills в task context, `scripts/check_repository.py` | Наличие skill в packet не доказывает его качественное применение; нужны свежие поведенческие evals. |
| Общая логика для десяти каналов | Channel profiles, generic workflow, synthetic ten-channel fairness test | В Git активны Paper Detour и Scenes on Repeat; Nuviko History заморожен до прямого указания пользователя. Stories остаётся ручным архивом; новые каналы сейчас не подключаются. |
| Ранние блокеры без остановки независимой работы | `doctor` учитывает будущую image/clip capability до storyboard; `test_requirements_recheck.py` | Неизвестная capability не считается доступной. Runtime preflight голоса/fonts/quota/storage/Studio остаётся обязательным. |
| Повторы и рестарты не создают новые расходы | Durable operations, leases, exact hashes, event/request dedup; PostgreSQL regressions | UNKNOWN нельзя безопасно разрешить без реального provider evidence. Exactly-once внешнего API не заявляется. |
| Изменение одной сцены/обложки не уничтожает всё | Dependency invalidation, scene cache; workflow/cache/thumbnail tests | Изменённая обложка снимает release binding, но сохраняет принятый MP4 и approvals. |
| Полное оформление и schedule после MP4 approval | ReleaseSpec, requirement matrix, remote evidence, synthetic lifecycle | Поддерживаемые OAuth/Studio adapters, настоящий календарь, assets и readbacks должны быть подключены на host. |
| Задержка upload не требует третьего согласования | `prepare_release` допускает только новый слот после подтверждённого upload и до dispatch schedule; `test_release_replanning.py` | Слот выбирает проверенный host по политике канала. Уже отправленное/UNKNOWN расписание сначала reconcile. |
| Не потерять действующие выпуски | Code/profile/skills pins и [migration](../migration.md) | Старые runs не мигрируют автоматически; inventory/backup/restore проверяются на целевой машине. |
| Скорость и эффективность | Независимые задачи, bounded attempts/cache, adaptive pool | Проценты ускорения не измерены. Нужен baseline active time/tokens/cost/rework на реальных выпусках. |

## Что ещё нужно до production-фермы

**Обязательный интеграционный этап, не выполненные в этом MR подключения:** trusted user-event bridge; actual native-session/image dispatcher; live media/release adapters и capability observations; общий storage с backup/restore; работоспособный постоянный host executor; привязка к календарю с безопасным резервированием слотов; выполнение deferred Public/A/B actions.

Отдельно проверить общий ресурсный контур. Runtime session cap и round-robin turn разделяются между runs. Явно настроенный `shared_review_capacity` добавляет общий admission/backlog limit (см. [контракт](../architecture/adaptive-workers.md#общий-review-backpressure)); по умолчанию он не включён. Бюджет и adaptive service-time состояние остаются per-run. Не считать review limit глобальным денежным бюджетом/API quota. До такой интеграции host обязан ограничивать admission и суммарные затраты самостоятельно; нельзя просто открыть десять координаторов с независимыми лимитами.

Внедрение должно доказать два разных свойства: проверяемые технические артефакты и редакционное качество реального выпуска. Fake provider receipts и декодируемая тестовая аудиодорожка не доказывают прослушивание, качество narration, визуальную последовательность или оригинальность материала.

## Последовательность фактической приёмки

1. Подключить один проверенный канал в изолированном workspace без изменения действующих выпусков. `doctor` показывает реальные наблюдения и отсутствующие capabilities; никакого автоматического переключения production.
2. Проверить малый набор независимых native generations: exact task packet, сохранённые файлы/handles, доставка результата, refill, потерянный ответ и restart без повторной отправки. Платный эксперимент требует явного разрешённого бюджета.
3. Пройти один реальный выпуск через script approval → MP4 approval → complete scheduled release. Не подменять пользовательское решение test signer; не публиковать автоматически в рамках аудита кода.
4. Повторить на другом production recipe, затем проверить одновременные runs: общий расход/квоты, суммарный backlog, fairness, неопределённые операции и конфликт слота календаря.
5. Проверить восстановление store+artifact backup и работу после закрытия/рестарта основной сессии. Подтвердить pending → executed/read-back для Public/A/B, а не только наличие записей.

## Воспроизводимость software-проверок

CI выполняет suite `tests/` с реальным PostgreSQL и существующие automation suites. Артефакт `contracts-<run_id>-<attempt>` содержит оба лога, `reviewed-commit.txt` и `reviewed-source.tar.gz`: отфильтрованный снимок **tracked** кода/текстовых конфигураций, без runtime media и credentials. Это не полный архив брендов или backup производства.

Test-first checkpoint `f25c8143e61d6db56abe5b86dd904dcb0bf22d03` воспроизвёл race request/event deduplication на PostgreSQL, устаревшую release binding после правки обложки, неполный/недостоверный preflight и разделяемые mutable списки графа. Фикс должен пройти те же регрессии и полный CI на новом HEAD. Итоговые результаты привязывать к commit/run в MR; не переносить старый PASS на новую версию.

## Native image executor: добавленный software-этап

[Image host](native-image-host.md) реализует реальные protocol requests и соединяет их с PoolService; tests используют отдельный fixture subprocess для wire protocol и синтетические native observations для DB integration. Они не выполняют запросы к модели. Paper и Scenes on Repeat активны; Nuviko History заморожен, Stories остаётся ручным архивом. Известные оставшиеся этапы: live-приёмка host, trusted approval ingress, остальные stage adapters/координатор, календарь, общие денежные/API-лимиты, backup/restore и Public/A/B follow-ups. Только наличие image host не закрывает эти пункты.
