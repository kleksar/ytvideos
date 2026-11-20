# Каналы

Машинные параметры и статус задаются `channels/<id>/channel.json`, художественные правила — выбранными канальными документами. Поддержка формата и live-доступность проверяются отдельно: `uv run ytv profiles` показывает конфигурацию пяти каналов, `doctor` — наблюдения конкретного окружения.

| Канал | Назначение | Статус |
|---|---|---|
| [Paper Detour](paper_detour/AGENTS.md) | Английские истории в бумажном мире | По умолчанию для нового запроса без канала |
| [Scenes on Repeat](scenes_on_repeat/AGENTS.md) | Английские киноразборы/сценовые форматы | Отдельный verified channel и licensed-clips recipe |
| [Nuviko History](nuviko_history/AGENTS.md) | Английские исторические рассказы с рисованным ведущим | Активен; illustrated Short и long |
| [Nuviko Videos](nuviko_videos/AGENTS.md) | Музыкальные Shorts с реальными футажами | Активен; `music_first` Short: `vocal` и `instrumental`, long не определён |
| [Two Ways Lab](two_ways_lab/AGENTS.md) | Англоязычные иллюстрированные эксперименты | Активен; illustrated Short, long не определён |

[Главред Борисенко](glavred_borisenko/PROFILE.md) ведётся вручную вне автоматического workflow. [Stories RU/EN](nuviko_stories/AGENTS.md) — отдельный ручной архив. Эти identities не заменяют ни один из пяти профилей. Подключение другого канала требует подтверждённой identity, прав, применимого голоса, календаря и исполняемого recipe.

[Vice Wreckroom](vice_wreckroom/PROFILE.md) — проверенная YouTube identity для ручного GTA VI Shorts workflow; не шестой активированный ChannelSpec. Канальный Resolve/Unlisted scope, playlists и ограничения discovery — в профиле.

[Easy English Routine](easy_english_routine/README.md) — исследовательский проект без YouTube identity, ChannelSpec и production runtime.

Общие brand assets и provenance — [BRAND_ASSETS](BRAND_ASSETS.md). Канальный профиль не подтверждает наличие всех media в checkout.
