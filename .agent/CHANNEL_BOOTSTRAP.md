# Выбор входа и канала

Использовать [ytv-start](../.agents/skills/ytv-start/SKILL.md). Новый запрос создаётся через `create`; ID выделяет приложение, существующий bundle не нужен. `resume`/`import-legacy` относятся только к уже существующей работе и требуют её фактических inputs/evidence.

Явный канал/существующий run имеет приоритет; default нового запроса — Paper Detour. Заморозка Nuviko History и идентичности архива/нового «Нувико» сохраняются. Профили — `channels/<id>/channel.json` и `PROFILE.md`; workflow общий.

Получить `next`/`context` и прочитать названный skill. Не создавать symlinks в каждом эпизоде и не читать неизвестные личные/архивные drafts ради обнаружения skills. Нужные tools/capabilities проверить через `doctor`, продолжая независимые этапы.
