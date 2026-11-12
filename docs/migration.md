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

Ручной архив Stories RU/EN, замороженный Nuviko History и новый русскоязычный канал коллеги остаются разными identities. Brand acceptance receipts, права и исторические публикационные данные сохраняются. Никаких live публикаций ради проверки MR.

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

Paper: полноценные paper/card диорамы, самостоятельные композиции без внешней декоративной рамки, typography, motion, 1.10× голос и музыкальное покрытие. Nuviko History: frozen до прямого поручения пользователя, точный 2D ведущий/фотореалистичный мир, 1.10×, собственные references. Scenes on Repeat: права, оригинальные английские реплики, 1.15× только диктор, канальные montage recipes. Общие: текст/MP4 approvals на точные artifacts, первый слушатель, viewer value, внутренние sources, manual SRT, нативные YouTube элементы, права и receipts.

Отменены как обычные gates: выбор темы после запроса полного сюжета; отдельное разрешение на каждое изображение/звук в принятом scope; обязательный выбор упаковки; Unlisted review; повторный вопрос о времени при действующей календарной политике. Исключения по изменённому scope, настоящему blocker или неопределённому approval target остаются предметными.

## Критерий активации

Контрактные tests и свежая Luna navigation/script проба проверяют новый route. Полный live production требует доступных tools, проверенных credentials/rights/fonts и control episode. Postgres/shared-storage/worker recovery проверяются отдельно. В MR явно перечислять проверенное и оставшееся; не подменять фактическую приёмку архитектурной схемой.
