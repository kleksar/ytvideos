# Вход в проект

Для новой задачи начать с [AGENTS](AGENTS.md) и [ytv-start](.agents/skills/ytv-start/SKILL.md). Запрос «мне нужен сюжет» идёт до полного текста без промежуточного выбора темы; затем два обычных пользовательских gates ведут к MP4 и расписанию.

## Разработчик

1. Получить исходники и выполнить setup из [development](docs/development.md).
2. Проверить CLI `--help`, локальное состояние и `doctor` реального окружения.
3. Прочитать [architecture](docs/architecture.md), затем только owner изменяемой области.
4. Проверить конкретный contract/failure case и приложить evidence к MR.

## Production worker

1. Использовать разрешённый workspace/store и runtime bridge, не личный draft или память другого чата.
2. Claim готовый task, получить `context`, открыть exact skill/references.
3. Сохранить actual outputs/checks/provider handles; complete только по проверенному контракту.
4. При restart продолжить сохранённый run; UNKNOWN сначала reconcile.

## Новый канал

Добавить проверенный ChannelSpec/PROFILE, выбрать поддерживаемый recipe и протестировать общий lifecycle без новой ветки workflow на имя канала. Проверить identity, voice/font/brand references, права, storage, provider capabilities, календарь/timezone и trusted approval bridge. Не создавать placeholders как работающие production каналы.

## Старый выпуск

Источник фактов — переданный bundle/receipts, а не новый README. До переключения закрепить прежний checkout и пройти [migration](docs/migration.md). Готовые media и реальные user decisions не восстанавливать из предположений.
