# Готовность производства

Машинный профиль определяет допустимый продукт и проверки. Статус `active` разрешает создание run; он не подтверждает доступность providers, аккаунтов, шрифтов, музыки или принятых изображений. Зелёный CI проверяет программный контракт на точном commit, а готовность выпустить настоящий ролик подтверждается выполнением в целевом окружении.

## Пять каналов

```bash
uv run ytv profiles
uv run ytv profiles --channel paper_detour --format short
```

Это read-only проверка конфигурации без run, DB или workspace. Ответ показывает status, требования/варианты формата и конкретные blockers; `live_readiness=unverified` не означает проверенное подключение tools. Для сохранённого выпуска использовать его `plan`, затем `doctor` фактического окружения по [task contract](task-contract.md).

| Канал | Поддерживаемый путь | Что проверить или определить до исполнения |
|---|---|---|
| [Paper Detour](../../channels/paper_detour/AGENTS.md) | Активный `illustrated`: Short и long | Точные style refs, Chalkboard SE Bold, голос, права/музыку и providers. Full-bleed оформление без внешней Paper Frame принадлежит профилю. |
| [Nuviko History](../../channels/nuviko_history/AGENTS.md) | Активный `illustrated`: Short и long | Точные эталоны ведущего/мира, Georgia Bold, голос, музыку и фактические источники истории. Параметры существующего run сохраняются по его pins. |
| [Scenes on Repeat](../../channels/scenes_on_repeat/AGENTS.md) | Активный `licensed_clips`: Short; `scene`, `character_edit`, `meme_time_machine` | Выбрать подходящий вариант 24/48 fps, проверить реальные source clips/права и средства монтажа. Long не имеет определённого delivery recipe. |
| [Two Ways Lab](../../channels/two_ways_lab/AGENTS.md) | Активный `illustrated`: Short 1080×1920/30 fps | Проверить Trebuchet MS Bold, голос и точные character reference PNG из brand storage по hashes реестра. Long не определён. Статические планы допустимы; music/zoom не превращать в обязательную политику Paper. |
| [Nuviko Videos](../../channels/nuviko_videos/AGENTS.md) | Активный `music_first`: Short 1080×1920/30 fps; `vocal`, `instrumental`; typed edit plan → `mix` → `music_render` | Проверить точную запись/отрывок, source clips и права, карту музыкальных акцентов; для вокала — Bradley Hand Bold, все слова и их тайминги. Инструментальный вариант использует проверенный `no_speech` без SRT. Нужен полный просмотр/прослушивание точного MP4; long не определён. |

Музыкальный compositor проверяет закреплённые параметры, происхождение звука/футажей и применимые титры; доступ к реальным исходникам, лицензиям и нужному шрифту подтверждается отдельно. Stories RU/EN и Главред Борисенко ведутся вручную вне этой пятёрки. Identity канала и сохранённое наблюдение Studio не заменяют проверку текущего доступа или статуса ролика.

## Что обеспечивает runtime

| Возможность | Программный контракт | Практическая граница |
|---|---|---|
| Вход и план до генерации | `start` сохраняет run, выдаёт plan summary, диагностику и reading packet; read-only `plan` показывает закреплённые требования, stages/checks/skills и blockers | Применяется также к новому запросу только на сценарий. Агент читает пакет и сообщает план; команда не является approval и не запускает providers. |
| Присланный полный сценарий | `start --source-script` сохраняет точные bytes/hash narration или поддержанного typed edit plan; research проверяет данный замысел, script получает исходник | Source не равен проверенному script или approval. Trusted host связывает подлинное исходное поручение с exact script/hash. |
| Требования каждого этапа | `claim.context`, `task_guide`, выбранные `reference_documents`, direct/supporting inputs | Доставка skill в packet не доказывает его качественное применение. Нужны проверка конкретного результата и поведенческие evals. |
| Приёмка точного результата | Обязательные checks, leases, artifact hashes, probe/decode и production contract | Технические измерения не подтверждают факты, смысл картинки, произношение или реальное прослушивание. |
| Две контрольные точки | Локальный `approve` связывает явное решение владельца с exact script/MP4, revision/hash; проверяет готовность и replay | Ключ/hooks/bridge не нужны для локальной сессии. Подлинность ответа доверена координатору. Signed-only ingress необязателен. Upload/публикация требуют прямого поручения. |
| Независимые задачи | Task graph, image pool, native image host и параллельная упаковка | Нужны actual provider sessions, доставка bytes и работающий host. Протокол App Server не подключает произвольный ChatGPT UI. |
| Повторы и восстановление | Durable operations, request/event dedup, code/profile/skills pins, dependency invalidation | `UNKNOWN` сверяется с provider evidence; exactly-once внешнего API не заявляется. Старые runs не мигрируют автоматически. |
| Выпуск после поручения | ReleaseSpec, remote evidence, календарные ограничения и deferred actions | Нужны actual OAuth/Studio adapters, проверенный календарь и исполнитель pending Public/A/B tasks. Запись задачи не означает фоновое наблюдение. |

`audio.listen` означает доступный способ реально прослушать звук с evidence. FFmpeg, decode и график сигнала не предоставляют этот способ. Незарегистрированную capability сначала проверить и записать; фактически отсутствующая capability блокирует зависимые этапы, кроме явно разрешённой [производственной отсрочки прослушивания](task-contract.md#audio-production-before-listening). Финальная проверка сохраняет реальные требования.

## Зависимости автономного host

Host должен обеспечить запись реальных пользовательских решений (локальный `approve` либо явно выбранный signed-only ingress), providers и [native image executor](native-image-host.md), остальные stage adapters/координатор, общее хранилище с backup/restore, календарь и выполнение deferred Public/A/B actions. Для production нужна проверка восстановления после закрытия основной сессии; foreground tool loop сам по себе не доказывает постоянную работу.

Runtime session cap и round-robin turn разделяются между runs. Явно настроенный `shared_review_capacity` добавляет общий admission/backlog limit по [контракту очереди](../architecture/adaptive-workers.md#общий-review-backpressure); по умолчанию он не включён. Бюджет и adaptive service-time состояние остаются per-run. Review limit не является общим денежным бюджетом или API quota: host ограничивает общий admission и суммарные расходы отдельно.

## Фактическая проверка готовности

1. Проверить один разрешённый канал и формат в изолированном workspace. `profiles`, `plan` и `doctor` должны различать конфигурацию, сохранённые наблюдения и реальные capabilities.
2. Проверить точный task packet, выбранные документы, actual files и приёмку результата на реальных tools. Платные генерации выполнять только в разрешённом бюджете; качество оценивать по результату, а не по receipt провайдера.
3. Пройти реальный путь от темы или присланного текста до MP4 с просмотром/прослушиванием. Подлинное решение пользователя не заменять test signer. Внешний выпуск проверять только при прямом поручении пользователя.
4. Проверить потерянный ответ, restart и сохранённый результат без повторной платной отправки. При нескольких runs проверить общий расход/квоты, backlog, fairness и конфликты календаря.
5. Проверить восстановление store+artifacts из backup. Для порученных последующих действий подтвердить переход pending → исполнено и read-back, а не только наличие записей.

Структурные проверки, свежий поведенческий прогон целевой модели и реальный выпуск отвечают на разные вопросы. Mock providers и fixture subprocess проверяют протокол; они не доказывают редакционное качество или доступность live tools. Скорость, затраты и долю переделок измерять на сопоставимых реальных задачах, без переноса результата одной пробы на все каналы.

## Воспроизводимость проверок

CI выполняет `tests/` с PostgreSQL и существующие automation suites. Артефакт `contracts-<run_id>-<attempt>` содержит test logs, `reviewed-commit.txt`, `reviewed-paths.json` и `reviewed-source.tar.gz`: отфильтрованный снимок tracked кода и текстовых конфигураций, без runtime media и credentials. Current entrypoints и объявленные `context_references` входят в snapshot; исторические журналы не являются обязательным контекстом production.

Для неполного source snapshot использовать `python scripts/check_repository.py --known-paths /path/to/reviewed-paths.json`. Inventory должен происходить из проверенного Git tree; в него нельзя дописывать отсутствующие PNG ради прохождения проверки. Ссылки на artwork восстанавливаются по реальным файлам и hashes. Source snapshot не является полным brand archive или backup производства. Результат проверки всегда привязывать к commit/run, не переносить прежний PASS на изменённую версию.
