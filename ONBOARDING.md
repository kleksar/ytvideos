# Вход в проект

Выбрать вход по [AGENTS](AGENTS.md). Запрос «мне нужен сюжет» идёт до полного текста без промежуточного выбора темы; согласования текста и точного MP4 ведут к принятому видео. Загрузка и расписание выполняются по прямому поручению на выпуск.

## Разработчик

1. Получить исходники и выполнить setup из [development](docs/development.md).
2. Выполнить `python scripts/check_repository.py` и адресную проверку из [development](docs/development.md#что-проверять). Проверка исходников не требует production store, OAuth или запуска video run.
3. Прочитать [architecture](docs/architecture.md), затем только owner изменяемой области.
4. Проверить конкретный contract/failure case и приложить evidence к MR.

## Production worker

1. Использовать разрешённый workspace/store и runtime bridge, не личный draft или память другого чата.
2. Claim готовый task, получить `context`, прочитать exact skill и выбранные `reference_documents`. Проверить профиль, формат и рецепт; список названий файлов не заменяет их содержимое.
3. Сохранить actual outputs/checks/provider handles; complete только по проверенному контракту.
4. При restart продолжить сохранённый run; UNKNOWN сначала reconcile.

## Новый канал

Добавить проверенный ChannelSpec/PROFILE и необходимые `context_references` по [контракту контекста](docs/operations/task-contract.md#требования-в-контексте). Выбрать поддерживаемый recipe и проверить общий lifecycle без ветвления по имени канала. Проверить identity, voice/font/brand references, права, storage, providers, календарь и trusted approval bridge. Не создавать placeholders как работающие production каналы.

## Старый выпуск

Источник фактов — переданный bundle/receipts, а не новый README. До переключения закрепить прежний checkout и пройти [migration](docs/migration.md). Готовые media и реальные user decisions не восстанавливать из предположений.
