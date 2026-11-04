# Роли Paper Detour

TOML задаёт обязанности и границы исполнителя. Процедуры принадлежат [проектным skills](../../.agent/skill-catalog.md), ограничения — [корневому](../../AGENTS.md) и [канальному AGENTS.md](../../channels/paper_detour/AGENTS.md). Наличие роли не запускает агента и не разрешает делегирование. Сначала личный проход координатора в Chrome Extra High; затем только отдельно разрешённая задача. Если пользователь поручил разработку ChatGPT.com, субагент её не подменяет.

При допустимом назначении проверить текущую схему инструмента. Если `agent_type` предлагает нужную роль, выбрать её явно; имя `task_name` роль не загружает. Если такой возможности нет, передать путь TOML и потребовать прочитать его инструкции в пределах действующих более высоких правил. Не утверждать автоматическую загрузку без проверки. Число слотов брать из текущего runtime, не из этого README.

| Роль / TOML | Ответственность | Основной workflow |
|---|---|---|
| [paper_researcher](paper_researcher.toml) | Источники и проверяемые утверждения | ytv-paper-production |
| [paper_writer](paper_writer.toml) | Принятый сценарный текст | ytv-paper-production |
| [paper_fact_checker](paper_fact_checker.toml) | Отдельная проверка утверждений | ytv-paper-production |
| [paper_director](paper_director.toml) | Действие, причинность, ритм | ytv-paper-storyboard |
| [paper_visual_director](paper_visual_director.toml) | Смысловая партитура цельных кадров | ytv-paper-storyboard |
| [paper_cinematographer](paper_cinematographer.toml) | Композиции, ракурсы, свет | ytv-paper-storyboard |
| [paper_motion_designer](paper_motion_designer.toml) | Монтажный ритм цельных кадров | ytv-paper-storyboard |
| [paper_art_director](paper_art_director.toml) | Единый бумажный мир и непрерывность | ytv-paper-images |
| [paper_artist](paper_artist.toml) | Готовые цельные картинки | ytv-paper-images |
| [paper_quality_reviewer](paper_quality_reviewer.toml) | Отдельная визуальная проверка | ytv-paper-images |
| [paper_editor](paper_editor.toml) | Исполнение принятых правок через FFmpeg | ytv-video-production |
| [paper_sound_designer](paper_sound_designer.toml) | Авторизованное аудио и микс | ytv-audio-delivery |
| [paper_av_reviewer](paper_av_reviewer.toml) | Отдельная проверка готового файла и синхрона | ytv-audio-delivery |
| [paper_publisher_analyst](paper_publisher_analyst.toml) | Разрешённые выпуск, метаданные и аналитика | ytv-youtube-release |

При передаче указать конкретные входы, файлы/таймлайн во владении, результат и критерии проверки. Не откатывать чужие изменения. Один writer на общий изменяемый монтажный план или output; непересекающиеся задачи используют отдельные work/output-пути.

Автор не становится независимым проверяющим после смены роли. Если независимая проверка не выполнена, записать это явно. Стадии, статусы и шаблон передачи — в [production skill](../../.agents/skills/ytv-paper-production/SKILL.md). Модель, permissions и глобальные настройки эти роли не меняют.
