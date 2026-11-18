# Переход на общий процесс

Новый вход сначала используется для новых runs. Изменение README или создание MR не мигрирует существующие local episodes и не доказывает, что активные сессии уже используют закреплённые правила.

## Порядок перехода

1. Инвентаризировать активные выпуски, владельцев, незакоммиченные изменения, текущие процессы/внешние операции и фактические media paths.
2. До переключения общих входов оставить каждому старому consumer предыдущий checkout либо проверенный snapshot code/rules. Не перемещать его зависимости ради новой структуры.
3. Для переносимого выпуска выбрать одного владельца и точный источник состояния. Сопоставить channel/episode IDs, текст, media hashes, QA, user events, video IDs/URLs, права и receipts.
4. `import-legacy` импортирует подтверждённое. Чужое свободное описание «принято» не становится trusted approval. Недостающие bytes/receipts/события сохранить UNKNOWN/UNVERIFIED с явной причиной.
5. Проверить `status`/`next` и состав готовых задач до возобновления. Незавершённый внешний вызов сначала reconcile, не запускать новый из-за отсутствия локального ответа.
6. Переключить только проверенный run. Сохранить исходный manifest, версию и migration receipt; не заявлять мигрированными остальные работы.
7. При rollback вернуть version/routing. Отдельно сверить уже выполненные внешние действия: откат кода не отменяет upload или schedule.

Ручной архив Stories RU/EN, активный Nuviko History и Nuviko Videos остаются разными identities; статус текущего профиля не меняет pins существующего run. Brand acceptance receipts, права и исторические публикационные данные сохраняются. Никаких live публикаций ради проверки MR.

## Миграция runtime сохранённого run

`migrate-runtime` переносит code/skills/reference pins существующего run без изменения его ID, revision, профиля, принятых artifacts, approvals, задач, операций и бюджетов. Маршрут предназначен для совместимых версий текущей workflow schema; он не преобразует художественный профиль или итоговые media contracts. Порядок исполнения принадлежит [ytv-operate](../.agents/skills/ytv-operate/references/runtime-migration.md).

```bash
uv run ytv --db STATE_DB --workspace WORKSPACE --project-root TARGET_ROOT migrate-runtime plan \
  --run RUN_ID --source-root SOURCE_ROOT --expected-version VERSION > migration-plan.json
uv run ytv --db STATE_DB --workspace WORKSPACE --project-root TARGET_ROOT migrate-runtime apply \
  --run RUN_ID --source-root SOURCE_ROOT --plan migration-plan.json \
  --source 'REAL_OWNER_MESSAGE_REFERENCE' --message 'Exact owner instruction'
```

Для выпуска до script approval допускается только `pending` script без outputs; существующие артефакты, включая кандидаты, сохраняются без принятия. При наличии approval он обязан соответствовать точному принятому сценарию. Plan связывает исходное состояние и operations, source/target code и тексты инструкций с hashes. Apply повторяет проверки под блокировкой run, отказывает при изменении входов или незавершённых внешних действиях и сохраняет исходный snapshot, receipt и событие. Артефакты добавляются в CAS; старые записи не переписываются. Повтор exact apply возвращает прежний результат без второй миграции. Этот локальный учёт решения доверяет координатору и не удостоверяет личность владельца криптографически.

Если то же поручение владельца включает дальнейший локальный ремонт, `apply --continue-receipt SHA256` явно связывает новый план с последним migration receipt. Проверяются точный исходный `source`/`message`, совпадение текущих и исходных pins с предыдущими target pins, неизменные revision, принятый сценарий и канал. Run может продвинуться после `to_version` предыдущего receipt: новый plan обязан фиксировать его актуальную версию, состояние и операции. Сохраняются channel/format/intent, точное script approval и лимиты бюджета; активные leases и неопределённые операции по-прежнему запрещены. Старый plan после production-перехода не применяется. Старый, неизвестный receipt или новое решение отклоняются. Без флага повтор источника решения для другого плана по-прежнему запрещён. Новый receipt и history entry сохраняют `continued_from_receipt_sha256`; повтор его apply требует того же значения. Цепочка не расширяет scope исходного поручения, не разрешает расходы и не заменяет план/проверки новой версии.

## Локальное согласие для уже сохранённого run

Новый `approve` использует прежние store/approvals/events, без смены схемы и без повторного создания выпуска. Согласие из исходной беседы можно зарегистрировать для того же показанного артефакта; не просить его заново. При этом code/profile/skills pins не переписываются автоматически.

Если run ещё привязан к прежнему checkout, запустить новый CLI с **этим закреплённым checkout** в `--project-root` и прежними `--db`/`--workspace`, затем продолжить сохранённый run на его закреплённой версии. Новый approval helper совместим с прежним форматом state; проверка code pin относится к переданному project root. Не заменять root случайным текущим деревом и не править pins напрямую. Если закреплённые исходники потеряны, сначала восстановить проверенный snapshot по порядку выше — это проблема версии, не отсутствие согласия или ключа.

## Карта переноса правил

| Прежний владелец | Текущий владелец | Решение |
|---|---|---|
| Root §§0–4, bootstrap, catalog | AGENTS + ytv-start + приложение | Короткий вход; create и resume различаются; ID создаёт код |
| topic-research + storycraft + history-verification | ytv-write-script + editorial | Research сразу продолжается полным текстом; факты и viewer value сохранены |
| shorts-story + shorts-loop | editorial + канальный recipe | Законченный первый просмотр; петля по смыслу |
| production + FLOW_STATE.md + EPISODE.md | workflow + store + generated views | Два gates; один source of truth; версии и evidence |
| visual-direction + scene-images + Paper aliases | visual + channel PROFILE | Постановка, фактические references и per-scene review сохранены |
| image-motion | visual + montage profiles | Цельный pan/zoom, отдельные ограничения соседних сцен |
| audio-delivery + srt + paper-subtitles | audio + channel/format profiles | Точная речь, единственная скорость, полный mix, alignment и отдельный SRT |
| video-export + video-qa | delivery + ytv-review-video | Один export contract; машинные и perceptual checks различаются |
| title/description/thumbnail/hashtags/tags/playlist/chapters | release + канальные профили | Полный пакет параллельно production, без отдельного согласования |
| youtube-release + A/B + dynamic scheduling | release + adapters | Explicit Private, полный read-back, schedule после MP4, A/B после Public |
| media-lifecycle + asset library | storage + helpers | Ownership, dependencies, cleanup receipt и честный TEXT_ONLY |
| RULES_SYNC + абсолютный Mac rules path | version pins + migration | Проверенный snapshot на run, без глобального stage-by-stage чтения чужого пути |
| chatgpt-session + extra-high | runtime + session backend | Capability-driven independent tasks; основной Luna; чужие чаты/черновики защищены |
| agents roles + длинные catalogs | 7 entry skills + manifest | Task context задаёт процедуру; роль не является доказательством review |
| Channel AGENTS с копией workflow | короткий AGENTS + PROFILE/recipe | Разные стили/права/календарь, общий lifecycle |

## Сохранённые обязательные требования

Paper: полноценные paper/card диорамы, самостоятельные композиции без внешней декоративной рамки, typography, motion, 1.10× голос и музыкальное покрытие. Nuviko History: активный illustrated рецепт, точный 2D ведущий/фотореалистичный мир, 1.10×, собственные references. Scenes on Repeat: права, оригинальные английские реплики, скорость только диктора по закреплённому профилю, канальные montage recipes. Общие: текст/MP4 approvals на точные artifacts, первый слушатель, viewer value, внутренние sources, manual SRT, нативные YouTube элементы, права и receipts.

Отменены как обычные gates: выбор темы после запроса полного сюжета; отдельное разрешение на каждое изображение/звук в принятом scope; обязательный выбор упаковки; Unlisted review; повторный вопрос о времени при действующей календарной политике. Исключения по изменённому scope, настоящему blocker или неопределённому approval target остаются предметными.

## Критерий активации

Копия runtime в output отдельного выпуска не становится общим production adapter. Прежде чем закреплять новую реализацию, её изменения должны быть сохранены как проверяемые source changes с контрактными тестами, документированными командами и маршрутом чтения правил. Нельзя сохранять новые команды только в эпизодическом fork и одновременно считать прежние skills полным описанием нового процесса. Исторический snapshot нужен для воспроизводимости; перенос его метода на другие каналы требует отдельной проверки. Новая миграция не разрешает задним числом дописать непроверенные approvals, costs или review receipts.

Для сохранённых внешних video batches `doctor` показывает read-only аудит объявленных связей: revision/script, показанная партия/настройки/лимит, provider operation/attempt, observation и фактическая стоимость. Отсутствующая связь в старой схеме означает `unverified`, а не несанкционированную реальную трату, брак изображения или разрешение повторить запрос. Диагностика не является dispatch permit и не меняет pins. Перед новым платным действием legacy-реализацию с непроверенными guards нельзя считать готовой только по успешной прошлой партии.

Контрактные tests и свежая Luna navigation/script проба проверяют новый route. Полный live production требует доступных tools, проверенных credentials/rights/fonts и control episode. Postgres/shared-storage/worker recovery проверяются отдельно. В MR явно перечислять проверенное и оставшееся; не подменять фактическую приёмку архитектурной схемой.

## Полнота инструкций и thumbnail evidence

Для новых/переработанных packaging применяется структурированный `thumbnail_plan`; generic PASS старого receipt не превращается в концепты автоматически. При переносе незавершённого выпуска подготовить недостающие концепты и reviewer JSON по текущему task contract, сохранив прежние source/approved media. Не переписывать старый pinned snapshot и не изобретать задним числом независимое review. Неизменённый run продолжает использовать исходный checkout по общему порядку выше. `instructions` предназначен для узкой работы без run и не является обходом migration.
