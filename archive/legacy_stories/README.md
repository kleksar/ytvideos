# Stories

- [Архитектура историй](docs/PROJECT_ARCHITECTURE.md) — типы выпусков, нумерация, границы проектов Palmier и структура хранения материалов.
- [Поиск и производство исторических выпусков](../../channels/nuviko_history/docs/HISTORY_STORY_PIPELINE.md) — исследование в несколько проходов, работа с ChatGPT в Chrome и путь от идеи до фильма, Shorts и YouTube.
- [Рабочий стандарт коротких историй v1](../../channels/nuviko_stories/docs/story-shorts-v1/README.md) — процесс, титры, измеренный референс ролика № 1, журнал решений и сохранённые исходники финального слоя.
- `footages/` — исходные видео.
- `videos/NNN_<slug>/` — постоянные исходники и материалы соответствующей истории; например, `videos/002_pompeii/`.
- Выпуски: `001_brother_ex_best_friend`, `002_pompeii`, `003_gus`; историческая серия к фильму 002 — [первый Shorts 004](../../channels/nuviko_history/videos/004_pompeii_short/README.md) и последующие [005](videos/005_pompeii_short2/README.md), [006](videos/006_pompeii_short3/README.md), [007](videos/007_pompeii_short4/README.md), [008](videos/008_pompeii_short5/README.md). Актуальные результаты и график — в README каждого выпуска. Другие выпуски: [009 — Black Death](../../channels/nuviko_history/videos/009_black_death/README.md) и [010 — Pfeilstorch](videos/010_pfeilstorch/README.md); их состояние и настройки не следует переносить на серию Помпей. Прежние пути `videos/1`, `videos/2`, `videos/003` сохранены как совместимые ссылки на эти каталоги для существующих обращений к медиа.
- `videos/001_brother_ex_best_friend/1.palmier` — живой проект Palmier Pro; его содержимое не редактировать вручную. Не класть файлы внутрь `.palmier`; редактировать проект только через Palmier.
- Не хранить исходники отдельных выпусков в корне `ytvideos/`: все материалы принадлежат `archive/legacy_stories/videos/NNN_<slug>/`. Прежние 43 PNG из `ytvideos/long_story/` архивированы в `videos/002_pompeii/Source/Archive/long_story/`; они не относятся к видеоряду Помпей и не используются в активном таймлайне.

Документация обновлена 28 октября 2026 года. Для нового выпуска использовать правила как отправную точку, а не копировать тайминги и текст текущего ролика.
