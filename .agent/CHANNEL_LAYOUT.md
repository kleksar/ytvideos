# Расположение данных

Исходный код — `src/ytvideos/` и технические modules `automation/`. ChannelSpec и художественные profiles — `channels/<id>/`. Skills — `.agents/skills/`; повторяемые требования — `docs/standards/`.

Новые run IDs/состояния создаёт приложение в заданном workspace/store. Files/URI связываются с artifact IDs/hashes. Исторический media path не переносится автоматически в новый layout. Читаемые `EPISODE.md`/`CURRENT_CONTEXT.md` — exports, а не вручную синхронизируемая база.

[Архитектура](../docs/architecture.md) · [Миграция](../docs/migration.md) · [Хранение](../docs/standards/storage.md)
