# Аудит документации и передачи задач — 13 ноября 2026

Исследование и проверка изменений [MR #10](https://github.com/kleksar/ytvideos/pull/10). Это evidence аудита, не дополнительный обязательный регламент для каждого выпуска.

## Вывод и область изменения

Главная подтверждённая проблема — существующие требования не доходили до конкретного исполнителя. Добавление ещё одного общего checklist не устраняло этот разрыв. MR передаёт выбранные стандарты и канальные рецепты с содержимым и hashes, сохраняет их на run, проверяет доставку в native worker и сокращает повторяющиеся инструкции. Production statuses, голоса, скорости, права и два бизнес-gates не переопределены.

Изменения относятся к software/workflow и документации. Новые видео, публикации, production migration и подключение живых провайдеров в этом аудите не выполнялись.

## Источники и пределы выводов

- База ytvideos: [`4423ca68184f8c41c5fca5b51d88d51711adf38d`](https://github.com/kleksar/ytvideos/commit/4423ca68184f8c41c5fca5b51d88d51711adf38d).
- Witok изучен read-only на `develop`, commit [`910f7a22ccee7fae1ffce3bb95e4e78b7f5b6201`](https://github.com/kleksar/witok/commit/910f7a22ccee7fae1ffce3bb95e4e78b7f5b6201). Изменений в нём нет.
- Приложенный архив последних сессий: SHA-256 `6148b62feaa5eaa4d28729d8cd331ea4be071ecc94ee4c442e4eea0c64ced9f7`; manifest SHA-256 `56495b1d96a9ec76a6317a84daf81f660aaac0ac0bc57453922912fa0f2a4483`. Все 42 перечисленных файла совпали с manifest. Raw chats, аккаунты и персональные пути в Git не перенесены.

Индекс содержит 20 сессий, но сообщения доступны только в 11; у остальных девяти `not_started`. Четыре сохранены как `blocked_oversized_turn`, четыре — `partial_interrupted`, три — `complete_available_history`. Последний статус означает конец доступной пагинации, а не полноту исходного разговора. В 105 turn-записях есть пять общих turns форка 02/03: после дедупликации остаются 100 уникальных turns, 2 292 items и 111 userMessage items. В исходной выборке 639 items имеют маркер усечения.

Это позволяет установить повторяющиеся механизмы ошибок. Выборка не позволяет надёжно оценить частоты для всего проекта, потраченное время, экономию токенов или причину каждого UI-блокера. Повтор одного turn в двух форках не считается двумя независимыми сбоями.

## Проблема → исправление → проверка

| Наблюдение | Изменение | Основание проверки |
|---|---|---|
| В сессиях 02/03 агент признал, что не открыл release standard; в 07 не применил уже записанный монтажный рецепт | Один selector стандартов и `ChannelSpec.context_references`; выбранные тексты входят в task context | [Context tests](../../tests/test_context.py): stage/format/purpose, содержание, missing path, сохранность после изменения/удаления recipe |
| В 09 правило путешественника Paper Detour применялось к кадрам, но терялось в сценарии | PAPER_PLANE явно включён для script и связанных этапов; сценовые и thumbnail references разделены | Проверка ChannelSpec и purpose filtering; отсутствие thumbnail-only playbook в обычной сцене |
| Native image worker ранее получал ограниченный набор файлов из checkout, а не все требования своей задачи | Проверка pinned manifest и запись `requirements/<repo path>` в sandbox | [Image host tests](../../tests/test_image_host.py): доступный thumbnail standard, полнота, SHA-256, пути, parent symlink, неизменный исходный packet |
| Текстовые инструкции расходились: Nuviko назывался активным; MP4 approval местами подразумевал последующий выпуск | Статус берётся из ChannelSpec; выпуск требует соответствующего прямого поручения | Сверка действующих entrypoints/skills/profile; бизнес-gates сохранены |
| В 08 смешивались лимит private uploads и публикационный календарь; наличие schedule не доказывало полный выпуск | Release standard явно разделяет эти сущности; подтверждение остаётся в существующих receipts/read-back | Сверка release/task contract; существующие release/approval/provider tests сохранены |
| В 06 два masters одинаковой длительности имели разные hashes и не были однозначно связаны с uploaded video; встречались недоступные worktree paths | Сохранены существующие artifact/approval/operation guards; packaging раньше проверяет полный `(run_id, channel_id, revision, format)` | [Workflow tests](../../tests/test_workflow.py); legacy assets не переименованы и не объявлены автоматически мигрированными |
| Документ существовал, но checker пропускал uppercase PROFILE, ONBOARDING, неверные anchors и drift каталога | Расширен существующий offline checker; отдельная детерминированная генерация каталога | 18 отрицательных/положительных fixtures в [checker tests](../../tests/test_repository_check.py), проверка не меняет файлы |
| Независимое review нашло новые gaps: повтор create после удаления recipe; отсутствующие long captions и Meme recipe | Ранний idempotency lookup; pinned LONG_CAPTIONS/MEME_SHORTS и общие cuts/music; явная применимость вариантов | Воспроизведения до исправления и три адресных regression tests после него |

## Контракт передачи требований

`run.reference_snapshot` хранит документы и маршруты один раз; digest входит в `pins.references`. Задача получает только выбранные пути и `{path, sha256, text}`. Для существующего run изменение отдельного recipe-файла не подменяет его сохранённый текст. Новый run получает новую версию. Повтор `create` с уже существующим `request_id` возвращает сохранённый run до чтения изменяемых source files; другой channel/intent/format под тем же ID отклоняется.

Native host сверяет packet с сохранённым job и pinned run, затем материализует тексты. В локальном `TASK.json` остаются `requirements` и компактный `reference_manifest`; полные тексты не дублируются внутри JSON. Файлы и TASK входят в проверяемый `job.inputs`. Изменённый outbox нельзя легализовать простым пересчётом собственного checksum.

Для старых runs без snapshot используется `reference_source: legacy_checkout` с проверкой исходного code pin. Исторические requirements не выдумываются. Смена кода/общих стандартов не разрешает переписать pins действующего выпуска: сохраняется [migration contract](../migration.md). Независимый reviewer проверил реальный baseline legacy fixture с новым host и исходным checkout: один dispatch, без blockers, без переписывания run.

Варианты Scenes on Repeat выбираются по принятому плану: сценовый Short, полноэкранный персонажный эдит, Meme Time Machine и long. `short/long` недостаточно для детерминированного выбора всех разновидностей. Поэтому Short получает оба применимых рецепта с явными границами: Meme использует 48 FPS и rating layout; 24 FPS и композиция сценового Short на него не переносятся. Keyword matching по свободному intent и новый variant API в MR не добавлены.

Точный контракт и фильтры находятся в [task contract](../operations/task-contract.md#требования-в-контексте), native представление — в [native image host](../operations/native-image-host.md).

## Документация и практики Witok

Перенесены подходы из [Witok docs skill](https://github.com/kleksar/witok/blob/910f7a22ccee7fae1ffce3bb95e4e78b7f5b6201/.agents/skills/witok-docs/SKILL.md), [docs checker](https://github.com/kleksar/witok/blob/910f7a22ccee7fae1ffce3bb95e4e78b7f5b6201/tools/docs.py) и его отрицательных fixtures: один владелец правила, короткий маршрут по задаче, read-only gate, ссылки/anchors, проверка generated drift, адресные проверки отказов. Большой ownership graph, полный registry документов и независимые механизмы архивирования Witok не перенесены.

В ytvideos теперь яснее разделены владельцы:

- Entry skill выбирает следующий шаг и owner; не повторяет весь стандарт.
- [Thumbnails](../standards/thumbnails.md) хранит творческие требования и QA карточки.
- [Thumbnail experiments](../operations/thumbnail-experiments.md) хранит план/observations/интерпретацию A/B; JSON вынесен в [пример](../examples/thumbnail-experiment.json).
- [Release](../standards/release.md) хранит применимость, готовность и подтверждение выпуска; точные schemas/CLI принадлежат task contract.
- ChannelSpec выбирает канальные документы; PROFILE/recipe владеют художественными различиями.
- JSON-каталог и frontmatter сверяются, Markdown-каталог генерируется командой checker. Исторические journals не включаются в обязательное чтение.

Сравнение UTF-8 bytes с базой аудита:

| Текст | До | После | Сокращение |
|---|---:|---:|---:|
| Корневой AGENTS | 7 041 | 5 608 | 20,4% |
| COLLABORATION | 3 938 | 3 127 | 20,6% |
| Start skill | 4 405 | 3 824 | 13,2% |
| Release skill | 8 402 | 5 664 | 32,6% |
| Творческий thumbnail standard | 40 203 | 27 273 | 32,2% |
| Все семь skills вместе | 35 764 | 32 017 | 10,5% |

Часть thumbnail текста перенесена в операционный документ, а не удалена. Это измерение объёма выбранных текстов, не token benchmark. Общий diff растёт из-за runtime-контракта, отказных tests и evidence; уменьшение числа строк всего репозитория не было самостоятельной целью.

## Проверки и evidence

- Итоговый локальный core suite: 380 discovered, 254 passed, 126 явных PostgreSQL skips; 13,450 s. Отсутствие локального PostgreSQL не названо проверкой его поведения.
- Все 15 существующих automation suites завершились успешно: 321 discovered, 320 passed, один skip proprietary caption font fixture. Их production code не менялся. FFmpeg/media tests выполнялись.
- Ruff (`src/ytvideos tests scripts`), `git diff --check`, offline docs/catalog gate — без ошибок.
- На опубликованном checkpoint `87193168` [CI](https://github.com/kleksar/ytvideos/actions/runs/43330829389) прошёл с реальным PostgreSQL: core 377 discovered / 376 passed / один SQLite-only skip PostgreSQL race case; automation 321 / 320 / один font skip. Последующие исправления трёх review findings проверены локально; состояние CI окончательной ревизии следует смотреть в MR, а не выводить из этого раннего запуска.
- Скачанный CI artifact проверен по SHA-256. Его source archive (GitHub test merge `19c754810d09ee97b15f10802364b34309dedb29`) восстановлен в отдельный каталог: docs gate с `reviewed-paths.json` прошёл, создание Paper Detour и Scenes on Repeat runs и выдача pinned context прошли без исходного checkout.
- Независимое review проверило runtime/path/pinning/legacy boundary и действующие recipes. Найденные три P2 воспроизведены, исправлены и повторно проверены. Это code review, не приёмка готового видео.
- Две свежие GPT-6 Luna-сессии проверили применение character-edit и Meme recipes к плану монтажа; [результаты, source pins, outputs и краткие trace summaries](../../evals/results/2026-11-13-luna-task-context/result.json) сохранены отдельно. Они не генерировали media и не выполняли release.

Baseline CI на `4423ca68` завершился за 2 мин 46 с от создания до обновления run ([источник](https://github.com/kleksar/ytvideos/actions/runs/43327727703)). Оснований удалять полные regression suites ради заявленного ускорения нет. Новый offline docs gate выполняется перед dependency setup; адресные локальные команды описаны в [development](../development.md#что-проверять).

## Что остаётся отдельной работой

Этот MR не доказывает готовность живого account/host. [Readiness](../operations/readiness.md) остаётся владельцем production-приёмки: trusted approval ingress, реальные provider capabilities, качество видео/звука, общий бюджет/календарь и исполнение последующих наблюдений. Старые masters и source clips требуют проверенных durable locators и явного импорта; соответствие legacy upload конкретному hash нельзя восстановить по одному имени или длительности. Медиа-эталоны Paper Detour остаются отдельными assets с provenance и hashes, не фиктивными PNG-заглушками в Git.

Без этого evidence нельзя обещать полностью автономный выпуск, отсутствие всех будущих ошибок или измеренное сокращение сроков. Изменения MR закрывают воспроизведённые программные разрывы и оставляют проверяемый путь дальнейшей работы.
