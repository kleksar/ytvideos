# Точка входа ytvideos

<!-- ytvideos-entrypoint-router:v1 -->

Сначала прочитать [корневой AGENTS.md](/Users/diplomat/ytvideos/AGENTS.md), затем [обязательный bootstrap](/Users/diplomat/ytvideos/.agent/CHANNEL_BOOTSTRAP.md).

Рабочий путь: `channels/scenes_on_repeat/videos/home-alone-1990`. Найти его в [реестре](/Users/diplomat/ytvideos/.agent/episode-registry.md), перейти к canonical-каталогу. Читать current_context и только нужные действию сведения из state_sources по bootstrap.

Канал: Scenes on Repeat. Обязательно прочитать [правила канала](/Users/diplomat/ytvideos/channels/scenes_on_repeat/AGENTS.md).

Процедуру выбрать в [каталоге skills](/Users/diplomat/ytvideos/.agent/skill-catalog.md). `.agents/skills` здесь — ссылка на единственный канонический набор, а не отдельная версия. Этот файл не даёт новых разрешений и не меняет состояние выпуска.
